import json
import os
import re
import sys


def get_event():
    path = os.environ.get("GITHUB_EVENT_PATH")
    if os.path.isfile(path):
        with open(path) as f:
            return json.load(f)
    return {}


def clean_flag(flag):
    if flag.startswith("["):
        flag = flag[1:]
    if flag.endswith("]"):
        flag = flag[:-1]
    flag = " ".join(
        flag.lower()
        .replace(";", " ")
        .replace("'", "")
        .replace("\"", "")
        .split()
    ).strip()
    return f"[{flag}]"


def flags_from_labels(labels):
    labels = [label.get("name") for label in labels]
    return [clean_flag(flag) for flag in labels if flag]


def flags_from_text(text):
    flags = re.findall(r"\[[0-9a-zA-Z\s'\"\.]+\]", string=text)
    return [clean_flag(flag) for flag in flags]


def main():
    event = get_event()
    event_name = os.environ.get("GITHUB_EVENT_NAME")
    result = {"labels": [], "text": []}
    if event and event_name in ["pull_request", "push"]:
        if event_name == "pull_request":
            labels = event.get("pull_request", {}).get("labels", [])
            text = event.get("pull_request", {}).get("title", "")
        elif event_name == "push":
            labels = []
            text = event.get("head_commit", {}).get("message", "")
        result["labels"] = flags_from_labels(labels or [])
        result["text"] = flags_from_text(text or "")
    if not result["labels"] and not result["text"]:
        result = None
    print(json.dumps(result))


if __name__ == "__main__":
    sys.exit(main())
