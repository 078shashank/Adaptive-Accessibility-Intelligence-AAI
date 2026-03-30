/**
 * Content Script for AAI Extension
 * Injected into all web pages to provide accessibility features
 */

import { storageService } from './services/storage.js';
import domUtils from './utils/dom-utils.js';

// State management
let currentSettings = {};
let accessibilityPanel = null;

console.log('AAI Content Script loaded');

// Initialize on load
initializeContentScript();

/**
 * Initialize content script
 */
async function initializeContentScript() {
  try {
    // Load current settings
    currentSettings = await storageService.getAllSettings();
    console.log('AAI settings loaded:', currentSettings);
    
    // Apply settings to page
    applyAllSettings(currentSettings);
    
    // Create floating accessibility panel (optional - can be toggled)
    if (currentSettings.aaiEnabled) {
      createAccessibilityPanel();
    }
  } catch (error) {
    console.error('Failed to initialize AAI content script:', error);
  }
}

/**
 * Listen for messages from background/popup
 */
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log('Content script received message:', request);
  
  switch (request.action) {
    case 'apply-all-settings':
      currentSettings = request.settings;
      applyAllSettings(currentSettings);
      sendResponse({ success: true });
      break;
      
    case 'setting-updated':
      currentSettings[request.key] = request.value;
      applySetting(request.key, request.value);
      sendResponse({ success: true });
      break;
      
    case 'simplify-text':
      handleTextSimplification(request.text);
      sendResponse({ success: true });
      break;
      
    case 'read-aloud':
      handleReadAloud(request.text);
      sendResponse({ success: true });
      break;
      
    case 'toggle-panel':
      toggleAccessibilityPanel();
      sendResponse({ success: true });
      break;
      
    default:
      console.warn('Unknown action:', request.action);
  }
  
  return true;
});

/**
 * Apply all settings to the page
 */
function applyAllSettings(settings) {
  // Font size
  if (settings.fontSize) {
    document.body.style.fontSize = `${settings.fontSize}px`;
  }
  
  // Line spacing
  if (settings.lineSpacing) {
    domUtils.applyStyles('p, h1, h2, h3, h4, h5, h6, li, span', {
      lineHeight: settings.lineSpacing.toString()
    });
  }
  
  // Letter spacing
  if (settings.letterSpacing) {
    domUtils.applyStyles('body', {
      letterSpacing: `${settings.letterSpacing}px`
    });
  }
  
  // Font family
  if (settings.fontFamily) {
    domUtils.applyFontFamily(settings.fontFamily);
  }
  
  // Color overlay
  if (settings.colorOverlay) {
    domUtils.applyColorOverlay(settings.colorOverlay);
  }
  
  // High contrast mode
  if (settings.highContrastMode) {
    domUtils.applyHighContrast(true);
  } else {
    domUtils.applyHighContrast(false);
  }
  
  // Dark mode
  if (settings.darkMode) {
    domUtils.applyDarkMode(true);
  } else {
    domUtils.applyDarkMode(false);
  }
  
  // Reduce motion
  if (settings.reduceMotion) {
    domUtils.applyReducedMotion(true);
  } else {
    domUtils.applyReducedMotion(false);
  }
}

/**
 * Apply a single setting change
 */
function applySetting(key, value) {
  console.log(`Applying setting: ${key} = ${value}`);
  
  switch (key) {
    case 'fontSize':
      document.body.style.fontSize = `${value}px`;
      break;
    case 'lineSpacing':
      domUtils.applyStyles('p, h1, h2, h3, h4, h5, h6, li, span', {
        lineHeight: value.toString()
      });
      break;
    case 'letterSpacing':
      domUtils.applyStyles('body', {
        letterSpacing: `${value}px`
      });
      break;
    case 'fontFamily':
      domUtils.applyFontFamily(value);
      break;
    case 'colorOverlay':
      domUtils.applyColorOverlay(value);
      break;
    case 'highContrastMode':
      domUtils.applyHighContrast(value);
      break;
    case 'darkMode':
      domUtils.applyDarkMode(value);
      break;
    case 'reduceMotion':
      domUtils.applyReducedMotion(value);
      break;
  }
}

