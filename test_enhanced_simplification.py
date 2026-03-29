"""Test enhanced text simplification with best practices"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.text_adapter import simplify_text

print("=" * 80)
print("TEST 1: Complex Academic Text with Causal Relationships")
print("=" * 80)

academic_text = """
Climate change is causing significant impacts on global ecosystems. Because of 
rising temperatures, polar ice caps are melting at an unprecedented rate. This 
leads to higher sea levels, which threatens coastal communities. Furthermore, 
if current trends continue, we will see more extreme weather events such as 
hurricanes and droughts. The Intergovernmental Panel on Climate Change (IPCC) 
reports that approximately 1.1C of warming has already occurred since 
pre-industrial times.
"""

print("ORIGINAL:")
print(academic_text)
print(f"\nWord count: {len(academic_text.split())}")

print("\n" + "-" * 80)
print("SIMPLIFIED (Basic Level - preserve_meaning=True):")
print("-" * 80)
result_basic = simplify_text(academic_text, reading_level="basic", preserve_meaning=True)
print(result_basic)
print(f"\nWord count: {len(result_basic.split())}")

print("\n" + "=" * 80)
print("TEST 2: YouTube Comment (Casual Content)")
print("=" * 80)

youtube_comment = """I hope you enjoyed this video



hit likes.

And do subscribe to my channel



Thank you so much for watching

god bless you all.

lots of love
"""

print("ORIGINAL:")
print(youtube_comment)

print("\n" + "-" * 80)
print("SIMPLIFIED (Should preserve meaning, no hallucinations):")
print("-" * 80)
result_casual = simplify_text(youtube_comment, reading_level="basic", preserve_meaning=True)
print(result_casual)

# Check for hallucinations
hallucinations = ["if you did", "if not", "send it to me", "share with friends"]
found = [h for h in hallucinations if h.lower() in result_casual.lower()]
if found:
    print(f"\n[FAIL] HALLUCINATIONS FOUND: {found}")
else:
    print(f"\n[PASS] NO HALLUCINATIONS - Perfect!")

print("\n" + "=" * 80)
print("TEST 3: Technical Text with Conditions")
print("=" * 80)

technical_text = """
The CRISPR-Cas9 system enables targeted genomic modifications through RNA-guided 
endonuclease activity. If the guide RNA (gRNA) successfully binds to the target 
DNA sequence adjacent to PAM motifs, then Cas9 induces double-strand breaks. 
This triggers cellular repair mechanisms including NHEJ or HDR. Because NHEJ 
often results in insertions or deletions, gene function can be disrupted. 
However, when provided with a donor DNA template, HDR enables precise editing.
"""

print("ORIGINAL:")
print(technical_text)

print("\n" + "-" * 80)
print("SIMPLIFIED (Basic - preserve conditions):")
print("-" * 80)
result_tech = simplify_text(technical_text, reading_level="basic", preserve_meaning=True)
print(result_tech)

# Check if conditions preserved
if "if" in result_tech.lower() or "when" in result_tech.lower():
    print("\n[PASS] Conditional logic preserved!")
else:
    print("\n[WARN] Conditional logic may be missing")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print("All tests completed! Check output above for quality assessment.")
