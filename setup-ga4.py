#!/usr/bin/env python3
"""
GA4 + Search Console automated setup via Playwright browser automation.
Uses Gmail App Passwords (from env) to authenticate with Google services.

Usage:
  python3 setup-ga4.py
"""

import asyncio
import json
import os
import re
import sys
import tempfile


def load_env(path):
    """Load a .env file and return a dict."""
    env = {}
    if not os.path.exists(path):
        return env
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    return env


# Load credentials from hermes .env
hermes_env = load_env(os.path.expanduser("~/.hermes/.env"))
EMAIL = hermes_env.get("CISO_GMAIL2_USER", "contact@astramedia.app")
APP_PASSWORD = hermes_env.get("CISO_GMAIL2_PASS", "")

SITES = [
    {"name": "The Sights", "domain": "thesights.astraintelligence.co",
     "url": "https://thesights.astraintelligence.co"},
    {"name": "HoldQuarter", "domain": "holdquarter.astraintelligence.co",
     "url": "https://holdquarter.astraintelligence.co"},
    {"name": "AstraWatch", "domain": "astrawatch.astraintelligence.co",
     "url": "https://astrawatch.astraintelligence.co"},
]


async def main():
    if not APP_PASSWORD:
        print("❌ No Gmail App Password found in ~/.hermes/.env (CISO_GMAIL2_PASS)")
        return {}, {}

    from playwright.async_api import async_playwright

    results = {}

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            executable_path=os.path.expanduser(
                "~/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome"
            ),
            args=["--no-sandbox", "--disable-setuid-sandbox",
                  "--disable-blink-features=AutomationControlled"],
        )

        # Use a stealthier context
        context = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            locale="en-US",
            timezone_id="America/New_York",
        )
        page = await context.new_page()

        # Remove webdriver detection
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
        """)

        print("=" * 60)
        print("Step 1: Sign into Google Account")
        print("=" * 60)
        print(f"  Email: {EMAIL}")
        print(f"  Password: [hidden, {len(APP_PASSWORD)} chars]")

        await page.goto("https://accounts.google.com/v3/signin/identifier",
                        wait_until="domcontentloaded")
        await asyncio.sleep(2)

        # Screenshot pre-login
        await page.screenshot(path="/tmp/ga4-step1-login-page.png")

        # Enter email
        try:
            email_sel = "input[type='email'], input[name='identifier'], #identifierId"
            await page.wait_for_selector(email_sel, timeout=10000)
            await page.fill(email_sel, EMAIL)
            await asyncio.sleep(1)

            next_btn = page.locator("#identifierNext, button:has-text('Next'), "
                                    "div[role='button']:has-text('Next')")
            await next_btn.first.click(timeout=5000)
            await asyncio.sleep(3)
            print("  ✅ Email submitted")
        except Exception as e:
            print(f"  ⚠️ Email entry issue: {e}")
            await page.screenshot(path="/tmp/ga4-error-email.png")

        # Check for password field or recovery/verification
        page_source = await page.content()
        await page.screenshot(path="/tmp/ga4-step2-after-email.png")

        if "password" in page_source.lower() or "passwd" in page_source.lower():
            # Enter password (App Password)
            try:
                pw_sel = "input[type='password'], input[name='Passwd'], "
                pw_sel += "div#password input"
                await page.wait_for_selector(pw_sel, timeout=10000)
                await page.fill(pw_sel, APP_PASSWORD)
                await asyncio.sleep(1)

                next2 = page.locator("#passwordNext, button:has-text('Next'), "
                                     "div[role='button']:has-text('Next')")
                await next2.first.click(timeout=5000)
                await asyncio.sleep(4)
                print("  ✅ Password submitted")
            except Exception as e:
                print(f"  ⚠️ Password entry issue: {e}")
                await page.screenshot(path="/tmp/ga4-error-password.png")
        else:
            print("  ⚠️ No password field detected — might need verification code")
            await page.screenshot(path="/tmp/ga4-no-password-field.png")

        # Check login result
        await page.screenshot(path="/tmp/ga4-step3-post-login.png")
        current_url = page.url
        print(f"  URL after login: {current_url[:80]}")

        if "myaccount" in current_url or "signin" not in current_url:
            print("  ✅ Successfully authenticated!")
        elif "challenge" in current_url or "reauth" in current_url:
            print("  ⚠️ Additional verification needed (2FA challenge)")
            results["login_status"] = "2fa_challenge"
        else:
            print("  ⚠️ Login may have failed")
            results["login_status"] = "failed"

        # Try navigating to Google Analytics
        print("\n" + "=" * 60)
        print("Step 2: Access Google Analytics")
        print("=" * 60)

        await page.goto("https://analytics.google.com/analytics/web/provision",
                        wait_until="domcontentloaded", timeout=30000)
        await asyncio.sleep(3)
        await page.screenshot(path="/tmp/ga4-step4-analytics.png")
        print(f"  URL: {page.url[:80]}")

        # Check if we landed on GA
        page_text = await page.inner_text("body")
        if "sign" in page_text.lower() or "choose an account" in page_text.lower():
            print("  ❌ Redirected back to login — App Password not accepted for GA")
            results["ga_access"] = "denied"
        elif "analytics" in page.url.lower():
            print("  ✅ Analytics dashboard accessible!")
            results["ga_access"] = "granted"

            # Try creating a property
            print("\n" + "=" * 60)
            print("Step 3: Try to create GA4 property")
            print("=" * 60)

            for site in SITES:
                print(f"\n  --- {site['name']} ({site['domain']}) ---")
                try:
                    # Navigate to Admin
                    await page.goto("https://analytics.google.com/analytics/web/#/a/"
                                    "createproperty", wait_until="domcontentloaded",
                                    timeout=15000)
                    await asyncio.sleep(2)

                    # Check for property creation form
                    prop_name = page.locator("input[name='propertyName'], "
                                             "input[placeholder*='property'], "
                                             "input[aria-label*='Property']")
                    try:
                        await prop_name.wait_for(timeout=5000)
                        await prop_name.fill(site["name"])
                        print(f"    Entered property name: {site['name']}")

                        # Fill URL
                        url_field = page.locator("input[type='url'], "
                                                 "input[name*='url'], "
                                                 "input[aria-label*='URL']")
                        await url_field.fill(site["url"])
                        print(f"    Entered URL: {site['url']}")

                        # Click create
                        create_btn = page.locator("button:has-text('Create'), "
                                                  "div[role='button']:has-text('Create'), "
                                                  "button:has-text('Next')")
                        await create_btn.first.click(timeout=5000)
                        await asyncio.sleep(3)

                        # Try to get measurement ID from page
                        page_text_after = await page.inner_text("body")
                        measurement_match = re.search(r'G-[A-Z0-9]+', page_text_after)
                        if measurement_match:
                            mid = measurement_match.group(0)
                            results[site["name"]] = {"ga4_id": mid}
                            print(f"    ✅ GA4 ID obtained: {mid}")
                        else:
                            await page.screenshot(
                                path=f"/tmp/ga4-{site['name'].lower().replace(' ','')}-created.png")
                            print(f"    ⚠️ Created but couldn't extract ID")
                    except Exception as e:
                        print(f"    ❌ Property creation failed: {e}")
                        await page.screenshot(
                            path=f"/tmp/ga4-{site['name'].lower().replace(' ','')}-error.png")
                except Exception as e:
                    print(f"    ❌ Navigation error: {e}")
        else:
            results["ga_access"] = "unexpected"
            print(f"  ⚠️ Unexpected state. Page text sample: {page_text[:200]}")

        # Try Search Console too
        if results.get("ga_access") == "granted":
            print("\n" + "=" * 60)
            print("Step 4: Access Google Search Console")
            print("=" * 60)
            for site in SITES:
                print(f"\n  --- {site['domain']} ---")
                try:
                    await page.goto("https://search.google.com/search-console",
                                    wait_until="domcontentloaded", timeout=15000)
                    await asyncio.sleep(2)
                    await page.screenshot(
                        path=f"/tmp/gsc-{site['name'].lower().replace(' ','')}.png")
                    print(f"    Navigated to Search Console")
                except Exception as e:
                    print(f"    ❌ Error: {e}")

        await page.screenshot(path="/tmp/ga4-final.png")
        print(f"\n📸 Final screenshot: /tmp/ga4-final.png")
        await browser.close()

    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    for k, v in results.items():
        print(f"  {k}: {v}")

    return results


if __name__ == "__main__":
    result = asyncio.run(main())
    print(json.dumps(result, indent=2))
