/**
 * jspsych-spr
 *
 * Custom jsPsych plugin for Self-Paced Reading (SPR) experiments
 * Displays sentence regions one at a time, records RT for each region
 *
 * @author Created for Talren SPR Experiment
 * @version 1.0.0
 */

var jsPsychSpr = (function (jspsych) {
  'use strict';

  const info = {
    name: 'spr',
    parameters: {
      /** The full sentence to display region by region */
      sentence: {
        type: jspsych.ParameterType.STRING,
        pretty_name: 'Sentence',
        default: undefined
      },
      /** Item ID from the stimulus list */
      item_id: {
        type: jspsych.ParameterType.STRING,
        pretty_name: 'Item ID',
        default: ''
      },
      /** Base item identifier */
      base: {
        type: jspsych.ParameterType.STRING,
        pretty_name: 'Base',
        default: ''
      },
      /** Emotion condition (H or N) */
      emotion: {
        type: jspsych.ParameterType.STRING,
        pretty_name: 'Emotion',
        default: ''
      },
      /** Plausibility condition (P or I) */
      plausibility: {
        type: jspsych.ParameterType.STRING,
        pretty_name: 'Plausibility',
        default: ''
      },
      /** Version number (1 or 2) */
      version: {
        type: jspsych.ParameterType.STRING,
        pretty_name: 'Version',
        default: ''
      },
      /** Whether this is a filler item (0 or 1) */
      is_filler: {
        type: jspsych.ParameterType.INT,
        pretty_name: 'Is Filler',
        default: 0
      },
      /** Key to press to advance to next region */
      advance_key: {
        type: jspsych.ParameterType.KEY,
        pretty_name: 'Advance key',
        default: ' '
      },
      /** Instruction text shown below the region */
      instruction_text: {
        type: jspsych.ParameterType.STRING,
        pretty_name: 'Instruction text',
        default: 'SPACE를 눌러 다음 부분으로 진행하세요.'
      }
    }
  };

  class SprPlugin {
    constructor(jsPsych) {
      this.jsPsych = jsPsych;
    }

    trial(display_element, trial) {
      // Split sentence into regions (by whitespace)
      const regions = trial.sentence.trim().split(/\s+/);

      // Data storage
      const region_rts = [];
      const region_texts = [];
      let current_region = 0;
      let region_start_time;

      // Create HTML structure
      const html = `
        <div class="spr-container">
          <div class="spr-region" id="spr-region-text"></div>
          <div class="spr-instruction">${trial.instruction_text}</div>
        </div>
      `;
      display_element.innerHTML = html;

      const region_element = display_element.querySelector('#spr-region-text');

      // Function to display a region
      const show_region = (region_index) => {
        if (region_index >= regions.length) {
          // All regions shown, end trial
          end_trial();
          return;
        }

        // Display the current region
        const region_text = regions[region_index];
        region_element.textContent = region_text;
        region_texts.push(region_text);

        // Record start time for this region
        region_start_time = performance.now();
        current_region = region_index;
      };

      // Function to handle key press
      const after_key_response = (info) => {
        // Record RT for the current region
        const rt = Math.round(performance.now() - region_start_time);
        region_rts.push(rt);

        // Move to next region
        show_region(current_region + 1);
      };

      // Function to end trial and save data
      const end_trial = () => {
        // Remove keyboard listener
        this.jsPsych.pluginAPI.cancelAllKeyboardResponses();

        // Collect trial data
        const trial_data = {
          // Use trial_type from trial.data if available, otherwise default to 'spr'
          ...trial.data,
          item_id: trial.item_id,
          base: trial.base,
          emotion: trial.emotion,
          plausibility: trial.plausibility,
          version: trial.version,
          is_filler: trial.is_filler,
          sentence_text: trial.sentence,
          regions: JSON.stringify(region_texts),
          region_rts: JSON.stringify(region_rts),
          total_regions: regions.length,
          total_reading_time: region_rts.reduce((a, b) => a + b, 0)
        };

        // Clear display
        display_element.innerHTML = '';

        // End trial
        this.jsPsych.finishTrial(trial_data);
      };

      // Set up keyboard listener
      this.jsPsych.pluginAPI.getKeyboardResponse({
        callback_function: after_key_response,
        valid_responses: [trial.advance_key],
        rt_method: 'performance',
        persist: true,
        allow_held_key: false
      });

      // Show first region
      show_region(0);
    }
  }

  SprPlugin.info = info;

  return SprPlugin;
})(jsPsychModule);
