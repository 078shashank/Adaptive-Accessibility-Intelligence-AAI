/** Main Content Area Component */
import React, { useState } from 'react';
import { textService } from '../../services/api';
import { AccessibilitySettings } from '../../types/accessibility';
import SignLanguageAvatar from '../SignLanguageAvatar/SignLanguageAvatar';

interface MainContentProps {
  settings: AccessibilitySettings;
}

export const MainContent: React.FC<MainContentProps> = ({ settings }) => {
  const [inputText, setInputText] = useState('');
  const [simplifiedText, setSimplifiedText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [speechActive, setSpeechActive] = useState(false);
  const [showAvatar, setShowAvatar] = useState(false);

  const handleSimplify = async () => {
    if (!inputText.trim()) {
      setError('Please enter some text');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const result = await textService.simplify(inputText, settings.readingLevel);
      setSimplifiedText(result.simplified_text);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to simplify text');
    } finally {
      setLoading(false);
    }
  };

  const handleReadAloud = () => {
    if (!simplifiedText) {
      setError('Please simplify text first');
      return;
    }

    const utterance = new SpeechSynthesisUtterance(simplifiedText);
    utterance.rate = settings.speechRate;

    utterance.onstart = () => setSpeechActive(true);
    utterance.onend = () => setSpeechActive(false);
    utterance.onerror = (event) => {
      setError(`Speech error: ${event.error}`);
      setSpeechActive(false);
    };

    if (settings.soundEnabled) {
      window.speechSynthesis.speak(utterance);
    } else {
      setError('Sound is disabled in accessibility settings');
    }
  };

  const handleDictate = () => {
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SpeechRecognition) {
      setError('Speech recognition not supported in this browser');
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.start();

    recognition.onresult = (event: any) => {
      const transcript = Array.from(event.results)
        .map((result: any) => result[0].transcript)
        .join('');
      setInputText((prev) => prev + ' ' + transcript);
    };

    recognition.onerror = (event: any) => {
      setError(`Speech recognition error: ${event.error}`);
    };
  };

  const handleCopy = async () => {
    if (!simplifiedText) {
      setError('No text to copy');
      return;
    }

    try {
      // Try modern Clipboard API first
      await navigator.clipboard.writeText(simplifiedText);
      setError('Copied to clipboard!');
    } catch (err) {
      // Fallback for older browsers or restricted contexts
      try {
        const textArea = document.createElement('textarea');
        textArea.value = simplifiedText;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        textArea.style.top = '-999999px';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        
        const successful = document.execCommand('copy');
        document.body.removeChild(textArea);
        
        if (successful) {
          setError('Copied to clipboard!');
        } else {
          setError('Failed to copy text');
        }
      } catch (fallbackError) {
        setError('Unable to copy. Please select and copy manually.');
      }
    }
    
    // Clear message after 2 seconds
    setTimeout(() => setError(''), 2000);
  };

  return (
    <main id="main-content" role="main">
      {/* Text Input Section */}
      <section aria-labelledby="input-heading">
        <h1 id="input-heading">Text Input</h1>
        <textarea
          aria-label="Paste complex text here"
          aria-describedby="input-help"
          placeholder="Paste complex text or article here..."
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          style={{
            minHeight: '150px',
            fontSize: `${settings.fontSize}px`,
            lineHeight: `${settings.lineSpacing}`,
            letterSpacing: `${settings.letterSpacing}px`,
          }}
        />
        <p id="input-help" className="help-text">
          Paste any complex text. We'll simplify it for you.
        </p>
        <button
          onClick={handleSimplify}
          disabled={loading || !inputText.trim()}
          aria-label="Simplify this text"
        >
          {loading ? 'Simplifying...' : 'Simplify This Text'}
        </button>
      </section>

      {/* Error Display */}
      {error && (
        <div
          role="alert"
          aria-live="polite"
          className={`message ${error.includes('Copied') ? 'success' : 'error'}`}
        >
          {error}
        </div>
      )}

      {/* Sign Language Avatar */}
      {settings.showAvatar && simplifiedText && (
        <SignLanguageAvatar
          text={simplifiedText}
          isVisible={showAvatar}
          onComplete={() => handleReadAloud()}
        />
      )}

      {/* Simplified Text Output */}
      {simplifiedText && (
        <section aria-labelledby="output-heading" className="results">
          <h2 id="output-heading">Simplified Text</h2>
          <div
            className="text-output"
            aria-live="polite"
            aria-label="Simplified text output"
            style={{
              fontSize: `${settings.fontSize}px`,
              lineHeight: `${settings.lineSpacing}`,
              letterSpacing: `${settings.letterSpacing}px`,
              fontFamily: settings.fontFamily,
              backgroundImage: `linear-gradient(180deg, var(--color-overlay) 0%, var(--color-overlay) 100%)`,
              backgroundColor: 'var(--bg-secondary)',
              padding: '1rem',
              borderRadius: '4px',
            }}
          >
            {simplifiedText}
          </div>

          <div className="controls" role="group" aria-label="Output actions">
            <button
              onClick={handleReadAloud}
              disabled={speechActive}
              aria-label="Read aloud (press R)"
              title="Keyboard shortcut: R"
            >
              🔊 {speechActive ? 'Reading...' : 'Read Aloud'}
            </button>
            <button
              onClick={handleCopy}
              aria-label="Copy to clipboard"
              title="Copy text"
            >
              📋 Copy
            </button>
            <button
              onClick={handleDictate}
              aria-label="Dictate text (press D)"
              title="Keyboard shortcut: D"
            >
              🎤 Dictate
            </button>
            {settings.showAvatar && (
              <button
                onClick={() => setShowAvatar(!showAvatar)}
                aria-label={showAvatar ? 'Hide sign language avatar' : 'Show sign language avatar'}
                title="Toggle sign language interpretation"
              >
                👋 {showAvatar ? 'Hide Avatar' : 'Show Avatar'}
              </button>
            )}
          </div>
        </section>
      )}

      {/* Status Bar */}
      <section aria-labelledby="status-heading" className="status-bar">
        <h2 id="status-heading" className="sr-only">Status</h2>
        <div aria-live="polite" aria-atomic="true">
          {loading ? '⏳ Processing...' : '✓ Ready'}
        </div>
      </section>
    </main>
  );
};
