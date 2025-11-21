/**
 * Main Experiment Script for Talren SPR Experiment
 * Uses jsPsych 7.x
 */

// ============================================================================
// 1. INITIALIZATION AND CONFIGURATION
// ============================================================================

// Generate random participant ID (6 digits)
const participant_id = Math.floor(Math.random() * 900000) + 100000;

// Parse URL parameters to determine which list to use
const urlParams = new URLSearchParams(window.location.search);
const list_param = urlParams.get('list');

// Determine list_id (1-4)
let list_id;
if (list_param && ['1', '2', '3', '4'].includes(list_param)) {
  list_id = parseInt(list_param);
} else {
  // If no valid list parameter, randomly assign one
  list_id = Math.floor(Math.random() * 4) + 1;
}

console.log(`Participant ID: ${participant_id}`);
console.log(`Assigned to List: ${list_id}`);

// Google Apps Script Web App URL
// TODO: Deploy Apps Script and paste your Web App URL here
const GOOGLE_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbzfsHLDd3i33J4eG0VtGAsAtype6W4KZyyyyQmeEgbTv2FnAX5o3hDeZv2qk1FKxFg4/exec';

// Track experiment start time
const experiment_start_time = Date.now();

// ============================================================================
// 2. INITIALIZE JSPSYCH
// ============================================================================

const jsPsych = initJsPsych({
  display_element: 'jspsych-target',
  on_finish: function() {
    // Save data to Google Sheets only
    saveDataToGoogleSheets();
  }
});

// Add participant and list info to all trials
jsPsych.data.addProperties({
  participant_id: participant_id,
  list_id: list_id
});

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================

/**
 * Shuffle array using Fisher-Yates algorithm
 * @param {Array} array - Array to shuffle
 * @returns {Array} - Shuffled array (creates new array, doesn't modify original)
 */
function shuffleArray(array) {
  const shuffled = [...array]; // Create copy
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled;
}

// ============================================================================
// 3. BACKGROUND PASSAGE TEXT (PLACEHOLDER - REPLACE WITH ACTUAL TEXT)
// ============================================================================

const BACKGROUND_PASSAGE = `
<div style="max-width: 700px; margin: 0 auto; text-align: left; line-height: 1.8;">
  <h2 style="text-align: center; margin-bottom: 30px;">탈렌족에 관한 배경 정보</h2>
  <p>
    탈렌족은 중앙아시아의 산악 지대에 거주했던 것으로 알려진 가상의 민족이다.
    이들의 생활 방식, 문화, 관습 등에 대한 다양한 기록이 전해져 내려오고 있다.
  </p>
  <p>
    탈렌족은 높은 산간 계곡에 위치한 여러 마을에 흩어져 거주하며, 주로 흙과 돌을 섞어 만든 반지하식 주택에서 살아간다. 이 지역은 일교차가 커서 의식이나 축제에서는 양털로 만든 겹옷을 입는 전통이 있다.
    식생활은 발효 곡물 음식, 산채류, 오리와 산양을 이용한 구이 요리가 중심을 이룬다.
    의식 전에는 허브 차를 마시는 관습이 있으며, 의식 중에는 공동체가 함께 모여 노래 의식을 치르는 것으로 알려져 있다.
  </p>
  <p>
    탈렌족은 장이라고 불리는 중앙 광장에서 토론을 진행하는 전통이 있고, 분쟁이 생길 때는 나이가 많은 구성원이 중재 의식을 주관한다.
    사회 구조는 비교적 느슨하지만, 마을마다 장인이 존재하여 목공·직조·도기 제작 등 기술이 세대 간에 전승된다.
    이동은 주로 산길을 따라 도보로 이루어지며, 교환과 무역은 계절별 장터를 중심으로 제한적으로 이루어진다.
  </p>
  <p>
    과거 인류학자들은 탈렌족이 외부 세력과의 접촉이 거의 없어, 관습과 믿음을 잘 유지해 왔다고 기록했다.
    이들은 자연을 신성한 존재로 여기는 정령 신앙을 가지고 있으며, 의식 중에는 산·물·바람을 상징하는 짧은 주술문을 외운다.
  </p>
  <div id="timer-display" style="text-align: center; margin-top: 30px; font-size: 18px; font-weight: bold; color: #666;">
    남은 시간: <span id="time-remaining">90</span>초
  </div>
</div>
`;

