<a id="top"></a>

[README](../README.md) | [Members](../MEMBERS.md) | [Plan](../PLAN.md) | [Design](../DESIGN.md) | [Sprint1](../Sprint1/README.md) | [Sprint2](../Sprint2/README.md) | [Sprint3](../Sprint3/README.md) | [Sprint4](README.md) | [Changelog](../CHANGELOG.md) | [Review](../SPRINT_REVIEW.md) | [Peer Eval](../PEER_EVALUATION.md) | [AI Log S1](../Sprint1/LEARNINGLOG.md) | [AI Log S2](../Sprint2/LEARNINGLOG.md) | [AI Log S3](../Sprint3/LEARNINGLOG.md)

# ประวัติการใช้ AI - Sprint 4 (AI Usage Log)

โปรเจกต์: Recipe Roulette (TheMealDB) | ช่วงงาน: 05/10/2569 | ทีมตาม Sprint4/README: Ter Planner / Khong Coder (wheel+shopping) / Benz Coder (tabs/filter) / Toey Debugger (tests)

## หมายเหตุด้านความถูกต้อง

- โค้ดตรงกับไฟล์งานปัจจุบัน (uncommitted, ตรวจด้วย node --check + pytest 53 passed) ทุกตัวอักษร ระบุบรรทัดไฟล์จริงกำกับทุกบล็อก
- บทสนทนา User Prompt เรียบเรียงใหม่จาก Sprint4/README + โค้ดจริง ทุก Step ติดป้าย (เรียบเรียงใหม่)
- คำถามก่อนลงมือ (ที่เก็บ favorites / scope ทีละส่วน / confetti วาดเอง / filter ฝั่ง client) อยู่ในแชต ไม่รวมในไฟล์นี้

### Step 1: วางแผน Sprint 4 (ผู้รับผิดชอบ: Ter, Planner) (เรียบเรียงใหม่)

**User Prompt:**
> ช่วยแตกงาน Sprint4/README เป็น 4 ฟีเจอร์ (วงล้อ canvas+confetti / favorites localStorage / shopping list / filter client) ให้หน่อย ถามก่อนตรงไหนกระทบเกรดหรือสถาปัตย์

**AI Response:**
AI ถาม 4 ข้อ (ที่เก็บ favorites / scope / confetti / filter ฝั่งไหน) ได้คำตอบว่า localStorage ไม่ล็อกอิน, ทำทีละส่วนเริ่มวงล้อ, confetti วาดเอง, filter client แล้วลงมือตามลำดับ

**สิ่งที่ทีมตรวจสอบ/ปรับเอง:** ยืนยัน favorites เก็บเครื่องไม่ล็อกอิน ไม่ใช้ไฟล์ server

### Step 2: วงล้อ canvas + confetti วาดเอง (ผู้รับผิดชอบ: Khong, Coder) (เรียบเรียงใหม่)

**User Prompt:**
> เขียนวงล้อ roulette ใน app.js หน่อย เอาชื่อจาก top_recipes (สูงสุด 10 ชื่อ มีผู้ชนะรวมอยู่แน่) canvas 320 หมุน ease-out ลงตรงช่องผู้ชนะ <2 ชิ้น fallback เปิด modal เดิม รองรับ reduced-motion จบยิง confetti วาดเองไม่ใช้ CDN แล้วต่อปุ่ม Spin เดิม

**AI Response:**
AI อธิบายมุม landing (target = -90 องศาลบจุดกลาง slice ผู้ชนะ + หมุน 5 รอบ) พร้อมโค้ดด้านล่าง (static/js/app.js บรรทัด 633-832)

