"""
Comprehensive Health Check System

Checks for:
1. Basic Health - Service up & running
2. Lint Check - Code quality
3. Skill Check - Skills discovery & loading
4. Webhook Check - Slack/Linear/ClickUp connectivity
5. GitHub Check - GitHub App & OAuth
6. Deep Research - Gemini API connectivity
"""

import os
import sys
import asyncio
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import importlib
import ast

logger = logging.getLogger(__name__)


@dataclass
class HealthCheckResult:
    """Result of a health check"""
    check_name: str
    status: str  # "ok", "warning", "error"
    message: str
    details: Dict[str, Any] = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.details is None:
            self.details = {}


class HealthChecker:
    """Main health checker"""
    
    def __init__(self):
        self.results: Dict[str, HealthCheckResult] = {}
        self.logger = logger
    
    async def run_all_checks(self) -> Dict[str, HealthCheckResult]:
        """Run all health checks"""
        self.results = {}
        
        # Sequential checks
        await self.check_basic_health()
        await self.check_lint()
        await self.check_skills()
        await self.check_webhooks()
        await self.check_github()
        await self.check_deep_research()
        
        return self.results
    
    def add_result(self, result: HealthCheckResult):
        """Add check result"""
        self.results[result.check_name] = result
    
    async def check_basic_health(self):
        """Check 1: Basic Health - Service up & running"""
        try:
            # Check Python version
            python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
            
            # Check required packages
            required_packages = [
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
            ]
            
            missing_packages = []
            for pkg in required_packages:
                try:
                    __import__(pkg)
                except ImportError:
                    missing_packages.append(pkg)
            
            if missing_packages:
                result = HealthCheckResult(
                    check_name="Health Check",
                    status="error",
                    message=f"Missing packages: {', '.join(missing_packages)}",
                    details={
                        "python_version": python_version,
                        "missing_packages": missing_packages,
                        "installed_count": len(required_packages) - len(missing_packages),
                        "total_required": len(required_packages)
                    }
                )
            else:
                result = HealthCheckResult(
                    check_name="Health Check",
                    status="ok",
                    message="All required packages installed",
                    details={
                        "python_version": python_version,
                        "packages_installed": len(required_packages)
                    }
                )
            
            self.add_result(result)
        
        except Exception as e:
            self.add_result(HealthCheckResult(
                check_name="Health Check",
                status="error",
                message=f"Error: {str(e)}",
                details={"error": str(e)}
            ))
    
    async def check_lint(self):
        """Check 2: Lint Check - Code quality"""
        try:
            src_dir = "/home/user/projects/bl1nk-architect/src"
            python_files = []
            lint_issues = []
            
            # Find all Python files
            import os
            for root, dirs, files in os.walk(src_dir):
                for file in files:
                    if file.endswith('.py'):
                        python_files.append(os.path.join(root, file))
            
            # Check each file
            for file_path in python_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        code = f.read()
                    
                    # Parse Python code
                    ast.parse(code)
                    
                    # Check for common issues
                    if len(code) > 50000:
                        lint_issues.append(f"{file_path}: File too large ({len(code)} chars)")
                    
                    if code.count('\t') > 0:
                        lint_issues.append(f"{file_path}: Contains tabs")
                    
                    # Check line length
                    for i, line in enumerate(code.split('\n'), 1):
                        if len(line) > 120:
                            lint_issues.append(f"{file_path}:{i}: Line too long ({len(line)} chars)")
                
                except SyntaxError as e:
                    lint_issues.append(f"{file_path}: Syntax error - {str(e)}")
            
            if lint_issues:
                status = "warning"
                message = f"Found {len(lint_issues)} potential issues"
            else:
                status = "ok"
                message = "Code quality OK"
            
            result = HealthCheckResult(
                check_name="Lint Check",
                status=status,
                message=message,
                details={
                    "files_checked": len(python_files),
                    "issues_found": len(lint_issues),
                    "issues": lint_issues[:10]  # First 10 issues
                }
            )
            
            self.add_result(result)
        
        except Exception as e:
            self.add_result(HealthCheckResult(
                check_name="Lint Check",
                status="error",
                message=f"Error: {str(e)}",
                details={"error": str(e)}
            ))
    
    async def check_skills(self):
        """Check 3: Skill Check - Skills discovery & loading"""
        try:
            from src.skill_loader import SkillDiscovery, SkillRegistry
            
            # Try to find skills
            skills_dir = "/home/user/skills"
            example_skills_dir = "/home/user/projects/bl1nk-architect/example-skills"
            
            discovered_skills = []
            failed_skills = []
            
            # Check multiple directories
            for skills_root in [skills_dir, example_skills_dir]:
                if os.path.exists(skills_root):
                    try:
                        skills = SkillDiscovery.find_skills(skills_root)
                        discovered_skills.extend(skills)
                    except Exception as e:
                        failed_skills.append(f"{skills_root}: {str(e)}")
            
            # Try to parse discovered skills
            parsed_skills = []
            parse_errors = []
            
            for skill_path in discovered_skills:
                try:
                    skill = SkillDiscovery.parse_skill_file(skill_path)
                    if skill:
                        parsed_skills.append(skill.metadata.name)
                    else:
                        parse_errors.append(f"Could not parse: {skill_path}")
                except Exception as e:
                    parse_errors.append(f"{skill_path}: {str(e)}")
            
            if parse_errors:
                status = "warning"
                message = f"Discovered {len(discovered_skills)} skills, {len(parse_errors)} errors"
            elif discovered_skills:
                status = "ok"
                message = f"Successfully discovered {len(parsed_skills)} skills"
            else:
                status = "warning"
                message = "No skills found in expected directories"
            
            result = HealthCheckResult(
                check_name="Skill Check",
                status=status,
                message=message,
                details={
                    "skills_found": len(discovered_skills),
                    "skills_parsed": len(parsed_skills),
                    "parsed_skill_names": parsed_skills,
                    "errors": parse_errors[:5]
                }
            )
            
            self.add_result(result)
        
        except Exception as e:
            self.add_result(HealthCheckResult(
                check_name="Skill Check",
                status="error",
                message=f"Error: {str(e)}",
                details={"error": str(e)}
            ))
    
    async def check_webhooks(self):
        """Check 4: Webhook Check - Slack/Linear/ClickUp connectivity"""
        try:
            webhook_results = {
                "slack": {"status": "unconfigured", "message": ""},
                "linear": {"status": "unconfigured", "message": ""},
                "clickup": {"status": "unconfigured", "message": ""},
            }
            
            # Check Slack
            slack_webhook = os.getenv("SLACK_WEBHOOK_URL")
            if slack_webhook:
                try:
                    import httpx
                    async with httpx.AsyncClient(timeout=5) as client:
                        response = await client.post(
                            slack_webhook,
                            json={"text": "Health check ping"}
                        )
                        if response.status_code == 200:
                            webhook_results["slack"] = {
                                "status": "ok",
                                "message": "Webhook accessible"
                            }
                        else:
                            webhook_results["slack"] = {
                                "status": "error",
                                "message": f"HTTP {response.status_code}"
                            }
                except Exception as e:
                    webhook_results["slack"] = {
                        "status": "error",
                        "message": str(e)
                    }
            
            # Check Linear
            linear_api_key = os.getenv("LINEAR_API_KEY")
            if linear_api_key:
                try:
                    import httpx
                    async with httpx.AsyncClient(timeout=5) as client:
                        response = await client.post(
                            "https://api.linear.app/graphql",
                            json={"query": "{ viewer { id } }"},
                            headers={"Authorization": f"Bearer {linear_api_key}"}
                        )
                        if "errors" not in response.json():
                            webhook_results["linear"] = {
                                "status": "ok",
                                "message": "API accessible"
                            }
                        else:
                            webhook_results["linear"] = {
                                "status": "error",
                                "message": "API error"
                            }
                except Exception as e:
                    webhook_results["linear"] = {
                        "status": "error",
                        "message": str(e)
                    }
            
            # Check ClickUp
            clickup_api_key = os.getenv("CLICKUP_API_KEY")
            if clickup_api_key:
                try:
                    import httpx
                    async with httpx.AsyncClient(timeout=5) as client:
                        response = await client.get(
                            "https://api.clickup.com/api/v2/user",
                            headers={"Authorization": clickup_api_key}
                        )
                        if response.status_code == 200:
                            webhook_results["clickup"] = {
                                "status": "ok",
                                "message": "API accessible"
                            }
                        else:
                            webhook_results["clickup"] = {
                                "status": "error",
                                "message": f"HTTP {response.status_code}"
                            }
                except Exception as e:
                    webhook_results["clickup"] = {
                        "status": "error",
                        "message": str(e)
                    }
            
            # Determine overall status
            configured = sum(1 for v in webhook_results.values() if v["status"] != "unconfigured")
            errors = sum(1 for v in webhook_results.values() if v["status"] == "error")
            
            if errors == 0 and configured > 0:
                status = "ok"
                message = f"All {configured} webhooks accessible"
            elif configured == 0:
                status = "warning"
                message = "No webhooks configured"
            else:
                status = "warning"
                message = f"{errors} webhook(s) have errors"
            
            result = HealthCheckResult(
                check_name="Webhook Check",
                status=status,
                message=message,
                details={
                    "slack": webhook_results["slack"],
                    "linear": webhook_results["linear"],
                    "clickup": webhook_results["clickup"],
                    "configured": configured,
                    "errors": errors
                }
            )
            
            self.add_result(result)
        
        except Exception as e:
            self.add_result(HealthCheckResult(
                check_name="Webhook Check",
                status="error",
                message=f"Error: {str(e)}",
                details={"error": str(e)}
            ))
    
    async def check_github(self):
        """Check 5: GitHub Check - GitHub App & OAuth"""
        try:
            github_checks = {
                "app_id": os.getenv("GITHUB_APP_ID"),
                "private_key": "***" if os.getenv("GITHUB_PRIVATE_KEY") else None,
                "app_name": os.getenv("GITHUB_APP_NAME"),
            }
            
            missing = []
            for key, value in github_checks.items():
                if not value:
                    missing.append(key)
            
            # Try to validate key format if present
            private_key = os.getenv("GITHUB_PRIVATE_KEY")
            key_valid = False
            if private_key:
                try:
                    from cryptography.hazmat.primitives import serialization
                    serialization.load_pem_private_key(
                        private_key.encode(),
                        password=None,
                        backend=None
                    )
                    key_valid = True
                except Exception as e:
                    missing.append(f"Invalid private key: {str(e)}")
            
            if not missing:
                status = "ok"
                message = "GitHub configuration valid"
            elif missing == ["app_id", "private_key", "app_name"]:
                status = "warning"
                message = "GitHub not configured"
            else:
                status = "error"
                message = f"Missing: {', '.join(missing)}"
            
            result = HealthCheckResult(
                check_name="GitHub Check",
                status=status,
                message=message,
                details={
                    "app_id": "✓" if github_checks["app_id"] else "✗",
                    "private_key": "✓" if key_valid else "✗",
                    "app_name": "✓" if github_checks["app_name"] else "✗",
                    "missing": missing
                }
            )
            
            self.add_result(result)
        
        except Exception as e:
            self.add_result(HealthCheckResult(
                check_name="GitHub Check",
                status="error",
                message=f"Error: {str(e)}",
                details={"error": str(e)}
            ))
    
    async def check_deep_research(self):
        """Check 6: Deep Research - Gemini API connectivity"""
        try:
            google_api_key = os.getenv("GOOGLE_API_KEY")
            
            if not google_api_key:
                result = HealthCheckResult(
                    check_name="Deep Research Check",
                    status="warning",
                    message="Gemini API key not configured",
                    details={"configured": False}
                )
            else:
                # Try to authenticate
                try:
                    import google.genai as genai
                    genai.configure(api_key=google_api_key)
                    
                    # Try a simple API call
                    model = genai.GenerativeModel('gemini-1.5-pro')
                    response = model.generate_content("ping")
                    
                    result = HealthCheckResult(
                        check_name="Deep Research Check",
                        status="ok",
                        message="Gemini API accessible",
                        details={
                            "configured": True,
                            "model": "gemini-1.5-pro",
                            "response_status": "ok"
                        }
                    )
                
                except Exception as e:
                    result = HealthCheckResult(
                        check_name="Deep Research Check",
                        status="error",
                        message=f"Gemini API error: {str(e)}",
                        details={
                            "configured": True,
                            "error": str(e)
                        }
                    )
            
            self.add_result(result)
        
        except Exception as e:
            self.add_result(HealthCheckResult(
                check_name="Deep Research Check",
                status="error",
                message=f"Error: {str(e)}",
                details={"error": str(e)}
            ))
    
    def get_summary(self) -> Dict[str, Any]:
        """Get health check summary"""
        total = len(self.results)
        ok_count = sum(1 for r in self.results.values() if r.status == "ok")
        warning_count = sum(1 for r in self.results.values() if r.status == "warning")
        error_count = sum(1 for r in self.results.values() if r.status == "error")
        
        # Determine overall status
        if error_count > 0:
            overall_status = "error"
        elif warning_count > 0:
            overall_status = "warning"
        else:
            overall_status = "ok"
        
        return {
            "overall_status": overall_status,
            "summary": {
                "total_checks": total,
                "ok": ok_count,
                "warning": warning_count,
                "error": error_count
            },
            "timestamp": datetime.now().isoformat(),
            "checks": {
                name: {
                    "status": result.status,
                    "message": result.message,
                    "details": result.details
                }
                for name, result in self.results.items()
            }
        }


# Global health checker instance
_health_checker: Optional[HealthChecker] = None


def get_health_checker() -> HealthChecker:
    """Get or create health checker"""
    global _health_checker
    if _health_checker is None:
        _health_checker = HealthChecker()
    return _health_checker


async def run_health_check() -> Dict[str, Any]:
    """Run all health checks and return summary"""
    checker = get_health_checker()
    await checker.run_all_checks()
    return checker.get_summary()


if __name__ == "__main__":
    import json
    
    async def main():
        result = await run_health_check()
        print(json.dumps(result, indent=2, default=str))
    
    asyncio.run(main())
