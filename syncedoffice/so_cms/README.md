# SO CMS Module

A headless CMS module for SyncedOffice, inspired by Strapi.

## Phase 1: Content Type Builder Backend ✅

### DocTypes Created

1. **CMS Content Type** - Main content type definition
   - Fields: content_type_name, display_name, description, kind, api_id, icon, is_published
   - Child table: fields (CMS Content Type Field)

2. **CMS Content Type Field** - Field definitions for content types
   - Fields: field_name, field_label, field_type, required, unique, position, options
   - Supports: Text, Long Text, Rich Text, Number, Date, Boolean, Email, URL, Media, Relation, Component, Dynamic Zone

3. **CMS Component** - Reusable field groups
   - Fields: component_name, display_name, category, icon, description
   - Child table: fields (CMS Component Field)

4. **CMS Component Category** - Organize components
   - Fields: category_name, icon, description

5. **CMS Component Field** - Fields within components
   - Similar to Content Type Field but simplified

6. **CMS Content** - Stores actual content data
   - Fields: content_type, status, locale, content_data (JSON), published_at
   - Tracks: created_by_user, modified_by_user

### Services Created

1. **content_type_service.py**
   - `create_content_type(data)` - Create new content type
   - `update_content_type(name, data)` - Update content type
   - `delete_content_type(name)` - Delete content type
   - `get_content_type(name)` - Get single content type
   - `list_content_types(filters)` - List all content types
   - `validate_content_type_schema(data)` - Validate schema
   - `get_content_type_by_api_id(api_id)` - Get by API ID (with caching)

2. **field_service.py**
   - `add_field(content_type, field_data)` - Add field to content type
   - `update_field(content_type, field_name, data)` - Update field
   - `delete_field(content_type, field_name)` - Delete field
   - `reorder_fields(content_type, field_order)` - Reorder fields
   - `validate_field_config(field_data)` - Validate field configuration

### API Endpoints Created

**File:** `api/content_type.py`

All endpoints are whitelisted and accessible via:
- `/api/method/syncedoffice.so_cms.api.content_type.<method_name>`

**Methods:**
- `get_content_types(filters)` - GET all content types
- `get_content_type(name)` - GET single content type
- `create_content_type(data)` - POST create content type
- `update_content_type(name, data)` - PUT update content type
- `delete_content_type(name)` - DELETE content type
- `add_field(content_type, field_data)` - POST add field
- `update_field(content_type, field_name, data)` - PUT update field
- `delete_field(content_type, field_name)` - DELETE field
- `reorder_fields(content_type, field_order)` - POST reorder fields

### Web Route

- `/cms/` - CMS SPA route (placeholder HTML for now)

## Setup Instructions

### 1. Start Bench (if not running)
```bash
cd /home/jumes/bench
bench start
```

### 2. Migrate Database (in another terminal)
```bash
cd /home/jumes/bench
bench --site syncedoffice.localhost migrate
```

### 3. Clear Cache
```bash
bench --site syncedoffice.localhost clear-cache
```

### 4. Access CMS
Navigate to: `http://syncedoffice.localhost:8002/cms/`

## Testing the API

### Create a Content Type
```python
# In Frappe console: bench --site syncedoffice.localhost console
import frappe
from syncedoffice.so_cms.services import content_type_service

# Create a Blog content type
blog_data = {
    "content_type_name": "Blog",
    "display_name": "Blog Post",
    "description": "Blog posts for the website",
    "kind": "Collection Type",
    "icon": "file-text",
    "fields": [
        {
            "field_name": "title",
            "field_label": "Title",
            "field_type": "Text",
            "required": 1,
            "position": 1
        },
        {
            "field_name": "slug",
            "field_label": "Slug",
            "field_type": "UID",
            "required": 1,
            "unique": 1,
            "position": 2
        },
        {
            "field_name": "content",
            "field_label": "Content",
            "field_type": "Rich Text",
            "required": 1,
            "position": 3
        },
        {
            "field_name": "featured_image",
            "field_label": "Featured Image",
            "field_type": "Media",
            "position": 4
        },
        {
            "field_name": "published_date",
            "field_label": "Published Date",
            "field_type": "Date",
            "position": 5
        }
    ]
}

doc = content_type_service.create_content_type(blog_data)
print(f"Created content type: {doc.name}")
```

### Via API (using curl or Postman)
```bash
# Get all content types
curl -X GET "http://syncedoffice.localhost:8002/api/method/syncedoffice.so_cms.api.content_type.get_content_types" \
  -H "Authorization: token YOUR_API_KEY:YOUR_API_SECRET"

# Create content type
curl -X POST "http://syncedoffice.localhost:8002/api/method/syncedoffice.so_cms.api.content_type.create_content_type" \
  -H "Content-Type: application/json" \
  -H "Authorization: token YOUR_API_KEY:YOUR_API_SECRET" \
  -d '{"data": {...}}'
```

## Next Steps: Phase 2 - Vue Frontend

1. Initialize Vue 3 app in `cms_app/`
2. Install dependencies (frappe-ui, pinia, vue-router, vuedraggable, tiptap)
3. Create Content Type Builder UI components
4. Implement drag-and-drop field builder
5. Build field configuration panels

## Architecture Notes

### Content Storage Strategy
- Using JSON field in `CMS Content` doctype for flexible schema
- This allows dynamic content types without creating new doctypes
- Content validation happens at the service layer based on content type definition

### Caching Strategy
- Content types are cached for 5 minutes
- Cache is cleared on content type updates
- Cache key format: `cms_content_type:{api_id}`

### Field Types Supported
- **Text** - Short text input
- **Long Text** - Textarea
- **Rich Text** - WYSIWYG editor
- **Number** - Integer input
- **Decimal** - Float input
- **Date** - Date picker
- **DateTime** - Date and time picker
- **Time** - Time picker
- **Boolean** - Checkbox
- **Email** - Email input with validation
- **URL** - URL input with validation
- **UID** - Unique identifier (auto-generated)
- **Enumeration** - Dropdown select
- **JSON** - JSON editor
- **Media** - File/Image upload
- **Relation** - Link to other content types
- **Component** - Reusable field group
- **Dynamic Zone** - Flexible content blocks

## File Structure
```
syncedoffice/so_cms/
├── api/
│   ├── __init__.py
│   └── content_type.py
├── doctype/
│   ├── cms_component/
│   ├── cms_component_category/
│   ├── cms_component_field/
│   ├── cms_content/
│   ├── cms_content_type/
│   └── cms_content_type_field/
├── services/
│   ├── __init__.py
│   ├── content_type_service.py
│   └── field_service.py
├── __init__.py
└── README.md
```

## Status
✅ Phase 1.1-1.4: DocTypes created
✅ Phase 1.5: Backend services implemented
✅ Phase 1.6: API endpoints created
⏳ Phase 2: Vue frontend (next)