// ============================================================================
// 4. TIMELINE COMPONENTS
// ============================================================================

const timeline = [];

// ----------------------------------------------------------------------------
// 4.1 Welcome / Consent Screen
// ----------------------------------------------------------------------------

const welcome = {
  type: jsPsychHtmlButtonResponse,
  stimulus: `
    <div style="max-width: 700px; margin: 0 auto;">
      <h1>실험 참여에 오신 것을 환영합니다</h1>
      <p style="text-align: left; line-height: 1.8;">
        본 연구는 "탈렌족"에 관한 문장을 읽는 과정에서의
        언어 처리 양상을 알아보기 위한 실험입니다.
      </p>
      <p style="text-align: left; line-height: 1.8;">
        실험 중 일부 문장에는 부정적이거나 불쾌한 표현이 포함될 수 있습니다.
        이러한 표현들은 실험 조작의 일부이며, 어떤 실제 집단에 대한
        연구자의 견해를 반영하는 것이 아님을 알려드립니다.
      </p>
      <p style="text-align: left; line-height: 1.8;">
        실험은 약 20-25분 정도 소요됩니다.
        참여에 동의하시면 아래 "시작" 버튼을 눌러주세요.
      </p>
    </div>
  `,
  choices: ['시작'],
  button_html: '<button class="jspsych-btn" style="font-size: 18px; padding: 12px 40px;">%choice%</button>'
};

timeline.push(welcome);

// ----------------------------------------------------------------------------
// 4.2 Background Passage Instructions
// ----------------------------------------------------------------------------

const background_instructions = {
  type: jsPsychHtmlButtonResponse,
  stimulus: `
    <div style="max-width: 700px; margin: 0 auto;">
      <h2>배경 정보 안내</h2>
      <p style="text-align: left; line-height: 1.8;">
        이제 탈렌족에 대한 배경 정보를 제공합니다.
        다음으로 나올 글은 탈렌족에 대한 검증된 문헌을 발췌한 것입니다.
      </p>
      <p style="text-align: left; line-height: 1.8;">
        배경 정보는 <strong>90초 동안</strong> 제시되며,<br>
        시간이 지나면 자동으로 다음 단계로 넘어갑니다.
      </p>
      <p style="text-align: left; line-height: 1.8;">
        제시되는 내용을 주의 깊게 읽어주세요.
      </p>
    </div>
  `,
  choices: ['배경 정보 읽기'],
  button_html: '<button class="jspsych-btn" style="font-size: 18px; padding: 12px 40px;">%choice%</button>'
};

timeline.push(background_instructions);

// ----------------------------------------------------------------------------
// 4.3 Background Passage Screen (90 seconds, auto-advance)
// ----------------------------------------------------------------------------

const background = {
  type: jsPsychHtmlKeyboardResponse,
  stimulus: BACKGROUND_PASSAGE,
  choices: "NO_KEYS",
  trial_duration: 90000, // 90 seconds
  data: { trial_type: 'background_passage' },
  on_load: function() {
    // Start countdown timer
    let timeRemaining = 90;
    const timerElement = document.getElementById('time-remaining');

    const countdown = setInterval(function() {
      timeRemaining--;
      if (timerElement) {
        timerElement.textContent = timeRemaining;
      }

      if (timeRemaining <= 0) {
        clearInterval(countdown);
      }
    }, 1000);
  }
};

timeline.push(background);

// ----------------------------------------------------------------------------
// 4.4 SPR Instructions
// ----------------------------------------------------------------------------

