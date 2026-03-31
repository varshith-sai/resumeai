import os
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
from utils.config import personal
GITHUB_USERNAME = personal["github_username"]

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def get_readme(repo_name):
    """Try to fetch README content as fallback description"""
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{repo_name}/readme"
    response = requests.get(url, headers=headers)
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
    url = f"https://api.github.com/users/{GITHUB_USERNAME}/repos"
    response = requests.get(url, headers=headers)

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
        lang_response = requests.get(lang_url, headers=headers)
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
