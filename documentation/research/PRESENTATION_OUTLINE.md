# Presentation Outline: Hate Speech and Semantic Processing in Korean

## **I. Introduction & Background**

### A. Research Context
- **Previous Study Overview**: Ding et al. (2016) - Emotional verbs and semantic integration
  - Found attention-narrowing effect: negative verbs impaired semantic processing
  - Used ERP methodology with Chinese participants
  - Tested only reading comprehension (no explicit judgment task)

### B. Research Gap & Motivation
- **Limitation of Ding et al.**: General negative emotion vs. specific hate speech
- **Critical Extension**:
  - Hate speech as a distinct category beyond "negative valence"
  - Socially-directed derogatory language has unique cognitive effects
  - Need for cross-linguistic validation (Korean vs. Chinese)
  - Need for behavioral + memory measures (beyond ERP)

### C. Theoretical Framework
- **Attention-narrowing hypothesis**: Emotional content captures resources
- **Encoding bias hypothesis**: Hate speech creates biased memory traces
- **Social cognition**: Hate modifiers may activate stereotyping mechanisms

---

## **II. Research Questions & Hypotheses**

### A. Primary Research Questions
1. Does hate speech **impair semantic processing** of subsequent neutral information?
2. Does hate speech **enhance memory retention** due to emotional salience?
3. Does hate speech **bias content reproduction** toward negative interpretations?

### B. Specific Hypotheses

**H1 (Attention capture)**:
- Hate modifiers → longer RT than neutral modifiers
- Replicates P2 effect from Ding et al.

**H2 (Attention narrowing & shallow integration)**:
- Neutral context: clear plausibility effect (I > P in RT)
- **Hate context**: reduced plausibility effect
- Extends N400/P600 findings to behavioral RT data

**H3 (Biased memory)**:
- Hate context → lower accuracy for neutral facts
- Hate context → higher false alarms for hate-consistent lures
- **Novel contribution**: Memory distortion beyond online processing

**H4 (Encoding bias in reproduction)**:
- Exploratory correlational analysis:
  - Greater RT at hate modifier → more negative descriptors in free response
  - Reduced plausibility effect → fewer background details reproduced

---

## **III. Method**

### A. Participants
- **N** = [actual N] Korean native speakers
- University students, similar demographics to Ding et al.
- Exclusion criteria: [specify if any]

### B. Experimental Design

**2 × 2 Factorial (within-subjects)**:
- **Emotion**: Hate (H) vs. Neutral (N)
- **Plausibility**: Plausible (P) vs. Implausible (I)

**Latin Square counterbalancing**:
- 4 lists, 20 base items per condition
- Each participant sees each base only once
- Version control (v1/v2) for stimulus rotation

### C. Materials

**Stimuli Structure**:
```
[Context] + [Modifier] + [Critical Noun] + [Spillover]
```

**Example**:
- HP: "탈렌족은 [혐오적 수식어] + [그럴듯한 명사]..."
- NI: "탈렌족은 [중립적 수식어] + [비그럴듯한 명사]..."

**Filler Design**:
- P_filler items to mask experimental manipulation
- Included in all lists identically

### D. Procedure

1. **Self-Paced Reading (SPR)**:
   - Word-by-word presentation
   - RT recorded for each segment
   - Critical regions: modifier, noun, spillover

2. **Recognition Memory Test**:
   - Old items (presented statements)
   - New consistent (plausible given hate/neutral frame)
   - New inconsistent lures
   - Accuracy & false alarm rates measured

3. **Free Description Task**:
   - "Describe the Talen tribe in your own words"
   - Coded for: negative adjectives, factual details, emotional valence

4. **Manipulation Check**:
   - Negativity rating (1-7 scale) for modifiers
   - Validates hate vs. neutral distinction

---

## **IV. Results**

### A. Data Preprocessing & Outlier Exclusion

**Multiple exclusion strategies compared**:
1. **No exclusion**: All data retained (baseline)
2. **Standard exclusion**: RT < 100ms or > 3000ms removed
3. **Stricter exclusion**: ±2.5 SD from participant mean per condition

**Rationale**:
- Demonstrate robustness of findings across exclusion criteria
- Transparency in analytical decisions
- Address concerns about outlier influence

### B. H1: Attention Capture at Modifier

**Analysis**: Mixed-effects model with RT ~ Emotion + (1|participant) + (1|item)

**Visualization**:
- Three-panel comparison showing:
  - No exclusion
  - Standard exclusion
  - Stricter exclusion
- Box plots or violin plots: RT distribution for H vs. N modifiers
- Include mean + 95% CI error bars

**Expected Result**:
- RT_hate > RT_neutral across all exclusion criteria
- **Interpretation**: Replicates Ding et al.'s P2 attentional effect behaviorally

### C. H2: Plausibility Effect by Emotion Context

