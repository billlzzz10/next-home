"""
GitHub API Client

Interacts with GitHub API using app installation token.
Handles repository scanning, dependency parsing, and code analysis.
"""

import logging
from typing import List, Dict, Optional, Any
import requests
import json

logger = logging.getLogger(__name__)


class GitHubClient:
    """GitHub API client for repository analysis"""
    
    def __init__(self, installation_id: str, access_token: str):
        """
        Initialize GitHub client.
        
        Args:
            installation_id: GitHub App installation ID
            access_token: GitHub API access token
        """
        self.installation_id = installation_id
        self.access_token = access_token
        self.headers = {
            "Authorization": f"token {access_token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        self.base_url = "https://api.github.com"
    
    async def list_repositories(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        List repositories accessible via GitHub App installation.
        
        Args:
            limit: Maximum number of repos to return
            
        Returns:
            List of repository information
        """
        try:
            url = f"{self.base_url}/installation/repositories"
            params = {"per_page": min(limit, 100)}
            
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            repos = data.get("repositories", [])
            
            logger.info(f"Found {len(repos)} repositories")
            
            return [
                {
                    "name": repo["name"],
                    "full_name": repo["full_name"],
                    "description": repo.get("description", ""),
                    "language": repo.get("language", ""),
                    "url": repo["html_url"],
                    "private": repo["private"],
                }
                for repo in repos[:limit]
            ]
        
        except Exception as e:
            logger.exception(f"Error listing repositories: {e}")
            return []
    
    async def list_files(
        self,
        repo_name: str,
        limit: int = 100,
        path: str = ""
    ) -> List[str]:
        """
        Recursively list all files in repository.
        
        Args:
            repo_name: Repository name
            limit: Maximum files to return
            path: Path within repository (for recursion)
            
        Returns:
            List of file paths
        """
        try:
            files = []
            
            url = f"{self.base_url}/repos/{repo_name}/contents/{path}"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            items = response.json()
            if not isinstance(items, list):
                items = [items]
            
            for item in items:
                if len(files) >= limit:
                    break
                
                if item["type"] == "file":
                    files.append(item["path"])
                elif item["type"] == "dir" and len(files) < limit - 10:
                    # Recursively add subdirectories (limit depth)
                    sub_files = await self.list_files(
                        repo_name,
                        limit - len(files),
                        item["path"]
                    )
                    files.extend(sub_files)
            
            return files
        
        except Exception as e:
            logger.exception(f"Error listing files: {e}")
            return []
    
    async def get_python_dependencies(self, repo_name: str) -> List[str]:
        """
        Extract Python dependencies from requirements files.
        
        Args:
            repo_name: Repository name
            
        Returns:
            List of dependencies
        """
        try:
            deps = []
            
            # Check requirements.txt, requirements-*.txt, setup.py, pyproject.toml
            files_to_check = [
                "requirements.txt",
                "requirements-dev.txt",
                "setup.py",
                "pyproject.toml",
            ]
            
            for filename in files_to_check:
                try:
                    url = f"{self.base_url}/repos/{repo_name}/contents/{filename}"
                    response = requests.get(url, headers=self.headers)
                    
                    if response.status_code == 200:
                        content = response.json().get("content", "")
                        # Decode base64
                        import base64
                        decoded = base64.b64decode(content).decode('utf-8')
                        
                        # Parse dependencies
                        for line in decoded.split('\n'):
                            line = line.strip()
                            if line and not line.startswith('#'):
                                # Extract package name
                                pkg = line.split('==')[0].split('>=')[0].split('<=')[0].strip()
                                if pkg and pkg not in deps:
                                    deps.append(pkg)
                except requests.exceptions.HTTPError:
                    continue
            
            logger.info(f"Found {len(deps)} Python dependencies")
            return deps
        
        except Exception as e:
            logger.exception(f"Error getting Python dependencies: {e}")
            return []
    
    async def get_typescript_dependencies(self, repo_name: str) -> List[str]:
        """
        Extract TypeScript/Node dependencies from package.json.
        
        Args:
            repo_name: Repository name
            
        Returns:
            List of dependencies
        """
        try:
            deps = []
            
            url = f"{self.base_url}/repos/{repo_name}/contents/package.json"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                content = response.json().get("content", "")
                # Decode base64
                import base64
                decoded = base64.b64decode(content).decode('utf-8')
                
                try:
                    package_data = json.loads(decoded)
                    
                    for dep_type in ["dependencies", "devDependencies"]:
                        for pkg_name in package_data.get(dep_type, {}).keys():
                            if pkg_name not in deps:
                                deps.append(pkg_name)
                except json.JSONDecodeError:
                    logger.warning("Could not parse package.json")
            
            logger.info(f"Found {len(deps)} TypeScript/Node dependencies")
            return deps
        
        except Exception as e:
            logger.exception(f"Error getting TypeScript dependencies: {e}")
            return []
    
    async def detect_code_duplicates(self, repo_name: str) -> List[Dict[str, Any]]:
        """
        Detect code duplication patterns (simplified).
        
        Args:
            repo_name: Repository name
            
        Returns:
            List of duplicate patterns found
        """
        try:
            # This is a simplified version
            # In production, you'd use proper tools like ast or duplication detection
            duplicates = []
            
            # Common patterns to look for
            patterns = [
                {"pattern": "Duplicate error handling", "count": 0},
                {"pattern": "Similar utility functions", "count": 0},
                {"pattern": "Repeated configuration", "count": 0},
            ]
            
            logger.info(f"Duplication scan completed: {len(duplicates)} patterns")
            return duplicates
        
        except Exception as e:
            logger.exception(f"Error detecting duplicates: {e}")
            return []
    
    async def get_file_content(
        self,
        repo_name: str,
        file_path: str
    ) -> Optional[str]:
        """
        Get raw content of a file.
        
        Args:
            repo_name: Repository name
            file_path: Path to file
            
        Returns:
            File content or None
        """
        try:
            url = f"{self.base_url}/repos/{repo_name}/contents/{file_path}"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            content = response.json().get("content", "")
            import base64
            return base64.b64decode(content).decode('utf-8')
        
        except Exception as e:
            logger.exception(f"Error getting file content: {e}")
            return None
    
    async def get_repository_info(self, repo_name: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed repository information.
        
        Args:
            repo_name: Repository name
            
        Returns:
            Repository information
        """
        try:
            url = f"{self.base_url}/repos/{repo_name}"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            repo = response.json()
            return {
                "name": repo["name"],
                "full_name": repo["full_name"],
                "description": repo.get("description", ""),
                "language": repo.get("language", ""),
                "stars": repo["stargazers_count"],
                "forks": repo["forks_count"],
                "open_issues": repo["open_issues_count"],
                "created_at": repo["created_at"],
                "updated_at": repo["updated_at"],
            }
        
        except Exception as e:
            logger.exception(f"Error getting repository info: {e}")
            return None
