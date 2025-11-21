# Talren SPR Experiment

Self-Paced Reading (SPR) 실험: 탈렌족에 대한 혐오 표현과 그럴듯함 조작 연구

## 📋 실험 개요

- **과제**: 자기조절 읽기 (Self-Paced Reading)
- **독립변인**:
  - 감정 (Emotion): Hate vs. Neutral
  - 그럴듯함 (Plausibility): Plausible vs. Implausible
- **종속변인**:
  - 영역별 읽기 시간 (Region RT)
  - 그럴듯함 평가 (1-5점)
- **설계**: 2×2 Latin Square (4개 리스트)

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
