#!/usr/bin/env python3
"""
Script to count root-commentary pairs from a dataset of Buddhist texts.
Uses a root-first approach: for each root file, find matching commentaries.
"""

import os
import argparse
from collections import defaultdict

def count_pairs_root_first(directory_path='.'):
    """
    Count root-commentary pairs starting from root files.
    
    Args:
        directory_path: Path to directory containing the files
    
    Returns:
        Dictionary with statistics about the pairs
    """
    try:
        files = os.listdir(directory_path)
    except FileNotFoundError:
        print(f"Directory '{directory_path}' not found.")
        return None
    
    # Get all root files
    root_files = [f for f in files if f.endswith('_root')]
    print(f"Found {len(root_files)} root files")
    
    total_pairs = 0
    root_only_count = 0
    single_pair_count = 0
    multiple_pair_count = 0
    
    results = []
    
    for root_file in root_files:
        # Extract prefix (everything before '_root')
        prefix = root_file[:-5]  # Remove '_root'
        
        # Find all files with same prefix that are commentaries
        commentaries = [f for f in files if 
                       f.startswith(prefix + '_') and 
                       not f.endswith('_root')]
        
        num_commentaries = len(commentaries)
        
        if num_commentaries == 0:
            root_only_count += 1
            pair_type = 'root-only'
            pairs_count = 0
        elif num_commentaries == 1:
            single_pair_count += 1
            total_pairs += 1
            pair_type = 'single-pair'
            pairs_count = 1
        else:
            multiple_pair_count += 1
            total_pairs += num_commentaries
            pair_type = 'multiple-pairs'
            pairs_count = num_commentaries
        
        results.append({
            'root': root_file,
            'commentaries': commentaries,
            'pairs': pairs_count,
            'type': pair_type
        })
    
    return {
        'total_root_files': len(root_files),
        'root_only_count': root_only_count,
        'single_pair_count': single_pair_count,
        'multiple_pair_count': multiple_pair_count,
        'total_pairs': total_pairs,
        'results': results
    }

def main():
    """Main function to run the pair counting analysis."""
    parser = argparse.ArgumentParser(description='Count root-commentary pairs in dataset')
    parser.add_argument('-d', '--directory', default='.', 
                       help='Directory containing the files (default: current directory)')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Show detailed breakdown and examples')
    parser.add_argument('--list-files', action='store_true',
                       help='List all files found in directory')
    
    args = parser.parse_args()
    
    if args.list_files:
        try:
            files = os.listdir(args.directory)
            print(f"All files in {args.directory}:")
            for i, f in enumerate(sorted(files), 1):
                print(f"{i:3d}. {f}")
            print(f"\nTotal files: {len(files)}")
        except FileNotFoundError:
            print(f"Directory '{args.directory}' not found.")
        return
    
    results = count_pairs_root_first(args.directory)
    
    if results is None:
        return
    
    print("Root-Commentary Pair Analysis (Root-First Approach)")
    print("=" * 55)
    print(f"Total root files found: {results['total_root_files']}")
    print(f"Root files with no commentary: {results['root_only_count']}")
    print(f"Root files with exactly one commentary: {results['single_pair_count']}")
    print(f"Root files with multiple commentaries: {results['multiple_pair_count']}")
    print()
    print(f"TOTAL ROOT-COMMENTARY PAIRS: {results['total_pairs']}")
    
    if args.verbose:
        print("\n" + "=" * 55)
        print("EXAMPLES")
        print("=" * 55)
        
        # Show root-only examples
        root_only = [r for r in results['results'] if r['type'] == 'root-only']
        if root_only:
            print(f"\nRoot-only files ({len(root_only)} total):")
            for r in root_only[:5]:
                print(f"  {r['root']}")
            if len(root_only) > 5:
                print(f"  ... and {len(root_only) - 5} more")
        
        # Show single-pair examples
        single_pairs = [r for r in results['results'] if r['type'] == 'single-pair']
        if single_pairs:
            print(f"\nSingle-pair examples ({len(single_pairs)} total):")
            for r in single_pairs[:5]:
                print(f"  {r['root']} -> {r['commentaries'][0]}")
            if len(single_pairs) > 5:
                print(f"  ... and {len(single_pairs) - 5} more")
        
        # Show multiple-pair examples
        multiple_pairs = [r for r in results['results'] if r['type'] == 'multiple-pairs']
        if multiple_pairs:
            print(f"\nMultiple-pair examples ({len(multiple_pairs)} total):")
            for r in multiple_pairs[:5]:
                comms = ', '.join(r['commentaries'])
                print(f"  {r['root']} -> {comms} ({r['pairs']} pairs)")
            if len(multiple_pairs) > 5:
                print(f"  ... and {len(multiple_pairs) - 5} more")
        
        # Breakdown by text siglum
        print(f"\n{'='*55}")
        print("BREAKDOWN BY TEXT SIGLUM")
        print("=" * 55)
        
        by_text = defaultdict(lambda: {'roots': 0, 'pairs': 0})
        for r in results['results']:
            text_siglum = r['root'].split('_')[0]
            by_text[text_siglum]['roots'] += 1
            by_text[text_siglum]['pairs'] += r['pairs']
        
        for text_siglum in sorted(by_text.keys()):
            stats = by_text[text_siglum]
            print(f"{text_siglum:6s}: {stats['roots']:3d} root files, {stats['pairs']:3d} pairs")

if __name__ == "__main__":
    main()
