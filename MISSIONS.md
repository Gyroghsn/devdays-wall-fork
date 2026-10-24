# 🎮 Missions: get your card on the Wall of Fame

Complete the missions in order and collect points. When your pull request is merged, your card
appears **live** on the wall: **https://hadeelhs.github.io/devdays-wall/**

> In the commands below, replace `<you>` with **your GitHub username in lowercase**.
> Lines starting with `#` are comments: you don't need to type them.

| Mission | You learn | Points |
|---|---|---|
| 0. Get ready | `git config` | 10 |
| 1. Fork | fork | 10 |
| 2. Clone | `git clone` | 10 |
| 3. Branch | `git switch -c` | 20 |
| 4. Create your card | files and JSON | 20 |
| 5. Commit | `git status`, `git add`, `git commit` | 20 |
| 6. Push | `git push` | 20 |
| 7. Pull request | pull requests, code review | 30 |
| 💥 Boss level | merge conflicts | 50 |
| ⭐ Bonus quests | collaboration, history | +20 each |

---

## Mission 0: Get ready (10 pts)

Check that Git is installed:

```bash
git --version
```

Tell Git who you are. **Use the same email as your GitHub account**, otherwise your commits
won't show up on your GitHub profile:

```bash
git config --global user.name "Your Name"
git config --global user.email "the-email-of-your-github-account@example.com"
```

> 💡 No Git on your laptop? Open this repository on GitHub, then click **Code → Codespaces → Create codespace**.
> You get a ready-to-use editor and terminal in your browser.

## Mission 1: Fork (10 pts)

Click the **Fork** button at the top right of this page, then **Create fork**.

You now have **your own copy** of the project at `github.com/<you>/devdays-wall`.
You can change it however you like without touching the original.

## Mission 2: Clone (10 pts)

Download **your fork** to your computer:

```bash
git clone https://github.com/<you>/devdays-wall.git
cd devdays-wall
```

## Mission 3: Branch (20 pts)

A branch is a parallel version of the project where you can work safely.

```bash
git switch -c add-<you>
git branch          # the * shows the branch you're on
```

## Mission 4: Create your card (20 pts)

Create the file `participants/<you>.json`. The name must be **exactly your GitHub username, in lowercase**.
Copy this and make it yours:

```json
{
  "name": "Sarah",
  "city": "Sfax",
  "fun_fact": "I once fixed a bug by deleting a semicolon"
}
```

Rules: keep the 3 fields, use double quotes `"`, put a comma after every line except the last one.
`fun_fact` can be up to 140 characters.

## Mission 5: Commit (20 pts)

A commit is a snapshot of your work, with a message explaining what changed.

```bash
git status                                # your file is shown in red: Git sees it but won't save it yet
git add participants/<you>.json
git status                                # now it's green: ready to be committed
git commit -m "Add <you> to the wall"
git log --oneline                         # your commit is on top of the history
```

## Mission 6: Push (20 pts)

Send your branch to your fork on GitHub:

```bash
git push -u origin add-<you>
```

## Mission 7: Pull request (30 pts)

1. Go to your fork on GitHub. A yellow banner shows up: click **Compare & pull request**.
2. Give it a title like `Add <you> to the wall` and click **Create pull request**.
3. Wait a few seconds for the 🤖 **Welcome Bot** to check your card:
   - ✅ **Everything is OK:** it merges your PR. Look at the projector!
   - 🔧 **Something is wrong:** read its comment, fix the file on your computer, then
     `git add`, `git commit` and `git push` again. **Your pull request updates itself.**

🎉 **Your card is on the wall!** You've just done the real open-source workflow:
**fork → clone → branch → commit → push → pull request → merge.**

---

## 💥 Boss level: the merge conflict (50 pts)

Everyone will now add a line **in the same place** in the same file. Git won't know which change to keep. 😈

**1. Get the latest version of the original project.** Your fork doesn't update by itself!

```bash
git switch main
git remote add upstream https://github.com/hadeelhs/devdays-wall.git
git pull upstream main
```

**2. Create a new branch:**

```bash
git switch -c quiz-<you>
```

**3. Answer the question** in `quiz/answers.md` by adding **one line at the very end** of the file:

```
- @<you>: your answer
```

**4. Commit, push and open a pull request,** just like in missions 5 to 7:

```bash
git add quiz/answers.md
git commit -m "Add my quiz answer"
git push -u origin quiz-<you>
```

**5. Did someone else's answer get merged before yours?** The bot will announce a **merge conflict**
and explain how to fix it. Resolve it, push again, and the boss is defeated. 🏆

---

## ⭐ Bonus quests (+20 pts each)

- **👯 Pair programming:** make your boss level commit with a neighbor. Add this as the last line of the
  commit message to credit them:
  ```
  Co-authored-by: Their Name <their-github-email>
  ```
  Use `git commit` without `-m` to write a message on several lines.
- **🕵️ Detective:** find out who added the first answer to the quiz, and when:
  `git log --reverse quiz/answers.md` and `git blame quiz/answers.md`
- **🌳 Time traveler:** draw the history as a tree: `git log --oneline --graph --all`
- **✏️ Update your card:** change your fun fact on a new branch and open a second pull request.

> 🏅 **GitHub achievements:** with 2 merged pull requests, GitHub can award you the **Pull Shark** badge
> on your profile. A merged co-authored commit can earn **Pair Extraordinaire**.

---

## 📜 Cheat sheet

| Command | What it does |
|---|---|
| `git clone <url>` | Download a repository |
| `git status` | Show what changed |
| `git add <file>` | Prepare a file for the next commit |
| `git commit -m "msg"` | Save a snapshot |
| `git log --oneline` | Show the history |
| `git switch -c <name>` | Create a branch and move to it |
| `git switch <name>` | Move to an existing branch |
| `git push` | Send your commits to GitHub |
| `git pull` | Get the latest commits from GitHub |
| `git remote -v` | Show the GitHub addresses your repo is connected to |
