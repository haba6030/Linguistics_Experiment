# Cognitive Linguistics Research Experiment

Self-Paced Reading (SPR): Hate-speech & plausibility

## 📋 Abstract

- **Task**: Self-Paced Reading
- **IV**:
  - Emotion: Hate vs. Neutral
  - Plausibility: Plausible vs. Implausible
- **DV**:
  - Regional RT
  - Likert scale on Plausibility (1-5 scale)
- **Structure**: 2×2 Latin Square (list of 4)

## 📁 프로젝트 구조

```
TermProject/
├── index.html                 # 본 실험 (20-25분)
├── index_pilot.html           # 파일럿 (2분)
├── css/
│   └── style.css
├── js/
│   ├── experiment.js          # 본 실험: 44 SPR, 32 Rating, 23 MC
│   ├── experiment_pilot.js    # 파일럿: 4 SPR, 4 Rating, 3 MC
│   └── plugins/
│       └── jspsych-spr.js
├── stimuli/
│   ├── list1.json            # Latin Square List 1
│   ├── list2.json            # Latin Square List 2
│   ├── list3.json            # Latin Square List 3
│   └── list4.json            # Latin Square List 4
└── google-apps-script.js      # Apps Script 코드 (참고용)
```

## 🔗 실험 URL

### 리스트 지정
```
?list=1  # List 1
?list=2  # List 2
?list=3  # List 3
?list=4  # List 4
```
리스트를 지정하지 않으면 자동으로 무작위 할당됩니다.

Built with [jsPsych 7.3.4](https://www.jspsych.org/)
