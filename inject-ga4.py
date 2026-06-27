#!/usr/bin/env python3
"""
GA4 Injection Script — injects Google Analytics 4 + Google Site Verification 
into static HTML files for all venture sites.

Usage:
  python3 inject-ga4.py --site thesights --measurement-id G-XXXXXXXX --verification-token abc123
  python3 inject-ga4.py --site holdquarter --measurement-id G-XXXXXXXX --verification-token abc123
  python3 inject-ga4.py --site thesights --dry-run
"""

import argparse
import os
import re
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SITES = {
    'thesights': {
        'path': os.path.join(BASE_DIR, 'thesights', 'index.html'),
        'domain': 'thesights.astraintelligence.co',
        'name': 'The Sights',
    },
    'holdquarter': {
        'path': os.path.join(BASE_DIR, 'holdquarter', 'index.html'),
        'domain': 'holdquarter.astraintelligence.co',
        'name': 'HoldQuarter',
    },
    'astrawatch': {
        'path': os.path.join(BASE_DIR, 'astrawatch', 'index.html'),
        'domain': 'astrawatch.astraintelligence.co',
        'name': 'AstraWatch',
    },
}

GA4_SNIPPET = """  <!-- Google Analytics (GA4) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={measurement_id}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', '{measurement_id}');
  </script>"""

VERIFICATION_META = """  <meta name="google-site-verification" content="{verification_token}" />"""


def inject_ga4(html_content, measurement_id):
    """Inject GA4 gtag snippet before </head>."""
    snippet = GA4_SNIPPET.format(measurement_id=measurement_id)
    if 'gtag/js?id=' in html_content:
        old_id = re.search(r'gtag/js\?id=([A-Z0-9-]+)', html_content)
        old_id = old_id.group(1) if old_id else 'unknown'
        print(f"  [SKIP] GA4 already injected (current ID: {old_id})")
        return html_content
    result = html_content.replace('</head>', f'{snippet}\n</head>')
    print(f"  [INJECT] GA4 measurement ID: {measurement_id}")
    return result


def inject_verification(html_content, verification_token):
    """Inject Google Site Verification meta tag before </head>."""
    meta = VERIFICATION_META.format(verification_token=verification_token)
    if verification_token in html_content:
        print(f"  [SKIP] Site verification already present")
        return html_content
    result = html_content.replace('</head>', f'{meta}\n</head>')
    print(f"  [INJECT] Site verification token: {verification_token}")
    return result


def main():
    parser = argparse.ArgumentParser(description='Inject GA4 + Google Site Verification')
    parser.add_argument('--site', required=True, choices=list(SITES.keys()) + ['all'],
                        help='Site to inject (or "all")')
    parser.add_argument('--measurement-id', help='GA4 Measurement ID (e.g., G-XXXXXXXX)')
    parser.add_argument('--verification-token', help='Google Site Verification token')
    parser.add_argument('--dry-run', action='store_true',
                        help='Show what would be injected without modifying files')
    parser.add_argument('--backup', action='store_true',
                        help='Create .bak backup before modifying')
    args = parser.parse_args()

    if args.dry_run and not args.measurement_id and not args.verification_token:
        # Show current state
        for name, site in SITES.items():
            with open(site['path']) as f:
                content = f.read()
            has_ga4 = 'gtag/js?id=' in content
            has_verification = 'google-site-verification' in content
            sep_line = "\n" + site['name'] + " (" + site['domain'] + "):"
            print(sep_line)
            if has_ga4:
                match = re.search(r'gtag/js\?id=([A-Z0-9-]+)', content)
                gaid = match.group(1) if match else 'unknown'
                print(f"  GA4: ✅ (ID: {gaid})")
            else:
                print("  GA4: ❌ (not configured)")
            print(f"  Site Verification: {'✅' if has_verification else '❌'}")
        return

    sites_to_process = [SITES[s] for s in (list(SITES.keys()) if args.site == 'all' else [args.site])]

    for site in sites_to_process:
        print(f"\nProcessing {site['name']} ({site['domain']})...")
        
        with open(site['path']) as f:
            content = f.read()
        
        if args.backup:
            backup_path = site['path'] + '.bak'
            shutil.copy2(site['path'], backup_path)
            print(f"  [BACKUP] Created {backup_path}")
        
        if args.measurement_id:
            content = inject_ga4(content, args.measurement_id)
        
        if args.verification_token:
            content = inject_verification(content, args.verification_token)
        
        if not args.dry_run:
            with open(site['path'], 'w') as f:
                f.write(content)
            print(f"  [DONE] Updated {site['path']}")
        else:
            print(f"  [DRY RUN] No changes written")


if __name__ == '__main__':
    main()
