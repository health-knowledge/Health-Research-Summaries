#!/usr/bin/env python3
"""
Markdown File Concatenator

This script recursively searches for .md files in specified directories
and concatenates them into a single output file.
"""

import os
import argparse
from datetime import datetime


def find_md_files(directory):
    """
    Recursively find all .md files in the given directory.
    
    Args:
        directory (str): The directory to search in
        
    Returns:
        list: List of paths to all found .md files
    """
    md_files = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                md_files.append(os.path.join(root, file))
    
    return md_files


def concatenate_md_files(file_paths, output_file, add_headers=True):
    """
    Concatenate multiple markdown files into a single file.
    
    Args:
        file_paths (list): List of file paths to concatenate
        output_file (str): Path to the output file
        add_headers (bool): Whether to add file headers to separate content
    """
    with open(output_file, 'w', encoding='utf-8') as outfile:
        # Add a header to the file
        outfile.write(f"# Concatenated Markdown Files\n\n")
        outfile.write(f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        outfile.write(f"This file contains content from {len(file_paths)} markdown files.\n\n")
        outfile.write("---\n\n")
        
        # Sort files to ensure consistent ordering
        file_paths.sort()
        
        # Process each file
        for file_path in file_paths:
            try:
                with open(file_path, 'r', encoding='utf-8') as infile:
                    # Add a header for this file if requested
                    if add_headers:
                        rel_path = os.path.relpath(file_path)
                        outfile.write(f"\n\n## File: {rel_path}\n\n")
                    
                    # Read and write the content
                    content = infile.read()
                    outfile.write(content)
                    
                    # Add a separator between files
                    outfile.write("\n\n---\n\n")
                    
            except Exception as e:
                outfile.write(f"\n\nError reading file {file_path}: {str(e)}\n\n")
                outfile.write("---\n\n")
    
    print(f"Successfully concatenated {len(file_paths)} files into {output_file}")


def main():
    # Set up command line arguments
    parser = argparse.ArgumentParser(description='Concatenate markdown files from directories.')
    parser.add_argument('directories', metavar='DIR', type=str, nargs='+',
                      help='directories to search for markdown files')
    parser.add_argument('-o', '--output', type=str, default='concatenated_markdown.md',
                      help='output file path (default: concatenated_markdown.md)')
    parser.add_argument('--no-headers', action='store_true',
                      help='do not add file headers to the concatenated content')
    
    args = parser.parse_args()
    
    # Find all markdown files
    md_files = []
    for directory in args.directories:
        if os.path.isdir(directory):
            md_files.extend(find_md_files(directory))
        else:
            print(f"Warning: {directory} is not a valid directory, skipping...")
    
    if not md_files:
        print("No markdown files found in the specified directories.")
        return
    
    print(f"Found {len(md_files)} markdown files.")
    
    # Concatenate the files
    concatenate_md_files(md_files, args.output, not args.no_headers)


if __name__ == "__main__":
    main()