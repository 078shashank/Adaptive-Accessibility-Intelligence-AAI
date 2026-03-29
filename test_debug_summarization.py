"""Test script to debug text summarization issues"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.text_adapter import simplify_text

# Test with complex text
complex_text = """
The phenomenon of anthropogenic climate change represents one of the most 
pressing challenges confronting contemporary society, necessitating immediate 
and comprehensive action across multiple dimensions of human civilization. The 
scientific consensus, as articulated by the Intergovernmental Panel on Climate 
Change (IPCC), indicates that global temperatures have risen approximately 1.1 
degrees Celsius above pre-industrial levels, primarily attributable to the 
emission of greenhouse gases including carbon dioxide, methane, and nitrous 
oxide. These emissions originate from multitudinous sources, encompassing fossil 
fuel combustion for electricity generation and transportation, industrial 
processes, agricultural activities, and deforestation.
"""

print("=" * 80)
print("ORIGINAL TEXT:")
print("=" * 80)
print(complex_text)
print(f"\nOriginal length: {len(complex_text)} characters, {len(complex_text.split())} words")

print("\n" + "=" * 80)
print("BASIC LEVEL (35% retention):")
print("=" * 80)
result_basic = simplify_text(complex_text, reading_level="basic")
print(result_basic)
print(f"\nSimplified length: {len(result_basic)} characters")
print(f"Reduction: {(1 - len(result_basic)/len(complex_text)) * 100:.1f}%")

print("\n" + "=" * 80)
print("INTERMEDIATE LEVEL (50% retention):")
print("=" * 80)
result_intermediate = simplify_text(complex_text, reading_level="intermediate")
print(result_intermediate)
print(f"\nSimplified length: {len(result_intermediate)} characters")
print(f"Reduction: {(1 - len(result_intermediate)/len(complex_text)) * 100:.1f}%")

print("\n" + "=" * 80)
print("ADVANCED LEVEL (75% retention):")
print("=" * 80)
result_advanced = simplify_text(complex_text, reading_level="advanced")
print(result_advanced)
print(f"\nSimplified length: {len(result_advanced)} characters")
print(f"Reduction: {(1 - len(result_advanced)/len(complex_text)) * 100:.1f}%")

# Test with very short text
print("\n" + "=" * 80)
print("TEST WITH SHORT TEXT (< 20 words):")
print("=" * 80)
short_text = "The quick brown fox jumps over the lazy dog."
print(f"Input: {short_text}")
result_short = simplify_text(short_text, reading_level="basic")
print(f"Output: {result_short}")
print(f"Note: Text under 20 words is returned unchanged")
