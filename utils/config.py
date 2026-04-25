import os
import yaml

_CONFIG_PATH = os.environ.get("RESUMEAI_CONFIG_PATH", "config.yaml")

_DEFAULT_PERSONAL = {
    "name": "",
    "phone": "",
    "email": "",
    "location": "",
    "linkedin": "",
    "github": "",
    "github_username": "",
}

# Keep shared objects so modules importing `personal`/`education`
# always see fresh values after reload_config().
personal = dict(_DEFAULT_PERSONAL)
education = []


def reload_config(path=None):
    path = path or _CONFIG_PATH
    if not os.path.exists(path):
        personal.clear()
        personal.update(_DEFAULT_PERSONAL)
        education.clear()
        return

    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    personal.clear()
    personal.update({**_DEFAULT_PERSONAL, **(data.get("personal") or {})})
    education.clear()
    education.extend(data.get("education") or [])


def load_config(path=None):
    path = path or _CONFIG_PATH
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"{path} not found. Copy config.example.yaml to config.yaml and fill in your details."
        )
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


reload_config()