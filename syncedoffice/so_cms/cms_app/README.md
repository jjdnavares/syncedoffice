# CMS Vue Frontend

Modern Vue 3 frontend for the SyncedOffice CMS module.

## Features

- ✅ Content Type Builder with drag-and-drop
- ✅ 18 field types supported
- ✅ Field configuration with validation
- ✅ Responsive design with Tailwind CSS
- ✅ Real-time updates with Pinia store
- ✅ Icon support with Lucide icons

## Setup

### 1. Install Dependencies

```bash
cd /home/jumes/bench/apps/syncedoffice/syncedoffice/so_cms/cms_app
npm install
```

### 2. Development Mode

```bash
npm run dev
```

This will start the Vite dev server on `http://localhost:8081` with hot module replacement.

### 3. Build for Production

```bash
npm run build
```

This will build the app and output to `../public/js/cms/` which is served by Frappe.

## Project Structure

```
cms_app/
├── src/
│   ├── components/       # Reusable Vue components
│   │   ├── BaseButton.vue
│   │   ├── BaseInput.vue
│   │   ├── BaseSelect.vue
│   │   ├── ConfirmDialog.vue
│   │   ├── ContentTypeCard.vue
│   │   ├── FieldBuilder.vue
│   │   ├── FieldConfigModal.vue
│   │   └── FieldItem.vue
│   ├── layouts/          # Layout components
│   │   └── MainLayout.vue
│   ├── views/            # Page components
│   │   ├── ContentTypeList.vue
│   │   ├── ContentTypeEditor.vue
│   │   └── ComponentList.vue
│   ├── stores/           # Pinia stores
│   │   └── contentTypeStore.js
│   ├── router/           # Vue Router config
│   │   └── index.js
│   ├── utils/            # Utilities
│   │   ├── api.js
│   │   └── fieldTypes.js
│   ├── App.vue
│   ├── main.js
│   └── style.css
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
└── postcss.config.js
```

## Tech Stack

- **Vue 3** - Progressive JavaScript framework
- **Vite** - Next generation frontend tooling
- **Pinia** - State management
- **Vue Router** - Official router
- **Tailwind CSS** - Utility-first CSS framework
- **Lucide Vue** - Beautiful icon library
- **VueDraggable** - Drag and drop functionality

## Development Workflow

1. **Start Frappe bench** (in one terminal):
   ```bash
   cd /home/jumes/bench
   bench start
   ```

2. **Start Vue dev server** (in another terminal):
   ```bash
   cd /home/jumes/bench/apps/syncedoffice/syncedoffice/so_cms/cms_app
   npm run dev
   ```

3. **Access the app**:
   - Dev mode: `http://localhost:8081/cms/`
   - Production: `http://syncedoffice.localhost:8002/cms/`

## Building for Production

When you're ready to deploy:

```bash
# Build the app
npm run build

# Clear Frappe cache
cd /home/jumes/bench
bench --site syncedoffice.localhost clear-cache

# Restart bench
bench restart
```

The built files will be in `../public/js/cms/` and will be served by Frappe.

## API Integration

The app uses the Frappe API utility (`src/utils/api.js`) to communicate with the backend:

```javascript
import { api } from '@/utils/api'

// Call a whitelisted method
const response = await api.call('syncedoffice.so_cms.api.content_type.get_content_types')
```

All API calls automatically include:
- CSRF token from cookies
- Proper headers
- Error handling

## Field Types

The following field types are supported:

### Basic
- Text, Long Text, Rich Text
- Number, Decimal
- Boolean

### Date & Time
- Date, DateTime, Time

### Advanced
- Email, URL, UID
- Enumeration, JSON

### Media
- Media (File/Image upload)

### Relational
- Relation (Link to other content)
- Component (Reusable field groups)
- Dynamic Zone (Flexible content blocks)

## Customization

### Adding New Field Types

1. Add to `src/utils/fieldTypes.js`:
   ```javascript
   {
     type: 'MyFieldType',
     label: 'My Field Type',
     icon: 'icon-name',
     category: 'Basic',
     description: 'Description',
   }
   ```

2. Update backend DocType field options

### Styling

The app uses Tailwind CSS. Customize colors in `tailwind.config.js`:

```javascript
theme: {
  extend: {
    colors: {
      primary: {
        // Your colors
      },
    },
  },
}
```

## Troubleshooting

### Build fails
- Check Node.js version (should be 18+)
- Delete `node_modules` and run `npm install` again

### API calls fail
- Ensure Frappe bench is running
- Check CSRF token in browser cookies
- Verify API endpoints are whitelisted

### Styles not loading
- Run `npm run build` after CSS changes
- Clear browser cache
- Clear Frappe cache: `bench --site syncedoffice.localhost clear-cache`

## License

MIT
