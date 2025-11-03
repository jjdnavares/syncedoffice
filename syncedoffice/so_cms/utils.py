import json
import os
import frappe


def get_cms_assets():
	"""
	Read Vite manifest and return CSS and JS file paths
	
	Returns:
		dict: Dictionary with 'css' and 'js' keys containing asset paths
	"""
	manifest_path = frappe.get_app_path('syncedoffice', 'public', 'js', 'cms', '.vite', 'manifest.json')
	
	if not os.path.exists(manifest_path):
		frappe.log_error(f"Vite manifest not found at {manifest_path}", "CMS Assets Error")
		return {
			'css': [],
			'js': '/assets/syncedoffice/js/cms/cms-app.js'
		}
	
	try:
		with open(manifest_path, 'r') as f:
			manifest = json.load(f)
		
		# Get the main entry point
		entry = manifest.get('index.html', {})
		
		# Get CSS files
		css_files = entry.get('css', [])
		css_paths = [f"/assets/syncedoffice/js/cms/{css}" for css in css_files]
		
		# Get JS file
		js_file = entry.get('file', 'cms-app.js')
		js_path = f"/assets/syncedoffice/js/cms/{js_file}"
		
		return {
			'css': css_paths,
			'js': js_path
		}
	except Exception as e:
		frappe.log_error(f"Error reading Vite manifest: {str(e)}", "CMS Assets Error")
		return {
			'css': [],
			'js': '/assets/syncedoffice/js/cms/cms-app.js'
		}