```javascript
// static/js/app.js:639-838
  /* ---------- roulette wheel (Sprint 4 part 1) ---------- */

  var WHEEL_COLORS = ["#f59e0b", "#fb923c", "#fbbf24", "#f97316", "#fcd34d", "#ea580c"];
  var WHEEL_CONFETTI = ["#f59e0b", "#f97316", "#10b981", "#f43f5e", "#ffffff", "#fbbf24"];
  var WHEEL_MAX_SLICES = 10;
  var WHEEL_SPIN_MS = 4200;

  function wheelCandidates(data) {
    var top = (data.top_recipes || []).slice(0, WHEEL_MAX_SLICES);
    var winner = data.selected_recipe;
    if (!winner) return { list: [], winnerId: null };
    var ids = top.map(function (r) { return String(r.id); });
    if (ids.indexOf(String(winner.id)) === -1) {
      top = [winner].concat(top).slice(0, WHEEL_MAX_SLICES);
    }
    registry[String(winner.id)] = winner;
    return { list: top, winnerId: String(winner.id) };
  }

  function wheelShortName(name) {
    var text = String(name || "Recipe");
    return text.length > 14 ? text.slice(0, 13) + "..." : text;
  }

  function wheelHtml(list) {
    var legend = list.map(function (r, i) {
      return '<li data-id="' + escapeHtml(r.id) + '" class="wheel-legend-item">' +
        '<span class="wheel-dot" style="background:' + WHEEL_COLORS[i % WHEEL_COLORS.length] + '"></span>' +
        '<span>' + escapeHtml(r.name) + '</span></li>';
    }).join("");
    return '<div class="modal-enter relative bg-white max-w-lg w-full rounded-3xl overflow-hidden shadow-2xl p-5 space-y-4">' +
      '<div class="flex items-start justify-between gap-2">' +
      '<div><h3 class="text-xl font-extrabold text-slate-800">Roulette Wheel</h3>' +
      '<p class="text-sm text-slate-400">Spinning among your matched recipes</p></div>' +
      '<button type="button" class="modal-close w-9 h-9 shrink-0 rounded-full bg-slate-100 flex items-center justify-center text-slate-500 hover:text-rose-500 transition" aria-label="Close"><i class="fa-solid fa-xmark"></i></button></div>' +
      '<div class="wheel-wrap"><div class="wheel-pointer"></div><canvas id="wheel-canvas" width="320" height="320"></canvas></div>' +
      '<ul id="wheel-legend" class="wheel-legend">' + legend + '</ul>' +
      '<div class="flex justify-end gap-2">' +
      '<button type="button" id="wheel-view" class="hidden px-5 py-3 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-600 text-white text-sm font-bold shadow-md active:scale-95 transition">View recipe</button>' +
      '<button type="button" class="modal-close px-5 py-3 rounded-xl bg-slate-800 text-white text-sm font-bold hover:bg-slate-700 transition active:scale-95">Close</button></div></div>';
  }

  function drawWheel(ctx, list, rotation) {
    var size = 320;
    var cx = size / 2;
    var cy = size / 2;
    var radius = size / 2 - 6;
    var arc = (Math.PI * 2) / list.length;
    ctx.clearRect(0, 0, size, size);
    list.forEach(function (r, i) {
      var start = rotation + i * arc;
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.arc(cx, cy, radius, start, start + arc);
      ctx.closePath();
      ctx.fillStyle = WHEEL_COLORS[i % WHEEL_COLORS.length];
      ctx.fill();
      ctx.lineWidth = 2;
      ctx.strokeStyle = "#ffffff";
      ctx.stroke();
      ctx.save();
      ctx.translate(cx, cy);
      ctx.rotate(start + arc / 2);
      ctx.textAlign = "right";
      ctx.fillStyle = "#ffffff";
      ctx.font = "bold 13px Kanit, sans-serif";
      ctx.shadowColor = "rgba(0,0,0,0.35)";
      ctx.shadowBlur = 3;
      ctx.fillText(wheelShortName(r.name), radius - 12, 5);
      ctx.restore();
    });
    ctx.beginPath();
    ctx.arc(cx, cy, 26, 0, Math.PI * 2);
    ctx.fillStyle = "#ffffff";
    ctx.fill();
    ctx.lineWidth = 3;
    ctx.strokeStyle = "#f59e0b";
    ctx.stroke();
  }

  function finishWheel(overlay, pack) {
    var items = $$(".wheel-legend-item", overlay);
    items.forEach(function (li) {
      if (li.dataset.id === pack.winnerId) li.classList.add("wheel-winner");
    });
    var viewBtn = $("#wheel-view", overlay);
    if (viewBtn) {
      viewBtn.classList.remove("hidden");
      viewBtn.addEventListener("click", function () {
        openModal(registry[pack.winnerId]);
      });
    }
    launchConfetti();
  }

  function startWheel(pack, canvas, overlay) {
    var ctx = canvas.getContext("2d");
    var n = pack.list.length;
    var arc = (Math.PI * 2) / n;
    var winnerIndex = 0;
    pack.list.forEach(function (r, i) {
      if (String(r.id) === pack.winnerId) winnerIndex = i;
    });
    var target = -(Math.PI / 2) - (winnerIndex * arc + arc / 2);
    var spins = Math.PI * 2 * 5;
    var total = spins + ((target % (Math.PI * 2)) + Math.PI * 2) % (Math.PI * 2);
    var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduceMotion) {
      drawWheel(ctx, pack.list, total);
      finishWheel(overlay, pack);
      return;
    }
    var startTime = null;
    function frame(now) {
      if (!startTime) startTime = now;
      var p = Math.min((now - startTime) / WHEEL_SPIN_MS, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      drawWheel(ctx, pack.list, total * eased);
      if (p < 1) {
        requestAnimationFrame(frame);
      } else {
        finishWheel(overlay, pack);
      }
    }
    drawWheel(ctx, pack.list, 0);
    requestAnimationFrame(frame);
  }

  function launchConfetti() {
    var c = document.createElement("canvas");
    c.className = "confetti-canvas";
    c.width = window.innerWidth;
    c.height = window.innerHeight;
    document.body.appendChild(c);
    var ctx = c.getContext("2d");
    var parts = [];
    for (var i = 0; i < 160; i++) {
      parts.push({
        x: c.width / 2 + (Math.random() - 0.5) * 220,
        y: c.height * 0.35,
        vx: (Math.random() - 0.5) * 9,
        vy: Math.random() * -8 - 2,
        size: Math.random() * 7 + 4,
        rot: Math.random() * Math.PI,
        vr: (Math.random() - 0.5) * 0.3,
        color: WHEEL_CONFETTI[i % WHEEL_CONFETTI.length]
      });
    }
    var startTime = null;
    function frame(now) {
      if (!startTime) startTime = now;
      var elapsed = now - startTime;
      ctx.clearRect(0, 0, c.width, c.height);
      parts.forEach(function (p) {
        p.x += p.vx;
        p.y += p.vy;
        p.vy += 0.25;
        p.rot += p.vr;
        ctx.save();
        ctx.translate(p.x, p.y);
        ctx.rotate(p.rot);
        ctx.fillStyle = p.color;
        ctx.fillRect(-p.size / 2, -p.size / 4, p.size, p.size / 2);
        ctx.restore();
      });
      if (elapsed < 2800) {
        requestAnimationFrame(frame);
      } else if (c.parentNode) {
        c.parentNode.removeChild(c);
      }
    }
    requestAnimationFrame(frame);
  }

  function openWheel(data) {
    if (!data || data.status !== "success" || !data.selected_recipe) return;
    var pack = wheelCandidates(data);
    if (pack.list.length < 2) {
      openModal(data.selected_recipe);
      return;
    }
    var overlay = $("#recipe-modal");
    overlay.innerHTML = wheelHtml(pack.list);
    overlay.classList.remove("hidden");
    overlay.classList.add("flex");
    document.body.style.overflow = "hidden";
    $$(".modal-close", overlay).forEach(function (btn) {
      btn.addEventListener("click", closeModal);
    });
    overlay.addEventListener("click", function (e) {
      if (e.target === overlay) closeModal();
    });
    document.addEventListener("keydown", onModalKeydown);
    var canvas = $("#wheel-canvas", overlay);
    if (canvas && canvas.getContext) {
      startWheel(pack, canvas, overlay);
    } else {
      openModal(data.selected_recipe);
    }
  }
```

