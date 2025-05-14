import re
import os

def extract_verses(root_text_file):
    """Extract verses from the root text file."""
    with open(root_text_file, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Pattern to match verses ending with || number ||
    verse_pattern = re.compile(r'(.*?\|\| (\d+) \|\|)', re.DOTALL)
    verses = []
    
    # Find all verses in the content
    last_end = 0
    for match in verse_pattern.finditer(content):
        verse_text = match.group(1).strip()
        verse_number = int(match.group(2))
        
        # Check if there's introductory text before the first verse
        if verse_number == 1 and last_end == 0 and match.start() > 0:
            intro_text = content[:match.start()].strip()
            if intro_text:
                verses.append((0, intro_text))
        
        verses.append((verse_number, verse_text))
        last_end = match.end()
    
    return verses

def extract_commentaries(commentary_file):
    """Extract commentaries from the commentary file."""
    with open(commentary_file, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Pattern to match commentary sections starting with a number
    # This pattern looks for a number at the beginning of a line
    commentary_pattern = re.compile(r'^\s*(\d+)\s*\n(.*?)(?=^\s*\d+\s*$|\Z)', re.MULTILINE | re.DOTALL)
    commentaries = {}
    
    # Find all commentaries in the content
    for match in commentary_pattern.finditer(content):
        verse_number = int(match.group(1))
        commentary_text = match.group(2).strip()
        commentaries[verse_number] = commentary_text
    
    return commentaries

def save_to_files(verses, commentaries, output_dir='output'):
    """Save verses and commentaries to separate files."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for verse_number, verse_text in verses:
        # Skip intro text (verse_number 0) if not needed
        if verse_number == 0:
            continue
            
        # Save verse file
        verse_filename = f"ht_1.5.{verse_number}_mula.txt"
        verse_path = os.path.join(output_dir, verse_filename)
        with open(verse_path, 'w', encoding='utf-8') as file:
            file.write(verse_text)
        print(f"Saved verse {verse_number} to {verse_filename}")
        
        # Save commentary file if it exists
        if verse_number in commentaries:
            commentary_filename = f"ht_1.5.{verse_number}_raa.txt"
            commentary_path = os.path.join(output_dir, commentary_filename)
            with open(commentary_path, 'w', encoding='utf-8') as file:
                file.write(commentaries[verse_number])
            print(f"Saved commentary {verse_number} to {commentary_filename}")
        else:
            print(f"No commentary found for verse {verse_number}")

def main(root_text_file, commentary_file, output_dir='output'):
    """Process the root text and commentary files."""
    verses = extract_verses(root_text_file)
    commentaries = extract_commentaries(commentary_file)
    save_to_files(verses, commentaries, output_dir)

if __name__ == "__main__":
    # Replace with your actual file paths
    root_text_file = "ht_1.5"
    commentary_file = "ht_1.5_raa"
    output_dir = "output"
    
    main(root_text_file, commentary_file, output_dir)