const spr_instructions = {
  type: jsPsychHtmlButtonResponse,
  stimulus: `
    <div style="max-width: 700px; margin: 0 auto;">
      <h2>읽기 과제 안내</h2>
      <p style="text-align: left; line-height: 1.8;">
        이제 탈렌족에 관한 여러 문장들을 하나씩 읽게 됩니다.
        이는 탈렌족을 연구하던 19세기 인류학자들의 회고록에서 발췌한 문장들입니다. 
      </p>
      <p style="text-align: left; line-height: 1.8;">
        각 문장은 <strong>여러 부분으로 나뉘어</strong> 제시됩니다.<br>
        <strong>스페이스 바(SPACE)</strong>를 누르면 다음 부분이 나타납니다.
      </p>
      <p style="text-align: left; line-height: 1.8;">
        각 부분을 편안한 속도로 읽으시되, 너무 빠르거나 느리게 읽지 않도록 주의해주세요.
      </p>
      <p style="text-align: left; line-height: 1.8;">
        준비되셨으면 "연습 시작" 버튼을 눌러주세요.
      </p>
    </div>
  `,
  choices: ['연습 시작'],
  button_html: '<button class="jspsych-btn" style="font-size: 18px; padding: 12px 40px;">%choice%</button>'
};

timeline.push(spr_instructions);

// ----------------------------------------------------------------------------
// 4.5 SPR Practice Trial
// ----------------------------------------------------------------------------

const practice_spr = {
  type: jsPsychSpr,
  sentence: '이것은 연습 문장입니다. 스페이스 바를 눌러 다음 부분으로 진행하세요.',
  item_id: 'practice',
  base: 'practice',
  emotion: 'NA',
  plausibility: 'NA',
  version: 'NA',
  is_filler: 1,
  data: { trial_type: 'spr_practice' }
};

timeline.push(practice_spr);

// Practice complete message
const practice_complete = {
  type: jsPsychHtmlButtonResponse,
  stimulus: `
    <div style="max-width: 700px; margin: 0 auto;">
      <h2>연습 완료</h2>
      <p style="text-align: left; line-height: 1.8;">
        연습이 끝났습니다. 이제 본 실험을 시작하겠습니다.
      </p>
      <p style="text-align: left; line-height: 1.8;">
        같은 방식으로 문장을 읽으시면 됩니다.
      </p>
    </div>
  `,
  choices: ['본 실험 시작'],
  button_html: '<button class="jspsych-btn" style="font-size: 18px; padding: 12px 40px;">%choice%</button>'
};

timeline.push(practice_complete);

// ----------------------------------------------------------------------------
// 4.6 Load Stimuli and Create SPR Trials
// ----------------------------------------------------------------------------

const stimuli_file = `stimuli/list${list_id}.json`;

// Preload stimuli
const preload = {
  type: jsPsychPreload,
  auto_preload: true,
  trials: timeline
};

