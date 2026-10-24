(() => {
  const claims = (window.CLAIMS || []).slice();
  const $ = (id) => document.getElementById(id);
  const state = { q: "", verdict: null, tag: null, sort: "new" };

  const esc = (s = "") => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
  const dateKey = (c) => (c.date || "").replace("~", "");
  const fmtDate = (d) => {
    if (!d) return "Date unknown";
    const approx = d.startsWith("~");
    const parsed = new Date(d.replace("~", ""));
    const out = isNaN(parsed) ? d : parsed.toLocaleDateString("en-KE", { day: "numeric", month: "short", year: "numeric" });
    return approx ? `c. ${out}` : out;
  };

  function chips(el, values, key) {
    el.innerHTML = "";
    [null, ...values].forEach((v) => {
      const b = document.createElement("button");
      b.className = "chip";
      b.textContent = v ?? (key === "verdict" ? "All verdicts" : "All topics");
      b.setAttribute("aria-pressed", String(state[key] === v));
      b.onclick = () => { state[key] = v; chips(el, values, key); render(); };
      el.appendChild(b);
    });
  }

  function matches(c) {
    if (state.verdict && c.verdict !== state.verdict) return false;
    if (state.tag && !(c.tags || []).includes(state.tag)) return false;
    if (!state.q) return true;
    const hay = [c.title, c.quote, c.context, c.reality, ...(c.tags || [])].join(" ").toLowerCase();
    return state.q.split(/\s+/).every((w) => hay.includes(w));
  }

  function card(c) {
    const li = document.createElement("li");
    li.className = "card";
    li.tabIndex = 0;
    const img = c.thumbnail
      ? `<img src="${esc(c.thumbnail)}" alt="" loading="lazy" onerror="this.remove()">`
      : "";
    li.innerHTML = `
      <div class="thumb ${c.tweet_url ? "" : "no-video"}">
        <div class="fallback">${esc(c.quote).slice(0, 140)}${(c.quote || "").length > 140 ? "…" : ""}</div>
        ${img}
        <span class="badge" data-v="${esc(c.verdict)}">${esc(c.verdict)}</span>
        <span class="play" aria-hidden="true"></span>
      </div>
      <div class="body">
        <h2>${esc(c.title)}</h2>
        <p class="meta">${fmtDate(c.date)}${c.context ? " · " + esc(c.context) : ""}</p>
      </div>`;
    li.onclick = () => open(c);
    li.onkeydown = (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); open(c); } };
    return li;
  }

  function render() {
    const list = claims.filter(matches).sort((a, b) =>
      state.sort === "new" ? dateKey(b).localeCompare(dateKey(a)) : dateKey(a).localeCompare(dateKey(b)));
    const grid = $("grid");
    grid.replaceChildren(...list.map(card));
    $("empty").hidden = list.length > 0;
    $("count").textContent = `${list.length} of ${claims.length} clips`;
  }

  // Load X's embed script only when someone opens a clip.
  let widgets;
  const loadWidgets = () => widgets ??= new Promise((res) => {
    const s = document.createElement("script");
    s.src = "https://platform.twitter.com/widgets.js";
    s.async = true;
    s.onload = () => res(window.twttr);
    s.onerror = () => res(null);
    document.head.appendChild(s);
  });

  async function open(c) {
    const v = $("v-verdict");
    v.textContent = c.verdict;
    v.dataset.v = c.verdict;
    $("v-title").textContent = c.title;
    $("v-meta").textContent = [fmtDate(c.date), c.context].filter(Boolean).join(" · ");
    $("v-quote").textContent = `“${c.quote}”`;
    $("v-reality").textContent = c.reality;
    $("v-check").href = c.factcheck_url;
    const tw = $("v-tweet");
    tw.hidden = !c.tweet_url;
    if (c.tweet_url) tw.href = c.tweet_url;
    const note = $("v-clipnote");
    note.hidden = !c.clip_note;
    note.textContent = c.clip_note ? `About this video: ${c.clip_note}` : "";

    const embed = $("v-embed");
    embed.innerHTML = "";
    $("viewer").showModal();
    if (!c.tweet_url) return;

    const id = (c.tweet_url.match(/status\/(\d+)/) || [])[1];
    const twttr = await loadWidgets();
    if (twttr && id) {
      const dark = matchMedia("(prefers-color-scheme: dark)").matches;
      const el = await twttr.widgets.createTweet(id, embed, { theme: dark ? "dark" : "light", align: "center", dnt: true });
      if (el) return;
    }
    embed.innerHTML = `<p class="meta">Couldn't load the embed (blocked or deleted). <a href="${esc(c.tweet_url)}" target="_blank" rel="noopener">Watch on X ↗</a></p>`;
  }

  const dlg = $("viewer");
  dlg.querySelector(".close").onclick = () => dlg.close();
  dlg.addEventListener("click", (e) => { if (e.target === dlg) dlg.close(); });
  dlg.addEventListener("close", () => { $("v-embed").innerHTML = ""; });

  $("search").addEventListener("input", (e) => { state.q = e.target.value.trim().toLowerCase(); render(); });
  $("sort").addEventListener("change", (e) => { state.sort = e.target.value; render(); });

  const verdicts = ["False", "Misleading", "Broken promise", "Unproven"].filter((v) => claims.some((c) => c.verdict === v));
  const tags = [...new Set(claims.flatMap((c) => c.tags || []))].sort();
  chips($("verdicts"), verdicts, "verdict");
  chips($("tags"), tags, "tag");
  render();
})();
