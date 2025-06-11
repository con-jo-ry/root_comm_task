import re
import os

def extract_root_verses(content, output_dir="extracted_seni"):
    """
    Extract root verses that start with '>' into individual files.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Find all lines that start with '>'
    verse_lines = []
    for line in content.split('\n'):
        if line.strip().startswith('>'):
            verse_lines.append(line.strip()[1:].strip())  # Remove '>' and extra spaces
    
    # Group verses by their ending pattern (SeNi X ||)
    verses_dict = {}
    current_verse = []
    
    for line in verse_lines:
        current_verse.append(line)
        
        # Check if this line ends with a verse number pattern like "|| SeNi 1 ||"
        verse_end_match = re.search(r'\|\| SeNi (\d+) \|\|\s*$', line)
        if verse_end_match:
            verse_num = verse_end_match.group(1)
            verses_dict[verse_num] = '\n'.join(current_verse)
            current_verse = []
    
    # Write each verse to a file
    extracted_count = 0
    for verse_num, verse_text in verses_dict.items():
        filename = f"seni_{verse_num}_root.txt"
        filepath = os.path.join(output_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(verse_text)
            extracted_count += 1
            print(f"Extracted root verse {verse_num} to {filename}")
        except Exception as e:
            print(f"Error writing file {filename}: {e}")
    
    return extracted_count

def extract_commentary_sections(content, output_dir="extracted_seni"):
    """
    Extract commentary sections separated by '--- [number]' into individual files.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Split content by section markers (--- followed by number)
    sections = re.split(r'^--- (\d+)$', content, flags=re.MULTILINE)
    
    # Remove the first element (content before first section, if any)
    if sections[0].strip() == '':
        sections = sections[1:]
    
    extracted_count = 0
    
    # Process sections in pairs (section_number, section_content)
    for i in range(0, len(sections) - 1, 2):
        section_number = sections[i]
        section_content = sections[i + 1]
        
        # Remove root verses (lines starting with '>') from commentary
        cleaned_lines = []
        for line in section_content.split('\n'):
            if not line.strip().startswith('>'):
                cleaned_lines.append(line)
        
        section_content = '\n'.join(cleaned_lines)
        
        # Remove leading blank lines from content
        section_content = section_content.lstrip('\n')
        # Remove trailing whitespace but keep internal formatting
        section_content = section_content.rstrip()
        
        # Skip empty sections
        if not section_content.strip():
            print(f"Warning: Commentary section {section_number} is empty, skipping...")
            continue
        
        # Create filename
        filename = f"seni_{section_number}_p.txt"
        filepath = os.path.join(output_dir, filename)
        
        # Write section to file
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(section_content)
            extracted_count += 1
            print(f"Extracted commentary {section_number} to {filename}")
        except Exception as e:
            print(f"Error writing file {filename}: {e}")
    
    return extracted_count

def extract_seni_texts(input_file, output_dir="extracted_seni"):
    """
    Extract both root verses and commentary from Sekanirdeśa text.
    
    Args:
        input_file (str): Path to the input file
        output_dir (str): Directory to save extracted files
    """
    
    print("Sekanirdeśa Text and Commentary Extractor")
    print("-" * 50)
    print(f"Input file: {input_file}")
    print(f"Output directory: {output_dir}")
    print()
    
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
    
    # Extract root verses
    print("Extracting root verses...")
    root_count = extract_root_verses(content, output_dir)
    
    print()
    
    # Extract commentary sections
    print("Extracting commentary sections...")
    commentary_count = extract_commentary_sections(content, output_dir)
    
    print()
    print(f"Extraction complete!")
    print(f"Root verses extracted: {root_count}")
    print(f"Commentary sections extracted: {commentary_count}")
    print(f"Total files created: {root_count + commentary_count}")
    print(f"Files saved in: {output_dir}")

def main():
    """
    Main function to run the Sekanirdeśa extractor.
    """
    
    # MODIFY THIS PATH to point to your input file
    input_file = "seni"  # Change this to your file path
    
    # Optional: specify output directory
    output_dir = "extracted_seni"
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Input file '{input_file}' not found.")
        print("Please update the 'input_file' variable in the script with the correct path.")
        return
    
    # Extract both root verses and commentary
    extract_seni_texts(input_file, output_dir)

if __name__ == "__main__":
    main()
