# AstraWatch Landing Page

## Two Deploy Options

### Option A: Netlify (Static — already configured)
- Directory: `/home/paperclip/astrawatch-landing/`
- Netlify site ID: `e772a94d-7541-49e8-89a1-62e03c61b7c3`
- Uses Netlify Forms for waitlist submissions
- Deploy: `npx netlify-cli deploy --dir=. --prod` (needs auth)

### Option B: Render (Node.js server — preferred)
- Directory: `/home/paperclip/astrawatch-server/`
- Includes Express server with waitlist API (`/api/waitlist`)
- Stores submissions to `data/waitlist.json`
- Health check at `/health`
- Form fallback: tries server API first, then Netlify Forms

## Render Setup
1. Create a **Web Service** on Render
2. Connect to `astra-business-sites` repo or deploy the `astrawatch-server/` directory
3. Build command: `cd astrawatch-server && npm install`
4. Start command: `cd astrawatch-server && node server.js`
5. Env var (optional): `ASTRAWATCH_DATA_DIR` to customize data storage path
6. Assign custom domain: `astrawatch.astraintelligence.co`

## DNS
Add CNAME record:
- `astrawatch.astraintelligence.co` → Render service URL or `mellifluous-salmiakki-8bf0ed.netlify.app`
