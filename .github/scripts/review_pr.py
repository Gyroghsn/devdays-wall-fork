"""Welcome Bot: reviews a participant's pull request and merges it when it follows the missions.

Runs on `pull_request_target`, so it NEVER executes code from the pull request.
It only reads the changed file through the GitHub API and checks it as data.
"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

from wall import EXAMPLE, QUIZ_FILE, card_path, parse_card

ROOT = Path(__file__).resolve().parents[2]
REPO = os.environ["REPO"]
PR = os.environ["PR"]
AUTHOR = os.environ["AUTHOR"]
HEAD_REPO = os.environ["HEAD_REPO"]
HEAD_SHA = os.environ["HEAD_SHA"]

OWNER, NAME = REPO.split("/")
SITE = f"https://{OWNER.lower()}.github.io/{NAME}/"
MISSIONS = f"https://github.com/{REPO}/blob/main/MISSIONS.md"

CONFLICT_HELP = f"""## 💥 Merge conflict! The boss has appeared.

Someone else's change was merged into the **same place** as yours, so Git can't decide which one to keep.
This is completely normal. Here's how to beat it:

```bash
git remote add upstream https://github.com/{REPO}.git   # only needed the first time
git fetch upstream
git merge upstream/main
```

Open the file Git complains about. You'll see something like this:

```
<<<<<<< HEAD
- @{AUTHOR}: your answer
=======
- @someone-else: their answer
>>>>>>> upstream/main
```

Keep **both** answers and delete the 3 marker lines (`<<<<<<<`, `=======`, `>>>>>>>`). Save the file, then run:

```bash
git add {QUIZ_FILE}
git commit -m "Resolve merge conflict"
git push
```

Your pull request updates itself, and I'll check it again automatically. 🤖"""


def gh(*args, check=True):
    return subprocess.run(["gh", *args], capture_output=True, text=True, check=check)


def say(body):
    gh("pr", "comment", PR, "--repo", REPO, "--body", body)


def fail(body):
    say(body)
    sys.exit(1)


def merge():
    """Squash-merge the PR (the commit is credited to the participant), then redeploy the wall."""
    for attempt in range(3):
        result = gh("pr", "merge", PR, "--repo", REPO, "--squash", check=False)
        if result.returncode == 0:
            # Merges made by the bot don't trigger `push` workflows, so start the deploy ourselves.
            gh("workflow", "run", "deploy.yml", "--repo", REPO, check=False)
            return
        mergeable = json.loads(gh("pr", "view", PR, "--repo", REPO, "--json", "mergeable").stdout)["mergeable"]
        if mergeable == "CONFLICTING":
            fail(CONFLICT_HELP)
        if mergeable != "UNKNOWN":
            break
        time.sleep(5)  # GitHub is still computing whether the PR can be merged
    fail(f"🤔 Everything looks right, but I couldn't merge automatically:\n\n```\n{result.stderr.strip()}\n```\n\n"
         "Don't worry, the trainer will merge it by hand.")


def review_card(file):
    path = file["filename"]
    raw = gh("api", "-H", "Accept: application/vnd.github.raw+json",
             f"repos/{HEAD_REPO}/contents/{path}?ref={HEAD_SHA}").stdout
    card, errors = parse_card(raw)
    if errors:
        problems = "\n".join(f"- {e}" for e in errors)
        fail(f"## 🔧 Almost there, @{AUTHOR}!\n\nI found a few problems in `{path}`:\n\n{problems}\n\n"
             f"Your file should look like this:\n\n{EXAMPLE}\n\n"
             "Fix it on your computer, then `git add`, `git commit` and `git push` again. "
             "This pull request will update itself and I'll check it again. 💪")

    is_new = file["status"] == "added"
    # The trainer's card (repository owner) doesn't count as a contributor
    cards = [p for p in (ROOT / "participants").glob("*.json") if p.stem != OWNER.lower()]
    number = len(cards) + (1 if is_new else 0)
    merge()
    if is_new:
        say(f"## 🎉 Welcome to the wall, @{AUTHOR}!\n\n"
            f"**{card['name']}** from {card['city']} is contributor **#{number}**.\n\n"
            f"I checked your pull request and merged it. Your card appears on the wall in about a minute: {SITE}\n\n"
            "**What you just did:** fork → clone → branch → commit → push → pull request → merge. "
            "That's the real open-source workflow. 🏆\n\n"
            f"Ready for more? Try the 💥 **Boss level** in [MISSIONS.md]({MISSIONS}).")
    else:
        say(f"## ✨ Card updated, @{AUTHOR}!\n\nYour changes are merged and will show on the wall in about a minute: {SITE}")


def review_quiz(file):
    added = [line[1:] for line in file.get("patch", "").splitlines()
             if line.startswith("+") and not line.startswith("+++")]
    if file["deletions"] > 0:
        fail(f"## 🛑 Careful, @{AUTHOR}!\n\nYour change **removes** lines from `{QUIZ_FILE}`. "
             "Other people's answers must stay. If you just resolved a conflict, keep **both** answers.\n\n"
             "Put the missing lines back, commit and push again.")
    if not 1 <= len(added) <= 3 or not any(f"@{AUTHOR.lower()}" in line.lower() for line in added):
        fail(f"## 🤔 Hmm, @{AUTHOR}\n\nAdd **one** line at the end of `{QUIZ_FILE}`, starting with your username:\n\n"
             f"```\n- @{AUTHOR}: your answer\n```")
    merge()
    say(f"## 🏆 Answer merged, @{AUTHOR}!\n\n"
        "If you had to resolve a merge conflict to get here: congratulations, you beat the boss level. 💥")


def main():
    if HEAD_REPO == REPO:
        return  # a branch of the main repo (the trainer's own work), not a participant's fork

    files = json.loads(gh("api", f"repos/{REPO}/pulls/{PR}/files?per_page=100").stdout)
    names = [f["filename"] for f in files]
    expected = card_path(AUTHOR)

    if names == [expected] and files[0]["status"] != "removed":
        review_card(files[0])
    elif names == [QUIZ_FILE]:
        review_quiz(files[0])
    elif len(names) == 1 and names[0].startswith("participants/"):
        fail(f"## 📛 Wrong file name, @{AUTHOR}\n\nYour card must be named after your GitHub username, in lowercase:\n\n"
             f"**`{expected}`** (yours is `{names[0]}`)\n\nRename it with:\n\n"
             f"```bash\ngit mv {names[0]} {expected}\ngit commit -m \"Rename my card\"\ngit push\n```")
    else:
        listed = "\n".join(f"- `{n}`" for n in names)
        say(f"## 🧑‍🏫 Over to the trainer\n\nThis pull request changes:\n\n{listed}\n\n"
            f"I only merge pull requests that change exactly **one** file: `{expected}` or `{QUIZ_FILE}`. "
            f"If that was a mistake, check [MISSIONS.md]({MISSIONS}). Otherwise the trainer will take a look. 👀")


if __name__ == "__main__":
    main()
