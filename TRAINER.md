# 🧑‍🏫 Trainer guide

## One-time setup (about 10 minutes)

1. **Create the repository** on GitHub: public, named `devdays-wall`, empty (no README).
   If you choose a different name or owner, replace `hadeelhs/devdays-wall` in `README.md` and `MISSIONS.md`.
2. **Push this project:**
   ```bash
   git add .
   git commit -m "Set up the Wall of Fame"
   git remote add origin https://github.com/hadeelhs/devdays-wall.git
   git push -u origin main
   ```
3. **Turn on the website:** Settings → Pages → Build and deployment → Source: **GitHub Actions**.
   Then Actions → **Deploy the wall** → **Run workflow**. The wall goes live at `https://hadeelhs.github.io/devdays-wall/`.
4. **Check the merge settings:** Settings → General → Pull Requests → **Allow squash merging** must be on.
   Don't add branch protection that requires reviews, or the bot won't be able to merge.
5. **Edit your own card** in `participants/hadeelhs.json`.

## Rehearse before the event (important!)

Use a second GitHub account, or ask a friend, to go through every mission once:

- a correct card → the bot merges it and the card appears on the wall about a minute later
- a broken card (missing comma) → the bot explains the error
- a wrongly named file → the bot asks to rename it
- two quiz answers at the same time → the second one gets the conflict explanation

## How the bot works

- `.github/workflows/welcome-bot.yml` runs on every pull request coming from a fork.
- It **auto-merges** PRs that change exactly one file:
  `participants/<author>.json` (valid card) or `quiz/answers.md` (adds a line, removes nothing).
- Anything else gets a comment and is left for you to review and merge by hand.
- It never runs code from the pull request. It only reads the changed file as data.
- After each merge it starts **Deploy the wall**, which rebuilds the site.
  The wall page refreshes on its own every 15 seconds, with confetti for each new arrival 🎊

## During the workshop

- **Projector:** keep the wall open in full screen (F11).
- **Points:** the missions table in `MISSIONS.md` gives points per level. Reward the first 3
  (🥇🥈🥉 on the wall) and whoever beats the boss level first.
- **Auth problems are the #1 time killer.** People who can't push can use **GitHub Desktop**,
  or a **Codespace** (Code → Codespaces), which needs no setup.
- **"My commits don't count on my profile":** their `user.email` doesn't match their GitHub email.
  Squash merges are credited to the PR author anyway, so the merged card still counts.

## Preview the site locally

```bash
python .github/scripts/build_wall.py    # creates participants.json
python -m http.server 8000              # then open http://localhost:8000
```

## Troubleshooting

| Problem | Fix |
|---|---|
| The bot doesn't run | Actions tab → enable workflows. Settings → Actions → General → allow all actions. |
| The bot can't comment or merge | Settings → Actions → General → Workflow permissions → **Read and write**. |
| The card doesn't appear | Actions → check that **Deploy the wall** succeeded, then wait about 1 minute (Pages cache). |
| Participant's fork is outdated | `git pull upstream main` (see the boss level in `MISSIONS.md`). |
