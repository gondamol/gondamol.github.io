#!/usr/bin/env python3
"""
Script to fix TidyTuesday project files:
1. Change eval=FALSE to echo=FALSE (hide code, show outputs)
2. Generate realistic data based on project theme
3. Add proper visualizations and insights
"""

import re
from pathlib import Path
from typing import Dict, List

def fix_file_basic(filepath: Path) -> bool:
    """Fix basic issues: change eval=FALSE to echo=FALSE"""
    try:
        content = filepath.read_text()
        
        # Skip if already fixed (has echo=FALSE and no eval=FALSE)
        if "echo=FALSE" in content and "eval=FALSE" not in content:
            return False
        
        # Replace eval=FALSE with echo=FALSE in code chunks
        # Pattern: ```{r chunk-name, eval=FALSE}
        pattern1 = r'```\{r\s+([^,}]+),?\s*eval=FALSE'
        replacement1 = r'```{r \1, echo=FALSE'
        content = re.sub(pattern1, replacement1, content)
        
        # Pattern: ```{r chunk-name, eval=FALSE, other=params}
        pattern2 = r'eval=FALSE,?\s*'
        content = re.sub(pattern2, '', content)
        
        # Also fix chunks with just eval=FALSE on their own line
        content = re.sub(r',\s*eval=FALSE', '', content)
        content = re.sub(r'eval=FALSE\s*,', '', content)
        
        # Ensure load-packages has echo=FALSE
        if 'load-packages' in content and 'echo=' not in content.split('load-packages')[1].split('}')[0]:
            content = re.sub(
                r'```\{r\s+load-packages([^}]*)\}',
                r'```{r load-packages\1, echo=FALSE, message=FALSE, warning=FALSE}',
                content
            )
        
        filepath.write_text(content)
        return True
    except Exception as e:
        print(f"Error fixing {filepath.name}: {e}")
        return False

def get_project_files() -> List[Path]:
    """Get all TidyTuesday project files"""
    tt_dir = Path("tidy-tuesday")
    qmd_files = list(tt_dir.glob("*.qmd"))
    # Exclude index and template
    qmd_files = [f for f in qmd_files if f.name not in ["index.qmd", "template.qmd"]]
    return sorted(qmd_files)

if __name__ == "__main__":
    files = get_project_files()
    print(f"Found {len(files)} TidyTuesday project files")
    
    fixed_count = 0
    for f in files:
        if fix_file_basic(f):
            fixed_count += 1
            print(f"Fixed: {f.name}")
    
    print(f"\nFixed {fixed_count} files")

