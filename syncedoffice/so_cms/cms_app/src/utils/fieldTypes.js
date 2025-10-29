/**
 * Field type definitions and configurations
 */

export const FIELD_TYPES = [
  {
    type: 'Text',
    label: 'Text',
    icon: 'type',
    category: 'Basic',
    description: 'Short text input',
  },
  {
    type: 'Long Text',
    label: 'Long Text',
    icon: 'align-left',
    category: 'Basic',
    description: 'Multi-line text area',
  },
  {
    type: 'Rich Text',
    label: 'Rich Text',
    icon: 'file-text',
    category: 'Basic',
    description: 'WYSIWYG editor',
  },
  {
    type: 'Number',
    label: 'Number',
    icon: 'hash',
    category: 'Basic',
    description: 'Integer number',
  },
  {
    type: 'Decimal',
    label: 'Decimal',
    icon: 'hash',
    category: 'Basic',
    description: 'Decimal number',
  },
  {
    type: 'Boolean',
    label: 'Boolean',
    icon: 'check-square',
    category: 'Basic',
    description: 'True/False checkbox',
  },
  {
    type: 'Date',
    label: 'Date',
    icon: 'calendar',
    category: 'Date & Time',
    description: 'Date picker',
  },
  {
    type: 'DateTime',
    label: 'Date Time',
    icon: 'calendar-clock',
    category: 'Date & Time',
    description: 'Date and time picker',
  },
  {
    type: 'Time',
    label: 'Time',
    icon: 'clock',
    category: 'Date & Time',
    description: 'Time picker',
  },
  {
    type: 'Email',
    label: 'Email',
    icon: 'mail',
    category: 'Advanced',
    description: 'Email address with validation',
  },
  {
    type: 'URL',
    label: 'URL',
    icon: 'link',
    category: 'Advanced',
    description: 'URL with validation',
  },
  {
    type: 'UID',
    label: 'UID',
    icon: 'key',
    category: 'Advanced',
    description: 'Unique identifier',
  },
  {
    type: 'Enumeration',
    label: 'Enumeration',
    icon: 'list',
    category: 'Advanced',
    description: 'Dropdown select',
  },
  {
    type: 'JSON',
    label: 'JSON',
    icon: 'braces',
    category: 'Advanced',
    description: 'JSON data',
  },
  {
    type: 'Media',
    label: 'Media',
    icon: 'image',
    category: 'Media',
    description: 'File or image upload',
  },
  {
    type: 'Relation',
    label: 'Relation',
    icon: 'link-2',
    category: 'Relational',
    description: 'Link to other content',
  },
  {
    type: 'Component',
    label: 'Component',
    icon: 'box',
    category: 'Relational',
    description: 'Reusable component',
  },
  {
    type: 'Dynamic Zone',
    label: 'Dynamic Zone',
    icon: 'layers',
    category: 'Relational',
    description: 'Flexible content blocks',
  },
]

export const FIELD_CATEGORIES = [
  { name: 'Basic', label: 'Basic Fields' },
  { name: 'Date & Time', label: 'Date & Time' },
  { name: 'Advanced', label: 'Advanced' },
  { name: 'Media', label: 'Media' },
  { name: 'Relational', label: 'Relational' },
]

export function getFieldTypeConfig(type) {
  return FIELD_TYPES.find(ft => ft.type === type)
}

export function getFieldTypesByCategory(category) {
  return FIELD_TYPES.filter(ft => ft.category === category)
}