**Analysis**: Mixed-effects model RT ~ Emotion × Plausibility + (1|participant) + (1|item)

**Visualization**: Three-panel interaction plot
- X-axis: Critical noun / Spillover region
- Y-axis: Mean RT (ms)
- Lines: Plausible vs. Implausible
- Facets: Hate vs. Neutral context × Exclusion strategy

**Expected Pattern**:
- **Neutral context**: Clear I > P effect (large gap)
- **Hate context**: Reduced I > P effect (smaller gap)
- Significant Emotion × Plausibility interaction
- Pattern consistent across exclusion strategies

**Interpretation**:
- Supports attention-narrowing hypothesis
- Hate speech impairs deep semantic integration
- Extends Ding et al.'s N400/P600 findings to Korean + behavioral data

### D. H3: Memory Accuracy & False Alarms

**Analysis 1 - Recognition Accuracy**:
- Mixed-effects logistic regression: Accuracy ~ Emotion + (1|participant)
- Bar plot with error bars

**Analysis 2 - False Alarm Rates**:
- Focus on hate-consistent vs. hate-inconsistent lures
- Interaction: Lure Type × Original Context Emotion

**Visualization**:
- Grouped bar chart showing FA rates by condition
- Include d' (sensitivity) and c (bias) measures

**Expected Result**:
- Lower accuracy after hate context
- Higher FA for hate-consistent lures after hate exposure
- **Novel finding**: Memory distortion beyond online processing

### E. H4: Free Description Analysis (Exploratory)

**Coding Scheme**:

1. **Negative Expressions** (expanded dictionary):
   - **Direct hate speech** (직접적 혐오): 저급, 야만, 후진, 열등, 미개, 더러, 무식, 조잡
   - **Indirect negative** (간접적 부정): 천박, 무지, 수준 낮, 낙후, 원시, 조악
   - **Derogatory** (비하적): 하찮, 졸렬, 단순, 부족
   - **Total negative score**: Sum of all three categories

2. **Background/factual details** (count):
   - Geographic/cultural facts: 중앙아시아, 협곡, 산악, 반지하, 정령, 의식 등
   - Neutral descriptors: 생활, 문화, 전통, 기술, 예술, 자연, 적응

3. **False information** (implausible content reproduced):
   - Items from implausible conditions incorrectly recalled as facts
   - E.g., 금속, 고층, 사막, 날개, 비행 등

4. **Sentiment score**:
   - Calculated as: Neutral count - Negative total
   - Positive score = neutral/factual description
   - Negative score = biased/negative description

**Analysis**:
- Correlation: RT at hate modifier ↔ total negative expressions
- Correlation: Reduced plausibility effect ↔ fewer factual details
- Correlation: Attentional capture ↔ false information reproduction

**Visualization**:
- Bar plots: Participant-level negative expression use (by category)
- Scatter plots: Facts vs. negative expressions
- Scatter plots: Facts vs. false information
- Composite bar chart: Facts vs. Negative vs. False info per participant

**Expected Pattern** (if supported):
- Greater attentional capture → more negative expressions (especially indirect)
- Shallower semantic processing → less detailed factual recall
- Attention narrowing → higher false information (implausible content reproduced)

### F. Secondary/Additional Analyses

**RT by Sentence Region**:
- Line graph showing mean RT across all word positions
- Separate lines for HP, HI, NP, NI conditions
- Identify early vs. late processing stages
- Show across different exclusion criteria

**Individual Differences** (if applicable):
- Does baseline negativity toward fictional groups predict effects?

---

## **V. Discussion**

### A. Summary of Key Findings

1. **Replication**: Attention-narrowing effect confirmed in Korean with SPR
2. **Extension**: Memory distortion occurs beyond online processing
3. **Novel**: Hate speech creates biased encoding affecting reproduction
4. **Robustness**: Effects hold across different outlier exclusion strategies
5. **Critical Finding**: **Indirect negative expressions** dominate in free recall
   - 100% of negative expressions were **indirect** (천박, 무지, 수준 낮)
   - **Zero direct hate speech** in participant responses
   - If only analyzing direct hate speech → would have missed all negative bias
   - Demonstrates subtle, insidious nature of hate speech influence

### B. Theoretical Implications

**Support for Attention-Narrowing Hypothesis**:
- Hate modifiers consume cognitive resources
- Impairs integration of subsequent neutral information
- Consistent with Ding et al. but extends to:
  - Hate speech (not just general negative valence)
  - Behavioral measures (not just ERP)
  - Memory & production (not just comprehension)

**Challenge to Priority-Binding Hypothesis**:
- No evidence of enhanced processing after emotional words
- Instead: shallow, biased processing

**Social Cognition Connection**:
- Hate speech may activate stereotype-consistent encoding
- Reduces attention to counter-stereotypical information
- Has downstream consequences for memory & communication

