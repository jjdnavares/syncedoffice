/**
 * API utility for making requests to Frappe backend
 */

export const api = {
  /**
   * Call a whitelisted Frappe method
   * @param {string} method - The method path (e.g., 'syncedoffice.so_cms.api.content_type.get_content_types')
   * @param {object} args - Arguments to pass to the method
   * @returns {Promise} - Response data
   */
  async call(method, args = {}) {
    const url = `/api/method/${method}`
    
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Frappe-CSRF-Token': this.getCSRFToken(),
        },
        body: JSON.stringify(args),
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.message || error.exc || 'API request failed')
      }

      const data = await response.json()
      return data
    } catch (error) {
      console.error('API Error:', error)
      throw error
    }
  },

  /**
   * Get CSRF token from cookie
   */
  getCSRFToken() {
    const token = this.getCookie('csrf_token')
    return token || ''
  },

  /**
   * Get cookie value by name
   */
  getCookie(name) {
    const value = `; ${document.cookie}`
    const parts = value.split(`; ${name}=`)
    if (parts.length === 2) return parts.pop().split(';').shift()
    return null
  },
}
