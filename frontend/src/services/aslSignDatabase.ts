/**
 * ASL Sign Language Database - Comprehensive Gesture Library
 * Defines hand movements and positions for sign language
 * Based on real ASL sign specifications
 */

interface HandFrame {
  left: { x: number; y: number; rotation: number; spread: number };
  right: { x: number; y: number; rotation: number; spread: number };
  bodyRotation: number;
}

interface SignAnimation {
  word: string;
  frames: HandFrame[];
  description: string;
  duration?: number; // milliseconds, default 1000
}

// Hand positions represent relative movements from neutral position
// spread: 0-100 (0 = closed fist, 100 = spread fingers)
// rotation: 0-360 degrees

export const aslSignDatabase: Record<string, SignAnimation> = {
  // Greetings and Politeness
  hello: {
    word: 'hello',
    description: 'Wave hand from side of face outward',
    frames: [
      { left: { x: -40, y: -25, rotation: 0, spread: 60 }, right: { x: 0, y: 0, rotation: 0, spread: 0 }, bodyRotation: 0 },
      { left: { x: -50, y: -10, rotation: 30, spread: 70 }, right: { x: 0, y: 0, rotation: 0, spread: 0 }, bodyRotation: 0 },
      { left: { x: -45, y: 10, rotation: 60, spread: 80 }, right: { x: 0, y: 0, rotation: 0, spread: 0 }, bodyRotation: 0 },
      { left: { x: -35, y: 5, rotation: 30, spread: 70 }, right: { x: 0, y: 0, rotation: 0, spread: 0 }, bodyRotation: 0 },
    ],
    duration: 1200,
  },

  goodbye: {
    word: 'goodbye',
    description: 'Wave hand in goodbye motion',
    frames: [
      { left: { x: 0, y: -40, rotation: 0, spread: 50 }, right: { x: 0, y: 0, rotation: 0, spread: 0 }, bodyRotation: 0 },
      { left: { x: 15, y: -30, rotation: 20, spread: 60 }, right: { x: 0, y: 0, rotation: 0, spread: 0 }, bodyRotation: 0 },
      { left: { x: 25, y: -15, rotation: 40, spread: 70 }, right: { x: 0, y: 0, rotation: 0, spread: 0 }, bodyRotation: 0 },
      { left: { x: 15, y: -30, rotation: 20, spread: 60 }, right: { x: 0, y: 0, rotation: 0, spread: 0 }, bodyRotation: 0 },
      { left: { x: 5, y: -35, rotation: 10, spread: 55 }, right: { x: 0, y: 0, rotation: 0, spread: 0 }, bodyRotation: 0 },
    ],
    duration: 1500,
  },

  thank: {
    word: 'thank',
    description: 'Both hands move from chin outward (expressing gratitude)',
    frames: [
      { left: { x: -15, y: -50, rotation: 0, spread: 50 }, right: { x: 15, y: -50, rotation: 180, spread: 50 }, bodyRotation: 0 },
      { left: { x: -35, y: -40, rotation: 0, spread: 60 }, right: { x: 35, y: -40, rotation: 180, spread: 60 }, bodyRotation: 0 },
      { left: { x: -50, y: -20, rotation: 0, spread: 70 }, right: { x: 50, y: -20, rotation: 180, spread: 70 }, bodyRotation: 0 },
      { left: { x: -40, y: -30, rotation: 0, spread: 65 }, right: { x: 40, y: -30, rotation: 180, spread: 65 }, bodyRotation: 0 },
    ],
    duration: 1400,
  },

  please: {
    word: 'please',
    description: 'Hand on chest, circular motion (polite request)',
    frames: [
      { left: { x: -10, y: -5, rotation: 0, spread: 70 }, right: { x: 0, y: 0, rotation: 0, spread: 0 }, bodyRotation: 0 },
      { left: { x: -20, y: 15, rotation: 45, spread: 75 }, right: { x: 0, y: 0, rotation: 0, spread: 0 }, bodyRotation: 0 },
      { left: { x: -15, y: 25, rotation: 90, spread: 75 }, right: { x: 0, y: 0, rotation: 0, spread: 0 }, bodyRotation: 0 },
      { left: { x: 5, y: 20, rotation: 135, spread: 70 }, right: { x: 0, y: 0, rotation: 0, spread: 0 }, bodyRotation: 0 },
      { left: { x: -10, y: -5, rotation: 180, spread: 70 }, right: { x: 0, y: 0, rotation: 0, spread: 0 }, bodyRotation: 0 },
    ],
    duration: 1600,
  },

  // Action Verbs
  help: {
    word: 'help',
    description: 'Right hand helps left hand up (to help/assist)',
    frames: [
      { left: { x: -25, y: 25, rotation: 0, spread: 25 }, right: { x: 25, y: 20, rotation: 90, spread: 40 }, bodyRotation: 0 },
      { left: { x: -25, y: 5, rotation: 0, spread: 35 }, right: { x: 25, y: 10, rotation: 90, spread: 50 }, bodyRotation: 0 },
      { left: { x: -25, y: -20, rotation: 0, spread: 45 }, right: { x: 25, y: -10, rotation: 90, spread: 60 }, bodyRotation: 0 },
      { left: { x: -25, y: 0, rotation: 0, spread: 40 }, right: { x: 25, y: 0, rotation: 90, spread: 55 }, bodyRotation: 0 },
    ],
    duration: 1400,
  },

  submit: {
    word: 'submit',
    description: 'Push hands forward (to submit/hand in)',
    frames: [
      { left: { x: -20, y: 0, rotation: 0, spread: 50 }, right: { x: 20, y: 0, rotation: 180, spread: 50 }, bodyRotation: 0 },
      { left: { x: -10, y: 0, rotation: 0, spread: 55 }, right: { x: 10, y: 0, rotation: 180, spread: 55 }, bodyRotation: 0 },
      { left: { x: 10, y: 0, rotation: 0, spread: 60 }, right: { x: -10, y: 0, rotation: 180, spread: 60 }, bodyRotation: 0 },
    ],
    duration: 1200,
  },

  send: {
    word: 'send',
    description: 'Flick hand forward (send away)',
    frames: [
      { left: { x: -15, y: 0, rotation: 0, spread: 35 }, right: { x: 0, y: 0, rotation: 0, spread: 0 }, bodyRotation: 0 },
      { left: { x: 0, y: -5, rotation: 0, spread: 40 }, right: { x: 0, y: 0, rotation: 0, spread: 0 }, bodyRotation: 0 },
      { left: { x: 20, y: -10, rotation: 0, spread: 50 }, right: { x: 0, y: 0, rotation: 0, spread: 0 }, bodyRotation: 0 },
    ],
    duration: 1000,
  },

  // Yes/No/Questions
  yes: {
    word: 'yes',
    description: 'Fist nods up and down (affirmative)',
    frames: [
      { left: { x: 0, y: -35, rotation: 0, spread: 20 }, right: { x: 0, y: 0, rotation: 0, spread: 0 }, bodyRotation: 0 },
      { left: { x: 0, y: -15, rotation: 0, spread: 20 }, right: { x: 0, y: 0, rotation: 0, spread: 0 }, bodyRotation: 0 },
      { left: { x: 0, y: 10, rotation: 0, spread: 20 }, right: { x: 0, y: 0, rotation: 0, spread: 0 }, bodyRotation: 0 },
      { left: { x: 0, y: -35, rotation: 0, spread: 20 }, right: { x: 0, y: 0, rotation: 0, spread: 0 }, bodyRotation: 0 },
    ],
    duration: 1200,
  },

  no: {
    word: 'no',
    description: 'Index finger shakes side to side (negative)',
    frames: [
      { left: { x: 0, y: -35, rotation: 0, spread: 20 }, right: { x: 0, y: 0, rotation: 0, spread: 0 }, bodyRotation: 0 },
      { left: { x: -20, y: -35, rotation: 0, spread: 20 }, right: { x: 0, y: 0, rotation: 0, spread: 0 }, bodyRotation: -8 },
      { left: { x: 20, y: -35, rotation: 0, spread: 20 }, right: { x: 0, y: 0, rotation: 0, spread: 0 }, bodyRotation: 8 },
      { left: { x: -15, y: -35, rotation: 0, spread: 20 }, right: { x: 0, y: 0, rotation: 0, spread: 0 }, bodyRotation: -5 },
      { left: { x: 15, y: -35, rotation: 0, spread: 20 }, right: { x: 0, y: 0, rotation: 0, spread: 0 }, bodyRotation: 5 },
      { left: { x: 0, y: -35, rotation: 0, spread: 20 }, right: { x: 0, y: 0, rotation: 0, spread: 0 }, bodyRotation: 0 },
    ],
    duration: 1400,
  },

  // Questions
  what: {
    word: 'what',
    description: 'Open hands with questioning expression',
    frames: [
      { left: { x: -20, y: 10, rotation: 0, spread: 80 }, right: { x: 20, y: 10, rotation: 180, spread: 80 }, bodyRotation: 0 },
      { left: { x: -25, y: 0, rotation: 0, spread: 85 }, right: { x: 25, y: 0, rotation: 180, spread: 85 }, bodyRotation: 2 },
      { left: { x: -20, y: -10, rotation: 0, spread: 80 }, right: { x: 20, y: -10, rotation: 180, spread: 80 }, bodyRotation: 0 },
    ],
    duration: 1300,
  },

  how: {
    word: 'how',
    description: 'Hands rotate from fists to palms up (how?)',
    frames: [
      { left: { x: -15, y: 15, rotation: 0, spread: 20 }, right: { x: 15, y: 15, rotation: 180, spread: 20 }, bodyRotation: 0 },
      { left: { x: -15, y: 5, rotation: 45, spread: 50 }, right: { x: 15, y: 5, rotation: 225, spread: 50 }, bodyRotation: 0 },
      { left: { x: -15, y: -5, rotation: 90, spread: 80 }, right: { x: 15, y: -5, rotation: 270, spread: 80 }, bodyRotation: 0 },
    ],
    duration: 1400,
  },

  // Emotions and States
  love: {
    word: 'love',
    description: 'Both hands cross on chest (love)',
    frames: [
      { left: { x: -5, y: 5, rotation: 45, spread: 60 }, right: { x: 5, y: 5, rotation: 315, spread: 60 }, bodyRotation: 0 },
      { left: { x: -15, y: 0, rotation: 45, spread: 70 }, right: { x: 15, y: 0, rotation: 315, spread: 70 }, bodyRotation: -2 },
      { left: { x: -20, y: -8, rotation: 45, spread: 75 }, right: { x: 20, y: -8, rotation: 315, spread: 75 }, bodyRotation: 2 },
      { left: { x: -15, y: 0, rotation: 45, spread: 70 }, right: { x: 15, y: 0, rotation: 315, spread: 70 }, bodyRotation: 0 },
    ],
    duration: 1400,
  },

  sorry: {
    word: 'sorry',
    description: 'Hand circles on chest (apology)',
    frames: [
      { left: { x: -12, y: -5, rotation: 0, spread: 60 }, right: { x: 0, y: 0, rotation: 0, spread: 0 }, bodyRotation: 0 },
      { left: { x: -18, y: 12, rotation: 90, spread: 65 }, right: { x: 0, y: 0, rotation: 0, spread: 0 }, bodyRotation: 0 },
      { left: { x: -12, y: 20, rotation: 180, spread: 60 }, right: { x: 0, y: 0, rotation: 0, spread: 0 }, bodyRotation: 0 },
      { left: { x: 3, y: 12, rotation: 270, spread: 65 }, right: { x: 0, y: 0, rotation: 0, spread: 0 }, bodyRotation: 0 },
      { left: { x: -12, y: -5, rotation: 0, spread: 60 }, right: { x: 0, y: 0, rotation: 0, spread: 0 }, bodyRotation: 0 },
    ],
    duration: 1600,
  },

  // Time and Objects
  form: {
    word: 'form',
    description: 'Rectangle shape with hands (form/document)',
    frames: [
      { left: { x: -20, y: -15, rotation: 0, spread: 30 }, right: { x: 20, y: -15, rotation: 0, spread: 30 }, bodyRotation: 0 },
      { left: { x: -20, y: 5, rotation: 0, spread: 30 }, right: { x: 20, y: 5, rotation: 0, spread: 30 }, bodyRotation: 0 },
      { left: { x: -20, y: 20, rotation: 0, spread: 30 }, right: { x: 20, y: 20, rotation: 0, spread: 30 }, bodyRotation: 0 },
    ],
    duration: 1300,
  },

  tomorrow: {
    word: 'tomorrow',
    description: 'Thumb touches cheek, hand moves forward (tomorrow)',
    frames: [
      { left: { x: -35, y: -35, rotation: 45, spread: 15 }, right: { x: 0, y: 0, rotation: 0, spread: 0 }, bodyRotation: 0 },
      { left: { x: -20, y: -20, rotation: 45, spread: 15 }, right: { x: 0, y: 0, rotation: 0, spread: 0 }, bodyRotation: 0 },
      { left: { x: 10, y: -5, rotation: 45, spread: 15 }, right: { x: 0, y: 0, rotation: 0, spread: 0 }, bodyRotation: 0 },
    ],
    duration: 1300,
  },

  today: {
    word: 'today',
    description: 'Both hands move down (today/present)',
    frames: [
      { left: { x: -15, y: -25, rotation: 0, spread: 60 }, right: { x: 15, y: -25, rotation: 180, spread: 60 }, bodyRotation: 0 },
      { left: { x: -15, y: 0, rotation: 0, spread: 60 }, right: { x: 15, y: 0, rotation: 180, spread: 60 }, bodyRotation: 0 },
      { left: { x: -15, y: 15, rotation: 0, spread: 60 }, right: { x: 15, y: 15, rotation: 180, spread: 60 }, bodyRotation: 0 },
    ],
    duration: 1200,
  },

  understand: {
    word: 'understand',
    description: 'Snap index finger up from temple (understand)',
    frames: [
      { left: { x: -40, y: -35, rotation: 0, spread: 20 }, right: { x: 0, y: 0, rotation: 0, spread: 0 }, bodyRotation: 0 },
      { left: { x: -25, y: -28, rotation: 0, spread: 30 }, right: { x: 0, y: 0, rotation: 0, spread: 0 }, bodyRotation: 0 },
      { left: { x: -15, y: -20, rotation: 0, spread: 50 }, right: { x: 0, y: 0, rotation: 0, spread: 0 }, bodyRotation: 0 },
    ],
    duration: 1200,
  },

  before: {
    word: 'before',
    description: 'Hand moves back over shoulder (before)',
    frames: [
      { left: { x: 30, y: -25, rotation: 0, spread: 50 }, right: { x: 0, y: 0, rotation: 0, spread: 0 }, bodyRotation: 0 },
      { left: { x: 10, y: -15, rotation: 0, spread: 50 }, right: { x: 0, y: 0, rotation: 0, spread: 0 }, bodyRotation: 0 },
      { left: { x: -10, y: -5, rotation: 0, spread: 50 }, right: { x: 0, y: 0, rotation: 0, spread: 0 }, bodyRotation: 0 },
    ],
    duration: 1300,
  },

  need: {
    word: 'need',
    description: 'Both hands bend down (need)',
    frames: [
      { left: { x: -20, y: -20, rotation: 0, spread: 30 }, right: { x: 20, y: -20, rotation: 180, spread: 30 }, bodyRotation: 0 },
      { left: { x: -20, y: 0, rotation: 0, spread: 30 }, right: { x: 20, y: 0, rotation: 180, spread: 30 }, bodyRotation: 0 },
      { left: { x: -20, y: 15, rotation: 0, spread: 25 }, right: { x: 20, y: 15, rotation: 180, spread: 25 }, bodyRotation: 0 },
    ],
    duration: 1200,
  },

  want: {
    word: 'want',
    description: 'Both hands palm up, fingers bend (want)',
    frames: [
      { left: { x: -20, y: 10, rotation: 0, spread: 80 }, right: { x: 20, y: 10, rotation: 180, spread: 80 }, bodyRotation: 0 },
      { left: { x: -20, y: 0, rotation: 0, spread: 75 }, right: { x: 20, y: 0, rotation: 180, spread: 75 }, bodyRotation: 0 },
      { left: { x: -20, y: -10, rotation: 0, spread: 70 }, right: { x: 20, y: -10, rotation: 180, spread: 70 }, bodyRotation: 0 },
      { left: { x: -20, y: 5, rotation: 0, spread: 75 }, right: { x: 20, y: 5, rotation: 180, spread: 75 }, bodyRotation: 0 },
    ],
    duration: 1300,
  },
};

