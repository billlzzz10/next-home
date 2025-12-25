"""Output Formatter - Convert analysis results to Markdown"""

from typing import List, Dict, Any


def format_architecture_plan(tasks: List[Dict[str, Any]]) -> str:
    """Format architecture analysis tasks as table"""
    if not tasks:
        return "No tasks"
    md = "| Task | Priority | Effort |\n|------|----------|--------|\n"
    for task in tasks[:10]:
        md += f"| {task.get('name', '')} | {task.get('priority', 'M')} | {task.get('effort', 'N/A')} |\n"
    return md


def format_dependencies_report(python_deps: List[str], typescript_deps: List[str]) -> str:
    """Format dependency report"""
    md = "## Dependencies\n\n"
    if python_deps:
        md += f"**Python**: {len(python_deps)} packages\n"
    if typescript_deps:
        md += f"**TypeScript**: {len(typescript_deps)} packages\n"
    return md


def format_duplicates_report(duplicates: List[Dict]) -> str:
    """Format duplication report"""
    if not duplicates:
        return "✅ No duplicates found"
    return f"⚠️ Found {len(duplicates)} duplicate patterns"


def format_summary_section(repo_name: str, total_files: int, issues: int, recs: int) -> str:
    """Format analysis summary"""
    return f"**Repository**: {repo_name} | **Files**: {total_files} | **Issues**: {issues}"
