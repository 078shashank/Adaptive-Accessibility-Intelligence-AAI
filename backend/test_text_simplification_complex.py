"""Complex Test Cases for Text Simplification Service"""
import pytest
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.services.text_adapter import simplify_text, manual_simplify_text


class TestTextSimplificationComplexCases:
    """Comprehensive test suite for text simplification with complex inputs"""

    # ============================================================================
    # EDGE CASES - Very Long Texts
    # ============================================================================
    
    def test_very_long_paragraph(self):
        """Test: Extremely long paragraph (500+ words)"""
        long_text = """
        The phenomenon of anthropogenic climate change represents one of the most 
        pressing challenges confronting contemporary society, necessitating immediate 
        and comprehensive action across multiple dimensions of human civilization. The 
        scientific consensus, as articulated by the Intergovernmental Panel on Climate 
        Change (IPCC), indicates that global temperatures have risen approximately 1.1 
        degrees Celsius above pre-industrial levels, primarily attributable to the 
        emission of greenhouse gases including carbon dioxide, methane, and nitrous 
        oxide. These emissions originate from multitudinous sources, encompassing fossil 
        fuel combustion for electricity generation and transportation, industrial 
        processes, agricultural activities, and deforestation. The ramifications of 
        these climatic alterations manifest through increasingly frequent and severe 
        meteorological events, including hurricanes, droughts, floods, and wildfires, 
        which disproportionately impact vulnerable populations in developing nations. 
        Furthermore, the cascading effects extend beyond environmental degradation to 
        encompass economic disruption, food insecurity, water scarcity, mass migration, 
        and potential geopolitical instability. Addressing this existential threat 
        requires unprecedented international cooperation, technological innovation, 
        policy reform, behavioral modification, and substantial financial investment 
        in renewable energy infrastructure, carbon capture technologies, and adaptive 
        measures designed to enhance resilience among communities worldwide.
        """
        
        result_basic = simplify_text(long_text, reading_level="basic")
        result_intermediate = simplify_text(long_text, reading_level="intermediate")
        result_advanced = simplify_text(long_text, reading_level="advanced")
        
        assert isinstance(result_basic, str)
        assert isinstance(result_intermediate, str)
        assert isinstance(result_advanced, str)
        assert len(result_basic) < len(long_text)
        assert len(result_intermediate) < len(long_text)

    def test_multiple_consecutive_paragraphs(self):
        """Test: Multiple paragraphs without breaks"""
        multi_para = """
        Quantum mechanics constitutes a fundamental theory in physics that provides 
        mathematical descriptions of the dual particle-like and wave-like behavior and 
        interactions of energy and matter at atomic and subatomic scales. The historical 
        development of quantum theory began with Max Planck's solution to the ultraviolet 
        catastrophe in 1900, followed by Albert Einstein's explanation of the photoelectric 
        effect, which demonstrated that light consists of discrete packets of energy called 
        photons. Werner Heisenberg's matrix mechanics and Erwin Schrödinger's wave mechanics 
        provided complementary mathematical frameworks for understanding quantum phenomena. 
        The Copenhagen interpretation, primarily developed by Niels Bohr and Werner 
        Heisenberg, posits that physical systems do not possess definite properties prior 
        to measurement, but rather exist in superpositions of all possible states.
        
        General relativity, developed by Albert Einstein between 1907 and 1915, represents 
        the geometric theory of gravitation that superseded Newton's law of universal 
        gravitation. The theory describes gravity not as a force but as a curvature of 
        spacetime caused by the presence of mass and energy. Massive objects like stars 
        and planets warp the fabric of spacetime around them, causing other objects to 
        follow curved trajectories. This revolutionary conception has been confirmed through 
        numerous experimental tests, including the bending of starlight during solar 
        eclipses, gravitational lensing of distant galaxies, time dilation measured by 
        atomic clocks, and the recent detection of gravitational waves by LIGO.
        """
        
        result = simplify_text(multi_para, reading_level="intermediate")
        assert len(result) > 0
        assert isinstance(result, str)

    # ============================================================================
    # EDGE CASES - Technical/Jargon-Heavy Text
    # ============================================================================
    
    def test_highly_technical_scientific_text(self):
        """Test: Dense scientific text with specialized terminology"""
        technical_text = """
        The CRISPR-Cas9 system facilitates targeted genomic modifications through 
        RNA-guided endonuclease activity. The Cas9 enzyme, complexed with guide RNA 
        (gRNA), recognizes and binds to specific DNA sequences adjacent to protospacer 
        adjacent motifs (PAM). Upon binding, Cas9 induces double-strand breaks (DSBs), 
        triggering cellular repair mechanisms including non-homologous end joining 
        (NHEJ) or homology-directed repair (HDR). NHEJ frequently results in insertions 
        or deletions (indels) that disrupt gene function, while HDR enables precise 
        gene editing when provided with a donor DNA template. Off-target effects remain 
        a significant concern, necessitating careful gRNA design and validation through 
        methods such as GUIDE-seq or CIRCLE-seq.
        """
        
        result_basic = simplify_text(technical_text, reading_level="basic")
        result_advanced = simplify_text(technical_text, reading_level="advanced")
        
        assert len(result_basic) > 0
        assert len(result_advanced) > 0
        # Advanced should retain more technical content
        assert len(result_advanced) >= len(result_basic)

    def test_legal_contract_language(self):
        """Test: Complex legal document with archaic terminology"""
        legal_text = """
        WHEREAS, the Party of the First Part (hereinafter referred to as "Licensor") 
        is the rightful proprietor of certain intellectual property rights pertaining 
        to the patented invention described in United States Patent Number 10,123,456; 
        and WHEREAS, the Party of the Second Part (hereinafter referred to as "Licensee") 
        desires to obtain a non-exclusive, non-transferable license to utilize said 
        intellectual property under the terms and conditions set forth herein; NOW, 
        THEREFORE, in consideration of the mutual covenants, representations, warranties, 
        and agreements contained herein, and for other good and valuable consideration, 
        the receipt and sufficiency of which are hereby acknowledged, the parties agree 
        as follows: Section 1. Grant of License. Subject to the terms and conditions of 
        this Agreement, Licensor hereby grants to Licensee a limited, non-exclusive, 
        non-transferable, revocable license to use the Licensed Property solely within 
        the Territory for the Term specified herein.
        """
        
        result = simplify_text(legal_text, reading_level="basic")
        assert len(result) > 0
        assert isinstance(result, str)

    # ============================================================================
    # EDGE CASES - Mixed Languages and Special Characters
    # ============================================================================
    
    def test_multilingual_text(self):
        """Test: Text containing multiple languages"""
        multilingual = """
        Welcome to our international conference! Bonjour à tous nos participants français.
        We are delighted to have colleagues from Deutschland qui apportent leur expertise.
        この会議は、国際協力にとって重要です。 Esperamos que disfruten de la presentación.
        La collaborazione internazionale è fondamentale per il progresso scientifico.
        """
        
        result = simplify_text(multilingual, reading_level="intermediate")
        # Should handle gracefully even if it can't summarize well
        assert isinstance(result, str)
        assert len(result) > 0

    def test_special_characters_and_symbols(self):
        """Test: Text with special characters, emojis, and symbols"""
        special_text = """
        The temperature reached 45°C (113°F) yesterday! That's ☀️🔥 hot! 
        The study showed a 200% increase (p < 0.001) in efficiency. 
        E = mc² remains one of the most famous equations. The price is $99.99 (£75.50).
        She said "Hello!" in 5 different languages: 你好，مرحبا, שלום, नमस्ते, สวัสดีครับ.
        The chemical formula is H₂O, and the reaction produces CO₂ + H₂O → energy.
        """
        
        result = simplify_text(special_text, reading_level="basic")
        assert isinstance(result, str)

    # ============================================================================
    # EDGE CASES - Structured Data and Lists
    # ============================================================================
    
    def test_numbered_lists_and_bullets(self):
        """Test: Text with numbered and bulleted lists"""
        list_text = """
        The key steps in machine learning are:
        1. Data Collection: Gathering relevant datasets from various sources
        2. Data Preprocessing: Cleaning and transforming raw data into usable format
        3. Feature Engineering: Selecting and creating meaningful input variables
        4. Model Selection: Choosing appropriate algorithms (linear regression, neural networks, etc.)
        5. Training: Feeding data to the model to learn patterns
        6. Validation: Testing model performance on unseen data
        7. Hyperparameter Tuning: Optimizing model configuration
        8. Deployment: Implementing the model in production environment
        9. Monitoring: Continuously tracking model performance and drift
        """
        
        result = simplify_text(list_text, reading_level="intermediate")
        assert len(result) > 0
        assert isinstance(result, str)

    def test_tables_and_structured_data(self):
        """Test: Text resembling table data"""
        table_text = """
        Product Name | Price | Quantity | Total
        Laptop Pro X1 | $1,299.99 | 5 | $6,499.95
        Wireless Mouse | $29.99 | 20 | $599.80
        USB-C Hub | $49.99 | 15 | $749.85
        Monitor 27" | $399.99 | 8 | $3,199.92
        Keyboard Mechanical | $89.99 | 12 | $1,079.88
        Subtotal: $12,129.40
        Tax (8%): $970.35
        Total: $13,099.75
        """
        
        result = simplify_text(table_text, reading_level="basic")
        assert isinstance(result, str)

    # ============================================================================
    # EDGE CASES - Code and Technical Content
    # ============================================================================
    
    def test_code_snippets_mixed_with_text(self):
        """Test: Programming code mixed with explanatory text"""
        code_text = """
        To implement a binary search tree in Python, we define a Node class:
        
        class Node:
            def __init__(self, key):
                self.left = None
                self.right = None
                self.val = key
        
        def insert(root, key):
            if root is None:
                return Node(key)
            else:
                if root.val < key:
                    root.right = insert(root.right, key)
                else:
                    root.left = insert(root.left, key)
            return root
        
        This recursive approach ensures proper tree structure maintenance.
        Time complexity: O(log n) for balanced trees, O(n) for skewed trees.
        """
        
        result = simplify_text(code_text, reading_level="intermediate")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_mathematical_formulas_inline(self):
        """Test: Text with inline mathematical expressions"""
        math_text = """
        The quadratic formula states that for any equation of the form 
        ax² + bx + c = 0, the solutions are given by:
        x = (-b ± √(b² - 4ac)) / (2a)
        
        The discriminant Δ = b² - 4ac determines the nature of roots:
        - If Δ > 0: Two distinct real roots
        - If Δ = 0: One repeated real root
        - If Δ < 0: Two complex conjugate roots
        
        For example, solving 2x² + 5x - 3 = 0:
        a=2, b=5, c=-3
        Δ = 5² - 4(2)(-3) = 25 + 24 = 49
        x = (-5 ± √49) / 4 = (-5 ± 7) / 4
        Therefore: x₁ = 0.5, x₂ = -3
        """
        
        result = simplify_text(math_text, reading_level="basic")
        assert isinstance(result, str)

    # ============================================================================
    # EDGE CASES - Ambiguous and Contradictory Content
    # ============================================================================
    
    def test_self_contradictory_text(self):
        """Test: Text that contradicts itself"""
        contradictory = """
        Scientists have definitively proven that coffee is extremely beneficial for health, 
        reducing risks of all major diseases and extending lifespan significantly. However, 
        other researchers argue that coffee consumption should be completely avoided as it 
        causes numerous health problems and dramatically shortens life expectancy. The truth 
        probably lies somewhere in between, with moderate consumption being neither entirely 
        harmful nor universally beneficial, depending on individual genetic factors and 
        pre-existing conditions.
        """
        
        result = simplify_text(contradictory, reading_level="intermediate")
        assert len(result) > 0
        assert isinstance(result, str)

    def test_hypothetical_and_conditional_statements(self):
        """Test: Complex hypothetical scenarios"""
        hypothetical = """
        If the government were to implement a universal basic income (UBI) program, 
        assuming sufficient funding could be secured through taxation of automated 
        industries, and if recipients were able to maintain employment incentives 
        without reduction in workforce participation, then potentially poverty rates 
        might decrease while consumer spending could increase, thereby stimulating 
        economic growth. However, should inflation rise concomitantly, the purchasing 
        power of UBI payments might erode, negating intended benefits. Conversely, 
        if automation accelerates faster than anticipated, UBI might become fiscally 
        unsustainable regardless of tax policies.
        """
        
        result = simplify_text(hypothetical, reading_level="basic")
        assert isinstance(result, str)

    # ============================================================================
    # EDGE CASES - Very Short and Very Long Sentences
    # ============================================================================
    
    def test_extremely_short_sentences(self):
        """Test: Many very short sentences"""
        short_sentences = """
        Run. Stop. Wait. Go. Look. See. Hear. Listen. Speak. Talk. 
        Walk. Jump. Climb. Fall. Rise. Stand. Sit. Lie. Sleep. Wake.
        Eat. Drink. Cook. Clean. Wash. Dry. Fold. Store. Use. Need.
        Want. Have. Give. Take. Make. Break. Fix. Build. Create.
        """
        
        result = simplify_text(short_sentences, reading_level="basic")
        # Very short text might be returned as-is
        assert isinstance(result, str)

    def test_extremely_long_run_on_sentence(self):
        """Test: Single extremely long sentence"""
        runon = """
        The researcher who had been working at the university for over three decades 
        despite numerous opportunities to leave for better positions at more prestigious 
        institutions because she believed deeply in the importance of the work she was 
        doing which involved studying the effects of climate change on local ecosystems 
        particularly the migration patterns of birds that nested in the wetlands surrounding 
        the campus decided finally to publish her findings which spanned more than twenty 
        years of meticulous observation data collection analysis and peer review before 
        reaching conclusions that would fundamentally alter our understanding of how species 
        adapt to changing environmental conditions over extended periods.
        """
        
        result = simplify_text(runon, reading_level="basic")
        assert len(result) > 0
        assert isinstance(result, str)

    # ============================================================================
    # EDGE CASES - Repetitive and Redundant Content
    # ============================================================================
    
    def test_highly_repetitive_text(self):
        """Test: Text with extreme repetition"""
        repetitive = """
        The important thing to remember is that safety is paramount. Safety must always 
        come first. When we prioritize safety, we ensure safety in all our operations. 
        Safety protocols exist for safety reasons. Without safety measures, safety 
        cannot be guaranteed. Safety training teaches safety practices. Safety equipment 
        provides safety protection. Safety inspections verify safety compliance. Safety 
        is everyone's responsibility because safety affects everyone. Remember: safety 
        first, safety always, safety forever.
        """
        
        result = simplify_text(repetitive, reading_level="intermediate")
        assert isinstance(result, str)
        # Summarization should reduce redundancy
        assert len(result) < len(repetitive)

    # ============================================================================
    # EDGE CASES - Quotes and Dialogue
    # ============================================================================
    
    def test_nested_quotes_and_dialogue(self):
        """Test: Complex dialogue with nested quotations"""
        dialogue = """
        The professor said, "When I asked my mentor, 'Why does quantum mechanics 
        seem so counterintuitive?', she replied, 'Because reality doesn't owe us 
        common sense,' and then added, 'Remember Feynman's words: "If you think 
        you understand quantum mechanics, you don't understand quantum mechanics."'
        I responded, "But how can we teach something we don't understand?" She 
        smiled and said, 'We teach the mathematics, not the intuition.'"
        """
        
        result = simplify_text(dialogue, reading_level="basic")
        assert isinstance(result, str)

    # ============================================================================
    # EDGE CASES - Negative Constructions and Double Negatives
    # ============================================================================
    
    def test_double_negatives_and_complex_negation(self):
        """Test: Text with multiple negative constructions"""
        negatives = """
        It is not uncommon for researchers to find that their hypotheses are not 
        unsupported by evidence, but rather that they cannot be considered entirely 
        incorrect either. The committee did not disagree with the conclusion that 
        the policy was not ineffective, but they nonetheless recommended against 
        its implementation due to concerns that were not unrelated to budgetary 
        constraints. No one denied that the results were not insignificant.
        """
        
        result = simplify_text(negatives, reading_level="basic")
        assert isinstance(result, str)

    # ============================================================================
    # BOUNDARY CASES - Empty and Near-Empty Inputs
    # ============================================================================
    
    def test_empty_string(self):
        """Test: Empty string input"""
        result = simplify_text("", reading_level="intermediate")
        assert result == ""

    def test_whitespace_only(self):
        """Test: String with only whitespace"""
        result = simplify_text("   \n\t  ", reading_level="basic")
        assert isinstance(result, str)

    def test_single_word(self):
        """Test: Single word input"""
        result = simplify_text("Photosynthesis", reading_level="advanced")
        assert result == "Photosynthesis"  # Too short to simplify

    def test_two_words(self):
        """Test: Two word input"""
        result = simplify_text("Climate change", reading_level="basic")
        assert result == "Climate change"  # Too short to simplify

    # ============================================================================
    # STRESS TESTS - Combined Edge Cases
    # ============================================================================
    
    def test_worst_case_scenario(self):
        """Test: Maximum complexity - all edge cases combined"""
        worst_case = """
        Dr. Smith said, "The E = mc² formula, which Einstein introduced in 1905, 
        demonstrates—contrary to what many believe—that energy and mass are 
        interchangeable." But wait! What if we're wrong? Consider: 1) Quantum 
        entanglement suggests instantaneous connections defy relativity; 2) Dark 
        matter (85% of universe mass!) remains undetected; 3) String theory 
        proposes 10+ dimensions. ¡Increíble! The implications are profound...
        Class Node:
            def __init__(self, val):
                self.left = None
                self.right = None
                self.val = val
        This code implements a binary tree. But WHY? Because ℏ = h/2π appears in 
        Heisenberg's uncertainty principle: ΔxΔp ≥ ℏ/2. Fascinating! 🎉
        WHEREAS, the party agrees to disagree about the agreement's terms...
        Si la vie est une équation différentielle, alors l'amour est sa solution.
        Not unlike how 2x² + 5x - 3 = 0 yields x = 0.5 or x = -3 via quadratic formula.
        """
        
        result = simplify_text(worst_case, reading_level="intermediate")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_manual_fallback_scenarios(self):
        """Test: Manual simplification fallback"""
        test_cases = [
            ("This is a test.", "basic"),
            ("Short text.", "intermediate"),
            ("Very brief.", "advanced"),
        ]
        
        for text, level in test_cases:
            result = manual_simplify_text(text, reading_level=level)
            assert isinstance(result, str)
            assert len(result) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
