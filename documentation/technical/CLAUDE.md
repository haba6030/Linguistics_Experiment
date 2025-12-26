# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an experimental linguistics (psycholinguistics) term project that generates balanced stimulus lists for a self-paced reading (SPR) experiment. The experiment manipulates two factors:
- **Emotion**: H (Hateful/derogatory) vs N (Neutral)
- **Plausibility**: P (Plausible) vs I (Implausible)

The study examines how readers process statements about the fictional "탈렌족" (Talen tribe) under different emotional valence and plausibility conditions.

## Commands

Run the list generation script:
```bash
python make_list.py
```

This reads `MasterSPR.csv` and generates four balanced lists: `List1.csv`, `List2.csv`, `List3.csv`, `List4.csv`.

## Architecture

### Experimental Design

**Latin Square Design**: Each list contains all base items (B1-B20), but each base appears in only ONE of the four conditions (HP, HI, NP, NI) per list. This ensures:
- No participant sees the same base twice
- All conditions are balanced across lists
- Each base has 2 versions per condition (version 1 and 2)

**List Structure**:
- List 1: All conditions use version 1
- List 2: All conditions use version 2
- List 3: HP uses v1, HI uses v2, NP uses v1, NI uses v2
- List 4: HP uses v2, HI uses v1, NP uses v2, NI uses v1

### Data Flow

1. **Input**: `MasterSPR.csv`
   - Contains all experimental stimuli and fillers
   - Each base item (B1-B20) has 8 rows: 4 conditions × 2 versions
   - Fillers marked by `base=NA` or `plausibility=P_filler`

2. **Processing** (make_list.py:42-68):
   - Creates mapping: `(base, emotion, plausibility) → {version: row_data}`
   - For each list, iterates through bases in order
   - For each base, selects ONE condition per the condition order: HP→HI→NP→NI
   - Picks the appropriate version according to the list's version pattern

3. **Output**: Four CSV files (List1-4.csv)
   - Contains columns: `list_id`, `item_id`, `base`, `emotion`, `plausibility`, `version`, `stimulus_text`, `is_filler`
   - Experimental items (`is_filler=0`) + all fillers (`is_filler=1`)

### Key Implementation Details

**Condition Order** (make_list.py:23-30): The fixed order `[HP, HI, NP, NI]` determines which condition is assigned to each base's "slot" in the list. The `cond_idx` maps to the version pattern.

**Version Patterns** (make_list.py:34-39): Dictionary defines which version (1 or 2) to use for each of the 4 condition positions per list.

**Filler Handling** (make_list.py:74-82): All fillers are included in every list identically. They are not counterbalanced.

## File Structure

- `MasterSPR.csv`: Master stimulus file with all conditions and versions
- `make_list.py`: List generation script
- `List1.csv` through `List4.csv`: Output files for experiment administration
- PDF files contain Korean documentation about experimental procedures and Qualtrics setup

## Data analysis strategy
### Research Questions
As an expert of experimental social linguistics, We are going to check below questions: 
1. Does hate speech **impair semantic processing**?
2. Does hate speech **enhance memory retention** due to emotional salience?
3. Does hate speech **increase the likelihood of negative content reproduction** in participants’ own language?

### Hypotheses
Therefore, main four hypotheses are as below: 
H1 (Attention capture): Hate-modifier sentences will show **longer reading times at the hate modifier** than at neutral modifiers.
   - This reflects affect-driven attentional capture.

H2 (Attention narrowing & shallow integration): 
1. At the critical noun and spillover regions, neutral-modifier sentences will show a clear plausibility effect (implausible > plausible RT)
2. Whereas **in the hate condition** this **plausibility effect will be reduced**,
   - This indicates shallower integration of subsequent content under attentional narrowing.

H3 (Biased memory / “trade-off + distortion”):
Relative to neutral context, hate context will lead to    
   (a) **Lower accuracy** for neutral/factual statements 
   (b) **Higher false alarm rates** for hate-consistent lures
   - This reflects a biased encoding of central hate-consistent elements and reduced encoding of peripheral factual details.

H4 (Encoding bias in reproduction)
Free descriptions after hate context will contain    
   (a) a **higher proportion of hate-consistent propositions** and negative adjectives
   (b) **fewer neutral background details**, compared to descriptions after neutral context
   - This indicating a **biased and partially distorted reproduction** of the target group.
   - However, due to experimental design that operated within-subject design, it would be infeasible to directly compare the response between hate context and neutral context - each participant saw both set
Therefore, as a preliminary & exploratory review:
   (a) Participants with more reading time at the hate modifier would contain more negative nuance and fewer background information.
   (b) Participants who showed reduced plausibility effect would contain more negative nuance and fewer background information.

### How to analyze
For statistical analysis, use MLE to control item and participant's confounding effect. 
For the SPR data, you should parse the words. 

1. Operate statistical test to check above hypotheses. 
2. Also, visualize the distribution of dependent variables to validate & the result of statistical tests above. 
3. As the stimuli sentences share same structure, visualize each part's (mean) Reaction time's mean and confidence interval. X axis is each part and Y axis is Reaction time. 
4. With H2 & H3, show the main and interaction effect of plausibility and hateness to RT or accuracy. 
5. Besides main hypotheses, test the difference of secondary metrics, such as RT of manipulation check. Manipulation check's negativity rating will be used to validate the modifier category (hate or neutral). 