```css
/* static/css/style.css:198-271 */
/* ---------- Roulette wheel (Sprint 4 part 1) ---------- */
.wheel-wrap {
  position: relative;
  width: min(78vw, 320px);
  margin: 0 auto;
}

#wheel-canvas {
  width: 100%;
  height: auto;
  display: block;
  border-radius: 9999px;
  box-shadow: 0 10px 30px rgba(245, 158, 11, 0.25);
}

.wheel-pointer {
  position: absolute;
  top: -8px;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 0;
  border-left: 12px solid transparent;
  border-right: 12px solid transparent;
  border-top: 20px solid #ea580c;
  filter: drop-shadow(0 2px 2px rgba(0, 0, 0, 0.25));
  z-index: 2;
}

.wheel-legend {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.4rem;
  max-height: 9rem;
  overflow-y: auto;
}

.wheel-legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8rem;
  color: #475569;
  background: #f8fafc;
  border-radius: 0.6rem;
  padding: 0.35rem 0.6rem;
}

.wheel-dot {
  width: 0.7rem;
  height: 0.7rem;
  border-radius: 9999px;
  flex-shrink: 0;
}

.wheel-legend-item.wheel-winner {
  background: #ecfdf5;
  border: 1px solid #10b981;
  color: #065f46;
  font-weight: 700;
}

.confetti-canvas {
  position: fixed;
  inset: 0;
  z-index: 90;
  pointer-events: none;
}

@media (prefers-reduced-motion: reduce) {
  .roulette-spin {
    animation: none;
  }
}
```

