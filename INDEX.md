# lingThesis Project Directory Structure

This document provides an overview of the reorganized project structure for the experimental linguistics research investigating hate speech effects on cognitive processing.

## Project Overview

This is an experimental linguistics (psycholinguistics) research project investigating how hate speech affects cognitive processing and memory in Korean speakers using a Self-Paced Reading (SPR) paradigm.

**Research Questions:**
- H1: Does hate speech capture attention (longer reading times)?
- H2: Does hate speech narrow attention/reduce semantic integration?
- H3: Does hate speech bias memory encoding toward hate-consistent content?
- H4: Do people reproduce biased descriptions after exposure to hate speech?

## Directory Structure

```
lingThesis/
├── README.md                    # Main project documentation
├── INDEX.md                     # This file - directory structure guide
│
├── experiment/                  # Web-based SPR experiment
│   ├── index.html              # Main experiment interface
│   ├── index_pilot.html        # Pilot experiment version
│   ├── server.js               # Local Node.js server
│   ├── google-apps-script.js   # Google Sheets integration
│   ├── package.json            # Node.js dependencies
│   ├── js/                     # JavaScript experiment logic
│   │   ├── experiment.js       # Main experiment script
│   │   ├── experiment_pilot.js # Pilot experiment script
│   │   └── plugins/
│   │       └── jspsych-spr.js  # Custom SPR plugin
│   └── css/
│       └── style.css           # Experiment styling
│
├── stimuli/                     # Stimulus generation & data
│   ├── MasterSPR.csv           # Master stimulus list
│   ├── List1.csv               # Balanced stimulus list 1
│   ├── List2.csv               # Balanced stimulus list 2
│   ├── List3.csv               # Balanced stimulus list 3
│   ├── List4.csv               # Balanced stimulus list 4
│   ├── make_list.py            # Script to generate balanced lists
│   ├── convert_csv_to_json.py  # Convert CSV to JSON for web experiment
│   └── json/                   # JSON versions of stimulus lists
│       ├── list1.json
│       ├── list2.json
│       ├── list3.json
│       └── list4.json
│
├── scripts/                     # Python analysis & visualization
│   ├── analysis/               # Main statistical analyses
│   │   ├── Hypothesis_Check.py           # Primary hypothesis testing
│   │   ├── analyze_results.py            # Initial analysis script
│   │   ├── analyze_result_1201.py        # Updated analysis (Dec 1)
│   │   ├── revised_analysis.py           # Revised analysis approach
│   │   ├── revised_analysis_stricter.py  # Stricter criteria analysis
│   │   └── additional_analyses.py        # Supplementary analyses
│   │
│   ├── hypothesis_specific/    # Hypothesis-focused analyses
│   │   ├── analyze_h3_memory.py         # H3: Memory bias analysis
│   │   ├── analyze_h4_detailed.py       # H4: Reproduction analysis
│   │   └── analyze_h3_h4_integrated.py  # H3+H4 integrated analysis
│   │
│   ├── visualization/          # Plotting and figure generation
│   │   ├── Visualizations.py                      # Main visualization script
│   │   ├── create_presentation_figures.py         # Generate presentation figures
│   │   ├── create_presentation_figures_from_excel.py
│   │   ├── visualize_region_rt_lines.py           # Region reading time plots
│   │   ├── visualize_outlier_comparison.py        # Outlier comparison plots
│   │   ├── create_outlier_comparison_plots.py
│   │   └── visualize_h4_for_presentation.py       # H4 presentation figures
│   │
│   └── preprocessing/          # Data preprocessing
│       ├── apply_outlier_exclusion_1201.py  # Outlier detection/exclusion
│       ├── manipulation_check.py            # Verify experimental manipulations
│       └── detailed_region_analysis.py      # Region-by-region analysis
│
├── results/                     # Analysis outputs
│   ├── result_1128/            # First analysis round (Nov 28)
│   │   ├── *.png               # Visualizations
│   │   ├── *.md                # Analysis reports
│   │   ├── *.pdf               # PDF reports
│   │   ├── *.csv               # Summary statistics
│   │   └── *.xlsx              # Excel workbook
│   │
│   └── result_1201/            # Final analysis round (Dec 1)
│       ├── *.png               # Updated visualizations
│       ├── COMPLETE_ANALYSIS_REPORT.md
│       ├── COMPLETE_ANALYSIS_REPORT_EN.pdf
│       ├── H4_DETAILED_FINDINGS.pdf
│       ├── h4_presentation_plots/
│       └── outlier_comparison_plots/
│
├── documentation/               # Guides and references
│   ├── deployment/             # Deployment instructions
│   │   ├── DEPLOY_GITHUB.md
│   │   ├── FINAL_CHECKLIST.md
│   │   ├── DEBUG_GUIDE.md
│   │   └── TEST_CHECKLIST.txt
│   │
│   ├── technical/              # Technical documentation
│   │   ├── GOOGLE_SHEETS_SETUP.md
│   │   ├── GOOGLE_SHEETS_QUICKSTART.txt
│   │   ├── README_EXPERIMENT.md
│   │   ├── VISUALIZATION_GUIDE.md
│   │   └── CLAUDE.md           # Technical guidance for Claude AI
│   │
│   └── research/               # Research documentation
│       ├── PRESENTATION_OUTLINE.md
│       ├── H4_ANALYSIS_SUMMARY.md
│       └── command.md
│
├── presentations/               # Final outputs & papers
│   ├── JinilKim_TermProject.pdf      # Final term project paper
│   ├── JinilKim_TermProject.pptx     # Final presentation slides
│   ├── ExpLing_TermProject.pdf       # Original project description
│   ├── presentation.pdf              # LaTeX-generated presentation
│   ├── hypothesis_visualization.pdf  # Hypothesis diagrams
│   ├── stimuli_structure_table.pdf   # Stimuli design table
│   ├── Qualtrics_문구들.pdf          # Qualtrics text materials
│   ├── 나만_보는_실험_준비.pdf       # Experiment preparation notes
│   ├── 순서_및_후속_질문.pdf         # Task order & follow-up questions
│   │
│   └── latex_sources/          # LaTeX source files
│       ├── presentation.tex
│       ├── presentation.aux
│       ├── hypothesis_visualization.tex
│       ├── hypothesis_visualization.aux
│       ├── hypothesis_visualization.log
│       ├── stimuli_structure_table.tex
│       ├── stimuli_structure_table.aux
│       └── stimuli_structure_table.log
│
└── images/                      # Visual stimuli
    ├── 2024Hate.jpeg           # Hate speech illustration
    ├── factfalse.jpeg          # Fact vs. false illustration
    ├── fakenews.png            # Fake news illustration
    └── hatespeech.png          # Hate speech illustration
```