/**
 * Get ASL animation for a word, or generate a fingerspelling animation if not found
 */
export function getSignAnimation(word: string): SignAnimation {
  const normalizedWord = word.toLowerCase().trim();

  // Return database entry if exists
  if (aslSignDatabase[normalizedWord]) {
    return aslSignDatabase[normalizedWord];
  }

  // Generate fingerspelling animation for unknown words
  return generateFingerspellingAnimation(normalizedWord);
}

/**
 * Generate a fingerspelling animation (letter by letter)
 */
function generateFingerspellingAnimation(word: string): SignAnimation {
  const letters = word.toUpperCase().split('');
  const frameCount = Math.max(4, letters.length);
  const frames: HandFrame[] = [];

  // Create frames for each letter position
  // Fingerspelling uses circular hand motions
  for (let i = 0; i < frameCount; i++) {
    const progress = i / Math.max(frameCount - 1, 1);
    const theta = progress * Math.PI * 2;
    
    frames.push({
      left: {
        x: Math.sin(theta) * 20,
        y: -30 + Math.cos(theta) * 12,
        rotation: (progress * 360) % 360,
        spread: 35 + (25 * (Math.sin(theta * 2) + 1) / 2),
      },
      right: { x: 0, y: 0, rotation: 0, spread: 0 },
      bodyRotation: Math.sin(theta) * 3,
    });
  }

  const duration = 200 * Math.max(1, letters.length / 2);

  return {
    word,
    description: `Fingerspell: ${letters.join('-')}`,
    frames,
    duration,
  };
}
