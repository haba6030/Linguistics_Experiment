/**
 * PILOT VERSION - Talren SPR Experiment
 * Shortened for quick testing
 * - Only 8 SPR trials (2 per condition)
 * - No time limits
 * - Reduced manipulation check items
 */

// ============================================================================
// CONFIGURATION
// ============================================================================

const participant_id = Math.floor(Math.random() * 900000) + 100000;
const urlParams = new URLSearchParams(window.location.search);
const list_param = urlParams.get('list');
let list_id = list_param && ['1', '2', '3', '4'].includes(list_param)
  ? parseInt(list_param)
  : Math.floor(Math.random() * 4) + 1;

console.log(`[PILOT] Participant ID: ${participant_id}`);
console.log(`[PILOT] Assigned to List: ${list_id}`);

const GOOGLE_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbzfsHLDd3i33J4eG0VtGAsAtype6W4KZyyyyQmeEgbTv2FnAX5o3hDeZv2qk1FKxFg4/exec';
const experiment_start_time = Date.now();

// ============================================================================
// INITIALIZE JSPSYCH
// ============================================================================

const jsPsych = initJsPsych({
  display_element: 'jspsych-target',
  on_finish: function() {
    saveDataToGoogleSheets();
  }
});

jsPsych.data.addProperties({
  participant_id: participant_id,
  list_id: list_id,
  version: 'pilot'
});

function shuffleArray(array) {
  const shuffled = [...array];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled;
}

// ============================================================================
// BACKGROUND TEXT (SHORTENED)
// ============================================================================

const BACKGROUND_PASSAGE = `
<div style="max-width: 700px; margin: 0 auto; text-align: left; line-height: 1.8;">
  <h2 style="text-align: center; margin-bottom: 30px;">탈렌족에 관한 배경 정보</h2>
  <p>
    탈렌족은 중앙아시아의 산악 지대에 거주했던 가상의 민족입니다.
    이들의 생활 방식과 문화에 대한 다양한 기록이 전해져 내려오고 있습니다.
  </p>
  <p style="color: #ff6600; font-weight: bold; text-align: center; margin-top: 30px;">
    ⚡ 파일럿 버전: 시간 제한 없이 자유롭게 읽으세요
  </p>
</div>
`;

// ============================================================================
// TIMELINE
// ============================================================================

const timeline = [];

// Welcome
timeline.push({
  type: jsPsychHtmlButtonResponse,
  stimulus: `
    <div style="max-width: 700px; margin: 0 auto;">
      <h1>⚡ 파일럿 테스트</h1>
      <p style="text-align: left; line-height: 1.8;">
        <strong style="color: #ff6600;">단축 버전:</strong> 빠른 테스트를 위해 문항 수를 줄였습니다.
      </p>
      <ul style="text-align: left;">
        <li>SPR: 4개 문장</li>
        <li>평가: 4개 문장</li>
        <li>표현 평가: 3개</li>
        <li>시간 제한: 없음</li>
        <li>예상 소요 시간: 약 2분</li>
      </ul>
    </div>
  `,
  choices: ['시작'],
  button_html: '<button class="jspsych-btn" style="font-size: 18px; padding: 12px 40px;">%choice%</button>'
});

// Background (no timer)
timeline.push({
  type: jsPsychHtmlButtonResponse,
  stimulus: BACKGROUND_PASSAGE,
  choices: ['계속'],
  button_html: '<button class="jspsych-btn" style="font-size: 18px; padding: 12px 40px;">%choice%</button>',
  data: { trial_type: 'background_passage' }
});

// SPR Instructions
timeline.push({
  type: jsPsychHtmlButtonResponse,
  stimulus: `
    <div style="max-width: 700px; margin: 0 auto;">
      <h2>읽기 과제 안내</h2>
      <p style="text-align: left; line-height: 1.8;">
        문장이 여러 부분으로 나뉘어 제시됩니다.<br>
        <strong>스페이스 바(SPACE)</strong>를 눌러 진행하세요.
      </p>
    </div>
  `,
  choices: ['시작'],
  button_html: '<button class="jspsych-btn" style="font-size: 18px; padding: 12px 40px;">%choice%</button>'
});

// Load stimuli
const stimuli_file = `stimuli/list${list_id}.json`;