// Load and create SPR trials dynamically
fetch(stimuli_file)
  .then(response => response.json())
  .then(data => {
    console.log(`Loaded ${data.length} stimuli from ${stimuli_file}`);

    // IMPORTANT: Randomize stimulus order
    const randomized_data = shuffleArray(data);
    console.log('Stimuli randomized');

    // Store stimuli for later use
    window.stimuli_data = randomized_data;

    // Create SPR trials for each stimulus
    randomized_data.forEach((stim, index) => {
      const spr_trial = {
        type: jsPsychSpr,
        sentence: stim.stimulus_text,
        item_id: stim.item_id,
        base: stim.base || '',
        emotion: stim.emotion || '',
        plausibility: stim.plausibility || '',
        version: String(stim.version || ''),
        is_filler: stim.is_filler || 0,
        data: {
          trial_type: 'spr_main',
          trial_index: index
        }
      };
      timeline.push(spr_trial);
    });

    // Add break after SPR block
    const spr_break = {
      type: jsPsychHtmlButtonResponse,
      stimulus: `
        <div style="max-width: 700px; margin: 0 auto;">
          <h2>읽기 과제 완료</h2>
          <p style="text-align: left; line-height: 1.8;">
            문장 읽기가 끝났습니다. 잠시 휴식을 취하신 후 계속 진행해주세요.
          </p>
          <p style="text-align: left; line-height: 1.8;">
            다음 단계에서는 방금 읽은 문장들에 대한 몇 가지 질문이 이어집니다.
          </p>
        </div>
      `,
      choices: ['계속'],
      button_html: '<button class="jspsych-btn" style="font-size: 18px; padding: 12px 40px;">%choice%</button>'
    };
    timeline.push(spr_break);

    // --------------------------------------------------------------------
    // 4.7 Plausibility Rating Block
    // --------------------------------------------------------------------

    const rating_instructions = {
      type: jsPsychHtmlButtonResponse,
      stimulus: `
        <div style="max-width: 700px; margin: 0 auto;">
          <h2>진실성 평가</h2>
          <p style="text-align: left; line-height: 1.8;">
            이제 방금 읽은 문장들이 탈렌족에 대해
            얼마나 사실적이고 그럴듯한지 평가해주시기 바랍니다.
            기억이 잘 나지 않아도 괜찮습니다.
            여기서는 "얼마나 그럴듯해 보이는지"만 판단해주세요.
          </p>
          <p style="text-align: left; line-height: 1.8;">
            각 문장에 대해 1점(매우 명백히 거짓)부터 5점(매우 명백히 사실)까지 평가해주세요.
          </p>
        </div>
      `,
      choices: ['시작'],
      button_html: '<button class="jspsych-btn" style="font-size: 18px; padding: 12px 40px;">%choice%</button>'
    };
    timeline.push(rating_instructions);

    // Create rating trials for experimental items only (is_filler == 0)
    // Use randomized_data to maintain same order as SPR trials
    const experimental_items = randomized_data.filter(stim => stim.is_filler == 0);

    experimental_items.forEach((stim, index) => {
      const rating_trial = {
        type: jsPsychSurveyLikert,
        preamble: `<div style="max-width: 800px; margin: 0 auto; margin-bottom: 20px; font-size: 18px; line-height: 1.6;">${stim.stimulus_text}</div>`,
        questions: [
          {
            prompt: '이 문장은 탈렌족에 대해 얼마나 사실적이고 그럴듯합니까?',
            labels: [
              '1<br>매우 명백히<br>거짓',
              '2',
              '3<br>불확실',
              '4',
              '5<br>매우 명백히<br>사실'
            ],
            required: true
          }
        ],
        data: {
          trial_type: 'plausibility_rating',
          item_id: stim.item_id,
          base: stim.base || '',
          emotion: stim.emotion || '',
          plausibility: stim.plausibility || '',
          is_filler: stim.is_filler || 0,
          stimulus_text: stim.stimulus_text
        }
      };
      timeline.push(rating_trial);
    });

    // --------------------------------------------------------------------
    // 4.8 Free Recall Block (with 1-minute minimum)
    // --------------------------------------------------------------------

    const free_recall = {
      type: jsPsychSurveyText,
      preamble: `
        <div style="max-width: 700px; margin: 0 auto;">
          <h2>자유 회상</h2>
          <p style="text-align: left; line-height: 1.8;">
            지금까지 읽은 문장들을 바탕으로,
            탈렌족에 대해 기억나는 모든 내용을 자유롭게 적어주세요.
          </p>
          <p style="text-align: left; line-height: 1.8;">
            <strong>최소 1분 동안</strong> 작성해주셔야 다음 단계로 넘어갈 수 있습니다.
          </p>
          <div id="recall-timer" style="text-align: center; margin-top: 15px; font-size: 18px; font-weight: bold; color: #666;">
            남은 시간: <span id="recall-time-remaining">60</span>초
          </div>
        </div>
      `,
      questions: [
        {
          prompt: '탈렌족에 대해 기억나는 내용을 자유롭게 적어주세요:',
          rows: 10,
          columns: 60,
          required: false
        }
      ],
      data: { trial_type: 'free_recall' },
      on_load: function() {
        // Disable submit button initially
        const submitButton = document.querySelector('#jspsych-survey-text-next');
        if (submitButton) {
          submitButton.disabled = true;
          submitButton.style.opacity = '0.5';
          submitButton.style.cursor = 'not-allowed';
        }

        // Start 60-second countdown
        let timeRemaining = 60;
        const timerElement = document.getElementById('recall-time-remaining');
        const timerContainer = document.getElementById('recall-timer');

        const countdown = setInterval(function() {
          timeRemaining--;
          if (timerElement) {
            timerElement.textContent = timeRemaining;
          }

          if (timeRemaining <= 0) {
            clearInterval(countdown);
            // Enable submit button
            if (submitButton) {
              submitButton.disabled = false;
              submitButton.style.opacity = '1';
              submitButton.style.cursor = 'pointer';
            }
            // Change timer message
            if (timerContainer) {
              timerContainer.innerHTML = '<span style="color: #4CAF50;">✓ 이제 제출할 수 있습니다</span>';
            }
          }
        }, 1000);
      }
    };
    timeline.push(free_recall);

    // --------------------------------------------------------------------
    // 4.9 Manipulation Check Block
    // --------------------------------------------------------------------

    const manipulation_check_intro = {
      type: jsPsychHtmlButtonResponse,
      stimulus: `
        <div style="max-width: 700px; margin: 0 auto;">
          <h2>표현 평가</h2>
          <p style="text-align: left; line-height: 1.8;">
            마지막으로, 실험에 사용된 일부 표현들이
            얼마나 부정적으로 느껴지는지 평가해주시기 바랍니다.
          </p>
        </div>
      `,
      choices: ['시작'],
      button_html: '<button class="jspsych-btn" style="font-size: 18px; padding: 12px 40px;">%choice%</button>'
    };
    timeline.push(manipulation_check_intro);

    // Sample modifiers to check (you can customize these)
    const hate_modifiers = ['미개한', '열등한', '저급한', '야만적인', '뒤떨어진',
      '천박한', '나태한', '저능한', '무지한', '격떨어지는', '수준낮은'
    ];
    const neutral_modifiers = ['고립된', '자급자족의', '폐쇄적', '독특한', '산악의',
      '소규모의', '전통적인', '자연적인', '산맥의', '정착한', '관습적', '적응적'
    ];

    [...hate_modifiers, ...neutral_modifiers].forEach(modifier => {
      const mc_trial = {
        type: jsPsychSurveyLikert,
        preamble: `<div style="font-size: 20px; margin-bottom: 20px;">"<strong>${modifier}</strong>"</div>`,
        questions: [
          {
            prompt: '이 표현은 얼마나 부정적입니까?',
            labels: ['1<br>전혀<br>부정적이지<br>않음', '2', '3', '4', '5<br>매우<br>부정적'],
            required: true
          }
        ],
        data: {
          trial_type: 'manipulation_check',
          mc_type: 'modifier_negativity',
          modifier_text: modifier,
          modifier_category: hate_modifiers.includes(modifier) ? 'hate' : 'neutral'
        }
      };
      timeline.push(mc_trial);
    });

    // --------------------------------------------------------------------
    // 4.10 Debriefing
    // --------------------------------------------------------------------

    const debrief = {
      type: jsPsychHtmlButtonResponse,
      stimulus: `
        <div style="max-width: 700px; margin: 0 auto;">
          <h2>실험 종료 및 사후 설명</h2>
          <p style="text-align: left; line-height: 1.8;">
            실험에 참여해주셔서 감사합니다.
          </p>
          <p style="text-align: left; line-height: 1.8;">
            본 연구에서 사용된 "탈렌족"은 <strong>실제로 존재하지 않는 가상의 민족</strong>입니다.
            실험에 포함된 부정적 표현들은 언어 처리 과정에서의
            감정적 반응을 측정하기 위한 실험 조작의 일부였으며,
            어떤 실제 집단을 지칭하거나 비하하는 것이 아닙니다.
          </p>
          <p style="text-align: left; line-height: 1.8;">
            궁금하신 사항이나 실험 관련 문의는 아래 연락처로 문의해주시기 바랍니다.
          </p>
          <p style="text-align: left; line-height: 1.8;">
            <strong>연구자 연락처: 010-5264-9444</strong><br>
            이메일: haba6030@snu.ac.kr<br>
            소속: 서울대학교 언어학과
          </p>
          <p style="text-align: left; line-height: 1.8; margin-top: 30px;">
            "완료" 버튼을 누르면 데이터가 저장됩니다.
          </p>
        </div>
      `,
      choices: ['완료'],
      button_html: '<button class="jspsych-btn" style="font-size: 18px; padding: 12px 40px;">%choice%</button>'
    };
    timeline.push(debrief);

    // --------------------------------------------------------------------
    // Run the experiment
    // --------------------------------------------------------------------

    jsPsych.run(timeline);
  })
  .catch(error => {
    console.error('Error loading stimuli:', error);
    document.getElementById('jspsych-target').innerHTML = `
      <div style="padding: 50px; text-align: center;">
        <h2>오류 발생</h2>
        <p>자극 파일을 불러오는 중 오류가 발생했습니다.</p>
        <p>파일 경로를 확인해주세요: ${stimuli_file}</p>
        <p>Error: ${error.message}</p>
      </div>
    `;
  });

