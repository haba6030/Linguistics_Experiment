import pandas as pd
import json
import numpy as np

# Convert each list CSV to JSON format for jsPsych
for list_num in range(1, 5):
    input_file = f"List{list_num}.csv"
    output_file = f"stimuli/list{list_num}.json"

    # Read CSV
    df = pd.read_csv(input_file)

    # Replace NaN values with empty strings or appropriate defaults
    df = df.fillna('')

    # Convert to list of dictionaries
    stimuli = df.to_dict('records')

    # Clean up the data: replace any remaining NaN/None with empty strings
    for item in stimuli:
        for key, value in item.items():
            if pd.isna(value) or value is None or (isinstance(value, float) and np.isnan(value)):
                item[key] = ''

    # Save as JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(stimuli, f, ensure_ascii=False, indent=2)

    print(f"Converted {input_file} to {output_file}")

print("\nAll CSV files converted to JSON successfully!")