fetch(stimuli_file)
  .then(response => response.json())
  .then(data => {
    console.log(`[PILOT] Loaded ${data.length} total stimuli`);

    // PILOT: Take only first 4 items (1 from each base)
    const pilot_data = data.slice(0, 4);
    const randomized_data = shuffleArray(pilot_data);

    console.log(`[PILOT] Using ${randomized_data.length} items`);

    // SPR trials
    randomized_data.forEach((stim, index) => {
      timeline.push({
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
      });
    });

    // Break
    timeline.push({
      type: jsPsychHtmlButtonResponse,
      stimulus: `
        <div style="max-width: 700px; margin: 0 auto;">
          <h2>읽기 완료!</h2>
          <p>이제 간단한 평가를 진행합니다.</p>
        </div>
      `,
      choices: ['계속'],
      button_html: '<button class="jspsych-btn" style="font-size: 18px; padding: 12px 40px;">%choice%</button>'
    });

    // Rating trials (only experimental items)
    const experimental_items = randomized_data.filter(stim => stim.is_filler == 0);

    experimental_items.forEach((stim) => {
      timeline.push({
        type: jsPsychSurveyLikert,
        preamble: `<div style="max-width: 800px; margin: 0 auto; margin-bottom: 20px; font-size: 18px; line-height: 1.6;">${stim.stimulus_text}</div>`,
        questions: [{
          prompt: '이 문장은 탈렌족에 대해 얼마나 사실적이고 그럴듯합니까?',
          labels: [
            '1<br>매우 명백히<br>거짓',
            '2',
            '3<br>불확실',
            '4',
            '5<br>매우 명백히<br>사실'
          ],
          required: true
        }],
        data: {
          trial_type: 'plausibility_rating',
          item_id: stim.item_id,
          base: stim.base || '',
          emotion: stim.emotion || '',
          plausibility: stim.plausibility || '',
          is_filler: stim.is_filler || 0,
          stimulus_text: stim.stimulus_text
        }
      });
    });

    // Free recall (NO TIME LIMIT in pilot)
    timeline.push({
      type: jsPsychSurveyText,
      preamble: `
        <div style="max-width: 700px; margin: 0 auto;">
          <h2>자유 회상</h2>
          <p style="text-align: left; line-height: 1.8;">
            탈렌족에 대해 기억나는 내용을 간단히 적어주세요.
          </p>
          <p style="color: #ff6600; font-weight: bold;">
            ⚡ 파일럿: 시간 제한 없음 (짧게 작성해도 됩니다)
          </p>
        </div>
      `,
      questions: [{
        prompt: '탈렌족에 대해 기억나는 내용:',
        rows: 5,
        columns: 60,
        required: false
      }],
      data: { trial_type: 'free_recall' }
    });

    // Manipulation check (REDUCED - only 6 items)
    timeline.push({
      type: jsPsychHtmlButtonResponse,
      stimulus: `
        <div style="max-width: 700px; margin: 0 auto;">
          <h2>표현 평가</h2>
          <p style="color: #ff6600; font-weight: bold;">⚡ 파일럿: 3개 항목만</p>
        </div>
      `,
      choices: ['시작'],
      button_html: '<button class="jspsych-btn" style="font-size: 18px; padding: 12px 40px;">%choice%</button>'
    });

    // Reduced MC items (2 hate + 1 neutral)
    const hate_modifiers = ['미개한', '열등한'];
    const neutral_modifiers = ['고립된'];

    [...hate_modifiers, ...neutral_modifiers].forEach(modifier => {
      timeline.push({
        type: jsPsychSurveyLikert,
        preamble: `<div style="font-size: 20px; margin-bottom: 20px;">"<strong>${modifier}</strong>"</div>`,
        questions: [{
          prompt: '이 표현은 얼마나 부정적입니까?',
          labels: ['1<br>전혀<br>부정적이지<br>않음', '2', '3', '4', '5<br>매우<br>부정적'],
          required: true
        }],
        data: {
          trial_type: 'manipulation_check',
          mc_type: 'modifier_negativity',
          modifier_text: modifier,
          modifier_category: hate_modifiers.includes(modifier) ? 'hate' : 'neutral'
        }
      });
    });

    // Debrief
    timeline.push({
      type: jsPsychHtmlButtonResponse,
      stimulus: `
        <div style="max-width: 700px; margin: 0 auto;">
          <h2>⚡ 파일럿 테스트 완료</h2>
          <p style="text-align: left; line-height: 1.8;">
            테스트에 참여해주셔서 감사합니다!
          </p>
          <p style="text-align: left; line-height: 1.8; color: #666;">
            참가자 ID: ${participant_id}<br>
            리스트: ${list_id}<br>
            버전: PILOT
          </p>
        </div>
      `,
      choices: ['완료'],
      button_html: '<button class="jspsych-btn" style="font-size: 18px; padding: 12px 40px;">%choice%</button>'
    });

    // Run experiment
    jsPsych.run(timeline);
  })
  .catch(error => {
    console.error('Error loading stimuli:', error);
    document.getElementById('jspsych-target').innerHTML = `
      <div style="padding: 50px; text-align: center;">
        <h2>오류 발생</h2>
        <p>자극 파일을 불러올 수 없습니다: ${stimuli_file}</p>
      </div>
    `;
  });

