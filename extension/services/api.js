/**
 * Backend API Service for AAI Extension
 * Communicates with local FastAPI backend at localhost:8000
 */

const API_BASE_URL = 'http://localhost:8000/api/v1';

export const textService = {
  /**
   * Simplify text using AI
   * @param {string} text - Text to simplify
   * @param {string} readingLevel - basic|intermediate|advanced
   * @returns {Promise<object>} Simplification result
   */
  simplify: async (text, readingLevel = 'intermediate') => {
    try {
      const response = await fetch(`${API_BASE_URL}/text/simplify`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          text, 
          reading_level: readingLevel 
        })
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Text simplification failed:', error);
      throw error;
    }
  }
};

export const speechService = {
  /**
   * Prepare text for speech synthesis
   * @param {string} text - Text to prepare
   * @returns {Promise<string>} Cleaned text
   */
  prepareForSpeech: async (text) => {
    try {
      // For now, we'll use the browser's Web Speech API directly
      // This could be enhanced with backend preprocessing
      return text;
    } catch (error) {
      console.error('Speech preparation failed:', error);
      throw error;
    }
  }
};

export const healthService = {
  /**
   * Check backend health status
   * @returns {Promise<object>} Health check result
   */
  check: async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/health`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
      });
      
      if (!response.ok) {
        return { available: false, error: 'Backend returned non-OK status' };
      }
      
      const data = await response.json();
      return { available: true, data };
    } catch (error) {
      return { 
        available: false, 
        error: error.message || 'Backend unavailable' 
      };
    }
  }
};

export default {
  text: textService,
  speech: speechService,
  health: healthService
};