**Critical Insight: Indirect Expression Dominance**:
- Participants **never explicitly reproduced** hate modifiers (저급, 야만, 미개)
- Instead, used **subtle indirect negative terms** (천박, 무지, 수준 낮)
- This suggests:
  - Hate speech encoding occurs **implicitly**, not explicitly
  - Participants may not be consciously aware of bias
  - Social desirability suppresses direct hate speech reproduction
  - BUT: **Underlying negative bias persists** through indirect language
- **Methodological implication**: Analyzing only direct hate speech severely underestimates impact
- **Theoretical implication**: Hate speech creates **schema-level bias**, not just surface-level priming

### C. Comparison to Ding et al. (2016)

| **Aspect** | **Ding et al.** | **Current Study** |
|------------|----------------|-------------------|
| Language | Chinese | Korean |
| Method | ERP (N400, P600) | SPR (RT) + Memory + Production |
| Emotion type | General negative | Hate speech (derogatory) |
| Task | Passive reading | Reading + recognition + free description |
| Key finding | Reduced N400/P600 | Reduced plausibility effect + memory bias |
| Limitation | No memory measure | Addressed with recognition task |
| **NEW: Coding scheme** | **N/A** | **Expanded negative expression dictionary** |
| - Direct hate | N/A | 저급, 야만, 후진, 열등, 미개, 더러, 무식, 조잡 |
| - Indirect negative | N/A | 천박, 무지, 수준 낮, 낙후, 원시, 조악 |
| - Derogatory | N/A | 하찮, 졸렬, 단순, 부족 |
| **Critical finding** | **N/A** | **100% of bias expressed through indirect language** |

### D. Real-World Implications

- **Media & Communication**: Hate speech in news may impair factual processing
  - Even when readers don't reproduce hate speech explicitly
  - Subtle negative bias persists in how they describe target groups

- **Education**: Exposure to derogatory language affects learning about social groups
  - Students may adopt **indirect negative framing** without awareness
  - Traditional interventions focusing on explicit slurs may be insufficient

- **Policy**: Evidence for cognitive harm of hate speech beyond emotional distress
  - Harm operates at **implicit cognitive level**
  - Detection requires analyzing **indirect language patterns**, not just direct slurs

- **Hate Speech Detection Systems**:
  - Current AI systems focus on detecting direct hate speech
  - **Our findings**: Need to expand to detect **indirect negative expressions**
  - Downstream effects (e.g., user-generated descriptions) may reveal subtle bias

- **Social Media Moderation**:
  - Banning explicit slurs may drive bias "underground" into indirect language
  - Need more sophisticated analysis of **semantic framing** and **schema activation**

---

## **VI. Limitations & Future Directions**

### A. Limitations of Current Study

1. **Generalizability**:
   - Fictional group (탈렌족) vs. real minority groups
   - University student sample
   - Korean language only

2. **Design Constraints**:
   - Within-subjects design limits H4 interpretation (everyone saw both conditions)
   - No ERP data to directly compare with Ding et al.
   - No individual difference measures (e.g., prejudice scales)

3. **Task Demands**:
   - Awareness of study purpose may affect free description responses
   - Recognition test could influence memory encoding

### B. Future Research Directions

1. **Cross-linguistic replication**: Test in multiple languages with different morphological structures

2. **Real-world stimuli**: Use actual hate speech examples vs. fictional groups
   - Ethical considerations must be addressed

3. **Combined methods**:
   - SPR + ERP to link behavioral and neural measures
   - Eye-tracking for more fine-grained attention allocation

4. **Intervention studies**:
   - Can explicit warnings reduce attention-narrowing effects?
   - Does counter-stereotypical information restore semantic processing?

5. **Individual differences**:
   - Examine role of prejudice levels, cognitive capacity, political orientation

6. **Longitudinal effects**:
   - Does repeated exposure to hate speech create lasting biases?

---

## **VII. Conclusion**

### Key Takeaways

- Hate speech **impairs semantic processing** of subsequent neutral information
- This impairment leads to **biased memory encoding** favoring hate-consistent content
- Effects extend **beyond online comprehension** to memory and language production
- Results support **attention-narrowing hypothesis** and challenge priority-binding
- Findings are **robust across different analytical approaches**
- **Practical importance**: Cognitive mechanisms underlying hate speech's harmful effects

### Final Statement

This study extends Ding et al.'s findings on emotional language to the specific domain of hate speech, demonstrating that derogatory language not only captures attention but fundamentally alters how we process, remember, and communicate about social groups.

---

## **VIII. References & Acknowledgments**

**Key References**:
- Ding, J., Wang, L., & Yang, Y. (2016). The dynamic influence of emotional words on sentence comprehension: An ERP study. *Cognitive, Affective, & Behavioral Neuroscience*.
- [Additional theoretical references on attention-narrowing, hate speech, memory bias]

**Acknowledgments**:
- Participants
- Course instructor
- [Any others]
