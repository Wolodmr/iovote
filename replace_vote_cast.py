import os

# Settings
OLD_NAME = "iovote"
NEW_NAME = "iovote"
EXTENSIONS = (".py", ".html", ".md", ".txt", ".yml", ".yaml", ".css", ".js")

EXCLUDE_DIRS = {".git", "venv", "__pycache__", "node_modules", "migrations"}

def should_exclude(dir_name):
    return any(part in EXCLUDE_DIRS for part in dir_name.split(os.sep))

def replace_in_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        if OLD_NAME in content:
            new_content = content.replace(OLD_NAME, NEW_NAME)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"✔ Replaced in: {filepath}")
    except (UnicodeDecodeError, PermissionError) as e:
        print(f"✖ Skipped (unreadable): {filepath}")

def walk_and_replace(base_dir="."):
    for root, dirs, files in os.walk(base_dir):
        # Skip unwanted directories
        if should_exclude(root):
            continue

        for file in files:
            if file.endswith(EXTENSIONS):
                full_path = os.path.join(root, file)
                replace_in_file(full_path)

if __name__ == "__main__":
    print(f"🔍 Replacing '{OLD_NAME}' with '{NEW_NAME}'...")
    walk_and_replace(".")
    print("✅ Done.")
