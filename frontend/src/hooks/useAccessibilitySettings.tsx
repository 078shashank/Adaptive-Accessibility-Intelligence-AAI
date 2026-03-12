/** Accessibility Settings Hook */
import { useState, useEffect } from 'react';
import { AccessibilitySettings } from '../types/accessibility';

const DEFAULT_SETTINGS: AccessibilitySettings = {
  fontSize: 16,
  lineSpacing: 1.5,
  letterSpacing: 0,
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
  showAvatar: false,
};

export const useAccessibilitySettings = () => {
  const [settings, setSettings] = useState<AccessibilitySettings>(DEFAULT_SETTINGS);
  const [loaded, setLoaded] = useState(false);

  // Load settings from localStorage on mount
  useEffect(() => {
    const stored = localStorage.getItem('accessibilitySettings');
    if (stored) {
      try {
        setSettings(JSON.parse(stored));
      } catch (e) {
        console.error('Failed to parse accessibility settings:', e);
      }
    }
    setLoaded(true);
  }, []);

  // Update a single setting
  const updateSetting = (key: keyof AccessibilitySettings, value: any) => {
    setSettings((prev) => {
      const updated = { ...prev, [key]: value };
      // Apply CSS changes immediately
      applyCSSSettings(updated);
      // Save to localStorage
      localStorage.setItem('accessibilitySettings', JSON.stringify(updated));
      return updated;
    });
  };

  // Reset all settings
  const resetSettings = () => {
    setSettings(DEFAULT_SETTINGS);
    localStorage.removeItem('accessibilitySettings');
    applyCSSSettings(DEFAULT_SETTINGS);
  };

  return {
    settings,
    updateSetting,
    resetSettings,
    loaded,
  };
};

export const applyCSSSettings = (settings: AccessibilitySettings) => {
  const root = document.documentElement;

  // Font size
  root.style.setProperty('--font-size', `${settings.fontSize}px`);

  // Line spacing
  root.style.setProperty('--line-spacing', `${settings.lineSpacing}`);

  // Letter spacing
  root.style.setProperty('--letter-spacing', `${settings.letterSpacing}px`);

  // Font family
  const fontMap: Record<string, string> = {
    system: 'system-ui, -apple-system, sans-serif',
    'OpenDyslexic': 'OpenDyslexic, sans-serif',
    'Arial': 'Arial, sans-serif',
    'Georgia': 'Georgia, serif',
    'Verdana': 'Verdana, sans-serif',
    'Trebuchet': 'Trebuchet MS, sans-serif',
  };
  root.style.setProperty('--font-family', fontMap[settings.fontFamily] || fontMap.system);

  // Color overlay
  const overlayMap: Record<string, string> = {
    none: 'transparent',
    blue: 'rgba(173, 216, 230, 0.15)',
    green: 'rgba(144, 238, 144, 0.15)',
    yellow: 'rgba(255, 255, 153, 0.15)',
    sepia: 'rgba(139, 90, 43, 0.15)',
  };
  root.style.setProperty('--color-overlay', overlayMap[settings.colorOverlay] || 'transparent');

  // High contrast mode
  if (settings.highContrastMode) {
    document.body.classList.add('high-contrast-mode');
  } else {
    document.body.classList.remove('high-contrast-mode');
  }

  // Dark mode
  if (settings.darkMode) {
    document.body.classList.add('dark-mode');
  } else {
    document.body.classList.remove('dark-mode');
  }

  // Reduce motion
  if (settings.reduceMotion) {
    root.style.setProperty('--transition-duration', '0s');
  } else {
    root.style.setProperty('--transition-duration', '0.2s');
  }

  // Reduce animation
  if (settings.reduceAnimation) {
    document.body.classList.add('reduce-animation');
  } else {
    document.body.classList.remove('reduce-animation');
  }

  // Minimal mode
  if (settings.minimalMode) {
    document.body.classList.add('minimal-mode');
  } else {
    document.body.classList.remove('minimal-mode');
  }
};
