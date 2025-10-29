# Copyright (c) 2025, jumes.dev and contributors
# Sample content types for testing

import frappe


def create_sample_content_types():
	"""Create sample content types for testing"""
	
	# Blog Post
	if not frappe.db.exists("CMS Content Type", "Blog"):
		blog = frappe.get_doc({
			"doctype": "CMS Content Type",
			"content_type_name": "Blog",
			"display_name": "Blog Post",
			"description": "Blog posts for the website",
			"kind": "Collection Type",
			"icon": "file-text",
			"is_published": 1,
			"fields": [
				{
					"field_name": "title",
					"field_label": "Title",
					"field_type": "Text",
					"required": 1,
					"position": 1,
					"placeholder": "Enter blog title"
				},
				{
					"field_name": "slug",
					"field_label": "Slug",
					"field_type": "UID",
					"required": 1,
					"unique": 1,
					"position": 2,
					"help_text": "URL-friendly version of the title"
				},
				{
					"field_name": "excerpt",
					"field_label": "Excerpt",
					"field_type": "Long Text",
					"position": 3,
					"max_length": 200,
					"help_text": "Short description for previews"
				},
				{
					"field_name": "content",
					"field_label": "Content",
					"field_type": "Rich Text",
					"required": 1,
					"position": 4
				},
				{
					"field_name": "featured_image",
					"field_label": "Featured Image",
					"field_type": "Media",
					"position": 5
				},
				{
					"field_name": "author",
					"field_label": "Author",
					"field_type": "Text",
					"position": 6
				},
				{
					"field_name": "published_date",
					"field_label": "Published Date",
					"field_type": "Date",
					"position": 7
				},
				{
					"field_name": "is_featured",
					"field_label": "Featured Post",
					"field_type": "Boolean",
					"position": 8
				}
			]
		})
		blog.insert()
		print(f"✅ Created content type: {blog.name}")
	
	# Product
	if not frappe.db.exists("CMS Content Type", "Product"):
		product = frappe.get_doc({
			"doctype": "CMS Content Type",
			"content_type_name": "Product",
			"display_name": "Product",
			"description": "Products for e-commerce",
			"kind": "Collection Type",
			"icon": "shopping-bag",
			"is_published": 1,
			"fields": [
				{
					"field_name": "name",
					"field_label": "Product Name",
					"field_type": "Text",
					"required": 1,
					"position": 1
				},
				{
					"field_name": "sku",
					"field_label": "SKU",
					"field_type": "Text",
					"required": 1,
					"unique": 1,
					"position": 2
				},
				{
					"field_name": "description",
					"field_label": "Description",
					"field_type": "Rich Text",
					"position": 3
				},
				{
					"field_name": "price",
					"field_label": "Price",
					"field_type": "Decimal",
					"required": 1,
					"position": 4
				},
				{
					"field_name": "images",
					"field_label": "Product Images",
					"field_type": "JSON",
					"position": 5,
					"help_text": "Array of image URLs"
				},
				{
					"field_name": "in_stock",
					"field_label": "In Stock",
					"field_type": "Boolean",
					"position": 6
				}
			]
		})
		product.insert()
		print(f"✅ Created content type: {product.name}")
	
	# Page (Single Type)
	if not frappe.db.exists("CMS Content Type", "Homepage"):
		homepage = frappe.get_doc({
			"doctype": "CMS Content Type",
			"content_type_name": "Homepage",
			"display_name": "Homepage",
			"description": "Homepage content",
			"kind": "Single Type",
			"icon": "home",
			"is_published": 1,
			"fields": [
				{
					"field_name": "hero_title",
					"field_label": "Hero Title",
					"field_type": "Text",
					"required": 1,
					"position": 1
				},
				{
					"field_name": "hero_subtitle",
					"field_label": "Hero Subtitle",
					"field_type": "Long Text",
					"position": 2
				},
				{
					"field_name": "hero_image",
					"field_label": "Hero Image",
					"field_type": "Media",
					"position": 3
				},
				{
					"field_name": "cta_text",
					"field_label": "CTA Button Text",
					"field_type": "Text",
					"position": 4
				},
				{
					"field_name": "cta_url",
					"field_label": "CTA Button URL",
					"field_type": "URL",
					"position": 5
				}
			]
		})
		homepage.insert()
		print(f"✅ Created content type: {homepage.name}")
	
	frappe.db.commit()
	print("\n✅ Sample content types created successfully!")


if __name__ == "__main__":
	create_sample_content_types()