**สิ่งที่ทีมตรวจสอบ/ปรับเอง:** แก้ quote ชนใน wheelHtml (ตรวจ node --check), แก้มุมคลาด quarter-turn, พิสูจน์คณิตด้วย node (n=3/7/10 ลงตรงทุกช่อง)

### Step 3: tests/test_final_sprint.py (ผู้รับผิดชอบ: Toey, Debugger) (เรียบเรียงใหม่)

**User Prompt:**
> เขียน tests/test_final_sprint.py เทสสัญญา data ที่วงล้อใช้ (top มี id+name ครบ ผู้ชนะอยู่ใน top, เคส 1 ชิ้น, เคสว่าง, ผู้ชนะคะแนนท็อป) mock run_roulette_simulation ทั้งหมด

**AI Response:**
AI ให้ 4 เทส mock ล้วน โค้ดทั้งไฟล์ด้านล่าง

```python
# tests/test_final_sprint.py - ทั้งไฟล์
"""Final sprint part 1 tests - roulette wheel data contract."""

# Tests the server payload the canvas wheel consumes:
# top_recipes (id + name candidates) and selected_recipe (the winner).
# All backend calls are mocked - no network access.

from unittest.mock import patch

import pytest

from src.web_app import app


def make_recipe(meal_id, name, score=1.0):
    """Builds a formatted recipe dict as produced by format_recipe()."""
    return {
        "id": meal_id,
        "name": name,
        "category": "Pork",
        "area": "Greek",
        "image_url": "http://img/x.jpg",
        "ingredients": ["pork", "garlic"],
        "instructions": "Grill and serve.",
        "youtube_url": "",
        "score": score,
    }


@pytest.fixture
def client():
    """Flask test client for the web application."""
    with app.test_client() as test_client:
        yield test_client


@patch("src.web_app.run_roulette_simulation")
def test_wheel_payload_has_candidates_and_winner(mock_run, client):
    """Wheel needs >=2 named candidates and a winner among them."""
    top = [
        make_recipe("1", "Pork Souvlaki"),
        make_recipe("2", "Garlic Pork"),
        make_recipe("3", "Lemon Pork"),
    ]
    mock_run.return_value = {
        "status": "success",
        "query": ["pork"],
        "match_count": 3,
        "selected_recipe": top[1],
        "top_recipes": top,
    }

    data = client.post("/api/search", json={"ingredients": "pork"}).get_json()

    assert data["status"] == "success"
    assert len(data["top_recipes"]) >= 2
    assert all(r["id"] and r["name"] for r in data["top_recipes"])
    top_ids = {str(r["id"]) for r in data["top_recipes"]}
    assert str(data["selected_recipe"]["id"]) in top_ids


@patch("src.web_app.run_roulette_simulation")
def test_wheel_single_candidate_falls_back_to_modal(mock_run, client):
    """One candidate carries enough data for the direct modal path."""
    only = make_recipe("9", "Lonely Pork")
    mock_run.return_value = {
        "status": "success",
        "query": ["pork"],
        "match_count": 1,
        "selected_recipe": only,
        "top_recipes": [only],
    }

    data = client.post("/api/search", json={"ingredients": "pork"}).get_json()

    assert len(data["top_recipes"]) == 1
    assert data["selected_recipe"]["name"] == "Lonely Pork"


@patch("src.web_app.run_roulette_simulation")
def test_wheel_empty_result_has_no_winner(mock_run, client):
    """Empty results must not produce a winner payload."""
    mock_run.return_value = {
        "status": "success",
        "query": ["avocado"],
        "match_count": 0,
        "selected_recipe": None,
        "top_recipes": [],
    }

    data = client.post("/api/search", json={"ingredients": "avocado"}).get_json()

    assert data["top_recipes"] == []
    assert data["selected_recipe"] is None


@patch("src.web_app.run_roulette_simulation")
def test_wheel_winner_comes_from_top_scores(mock_run, client):
    """Winner id matches one of the top-scored candidates."""
    top = [
        make_recipe("1", "Low Pork", score=0.5),
        make_recipe("2", "Top Pork A", score=1.0),
        make_recipe("3", "Top Pork B", score=1.0),
    ]
    mock_run.return_value = {
        "status": "success",
        "query": ["pork"],
        "match_count": 3,
        "selected_recipe": top[2],
        "top_recipes": top,
    }

    data = client.post("/api/search", json={"ingredients": "pork"}).get_json()

    best = max(r["score"] for r in data["top_recipes"])
    assert data["selected_recipe"]["score"] == best
```

