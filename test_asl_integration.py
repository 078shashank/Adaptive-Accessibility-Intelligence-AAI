#!/usr/bin/env python
"""
Test script to verify ASL grammar converter integration with avatar service
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.sign_language_converter import SignLanguageConverter
from app.services.avatar import SignLanguageAvatarService

# Test cases
test_cases = [
    "Please submit the form before tomorrow",
    "Hello how are you today",
    "What is your name",
    "I need help with this task",
    "Thank you for your assistance",
]

print("=" * 70)
print("ASL GRAMMAR CONVERSION & AVATAR INTEGRATION TEST")
print("=" * 70)

for test_text in test_cases:
    print(f"\n{'─' * 70}")
    print(f"INPUT (English): {test_text}")
    print(f"{'─' * 70}")
    
    # Get ASL conversion
    asl_words = SignLanguageConverter.convert_to_asl(test_text)
    print(f"OUTPUT (ASL): {' '.join(asl_words)}")
    
    # Get avatar animation data
    avatar_data = SignLanguageAvatarService.text_to_sign_animation(test_text)
    
    print(f"\nAnimation Sequence:")
    for i, anim in enumerate(avatar_data['animations'], 1):
        status = "✓ RECOGNIZED" if anim['recognized'] else "✗ FINGERSPELLED"
        duration = anim.get('duration', 0)
        print(f"  {i}. {anim['word']:15} -> {status:18} ({duration}ms)")
    
    print(f"\nMetadata:")
    print(f"  Total words: {len(asl_words)}")
    print(f"  Total duration: {avatar_data['total_duration_ms']}ms")
    print(f"  Recognized: {sum(1 for a in avatar_data['animations'] if a['recognized'])}/{len(asl_words)}")
    print(f"  Is Question: {avatar_data['grammar_metadata']['is_question']}")
    print(f"  Has Actions: {avatar_data['grammar_metadata']['has_actions']}")
    print(f"  Has Time References: {avatar_data['grammar_metadata']['has_time']}")

print(f"\n{'=' * 70}")
print("✅ ALL TESTS COMPLETED SUCCESSFULLY")
print("=" * 70)
