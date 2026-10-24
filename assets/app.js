// Polls participants.json and adds new cards to the wall as pull requests get merged.
const POLL_MS = 15000;
const MEDALS = ["🥇", "🥈", "🥉"];

const wall = document.getElementById("wall");
const empty = document.getElementById("empty");
const count = document.getElementById("count");
const latest = document.getElementById("latest");
const toast = document.getElementById("toast");

const seen = new Set();
let firstLoad = true;
let toastTimer;

// On GitHub Pages the URL is https://<owner>.github.io/<repo>/
function repoUrl() {
  const owner = location.hostname.endsWith(".github.io") ? location.hostname.split(".")[0] : null;
  const repo = location.pathname.split("/").filter(Boolean)[0];
  return owner && repo ? `https://github.com/${owner}/${repo}` : null;
}

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text; // textContent: participant text is never treated as HTML
  return node;
}

function buildCard(p, index) {
  const card = el("li", "card");

  const rank = el("span", index < 3 ? "rank medal" : "rank", index < 3 ? MEDALS[index] : `#${index + 1}`);
  rank.title = `Contributor #${index + 1}`;

  const avatarWrap = el("div", "avatar-wrap");
  const avatar = el("img", "avatar");
  avatar.src = `https://github.com/${encodeURIComponent(p.username)}.png?size=168`;
  avatar.alt = "";
  avatar.loading = "lazy";
  avatar.onerror = () => { avatar.style.visibility = "hidden"; };
  avatarWrap.append(avatar, el("span", "emoji", p.emoji));

  const username = el("a", "username", `@${p.username}`);
  username.href = `https://github.com/${encodeURIComponent(p.username)}`;
  username.target = "_blank";
  username.rel = "noopener";

  card.append(rank, avatarWrap, el("h2", "name", p.name), username,
    el("p", "city", `📍 ${p.city}`), el("p", "fact", p.fun_fact));
  return card;
}

function celebrate(p) {
  toast.textContent = `🎉 ${p.name} just joined the wall!`;
  toast.classList.add("show");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove("show"), 4000);
  if (window.confetti && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
    confetti({ particleCount: 140, spread: 80, origin: { y: 0.7 } });
  }
}

async function load() {
  let participants;
  try {
    const res = await fetch(`participants.json?t=${Date.now()}`, { cache: "no-store" });
    if (!res.ok) throw new Error(res.status);
    participants = (await res.json()).participants;
  } catch {
    if (firstLoad) empty.hidden = false;
    firstLoad = false;
    return;
  }

  participants.forEach((p, index) => {
    if (seen.has(p.username)) return;
    seen.add(p.username);
    const card = buildCard(p, index);
    wall.prepend(card); // newest first, so new arrivals show up at the top of the projector
    if (!firstLoad) {
      card.classList.add("new");
      celebrate(p);
    }
  });

  empty.hidden = participants.length > 0;
  count.textContent = participants.length;
  latest.textContent = participants.length ? participants[participants.length - 1].name : "—";
  firstLoad = false;
}

const url = repoUrl();
if (url) document.getElementById("join").href = `${url}/blob/main/MISSIONS.md`;

load();
setInterval(load, POLL_MS);