**สิ่งที่ทีมตรวจสอบ/ปรับเอง:** แก้ docstring หลุด quote 1 จุด รัน pytest ได้ 53 passed

### Step 4: Favorites localStorage + tab (ผู้รับผิดชอบ: Benz, Coder) (เรียบเรียงใหม่)

**User Prompt:**
> ทำ favorites ไม่ล็อกอินเก็บ localStorage หน่อย มี store (load/save/toggle/badge), หัวใจบนการ์ดกดแล้วไม่เปิด modal, tab Favorites + badge ใน nav, ปุ่ม Save ใน modal, อยู่หน้า favorites กดลบแล้วรีเฟรชทันที

**AI Response:**
AI อธิบาย store + 2 views (explore/favorites) พร้อมโค้ด store (app.js:445-513) และ views (app.js:514-536) ด้านล่าง

```javascript
// static/js/app.js:445-513 (store)
  /* ---------- favorites store (localStorage, Sprint 4 part 2) ---------- */

  function loadFavorites() {
    try {
      return JSON.parse(localStorage.getItem(FAVORITES_KEY)) || {};
    } catch (e) {
      return {};
    }
  }

  function saveFavorites(favs) {
    try {
      localStorage.setItem(FAVORITES_KEY, JSON.stringify(favs));
    } catch (e) {
      showToast('Could not save favorites on this device', 'danger');
    }
  }

  function isFavorite(id) {
    return !!loadFavorites()[String(id)];
  }

  function toggleFavorite(recipe) {
    if (!recipe) return false;
    var favs = loadFavorites();
    var id = String(recipe.id);
    if (favs[id]) {
      delete favs[id];
    } else {
      favs[id] = recipe;
    }
    saveFavorites(favs);
    updateFavBadge();
    return !!favs[id];
  }

  function favoriteList() {
    var favs = loadFavorites();
    return Object.keys(favs).map(function (k) { return favs[k]; });
  }

  function updateFavBadge() {
    var badge = document.getElementById('fav-count');
    if (!badge) return;
    var n = favoriteList().length;
    badge.textContent = n;
    badge.classList.toggle('hidden', n === 0);
  }

  function favBtnHtml(recipe) {
    var active = isFavorite(recipe.id) ? ' active' : '';
    return '<button type="button" data-id="' + escapeHtml(recipe.id) + '" class="fav-btn' + active + '" aria-label="Toggle favorite"><i class="fa-solid fa-heart"></i></button>';
  }

  function toggleFavoriteById(id, grid) {
    var recipe = registry[String(id)];
    if (!recipe) return;
    var on = toggleFavorite(recipe);
    showToast(on ? 'Saved to favorites' : 'Removed from favorites', on ? 'success' : 'danger');
    if (state.view === 'favorites') {
      showFavorites();
    } else if (grid) {
      var btn = grid.querySelector('.fav-btn[data-id="' + id + '"]');
      if (btn) btn.classList.toggle('active', on);
    }
    var modalBtn = document.getElementById('modal-fav');
    if (modalBtn) syncModalFavBtn(modalBtn, on);
  }

```

