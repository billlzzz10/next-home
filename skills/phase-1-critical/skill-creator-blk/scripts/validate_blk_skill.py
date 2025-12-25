#!/usr/bin/env python3
"""
Validate BL1NK-specific skill requirements
Checks if a skill fits into BL1NK workspace architecture
"""

import sys
import json
from pathlib import Path

def validate_blk_skill(skill_path):
    """Validate BL1NK-specific skill requirements"""
    
    skill_path = Path(skill_path)
    skill_md = skill_path / "SKILL.md"
    
    if not skill_md.exists():
        print("❌ SKILL.md not found")
        return False
    
    with open(skill_md, 'r') as f:
        content = f.read()
    
    issues = []
    warnings = []
    
    # Check 1: Name format
    if "name:" not in content:
        issues.append("Missing 'name:' in SKILL.md frontmatter")
    
    # Check 2: Description
    if "description:" not in content:
        issues.append("Missing 'description:' in frontmatter")
    
    # Check 3: BL1NK context
    if "BL1NK" not in content and "workspace" not in content.lower():
        warnings.append("No reference to BL1NK workspace in documentation")
    
    # Check 4: Integration points
    if "notification" not in content and "github" not in content and "poe" not in content:
        if "external" not in content.lower() and "integration" not in content.lower():
            warnings.append("No clear integration points documented")
    
    # Check 5: Phase mention
    if "Phase" not in content:
        warnings.append("Phase placement not mentioned (Phase 1-4)")
    
    # Check 6: Examples
    if "example" not in content.lower() and "input" not in content.lower():
        warnings.append("No examples or test cases documented")
    
    # Print results
    print("\n✅ BL1NK Skill Validation Results")
    print("=" * 50)
    
    if issues:
        print(f"\n❌ Issues ({len(issues)}):")
        for issue in issues:
            print(f"  - {issue}")
    
    if warnings:
        print(f"\n⚠️  Warnings ({len(warnings)}):")
        for warning in warnings:
            print(f"  - {warning}")
    
    if not issues:
        print("\n✅ All checks passed!")
    
    return len(issues) == 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: validate_blk_skill.py <skill-path>")
        sys.exit(1)
    
    success = validate_blk_skill(sys.argv[1])
    sys.exit(0 if success else 1)
