import pandas as pd
import os
import yaml

def update_markdown_files(spreadsheet_path, markdown_dir):
    # Read the spreadsheet
    df = pd.read_csv(spreadsheet_path)  # Use pd.read_csv() if it's a CSV

    # Convert DataFrame to a list of dictionaries
    data = df.to_dict(orient='records')

    for entry in data:
        filename = entry['filename']  # Assuming one column is 'filename'
        if not filename.endswith('.md'):
            filename += '.md'
        
        markdown_file_path = os.path.join(markdown_dir, filename)

        # Check if the markdown file exists
        if not os.path.exists(markdown_file_path):
            print(f"File {markdown_file_path} does not exist. Skipping.")
            continue

        # Read the existing Markdown file
        with open(markdown_file_path, 'r') as file:
            content = file.read()

        # Prepare the YAML front matter
        yaml_content = yaml.dump(entry, default_flow_style=False)
        yaml_header = f"---\n{yaml_content}---\n"

        # Check for existing front matter
        if content.startswith('---'):
            # Replace existing YAML front matter
            end_of_front_matter = content.find('---', 3) + 3  # Find the second '---'
            if end_of_front_matter > 3:  # Ensure a valid second separator exists
                new_content = yaml_header + content[end_of_front_matter:]
            else:
                new_content = yaml_header + content
        else:
            # No existing front matter
            new_content = yaml_header + content

        # Write the updated content back to the Markdown file
        with open(markdown_file_path, 'w') as file:
            file.write(new_content)

        print(f"Updated {markdown_file_path} with new YAML front matter.")

# Usage
spreadsheet_path = '/Users/jayfriesen/Downloads/crew.csv'  # Update with your spreadsheet path
markdown_dir = '/Users/jayfriesen/Downloads/_crews'  # Update with your markdown files directory

update_markdown_files(spreadsheet_path, markdown_dir)