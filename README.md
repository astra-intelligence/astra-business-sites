# Astra Business Sites

Subdomain landing pages for Astra Intelligence Labs subsidiary businesses.

## Structure

```
├── thesights/        → thesights.astraintelligence.co
│   └── index.html    Cryptid, dragon & paranormal sticker shop
├── holdquarter/      → holdquarter.astraintelligence.co
│   └── index.html    Automated quarterly tax withholding
├── server.js          Express host-header router
├── package.json
└── render.yaml        Render deployment config
```

## Deployment

### Option 1: Render (recommended)

1. Create a new GitHub repo: `astra-intelligence/astra-business-sites`
2. Push these files
3. In Render Dashboard → New Web Service → Connect your repo
4. The `render.yaml` auto-configures the service
5. Add custom domains in Render:
   - `thesights.astraintelligence.co`
   - `holdquarter.astraintelligence.co`
6. Add CNAME records in Spaceship DNS:
   - `thesights` → `your-render-service.onrender.com`
   - `holdquarter` → `your-render-service.onrender.com`

### Option 2: Static hosting (GitHub Pages, Vercel, Netlify)

Each site is pure static HTML/CSS. Can be hosted as two separate static sites:

- `thesights.astraintelligence.co` → deploy `/thesights/` as root
- `holdquarter.astraintelligence.co` → deploy `/holdquarter/` as root

## Local Dev

```bash
npm install
npm start
# Server on http://localhost:4444
```

## DNS Configuration (Spaceship)

In the Spaceship DNS dashboard for astraintelligence.co:

```
thesights    CNAME    your-render-service.onrender.com
holdquarter  CNAME    your-render-service.onrender.com
```

Or if using separate services:

```
thesights    CNAME    thesights-site.onrender.com
holdquarter  CNAME    holdquarter-site.onrender.com
```
