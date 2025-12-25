#!/usr/bin/env python
"""
Dependency Check Script

Checks:
1. Python version
2. Virtual environment
3. Required packages
4. .env configuration
5. Environment variables
"""

import os
import sys
import subprocess
from typing import List, Tuple

def print_header(text: str):
    """Print colored header"""
    print(f"\n\033[94m{'=' * 60}\033[0m")
    print(f"\033[94m{text:^60}\033[0m")
    print(f"\033[94m{'=' * 60}\033[0m\n")

def print_check(name: str, passed: bool, details: str = ""):
    """Print check result"""
    symbol = "✓" if passed else "✗"
    color = "\033[92m" if passed else "\033[91m"
    reset = "\033[0m"
    print(f"{color}{symbol}{reset} {name}")
    if details:
        print(f"  {details}")

def check_python_version() -> Tuple[bool, str]:
    """Check Python version"""
    required_version = (3, 11)
    current = sys.version_info[:2]
    
    if current >= required_version:
        return True, f"Python {current[0]}.{current[1]} ✓"
    else:
        return False, f"Python {current[0]}.{current[1]} (need 3.11+)"

def check_venv() -> Tuple[bool, str]:
    """Check if in virtual environment"""
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    if in_venv:
        return True, f"Using: {sys.prefix}"
    else:
        return False, "Not in virtual environment"

def check_packages() -> Tuple[bool, List[str]]:
    """Check required packages"""
    required = [
        'fastapi',
        'fastapi_poe',
        'modal',
        'google.genai',
        'PyGithub',
        'requests',
        'pyjwt',
        'cryptography',
        'jinja2',
        'python_dotenv',
        'httpx',
        'pyyaml',
        'streamlit',
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if not missing:
        return True, []
    else:
        return False, missing

def check_env_file() -> Tuple[bool, str]:
    """Check .env file"""
    if os.path.exists('.env'):
        return True, ".env file exists"
    elif os.path.exists('.env.example'):
        return False, ".env not found (use .env.example as template)"
    else:
        return False, ".env not found"

def check_env_vars() -> Tuple[bool, List[str]]:
    """Check required environment variables"""
    required_vars = [
        'POE_ACCESS_KEY',
        'GITHUB_APP_ID',
        'GITHUB_PRIVATE_KEY',
        'GOOGLE_API_KEY',
    ]
    
    missing = []
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
    
    if not missing:
        return True, []
    else:
        return False, missing

def check_directories() -> Tuple[bool, str]:
    """Check required directories"""
    required_dirs = [
        'src',
        'src/notifications',
        'src/widgets',
        'example-skills',
    ]
    
    missing = []
    for dir_name in required_dirs:
        if not os.path.isdir(dir_name):
            missing.append(dir_name)
    
    if not missing:
        return True, "All directories present"
    else:
        return False, f"Missing: {', '.join(missing)}"

def check_files() -> Tuple[bool, str]:
    """Check required files"""
    required_files = [
        'modal_app.py',
        'health_check.py',
        '.env.example',
        'pyproject.toml',
    ]
    
    missing = []
    for file_name in required_files:
        if not os.path.isfile(file_name):
            missing.append(file_name)
    
    if not missing:
        return True, "All required files present"
    else:
        return False, f"Missing: {', '.join(missing)}"

def main():
    """Run all checks"""
    print_header("🏥 DEPENDENCY CHECK")
    
    # Python version
    passed, details = check_python_version()
    print_check("Python Version", passed, details)
    
    # Virtual environment
    passed, details = check_venv()
    print_check("Virtual Environment", passed, details)
    
    # Directories
    passed, details = check_directories()
    print_check("Project Structure", passed, details)
    
    # Files
    passed, details = check_files()
    print_check("Required Files", passed, details)
    
    # Packages
    passed, missing = check_packages()
    if passed:
        print_check("Required Packages", True, f"All {13} packages installed")
    else:
        print_check("Required Packages", False)
        print(f"  Missing packages ({len(missing)}):")
        for pkg in missing:
            print(f"    - {pkg}")
        print(f"\n  Install with: pip install -e \".[dev]\"")
    
    # .env file
    passed, details = check_env_file()
    print_check(".env Configuration", passed, details)
    
    # Environment variables
    passed, missing = check_env_vars()
    if passed:
        print_check("Environment Variables", True, "All required vars set")
    else:
        print_check("Environment Variables", False)
        print(f"  Missing variables ({len(missing)}):")
        for var in missing:
            print(f"    - {var}")
        print(f"\n  Set in .env file or export")
    
    # Summary
    print_header("📋 SUMMARY")
    
    all_checks = [
        check_python_version()[0],
        check_venv()[0],
        check_directories()[0],
        check_files()[0],
        check_packages()[0],
        check_env_file()[0],
    ]
    
    passed_count = sum(all_checks)
    total_count = len(all_checks)
    
    print(f"Passed: {passed_count}/{total_count}")
    
    if passed_count == total_count:
        print("\n✅ All checks passed! Ready to run.")
        print("\nNext: python health_check.py")
        return 0
    else:
        print(f"\n❌ {total_count - passed_count} check(s) failed.")
        print("\nFix issues above and run again.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
