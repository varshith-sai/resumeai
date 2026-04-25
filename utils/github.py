import os
import requests
from dotenv import load_dotenv

load_dotenv()

from utils.config import personal

def _headers():
    token = os.getenv("GITHUB_TOKEN") or ""
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"
    return headers

def get_readme(repo_name):
    """Try to fetch README content as fallback description"""
    github_username = personal.get("github_username") or ""
    if not github_username:
        return "No description available"
    url = f"https://api.github.com/repos/{github_username}/{repo_name}/readme"
    response = requests.get(url, headers=_headers())
    if response.status_code == 200:
        import base64
        content = base64.b64decode(response.json()["content"]).decode("utf-8", errors="ignore")
        # Return first non-empty line of README
        for line in content.splitlines():
            line = line.strip().lstrip("#").strip()
            if line:
                return line[:200]
    return "No description available"

def get_github_projects():
    """Fetch all public repos with name, description, and languages"""
    github_username = personal.get("github_username") or ""
    if not github_username:
        print("⚠️ GitHub username missing in config")
        return []

    url = f"https://api.github.com/users/{github_username}/repos"
    response = requests.get(url, headers=_headers())

    if response.status_code != 200:
        print("❌ GitHub API error:", response.status_code, response.text)
        return []

    repos = response.json()
    projects = []

    for repo in repos:
        # Skip forked repos
        if repo.get("fork"):
            continue

        # Get description or fallback to README
        description = repo.get("description")
        if not description:
            description = get_readme(repo["name"])

        # Get languages
        lang_url = repo["languages_url"]
        lang_response = requests.get(lang_url, headers=_headers())
        languages = list(lang_response.json().keys()) if lang_response.status_code == 200 else []

        # Skip repos with no languages and no description
        if not languages and description == "No description available":
            continue

        projects.append({
            "name": repo["name"],
            "description": description,
            "languages": languages if languages else ["Not specified"],
            "url": repo["html_url"],
            "stars": repo["stargazers_count"]
        })

    return projects
