# CMS Module - Quick Start

## 🚀 Get Running in 5 Minutes

### 1. Install & Build (2 min)
```bash
cd /home/jumes/bench/apps/syncedoffice/syncedoffice/so_cms/cms_app
npm install
npm run build
```

### 2. Migrate & Cache (1 min)
```bash
cd /home/jumes/bench
bench --site syncedoffice.localhost migrate
bench --site syncedoffice.localhost clear-cache
bench restart
```

### 3. Access (Now!)
**Navigate to:** http://syncedoffice.localhost:8002/cms/

---

## 📝 Create Your First Content Type

1. Click **"Create Content Type"**
2. Enter name: `Blog`
3. Click field types to add:
   - **Text** → Name it `title` (required)
   - **Rich Text** → Name it `content` (required)
   - **Media** → Name it `featured_image`
   - **Date** → Name it `published_date`
4. Drag fields to reorder
5. Click **"Create"**

Done! You now have a Blog content type.

---

## 🎨 What You Can Do

### Content Type Builder
- ✅ Create collection types (multiple entries)
- ✅ Create single types (one entry)
- ✅ Add 18 different field types
- ✅ Drag-and-drop to reorder fields
- ✅ Configure validation rules
- ✅ Set required/unique fields

### Field Types Available
- **Basic**: Text, Long Text, Rich Text, Number, Boolean
- **Date**: Date, DateTime, Time
- **Advanced**: Email, URL, UID, Enumeration, JSON
- **Media**: File/Image upload
- **Relational**: Relation, Component, Dynamic Zone

---

## 🔧 Common Commands

```bash
# Build frontend
cd cms_app && npm run build

# Dev mode (hot reload)
cd cms_app && npm run dev

# Migrate database
bench --site syncedoffice.localhost migrate

# Clear cache
bench --site syncedoffice.localhost clear-cache

# Restart bench
bench restart

# Console
bench --site syncedoffice.localhost console

# Create sample data
bench --site syncedoffice.localhost console
>>> from syncedoffice.so_cms.fixtures.sample_content_types import create_sample_content_types
>>> create_sample_content_types()
```

---

## 🐛 Troubleshooting

### App not loading?
```bash
npm run build
bench --site syncedoffice.localhost clear-cache
bench restart
```

### API errors?
- Check you're logged in to Frappe
- Verify bench is running: `bench start`

### Build fails?
```bash
rm -rf node_modules package-lock.json
npm install
npm run build
```

---

## 📚 Documentation

- **Full Setup**: `SETUP_GUIDE.md`
- **Backend Details**: `PHASE_1_COMPLETE.md`
- **Frontend Details**: `PHASE_2_COMPLETE.md`
- **Project Overview**: `PROJECT_SUMMARY.md`
- **Vue App**: `cms_app/README.md`

---

## 🎯 Next Steps

1. ✅ Create content types
2. ⏳ Build content manager (Phase 3)
3. ⏳ Add media library
4. ⏳ Implement i18n
5. ⏳ Add permissions UI

---

## 📞 Need Help?

Check the detailed guides:
- Installation issues → `SETUP_GUIDE.md`
- Understanding the code → `PHASE_1_COMPLETE.md` & `PHASE_2_COMPLETE.md`
- API usage → `README.md`

---

**You're all set! Start building your content types! 🎉**
