# CMS Module - Complete Setup Guide

## Quick Start

Follow these steps to get the CMS module running:

### 1. Install Frontend Dependencies

```bash
cd /home/jumes/bench/apps/syncedoffice/syncedoffice/so_cms/cms_app
npm install
```

### 2. Build the Frontend

```bash
npm run build
```

### 3. Migrate Database (if not done)

```bash
cd /home/jumes/bench
bench --site syncedoffice.localhost migrate
```

### 4. Clear Cache & Restart

```bash
bench --site syncedoffice.localhost clear-cache
bench restart
```

### 5. Access the CMS

Navigate to: **http://syncedoffice.localhost:8002/cms/**

---

## Detailed Setup

### Prerequisites

- ✅ Frappe Framework installed
- ✅ SyncedOffice app installed
- ✅ Node.js 18+ installed
- ✅ npm or yarn installed

### Step-by-Step Installation

#### 1. Backend Setup (Already Complete)

The backend was created in Phase 1:
- 6 DocTypes created
- Backend services implemented
- API endpoints configured

#### 2. Frontend Setup

```bash
# Navigate to Vue app directory
cd /home/jumes/bench/apps/syncedoffice/syncedoffice/so_cms/cms_app

# Install dependencies (first time only)
npm install

# Build for production
npm run build
```

**What this does:**
- Installs Vue 3, Tailwind CSS, and all dependencies
- Builds the Vue app
- Outputs to `../public/js/cms/` for Frappe to serve

#### 3. Database Migration

```bash
cd /home/jumes/bench

# Migrate to create DocTypes
bench --site syncedoffice.localhost migrate

# Clear cache
bench --site syncedoffice.localhost clear-cache
```

#### 4. Create Sample Data (Optional)

```bash
bench --site syncedoffice.localhost console

# In the console:
from syncedoffice.so_cms.fixtures.sample_content_types import create_sample_content_types
create_sample_content_types()
exit()
```

This creates 3 sample content types:
- **Blog** - Collection type for blog posts
- **Product** - Collection type for products
- **Homepage** - Single type for homepage content

#### 5. Start/Restart Bench

```bash
# If bench is not running
bench start

# If bench is already running
bench restart
```

---

## Development Workflow

### Option 1: Production Mode (Recommended for Testing)

```bash
# Build the app
cd /home/jumes/bench/apps/syncedoffice/syncedoffice/so_cms/cms_app
npm run build

# Clear cache
cd /home/jumes/bench
bench --site syncedoffice.localhost clear-cache

# Access at http://syncedoffice.localhost:8002/cms/
```

### Option 2: Development Mode (Hot Reload)

```bash
# Terminal 1: Start Frappe
cd /home/jumes/bench
bench start

# Terminal 2: Start Vue dev server
cd /home/jumes/bench/apps/syncedoffice/syncedoffice/so_cms/cms_app
npm run dev

# Access at http://localhost:8081/cms/
```

**Development mode benefits:**
- Hot module replacement (instant updates)
- Better error messages
- Source maps for debugging

---

## Verification Steps

### 1. Check Backend

```bash
bench --site syncedoffice.localhost console

# Test API
import frappe
from syncedoffice.so_cms.api import content_type

# Get content types
result = content_type.get_content_types()
print(result)
```

### 2. Check Frontend

1. Navigate to `http://syncedoffice.localhost:8002/cms/`
2. You should see the CMS interface
3. Click "Create Content Type"
4. Add fields using drag-and-drop
5. Save and verify

### 3. Check Built Files

```bash
ls -la /home/jumes/bench/apps/syncedoffice/syncedoffice/so_cms/public/js/cms/

# Should see:
# - cms-app.js
# - chunks/
# - assets/
```

---

## Troubleshooting

### Issue: "npm: command not found"

**Solution:** Install Node.js
```bash
# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify
node --version  # Should be 18+
npm --version
```

### Issue: Build fails with dependency errors

**Solution:** Clean install
```bash
cd /home/jumes/bench/apps/syncedoffice/syncedoffice/so_cms/cms_app
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Issue: CMS page shows 404

**Solution:** Check route configuration
```bash
# Verify hooks.py has the route
grep -A 2 "website_route_rules" /home/jumes/bench/apps/syncedoffice/syncedoffice/hooks.py

# Should show:
# website_route_rules = [
#   {'from_route': '/cms/<path:app_path>', 'to_route': 'cms'},
# ]

# Clear cache
bench --site syncedoffice.localhost clear-cache
bench restart
```

### Issue: App loads but shows blank page

**Solution:** Check browser console
1. Open browser DevTools (F12)
2. Check Console tab for errors
3. Check Network tab for failed requests

Common fixes:
```bash
# Rebuild
cd /home/jumes/bench/apps/syncedoffice/syncedoffice/so_cms/cms_app
npm run build

# Clear all caches
cd /home/jumes/bench
bench --site syncedoffice.localhost clear-cache
bench --site syncedoffice.localhost clear-website-cache

