/** Accessibility Control Panel Component */
import React from 'react';
import { AccessibilitySettings } from '../../types/accessibility';

interface AccessibilityPanelProps {
  settings: AccessibilitySettings;
  onSettingChange: (key: keyof AccessibilitySettings, value: any) => void;
  onReset: () => void;
}

export const AccessibilityPanel: React.FC<AccessibilityPanelProps> = ({
  settings,
  onSettingChange,
  onReset,
}) => {
  return (
    <aside
      aria-label="Accessibility Controls"
      className="accessibility-panel"
    >
      <h2>Accessibility Controls</h2>

      {/* Visual Adjustments */}
      <section>
        <h3 id="visual-heading">Visual Adjustments</h3>
        <fieldset aria-labelledby="visual-heading">
          <div className="control-group">
            <label htmlFor="font-size">
              Font Size: {settings.fontSize}px
            </label>
            <input
              id="font-size"
              type="range"
              min="12"
              max="32"
              value={settings.fontSize}
              onChange={(e) => onSettingChange('fontSize', parseInt(e.target.value))}
              aria-label="Font size"
              aria-valuemin={12}
              aria-valuemax={32}
              aria-valuenow={settings.fontSize}
            />
          </div>

          <div className="control-group">
            <label htmlFor="line-spacing">
              Line Spacing: {settings.lineSpacing.toFixed(1)}x
            </label>
            <input
              id="line-spacing"
              type="range"
              min="1.0"
              max="3.0"
              step="0.1"
              value={settings.lineSpacing}
              onChange={(e) => onSettingChange('lineSpacing', parseFloat(e.target.value))}
              aria-label="Line spacing"
              aria-valuemin={1.0}
              aria-valuemax={3.0}
              aria-valuenow={settings.lineSpacing}
            />
          </div>

          <div className="control-group">
            <label htmlFor="letter-spacing">
              Letter Spacing: {settings.letterSpacing.toFixed(1)}px
            </label>
            <input
              id="letter-spacing"
              type="range"
              min="0.0"
              max="2.0"
              step="0.1"
              value={settings.letterSpacing}
              onChange={(e) => onSettingChange('letterSpacing', parseFloat(e.target.value))}
              aria-label="Letter spacing"
              aria-valuemin={0.0}
              aria-valuemax={2.0}
              aria-valuenow={settings.letterSpacing}
            />
          </div>

          <div className="control-group">
            <label htmlFor="font-family">Font Family</label>
            <select
              id="font-family"
              value={settings.fontFamily}
              onChange={(e) => onSettingChange('fontFamily', e.target.value)}
              aria-label="Select font family"
            >
              <option value="system">System Default</option>
              <option value="OpenDyslexic">OpenDyslexic (Dyslexia-Friendly)</option>
              <option value="Arial">Arial</option>
              <option value="Georgia">Georgia</option>
              <option value="Verdana">Verdana</option>
              <option value="Trebuchet">Trebuchet MS</option>
            </select>
          </div>

          <div className="control-group">
            <label htmlFor="color-overlay">Color Overlay</label>
            <select
              id="color-overlay"
              value={settings.colorOverlay}
              onChange={(e) => onSettingChange('colorOverlay', e.target.value)}
              aria-label="Select color overlay"
            >
              <option value="none">None</option>
              <option value="blue">Light Blue</option>
              <option value="green">Green</option>
              <option value="yellow">Yellow</option>
              <option value="sepia">Sepia</option>
            </select>
          </div>

          <div className="control-group">
            <label htmlFor="high-contrast">
              <input
                id="high-contrast"
                type="checkbox"
                checked={settings.highContrastMode}
                onChange={(e) => onSettingChange('highContrastMode', e.target.checked)}
                aria-label="Enable high contrast mode"
              />
              High Contrast Mode
            </label>
          </div>

          <div className="control-group">
            <label htmlFor="dark-mode">
              <input
                id="dark-mode"
                type="checkbox"
                checked={settings.darkMode}
                onChange={(e) => onSettingChange('darkMode', e.target.checked)}
                aria-label="Enable dark mode"
              />
              Dark Mode
            </label>
          </div>
        </fieldset>
      </section>

      {/* Content Controls */}
      <section>
        <h3 id="content-heading">Content</h3>
        <fieldset aria-labelledby="content-heading">
          <div className="control-group">
            <label htmlFor="simplify-text">
              <input
                id="simplify-text"
                type="checkbox"
                checked={settings.simplifyText}
                onChange={(e) => onSettingChange('simplifyText', e.target.checked)}
                aria-label="Enable text simplification"
              />
              Simplify Text
            </label>
          </div>

          <div className="control-group">
            <label htmlFor="reading-level">Reading Level</label>
            <select
              id="reading-level"
              value={settings.readingLevel}
              onChange={(e) => onSettingChange('readingLevel', e.target.value)}
              aria-label="Select reading level"
            >
              <option value="basic">Basic</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
            </select>
          </div>
        </fieldset>
      </section>

      {/* Interaction Controls */}
      <section>
        <h3 id="interaction-heading">Interaction</h3>
        <fieldset aria-labelledby="interaction-heading">
          <div className="control-group">
            <label htmlFor="speech-rate">
              Speech Rate: {settings.speechRate.toFixed(1)}x
            </label>
            <input
              id="speech-rate"
              type="range"
              min="0.5"
              max="2.0"
              step="0.1"
              value={settings.speechRate}
              onChange={(e) => onSettingChange('speechRate', parseFloat(e.target.value))}
              aria-label="Speech rate"
              aria-valuemin={0.5}
              aria-valuemax={2.0}
              aria-valuenow={settings.speechRate}
            />
          </div>
        </fieldset>
      </section>

      {/* Motion & Sensory */}
      <section>
        <h3 id="motion-heading">Motion & Sensory</h3>
        <fieldset aria-labelledby="motion-heading">
          <div className="control-group">
            <label htmlFor="reduce-motion">
              <input
                id="reduce-motion"
                type="checkbox"
                checked={settings.reduceMotion}
                onChange={(e) => onSettingChange('reduceMotion', e.target.checked)}
                aria-label="Enable reduce motion"
              />
              Reduce Motion
            </label>
          </div>

          <div className="control-group">
            <label htmlFor="reduce-animation">
              <input
                id="reduce-animation"
                type="checkbox"
                checked={settings.reduceAnimation}
                onChange={(e) => onSettingChange('reduceAnimation', e.target.checked)}
                aria-label="Enable reduce animation"
              />
              Reduce Animation
            </label>
          </div>

          <div className="control-group">
            <label htmlFor="sound-enabled">
              <input
                id="sound-enabled"
                type="checkbox"
                checked={settings.soundEnabled}
                onChange={(e) => onSettingChange('soundEnabled', e.target.checked)}
                aria-label="Enable sound"
              />
              Enable Sound
            </label>
          </div>

          <div className="control-group">
            <label htmlFor="vibration-enabled">
              <input
                id="vibration-enabled"
                type="checkbox"
                checked={settings.vibrationEnabled}
                onChange={(e) => onSettingChange('vibrationEnabled', e.target.checked)}
                aria-label="Enable vibration"
              />
              Enable Vibration
            </label>
          </div>
        </fieldset>
      </section>

      {/* Advanced Controls */}
      <section>
        <details>
          <summary id="advanced-heading">Advanced Options</summary>
          <fieldset aria-labelledby="advanced-heading">
            <div className="control-group">
              <label htmlFor="minimal-mode">
                <input
                  id="minimal-mode"
                  type="checkbox"
                  checked={settings.minimalMode}
                  onChange={(e) => onSettingChange('minimalMode', e.target.checked)}
                  aria-label="Enable minimal mode"
                />
                Minimal Mode
              </label>
            </div>

            <div className="control-group">
              <label htmlFor="guided-mode">
                <input
                  id="guided-mode"
                  type="checkbox"
                  checked={settings.guidedMode}
                  onChange={(e) => onSettingChange('guidedMode', e.target.checked)}
                  aria-label="Enable guided mode"
                />
                Guided Mode
              </label>
            </div>

            <div className="control-group">
              <label htmlFor="show-avatar">
                <input
                  id="show-avatar"
                  type="checkbox"
                  checked={settings.showAvatar}
                  onChange={(e) => onSettingChange('showAvatar', e.target.checked)}
                  aria-label="Show sign language avatar"
                />
                Show Sign Language Avatar
              </label>
            </div>
          </fieldset>
        </details>
      </section>

      {/* Reset Button */}
      <button
        className="reset-button"
        onClick={onReset}
        aria-label="Reset all accessibility settings to defaults"
      >
        Reset All Settings
      </button>
    </aside>
  );
};
