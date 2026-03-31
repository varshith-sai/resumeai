import yaml
import os

def load_config(path="config.yaml"):
    if not os.path.exists(path):
        raise FileNotFoundError("config.yaml not found. Copy config.example.yaml to config.yaml and fill in your details.")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

config = load_config()
personal = config["personal"]
education = config["education"]