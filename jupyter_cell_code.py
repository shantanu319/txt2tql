# Copy this code into a new Jupyter notebook cell

import json

def convert_query_tql_to_finetune_format():
    """
    Convert data from query_tql_pairs.jsonl format to the format used in tql_data.jsonl,
    suitable for finetuning ChatGPT.
    
    This function:
    1. Reads the content from query_tql_pairs.jsonl
    2. Reformats each entry to match the structure in tql_data.jsonl
    3. Writes the result to a new file: tql_data_converted.jsonl
    
    Returns:
        The path to the output file
    """
    # Path to input and output files
    input_path = 'query_tql_pairs.jsonl'
    output_path = 'tql_data_converted.jsonl'
    
    converted_data = []
    
    # Read the input file
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():  # Skip empty lines
                try:
                    # Parse the JSON object
                    entry = json.loads(line)
                    
                    # Create the new format matching tql_data.jsonl
                    new_entry = {
                        "messages": [
                            {"role": "system", "content": "You are a helpful assistant, returning correct TQL content."},
                            {"role": "user", "content": "Please share the TQL content."},
                            {"role": "assistant", "content": entry["original_tql"]}
                        ]
                    }
                    
                    # Add to our list of converted entries
                    converted_data.append(new_entry)
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON: {e}")
                    continue
    
    # Write to the output file
    with open(output_path, 'w', encoding='utf-8') as f:
        for entry in converted_data:
            f.write(json.dumps(entry) + '\n')
    
    print(f"Conversion complete. {len(converted_data)} entries written to {output_path}")
    return output_path

# Execute the function
output_file = convert_query_tql_to_finetune_format()
print(f"Converted data saved to: {output_file}")
