/**
 * Sign Language Avatar Component
 * Display sign language interpretation of text for deaf/hard of hearing users
 */

import React, { useState, useEffect } from 'react';
import { avatarService } from '../../services/api';
import { getSignAnimation } from '../../services/aslSignDatabase';

interface Animation {
  word: string;
  video?: string;
  letters?: string[];
  type?: string;
  duration: number;
  recognized: boolean;
}

interface AvatarData {
  text: string;
  word_count: number;
  recognized_words: number;
  unrecognized_words: string[];
  total_duration_seconds: number;
  animation_data: {
    animations: Animation[];
  };
  avatar_speed: string;
}

interface SignLanguageAvatarProps {
  text: string;
  onComplete?: () => void;
  isVisible: boolean;
}

interface HandPosition {
  left: { x: number; y: number; rotation: number; spread: number };
  right: { x: number; y: number; rotation: number; spread: number };
  bodyRotation: number;
}

export const SignLanguageAvatar: React.FC<SignLanguageAvatarProps> = ({
  text,
  onComplete,
  isVisible,
}) => {
  const [loading, setLoading] = useState(false);
  const [avatarData, setAvatarData] = useState<AvatarData | null>(null);
  const [currentWordIndex, setCurrentWordIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [handPosition, setHandPosition] = useState<HandPosition>({
    left: { x: 0, y: 0, rotation: 0, spread: 0 },
    right: { x: 0, y: 0, rotation: 0, spread: 0 },
    bodyRotation: 0,
  });

  useEffect(() => {
    if (text && isVisible) {
      generateAvatarAnimation();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [text, isVisible]);

  const generateAvatarAnimation = async () => {
    if (!text.trim()) {
      setError('Please provide text for sign language interpretation');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await avatarService.generateSignAnimation(text);
      setAvatarData(response.avatar_data);
      setCurrentWordIndex(0);
    } catch (err) {
      setError('Failed to generate sign language animation. Please try again.');
      console.error('Avatar generation error:', err);
    } finally {
      setLoading(false);
    }
  };

  const playAnimation = () => {
    if (!avatarData) return;

    setIsPlaying(true);
    let wordIndex = 0;

    const playNextWord = () => {
      if (wordIndex < avatarData.animation_data.animations.length) {
        setCurrentWordIndex(wordIndex);
        const animation = avatarData.animation_data.animations[wordIndex];
        const word = animation.word;

        // Get the ASL sign animation for this word
        const signAnimation = getSignAnimation(word);

        if (signAnimation) {
          animateSignFrames(signAnimation.frames, signAnimation.duration || 1000, () => {
            wordIndex++;
            playNextWord();
          });
        } else {
          wordIndex++;
          playNextWord();
        }
      } else {
        setIsPlaying(false);
        setCurrentWordIndex(0);
        if (onComplete) {
          onComplete();
        }
      }
    };

    playNextWord();
  };

  const animateSignFrames = (
    frames: any[],
    duration: number,
    onComplete: () => void
  ) => {
    const startTime = Date.now();
    const frameCount = frames.length;
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    let animationFrameId: ReturnType<typeof setTimeout>;

    const updateFrame = () => {
      const elapsed = Date.now() - startTime;
      const progress = Math.min(elapsed / duration, 1);

      // Calculate current frame index
      const frameProgress = progress * (frameCount - 1);
      const currentFrame = Math.floor(frameProgress);
      const nextFrame = Math.min(currentFrame + 1, frameCount - 1);
      const frameLerp = frameProgress - currentFrame;

      // Get frames
      const frame1 = frames[currentFrame];
      const frame2 = frames[nextFrame];

      // Interpolate between frames
      const interpolatedPosition: HandPosition = {
        left: {
          x:
            frame1.left.x +
            (frame2.left.x - frame1.left.x) * frameLerp,
          y:
            frame1.left.y +
            (frame2.left.y - frame1.left.y) * frameLerp,
          rotation:
            frame1.left.rotation +
            (frame2.left.rotation - frame1.left.rotation) * frameLerp,
          spread:
            frame1.left.spread +
            (frame2.left.spread - frame1.left.spread) * frameLerp,
        },
        right: {
          x:
            frame1.right.x +
            (frame2.right.x - frame1.right.x) * frameLerp,
          y:
            frame1.right.y +
            (frame2.right.y - frame1.right.y) * frameLerp,
          rotation:
            frame1.right.rotation +
            (frame2.right.rotation - frame1.right.rotation) * frameLerp,
          spread:
            frame1.right.spread +
            (frame2.right.spread - frame1.right.spread) * frameLerp,
        },
        bodyRotation:
          frame1.bodyRotation +
          (frame2.bodyRotation - frame1.bodyRotation) * frameLerp,
      };

      setHandPosition(interpolatedPosition);

      if (progress < 1) {
        animationFrameId = setTimeout(updateFrame, 16); // ~60fps
      } else {
        onComplete();
      }
    };

    updateFrame();
  };

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const animateHands = (animation: Animation) => {
    // This function is intentionally left empty for backwards compatibility
    // Animation logic is now handled by animateSignFrames
    console.log('animateHands deprecated - use animateSignFrames instead');
  };

  const pauseAnimation = () => {
    setIsPlaying(false);
  };

  const resetAnimation = () => {
    setCurrentWordIndex(0);
    setIsPlaying(false);
  };

  if (!isVisible) {
    return null;
  }

  return (
    <div
      className="sign-language-avatar"
      role="region"
      aria-label="Sign language avatar interpretation"
    >
      <h3>Sign Language Interpretation (ASL)</h3>

      {error && (
        <div className="error-message" role="alert">
          {error}
        </div>
      )}

      {loading && (
        <div className="loading">
          <p>Generating sign language animation...</p>
        </div>
      )}

      {avatarData && !loading && (
        <div className="avatar-container">
          {/* Avatar Display Area */}
          <div className="avatar-display">
            <div className="avatar-placeholder">
              <svg
                viewBox="0 0 200 350"
                className="avatar-figure"
                aria-label={`Avatar showing sign for: ${avatarData.animation_data.animations[currentWordIndex]?.word}`}
              >
                {/* Background */}
                <rect width="200" height="350" fill="#fafafa" />
                
                {/* Body with rotation */}
                <g transform={`rotate(${handPosition.bodyRotation} 100 200)`}>
                  {/* Head */}
                  <circle cx="100" cy="50" r="25" fill="#8B4513" stroke="#654321" strokeWidth="2" />
                  
                  {/* Face */}
                  <circle cx="92" cy="45" r="3" fill="black" />
                  <circle cx="108" cy="45" r="3" fill="black" />
                  <path d="M 100 50 Q 100 55 95 57" stroke="black" strokeWidth="1.5" fill="none" />
                  
                  {/* Neck */}
                  <line x1="100" y1="75" x2="100" y2="90" stroke="#8B4513" strokeWidth="6" />
                  
                  {/* Main Body */}
                  <rect x="75" y="90" width="50" height="70" fill="#333" rx="5" />
                  
                  {/* Waist */}
                  <line x1="75" y1="160" x2="125" y2="160" stroke="#333" strokeWidth="4" />
                  
                  {/* Left leg */}
                  <line x1="85" y1="160" x2="80" y2="250" stroke="#444" strokeWidth="12" strokeLinecap="round" />
                  <circle cx="80" cy="260" r="10" fill="#333" />
                  
                  {/* Right leg */}
                  <line x1="115" y1="160" x2="120" y2="250" stroke="#444" strokeWidth="12" strokeLinecap="round" />
                  <circle cx="120" cy="260" r="10" fill="#333" />
                </g>

                {/* Left arm and hand with animation */}
                <g
                  transform={`translate(${handPosition.left.x}, ${handPosition.left.y}) rotate(${handPosition.left.rotation})`}
                  className="arm-group"
                >
                  {/* Left arm */}
                  <line x1="75" y1="105" x2="30" y2="120" stroke="#FFB6C1" strokeWidth="10" strokeLinecap="round" />
                  
                  {/* Left hand */}
                  <circle cx="30" cy="120" r="15" fill="#FFB6C1" stroke="#D4A5A5" strokeWidth="2" className="hand-animated" />
                  
                  {/* Fingers - spread based on spread value */}
                  <g className="fingers" style={{ opacity: Math.max(0.3, handPosition.left.spread / 100) }}>
                    <circle
                      cx={20 - (handPosition.left.spread / 100) * 5}
                      cy={110 - (handPosition.left.spread / 100) * 8}
                      r="4"
                      fill="#D4A5A5"
                      className="finger"
                    />
                    <circle
                      cx={15 - (handPosition.left.spread / 100) * 8}
                      cy={125}
                      r="4"
                      fill="#D4A5A5"
                      className="finger"
                    />
                    <circle
                      cx={25 + (handPosition.left.spread / 100) * 3}
                      cy={135}
                      r="4"
                      fill="#D4A5A5"
                      className="finger"
                    />
                    <circle
                      cx={40 + (handPosition.left.spread / 100) * 5}
                      cy={135}
                      r="4"
                      fill="#D4A5A5"
                      className="finger"
                    />
                  </g>
                </g>

                {/* Right arm and hand with animation */}
                <g
                  transform={`translate(${handPosition.right.x}, ${handPosition.right.y}) rotate(${handPosition.right.rotation})`}
                  className="arm-group"
                >
                  {/* Right arm */}
                  <line x1="125" y1="105" x2="170" y2="120" stroke="#FFB6C1" strokeWidth="10" strokeLinecap="round" />
                  
                  {/* Right hand */}
                  <circle cx="170" cy="120" r="15" fill="#FFB6C1" stroke="#D4A5A5" strokeWidth="2" className="hand-animated" />
                  
                  {/* Fingers - spread based on spread value */}
                  <g className="fingers" style={{ opacity: Math.max(0.3, handPosition.right.spread / 100) }}>
                    <circle
                      cx={180 + (handPosition.right.spread / 100) * 5}
                      cy={110 - (handPosition.right.spread / 100) * 8}
                      r="4"
                      fill="#D4A5A5"
                      className="finger"
                    />
                    <circle
                      cx={185 + (handPosition.right.spread / 100) * 8}
                      cy={125}
                      r="4"
                      fill="#D4A5A5"
                      className="finger"
                    />
                    <circle
                      cx={175 - (handPosition.right.spread / 100) * 3}
                      cy={135}
                      r="4"
                      fill="#D4A5A5"
                      className="finger"
                    />
                    <circle
                      cx={160 - (handPosition.right.spread / 100) * 5}
                      cy={135}
                      r="4"
                      fill="#D4A5A5"
                      className="finger"
                    />
                  </g>
                </g>
                
                {/* Animation indicator for recognized signs */}
                {currentWordIndex < avatarData.animation_data.animations.length && 
                 avatarData.animation_data.animations[currentWordIndex].recognized && (
                  <g className="animation-indicator">
                    <circle cx="100" cy="30" r="8" fill="none" stroke="#FFD700" strokeWidth="2" opacity="0.8" />
                    <circle cx="100" cy="30" r="12" fill="none" stroke="#FFD700" strokeWidth="1" opacity="0.4" />
                  </g>
                )}
                
                {/* Fingerspelling indicator */}
                {currentWordIndex < avatarData.animation_data.animations.length && 
                 !avatarData.animation_data.animations[currentWordIndex].recognized && (
                  <g className="fingerspell-indicator">
                    <text x="100" y="290" textAnchor="middle" fontSize="14" fontWeight="bold" fill="#FF9800">
                      Spelling: {avatarData.animation_data.animations[currentWordIndex].letters?.join('')}
                    </text>
                  </g>
                )}
              </svg>
            </div>

            {/* Current Word Display */}
            <div className="current-word">
              {currentWordIndex < avatarData.animation_data.animations.length && (
                <div>
                  <p className="word-label">Now signing:</p>
                  <p className="word-text">
                    {avatarData.animation_data.animations[currentWordIndex].word}
                  </p>
                  <p className="sign-type">
                    {avatarData.animation_data.animations[currentWordIndex].recognized 
                      ? '✓ Recognized Sign' 
                      : '✋ Fingerspelling'}
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* Controls */}
          <div className="avatar-controls">
            <button
              onClick={playAnimation}
              disabled={isPlaying}
              aria-label="Play sign language animation"
            >
              ▶ Play
            </button>
            <button
              onClick={pauseAnimation}
              disabled={!isPlaying}
              aria-label="Pause animation"
            >
              ⏸ Pause
            </button>
            <button
              onClick={resetAnimation}
              aria-label="Reset animation to beginning"
            >
              ↻ Reset
            </button>
          </div>

          {/* Progress */}
          <div className="avatar-progress">
            <div className="progress-bar">
              <div
                className="progress-fill"
                style={{
                  width: `${(currentWordIndex / avatarData.animation_data.animations.length) * 100}%`,
                }}
              />
            </div>
            <p className="progress-text">
              {currentWordIndex + 1} of {avatarData.animation_data.animations.length} words
            </p>
          </div>

          {/* Word List */}
          <div className="word-list">
            <h4>Word by word:</h4>
            <div className="words-container">
              {avatarData.animation_data.animations.map((animation, index) => (
                <button
                  key={index}
                  className={`word-chip ${index === currentWordIndex ? 'active' : ''} ${animation.recognized ? 'recognized' : 'fingerspelled'}`}
                  onClick={() => setCurrentWordIndex(index)}
                  title={animation.recognized ? 'Recognized sign' : 'Fingerspelled'}
                >
                  {animation.word}
                </button>
              ))}
            </div>
          </div>

          {/* Statistics */}
          <div className="avatar-stats">
            <p>
              <strong>Recognized signs:</strong> {avatarData.recognized_words} /{' '}
              {avatarData.word_count}
            </p>
            <p>
              <strong>Duration:</strong> {avatarData.total_duration_seconds.toFixed(1)} seconds
            </p>
          </div>
        </div>
      )}

      <style>{`
        .sign-language-avatar {
          background: #f5f5f5;
          border: 2px solid #ddd;
          border-radius: 8px;
          padding: 20px;
          margin: 20px 0;
        }

        .avatar-container {
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 20px;
        }

        .avatar-display {
          display: flex;
          gap: 30px;
          align-items: center;
          width: 100%;
          justify-content: center;
          flex-wrap: wrap;
        }

        .avatar-placeholder {
          background: white;
          border: 2px solid #ccc;
          border-radius: 12px;
          padding: 20px;
          width: 240px;
          height: 380px;
          display: flex;
          align-items: center;
          justify-content: center;
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
          position: relative;
          overflow: hidden;
        }

        .avatar-figure {
          width: 100%;
          height: 100%;
          filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
        }

        .hand-animated {
          transition: all 0.3s ease;
          animation: pulse 0.4s ease-in-out;
        }

        @keyframes pulse {
          0%, 100% { r: 15; }
          50% { r: 18; }
        }

        .finger {
          transition: all 0.4s ease;
        }

        .arm-group {
          transform-origin: 75px 105px;
          transition: transform 0.05s linear;
        }

        .animation-indicator {
          animation: glow 1s ease-in-out infinite;
        }

        @keyframes glow {
          0%, 100% {
            opacity: 0.4;
          }
          50% {
            opacity: 1;
          }
        }

        .current-word {
          text-align: center;
          min-height: 100px;
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 15px;
          background: white;
          border-radius: 8px;
          min-width: 200px;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        }

        .word-label {
          font-size: 12px;
          color: #999;
          margin: 0;
          text-transform: uppercase;
          letter-spacing: 1px;
        }

        .word-text {
          font-size: 32px;
          font-weight: bold;
          margin: 8px 0;
          color: #0066cc;
          animation: wordPulse 0.4s ease-in-out;
        }

        @keyframes wordPulse {
          0% { transform: scale(0.8); opacity: 0; }
          100% { transform: scale(1); opacity: 1; }
        }

        .sign-type {
          font-size: 13px;
          margin: 8px 0 0 0;
          font-weight: 600;
          color: #666;
        }

        .avatar-controls {
          display: flex;
          gap: 10px;
          justify-content: center;
          flex-wrap: wrap;
        }

        .avatar-controls button {
          padding: 12px 24px;
          background: #0066cc;
          color: white;
          border: none;
          border-radius: 6px;
          cursor: pointer;
          font-size: 14px;
          font-weight: 600;
          transition: all 0.2s;
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        .avatar-controls button:disabled {
          background: #ccc;
          cursor: not-allowed;
          box-shadow: none;
        }

        .avatar-controls button:hover:not(:disabled) {
          background: #0052a3;
          transform: translateY(-2px);
          box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }

        .avatar-progress {
          width: 100%;
          max-width: 400px;
        }

        .progress-bar {
          height: 10px;
          background: #e0e0e0;
          border-radius: 5px;
          overflow: hidden;
          box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
        }

        .progress-fill {
          height: 100%;
          background: linear-gradient(90deg, #4CAF50, #45a049);
          transition: width 0.3s ease;
          box-shadow: 0 0 10px rgba(76, 175, 80, 0.4);
        }

        .progress-text {
          font-size: 12px;
          color: #666;
          margin-top: 8px;
          text-align: center;
          font-weight: 600;
        }

        .word-list {
          width: 100%;
        }

        .word-list h4 {
          margin: 0 0 12px 0;
          font-size: 14px;
          color: #333;
          font-weight: 600;
        }

        .words-container {
          display: flex;
          flex-wrap: wrap;
          gap: 8px;
          justify-content: center;
        }

        .word-chip {
          padding: 8px 14px;
          background: white;
          border: 2px solid #ddd;
          border-radius: 24px;
          cursor: pointer;
          font-size: 13px;
          font-weight: 600;
          transition: all 0.2s;
          color: #333;
        }

        .word-chip.recognized {
          border-color: #4CAF50;
          background: #f1f8f4;
        }

        .word-chip.fingerspelled {
          border-color: #FF9800;
          background: #fff3e0;
        }

        .word-chip.active {
          background: #0066cc;
          color: white;
          border-color: #0066cc;
          box-shadow: 0 4px 12px rgba(0, 102, 204, 0.3);
          transform: scale(1.1);
        }

        .word-chip:hover {
          transform: translateY(-2px);
          box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }

        .avatar-stats {
          width: 100%;
          padding: 15px;
          background: white;
          border-radius: 8px;
          font-size: 13px;
          color: #666;
          border-left: 4px solid #0066cc;
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }

        .avatar-stats p {
          margin: 6px 0;
          font-weight: 500;
        }

        .error-message {
          color: #d32f2f;
          background: #ffebee;
          padding: 12px 15px;
          border-radius: 6px;
          margin-bottom: 10px;
          border-left: 4px solid #d32f2f;
          font-weight: 500;
        }

        .loading {
          text-align: center;
          padding: 30px 20px;
          color: #0066cc;
          font-weight: 600;
          animation: fadeInOut 1.5s ease-in-out infinite;
        }

        @keyframes fadeInOut {
          0%, 100% { opacity: 0.6; }
          50% { opacity: 1; }
        }

        @media (max-width: 768px) {
          .avatar-display {
            flex-direction: column;
            gap: 15px;
          }

          .word-text {
            font-size: 24px;
          }

          .avatar-placeholder {
            width: 200px;
            height: 320px;
          }
        }
      `}</style>
    </div>
  );
};

export default SignLanguageAvatar;
