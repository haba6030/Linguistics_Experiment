
You are an expert JavaScript/jsPsych developer. Your task is to build a complete, ready-to-run online self-paced reading (SPR) experiment using jsPsych. I will provide you with my stimulus CSV files (MasterSPR.csv and 4 list files: List1.csv, List2.csv, List3.csv, List4.csv). Please read the instructions carefully and then generate all necessary code files.
“I will also upload my CSV files (MasterSPR.csv and List1–4). Please use them.”
⸻

1. Input data description

I will give you these CSV files:
	1.	MasterSPR.csv
Columns (exact names):
	•	item_id (e.g., E1, E2, …, F1, F2 …)
	•	base (B1–B8 for experimental items, NA or empty for fillers)
	•	emotion (H or N, or NA for fillers)
	•	plausibility (P, I, or P_filler for fillers)
	•	version (1 or 2 for experimental items, NA for fillers)
	•	stimulus_text (Korean sentence to display)
	2.	List1.csv, List2.csv, List3.csv, List4.csv
These are already counterbalanced lists derived from MasterSPR.csv.
Each list file has at least the following columns:
	•	item_id
	•	base
	•	emotion
	•	plausibility
	•	version
	•	stimulus_text
	•	is_filler (0 = experimental item, 1 = filler)

You may assume:
	•	Each list has 32 experimental items (8 bases × 4 conditions: H×P, H×I, N×P, N×I)
plus a number of fillers.
	•	The subject should see only one list (between List1–List4).

⸻

2. Overall technical requirements

Create a minimal jsPsych project with the following structure (you can adjust filenames if needed, but keep it clean and consistent):
	•	index.html
	•	js/
	•	jspsych.js (assume we include jsPsych via CDN is also fine)
	•	plugins/ (standard jsPsych plugins + one custom SPR plugin)
	•	experiment.js (main experiment logic)
	•	stimuli/
	•	list1.json, list2.json, list3.json, list4.json
(you should show how to convert the CSVs to JSON format, or load CSV directly if you prefer)
	•	css/
	•	style.css

You do NOT need to actually download jsPsych yourself; just write the correct HTML <script> tags (using a current jsPsych CDN), and assume I will include any external library files myself. Focus on the experiment logic and structure.

⸻

3. Experimental design and flow

Implement the following flow in jsPsych:
	1.	Welcome / Consent screen
	•	Simple HTML page explaining that the study is about reading sentences about a fictional group (“Talren족”), with potentially negative descriptions.
	•	A “Start” button to proceed.
	2.	Background passage screen
	•	Show a longer background text (I will fill in the actual Korean passage later; use a placeholder variable and a clear comment where to insert it).
	•	Either:
	•	A “Continue” button that the participant clicks once they feel they have read it, and
	•	Optionally record the time spent on this page in the data.
	•	No JavaScript timing tricks beyond jsPsych; basic html-button-response is fine.
	3.	List selection logic
	•	The experiment must select one of the four lists based on a URL parameter.
	•	Use a query parameter like ?list=1, ?list=2, etc.
	•	If no list parameter is provided, you may:
	•	Randomly choose one list between 1 and 4, OR
	•	Default to list 1.
	•	After determining list_id, load the corresponding stimuli (list1.json, list2.json, etc.).
	4.	Self-Paced Reading (SPR) block
	•	For each row in the selected list:
	•	Show the sentence in region-by-region fashion using a custom jsPsych plugin.
	•	Regions can be defined as simple whitespace-based tokens (split by spaces).
	•	The participant presses the spacebar to move to the next region.
	•	Only one region is visible at a time.
	•	For each region, record:
	•	region_index
	•	region_text
	•	rt (time in ms from appearance of region to keypress)
	•	Also keep track of:
	•	item_id
	•	base
	•	emotion
	•	plausibility
	•	version
	•	is_filler
	•	Implement this as a custom jsPsych plugin (for example jspsych-spr.js) that:
	•	Receives stimulus_text and meta-data as parameters.
	•	Splits the sentence into regions.
	•	Displays them sequentially with keyboard control.
	•	Logs each region’s RT in the trial data.
	•	The UI should:
	•	Center the region text on screen.
	•	Use a reasonably large font (e.g., 28 px) and plenty of vertical margin.
	•	Show a small instruction line like “Press SPACE to proceed to the next part of the sentence.”
	5.	Plausibility rating block
	•	After the SPR block, present each experimental sentence again (you can choose whether to include fillers here; I recommend including only non-filler items where is_filler == 0).
	•	For each item:
	•	Show the full stimulus_text.
	•	Ask the participant to rate how factually plausible the sentence seems about the Talren족.
	•	Use a 5-point Likert scale:
	•	1 = “very clearly false”
	•	2
	•	3 = “uncertain”
	•	4
	•	5 = “very clearly true”
	•	Use a survey-likert or html-button-response style, whichever is more convenient, but ensure the rating is saved as a numeric value in the data.
	•	Trial data should retain: item_id, emotion, plausibility, is_filler, and rating.
	6.	Free recall block
	•	Present a survey-text style trial where the participant is asked to freely recall and summarize everything they remember about the Talren족.
	•	The instruction should say something like:
	•	“Please write down as much as you can remember about the Talren족 based on the sentences you have read. There is no time limit.”
	•	Save the response as free_recall_text field in the data.
	7.	Manipulation check block
	•	Present a few short questions checking whether the negative (“hate-like”) expressions were perceived as more negative than neutral ones.
	•	For example, show some of the hate and neutral modifiers as single words/short phrases and ask for a negativity rating from 1 to 7.
	•	Store these as separate trials with fields like:
	•	mc_type = "modifier_negativity"
	•	modifier_text
	•	rating.
	8.	Debriefing screen
	•	Explain that “Talren족” is fictional and that the negative descriptions were part of the experimental manipulation.
	•	Provide contact information.
	•	A final “End” or “Submit” button.

