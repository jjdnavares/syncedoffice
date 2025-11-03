# Manual Trigger Design Update

## Overview

Updated the Manual Trigger node to match n8n's exact design with a mouse pointer icon and proper label text.

## Changes Made

### ✅ 1. Icon Changed to Mouse Pointer

**Before:** Generic box icon  
**After:** Mouse pointer/cursor icon

```javascript
// CustomNode.vue
const nodeIcon = computed(() => {
  // Manual trigger gets MousePointer icon
  if (isManualTrigger.value) {
    return MousePointer
  }
  // ... other icons
})
```

### ✅ 2. Label Text Updated

**Before:** "Trigger manually"  
**After:** "When clicking 'Execute workflow'"

```javascript
// WorkflowEditor.vue
{
  type: 'trigger-manual',
  label: 'When clicking \'Execute workflow\'',
  description: 'Runs the flow on clicking a button in n8n. Good for getting started quickly',
  icon: MousePointer,
  color: 'text-gray-400'
}
```

### ✅ 3. Improved Trigger Detection

Added separate detection for manual trigger vs other triggers:

```javascript
// Check if it's a manual trigger specifically
const isManualTrigger = computed(() => {
  return props.data.type === 'trigger-manual' ||
         props.data.nodeType === 'trigger_manually' ||
         props.data.label?.toLowerCase().includes('trigger manually') ||
         props.data.label?.toLowerCase().includes('manual trigger') ||
         props.data.label?.toLowerCase().includes('clicking')
})

// Check if it's any trigger node (for styling)
const isTriggerManually = computed(() => {
  const isTrigger = props.data.type === 'trigger' ||
                    props.data.type?.startsWith('trigger-') ||
                    props.data.nodeType?.includes('trigger') ||
                    props.data.label?.toLowerCase().includes('trigger') ||
                    props.data.label?.toLowerCase().includes('schedule') ||
                    props.data.label?.toLowerCase().includes('webhook') ||
                    props.data.label?.toLowerCase().includes('on ') ||
                    props.data.label?.toLowerCase().includes('when ')
  
  return isTrigger
})
```

## Visual Comparison

### n8n Design (Reference)
- ✅ Mouse pointer/cursor icon
- ✅ "When clicking 'Execute workflow'" label
- ✅ Dark rounded square background
- ✅ White icon on dark background
- ✅ Red lightning bolt indicator

### Our Implementation
- ✅ MousePointer icon from lucide-vue-next
- ✅ "When clicking 'Execute workflow'" label
- ✅ Dark gradient background (#4a5568 → #2d3748)
- ✅ White icon (48px)
- ✅ Red lightning bolt badge (32px circle)
- ✅ Text below with shadow

## Files Modified

### 1. `/workflow/src/components/workflow/CustomNode.vue`
- Added `isManualTrigger` computed property
- Updated `nodeIcon` to return `MousePointer` for manual triggers
- Kept `isTriggerManually` for general trigger styling

### 2. `/workflow/src/pages/WorkflowEditor.vue`
- Updated trigger label: "Trigger manually" → "When clicking 'Execute workflow'"
- Changed icon from `Zap` to `MousePointer`
- Changed color from `text-yellow-600` to `text-gray-400`
- Added `MousePointer` to lucide-vue-next imports

## Icon Mapping

| Trigger Type | Icon | Label |
|-------------|------|-------|
| Manual | MousePointer | When clicking 'Execute workflow' |
| Schedule | Zap | On a schedule |
| Webhook | Webhook | On webhook call |
| Other | Box (default) | Various |

## Testing

To see the updated manual trigger:

1. Start the development server:
```bash
cd /home/jumes/bench
bench start
```

2. Navigate to workflow editor
3. Add a manual trigger node
4. Verify:
   - ✅ Mouse pointer icon (white on dark background)
   - ✅ "When clicking 'Execute workflow'" label below
   - ✅ Dark rounded square design
   - ✅ Red lightning bolt on left
   - ✅ Smooth hover effects

## Result

The manual trigger now matches n8n's design exactly:
- Mouse pointer icon instead of generic box
- Proper label text matching n8n
- Same dark rounded styling as other triggers
- Consistent visual hierarchy

---

*Status: Complete - Ready for Testing*
*Reference: n8n Manual Trigger Design*
