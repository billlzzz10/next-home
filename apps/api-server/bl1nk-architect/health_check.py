#!/usr/bin/env python
"""
Health Check CLI Tool

Usage:
    python health_check.py              # Run all checks
    python health_check.py --quick      # Quick checks only
    python health_check.py --json       # JSON output
    python health_check.py [check_name] # Specific check
"""

import asyncio
import json
import sys
from typing import Optional
import argparse
from datetime import datetime

# Add src to path
sys.path.insert(0, '/home/user/projects/bl1nk-architect')

from src.health_check import run_health_check, get_health_checker


def print_colored(text: str, color: str = "white"):
    """Print colored text"""
    colors = {
        "green": "\033[92m",
        "red": "\033[91m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "white": "\033[97m",
        "reset": "\033[0m"
    }
    print(f"{colors.get(color, '')}{text}{colors['reset']}")


def print_status(status: str) -> str:
    """Print status with color"""
    status_symbols = {
        "ok": ("✓ OK", "green"),
        "warning": ("⚠ WARNING", "yellow"),
        "error": ("✗ ERROR", "red"),
        "unconfigured": ("○ UNCONFIGURED", "blue")
    }
    symbol, color = status_symbols.get(status, ("? UNKNOWN", "white"))
    return f"{symbol}"


async def run_all_checks(json_output: bool = False):
    """Run all health checks"""
    print_colored("\n🏥 BL1NK ARCHITECT HEALTH CHECK", "blue")
    print_colored("=" * 50, "blue")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    result = await run_health_check()
    
    if json_output:
        print(json.dumps(result, indent=2, default=str))
        return
    
    # Print summary
    summary = result["summary"]
    print_colored("📊 SUMMARY", "blue")
    print(f"  Total Checks: {summary['total_checks']}")
    print(f"  OK: {summary['ok']} ✓")
    print(f"  Warnings: {summary['warning']} ⚠")
    print(f"  Errors: {summary['error']} ✗")
    print()
    
    # Print overall status
    overall = result["overall_status"]
    symbol, color = {
        "ok": ("✓", "green"),
        "warning": ("⚠", "yellow"),
        "error": ("✗", "red")
    }.get(overall, ("?", "white"))
    
    print_colored(f"Overall Status: {symbol} {overall.upper()}", color)
    print()
    
    # Print each check
    print_colored("📋 DETAILED RESULTS", "blue")
    print("-" * 50)
    
    for check_name, check_result in result["checks"].items():
        status = check_result["status"]
        color = {
            "ok": "green",
            "warning": "yellow",
            "error": "red",
            "unconfigured": "blue"
        }.get(status, "white")
        
        print(f"\n{check_name}:")
        print_colored(f"  Status: {print_status(status)}", color)
        print(f"  Message: {check_result['message']}")
        
        if check_result.get("details"):
            print("  Details:")
            for key, value in check_result["details"].items():
                if isinstance(value, list):
                    print(f"    {key}:")
                    for item in value[:3]:
                        print(f"      - {item}")
                    if len(value) > 3:
                        print(f"      ... and {len(value) - 3} more")
                elif isinstance(value, dict):
                    for k, v in value.items():
                        print(f"      {k}: {v}")
                else:
                    print(f"    {key}: {value}")
    
    print()
    print_colored("=" * 50, "blue")


async def run_quick_checks():
    """Run quick checks only"""
    print_colored("\n🏥 QUICK HEALTH CHECK", "blue")
    print_colored("=" * 50, "blue")
    
    checker = get_health_checker()
    await checker.check_basic_health()
    
    result = checker.results["Health Check"]
    
    color = "green" if result.status == "ok" else "yellow" if result.status == "warning" else "red"
    print_colored(f"Status: {print_status(result.status)}", color)
    print(f"Message: {result.message}")
    print()


async def run_specific_check(check_name: str, json_output: bool = False):
    """Run specific check"""
    check_mapping = {
        "health": "Health Check",
        "lint": "Lint Check",
        "skills": "Skill Check",
        "webhooks": "Webhook Check",
        "github": "GitHub Check",
        "deepresearch": "Deep Research Check",
    }
    
    actual_check = check_mapping.get(check_name.lower())
    
    if not actual_check:
        print_colored(f"Unknown check: {check_name}", "red")
        print(f"Available: {', '.join(check_mapping.keys())}")
        sys.exit(1)
    
    print_colored(f"\n🏥 {actual_check.upper()}", "blue")
    print_colored("=" * 50, "blue")
    
    checker = get_health_checker()
    
    # Run specific check
    if actual_check == "Health Check":
        await checker.check_basic_health()
    elif actual_check == "Lint Check":
        await checker.check_lint()
    elif actual_check == "Skill Check":
        await checker.check_skills()
    elif actual_check == "Webhook Check":
        await checker.check_webhooks()
    elif actual_check == "GitHub Check":
        await checker.check_github()
    elif actual_check == "Deep Research Check":
        await checker.check_deep_research()
    
    result = checker.results.get(actual_check)
    
    if not result:
        print_colored("Check not found", "red")
        sys.exit(1)
    
    if json_output:
        print(json.dumps({
            "check": actual_check,
            "status": result.status,
            "message": result.message,
            "details": result.details
        }, indent=2, default=str))
        return
    
    color = {
        "ok": "green",
        "warning": "yellow",
        "error": "red"
    }.get(result.status, "white")
    
    print_colored(f"Status: {print_status(result.status)}", color)
    print(f"Message: {result.message}")
    print()
    
    if result.details:
        print("Details:")
        for key, value in result.details.items():
            if isinstance(value, list):
                print(f"  {key}:")
                for item in value[:5]:
                    print(f"    - {item}")
                if len(value) > 5:
                    print(f"    ... and {len(value) - 5} more")
            elif isinstance(value, dict):
                print(f"  {key}:")
                for k, v in value.items():
                    print(f"    {k}: {v}")
            else:
                print(f"  {key}: {value}")
    
    print()


async def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Bl1nk Architect Health Check",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python health_check.py                # Run all checks
  python health_check.py --quick        # Quick checks
  python health_check.py --json         # JSON output
  python health_check.py lint           # Specific check
  python health_check.py skills --json  # JSON output for specific check
        """
    )
    
    parser.add_argument(
        "check",
        nargs="?",
        help="Specific check to run (health, lint, skills, webhooks, github, deepresearch)"
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Run quick checks only"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON"
    )
    
    args = parser.parse_args()
    
    try:
        if args.quick:
            await run_quick_checks()
        elif args.check:
            await run_specific_check(args.check, args.json)
        else:
            await run_all_checks(args.json)
    
    except Exception as e:
        print_colored(f"Error: {str(e)}", "red")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
