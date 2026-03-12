/** Main App Component */
import React, { useEffect, useState } from 'react';
import { useAccessibilitySettings } from './hooks/useAccessibilitySettings';
import { AccessibilityPanel } from './components/AccessibilityPanel/AccessibilityPanel';
import { MainContent } from './components/MainContent/MainContent';
import { authService, healthService } from './services/api';
import './styles/index.css';

const App: React.FC = () => {
  const { settings, updateSetting, resetSettings, loaded } = useAccessibilitySettings();
  const [, setAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  // Check health and login on mount
  useEffect(() => {
    const initialize = async () => {
      try {
        // Check backend health
        await healthService.check();

        // Try demo login
        const token = localStorage.getItem('access_token');
        if (!token) {
          // Auto-login with demo credentials
          try {
            await authService.login('demo@aai.com', 'demo123456');
            setAuthenticated(true);
          } catch (err) {
            // If demo user doesn't exist, register and login
            try {
              await authService.register('demo@aai.com', 'demo123456', 'Demo User');
              await authService.login('demo@aai.com', 'demo123456');
              setAuthenticated(true);
            } catch (regErr) {
              console.warn('Auto-login failed:', regErr);
            }
          }
        } else {
          setAuthenticated(true);
        }
      } catch (err) {
        console.warn('Backend not available:', err);
      } finally {
        setLoading(false);
      }
    };

    if (loaded) {
      initialize();
    }
  }, [loaded]);

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'r' || e.key === 'R') {
        const readAloudBtn = document.querySelector('[aria-label*="Read aloud"]') as HTMLButtonElement;
        if (readAloudBtn && !readAloudBtn.disabled) {
          e.preventDefault();
          readAloudBtn.click();
        }
      }
      if (e.key === 'd' || e.key === 'D') {
        const dictateBtn = document.querySelector('[aria-label*="Dictate"]') as HTMLButtonElement;
        if (dictateBtn) {
          e.preventDefault();
          dictateBtn.click();
        }
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="app-container" style={{ display: 'flex', minHeight: '100vh' }}>
      <AccessibilityPanel
        settings={settings}
        onSettingChange={updateSetting}
        onReset={resetSettings}
      />
      <MainContent settings={settings} />
    </div>
  );
};

export default App;
