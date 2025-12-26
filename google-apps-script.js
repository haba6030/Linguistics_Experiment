/**
 * Google Apps Script for Talren SPR Experiment Data Collection
 *
 * SETUP INSTRUCTIONS:
 * 1. Google Drive에서 새 Google Sheets 생성
 * 2. Extensions > Apps Script 메뉴 선택
 * 3. 이 코드를 복사해서 붙여넣기
 * 4. Deploy > New deployment 클릭
 *    - Type: Web app
 *    - Execute as: Me
 *    - Who has access: Anyone
 * 5. Deploy 후 나온 Web app URL을 복사
 * 6. experiment.js에서 GOOGLE_SCRIPT_URL 변수에 붙여넣기
 */

// ============================================================================
// CONFIGURATION
// ============================================================================

// 시트 이름 설정
const SHEET_NAMES = {
  SPR_DATA: 'SPR_Data',
  RATING_DATA: 'Rating_Data',
  RECALL_DATA: 'Recall_Data',
  MANIPULATION_CHECK: 'Manipulation_Check',
  METADATA: 'Metadata'
};

// ============================================================================
// MAIN HANDLER
// ============================================================================

/**
 * POST 요청을 처리하는 메인 함수
 */
function doPost(e) {
  try {
    // CORS 헤더 설정
    const output = ContentService.createTextOutput();
    output.setMimeType(ContentService.MimeType.JSON);

    // 요청 데이터 파싱
    const data = JSON.parse(e.postData.contents);

    // 데이터 유형에 따라 적절한 시트에 저장
    if (data.dataType === 'complete') {
      // 전체 실험 데이터
      saveCompleteData(data);
      return output.setContent(JSON.stringify({
        success: true,
        message: 'All data saved successfully',
        timestamp: new Date().toISOString()
      }));
    }

    return output.setContent(JSON.stringify({
      success: false,
      message: 'Unknown data type'
    }));

  } catch (error) {
    return ContentService.createTextOutput(JSON.stringify({
      success: false,
      error: error.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

/**
 * GET 요청 처리 (테스트용)
 */
function doGet(e) {
  return ContentService.createTextOutput(JSON.stringify({
    status: 'ok',
    message: 'Talren SPR Data Collection Endpoint',
    timestamp: new Date().toISOString()
  })).setMimeType(ContentService.MimeType.JSON);
}

// ============================================================================
// DATA SAVING FUNCTIONS
// ============================================================================

/**
 * 전체 실험 데이터를 시트에 저장
 */
function saveCompleteData(data) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const timestamp = new Date();

  // Debug logging
  Logger.log('saveCompleteData called');
  Logger.log('Participant ID: ' + data.participant_id);
  Logger.log('List ID: ' + data.list_id);
  Logger.log('SPR data length: ' + (data.spr_data ? data.spr_data.length : 0));
  Logger.log('Rating data length: ' + (data.rating_data ? data.rating_data.length : 0));
  Logger.log('MC data length: ' + (data.mc_data ? data.mc_data.length : 0));

  // 1. Metadata 저장
  saveMetadata(ss, data, timestamp);
  Logger.log('Metadata saved');

  // 2. SPR 데이터 저장
  if (data.spr_data && data.spr_data.length > 0) {
    saveSPRData(ss, data.spr_data, data.participant_id, data.list_id, timestamp);
    Logger.log('SPR data saved: ' + data.spr_data.length + ' items');
  } else {
    Logger.log('WARNING: No SPR data to save');
  }

  // 3. Rating 데이터 저장
  if (data.rating_data && data.rating_data.length > 0) {
    saveRatingData(ss, data.rating_data, data.participant_id, data.list_id, timestamp);
    Logger.log('Rating data saved: ' + data.rating_data.length + ' items');
  } else {
    Logger.log('WARNING: No Rating data to save');
  }

  // 4. Recall 데이터 저장
  if (data.recall_data) {
    saveRecallData(ss, data.recall_data, data.participant_id, data.list_id, timestamp);
    Logger.log('Recall data saved');
  }

  // 5. Manipulation Check 데이터 저장
  if (data.mc_data && data.mc_data.length > 0) {
    saveManipulationCheckData(ss, data.mc_data, data.participant_id, data.list_id, timestamp);
    Logger.log('MC data saved: ' + data.mc_data.length + ' items');
  } else {
    Logger.log('WARNING: No MC data to save');
  }
}

/**
 * Metadata 시트에 참가자 정보 저장
 */
function saveMetadata(ss, data, timestamp) {
  let sheet = ss.getSheetByName(SHEET_NAMES.METADATA);

  if (!sheet) {
    sheet = ss.insertSheet(SHEET_NAMES.METADATA);
    sheet.appendRow([
      'Timestamp',
      'Participant_ID',
      'List_ID',
      'Background_Reading_Time_ms',
      'Total_Experiment_Duration_ms',
      'Browser',
      'Screen_Width',
      'Screen_Height'
    ]);
  }

  sheet.appendRow([
    timestamp,
    data.participant_id,
    data.list_id,
    data.background_reading_time || '',
    data.total_duration || '',
    data.browser || '',
    data.screen_width || '',
    data.screen_height || ''
  ]);
}

/**
 * SPR 데이터 저장
 */
function saveSPRData(ss, sprData, participantId, listId, timestamp) {
  let sheet = ss.getSheetByName(SHEET_NAMES.SPR_DATA);

  if (!sheet) {
    sheet = ss.insertSheet(SHEET_NAMES.SPR_DATA);
    sheet.appendRow([
      'Timestamp',
      'Participant_ID',
      'List_ID',
      'Trial_Index',
      'Item_ID',
      'Base',
      'Emotion',
      'Plausibility',
      'Version',
      'Is_Filler',
      'Sentence_Text',
      'Total_Regions',
      'Total_Reading_Time_ms',
      'Regions',
      'Region_RTs'
    ]);
  }

  sprData.forEach(trial => {
    sheet.appendRow([
      timestamp,
      participantId,
      listId,
      trial.trial_index || '',
      trial.item_id || '',
      trial.base || '',
      trial.emotion || '',
      trial.plausibility || '',
      trial.version || '',
      trial.is_filler || 0,
      trial.sentence_text || '',
      trial.total_regions || '',
      trial.total_reading_time || '',
      trial.regions || '',
      trial.region_rts || ''
    ]);
  });
}

/**
 * Rating 데이터 저장
 */
function saveRatingData(ss, ratingData, participantId, listId, timestamp) {
  let sheet = ss.getSheetByName(SHEET_NAMES.RATING_DATA);

  if (!sheet) {
    sheet = ss.insertSheet(SHEET_NAMES.RATING_DATA);
    sheet.appendRow([
      'Timestamp',
      'Participant_ID',
      'List_ID',
      'Item_ID',
      'Base',
      'Emotion',
      'Plausibility',
      'Stimulus_Text',
      'Rating',
      'RT_ms'
    ]);
  }

  ratingData.forEach(trial => {
    sheet.appendRow([
      timestamp,
      participantId,
      listId,
      trial.item_id || '',
      trial.base || '',
      trial.emotion || '',
      trial.plausibility || '',
      trial.stimulus_text || '',
      trial.rating || '',
      trial.rt || ''
    ]);
  });
}

/**
 * Recall 데이터 저장
 */
function saveRecallData(ss, recallData, participantId, listId, timestamp) {
  let sheet = ss.getSheetByName(SHEET_NAMES.RECALL_DATA);

  if (!sheet) {
    sheet = ss.insertSheet(SHEET_NAMES.RECALL_DATA);
    sheet.appendRow([
      'Timestamp',
      'Participant_ID',
      'List_ID',
      'Recall_Text'
    ]);
  }

  sheet.appendRow([
    timestamp,
    participantId,
    listId,
    recallData.text || ''
  ]);
}

/**
 * Manipulation Check 데이터 저장
 */
function saveManipulationCheckData(ss, mcData, participantId, listId, timestamp) {
  let sheet = ss.getSheetByName(SHEET_NAMES.MANIPULATION_CHECK);

  if (!sheet) {
    sheet = ss.insertSheet(SHEET_NAMES.MANIPULATION_CHECK);
    sheet.appendRow([
      'Timestamp',
      'Participant_ID',
      'List_ID',
      'Modifier_Text',
      'Modifier_Category',
      'Negativity_Rating',
      'RT_ms'
    ]);
  }

  mcData.forEach(trial => {
    sheet.appendRow([
      timestamp,
      participantId,
      listId,
      trial.modifier_text || '',
      trial.modifier_category || '',
      trial.rating || '',
      trial.rt || ''
    ]);
  });
}
