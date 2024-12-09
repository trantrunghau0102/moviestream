#!/usr/bin/env python3
import os
import fnmatch
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Optional

class FileConcatenator:
    # Comprehensive list of supported file extensions and their syntax highlighting
    SUPPORTED_EXTENSIONS = {
        # Configuration & Infrastructure
        '.tf': 'hcl',
        '.tfvars': 'hcl',
        '.yaml': 'yaml',
        '.yml': 'yaml',
        '.json': 'json',
        '.xml': 'xml',
        '.toml': 'toml',
        '.ini': 'ini',
        '.conf': 'nginx',
        '.config': 'xml',
        '.env': 'plaintext',
        
        # Web Development
        '.js': 'javascript',
        '.jsx': 'jsx',
        '.ts': 'typescript',
        '.tsx': 'tsx',
        '.html': 'html',
        '.css': 'css',
        '.scss': 'scss',
        '.less': 'less',
        '.vue': 'vue',
        '.svelte': 'svelte',
        
        # Backend Development
        '.py': 'python',
        '.java': 'java',
        '.go': 'go',
        '.rb': 'ruby',
        '.php': 'php',
        '.cs': 'csharp',
        '.cpp': 'cpp',
        '.c': 'c',
        '.rs': 'rust',
        '.scala': 'scala',
        '.kt': 'kotlin',
        '.swift': 'swift',
        
        # Database
        '.sql': 'sql',
        '.prisma': 'prisma',
        '.graphql': 'graphql',
        '.gql': 'graphql',
        
        # Shell & Scripts
        '.sh': 'bash',
        '.bash': 'bash',
        '.zsh': 'bash',
        '.fish': 'fish',
        '.ps1': 'powershell',
        '.bat': 'batch',
        '.cmd': 'batch',
        
        # Documentation
        '.md': 'markdown',
        '.mdx': 'mdx',
        '.txt': 'plaintext',
        '.rst': 'rst',
        
        # Docker & Container
        '.dockerfile': 'dockerfile',
        '.containerfile': 'dockerfile',
        
        # Build & Package
        '.lock': 'yaml',
        '.gradle': 'groovy',
        '.maven': 'xml',
        '.pom': 'xml',
        
        # Other
        '.vim': 'vim',
        '.lua': 'lua'
    }

    def __init__(self, 
                 directory: str,
                 extensions: List[str],
                 output_dir: str = 'export',
                 exclude_dirs: Optional[List[str]] = None,
                 exclude_files: Optional[List[str]] = None):
        self.start_path = os.path.abspath(directory)
        self.folder_name = os.path.basename(directory)
        self.exclude_dirs = exclude_dirs or ['.git', 'node_modules', '__pycache__']
        self.exclude_files = exclude_files or []
        
        # Handle 'all' extension case
        if len(extensions) == 1 and extensions[0].lower() == 'all':
            self.extensions = list(self.SUPPORTED_EXTENSIONS.keys())
        else:
            self.extensions = [ext if ext.startswith('.') else f'.{ext}' for ext in extensions]
        
        # Create output directory
        self.export_dir = os.path.join(os.getcwd(), output_dir)
        os.makedirs(self.export_dir, exist_ok=True)
        
        # Generate output filename
        date_str = datetime.now().strftime("%Y%m%d")
        if len(extensions) == 1 and extensions[0].lower() == 'all':
            extensions_str = 'all'
        else:
            extensions_str = '-'.join(ext.replace('.', '') for ext in self.extensions)
        
        self.output_file = os.path.join(
            self.export_dir,
            f"extract_{self.folder_name}-{extensions_str}_{date_str}.md"
        )
        
        self.files_found = []

    def should_exclude_dir(self, dir_name: str) -> bool:
        """Check if directory should be excluded from scanning"""
        return any(exclude in dir_name for exclude in self.exclude_dirs)

    def should_exclude_file(self, file_name: str) -> bool:
        """Check if file should be excluded based on patterns"""
        if not self.exclude_files:
            return False
        return any(fnmatch.fnmatch(file_name, pattern) for pattern in self.exclude_files)

    def find_files(self):
        """Find all files with specified extensions"""
        print(f"Scanning directory: {self.start_path}")
        if len(self.extensions) > 10:
            print("Looking for all supported file types")
        else:
            print(f"Looking for files with extensions: {', '.join(self.extensions)}")
        
        if self.exclude_files:
            print(f"Excluding files matching: {', '.join(self.exclude_files)}")
        
        for root, dirs, files in os.walk(self.start_path):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if not self.should_exclude_dir(d)]
            
            for file in files:
                if any(file.endswith(ext) for ext in self.extensions):
                    if not self.should_exclude_file(file):
                        full_path = os.path.join(root, file)
                        self.files_found.append(full_path)
                        print(f"Found: {os.path.relpath(full_path, self.start_path)}")
                    else:
                        print(f"Excluded: {os.path.relpath(os.path.join(root, file), self.start_path)}")
        
        self.files_found.sort()
        print(f"\nTotal files found: {len(self.files_found)}")

    def get_file_type(self, file_name: str) -> str:
        """Determine the markdown code block type based on file extension"""
        ext = os.path.splitext(file_name)[1].lower()
        return self.SUPPORTED_EXTENSIONS.get(ext, 'plaintext')

    def concatenate_files(self):
        """Concatenate all found files into a single markdown file"""
        if not self.files_found:
            print("No files found to concatenate!")
            return

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"\nWriting to: {self.output_file}")
        with open(self.output_file, 'w', encoding='utf-8') as outfile:
            # Write header
            outfile.write(f"# Files Concatenation Report\n\n")
            outfile.write(f"Generated on: {timestamp}\n\n")
            outfile.write(f"Source directory: {self.start_path}\n")
            if len(self.extensions) > 10:
                outfile.write("File types: All supported types\n\n")
            else:
                outfile.write(f"File types: {', '.join(self.extensions)}\n\n")
            outfile.write("---\n\n")
            outfile.write("## Table of Contents\n\n")
            
            # Generate table of contents
            for file_path in self.files_found:
                rel_path = os.path.relpath(file_path, self.start_path)
                link_path = rel_path.replace(' ', '-').replace('/', '-')
                outfile.write(f"- [{rel_path}](#{link_path})\n")
            
            outfile.write("\n---\n\n")
            
            # Process each file
            for file_path in self.files_found:
                rel_path = os.path.relpath(file_path, self.start_path)
                abs_path = os.path.abspath(file_path)
                file_type = self.get_file_type(file_path)
                
                # File header with anchor for ToC
                anchor = rel_path.replace(' ', '-').replace('/', '-')
                outfile.write(f"## <a id='{anchor}'></a>File: {rel_path}\n")
                outfile.write(f"**Full Path**: `{abs_path}`\n\n")
                outfile.write(f"```{file_type}\n")
                
                # File content
                try:
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        outfile.write(infile.read())
                except Exception as e:
                    outfile.write(f"Error reading file: {str(e)}")
                
                outfile.write("\n```\n\n")
                outfile.write("---\n\n")
            
            # Write summary
            outfile.write(f"## Summary\n")
            outfile.write(f"Total files processed: {len(self.files_found)}\n\n")
            outfile.write("### Files List:\n")
            for file_path in self.files_found:
                rel_path = os.path.relpath(file_path, self.start_path)
                outfile.write(f"- {rel_path}\n")

