/**
 * Background Service Worker for AAI Chrome Extension
 * Handles extension installation, context menus, and message routing
 */

// Install/Update handler
chrome.runtime.onInstalled.addListener((details) => {
  console.log('AAI Extension installed/updated', details);
  
  // Initialize default settings
  chrome.storage.sync.set({
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
    reduceAnimation: false
  });
  
  // Create context menu for text simplification
  createContextMenu();
});

// Create context menu items
function createContextMenu() {
  chrome.contextMenus.create({
    id: 'aai-simplify',
    title: 'Simplify with AAI',
    contexts: ['selection']
  });
  
  chrome.contextMenus.create({
    id: 'aai-read-aloud',
    title: 'Read Aloud with AAI',
    contexts: ['selection']
  });
}

// Context menu click handler
chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === 'aai-simplify') {
    // Send message to content script to simplify selected text
    chrome.tabs.sendMessage(tab.id, {
      action: 'simplify-text',
      text: info.selectionText
    });
  } else if (info.menuItemId === 'aai-read-aloud') {
    // Send message to content script to read selected text
    chrome.tabs.sendMessage(tab.id, {
      action: 'read-aloud',
      text: info.selectionText
    });
  }
});

// Message router between popup, content scripts, and background
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log('Background received message:', request);
  
  switch (request.action) {
    case 'get-settings':
      // Retrieve all settings from storage
      chrome.storage.sync.get(null, (settings) => {
        sendResponse(settings);
      });
      return true; // Keep channel open for async response
      
    case 'update-setting':
      // Update a single setting
      chrome.storage.sync.set({ [request.key]: request.value }, () => {
        sendResponse({ success: true });
        
        // Notify all tabs about the change
        chrome.tabs.query({}, (tabs) => {
          tabs.forEach(tab => {
            chrome.tabs.sendMessage(tab.id, {
              action: 'setting-updated',
              key: request.key,
              value: request.value
            }).catch(() => {}); // Ignore errors for closed tabs
          });
        });
      });
      return true;
      
    case 'check-backend':
      // Check if local backend is available
      checkBackendHealth(sendResponse);
      return true;
      
    case 'notify-content-script':
      // Forward message to content script in specific tab
      chrome.tabs.sendMessage(request.tabId, request.message).catch(() => {});
      sendResponse({ success: true });
      break;
      
    default:
      console.warn('Unknown action:', request.action);
  }
  
  return false;
});

// Check backend health
async function checkBackendHealth(sendResponse) {
  try {
    const response = await fetch('http://localhost:8000/api/v1/health', {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
    });
    
    if (response.ok) {
      const data = await response.json();
      sendResponse({ available: true, data });
    } else {
      sendResponse({ available: false, error: 'Backend returned non-OK status' });
    }
  } catch (error) {
    sendResponse({ available: false, error: error.message });
  }
}

// Tab activation handler - apply settings to active tab
chrome.tabs.onActivated.addListener((activeInfo) => {
  // Apply current settings to the newly activated tab
  chrome.storage.sync.get(null, (settings) => {
    chrome.tabs.sendMessage(activeInfo.tabId, {
      action: 'apply-all-settings',
      settings: settings
    }).catch(() => {}); // Ignore if content script not ready
  });
});

// Keep service worker alive for faster response times
setInterval(() => {
  console.log('AAI Background: Keeping service worker active');
}, 20000);
