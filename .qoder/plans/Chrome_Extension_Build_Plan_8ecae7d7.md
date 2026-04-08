# Chrome Extension Implementation Plan

## Overview
Convert the AAI web application into a Chrome extension that works across all websites with:
- **Architecture**: Hybrid (Extension popup + Content script injection)
- **Backend**: Local FastAPI server (localhost:8000)
- **MVP Features**: Text simplification, TTS, font/size adjustments, contrast modes

---

## Phase 1: Extension Structure Setup

### 1.1 Create Extension Directory Structure
```
extension/
├── manifest.json              # Extension configuration
├── background.js              # Service worker
├── popup/
│   ├── popup.html            # Extension popup UI
│   ├── popup.css             # Popup styles
│   └── popup.js              # Popup logic
├── content/
│   ├── content.js            # Content script (DOM injection)
│   └── accessibility-panel.tsx  # Injected React component
├── services/
│   ├── api.js                # Backend API client
│   └── storage.js            # Chrome storage wrapper
├── styles/
│   └── injected.css          # Styles for injected panel
├── icons/
│   ├── icon48.png
│   └── icon128.png
└── utils/
    └── dom-utils.js          # DOM manipulation helpers
```

### 1.2 Create manifest.json
**File**: `extension/manifest.json`
```json
{
  "manifest_version": 3,
  "name": "AAI - Adaptive Accessibility Intelligence",
  "version": "1.0.0",
  "description": "AI-powered accessibility tools for reading assistance",
  "permissions": [
    "activeTab",
    "storage",
    "scripting"
  ],
  "host_permissions": [
    "<all_urls>"
  ],
  "background": {
    "service_worker": "background.js"
  },
  "action": {
    "default_popup": "popup/popup.html",
    "default_icon": {
      "48": "icons/icon48.png",
      "128": "icons/icon128.png"
    }
  },
  "content_scripts": [
    {
      "matches": ["<all_urls>"],
      "js": ["content/content.js"],
      "css": ["styles/injected.css"],
      "run_at": "document_end"
    }
  ],
  "web_accessible_resources": [
    {
      "resources": ["content/*", "styles/*"],
      "matches": ["<all_urls>"]
    }
  ]
}
```

---

## Phase 2: Core Extension Files

### 2.1 Background Service Worker
**File**: `extension/background.js`
- Handle extension installation/updates
- Manage communication between popup and content scripts
- Store user preferences in chrome.storage
- Monitor tab changes for accessibility state

### 2.2 Popup Component
**Files**: 
- `extension/popup/popup.html` - Main popup UI
- `extension/popup/popup.jsx` - React-based popup (similar to existing App.tsx)
- `extension/popup/popup.css` - Popup-specific styles

**Features**:
- Quick access to most-used settings
- Toggle accessibility features on/off
- Link to full settings panel
- Backend connection status indicator

### 2.3 Content Script
**File**: `extension/content/content.js`
- Detect page load
- Inject accessibility panel into DOM
- Listen for messages from popup/background
- Apply CSS modifications based on user settings

### 2.4 Injected Accessibility Panel
**File**: `extension/content/accessibility-panel.tsx`
- Adapted from existing `AccessibilityPanel.tsx`
- Modified to work as injected component
- Shadow DOM encapsulation to avoid style conflicts
- Draggable/resizable panel

---

## Phase 3: Service Layer

### 3.1 API Client
**File**: `extension/services/api.js`
```javascript
const API_BASE_URL = 'http://localhost:8000/api/v1';

export const textService = {
  simplify: async (text, readingLevel) => {
    const response = await fetch(`${API_BASE_URL}/text/simplify`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, reading_level: readingLevel })
    });
    return response.json();
  }
};
```

### 3.2 Storage Wrapper
**File**: `extension/services/storage.js`
- Wrap chrome.storage.local and chrome.storage.sync
- Sync user preferences across devices
- Cache simplified text results

---

## Phase 4: Feature Implementation

### 4.1 Text Simplification
**Implementation**:
1. User selects text on webpage → Right-click context menu → "Simplify with AAI"
2. Selected text sent to localhost:8000
3. Simplified text displayed in tooltip or replacement
4. Option to toggle between original/simplified

### 4.2 Text-to-Speech
**Implementation**:
1. Add "Read Aloud" button to selected text toolbar
2. Use Web Speech API (existing implementation)
3. Highlight text as it's being read

