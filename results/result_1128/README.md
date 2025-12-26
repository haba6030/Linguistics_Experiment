# Results Directory - README

This directory contains comprehensive analysis outputs for the Experimental Linguistics Term Project examining hate speech effects on reading comprehension and memory.

## 📁 Files Overview

### 📊 **Data**
- `ExpLing_Project.xlsx` - Raw experimental data (5 sheets: SPR, Rating, Manipulation Check, Recall, Metadata)

### 📈 **Visualizations**
1. **`analysis_plots.png`** (4 panels)
   - Panel 1: Mean RT by word position (overall)
   - Panel 2: H1 test - Modifier RT by Emotion (Hate vs Neutral)
   - Panel 3: H2 test - Emotion × Plausibility interaction
   - Panel 4: Manipulation check - Negativity ratings (violin + swarm plot)

2. **`distribution_plots.png`** (3 panels)
   - Panel 1: RT distribution at modifiers (Hate vs Neutral)
   - Panel 2: RT distribution at critical regions (Plausible vs Implausible)
   - Panel 3: Negativity rating distribution (Hate vs Neutral modifiers)

3. **`detailed_region_analysis.png`** (6 panels)
   - Panel 1: Word-by-word RT - Emotion effect
   - Panel 2: Word-by-word RT - Plausibility effect
   - Panel 3: Heatmap - RT by position × emotion
   - Panel 4: All four conditions (HP, HI, NP, NI)
   - Panel 5: Attention capture by region (difference scores)
   - Panel 6: Plausibility effect by region and emotion (H2 test)

### 📝 **Reports**
1. **`SUMMARY.md`** - **START HERE** - Quick reference guide with key findings
2. **`ANALYSIS_REPORT.md`** - Comprehensive technical report (~5000 words) with:
   - Full hypothesis tests
   - Statistical models (mixed effects)
   - Interpretation and discussion
   - Limitations and recommendations
   - 8 detailed sections

3. **`statistics_table.txt`** - Clean summary table of all statistical tests

### 💻 **Code**
- `../analyze_results.py` - Main analysis script
- `../detailed_region_analysis.py` - Word-by-word analysis script

---

## 🚀 Quick Start

### If you want a quick overview:
👉 **Read `SUMMARY.md`** (5 min read)

### If you want full details:
👉 **Read `ANALYSIS_REPORT.md`** (20 min read)

### If you want to see the data:
👉 **Look at the 3 PNG files** (visualizations are self-explanatory)

### If you want to rerun analysis:
```bash
python ../analyze_results.py
python ../detailed_region_analysis.py
```

---

## 📌 Key Findings at a Glance

| Finding | Status | Evidence |
|---------|--------|----------|
| ✅ Manipulation works | **STRONG** | t=25.43, p<.0001, d=4.33 |
| ⚠️ H1: Attention capture | Trend | +12ms, p=.569 (underpowered) |
| ❌ H2: Shallow integration | Not supported | Opposite pattern, p=.204 |
| ⚠️ H3: Memory bias | Inconclusive | Needs proper old/new coding |
| 📝 H4: Reproduction bias | Pending | Needs qualitative analysis |

**Bottom line:** Pilot study successful, but **N=6 too small**. Need **N≥30** for replication.

---

## 📖 How to Interpret the Visualizations

### `analysis_plots.png`
- **Top-left:** Overall word reading pattern - RTs decrease across sentence
- **Top-right:** H1 - Look for hate bars being taller than neutral (marginal)
- **Bottom-left:** H2 - Lines should diverge if interaction exists (they don't)
- **Bottom-right:** Manipulation check - Clear separation = success ✅

### `distribution_plots.png`
- **Left:** Hate (red) shifted right = longer RT (H1 trend)
- **Middle:** Large overlap = weak plausibility effect (H2 issue)
- **Right:** Bimodal = perfect manipulation (hate high, neutral low)

### `detailed_region_analysis.png`
- **Panel 1 (top-left):** Red line above blue = attention capture (mostly overlapping)
- **Panel 5 (bottom-left):** Bars above zero = attention capture at that position (none significant - all gray)
- **Panel 6 (bottom-right):** Diverging lines = interaction (lines cross back and forth = no consistent pattern)

---

## 🔍 What to Look For

### Strong Evidence (What Worked)
1. **Manipulation check** - Panel 4 of analysis_plots.png shows perfect separation
2. **Data quality** - Distributions look normal, outlier rate only 0.5%
3. **Feasibility** - All 6 participants completed full protocol (~18 min)

### Weak Evidence (What Needs Work)
1. **H1 effect** - Visible in distributions but not significant
2. **H2 effect** - Plausibility manipulation didn't work as expected
3. **Sample size** - N=6 provides only 15% power for medium effects

### Missing Analyses (Future Work)
1. **H4** - Free recall content coding (6 Korean text responses)
2. **Individual differences** - Correlations between RT patterns and recall
3. **Item analysis** - Which specific items drove effects?

---

## 📧 Next Steps

### For Publication
1. Increase N to 30-40
2. Strengthen plausibility manipulation (pilot test)
3. Add comprehension questions
4. Pre-register replication study

### For Class Presentation
1. Show manipulation check (clear success)
2. Show word-by-word patterns (complexity)
3. Emphasize pilot nature and power analysis
4. Discuss methodological contributions

### For Thesis/Dissertation
1. Use as pilot data for grant applications
2. Report effect sizes for meta-analysis
3. Highlight novel paradigm (hate speech + SPR)
4. Discuss theoretical implications despite low power

---

## 🛠️ Technical Details

### Statistical Methods Used
- **Mixed-effects models** with random intercepts for participants
- **Maximum Likelihood Estimation (MLE)** for parameter estimation
- **Outlier removal:** RT < 200ms or > 3000ms (0.5% of data)
- **Paired t-tests** as backup when mixed models failed to converge

### Software
- Python 3.x
- pandas (data manipulation)
- statsmodels (mixed effects models)
- scipy (statistical tests)
- matplotlib + seaborn (visualization)

### Data Structure
- **Within-subjects design:** 2 (Emotion: H/N) × 2 (Plausibility: P/I)
- **Latin square counterbalancing:** 4 lists
- **Base items:** 20 experimental + fillers
- **Word regions:** 9-12 per sentence (variable length)

---

## 📚 References

See `ANALYSIS_REPORT.md` Section 6.5 for detailed recommendations and `CLAUDE.md` in parent directory for full project documentation.

---

**Analysis Date:** November 28, 2025
**Analyst:** Claude Code (Anthropic)
**Questions?** Refer to detailed report or rerun scripts with `--help` flag