## Key Files

### Experiment Entry Points
- `experiment/index.html` - Main experiment (access with ?list=1-4 parameter)
- `experiment/index_pilot.html` - Pilot version

### Primary Analysis Scripts
- `scripts/analysis/Hypothesis_Check.py` - Main hypothesis testing
- `scripts/analysis/analyze_result_1201.py` - Most recent analysis

### Results
- `results/result_1201/` - Latest analysis results with outlier exclusion
- `results/result_1201/COMPLETE_ANALYSIS_REPORT.md` - Comprehensive findings

### Final Outputs
- `presentations/JinilKim_TermProject.pdf` - Final paper
- `presentations/JinilKim_TermProject.pptx` - Final presentation

## Running the Experiment

1. Open `experiment/index.html` in a web browser
2. Add `?list=N` parameter (N = 1, 2, 3, or 4) for specific stimulus list
3. Or let the script randomly assign a list

## Running Analyses

All Python scripts should be run from the project root directory:

```bash
# Main analysis
python scripts/analysis/Hypothesis_Check.py

# Hypothesis-specific analyses
python scripts/hypothesis_specific/analyze_h4_detailed.py

# Visualization
python scripts/visualization/Visualizations.py
```

## Notes

- LaTeX build artifacts (.aux, .log) are preserved for reproducibility
- Duplicate "further research" folder has been removed
- All file paths in experiment.js have been updated for new structure
- Python scripts may need path adjustments depending on input/output locations

## Research Contact

- **Researcher:** Jinil Kim
- **Phone:** 010-5264-9444
- **Email:** haba6030@snu.ac.kr
- **Institution:** Seoul National University, Department of Linguistics

---

*Last updated: December 26, 2025*
