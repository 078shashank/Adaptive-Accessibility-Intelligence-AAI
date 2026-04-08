"""Test hallucination prevention"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.text_adapter import simplify_text

# Test case 1: YouTube comment (your example)
youtube_comment = """I hope you enjoyed this video



hit likes.

And do subscribe to my channel



Thank you so much for watching

god bless you all.

lots of ❤️
"""

print("=" * 80)
print("TEST 1: YouTube Comment (Your Example)")
print("=" * 80)
print("ORIGINAL:")
print(youtube_comment)
print("\nSIMPLIFIED:")
result1 = simplify_text(youtube_comment, reading_level="basic")
print(result1)
print(f"\nLength: {len(result1)} characters")

# Check if hallucinated content is present
hallucinations = [
    "if you did",
    "if not",
    "send it to me",
    "share it with your friends"
]

found_hallucinations = [h for h in hallucinations if h.lower() in result1.lower()]
if found_hallucinations:
    print(f"\n❌ HALLUCINATIONS FOUND: {found_hallucinations}")
else:
    print(f"\n✅ NO HALLUCINATIONS - Content preserved correctly!")

# Test case 2: Complex academic text (should still use BART)
academic_text = """
The phenomenon of anthropogenic climate change represents one of the most 
pressing challenges confronting contemporary society, necessitating immediate 
and comprehensive action across multiple dimensions of human civilization.
"""

print("\n" + "=" * 80)
print("TEST 2: Complex Academic Text (Should Use BART)")
print("=" * 80)
print("ORIGINAL:")
print(academic_text)
print("\nSIMPLIFIED (Basic):")
result2 = simplify_text(academic_text, reading_level="basic")
print(result2)

# Test case 3: Casual message
casual_message = "Hey! Just wanted to say thanks for all your help. You're amazing! 😊"

print("\n" + "=" * 80)
print("TEST 3: Casual Message with Emoji")
print("=" * 80)
print("ORIGINAL:")
print(casual_message)
print("\nSIMPLIFIED:")
result3 = simplify_text(casual_message, reading_level="basic")
print(result3)