/**
 * Handle text simplification request
 */
async function handleTextSimplification(text) {
  try {
    // Show loading indicator
    const tooltip = domUtils.createTooltip('Simplifying...', document.body);
    
    // Call backend API
    const response = await fetch('http://localhost:8000/api/v1/text/simplify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        text, 
        reading_level: currentSettings.readingLevel || 'intermediate' 
      })
    });
    
    tooltip.remove();
    
    if (!response.ok) {
      throw new Error('Simplification failed');
    }
    
    const result = await response.json();
    
    // Show simplified text in tooltip
    const resultTooltip = domUtils.createTooltip(
      `Simplified:\n${result.simplified_text}`,
      document.body
    );
    
    // Auto-remove after 10 seconds
    setTimeout(() => resultTooltip.remove(), 10000);
    
  } catch (error) {
    console.error('Text simplification failed:', error);
    const errorTooltip = domUtils.createTooltip(
      'Error: Could not simplify text. Make sure the backend is running.',
      document.body
    );
    setTimeout(() => errorTooltip.remove(), 5000);
  }
}

/**
 * Handle read aloud request
 */
function handleReadAloud(text) {
  if ('speechSynthesis' in window) {
    // Cancel any ongoing speech
    window.speechSynthesis.cancel();
    
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = currentSettings.speechRate || 1.0;
    
    window.speechSynthesis.speak(utterance);
    
    console.log('Reading aloud:', text);
  } else {
    console.warn('Web Speech API not supported in this browser');
  }
}

/**
 * Create floating accessibility panel
 */
function createAccessibilityPanel() {
  if (accessibilityPanel) return;
  
  const panel = document.createElement('div');
  panel.id = 'aai-accessibility-panel';
  panel.innerHTML = `
    <div class="aai-panel-header">
      <span>AAI Tools</span>
      <button id="aai-panel-close" aria-label="Close panel">&times;</button>
    </div>
    <div class="aai-panel-content">
      <button id="aai-simplify-btn" class="aai-panel-btn">Simplify Text</button>
      <button id="aai-read-btn" class="aai-panel-btn">Read Aloud</button>
      <button id="aai-settings-btn" class="aai-panel-btn">Settings</button>
    </div>
  `;
  
  // Style the panel
  Object.assign(panel.style, {
    position: 'fixed',
    bottom: '20px',
    right: '20px',
    width: '200px',
    backgroundColor: '#fff',
    border: '2px solid #0078d4',
    borderRadius: '8px',
    boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
    zIndex: '2147483647',
    fontFamily: 'system-ui, sans-serif',
    fontSize: '14px'
  });
  
  document.body.appendChild(panel);
  accessibilityPanel = panel;
  
  // Add event listeners
  document.getElementById('aai-panel-close').addEventListener('click', toggleAccessibilityPanel);
  document.getElementById('aai-simplify-btn').addEventListener('click', () => {
    const selectedText = domUtils.getSelectedText();
    if (selectedText) {
      handleTextSimplification(selectedText);
    } else {
      alert('Please select some text first');
    }
  });
  document.getElementById('aai-read-btn').addEventListener('click', () => {
    const selectedText = domUtils.getSelectedText();
    if (selectedText) {
      handleReadAloud(selectedText);
    } else {
      alert('Please select some text first');
    }
  });
  document.getElementById('aai-settings-btn').addEventListener('click', () => {
    // Open extension popup or show settings modal
    chrome.runtime.sendMessage({ action: 'open-popup' });
  });
}

/**
 * Toggle accessibility panel visibility
 */
function toggleAccessibilityPanel() {
  if (accessibilityPanel) {
    accessibilityPanel.style.display = accessibilityPanel.style.display === 'none' ? 'block' : 'none';
  } else {
    createAccessibilityPanel();
  }
}

// Listen for storage changes
storageService.onChanged((changes, namespace) => {
  if (namespace === 'sync') {
    Object.entries(changes).forEach(([key, { newValue }]) => {
      currentSettings[key] = newValue;
      applySetting(key, newValue);
    });
  }
});

console.log('AAI Content Script initialized successfully');