```javascript
// static/js/app.js:514-536 (views)
  /* ---------- views: explore / favorites ---------- */

  function setNav(view) {
    state.view = view;
    var fav = document.getElementById('nav-favorites');
    var exp = document.getElementById('nav-explore');
    if (fav) fav.classList.toggle('active', view === 'favorites');
    if (exp) exp.classList.toggle('active', view === 'explore');
  }

  function showFavorites() {
    setNav('favorites');
    renderResults({ status: 'success', top_recipes: favoriteList() }, 'favorites');
    var section = document.getElementById('results-section');
    if (section) section.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function showExplore() {
    setNav('explore');
    if (state.lastData) {
      renderResults(state.lastData, 'explore');
    }
  }
```

```html
<!-- templates/base.html:26-33 (nav) -->
            <nav class="flex items-center gap-1 sm:gap-2" aria-label="Main navigation">
                <a href="/" id="nav-explore" class="nav-tab active">
                    <i class="fa-solid fa-compass"></i><span class="nav-label">Explore</span>
                </a>
                <button id="nav-favorites" type="button" class="nav-tab">
                    <i class="fa-solid fa-heart"></i><span class="nav-label">Favorites</span><span id="fav-count" class="nav-badge hidden">0</span>
                </button>
            </nav>
```

```css
/* static/css/style.css:273-312 (fav + badge) */
/* ---------- Favorites + filter + shopping (Sprint 4 parts 2-4) ---------- */
.fav-btn {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  z-index: 2;
  width: 2rem;
  height: 2rem;
  border-radius: 9999px;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(4px);
  color: #cbd5e1;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.15s ease, color 0.15s ease;
}

.fav-btn:hover {
  transform: scale(1.12);
  color: #f43f5e;
}

.fav-btn.active {
  color: #f43f5e;
}

.nav-badge {
  background: #f43f5e;
  color: #fff;
  font-size: 10px;
  font-weight: 700;
  min-width: 1.25rem;
  height: 1.25rem;
  padding: 0 0.3rem;
  border-radius: 9999px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
```

**สิ่งที่ทีมตรวจสอบ/ปรับเอง:** รื้อ nav ที่พันกันตอนแก้ครั้งแรก ผ่าตัดรายบรรทัดจนสะอาด

### Step 5: Shopping list + ปุ่ม copy (ผู้รับผิดชอบ: Khong, Coder) (เรียบเรียงใหม่)

**User Prompt:**
> ทำ shopping list ใน modal หน่อย เทียบ ingredients กับ query ที่กรอก อันไหนขาดติดป้าย missing มีแถบบอกจำนวน + ปุ่ม copy (มี fallback เบราว์เซอร์เก่า) toast แจ้งผล

**AI Response:**
AI อธิบาย have-map + missingCount + clipboard/fallback พร้อมโค้ด (app.js:602-636) และ CSS (style.css:314-384) ด้านล่าง

```javascript
// static/js/app.js:602-636 (shopping)
  /* ---------- shopping list (Sprint 4 part 3) ---------- */

  function missingIngredients(recipe) {
    var have = {};
    state.query.forEach(function (q) { have[q] = true; });
    return (recipe.ingredients || []).filter(function (ing) { return !have[ing]; });
  }

  function copyShopping(recipe) {
    var missing = missingIngredients(recipe);
    var text = 'Shopping list for ' + recipe.name + ':' + '\n' + missing.map(function (m) { return '- ' + m; }).join('\n');
    function done(ok) {
      showToast(ok ? 'Shopping list copied' : 'Copy failed on this browser', ok ? 'success' : 'danger');
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function () { done(true); }, function () { done(false); });
    } else {
      var ta = document.createElement('textarea');
      ta.value = text;
      document.body.appendChild(ta);
      ta.select();
      try {
        document.execCommand('copy');
        done(true);
      } catch (e) {
        done(false);
      }
      document.body.removeChild(ta);
    }
  }

  function syncModalFavBtn(btn, on) {
    btn.classList.toggle('active', on);
    btn.querySelector('span').textContent = on ? 'Saved' : 'Save';
  }
```

