import httpx
import base64
import re
from typing import Dict, List, Optional
from app.core.config import get_settings


class GitHubClient:
    """Async client for fetching GitHub repository data."""

    BASE_URL = "https://api.github.com"

    def __init__(self):
        settings = get_settings()
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-Repo-Analyzer-AI",
        }
        if settings.GITHUB_TOKEN:
            self.headers["Authorization"] = f"token {settings.GITHUB_TOKEN}"

    def _parse_repo_url(self, repo_url: str) -> tuple:
        """Extract owner and repo name from GitHub URL."""
        patterns = [
            r"github\.com/([^/]+)/([^/\s]+?)(?:\.git)?$",
            r"github\.com/([^/]+)/([^/\s]+?)/?$",
        ]
        for pattern in patterns:
            match = re.search(pattern, repo_url.strip())
            if match:
                return match.group(1), match.group(2)
        raise ValueError(f"Invalid GitHub URL: {repo_url}")

    async def _get(self, url: str, params: Optional[Dict] = None) -> Dict:
        """Make an async GET request to GitHub API."""
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            response = await client.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()

    async def fetch_repo_metadata(self, repo_url: str) -> Dict:
        """Fetch repository metadata (description, stars, language, etc.)."""
        owner, repo = self._parse_repo_url(repo_url)
        url = f"{self.BASE_URL}/repos/{owner}/{repo}"
        return await self._get(url)

    async def fetch_readme(self, repo_url: str) -> str:
        """Fetch and decode the README file content."""
        owner, repo = self._parse_repo_url(repo_url)
        try:
            url = f"{self.BASE_URL}/repos/{owner}/{repo}/readme"
            data = await self._get(url)
            content = data.get("content", "")
            return base64.b64decode(content).decode("utf-8", errors="replace")
        except Exception:
            return "README not found or could not be decoded."

    async def fetch_directory_structure(self, repo_url: str, path: str = "") -> List[Dict]:
        """Fetch the top-level directory structure of the repository."""
        owner, repo = self._parse_repo_url(repo_url)
        try:
            url = f"{self.BASE_URL}/repos/{owner}/{repo}/contents/{path}"
            data = await self._get(url)
            if isinstance(data, list):
                return data
            return [data]
        except Exception:
            return []

    async def fetch_file_content(self, repo_url: str, filepath: str) -> Optional[str]:
        """Fetch and decode a single file's content from the repository."""
        owner, repo = self._parse_repo_url(repo_url)
        try:
            url = f"{self.BASE_URL}/repos/{owner}/{repo}/contents/{filepath}"
            data = await self._get(url)
            content = data.get("content", "")
            if data.get("encoding") == "base64" and content:
                return base64.b64decode(content).decode("utf-8", errors="replace")[:5000]
            return content[:5000] if content else None
        except Exception:
            return None

    async def fetch_key_files(self, repo_url: str) -> Dict[str, str]:
        """Fetch content of key configuration and documentation files."""
        key_filenames = [
            "requirements.txt",
            "package.json",
            "setup.py",
            "setup.cfg",
            "pyproject.toml",
            "Cargo.toml",
            "go.mod",
            "Dockerfile",
            "docker-compose.yml",
            "Makefile",
            ".env.example",
            "config.yaml",
            "config.yml",
            "tsconfig.json",
            "Gemfile",
            "pom.xml",
            "build.gradle",
            "CMakeLists.txt",
        ]

        files_content = {}

        # First get root-level files
        root_files = await self.fetch_directory_structure(repo_url)
        root_file_names = [f.get("name", "") for f in root_files if f.get("type") == "file"]

        # Fetch key files from root
        for filename in root_file_names:
            if filename in key_filenames:
                content = await self.fetch_file_content(repo_url, filename)
                if content:
                    files_content[filename] = content

        # Also check common subdirectories for config files
        subdirs = [f for f in root_files if f.get("type") == "dir"]
        important_subdirs = ["src", "config", "docs", "app", "backend", "frontend"]
        for subdir in subdirs:
            subdir_name = subdir.get("name", "")
            if subdir_name in important_subdirs:
                sub_files = await self.fetch_directory_structure(repo_url, subdir_name)
                for sf in sub_files:
                    sf_name = sf.get("name", "")
                    if sf_name in key_filenames:
                        filepath = f"{subdir_name}/{sf_name}"
                        content = await self.fetch_file_content(repo_url, filepath)
                        if content:
                            files_content[filepath] = content

        return files_content

    async def fetch_languages(self, repo_url: str) -> Dict[str, int]:
        """Fetch language breakdown for the repository."""
        owner, repo = self._parse_repo_url(repo_url)
        try:
            url = f"{self.BASE_URL}/repos/{owner}/{repo}/languages"
            return await self._get(url)
        except Exception:
            return {}

    async def get_full_repo_data(self, repo_url: str) -> Dict:
        """Aggregate all repository data into a single dictionary."""
        print(f"Fetching data for: {repo_url}")

        # Fetch all data sequentially
        metadata = await self.fetch_repo_metadata(repo_url)
        readme = await self.fetch_readme(repo_url)
        structure = await self.fetch_directory_structure(repo_url)
        key_files = await self.fetch_key_files(repo_url)
        languages = await self.fetch_languages(repo_url)

        # Build directory tree string
        dir_tree = self._build_tree(structure)

        return {
            "repo_url": repo_url,
            "metadata": {
                "name": metadata.get("name", ""),
                "full_name": metadata.get("full_name", ""),
                "description": metadata.get("description", ""),
                "language": metadata.get("language", ""),
                "languages": languages,
                "stargazers_count": metadata.get("stargazers_count", 0),
                "forks_count": metadata.get("forks_count", 0),
                "topics": metadata.get("topics", []),
                "license": metadata.get("license", {}).get("name", "No license") if metadata.get("license") else "No license",
                "default_branch": metadata.get("default_branch", "main"),
                "created_at": metadata.get("created_at", ""),
                "updated_at": metadata.get("updated_at", ""),
                "open_issues_count": metadata.get("open_issues_count", 0),
                "size": metadata.get("size", 0),
            },
            "readme": readme[:8000],
            "directory_structure": dir_tree,
            "key_files": key_files,
        }

    def _build_tree(self, structure: List[Dict], indent: int = 0) -> str:
        """Build a tree-like string from the directory structure."""
        tree = ""
        for item in structure[:50]:
            prefix = "  " * indent + ("DIR " if item.get("type") == "dir" else "FILE ")
            tree += f"{prefix}{item.get('name', '')}\n"
            # Recurse one level deep for directories
            if item.get("type") == "dir" and indent == 0:
                tree += f"  {item.get('name', '')}/\n"
        return tree
