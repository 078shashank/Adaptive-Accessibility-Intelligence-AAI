# AAI Chrome Extension

Adaptive Accessibility Intelligence (AAI) - Chrome Extension for reading assistance and accessibility support.

## Features

### MVP Features (v1.0)
- **Text Simplification**: AI-powered text simplification using your local FastAPI backend
- **Text-to-Speech**: Read selected text aloud with adjustable speech rate
- **Font Adjustments**: Change font size, family, line spacing, and letter spacing
- **Visual Overlays**: Color overlays for visual comfort (blue, green, yellow, sepia)
- **Display Modes**: High contrast mode, dark mode, reduced motion
- **Context Menu**: Right-click to simplify or read aloud any selected text
- **Floating Panel**: Quick access toolbar on every webpage

## Installation

### Development Installation

1. **Build the extension**:
```bash
cd extension
npm install
npm run build:dev  # For development with auto-reload
# Or use: npm run build  # For production build
```

2. **Load in Chrome**:
   - Open Chrome and navigate to `chrome://extensions/`
   - Enable "Developer mode" (toggle in top right)
   - Click "Load unpacked"
   - Select the `extension/dist` folder
   - Extension icon should appear in toolbar

### Production Installation

1. **Package the extension**:
```bash
npm run package
```

2. **Upload to Chrome Web Store** (coming soon)

## Backend Requirements

The extension requires the AAI FastAPI backend running locally:

```bash
# Setup Python virtual environment (recommended)
cd ../backend
python -m venv venv

# Activate virtual environment
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Command Prompt:
venv\Scripts\activate.bat
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the backend server
uvicorn app.main:app --reload
```

Backend should be accessible at `http://localhost:8000`

Verify backend is running: http://localhost:8000/health

## Usage

### Quick Settings (Popup)
1. Click the AAI extension icon in toolbar
2. Adjust font size, spacing, colors using sliders
3. Toggle display modes (high contrast, dark mode, etc.)
4. Enable text simplification and select reading level

### Context Menu
1. Select any text on a webpage
2. Right-click
3. Choose "Simplify with AAI" or "Read Aloud with AAI"

### Floating Panel
- The panel appears automatically when extension is enabled
- Click buttons to simplify text or read aloud
- Drag to reposition
- Click X to close (can reopen from popup)

## File Structure

```
extension/
├── manifest.json              # Extension configuration
├── background.js              # Service worker
├── content/
│   └── content.js            # Content script (injected into pages)
├── popup/
│   ├── popup.html            # Popup UI
│   ├── popup.css             # Popup styles
│   └── popup.js              # Popup logic
├── services/
│   ├── api.js                # Backend API client
│   └── storage.js            # Chrome storage wrapper
├── utils/
│   └── dom-utils.js          # DOM manipulation helpers
├── styles/
│   └── injected.css          # Styles applied to web pages
├── icons/                     # Extension icons
└── fonts/                     # Custom fonts (OpenDyslexic)
```

## Permissions

- `activeTab`: Access current tab for applying settings
- `storage`: Save user preferences across sessions
- `scripting`: Inject content scripts into web pages
- `contextMenus`: Add right-click menu options
- `<all_urls>`: Work on all websites

## Privacy

- All data stored locally in Chrome storage
- No data sent to external servers except your local backend
- Text simplification requests sent to `localhost:8000` only
- No tracking or analytics

## Development

### Build Commands
```bash
# Development build with watch mode
npm run build:dev

# Production build
npm run build:prod

# Package for distribution
npm run package
```

### Debugging

1. **Popup**: Right-click extension icon → "Inspect popup"
2. **Background**: Go to `chrome://extensions/` → Details → "Service Worker" → "Inspect"
3. **Content Script**: Open DevTools on any webpage → Console tab

## Troubleshooting

### Backend Not Connecting
- Ensure backend is running: `http://localhost:8000/health`
- Check CORS settings allow extension origins
- Verify no firewall blocking localhost connections

### Features Not Working
- Reload the extension from `chrome://extensions/`
- Refresh the webpage
- Check browser console for errors

### Settings Not Persisting
- Check if Chrome storage sync is enabled
- Try clearing extension data and reconfiguring

## Roadmap

### v1.1 (Coming Soon)
- [ ] Full settings panel page
- [ ] Import/export settings
- [ ] Keyboard shortcuts
- [ ] Multiple language support

### v2.0 (Future)
- [ ] Sign language avatar integration
- [ ] Guided mode wizard
- [ ] Predictive typing
- [ ] Cloud sync for settings

## Known Issues

- Some features may not work on certain websites with strict CSP
- React-based sites may require page refresh after setting changes
- PDF viewer not supported

## Contributing

Contributions welcome! Please see main repository:
https://github.com/078shashank/Adaptive-Accessibility-Intelligence-AAI

## License

MIT License - See main repository for details

## Support

For issues or questions:
- GitHub Issues: https://github.com/078shashank/Adaptive-Accessibility-Intelligence-AAI/issues
- Documentation: https://github.com/078shashank/Adaptive-Accessibility-Intelligence-AAI/blob/main/README.md

---

**Version**: 1.0.0  
**Last Updated**: March 2026  
**Author**: 078shashank