def main():
    parser = argparse.ArgumentParser(
        description='''Extract and concatenate files into a markdown document.
        
Usage examples:
  1. Simple:        python3 md_extractor.py frontend js
  2. Extended:      python3 md_extractor.py -d frontend -e js -o code_export
  3. All files:     python3 md_extractor.py -d frontend -e all
  4. Exclude files: python3 md_extractor.py -d frontend -e js --exclude-files "*.test.js" "*.spec.js"
        ''',
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    # Create two mutually exclusive groups for the two usage styles
    mode_group = parser.add_mutually_exclusive_group(required=True)
    
    # Simple mode arguments
    mode_group.add_argument('simple_dir', nargs='?',
                         help='Directory to scan (simple mode)')
    parser.add_argument('simple_ext', nargs='?',
                      help='File extension to process (simple mode)')
    
    # Extended mode arguments
    mode_group.add_argument('-d', '--directory',
                         help='Source directory to scan (extended mode)')
    parser.add_argument('-e', '--extensions', nargs='+',
                      help='File extensions to process (use "all" for all supported types)')
    
    # Common arguments
    parser.add_argument('-o', '--output-dir', default='export',
                      help='Output directory name (default: export)')
    parser.add_argument('--exclude-dirs', nargs='+',
                      help='Additional directories to exclude')
    parser.add_argument('--exclude-files', nargs='+',
                      help='File patterns to exclude (e.g., "*.test.js" "*.spec.js")')

    args = parser.parse_args()

    # Determine which mode we're in and set variables accordingly
    if args.simple_dir:
        if not args.simple_ext:
            parser.error('Simple mode requires both directory and extension')
        directory = args.simple_dir
        extensions = [args.simple_ext]
    else:
        if not args.extensions:
            parser.error('Extended mode requires -e/--extensions')
        directory = args.directory
        extensions = args.extensions

    # Add output directory to exclude dirs to prevent scanning
    exclude_dirs = ['.git', 'node_modules', '__pycache__', args.output_dir]
    if args.exclude_dirs:
        exclude_dirs.extend(args.exclude_dirs)

    try:
        concatenator = FileConcatenator(
            directory=directory,
            extensions=extensions,
            output_dir=args.output_dir,
            exclude_dirs=exclude_dirs,
            exclude_files=args.exclude_files
        )
        
        concatenator.find_files()
        concatenator.concatenate_files()
        print(f"\nSuccessfully created: {os.path.abspath(concatenator.output_file)}")
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())