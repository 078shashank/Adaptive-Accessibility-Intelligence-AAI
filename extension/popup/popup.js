/**
 * Popup Script for AAI Extension
 * Handles user interactions in the extension popup
 */

import { storageService } from '../services/storage.js';
import apiService from '../services/api.js';

// DOM Elements
const elements = {
  fontSize: document.getElementById('font-size'),
  fontSizeValue: document.getElementById('font-size-value'),
  lineSpacing: document.getElementById('line-spacing'),
  lineSpacingValue: document.getElementById('line-spacing-value'),
  letterSpacing: document.getElementById('letter-spacing'),
  letterSpacingValue: document.getElementById('letter-spacing-value'),
  fontFamily: document.getElementById('font-family'),
  colorOverlay: document.getElementById('color-overlay'),
  highContrast: document.getElementById('high-contrast'),
  darkMode: document.getElementById('dark-mode'),
  reduceMotion: document.getElementById('reduce-motion'),
  simplifyText: document.getElementById('simplify-text'),
  readingLevel: document.getElementById('reading-level'),
  resetBtn: document.getElementById('reset-btn'),
  helpBtn: document.getElementById('help-btn'),
  openFullSettings: document.getElementById('open-full-settings'),
  backendStatus: document.getElementById('backend-status')
};

// Initialize popup
initializePopup();

/**
 * Initialize popup with current settings
 */
async function initializePopup() {
  try {
    // Load settings from storage
    const settings = await storageService.getAllSettings();
    console.log('Popup loaded settings:', settings);
    
    // Populate UI with current settings
    populateSettings(settings);
    
    // Check backend health
    checkBackendHealth();
  } catch (error) {
    console.error('Failed to initialize popup:', error);
  }
}

/**
 * Populate form fields with current settings
 */
function populateSettings(settings) {
  if (settings.fontSize) {
    elements.fontSize.value = settings.fontSize;
    elements.fontSizeValue.textContent = settings.fontSize;
  }
  
  if (settings.lineSpacing) {
    elements.lineSpacing.value = settings.lineSpacing;
    elements.lineSpacingValue.textContent = settings.lineSpacing.toFixed(1);
  }
  
  if (settings.letterSpacing) {
    elements.letterSpacing.value = settings.letterSpacing;
    elements.letterSpacingValue.textContent = settings.letterSpacing.toFixed(1);
  }
  
  if (settings.fontFamily) {
    elements.fontFamily.value = settings.fontFamily;
  }
  
  if (settings.colorOverlay) {
    elements.colorOverlay.value = settings.colorOverlay;
  }
  
  if (settings.highContrastMode !== undefined) {
    elements.highContrast.checked = settings.highContrastMode;
  }
  
  if (settings.darkMode !== undefined) {
    elements.darkMode.checked = settings.darkMode;
  }
  
  if (settings.reduceMotion !== undefined) {
    elements.reduceMotion.checked = settings.reduceMotion;
  }
  
  if (settings.simplifyText !== undefined) {
    elements.simplifyText.checked = settings.simplifyText;
  }
  
  if (settings.readingLevel) {
    elements.readingLevel.value = settings.readingLevel;
  }
}

/**
 * Add event listeners to all controls
 */
function addEventListeners() {
  // Font size slider
  elements.fontSize.addEventListener('input', (e) => {
    const value = e.target.value;
    elements.fontSizeValue.textContent = value;
    updateSetting('fontSize', parseInt(value));
  });
  
  // Line spacing slider
  elements.lineSpacing.addEventListener('input', (e) => {
    const value = e.target.value;
    elements.lineSpacingValue.textContent = parseFloat(value).toFixed(1);
    updateSetting('lineSpacing', parseFloat(value));
  });
  
  // Letter spacing slider
  elements.letterSpacing.addEventListener('input', (e) => {
    const value = e.target.value;
    elements.letterSpacingValue.textContent = parseFloat(value).toFixed(1);
    updateSetting('letterSpacing', parseFloat(value));
  });
  
  // Font family dropdown
  elements.fontFamily.addEventListener('change', (e) => {
    updateSetting('fontFamily', e.target.value);
  });
  
  // Color overlay dropdown
  elements.colorOverlay.addEventListener('change', (e) => {
    updateSetting('colorOverlay', e.target.value);
  });
  
  // Toggle controls
  elements.highContrast.addEventListener('change', (e) => {
    updateSetting('highContrastMode', e.target.checked);
  });
  
  elements.darkMode.addEventListener('change', (e) => {
    updateSetting('darkMode', e.target.checked);
  });
  
  elements.reduceMotion.addEventListener('change', (e) => {
    updateSetting('reduceMotion', e.target.checked);
  });
  
  elements.simplifyText.addEventListener('change', (e) => {
    updateSetting('simplifyText', e.target.checked);
  });
  
  // Reading level dropdown
  elements.readingLevel.addEventListener('change', (e) => {
    updateSetting('readingLevel', e.target.value);
  });
  
  // Reset button
  elements.resetBtn.addEventListener('click', async () => {
    if (confirm('Reset all settings to defaults?')) {
      await storageService.resetToDefaults();
      initializePopup();
      
      // Notify content scripts to apply defaults
      chrome.tabs.query({ active: true, currentWindow: true }, async (tabs) => {
        const settings = await storageService.getAllSettings();
        chrome.tabs.sendMessage(tabs[0].id, {
          action: 'apply-all-settings',
          settings
        }).catch(() => {});
      });
    }
  });
  
  // Help button
  elements.helpBtn.addEventListener('click', () => {
    window.open('https://github.com/078shashank/Adaptive-Accessibility-Intelligence-AAI/blob/main/README.md', '_blank');
  });
  
  // Open full settings link
  elements.openFullSettings.addEventListener('click', (e) => {
    e.preventDefault();
    // Could open a full settings page or options page
    alert('Full settings panel coming soon! For now, use the quick settings above.');
  });
}

/**
 * Update a setting in storage and notify background/content scripts
 */
async function updateSetting(key, value) {
  try {
    await storageService.updateSetting(key, value);
    console.log(`Updated setting: ${key} = ${value}`);
    
    // Notify background script to broadcast to all tabs
    chrome.runtime.sendMessage({
      action: 'update-setting',
      key,
      value
    });
  } catch (error) {
    console.error(`Failed to update ${key}:`, error);
  }
}

/**
 * Check backend health status
 */
async function checkBackendHealth() {
  try {
    const result = await apiService.health.check();
    
    if (result.available) {
      elements.backendStatus.textContent = '●';
      elements.backendStatus.className = 'status-indicator online';
      elements.backendStatus.title = 'Backend online';
    } else {
      elements.backendStatus.textContent = '●';
      elements.backendStatus.className = 'status-indicator offline';
      elements.backendStatus.title = 'Backend offline - some features may not work';
    }
  } catch (error) {
    elements.backendStatus.textContent = '●';
    elements.backendStatus.className = 'status-indicator offline';
    elements.backendStatus.title = 'Backend status unknown';
  }
}

// Initialize event listeners when DOM is ready
document.addEventListener('DOMContentLoaded', addEventListeners);

// Refresh backend status every 30 seconds
setInterval(checkBackendHealth, 30000);