// ============================================================================
// 5. DATA SAVING FUNCTIONS
// ============================================================================

/**
 * Save data to Google Sheets via Apps Script Web App
 */
function saveDataToGoogleSheets() {
  // Show loading message
  document.getElementById('jspsych-target').innerHTML = `
    <div style="text-align: center; padding: 50px;">
      <div class="loading-spinner"></div>
      <h2 style="margin-top: 20px;">데이터를 저장하고 있습니다...</h2>
      <p>잠시만 기다려주세요.</p>
    </div>
  `;

  // Prepare data for Google Sheets
  const allData = jsPsych.data.get().values();

  // DEBUG: Log all trial types
  console.log('Total trials:', allData.length);
  console.log('All trial types:', allData.map(t => t.trial_type || 'UNDEFINED'));
  console.log('First SPR trial:', allData.find(t => t.trial_type && t.trial_type.includes('spr')));

  // Extract different types of data (flexible to handle both old and new trial_type values)
  const spr_data = allData.filter(trial =>
    trial.trial_type === 'spr_main' || trial.trial_type === 'spr'
  );
  const rating_data = allData.filter(trial =>
    (trial.trial_type === 'plausibility_rating' || trial.trial_type === 'survey-likert') &&
    trial.item_id && !trial.modifier_text  // Has item_id but not modifier_text
  );
  const recall_data = allData.find(trial =>
    trial.trial_type === 'free_recall' || trial.trial_type === 'survey-text'
  );
  const mc_data = allData.filter(trial =>
    trial.trial_type === 'manipulation_check' ||
    (trial.trial_type === 'survey-likert' && trial.modifier_text)  // Has modifier_text
  );
  const background_data = allData.find(trial => trial.trial_type === 'background_passage');

  // Debug: Log data counts
  console.log('Data counts:');
  console.log('- SPR trials:', spr_data.length);
  console.log('- Rating trials:', rating_data.length);
  console.log('- Recall trials:', recall_data ? 1 : 0);
  console.log('- MC trials:', mc_data.length);

  // Calculate total experiment duration
  const total_duration = Date.now() - experiment_start_time;

  // Prepare payload
  const payload = {
    dataType: 'complete',
    participant_id: participant_id,
    list_id: list_id,
    timestamp: new Date().toISOString(),
    total_duration: total_duration,
    background_reading_time: background_data ? background_data.rt : null,
    browser: navigator.userAgent,
    screen_width: screen.width,
    screen_height: screen.height,
    spr_data: spr_data.map(trial => ({
      trial_index: trial.trial_index,
      item_id: trial.item_id,
      base: trial.base,
      emotion: trial.emotion,
      plausibility: trial.plausibility,
      version: trial.version,
      is_filler: trial.is_filler,
      sentence_text: trial.sentence_text,
      total_regions: trial.total_regions,
      total_reading_time: trial.total_reading_time,
      regions: trial.regions,
      region_rts: trial.region_rts
    })),
    rating_data: rating_data.map(trial => ({
      item_id: trial.item_id,
      base: trial.base,
      emotion: trial.emotion,
      plausibility: trial.plausibility,
      stimulus_text: trial.stimulus_text,
      rating: trial.response ? trial.response.Q0 : null,
      rt: trial.rt
    })),
    recall_data: {
      text: recall_data && recall_data.response ? recall_data.response.Q0 : ''
    },
    mc_data: mc_data.map(trial => ({
      modifier_text: trial.modifier_text,
      modifier_category: trial.modifier_category,
      rating: trial.response ? trial.response.Q0 : null,
      rt: trial.rt
    }))
  };

  // Debug: Log payload summary
  console.log('Payload prepared:');
  console.log('- SPR data items:', payload.spr_data.length);
  console.log('- Rating data items:', payload.rating_data.length);
  console.log('- MC data items:', payload.mc_data.length);
  console.log('Full payload:', payload);

  console.log('About to send fetch request to:', GOOGLE_SCRIPT_URL);
  console.log('Payload size:', JSON.stringify(payload).length, 'characters');

  // Send to Google Sheets
  fetch(GOOGLE_SCRIPT_URL, {
    method: 'POST',
    mode: 'no-cors',  // Google Apps Script requires no-cors mode
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  })
  .then(response => {
    console.log('Response received');
    console.log('Response status:', response.status);
    console.log('Response ok:', response.ok);
    console.log('Response type:', response.type);
    return response.text();
  })
  .then(text => {
    console.log('Response body:', text);
    console.log('Data sent to Google Sheets');
    showCompletionMessage(true);
  })
  .catch(error => {
    console.error('Error saving to Google Sheets:', error);
    console.error('Error name:', error.name);
    console.error('Error message:', error.message);
    console.error('Error stack:', error.stack);
    showCompletionMessage(false, error.message);
  });
}