```css
/* static/css/style.css:314-384 (missing + shopping + modal-fav) */
.ingredient-item.missing {
  background: #fffbeb;
  border: 1px dashed #f59e0b;
}

.ing-tag {
  margin-left: auto;
  flex-shrink: 0;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: #b45309;
  background: #fef3c7;
  border-radius: 9999px;
  padding: 0.1rem 0.5rem;
}

.shopping-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
  flex-wrap: wrap;
  background: #fffbeb;
  border: 1px solid #fde68a;
  border-radius: 0.75rem;
  padding: 0.6rem 0.8rem;
  font-size: 0.8rem;
  font-weight: 600;
  color: #92400e;
}

.shopping-copy {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  background: #f59e0b;
  color: #fff;
  font-size: 0.75rem;
  font-weight: 700;
  border-radius: 0.6rem;
  padding: 0.45rem 0.8rem;
  transition: filter 0.15s ease, transform 0.15s ease;
}

.shopping-copy:hover {
  filter: brightness(1.08);
}

.shopping-copy:active {
  transform: scale(0.95);
}

.modal-fav {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  border-radius: 0.75rem;
  font-size: 0.875rem;
  font-weight: 700;
  background: #f1f5f9;
  color: #64748b;
  transition: background-color 0.2s ease, color 0.2s ease, transform 0.15s ease;
}

.modal-fav.active {
  background: #ffe4e6;
  color: #e11d48;
}
```

```javascript
// static/js/app.js:281-294 (wiring ปุ่ม modal-fav + copy-shopping ใน openModal)
    var favBtn = overlay.querySelector('#modal-fav');
    if (favBtn) {
      syncModalFavBtn(favBtn, isFavorite(recipe.id));
      favBtn.addEventListener('click', function () {
        toggleFavoriteById(String(recipe.id), document.getElementById('results-grid'));
      });
    }

    var copyBtn = overlay.querySelector('#copy-shopping');
    if (copyBtn) {
      copyBtn.addEventListener('click', function () {
        copyShopping(recipe);
      });
    }
```

**สิ่งที่ทีมตรวจสอบ/ปรับเอง:** ลบบรรทัด ul ซ้ำจากตอนแก้ modal (node ผ่านแต่ HTML ผิด)

### Step 6: Filter category/area ฝั่ง client (ผู้รับผิดชอบ: Benz, Coder) (เรียบเรียงใหม่)

**User Prompt:**
> ทำ filter chips จาก category/area ของผลลัพธ์จริง กดซ้ำยกเลิก ผสมกันได้ มี All รีเซ็ต นับแบบ X of Y ไม่แตะ engine

**AI Response:**
AI อธิบาย filterValues/applyFilter/renderFilterBar + เก็บ lastData พร้อมโค้ด (app.js:538-600) ด้านล่าง

```javascript
// static/js/app.js:538-600 (filter)
  /* ---------- client-side category / area filter (Sprint 4 part 4) ---------- */

  function filterValues(data) {
    var cats = [];
    var areas = [];
    (data.top_recipes || []).forEach(function (r) {
      if (r.category && cats.indexOf(r.category) === -1) cats.push(r.category);
      if (r.area && areas.indexOf(r.area) === -1) areas.push(r.area);
    });
    return { categories: cats, areas: areas };
  }

  function applyFilter(recipes) {
    return (recipes || []).filter(function (r) {
      var okCat = !state.filter.category || r.category === state.filter.category;
      var okArea = !state.filter.area || r.area === state.filter.area;
      return okCat && okArea;
    });
  }

  function filterChip(label, kind, value, active) {
    var cls = active ? 'bg-amber-500 text-white shadow-sm' : 'bg-white border border-slate-200 text-slate-500 hover:bg-amber-50';
    return '<button type="button" data-kind="' + kind + '" data-value="' + escapeHtml(value) + '" class="filter-chip shrink-0 text-xs font-semibold px-3 py-1.5 rounded-full transition active:scale-95 ' + cls + '">' + escapeHtml(label) + '</button>';
  }

  function renderFilterBar(data) {
    var section = document.getElementById('results-section');
    var grid = document.getElementById('results-grid');
    if (!section || !grid) return;
    var old = document.getElementById('filter-bar');
    if (old) old.remove();
    var vals = filterValues(data);
    if (!vals.categories.length && !vals.areas.length) return;
    var bar = document.createElement('div');
    bar.id = 'filter-bar';
    bar.className = 'flex flex-wrap gap-2';
    var html = '';
    var allActive = !state.filter.category && !state.filter.area;
    html += filterChip('All', '', '', allActive);
    vals.categories.forEach(function (c) {
      html += filterChip(c, 'category', c, state.filter.category === c);
    });
    vals.areas.forEach(function (a) {
      html += filterChip(a, 'area', a, state.filter.area === a);
    });
    bar.innerHTML = html;
    section.insertBefore(bar, grid);
    var chips = bar.querySelectorAll('.filter-chip');
    Array.prototype.forEach.call(chips, function (chip) {
      chip.addEventListener('click', function () {
        var kind = chip.getAttribute('data-kind');
        var value = chip.getAttribute('data-value');
        if (!kind) {
          state.filter = { category: '', area: '' };
        } else if (kind === 'category') {
          state.filter.category = state.filter.category === value ? '' : value;
        } else {
          state.filter.area = state.filter.area === value ? '' : value;
        }
        renderResults(state.lastData, state.view);
      });
    });
  }
```

