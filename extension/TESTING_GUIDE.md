# 🎉 Your Chrome Extension is Ready!

## ✅ Build Status: COMPLETE

The extension has been successfully built and is ready to test!

---

## 📦 Location of Built Files

All files are in: `extension/dist/`

```
extension/dist/
├── manifest.json
├── background.js
├── content/
│   └── content.js
├── popup/
│   ├── popup.html
│   ├── popup.css
│   └── popup.js
├── styles/
│   └── injected.css
└── icons/
    └── icon.svg
```

---

## 🚀 How to Load in Chrome

### Step 1: Open Chrome Extensions Page
1. Open Google Chrome browser
2. In the address bar, type: `chrome://extensions/`
3. Press Enter

### Step 2: Enable Developer Mode
1. Look for "Developer mode" toggle in the top right corner
2. Click to enable it (toggle should turn blue)

### Step 3: Load the Extension
1. Click the "Load unpacked" button that appears
2. Navigate to your extension folder:
   ```
   C:\Users\Shashank\OneDrive\Desktop\shashank\accenture\Adaptive-Accessibility-Intelligence-AAI-\extension\dist
   ```
3. Click "Select Folder" or "Open"

### Step 4: Verify Installation
✅ You should see "AAI - Adaptive Accessibility Intelligence" in the extensions list  
✅ Extension icon should appear in Chrome toolbar (top right)  
✅ If you don't see the icon, click the puzzle piece icon → pin the AAI extension

---

## ⚙️ Start the Backend Server

The extension needs the FastAPI backend running:

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Verify backend is running:**
- Open: http://localhost:8000/health
- Should show: `{"status": "healthy", ...}`

---

## 🧪 Test the Extension

### Test 1: Popup Settings
1. Click the AAI extension icon in toolbar
2. You should see the settings panel with:
   - Font size slider
   - Line spacing slider
   - Letter spacing slider
   - Font family dropdown
   - Color overlay options
   - High contrast, Dark mode toggles
3. Adjust a slider → navigate to any website → see if changes apply

### Test 2: Context Menu
1. Go to any website with text (e.g., https://www.wikipedia.org)
2. Select some text with your mouse
3. Right-click on selected text
4. You should see menu options:
   - "Simplify with AAI"
   - "Read Aloud with AAI"
5. Click one to test!

### Test 3: Visual Changes
1. Navigate to a news website (CNN, BBC, etc.)
2. Click extension icon
3. Change font size to 24px
4. Enable high contrast mode
5. Select "Sepia" color overlay
6. Check if the page appearance changes

### Test 4: Floating Panel
1. After loading the extension, a floating panel should appear on webpages
2. It should have buttons:
   - "Simplify Text"
   - "Read Aloud"
   - "Settings"
3. Try clicking these buttons

---

## 🔍 Debugging Tips

### If Extension Doesn't Load:
1. Check Chrome console for errors:
   - Go to `chrome://extensions/`
   - Find AAI extension
   - Click "Errors" button (if visible)
   
2. Reload the extension:
   - Click the refresh icon on the extension card
   - Refresh the webpage you're testing on

### If Features Don't Work:
1. **Check Backend Connection**:
   - Click extension icon
   - Look for status indicator (green dot = online, red = offline)
   - If red, start the backend server

2. **Check Browser Console**:
   - Press F12 to open DevTools
   - Go to Console tab
   - Look for AAI-related messages

3. **Check Permissions**:
   - Go to `chrome://extensions/`
   - Click "Details" on AAI extension
   - Verify permissions include:
     - "Access your data for all websites"
     - "Display notifications" (optional)

### If Settings Don't Persist:
1. Check Chrome storage:
   - Open DevTools (F12)
   - Go to Application tab
   - Expand "Chrome Storage" → "Sync"
   - You should see AAI settings listed

---

## 🎯 Quick Feature Test Checklist

Copy this checklist and test each feature:

```
□ Extension loads without errors
□ Popup opens when clicking extension icon
□ Backend status indicator shows (green/red dot)
□ Font size slider changes text on websites
□ Line spacing adjustment works
□ High contrast mode toggle functions
□ Dark mode applies to websites
□ Right-click context menu appears on selected text
□ "Simplify with AAI" sends request to backend
□ "Read Aloud" plays audio
□ Floating panel appears on webpages
□ Settings persist after closing Chrome
```

---

## 🐛 Common Issues & Fixes

### Issue: "Backend offline" shown
**Fix**: Start the FastAPI backend server

### Issue: Context menu doesn't appear
**Fix**: Make sure you're selecting actual text (not images)

### Issue: Settings don't apply to page
**Fix**: Refresh the webpage after changing settings

### Issue: Can't see extension icon
**Fix**: Click puzzle piece icon → Pin AAI to toolbar

### Issue: "Failed to simplify text" error
**Fix**: 
1. Verify backend is running at http://localhost:8000
2. Check CORS settings in backend config
3. Look at browser console for detailed error

---

## 📝 Next Steps After Testing

1. **Create PNG Icons**:
   - Convert icon.svg to PNG (48x48px and 128x128px)
   - Place in `extension/icons/` folder
   - Rebuild: `npm run build`

2. **Test on Multiple Sites**:
   - News: CNN, BBC, New York Times
   - Documentation: MDN, W3C
   - E-commerce: Amazon, eBay
   - Social Media: Twitter, Facebook

3. **Fix Any Bugs Found**:
   - Note which websites have issues
   - Check browser console for errors
   - Update code and rebuild

4. **Package for Chrome Web Store** (when ready):
   ```bash
   npm run package
   ```
   This creates `aai-extension-v1.0.0.zip`

---

## 💡 Pro Tips

1. **Hot Reload During Development**:
   ```bash
   npm run build:dev
   ```
   Automatically rebuilds when you change files

2. **Debug Specific Components**:
   - **Popup**: Right-click extension icon → "Inspect popup"
   - **Background**: chrome://extensions/ → Details → "Service Worker" → "Inspect"
   - **Content Script**: F12 on any webpage → Console tab

3. **Quick Reset**:
   If something breaks:
   - Go to chrome://extensions/
   - Remove the extension
   - Rebuild: `npm run build`
   - Reload extension

---

## 🎉 Success Indicators

You'll know everything is working when:
- ✅ Extension icon visible in toolbar
- ✅ Popup opens with all settings
- ✅ Green dot showing backend online
- ✅ Right-click menu shows AAI options
- ✅ Font/size changes apply to websites
- ✅ Text simplification returns results
- ✅ Read aloud plays audio

---

## 📞 Need Help?

If you encounter issues:
1. Check browser console (F12 → Console tab)
2. Review extension README: `extension/README.md`
3. See full documentation: `extension/CHROME_EXTENSION_SUMMARY.md`
4. Check main project docs: `/docs/` folder

---

**Happy Testing! 🚀**

Extension Version: 1.0.0  
Build Date: March 30, 2026  
Status: Ready for Testing