/**
 * Show completion message
 */
function showCompletionMessage(success, errorMsg = '') {
  const message = success
    ? `
      <div style="text-align: center; padding: 50px;">
        <h1 style="color: #4CAF50;">✓ 실험이 완료되었습니다!</h1>
        <p style="font-size: 18px; margin-top: 20px;">
          데이터가 성공적으로 저장되었습니다.<br>
          참여해주셔서 감사합니다.
        </p>
        <p style="margin-top: 30px; color: #666;">
          참가자 ID: ${participant_id}<br>
          리스트: ${list_id}
        </p>
        <p style="margin-top: 20px; font-size: 14px; color: #999;">
          이 창을 닫으셔도 됩니다.
        </p>
      </div>
    `
    : `
      <div style="text-align: center; padding: 50px;">
        <h1 style="color: #f44336;">⚠ 저장 중 오류 발생</h1>
        <p style="font-size: 18px; margin-top: 20px;">
          온라인 저장에 실패했지만, 로컬 백업이 다운로드되었습니다.
        </p>
        <p style="margin-top: 20px; color: #666;">
          오류 메시지: ${errorMsg}
        </p>
        <p style="margin-top: 30px;">
          다운로드된 CSV 파일을 연구자에게 전달해주세요.
        </p>
      </div>
    `;

  document.getElementById('jspsych-target').innerHTML = message;
}

/**
 * Save data to Node.js server (alternative method - kept for reference)
 */
function saveDataToServer() {
  const data = jsPsych.data.get().json();

  fetch('http://localhost:3000/save-data', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      participant_id: participant_id,
      list_id: list_id,
      data: data
    })
  })
  .then(response => response.json())
  .then(result => {
    console.log('Data saved to server:', result);
    alert('데이터가 성공적으로 저장되었습니다!');
  })
  .catch(error => {
    console.error('Error saving data to server:', error);
    alert('서버 저장 실패. 데이터를 로컬로 다운로드합니다.');
    jsPsych.data.get().localSave('csv', `talren_spr_data_p${participant_id}_list${list_id}.csv`);
  });
}
