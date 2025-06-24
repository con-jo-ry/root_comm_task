#!/usr/bin/env python3
"""
Sanskrit Root Text Extractor
Extracts root verses (marked with >) from combined Sanskrit text and commentary files.
Each section is separated by ---, and each root verse consists of two lines.
Saves each root verse as a separate file with naming convention: nasa_N_root
"""

import re
import os
from pathlib import Path

def extract_root_verses(input_file_path, output_directory="extracted_texts"):
    """
    Extract root verses from a Sanskrit text file and save them individually.
    
    Args:
        input_file_path (str): Path to the input file containing root text and commentary
        output_directory (str): Directory to save extracted root verses
    """
    
    # Create output directory if it doesn't exist
    Path(output_directory).mkdir(exist_ok=True)
    
    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"Error: File '{input_file_path}' not found.")
        return
    except UnicodeDecodeError:
        print(f"Error: Could not decode '{input_file_path}'. Trying with different encoding...")
        try:
            with open(input_file_path, 'r', encoding='latin-1') as file:
                content = file.read()
        except Exception as e:
            print(f"Error reading file: {e}")
            return
    
    # Split content by --- to get individual sections
    sections = content.split('---')
    
    verse_counter = 1
    
    for section in sections:
        # Only strip leading/trailing whitespace from the entire section
        section = section.strip()
        
        # Skip empty sections
        if not section:
            continue
        
        # Split section into lines, preserving original formatting
        lines = section.split('\n')
        
        # Find lines that start with >
        root_lines = []
        for line in lines:
            if line.startswith('>'):
                # Remove the > marker but preserve indentation after >
                root_line = line[1:]
                if root_line.strip():  # Only add non-empty lines (after stripping for check)
                    root_lines.append(root_line)
        
        # Each root verse should have exactly 2 lines
        if len(root_lines) == 2:
            save_root_verse(root_lines, verse_counter, output_directory)
            verse_counter += 1
        elif len(root_lines) > 0:
            # Handle cases where there might be a different number of lines
            print(f"Warning: Found {len(root_lines)} root lines in verse {verse_counter}, expected 2")
            save_root_verse(root_lines, verse_counter, output_directory)
            verse_counter += 1
    
    print(f"Extraction complete! Found {verse_counter - 1} root verses.")
    print(f"Files saved in '{output_directory}' directory.")

def save_root_verse(verse_lines, verse_number, output_directory):
    """
    Save a root verse to a file.
    
    Args:
        verse_lines (list): Lines of the root verse
        verse_number (int): Verse number for filename
        output_directory (str): Directory to save the file
    """
    filename = f"medū_{verse_number}_root.txt"
    filepath = os.path.join(output_directory, filename)
    
    # Join lines with newlines, only strip from beginning and end
    verse_content = '\n'.join(verse_lines).strip()
    
    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(verse_content)
        print(f"Saved: {filename}")
    except Exception as e:
        print(f"Error saving {filename}: {e}")

def preview_extraction(input_file_path, num_verses=3):
    """
    Preview the first few verses that would be extracted.
    
    Args:
        input_file_path (str): Path to the input file
        num_verses (int): Number of verses to preview
    """
    print("=== PREVIEW MODE ===")
    
    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return
    
    # Split content by --- to get individual sections
    sections = content.split('---')
    
    verse_counter = 1
    
    for section in sections:
        # Only strip leading/trailing whitespace from the entire section
        section = section.strip()
        
        if not section:
            continue
        
        # Split section into lines, preserving original formatting
        lines = section.split('\n')
        
        # Find lines that start with >
        root_lines = []
        for line in lines:
            if line.startswith('>'):
                # Remove the > marker but preserve indentation after >
                root_line = line[1:]
                if root_line.strip():  # Only add non-empty lines (after stripping for check)
                    root_lines.append(root_line)
        
        if root_lines:
            print(f"\nVerse {verse_counter}:")
            print('-' * 50)
            for line in root_lines:
                print(line)
            
            verse_counter += 1
            
            if verse_counter > num_verses:
                break

def extract_commentary(input_file_path, output_directory="extracted_texts"):
    """
    Extract commentary (non-root text) for each verse and save separately.
    Saves to nasa_X_vi.txt format where X is the verse number.
    
    Args:
        input_file_path (str): Path to the input file
        output_directory (str): Directory to save commentary files
    """
    
    Path(output_directory).mkdir(exist_ok=True)
    
    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return
    
    sections = content.split('---')
    verse_counter = 1
    
    for section in sections:
        # Only strip leading/trailing whitespace from the entire section
        section = section.strip()
        
        if not section:
            continue
        
        # Split section into lines, preserving original formatting
        lines = section.split('\n')
        
        # Extract commentary (lines that don't start with >)
        commentary_lines = []
        for line in lines:
            if line and not line.startswith('>'):
                commentary_lines.append(line)
        
        if commentary_lines:
            filename = f"medū_{verse_counter}_vi.txt"
            filepath = os.path.join(output_directory, filename)
            
            # Join lines preserving internal formatting, only strip beginning/end
            commentary_content = '\n'.join(commentary_lines).strip()
            
            try:
                with open(filepath, 'w', encoding='utf-8') as file:
                    file.write(commentary_content)
                print(f"Saved commentary: {filename}")
            except Exception as e:
                print(f"Error saving {filename}: {e}")
        
        verse_counter += 1
    
    print(f"Commentary extraction complete! Found {verse_counter - 1} commentaries.")

# Example usage
if __name__ == "__main__":
    # Configuration
    input_file = "meghadūta_shortened.txt"  # Change this to your input file name
    output_dir = "extracted_texts"  # Same folder for both root verses and commentaries
    
    print("Sanskrit Root Text and Commentary Extractor")
    print("=" * 50)
    
    # First, preview what will be extracted
    print("\nPreviewing first 3 verses...")
    preview_extraction(input_file, 3)
    
    # Ask user what they want to do
    print("\n" + "=" * 50)
    print("Options:")
    print("1. Extract root verses only (nasa_X_root.txt)")
    print("2. Extract commentaries only (nasa_X_vi.txt)") 
    print("3. Extract both root verses and commentaries to same folder")
    print("4. Cancel")
    
    choice = input("Enter your choice (1-4): ").strip()
    
    if choice == "1":
        extract_root_verses(input_file, output_dir)
    elif choice == "2":
        extract_commentary(input_file, output_dir)
    elif choice == "3":
        print("\nExtracting root verses...")
        extract_root_verses(input_file, output_dir)
        print("\nExtracting commentaries...")
        extract_commentary(input_file, output_dir)
        print(f"\nAll files saved in '{output_dir}' directory!")
    elif choice == "4":
        print("Extraction cancelled.")
    else:
        print("Invalid choice. Extraction cancelled.")