⸻

4. Data structure requirements

For every experimental SPR trial, the saved data should include:
	•	participant_id (generated randomly at start, e.g. from 100000–999999)
	•	list_id (1–4)
	•	item_id
	•	base
	•	emotion
	•	plausibility
	•	version
	•	is_filler
	•	sentence_text (full sentence)
	•	regions (array or stringified representation of region texts)
	•	region_rts (array or stringified representation of RTs for each region)
	•	trial_index or something similar

For plausibility rating trials, save:
	•	participant_id
	•	list_id
	•	item_id
	•	emotion
	•	plausibility
	•	is_filler
	•	rating

For free recall:
	•	participant_id
	•	list_id
	•	free_recall_text

For manipulation check:
	•	participant_id
	•	mc_type
	•	modifier_text
	•	rating

It is fine if arrays (regions and RTs) are stored as JSON strings; I will parse them later in R or Python.

⸻

5. Implementation details and style
	•	Use jsPsych 7.x (or the latest stable jsPsych) and reference it via CDN in index.html.
	•	Implement a custom plugin for SPR, e.g. jspsych-spr.js. Show the full plugin code.
	•	The plugin should:
	•	Accept parameters:
	•	sentence
	•	item_id
	•	base
	•	emotion
	•	plausibility
	•	version
	•	is_filler
	•	Split the sentence into regions (by spaces is okay).
	•	Display each region in sequence, one at a time.
	•	Wait for SPACE keypress to advance.
	•	Record RT for each region.
	•	At the end, send back all meta-data + arrays of regions and RTs in trial data.
	•	Use clean, readable, commented code.
	•	Use a simple CSS style (style.css) to center content and use a readable font (you can suggest using Noto Sans KR).

⸻

6. Data saving

Please implement at least two options for saving data:
	1.	Client-side CSV download at the end of the experiment
	•	Show a “Download data” button that triggers jsPsych.data.get().localSave('csv', 'talren_spr_data.csv').
	2.	Template for server-side saving
	•	Provide example code for:
	•	A simple Node.js + Express endpoint /save-data that receives a POST with the full data as JSON and writes it to a file.
	•	A minimal fetch() call in the jsPsych code that sends the data to that endpoint when the experiment ends.
	•	The server-side does not need to be fully production-ready; it is enough to show a working example that I can adapt.

You do NOT need to actually host the server; just give complete example code for server.js and the client-side fetch call.

⸻

7. What to output

Please output:
	1.	The complete index.html file content (with script and link tags).
	2.	The complete experiment.js file that:
	•	Handles URL parameter parsing for list,
	•	Sets participant_id,
	•	Loads the appropriate list JSON,
	•	Defines the jsPsych timeline and calls jsPsych.run(timeline).
	3.	The complete custom plugin file jspsych-spr.js.
	4.	A minimal style.css.
	5.	Example JSON structure for list1.json (so I can convert my List1.csv to that format).
	6.	Example server code (server.js) using Node.js + Express for saving data.
	7.	Any other supporting code you feel is necessary for a working experiment.

Make sure the code is coherent and directly runnable after I place the files in a folder and serve them with a simple static server (and an Express server for saving, if I choose to use it).
Comment the code where appropriate so that I can easily adapt texts and add my real background passage in Korean.

⸻

Now, based on all of the above, generate the full project code.

⸻