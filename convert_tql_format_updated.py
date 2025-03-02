#!/usr/bin/env python3
"""
Script to convert data from query_tql_pairs.jsonl format to the format used in tql_data.jsonl,
suitable for finetuning ChatGPT.
"""
import json
import re

def clean_json_line(line):
    """
    Clean a JSON line by removing any leading non-JSON characters.
    """
    # Find the first occurrence of '{' which should be the start of the JSON object
    start_idx = line.find('{')
    if start_idx > 0:
        # There are characters before the JSON object starts
        print(f"Cleaning line: removed {start_idx} characters from the beginning")
        return line[start_idx:]
    return line

def convert_query_tql_to_finetune_format():
    """
    Convert data from query_tql_pairs.jsonl format to the format used in tql_data.jsonl,
    suitable for finetuning ChatGPT.
    """
    # Path to input and output files
    input_path = 'query_tql_pairs.jsonl'
    output_path = 'tql_data_converted.jsonl'
    
    converted_data = []
    success_count = 0
    error_count = 0
    
    print(f"Starting conversion from {input_path} to {output_path}")
    
    # Read the input file
    with open(input_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            if not line.strip():  # Skip empty lines
                continue
                
            try:
                # Clean the line before parsing JSON
                cleaned_line = clean_json_line(line.strip())
                
                # Parse the JSON object
                entry = json.loads(cleaned_line)
                
                # Create the new format matching tql_data.jsonl but using query as user content
                new_entry = {
                    "messages": [
                        {"role": "system", "content": "You are a helpful assistant, returning correct TQL content."},
                        {"role": "user", "content": entry["query"]},
                        {"role": "assistant", "content": entry["original_tql"]}
                    ]
                }
                
                # Add to our list of converted entries
                converted_data.append(new_entry)
                success_count += 1
                
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON at line {line_num}: {e}")
                print(f"Problematic line: {line[:50]}...")  # Show first 50 chars
                error_count += 1
                continue
            except KeyError as e:
                print(f"Missing key in JSON at line {line_num}: {e}")
                error_count += 1
                continue
    
    # Write to the output file
    with open(output_path, 'w', encoding='utf-8') as f:
        for entry in converted_data:
            f.write(json.dumps(entry) + '\n')
    
    print(f"Conversion complete:")
    print(f"- Successfully converted: {success_count} entries")
    print(f"- Errors encountered: {error_count} entries")
    print(f"- Total entries written to {output_path}: {len(converted_data)}")
    
    return output_path

if __name__ == "__main__":
    output_file = convert_query_tql_to_finetune_format()
    print(f"Converted data saved to: {output_file}")
