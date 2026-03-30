/**
 * DOM Manipulation Utilities for AAI Extension
 */

/**
 * Apply CSS styles to document elements
 * @param {string} selector - CSS selector
 * @param {object} styles - Style properties
 */
export const applyStyles = (selector, styles) => {
  const elements = document.querySelectorAll(selector);
  elements.forEach(element => {
    Object.assign(element.style, styles);
  });
};

/**
 * Inject CSS variables into document
 * @param {object} variables - CSS custom properties
 */
export const injectCSSVariables = (variables) => {
  const root = document.documentElement;
  
  Object.entries(variables).forEach(([property, value]) => {
    root.style.setProperty(`--aai-${property}`, value);
  });
};

/**
 * Remove all AAI CSS variables from document
 */
export const removeCSSVariables = () => {
  const root = document.documentElement;
  const aaiVars = Array.from(root.style).filter(prop => prop.startsWith('--aai-'));
  aaiVars.forEach(varName => {
    root.style.removeProperty(varName);
  });
};

/**
 * Apply font family to entire document
 * @param {string} fontFamily - Font family name
 */
export const applyFontFamily = (fontFamily) => {
  const fontMappings = {
    'system': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif',
    'OpenDyslexic': '"OpenDyslexic", "Comic Sans MS", cursive',
    'Arial': 'Arial, "Helvetica Neue", Helvetica, sans-serif',
    'Georgia': 'Georgia, Cambria, "Times New Roman", Times, serif',
    'Verdana': 'Verdana, Geneva, sans-serif',
    'Trebuchet': '"Trebuchet MS", "Lucida Grande", "Lucida Sans Unicode", "Lucida Sans", Tahoma, sans-serif'
  };
  
  const fontValue = fontMappings[fontFamily] || fontFamily;
  document.body.style.fontFamily = fontValue;
};

/**
 * Load external font (e.g., OpenDyslexic)
 * @param {string} fontName - Font name
 * @param {string} fontUrl - Font file URL
 */
export const loadExternalFont = (fontName, fontUrl) => {
  const fontFace = new FontFace(fontName, `url(${fontUrl})`);
  
  fontFace.load().then((loadedFont) => {
    document.fonts.add(loadedFont);
    console.log(`Font ${fontName} loaded successfully`);
  }).catch((error) => {
    console.error(`Failed to load font ${fontName}:`, error);
  });
};

/**
 * Apply color overlay to document
 * @param {string} color - Overlay color (blue, green, yellow, sepia, none)
 */
export const applyColorOverlay = (color) => {
  // Remove existing overlay if any
  const existingOverlay = document.getElementById('aai-color-overlay');
  if (existingOverlay) {
    existingOverlay.remove();
  }
  
  if (color === 'none') {
    return;
  }
  
  const overlayColors = {
    blue: 'rgba(173, 216, 230, 0.2)',
    green: 'rgba(144, 238, 144, 0.2)',
    yellow: 'rgba(255, 255, 224, 0.3)',
    sepia: 'rgba(112, 66, 20, 0.1)'
  };
  
  const overlay = document.createElement('div');
  overlay.id = 'aai-color-overlay';
  overlay.style.position = 'fixed';
  overlay.style.top = '0';
  overlay.style.left = '0';
  overlay.style.width = '100%';
  overlay.style.height = '100%';
  overlay.style.pointerEvents = 'none';
  overlay.style.zIndex = '999998';
  overlay.style.backgroundColor = overlayColors[color] || 'transparent';
  
  document.body.appendChild(overlay);
};

/**
 * Apply high contrast mode
 * @param {boolean} enabled - Enable/disable high contrast
 */
export const applyHighContrast = (enabled) => {
  if (enabled) {
    document.body.style.filter = 'contrast(1.2)';
    document.body.classList.add('aai-high-contrast');
  } else {
    document.body.style.filter = '';
    document.body.classList.remove('aai-high-contrast');
  }
};

/**
 * Apply dark mode
 * @param {boolean} enabled - Enable/disable dark mode
 */
export const applyDarkMode = (enabled) => {
  if (enabled) {
    document.body.classList.add('aai-dark-mode');
  } else {
    document.body.classList.remove('aai-dark-mode');
  }
};

/**
 * Reduce motion/animations
 * @param {boolean} enabled - Enable reduced motion
 */
export const applyReducedMotion = (enabled) => {
  if (enabled) {
    document.body.classList.add('aai-reduce-motion');
  } else {
    document.body.classList.remove('aai-reduce-motion');
  }
};

/**
 * Get selected text from page
 * @returns {string|null} Selected text or null
 */
export const getSelectedText = () => {
  const selection = window.getSelection();
  return selection ? selection.toString() : null;
};

/**
 * Replace selected text with simplified version
 * @param {string} originalText - Original text
 * @param {string} simplifiedText - Simplified text
 */
export const replaceSelectedText = (originalText, simplifiedText) => {
  const selection = window.getSelection();
  if (!selection || selection.rangeCount === 0) return;
  
  const range = selection.getRangeAt(0);
  range.deleteContents();
  
  const textNode = document.createTextNode(simplifiedText);
  range.insertNode(textNode);
};

/**
 * Create a tooltip element
 * @param {string} content - Tooltip content
 * @param {HTMLElement} target - Target element
 */
export const createTooltip = (content, target) => {
  const tooltip = document.createElement('div');
  tooltip.className = 'aai-tooltip';
  tooltip.textContent = content;
  tooltip.style.position = 'absolute';
  tooltip.style.zIndex = '1000000';
  tooltip.style.padding = '8px 12px';
  tooltip.style.backgroundColor = '#333';
  tooltip.style.color = '#fff';
  tooltip.style.borderRadius = '4px';
  tooltip.style.fontSize = '14px';
  tooltip.style.maxWidth = '300px';
  tooltip.style.boxShadow = '0 2px 8px rgba(0,0,0,0.2)';
  
  document.body.appendChild(tooltip);
  
  const rect = target.getBoundingClientRect();
  tooltip.style.top = `${rect.bottom + window.scrollY + 5}px`;
  tooltip.style.left = `${rect.left + window.scrollX}px`;
  
  return tooltip;
};

export default {
  applyStyles,
  injectCSSVariables,
  removeCSSVariables,
  applyFontFamily,
  loadExternalFont,
  applyColorOverlay,
  applyHighContrast,
  applyDarkMode,
  applyReducedMotion,
  getSelectedText,
  replaceSelectedText,
  createTooltip
};
