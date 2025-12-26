# Outlier Exclusion Criteria for SPR Data (result_1201)

## Overview
This document describes the outlier exclusion criteria applied to the self-paced reading (SPR) reaction time data for the 1201 dataset.

## Rationale
- **Extremely short RTs (<200ms)**: Likely anticipatory responses or button mashing, not genuine reading
- **Extremely long RTs (>3000ms or >1600ms)**: May reflect distraction, confusion, or task disengagement
- The presence of RTs in the 1600-1800ms range for neutral modifiers suggests potential outliers that could distort the analysis

## Exclusion Criteria Applied

### Criterion 1: Original (200-3000ms)
- **Lower bound**: 200ms
- **Upper bound**: 3000ms
- **Rationale**: Standard broad exclusion used in SPR research
- This is the baseline criterion used in initial analyses

### Criterion 2: Stricter (200-1600ms)
- **Lower bound**: 200ms
- **Upper bound**: 1600ms
- **Rationale**: More conservative upper bound to exclude potentially distracted trials
- Recommended when data shows substantial RTs >1600ms that appear disconnected from normal reading behavior

## Comparison Strategy
We apply both criteria and compare:
1. **Descriptive statistics**: Mean RT by condition before and after exclusion
2. **Effect sizes**: How exclusion affects the hate vs. neutral comparison
3. **Statistical power**: Number of observations retained
4. **Distribution shape**: Visual inspection of RT distributions

## Implementation
- Exclusion applied to modifier region RTs (the critical manipulation region)
- All other data columns retained for excluded trials (for transparency)
- Both versions of the dataset saved for sensitivity analysis

## Recommendation
- If results are robust across both criteria → use Original (200-3000ms) for maximum power
- If results differ substantially → use Stricter (200-1600ms) to ensure data quality
- If extreme outliers are participant-specific → consider participant-level exclusion

---
Generated: 2025-12-02
Dataset: result_1201
