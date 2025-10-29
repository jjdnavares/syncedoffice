# CMS Asset Loading System

## Overview

The CMS uses a dynamic asset loading system that automatically reads the Vite build manifest to load the correct CSS and JS files, even when their filenames change due to content hashing.

## How It Works

### 1. Build Process

When you run `npm run build` in the `cms_app` directory:
- Vite generates hashed filenames for cache busting (e.g., `index-D7a-dS_-.css`)
- A manifest file is created at `public/js/cms/.vite/manifest.json`
- The manifest maps entry points to their actual built filenames

### 2. Python Helper (`so_cms/utils.py`)

The `get_cms_assets()` function:
- Reads the Vite manifest JSON file
- Extracts CSS and JS file paths for the main entry point
- Returns absolute URLs with the correct base path
- Handles errors gracefully with fallback values

### 3. Template Context (`www/cms.py`)

The `get_context()` function:
- Calls `get_cms_assets()` to get current asset paths
- Adds `cms_css` and `cms_js` to the template context
- These variables are available in the Jinja template

### 4. HTML Template (`www/cms.html`)

The template uses Jinja to:
- Loop through CSS files: `{% for css_file in cms_css %}`
- Load the JS file: `{{ cms_js }}`
- Add cache-busting query parameters with timestamps

## Benefits

1. **No manual updates needed** - Asset paths update automatically after rebuild
2. **Cache busting** - Hashed filenames ensure browsers load new versions
3. **Error handling** - Falls back to default paths if manifest is missing
4. **Future-proof** - Works with any Vite configuration changes

## Rebuilding Frontend

When you rebuild the CMS frontend:

```bash
cd /home/jumes/bench/apps/syncedoffice/syncedoffice/so_cms/cms_app
npm run build
```

The system automatically:
1. Generates new hashed filenames
2. Updates the manifest
3. Serves the new files on next page load

No code changes required!

## Troubleshooting

### CSS not loading
- Check if manifest exists: `ls public/js/cms/.vite/manifest.json`
- Verify CSS files exist: `ls public/js/cms/assets/*.css`
- Check Frappe logs for errors from `get_cms_assets()`

### Wrong files loading
- Clear browser cache (Ctrl+Shift+R)
- Restart bench: `bench restart`
- Rebuild frontend: `npm run build`

## File Locations

- **Manifest**: `syncedoffice/public/js/cms/.vite/manifest.json`
- **CSS**: `syncedoffice/public/js/cms/assets/*.css`
- **JS**: `syncedoffice/public/js/cms/cms-app.js`
- **Helper**: `syncedoffice/so_cms/utils.py`
- **Context**: `syncedoffice/www/cms.py`
- **Template**: `syncedoffice/www/cms.html`