**สิ่งที่ทีมตรวจสอบ/ปรับเอง:** แก้ฟังก์ชันซ้ำจาก off-by-one (runSearch/spinRoulette) ตรวจ node --check ผ่าน

### Step 7: งานเชื่อม micro-edits + ตรวจรวม (ผู้รับผิดชอบ: ทีม) (เรียบเรียงใหม่)

**User Prompt:**
> ช่วยผูกทุกอย่างเข้าด้วยกันหน่อย state เพิ่ม view/lastData/filter, การ์ดมีปุ่มหัวใจ, คลิกหัวใจไม่เปิด modal, renderResults รับ mode + จำ lastData, search/spin กลับหน้า explore, nav + badge, clear รีเซ็ต filter

**AI Response:**
AI แก้เป็นจุดเล็กด้านล่าง (เลขบรรทัดปัจจุบันของ app.js)

```javascript
// state + key (app.js:15-21)
  var state = {
    query: [], // selected ingredients / chips
    view: 'explore',
    lastData: null, // last successful search payload
    filter: { category: '', area: '' }
  };
  var FAVORITES_KEY = 'rr-favorites-v1';
```

```javascript
// หัวใจบนการ์ด + กันเปิด modal (app.js:175, app.js:247-253)
      favBtnHtml(recipe) +
      var fav = e.target.closest('.fav-btn');
      if (fav) {
        e.stopPropagation();
        toggleFavoriteById(fav.getAttribute('data-id'), grid);
        return;
      }
```

```javascript
// กลับหน้า explore เมื่อค้นหา/สุ่มใหม่ + nav + clear
    setNav('explore'); // ใน runSearch, spinRoulette
    updateFavBadge(); // ใน initExplore
      state.filter = { category: '', area: '' }; // ใน clear
      state.lastData = null; // ใน clear
```

**สิ่งที่ทีมตรวจสอบ/ปรับเอง:** เจอ delegation หัวใจหายจากการแก้ครั้งก่อน (กดแล้วเปิด modal) ใส่กลับ + node --check + pytest 53 passed

## ตารางสรุป

| ขั้นตอน | ไฟล์ | ผู้รับผิดชอบ | สิ่งที่ AI ช่วย | สิ่งที่ทีมทำเอง |
|---|---|---|---|---|
| 1 วางแผน | - | Ter | ถาม 4 ข้อก่อนลงมือ | ตอบ scope ทีละส่วน |
| 2 วงล้อ | app.js + style.css | Khong | canvas+easing+confetti | แก้ quote/มุม + พิสูจน์คณิต |
| 3 เทส | test_final_sprint.py | Toey | 4 เทส mock | แก้ docstring + รันเขียว |
| 4 favorites | app.js + base.html + css | Benz | store/views/nav | รื้อ nav ที่พัน + delegation หายใส่กลับ |
| 5 shopping | app.js + css | Khong | missing+copy/fallback | ลบ ul ซ้ำ |
| 6 filter | app.js | Benz | chips client + lastData | แก้ฟังก์ชันซ้ำ off-by-one |
| 7 เชื่อม | app.js | ทีม | micro-edits + ตรวจรวม | node + pytest ผ่าน |

---

[Back to top](#top) | [README](../README.md)
