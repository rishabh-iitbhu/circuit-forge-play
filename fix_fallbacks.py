#!/usr/bin/env python3
"""
Fix component suggestion fallbacks to prevent mixing web and local results
"""

import re

def fix_component_suggestions():
    """Fix the fallback behavior in component_suggestions.py"""
    
    file_path = "lib/component_suggestions.py"
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace all instances of fallback to local database
    old_pattern = r'st\.warning\(f"Web search failed: \{e\}\. Using local database\."\)'
    new_pattern = 'st.error(f"Web search failed: {e}")\n            return []  # Return empty list for pure web search mode'
    
    content = re.sub(old_pattern, new_pattern, content)
    
    # Write back the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Fixed component suggestion fallbacks")
    print("🚀 Web search mode now returns ONLY web results")

if __name__ == "__main__":
    fix_component_suggestions()