# Restart
bench restart
```

### Issue: API calls fail (401/403 errors)

**Solution:** Check authentication
1. Ensure you're logged into Frappe
2. Check CSRF token in cookies
3. Verify API endpoints are whitelisted

```bash
# Test in console
bench --site syncedoffice.localhost console

import frappe
frappe.set_user("Administrator")
from syncedoffice.so_cms.api import content_type
result = content_type.get_content_types()
print(result)
```

### Issue: Styles not loading

**Solution:** Rebuild with Tailwind
```bash
cd /home/jumes/bench/apps/syncedoffice/syncedoffice/so_cms/cms_app

# Check Tailwind is installed
npm list tailwindcss

# Rebuild
npm run build

# Clear browser cache (Ctrl+Shift+R)
```

### Issue: Drag-and-drop not working

**Solution:** Check VueDraggable
```bash
cd /home/jumes/bench/apps/syncedoffice/syncedoffice/so_cms/cms_app

# Verify installation
npm list vuedraggable

# Reinstall if needed
npm install vuedraggable@^4.1.0
npm run build
```

---

## File Locations

### Backend Files
```
syncedoffice/so_cms/
├── api/
│   └── content_type.py          # API endpoints
├── doctype/                     # 6 DocTypes
├── services/                    # Backend logic
├── fixtures/                    # Sample data
└── www/
    ├── cms.html                 # Entry point
    └── cms.py                   # Context
```

### Frontend Files
```
syncedoffice/so_cms/cms_app/
├── src/                         # Vue source
├── package.json                 # Dependencies
├── vite.config.js              # Build config
└── tailwind.config.js          # Styles config
```

### Built Files (Auto-generated)
```
syncedoffice/so_cms/public/js/cms/
├── cms-app.js                   # Main bundle
├── chunks/                      # Code-split chunks
└── assets/                      # CSS, images
```

---

## Configuration

### Change Port (Vite Dev Server)

Edit `cms_app/vite.config.js`:
```javascript
server: {
  port: 8081,  // Change this
  proxy: {
    '/api': 'http://localhost:8002',  // Match your Frappe port
  },
}
```

### Customize Colors

Edit `cms_app/tailwind.config.js`:
```javascript
theme: {
  extend: {
    colors: {
      primary: {
        500: '#0ea5e9',  // Change primary color
        600: '#0284c7',
        // ...
      },
    },
  },
}
```

### Add Custom Field Types

1. Edit `cms_app/src/utils/fieldTypes.js`
2. Add to `FIELD_TYPES` array
3. Update backend DocType field options
4. Rebuild: `npm run build`

---

## Performance Tips

### 1. Production Build Optimization

```bash
# Build with optimizations
npm run build

# Check bundle size
ls -lh ../public/js/cms/cms-app.js
```

### 2. Enable Gzip (Nginx)

Add to your nginx config:
```nginx
gzip on;
gzip_types text/css application/javascript;
gzip_min_length 1000;
```

### 3. Browser Caching

The built files include hashes in filenames for cache busting.

---

## Security Checklist

- ✅ All API endpoints require authentication
- ✅ CSRF tokens validated
- ✅ Role-based permissions (System Manager)
- ✅ Input validation on backend
- ✅ XSS protection (Vue escapes by default)
- ✅ SQL injection protection (Frappe ORM)

---

## Maintenance

### Update Dependencies

```bash
cd /home/jumes/bench/apps/syncedoffice/syncedoffice/so_cms/cms_app

# Check for updates
npm outdated

# Update all
npm update

# Rebuild
npm run build
```

### Backup

```bash
# Backup database
bench --site syncedoffice.localhost backup

# Backup files
tar -czf cms_backup.tar.gz /home/jumes/bench/apps/syncedoffice/syncedoffice/so_cms/
```

---

## Next Steps

After setup is complete:

1. **Create your first content type**
   - Navigate to `/cms/content-types`
   - Click "Create Content Type"
   - Add fields and save

2. **Explore the API**
   - Check `/api/method/syncedoffice.so_cms.api.content_type.get_content_types`
   - Use for headless CMS

3. **Customize the UI**
   - Edit Vue components in `cms_app/src/`
   - Modify Tailwind config for branding

4. **Plan Phase 3**
   - Content Manager
   - Media Library
   - Content editing

---

## Support

- **Documentation**: See `README.md` files in each directory
- **Phase 1 Guide**: `PHASE_1_COMPLETE.md`
- **Phase 2 Guide**: `PHASE_2_COMPLETE.md`
- **Vue App Guide**: `cms_app/README.md`

---

## Quick Commands Reference

```bash
# Install
cd cms_app && npm install

# Build
npm run build

# Dev mode
npm run dev

# Migrate
bench --site syncedoffice.localhost migrate

# Clear cache
bench --site syncedoffice.localhost clear-cache

# Restart
bench restart

# Console
bench --site syncedoffice.localhost console

# Logs
tail -f logs/web.error.log
```

---

**Status:** Ready for production use! 🚀
