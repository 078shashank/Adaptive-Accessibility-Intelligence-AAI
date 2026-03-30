/**
 * Chrome Storage Service for AAI Extension
 * Wraps chrome.storage API for easy access to user preferences
 */

export const storageService = {
  /**
   * Get all settings from chrome.storage.sync
   * @returns {Promise<object>} All stored settings
   */
  getAllSettings: () => {
    return new Promise((resolve, reject) => {
      chrome.storage.sync.get(null, (settings) => {
        if (chrome.runtime.lastError) {
          reject(new Error(chrome.runtime.lastError.message));
        } else {
          resolve(settings);
        }
      });
    });
  },
  
  /**
   * Get a specific setting
   * @param {string} key - Setting key
   * @returns {Promise<any>} Setting value
   */
  getSetting: (key) => {
    return new Promise((resolve, reject) => {
      chrome.storage.sync.get([key], (result) => {
        if (chrome.runtime.lastError) {
          reject(new Error(chrome.runtime.lastError.message));
        } else {
          resolve(result[key]);
        }
      });
    });
  },
  
  /**
   * Update a single setting
   * @param {string} key - Setting key
   * @param {any} value - Setting value
   * @returns {Promise<boolean>} Success status
   */
  updateSetting: (key, value) => {
    return new Promise((resolve, reject) => {
      chrome.storage.sync.set({ [key]: value }, () => {
        if (chrome.runtime.lastError) {
          reject(new Error(chrome.runtime.lastError.message));
        } else {
          resolve(true);
        }
      });
    });
  },
  
  /**
   * Update multiple settings at once
   * @param {object} settings - Key-value pairs of settings
   * @returns {Promise<boolean>} Success status
   */
  updateSettings: (settings) => {
    return new Promise((resolve, reject) => {
      chrome.storage.sync.set(settings, () => {
        if (chrome.runtime.lastError) {
          reject(new Error(chrome.runtime.lastError.message));
        } else {
          resolve(true);
        }
      });
    });
  },
  
  /**
   * Reset all settings to defaults
   * @returns {Promise<boolean>} Success status
   */
  resetToDefaults: () => {
    const defaultSettings = {
      aaiEnabled: true,
      fontSize: 16,
      lineSpacing: 1.5,
      letterSpacing: 0.0,
      fontFamily: 'system',
      colorOverlay: 'none',
      highContrastMode: false,
      darkMode: false,
      simplifyText: false,
      readingLevel: 'intermediate',
      speechRate: 1.0,
      reduceMotion: false,
      reduceAnimation: false,
      soundEnabled: true,
      vibrationEnabled: true,
      minimalMode: false,
      guidedMode: false,
      showAvatar: false
    };
    
    return storageService.updateSettings(defaultSettings);
  },
  
  /**
   * Listen for setting changes
   * @param {function} callback - Callback function(changes)
   */
  onChanged: (callback) => {
    chrome.storage.onChanged.addListener(callback);
  }
};

export default storageService;