// ============================================================================
// DATA SAVING
// ============================================================================

function saveDataToGoogleSheets() {
  document.getElementById('jspsych-target').innerHTML = `
    <div style="text-align: center; padding: 50px;">
      <div class="loading-spinner"></div>
      <h2 style="margin-top: 20px;">데이터 저장 중...</h2>
    </div>
  `;

  const allData = jsPsych.data.get().values();

  // DEBUG: Log all trial types
  console.log('[PILOT] Total trials:', allData.length);
  console.log('[PILOT] All trial types:', allData.map(t => t.trial_type || 'UNDEFINED'));
  console.log('[PILOT] First SPR trial:', allData.find(t => t.trial_type && t.trial_type.includes('spr')));

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

  console.log('[PILOT] Data counts:', {
    spr: spr_data.length,
    rating: rating_data.length,
    recall: recall_data ? 1 : 0,
    mc: mc_data.length
  });

  const payload = {
    dataType: 'complete',
    participant_id: participant_id,
    list_id: list_id,
    timestamp: new Date().toISOString(),
    total_duration: Date.now() - experiment_start_time,
    background_reading_time: background_data ? background_data.rt : null,
    browser: navigator.userAgent,
    screen_width: screen.width,
    screen_height: screen.height,
    version: 'pilot',
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

  console.log('[PILOT] About to send fetch request to:', GOOGLE_SCRIPT_URL);
  console.log('[PILOT] Payload size:', JSON.stringify(payload).length, 'characters');

  fetch(GOOGLE_SCRIPT_URL, {
    method: 'POST',
    mode: 'no-cors',  // Google Apps Script requires no-cors mode
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })
  .then(response => {
    console.log('[PILOT] Response received');
    console.log('[PILOT] Response status:', response.status);
    console.log('[PILOT] Response ok:', response.ok);
    console.log('[PILOT] Response type:', response.type);
    return response.text();
  })
  .then(text => {
    console.log('[PILOT] Response body:', text);
    document.getElementById('jspsych-target').innerHTML = `
      <div style="text-align: center; padding: 50px;">
        <h1 style="color: #4CAF50;">✓ 완료!</h1>
        <p style="font-size: 18px; margin-top: 20px;">
          파일럿 테스트 데이터가 저장되었습니다.
        </p>
        <p style="margin-top: 30px; color: #666;">
          참가자 ID: ${participant_id}<br>
          버전: PILOT
        </p>
      </div>
    `;
  })
  .catch(error => {
    console.error('[PILOT] Save error:', error);
    console.error('[PILOT] Error name:', error.name);
    console.error('[PILOT] Error message:', error.message);
    console.error('[PILOT] Error stack:', error.stack);
    document.getElementById('jspsych-target').innerHTML = `
      <div style="text-align: center; padding: 50px;">
        <h1 style="color: #f44336;">⚠ 저장 실패</h1>
        <p>${error.message}</p>
        <p style="font-size: 14px; color: #666; margin-top: 20px;">
          브라우저 콘솔(F12)을 확인해주세요.
        </p>
      </div>
    `;
  });
}
