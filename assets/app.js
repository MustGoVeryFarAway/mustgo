(() => {
  const claims = (window.CLAIMS || []).slice();
  const $ = (id) => document.getElementById(id);
  const state = { q: "", verdict: null, tag: null, sort: "new" };
  let currentClaim = null;
  let currentFilteredList = [];

  const esc = (s = "") => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
  const dateKey = (c) => (c.date || "").replace("~", "");
  const fmtDate = (d) => {
    if (!d) return "Date unknown";
    const approx = d.startsWith("~");
    const parsed = new Date(d.replace("~", ""));
    const out = isNaN(parsed) ? d : parsed.toLocaleDateString("en-KE", { day: "numeric", month: "short", year: "numeric" });
    return approx ? `c. ${out}` : out;
  };

  function showToast(msg, ms = 2500) {
    const t = $("toast");
    if (!t) return;
    t.textContent = msg;
    t.hidden = false;
    clearTimeout(t._timer);
    t._timer = setTimeout(() => { t.hidden = true; }, ms);
  }

  // --- Scorecard / Truth Meter ---
  function initScorecard() {
    const total = claims.length;
    if (!total) return;

    const verdictOrder = ["False", "Misleading", "Broken promise", "Unproven"];
    const counts = {};
    verdictOrder.forEach((v) => { counts[v] = 0; });
    claims.forEach((c) => {
      counts[c.verdict] = (counts[c.verdict] || 0) + 1;
    });

    const debunked = (counts["False"] || 0) + (counts["Misleading"] || 0);
    const debunkedPct = Math.round((debunked / total) * 100);

    const summaryEl = $("sc-summary");
    if (summaryEl) {
      summaryEl.textContent = `${total} Statements · ${debunkedPct}% Debunked (False + Misleading)`;
    }

    const barEl = $("sc-bar");
    if (barEl) {
      barEl.innerHTML = "";
      verdictOrder.forEach((v) => {
        const count = counts[v] || 0;
        if (!count) return;
        const pct = ((count / total) * 100).toFixed(1);
        const seg = document.createElement("div");
        seg.className = "score-seg";
        seg.dataset.v = v;
        seg.style.width = `${pct}%`;
        seg.title = `${v}: ${count} (${pct}%) - Click to filter`;
        seg.onclick = () => {
          state.verdict = state.verdict === v ? null : v;
          updateChipSelection();
          render();
        };
        barEl.appendChild(seg);
      });
    }

    const pillsEl = $("sc-pills");
    if (pillsEl) {
      pillsEl.innerHTML = "";
      verdictOrder.forEach((v) => {
        const count = counts[v] || 0;
        if (!count) return;
        const pct = Math.round((count / total) * 100);
        const pill = document.createElement("button");
        pill.type = "button";
        pill.className = "score-pill";
        pill.dataset.v = v;
        pill.setAttribute("aria-pressed", String(state.verdict === v));
        pill.innerHTML = `<span class="dot"></span><span>${v}</span> <strong>${count}</strong> <span class="meta">(${pct}%)</span>`;
        pill.onclick = () => {
          state.verdict = state.verdict === v ? null : v;
          updateChipSelection();
          render();
        };
        pillsEl.appendChild(pill);
      });
    }
  }

  function updateScorecardPills() {
    document.querySelectorAll(".score-pill").forEach((pill) => {
      pill.setAttribute("aria-pressed", String(state.verdict === pill.dataset.v));
    });
  }

  // --- Chips & Filters ---
  function getTagCounts() {
    const counts = {};
    claims.forEach((c) => {
      (c.tags || []).forEach((t) => { counts[t] = (counts[t] || 0) + 1; });
    });
    return counts;
  }

  function getVerdictCounts() {
    const counts = {};
    claims.forEach((c) => {
      counts[c.verdict] = (counts[c.verdict] || 0) + 1;
    });
    return counts;
  }

  function renderChips() {
    const verdictCounts = getVerdictCounts();
    const verdicts = ["False", "Misleading", "Broken promise", "Unproven"].filter((v) => verdictCounts[v]);
    const vEl = $("verdicts");
    vEl.innerHTML = "";
    [null, ...verdicts].forEach((v) => {
      const b = document.createElement("button");
      b.className = "chip";
      b.dataset.val = v || "";
      const label = v ? `${v} <span class="chip-count">(${verdictCounts[v]})</span>` : `All verdicts <span class="chip-count">(${claims.length})</span>`;
      b.innerHTML = label;
      b.setAttribute("aria-pressed", String(state.verdict === v));
      b.onclick = () => {
        state.verdict = v;
        updateChipSelection();
        render();
      };
      vEl.appendChild(b);
    });

    const tagCounts = getTagCounts();
    const tags = Object.keys(tagCounts).sort();
    const tEl = $("tags");
    tEl.innerHTML = "";
    [null, ...tags].forEach((t) => {
      const b = document.createElement("button");
      b.className = "chip";
      b.dataset.val = t || "";
      const label = t ? `#${t} <span class="chip-count">(${tagCounts[t]})</span>` : `All topics <span class="chip-count">(${claims.length})</span>`;
      b.innerHTML = label;
      b.setAttribute("aria-pressed", String(state.tag === t));
      b.onclick = () => {
        state.tag = t;
        updateChipSelection();
        render();
      };
      tEl.appendChild(b);
    });
  }

  function updateChipSelection() {
    document.querySelectorAll("#verdicts .chip").forEach((b) => {
      b.setAttribute("aria-pressed", String(state.verdict === (b.dataset.val || null)));
    });
    document.querySelectorAll("#tags .chip").forEach((b) => {
      b.setAttribute("aria-pressed", String(state.tag === (b.dataset.val || null)));
    });
    updateScorecardPills();
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
    const hasVideo = Boolean(c.tweet_url);
    const videoTag = hasVideo
      ? `<span class="video-status-tag">▶ Video Clip</span>`
      : `<span class="video-status-tag">📜 Record</span>`;

    const tagPills = (c.tags || []).slice(0, 3).map((t) => `<span class="tag-pill">#${esc(t)}</span>`).join("");

    li.innerHTML = `
      <div class="thumb ${hasVideo ? "" : "no-video"}">
        <div class="fallback">${esc(c.quote).slice(0, 130)}${(c.quote || "").length > 130 ? "…" : ""}</div>
        ${img}
        <span class="badge" data-v="${esc(c.verdict)}">${esc(c.verdict)}</span>
        <span class="play" aria-hidden="true"></span>
        ${videoTag}
      </div>
      <div class="body">
        <h2>${esc(c.title)}</h2>
        <p class="meta">${fmtDate(c.date)}${c.context ? " · " + esc(c.context) : ""}</p>
        <div class="tags-list">${tagPills}</div>
      </div>`;
    li.onclick = () => open(c);
    li.onkeydown = (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); open(c); } };
    return li;
  }

  function resetAllFilters() {
    state.q = "";
    state.verdict = null;
    state.tag = null;
    const searchInput = $("search");
    if (searchInput) searchInput.value = "";
    $("clear-search").hidden = true;
    updateChipSelection();
    render();
  }

  function render() {
    currentFilteredList = claims.filter(matches).sort((a, b) =>
      state.sort === "new" ? dateKey(b).localeCompare(dateKey(a)) : dateKey(a).localeCompare(dateKey(b)));
    const grid = $("grid");
    grid.replaceChildren(...currentFilteredList.map(card));
    $("empty").hidden = currentFilteredList.length > 0;
    $("count").textContent = `${currentFilteredList.length} of ${claims.length} receipts`;

    const isFiltered = Boolean(state.q || state.verdict || state.tag);
    $("reset-filters").hidden = !isFiltered;
    updateScorecardPills();
  }

  // Load X's embed script on demand
  let widgets;
  const loadWidgets = () => widgets ??= new Promise((res) => {
    const s = document.createElement("script");
    s.src = "https://platform.twitter.com/widgets.js";
    s.async = true;
    s.onload = () => res(window.twttr);
    s.onerror = () => res(null);
    document.head.appendChild(s);
  });

  // --- Viewer & Deep Linking ---
  async function open(c, updateHash = true) {
    if (!c) return;
    currentClaim = c;

    if (updateHash && window.location.hash !== `#${c.id}`) {
      history.pushState(null, "", `#${c.id}`);
    }

    const v = $("v-verdict");
    v.textContent = c.verdict;
    v.dataset.v = c.verdict;

    $("v-id").textContent = `#${c.id}`;
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
    note.textContent = c.clip_note ? `About this clip: ${c.clip_note}` : "";

    // Position indicator in viewer
    const idx = currentFilteredList.findIndex((item) => item.id === c.id);
    if (idx !== -1) {
      $("v-position").textContent = `${idx + 1} of ${currentFilteredList.length}`;
      $("v-prev").disabled = idx === 0;
      $("v-next").disabled = idx === currentFilteredList.length - 1;
    } else {
      $("v-position").textContent = "";
    }

    const embed = $("v-embed");
    embed.innerHTML = "";

    const viewer = $("viewer");
    if (!viewer.open) viewer.showModal();

    if (!c.tweet_url) {
      embed.innerHTML = `
        <div class="no-video-plaque">
          <div class="plaque-icon">📜</div>
          <div class="plaque-body">
            <span class="plaque-label">Official Press / Speech Record</span>
            <p class="plaque-context">This statement was documented in official public broadcasts or press reporting. An isolated video clip has not yet been attached.</p>
            <p class="plaque-help">Have a direct video link of this moment? <a href="javascript:void(0)" id="plaque-submit-link">Submit the clip URL ↗</a></p>
          </div>
        </div>`;
      const subLink = $("plaque-submit-link");
      if (subLink) {
        subLink.onclick = () => {
          viewer.close();
          openSubmitModalWithClaim(c);
        };
      }
      return;
    }

    const id = (c.tweet_url.match(/status\/(\d+)/) || [])[1];
    embed.innerHTML = `<div class="meta" style="padding:16px 0; text-align:center;">Loading video player...</div>`;
    const twttr = await loadWidgets();
    if (twttr && id) {
      embed.innerHTML = "";
      const dark = matchMedia("(prefers-color-scheme: dark)").matches;
      const el = await twttr.widgets.createTweet(id, embed, { theme: dark ? "dark" : "light", align: "center", dnt: true });
      if (el) return;
    }
    embed.innerHTML = `
      <div class="no-video-plaque">
        <div class="plaque-icon">▶️</div>
        <div class="plaque-body">
          <span class="plaque-label">Video Clip on X</span>
          <p class="plaque-context">The embedded player could not load (it may be blocked by ad blockers or privacy shields).</p>
          <p class="plaque-help"><a href="${esc(c.tweet_url)}" target="_blank" rel="noopener">Watch the video directly on X ↗</a></p>
        </div>
      </div>`;
  }

  function handleHashChange() {
    const hash = window.location.hash.slice(1);
    if (!hash) {
      const viewer = $("viewer");
      if (viewer && viewer.open) viewer.close();
      return;
    }
    const found = claims.find((c) => c.id === hash);
    if (found) {
      open(found, false);
    }
  }

  // Previous & Next Navigation
  function navigateViewer(offset) {
    if (!currentClaim || !currentFilteredList.length) return;
    const idx = currentFilteredList.findIndex((item) => item.id === currentClaim.id);
    if (idx === -1) return;
    const targetIdx = idx + offset;
    if (targetIdx >= 0 && targetIdx < currentFilteredList.length) {
      open(currentFilteredList[targetIdx]);
    }
  }

  // --- Sharing Functions ---
  function getShareUrl(c) {
    const origin = window.location.origin === "null" || !window.location.origin ? "https://mustgo.co.ke" : window.location.origin;
    return `${origin}${window.location.pathname}#${c.id}`;
  }

  function shareWhatsApp(c) {
    const url = getShareUrl(c);
    const text = `🚨 *MustGo.co.ke Receipt*\n\n"${c.quote}"\n\n*Verdict:* ${c.verdict.toUpperCase()}\n*The Record:* ${c.reality}\n\n👉 See full video and fact-check:\n${url}`;
    window.open(`https://api.whatsapp.com/send?text=${encodeURIComponent(text)}`, "_blank");
  }

  function shareX(c) {
    const url = getShareUrl(c);
    const quoteShort = c.quote.length > 90 ? c.quote.slice(0, 87) + "..." : c.quote;
    const text = `"${quoteShort}"\n\nVerdict: ${c.verdict.toUpperCase()}\nRecord: ${c.reality.slice(0, 80)}...\n\nReceipt via mustgo.co.ke:\n${url}`;
    window.open(`https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}`, "_blank");
  }

  function copyClaimLink(c) {
    const url = getShareUrl(c);
    navigator.clipboard.writeText(url).then(() => {
      const textEl = $("copy-text");
      if (textEl) textEl.textContent = "✓ Copied!";
      showToast("Direct link copied to clipboard!");
      setTimeout(() => {
        if (textEl) textEl.textContent = "Copy Link";
      }, 2000);
    }).catch(() => {
      prompt("Copy link:", url);
    });
  }

  // --- Downloadable Receipt Slip Generator (Canvas) ---
  function wrapText(ctx, text, x, y, maxWidth, lineHeight) {
    const words = text.split(" ");
    let line = "";
    let curY = y;
    for (let n = 0; n < words.length; n++) {
      const testLine = line + words[n] + " ";
      const metrics = ctx.measureText(testLine);
      if (metrics.width > maxWidth && n > 0) {
        ctx.fillText(line, x, curY);
        line = words[n] + " ";
        curY += lineHeight;
      } else {
        line = testLine;
      }
    }
    ctx.fillText(line, x, curY);
    return curY + lineHeight;
  }

  function generateReceiptSlip(c) {
    const btn = $("btn-download-slip");
    const label = $("download-text");
    if (label) label.textContent = "Generating...";

    // 1080 x 1440 (Standard 3:4 / portrait card for WhatsApp & Instagram)
    const canvas = document.createElement("canvas");
    canvas.width = 1080;
    canvas.height = 1440;
    const ctx = canvas.getContext("2d");

    // Background: Crisp warm paper
    ctx.fillStyle = "#faf8f5";
    ctx.fillRect(0, 0, 1080, 1440);

    // Kenyan Flag accent stripe across the very top
    ctx.fillStyle = "#000000";
    ctx.fillRect(0, 0, 360, 20);
    ctx.fillStyle = "#bb1e1e";
    ctx.fillRect(360, 0, 360, 20);
    ctx.fillStyle = "#0f6b3a";
    ctx.fillRect(720, 0, 360, 20);

    // Outer receipt border with stitch dots
    ctx.strokeStyle = "#e2ddd4";
    ctx.lineWidth = 4;
    ctx.strokeRect(40, 50, 1000, 1340);

    // Top Header: MUSTGO.CO.KE
    ctx.fillStyle = "#141414";
    ctx.font = "bold 52px 'Archivo Black', Impact, sans-serif";
    ctx.fillText("MUSTGO.CO.KE", 80, 130);

    ctx.fillStyle = "#5d5a55";
    ctx.font = "bold 20px 'JetBrains Mono', monospace";
    ctx.fillText("KENYA PUBLIC ACCOUNTABILITY ARCHIVE", 80, 168);

    // Metadata line
    ctx.font = "500 22px Inter, sans-serif";
    const metaStr = `DATE: ${fmtDate(c.date).toUpperCase()}   |   ID: #${c.id.toUpperCase()}`;
    ctx.fillText(metaStr, 80, 220);

    // Perforated line
    ctx.setLineDash([12, 10]);
    ctx.strokeStyle = "#c8c3ba";
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(80, 250);
    ctx.lineTo(1000, 250);
    ctx.stroke();
    ctx.setLineDash([]);

    // SECTION 1: THE CLAIM / QUOTE
    ctx.fillStyle = "#bb1e1e";
    ctx.font = "bold 22px 'JetBrains Mono', monospace";
    ctx.fillText("WHAT WAS CLAIMED:", 80, 310);

    ctx.fillStyle = "#141414";
    ctx.font = "italic 38px Georgia, serif";
    const quoteY = wrapText(ctx, `“${c.quote}”`, 80, 365, 920, 52);

    // Context
    let curY = quoteY + 20;
    if (c.context) {
      ctx.fillStyle = "#5d5a55";
      ctx.font = "500 22px Inter, sans-serif";
      curY = wrapText(ctx, `Context: ${c.context}`, 80, curY, 920, 30);
    }

    curY += 20;

    // VERDICT STAMP BADGE
    let stampColor = "#4f5b66";
    if (c.verdict === "False") stampColor = "#bb1e1e";
    else if (c.verdict === "Misleading") stampColor = "#c46a00";
    else if (c.verdict === "Broken promise") stampColor = "#6b2fa3";

    ctx.fillStyle = stampColor;
    ctx.beginPath();
    ctx.roundRect(80, curY, 340, 64, 8);
    ctx.fill();

    ctx.fillStyle = "#ffffff";
    ctx.font = "bold 30px 'Archivo Black', Impact, sans-serif";
    ctx.fillText(`VERDICT: ${c.verdict.toUpperCase()}`, 105, curY + 44);

    curY += 105;

    // SECTION 2: THE PUBLIC RECORD
    ctx.fillStyle = "#0f6b3a";
    ctx.font = "bold 22px 'JetBrains Mono', monospace";
    ctx.fillText("WHAT THE RECORD SHOWS:", 80, curY);
    curY += 45;

    ctx.fillStyle = "#141414";
    ctx.font = "500 28px Inter, sans-serif";
    curY = wrapText(ctx, c.reality, 80, curY, 920, 42);

    // Source link note
    curY += 30;
    ctx.fillStyle = "#5d5a55";
    ctx.font = "600 20px 'JetBrains Mono', monospace";
    ctx.fillText("SOURCE: INDEPENDENT FACT-CHECK & PUBLIC RECORD", 80, curY);

    // Decorative Barcode at the bottom
    const barcodeY = 1260;
    ctx.fillStyle = "#141414";
    // Draw procedural barcode stripes
    let bx = 80;
    const barWidths = [3, 8, 4, 12, 3, 6, 14, 4, 8, 3, 10, 4, 16, 3, 6, 10, 4, 14, 6, 8, 3, 12, 4, 8, 3, 14, 4, 6, 12, 4, 8, 14, 3, 8, 6, 10, 4, 12, 4, 8, 14, 3, 10];
    barWidths.forEach((w) => {
      ctx.fillRect(bx, barcodeY, w, 60);
      bx += w + 8;
    });

    // Bottom slogan
    ctx.fillStyle = "#5d5a55";
    ctx.font = "bold 20px 'JetBrains Mono', monospace";
    ctx.fillText(`mustgo.co.ke/#${c.id}   ·   THE INTERNET NEVER FORGETS`, 80, 1360);

    // Export image
    canvas.toBlob((blob) => {
      if (!blob) {
        if (label) label.textContent = "Download Receipt";
        return;
      }
      const fileUrl = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = fileUrl;
      a.download = `mustgo-receipt-${c.id}.png`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(fileUrl);

      if (label) label.textContent = "✓ Downloaded!";
      showToast("Receipt card downloaded!");
      setTimeout(() => {
        if (label) label.textContent = "Download Receipt";
      }, 2500);
    }, "image/png");
  }

  // --- Submit Modal Handling ---
  function openSubmitModalWithClaim(c = null) {
    const sub = $("submit-dialog");
    if (!sub) return;
    if (c) {
      $("sub-headline").value = `Video Clip for: ${c.title}`;
      $("sub-quote").value = c.quote;
      $("sub-date").value = (c.date || "").replace("~", "");
      $("sub-context").value = c.context || "";
      $("sub-factcheck").value = c.factcheck_url || "";
    }
    sub.showModal();
  }

  function handleFormSubmit(e) {
    e.preventDefault();
    const title = $("sub-headline").value.trim();
    const quote = $("sub-quote").value.trim();
    const date = $("sub-date").value.trim();
    const context = $("sub-context").value.trim();
    const video = $("sub-video").value.trim();
    const factcheck = $("sub-factcheck").value.trim();

    const body = [
      `### Receipt Submission for mustgo.co.ke`,
      ``,
      `**Title:** ${title}`,
      `**Quote:** ${quote}`,
      `**Date:** ${date}`,
      `**Context:** ${context || "N/A"}`,
      `**Video URL:** ${video || "N/A"}`,
      `**Fact-Check / Record URL:** ${factcheck}`,
    ].join("\n");

    const issueUrl = `https://github.com/trucktar/ruto-receipts/issues/new?title=${encodeURIComponent(`Receipt: ${title}`)}&body=${encodeURIComponent(body)}`;
    window.open(issueUrl, "_blank");
    showToast("Opened submission in GitHub Issues!");
    $("submit-dialog").close();
  }

  function copySubmissionText() {
    const title = $("sub-headline").value.trim();
    const quote = $("sub-quote").value.trim();
    const date = $("sub-date").value.trim();
    const context = $("sub-context").value.trim();
    const video = $("sub-video").value.trim();
    const factcheck = $("sub-factcheck").value.trim();

    const text = `MUSTGO RECEIPT SUBMISSION\nTitle: ${title}\nQuote: "${quote}"\nDate: ${date}\nContext: ${context}\nVideo: ${video}\nFact-check: ${factcheck}`;
    navigator.clipboard.writeText(text).then(() => {
      showToast("Submission text copied to clipboard!");
    });
  }

  // --- Setup Event Listeners ---
  function initEvents() {
    const viewer = $("viewer");
    viewer.querySelector(".close").onclick = () => {
      viewer.close();
      if (window.location.hash) {
        history.pushState(null, "", window.location.pathname + window.location.search);
      }
    };
    viewer.addEventListener("click", (e) => {
      if (e.target === viewer) {
        viewer.close();
        if (window.location.hash) {
          history.pushState(null, "", window.location.pathname + window.location.search);
        }
      }
    });
    viewer.addEventListener("close", () => {
      $("v-embed").innerHTML = "";
      currentClaim = null;
    });

    // Navigation buttons in viewer
    $("v-prev").onclick = () => navigateViewer(-1);
    $("v-next").onclick = () => navigateViewer(1);

    // Keyboard shortcuts in viewer
    window.addEventListener("keydown", (e) => {
      if (!viewer.open) return;
      if (e.key === "ArrowLeft") navigateViewer(-1);
      if (e.key === "ArrowRight") navigateViewer(1);
    });

    // Share buttons in viewer
    $("btn-share-wa").onclick = () => currentClaim && shareWhatsApp(currentClaim);
    $("btn-share-x").onclick = () => currentClaim && shareX(currentClaim);
    $("btn-copy-link").onclick = () => currentClaim && copyClaimLink(currentClaim);
    $("btn-download-slip").onclick = () => currentClaim && generateReceiptSlip(currentClaim);

    // Search events
    const searchInput = $("search");
    const clearBtn = $("clear-search");
    searchInput.addEventListener("input", (e) => {
      state.q = e.target.value.trim().toLowerCase();
      clearBtn.hidden = !state.q;
      render();
    });
    clearBtn.onclick = () => {
      searchInput.value = "";
      state.q = "";
      clearBtn.hidden = true;
      searchInput.focus();
      render();
    };

    $("sort").addEventListener("change", (e) => {
      state.sort = e.target.value;
      render();
    });

    $("reset-filters").onclick = resetAllFilters;
    $("empty-reset-btn").onclick = resetAllFilters;

    // Submit dialog events
    const submitDialog = $("submit-dialog");
    $("open-submit").onclick = () => submitDialog.showModal();
    submitDialog.querySelector(".close").onclick = () => submitDialog.close();
    submitDialog.addEventListener("click", (e) => {
      if (e.target === submitDialog) submitDialog.close();
    });
    $("submit-form").addEventListener("submit", handleFormSubmit);
    $("btn-copy-submission").onclick = copySubmissionText;

    const footSubmitLink = $("foot-submit-link");
    if (footSubmitLink) {
      footSubmitLink.onclick = (e) => {
        e.preventDefault();
        submitDialog.showModal();
      };
    }

    // Hash routing
    window.addEventListener("hashchange", handleHashChange);
  }

  // --- Initial Launch ---
  initScorecard();
  renderChips();
  render();
  initEvents();
  handleHashChange();
})();
