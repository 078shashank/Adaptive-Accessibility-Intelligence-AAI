# Text Simplification - Real Examples

## Quick Reference: Input → Output Examples

### Example 1: Academic Text

**Original:**
> "The phenomenon of anthropogenic climate change represents one of the most pressing challenges confronting contemporary society, necessitating immediate and comprehensive action across multiple dimensions of human civilization."

**Simplified (Basic - 35%):**
> "Human-caused climate change is a major problem for society today. The UN says we need to act quickly in many areas."

**Simplified (Intermediate - 50%):**
> "Climate change caused by humans is one of the biggest challenges facing modern society. It requires immediate action across many areas of human activity, according to the UN."

**Simplified (Advanced - 75%):**
> "Anthropogenic climate change is a pressing challenge for contemporary society, requiring immediate and comprehensive action across multiple dimensions of human civilization, the UN says."

---

### Example 2: Technical Documentation

**Original:**
> "The CRISPR-Cas9 system facilitates targeted genomic modifications through RNA-guided endonuclease activity. The Cas9 enzyme, complexed with guide RNA (gRNA), recognizes and binds to specific DNA sequences adjacent to protospacer adjacent motifs (PAM)."

**Simplified (Basic):**
> "CRISPR-Cas9 is a gene-editing tool that uses RNA to cut DNA at specific locations. The Cas9 protein works with guide RNA to find and bind to target DNA sequences."

**Simplified (Intermediate):**
> "The CRISPR-Cas9 system enables precise genetic changes using RNA-guided enzymes. Cas9 binds to specific DNA sequences near PAM sites when combined with guide RNA."

---

### Example 3: Legal Language

**Original:**
> "WHEREAS, the Party of the First Part (hereinafter referred to as 'Licensor') is the rightful proprietor of certain intellectual property rights pertaining to the patented invention described in United States Patent Number 10,123,456; and WHEREAS, the Party of the Second Part desires to obtain a non-exclusive license..."

**Simplified (Basic):**
> "The Licensor owns patent number 10,123,456. The Licensee wants to get permission to use this patented invention under a non-exclusive license agreement."

---

### Example 4: Scientific Abstract

**Original:**
> "Quantum entanglement suggests instantaneous connections defy relativity. Dark matter comprises 85% of universe mass yet remains undetected. String theory proposes existence of 10 or more spatial dimensions beyond our perceivable three-dimensional reality."

**Simplified (Basic):**
> "Quantum physics shows particles can connect instantly across distances. Scientists believe most of the universe is made of invisible dark matter. String theory suggests there may be 10+ dimensions we cannot see."

**Simplified (Advanced):**
> "Quantum entanglement creates instant connections that seem to violate relativity. Dark matter makes up 85% of the universe's mass but has not been directly detected. String theory hypothesizes 10+ dimensions beyond our observable 3D space."

---

## Reading Level Guidelines

### Basic (35% retention)
- **Target audience:** Elementary school reading level
- **Use cases:** 
  - Cognitive disabilities
  - ESL learners
  - Children
  - Quick summaries
- **Characteristics:**
  - Short sentences (10-15 words)
  - Simple vocabulary
  - Removes technical jargon
  - Keeps only essential information

### Intermediate (50% retention)
- **Target audience:** Average adult reader
- **Use cases:**
  - General public
  - News articles
  - Blog posts
  - Educational materials
- **Characteristics:**
  - Moderate sentence length
  - Some technical terms explained
  - Balances detail and clarity

### Advanced (75% retention)
- **Target audience:** Educated readers
- **Use cases:**
  - Academic papers (simplified)
  - Professional documents
  - Technical reports
  - Research summaries
- **Characteristics:**
  - Retains most details
  - Maintains technical accuracy
  - Slightly shorter sentences
  - Removes redundancy only

---

## API Usage Examples

### Python Client
```python
from app.services.text_adapter import simplify_text

# Basic simplification
simple = simplify_text(complex_text, reading_level="basic")

# Intermediate (default)
moderate = simplify_text(complex_text)

# Advanced (minimal changes)
detailed = simplify_text(complex_text, reading_level="advanced")
```

### REST API
```bash
curl -X POST "http://localhost:8000/api/v1/text/simplify" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your complex text here...",
    "reading_level": "intermediate"
  }'
```

