import re
import os

def extract_commentary_sections(input_file, output_dir="extracted_commentaries"):
    """
    Extract commentary sections from a Sanskrit text file.
    Each section starts with '--- X.Y' where X.Y is the chapter.verse number.
    
    Args:
        input_file (str): Path to the input file containing commentaries
        output_dir (str): Directory to save extracted files (default: "extracted_commentaries")
    """
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        return
    except UnicodeDecodeError:
        print(f"Error: Could not decode file '{input_file}'. Trying with different encoding...")
        try:
            with open(input_file, 'r', encoding='latin1') as file:
                content = file.read()
        except:
            print(f"Error: Could not read file '{input_file}' with any encoding.")
            return
    
    # Split content by section markers
    # Pattern matches lines starting with "--- " followed by chapter.verse numbers
    sections = re.split(r'^--- (\d+\.\d+)$', content, flags=re.MULTILINE)
    
    # Remove the first element (content before first section, if any)
    if sections[0].strip() == '':
        sections = sections[1:]
    
    # Process sections in pairs (section_number, section_content)
    extracted_count = 0
    for i in range(0, len(sections) - 1, 2):
        section_number = sections[i]
        section_content = sections[i + 1]
        
        # Remove leading blank lines from content
        section_content = section_content.lstrip('\n')
        # Remove trailing whitespace but keep internal formatting
        section_content = section_content.rstrip()
        
        # Skip empty sections
        if not section_content.strip():
            print(f"Warning: Section {section_number} is empty, skipping...")
            continue
        
        # Create filename
        filename = f"bca_p_{section_number}.txt"
        filepath = os.path.join(output_dir, filename)
        
        # Write section to file
        try:
            with open(filepath, 'w', encoding='utf-8') as output_file:
                output_file.write(section_content)
            extracted_count += 1
            print(f"Extracted section {section_number} to {filename}")
        except Exception as e:
            print(f"Error writing file {filename}: {e}")
    
    print(f"\nExtraction complete! {extracted_count} sections extracted to '{output_dir}' directory.")

def main():
    """
    Main function to run the commentary extractor.
    Modify the input_file variable to point to your Sanskrit commentary file.
    """
    
    # MODIFY THIS PATH to point to your input file
    input_file = "bca_5_comm"  # Change this to your file path
    
    # Optional: specify output directory
    output_dir = "extracted_commentaries"
    
    print("Sanskrit Commentary Extractor")
    print("-" * 40)
    print(f"Input file: {input_file}")
    print(f"Output directory: {output_dir}")
    print()
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Input file '{input_file}' not found.")
        print("Please update the 'input_file' variable in the script with the correct path.")
        return
    
    # Extract sections
    extract_commentary_sections(input_file, output_dir)

if __name__ == "__main__":
    main()
