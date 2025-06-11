import re
import os

def extract_verse_sections(input_file, output_dir="extracted_verses"):
    """
    Extract verse sections from a Sanskrit root text file.
    Each verse ends with '|| X.Y ||' where X.Y is the chapter.verse number.
    
    Args:
        input_file (str): Path to the input file containing verses
        output_dir (str): Directory to save extracted files (default: "extracted_verses")
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
    
    # Pattern to match verses ending with || X.Y ||
    # This captures everything from start of verse to the verse number marker
    verse_pattern = r'(.*?)\|\| (\d+\.\d+) \|\|'
    
    # Find all verses
    matches = re.findall(verse_pattern, content, re.DOTALL)
    
    if not matches:
        print("No verses found. Please check the input file format.")
        return
    
    extracted_count = 0
    
    for verse_text, verse_number in matches:
        # Clean up the verse text
        verse_text = verse_text.strip()
        
        # Remove any leading blank lines
        verse_text = verse_text.lstrip('\n')
        
        # Skip empty verses
        if not verse_text.strip():
            print(f"Warning: Verse {verse_number} is empty, skipping...")
            continue
        
        # Add the verse number marker back to the end
        full_verse = verse_text + f" || {verse_number} ||"
        
        # Create filename
        filename = f"bca_{verse_number}.txt"
        filepath = os.path.join(output_dir, filename)
        
        # Write verse to file
        try:
            with open(filepath, 'w', encoding='utf-8') as output_file:
                output_file.write(full_verse)
            extracted_count += 1
            print(f"Extracted verse {verse_number} to {filename}")
        except Exception as e:
            print(f"Error writing file {filename}: {e}")
    
    print(f"\nExtraction complete! {extracted_count} verses extracted to '{output_dir}' directory.")

def extract_verses_alternative_method(input_file, output_dir="extracted_verses"):
    """
    Alternative extraction method that splits the text by verse markers
    and reconstructs each verse. Use this if the primary method doesn't work well.
    """
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            content = file.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return
    
    # Split by verse number markers
    parts = re.split(r'\|\| (\d+\.\d+) \|\|', content)
    
    # Remove empty first part if it exists
    if parts[0].strip() == '':
        parts = parts[1:]
    
    extracted_count = 0
    current_verse = ""
    current_number = ""
    
    for i, part in enumerate(parts):
        if re.match(r'\d+\.\d+$', part.strip()):
            # This is a verse number
            if current_verse and current_number:
                # Save the previous verse
                verse_text = current_verse.strip()
                if verse_text:
                    full_verse = verse_text + f" || {current_number} ||"
                    filename = f"bca_{current_number}.txt"
                    filepath = os.path.join(output_dir, filename)
                    
                    try:
                        with open(filepath, 'w', encoding='utf-8') as output_file:
                            output_file.write(full_verse)
                        extracted_count += 1
                        print(f"Extracted verse {current_number} to {filename}")
                    except Exception as e:
                        print(f"Error writing file {filename}: {e}")
            
            current_number = part.strip()
            current_verse = ""
        else:
            # This is verse content
            if i > 0:  # Skip first part if it's before any verse number
                current_verse = part
    
    # Handle the last verse if it exists
    if current_verse and current_number:
        verse_text = current_verse.strip()
        if verse_text:
            full_verse = verse_text + f" || {current_number} ||"
            filename = f"bca_{current_number}.txt"
            filepath = os.path.join(output_dir, filename)
            
            try:
                with open(filepath, 'w', encoding='utf-8') as output_file:
                    output_file.write(full_verse)
                extracted_count += 1
                print(f"Extracted verse {current_number} to {filename}")
            except Exception as e:
                print(f"Error writing file {filename}: {e}")
    
    print(f"\nExtraction complete! {extracted_count} verses extracted to '{output_dir}' directory.")

def main():
    """
    Main function to run the verse extractor.
    Modify the input_file variable to point to your Sanskrit verse file.
    """
    
    # MODIFY THIS PATH to point to your input file
    input_file = "bca_5.txt"  # Change this to your file path
    
    # Optional: specify output directory
    output_dir = "extracted_verses"
    
    print("Sanskrit Verse Extractor")
    print("-" * 40)
    print(f"Input file: {input_file}")
    print(f"Output directory: {output_dir}")
    print()
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Input file '{input_file}' not found.")
        print("Please update the 'input_file' variable in the script with the correct path.")
        return
    
    # Try primary extraction method
    print("Using primary extraction method...")
    extract_verse_sections(input_file, output_dir)
    
    # Uncomment the line below if you want to try the alternative method
    # print("\nTrying alternative extraction method...")
    # extract_verses_alternative_method(input_file, output_dir)

if __name__ == "__main__":
    main()