### 4.3 Visual Adjustments
**Implementation**:
1. Inject CSS variables into page `<head>`
2. Modify existing elements' styles:
   - Font size: Update all text elements
   - Line spacing: Apply to paragraphs, headings
   - Letter spacing: Apply globally
   - Color overlays: Semi-transparent overlay div
   - High contrast: CSS filter overrides

### 4.4 Font Family Changes
**Implementation**:
1. Load custom fonts (OpenDyslexic) via @font-face
2. Apply font-family to document root
3. Store font preferences in chrome.storage

---

## Phase 5: Integration & Testing

### 5.1 Backend Integration
**Tasks**:
- Ensure FastAPI CORS allows extension origins
- Test API calls from extension context
- Handle offline/error scenarios
- Add retry logic for failed requests

### 5.2 Cross-Browser Compatibility
**Test Sites**:
- News websites (CNN, BBC)
- Documentation sites (MDN, W3C)
- Social media (Twitter, Facebook)
- E-commerce (Amazon, eBay)
- Government sites (.gov domains)

### 5.3 Performance Optimization
**Metrics**:
- Page load impact < 100ms
- Memory usage < 50MB
- CPU usage minimal during idle
- Smooth scrolling maintained

---

## Phase 6: Build & Packaging

### 6.1 Build Configuration
**File**: `extension/webpack.config.js`
- Bundle TypeScript/React files
- Minify JavaScript/CSS
- Copy static assets
- Generate source maps

### 6.2 Extension Packaging
**Commands**:
```bash
# Development
npm run build:dev

# Production
npm run build:prod

# Package for Chrome Web Store
npm run package
```

### 6.3 Chrome Web Store Submission
**Requirements**:
- 440x280px promotional images
- Detailed description
- Privacy policy
- Screenshots (6 recommended)
- Category: Accessibility

---

## File Creation Checklist

### Root Extension Files
- [ ] extension/manifest.json
- [ ] extension/background.js
- [ ] extension/package.json
- [ ] extension/webpack.config.js

### Popup Components
- [ ] extension/popup/popup.html
- [ ] extension/popup/popup.jsx
- [ ] extension/popup/popup.css
- [ ] extension/popup/components/QuickSettings.jsx

### Content Scripts
- [ ] extension/content/content.js
- [ ] extension/content/accessibility-panel.tsx
- [ ] extension/content/styles/injected.css

### Services
- [ ] extension/services/api.js
- [ ] extension/services/storage.js
- [ ] extension/services/tts-service.js

### Utilities
- [ ] extension/utils/dom-utils.js
- [ ] extension/utils/style-utils.js

### Assets
- [ ] extension/icons/icon48.png
- [ ] extension/icons/icon128.png
- [ ] extension/icons/banner.png

---

## Migration Strategy

### From Existing Codebase
1. **Copy**: `frontend/src/components/AccessibilityPanel/` → `extension/content/`
2. **Adapt**: Modify to work without React app wrapper
3. **Reuse**: `frontend/src/services/api.ts` → `extension/services/api.js`
4. **Port**: TTS/STT logic from `frontend/src/hooks/` → `extension/services/`

### Backend Compatibility
- Keep existing FastAPI routes unchanged
- Add extension-specific endpoints if needed
- Update CORS to allow chrome-extension:// origins

---

## Timeline Estimate

| Phase | Tasks | Estimated Time |
|-------|-------|----------------|
| Phase 1 | Structure setup | 2-3 hours |
| Phase 2 | Core files | 4-5 hours |
| Phase 3 | Services | 2-3 hours |
| Phase 4 | Features | 6-8 hours |
| Phase 5 | Testing | 3-4 hours |
| Phase 6 | Packaging | 2-3 hours |
| **Total** | | **19-26 hours** |

---

## Success Criteria

✅ Extension installs without errors  
✅ Popup opens and shows settings  
✅ Content script injects on all websites  
✅ Text simplification works via right-click menu  
✅ TTS reads selected text aloud  
✅ Font/size adjustments apply globally  
✅ Settings persist across browser sessions  
✅ No console errors on major websites  
✅ Memory usage stays under 50MB  
✅ Chrome Web Store approval received  

---

## Next Steps After Confirmation

1. Create extension directory structure
2. Implement manifest.json and core files
3. Build MVP features (text simplification + TTS)
4. Test on 10+ different websites
5. Package and submit to Chrome Web Store