### Response Format
```json
{
  "original_text": "The phenomenon of anthropogenic climate change...",
  "simplified_text": "Human-caused climate change is a major problem...",
  "reading_level": "basic",
  "reduction_percentage": 65.2,
  "original_length": 234,
  "simplified_length": 81
}
```

---

## Performance Benchmarks

| Text Length | Processing Time | Model Used |
|-------------|----------------|------------|
| < 20 words | < 0.1s (returned as-is) | None |
| 20-50 words | 1-3 seconds | BART-large-cnn |
| 50-200 words | 3-8 seconds | BART-large-cnn |
| 200-500 words | 8-20 seconds | BART-large-cnn |
| 500+ words | 20-40 seconds | BART-large-cnn |

**Note:** Times vary based on hardware and whether model is cached.

---

## Best Practices

### ✅ DO:
- Use for texts longer than 20 words
- Choose reading level based on target audience
- Cache results for repeated requests
- Provide fallback for offline scenarios
- Test with domain-specific content

### ❌ DON'T:
- Expect perfect simplification for very short texts
- Use for creative writing or poetry
- Rely on it for legal/medical advice simplification
- Process texts under 20 words (wastes resources)
- Assume 100% accuracy on technical content

---

## Limitations

### Current Limitations:
1. **Very short texts:** Returned unchanged (< 20 words)
2. **Non-English text:** May produce unexpected results
3. **Code snippets:** Preserved but not simplified
4. **Mathematical formulas:** Kept as-is (correct behavior)
5. **Multiple topics:** May lose coherence across topic shifts
6. **Sarcasm/irony:** Not preserved in simplification

### Known Issues:
- BART sometimes adds phrases like "the study says" or "researchers found"
- May lose subtle nuances in philosophical arguments
- Technical accuracy not guaranteed for specialized fields
- Proper nouns sometimes omitted in aggressive summarization

---

## Troubleshooting

### Issue: Output identical to input
**Cause:** Text too short (< 20 words)  
**Solution:** Provide longer input or accept default behavior

### Issue: Nonsensical output
**Cause:** Model hallucination or input too complex  
**Solution:** Try higher reading level or manual fallback

### Issue: Slow processing
**Cause:** Long text or model loading overhead  
**Solution:** Implement caching, use async processing

### Issue: Loss of key information
**Cause:** Too aggressive summarization (basic level)  
**Solution:** Use intermediate or advanced level

---

## Comparison with Alternatives

| Method | Accuracy | Speed | Complexity | Cost |
|--------|----------|-------|------------|------|
| **BART (current)** | High | Medium | High | Free |
| GPT-4 | Very High | Fast | Very High | Paid |
| Rule-based | Low | Very Fast | Low | Free |
| T5-Small | Medium | Fast | Medium | Free |
| Manual editing | Very High | Very Slow | N/A | Expensive |

**Recommendation:** BART provides best balance of quality, speed, and cost for accessibility purposes.

---

## Future Improvements

### Planned Features:
1. **Custom model training:** Fine-tune on Newsela corpus
2. **Vocabulary substitution:** Replace complex words with simpler synonyms
3. **Sentence splitting:** Automatically break long sentences
4. **Readability metrics:** Show Flesch-Kincaid scores
5. **User preferences:** Learn from user corrections
6. **Domain adaptation:** Medical, legal, technical presets

### Research Directions:
- Multi-document simplification
- Context-aware terminology preservation
- Personalized difficulty adjustment
- Real-time simplification (streaming)
- Multilingual simplification support

---

## Citations

**Model:** BART (Bidirectional Encoder Representations from Transformers)  
**Paper:** "BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension"  
**Authors:** Lewis et al. (2019)  
**Dataset:** CNN/Daily Mail news articles  

**Alternative Datasets:**
- Newsela (news articles at multiple reading levels)
- Wikipedia Simple English
- OneStopEnglish (simplified news corpus)

---

## Contact & Support

For questions about text simplification:
- **Documentation:** `/docs/TEXT_SIMPLIFICATION_TEST_CASES.md`
- **API Spec:** `/docs/API_SPEC.md`
- **Source Code:** `backend/app/services/text_adapter.py`
- **Tests:** `backend/test_text_simplification_complex.py`
