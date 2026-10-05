/* Recipe Roulette — Sprint 3 client interactivity.
   Implemented against the API contract in src/web_app.py.
   UI follows DESIGN.md (recipe cards, modal, roulette spin, toasts). */
(function () {
  "use strict";

  var $ = function (sel, root) {
    return (root || document).querySelector(sel);
  };
  var $$ = function (sel, root) {
    return Array.prototype.slice.call((root || document).querySelectorAll(sel));
  };

  var registry = {}; // id -> formatted recipe, used by shared click handlers
  var state = {
    query: [], // selected ingredients / chips
    view: 'explore',
    lastData: null, // last successful search payload
    filter: { category: '', area: '' }
  };
  var FAVORITES_KEY = 'rr-favorites-v1';

  var PLACEHOLDER = "data:image/svg+xml;utf8," + encodeURIComponent(
    '<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300">' +
    '<rect width="100%" height="100%" fill="#fef3c7"/>' +
    '<text x="50%" y="50%" font-family="Arial" font-size="20" fill="#d97706" ' +
    'text-anchor="middle">No image</text></svg>'
  );

  /* ---------- utilities ---------- */

  function escapeHtml(value) {
    return String(value == null ? "" : value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  window.fallbackImg = function (img) {
    img.onerror = null;
    img.src = PLACEHOLDER;
  };

  function imgHtml(url, alt) {
    if (!url) {
      return '<div class="w-full h-full bg-gradient-to-br from-amber-100 to-orange-100 ' +
        'flex items-center justify-center text-amber-400 text-4xl">' +
        '<i class="fa-solid fa-utensils"></i></div>';
    }
    return '<img src="' + escapeHtml(url) + '" alt="' + escapeHtml(alt) + '" loading="lazy" ' +
      'class="w-full h-full object-cover transform group-hover:scale-105 transition-transform duration-300" ' +
      'onerror="window.fallbackImg && fallbackImg(this)">';
  }

  function api(url, options) {
    return fetch(url, options).then(function (resp) {
      return resp.json();
    });
  }

  function postPayload(body) {
    return {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    };
  }

  /* ---------- toast ---------- */

  var toastTimer = null;

  function showToast(message, type) {
    var toast = $("#toast");
    if (!toast) return;
    toast.textContent = message;
    toast.className = "fixed bottom-6 left-1/2 z-[80] -translate-x-1/2 px-5 py-3 " +
      "rounded-xl text-white text-sm font-semibold shadow-xl transition-all " +
      "duration-300 translate-y-2 " + (type === "danger" ? "danger" : "success") + " visible";
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () {
      toast.className = "fixed bottom-6 left-1/2 z-[80] -translate-x-1/2 px-5 py-3 " +
        "rounded-xl text-white text-sm font-semibold shadow-xl transition-all " +
        "duration-300 translate-y-2 opacity-0 pointer-events-none";
    }, 2600);
  }

  /* ---------- loading progress (below Search bar) ---------- */

  var loading = false;

  function showLoading(message) {
    var text = $("#loading-text");
    if (text && message) text.textContent = message;
    var bar = $("#loading-bar");
    if (bar) bar.classList.remove("hidden");
    loading = true;
  }

  function hideLoading() {
    var bar = $("#loading-bar");
    if (bar) bar.classList.add("hidden");
    loading = false;
  }

  /* ---------- ingredient chips (Explore) ---------- */

  function addSelectedChip(name) {
    if (state.query.indexOf(name) !== -1) return;
    state.query.push(name);
    var container = $("#selected-ingredients");
    var chip = document.createElement("span");
    chip.className = "select-chip";
    chip.dataset.value = name;
    chip.innerHTML = "<span>" + escapeHtml(name) + "</span>" +
      '<i class="fa-solid fa-xmark" role="button" aria-label="Remove"></i>';
    chip.querySelector(".fa-xmark").addEventListener("click", function () {
      state.query = state.query.filter(function (item) {
        return item !== name;
      });
      chip.remove();
    });
    container.appendChild(chip);
  }

  function readInput() {
    var input = $("#ingredient-input");
    return input ? input.value.trim() : "";
  }

  function addFromInput() {
    var value = readInput();
    if (!value) {
      showToast("Type an ingredient first", "danger");
      return;
    }
    value.split(",").forEach(function (part) {
      var cleaned = part.trim().toLowerCase();
      if (cleaned) addSelectedChip(cleaned);
    });
    var input = $("#ingredient-input");
    if (input) input.value = "";
  }

  /* ---------- results rendering ---------- */

  function matchedIngredientTags(recipe) {
    var matched = new Set(state.query);
    var shown = recipe.ingredients || [];
    return shown.slice(0, 4).map(function (ing) {
      var hit = matched.has(ing);
      var cls = hit
        ? "bg-emerald-50 text-emerald-700 border border-emerald-200"
        : "bg-slate-100 text-slate-500";
      var icon = hit
        ? '<i class="fa-solid fa-check"></i>'
        : '<i class="fa-solid fa-leaf"></i>';
      return '<span class="inline-flex items-center gap-1 text-[11px] px-2 py-1 rounded-full ' + cls + '">' +
        icon + " " + escapeHtml(ing) + "</span>";
    }).join("");
  }

  function recipeCardHtml(recipe) {
    var pct = recipe.score != null ? Math.round(recipe.score * 100) : null;
    var badge = pct != null
      ? '<span class="absolute bottom-2 left-2 bg-emerald-500 text-white text-xs font-bold px-2 py-1 rounded-lg">' +
        pct + "% match</span>"
      : "";
    return '<article class="recipe-card group bg-white rounded-2xl overflow-hidden shadow-md ' +
      'hover:shadow-xl transition-all duration-300 cursor-pointer" data-id="' + escapeHtml(recipe.id) + '">' +
      '<div class="relative h-48 overflow-hidden">' +
      imgHtml(recipe.image_url, recipe.name) +
      favBtnHtml(recipe) +
      '<span class="absolute top-2 left-2 bg-slate-900/60 backdrop-blur-md text-white text-xs px-2 py-1 rounded-lg">' +
      escapeHtml(recipe.area || recipe.category || "Recipe") + "</span>" +
      badge +
      "</div>" +
      '<div class="p-4 space-y-2">' +
      '<div class="flex items-center gap-2 text-xs text-slate-400">' +
      '<span class="bg-amber-50 text-amber-700 px-2 py-0.5 rounded-full font-medium">' +
      escapeHtml(recipe.category || "Recipe") + "</span>" +
      '<span class="flex items-center gap-1"><i class="fa-solid fa-star text-amber-400"></i> 4.5</span>' +
      "</div>" +
      '<h3 class="font-bold text-slate-800 line-clamp-1">' + escapeHtml(recipe.name) + "</h3>" +
      '<div class="flex flex-wrap gap-1.5 pt-1">' + matchedIngredientTags(recipe) + "</div>" +
      "</div></article>";
  }

  function renderResults(data, mode) {
    mode = mode || state.view;
    var section = $("#results-section");
    var empty = $("#empty-state");
    var grid = $("#results-grid");
    var count = $("#results-count");
    var title = $("#results-title");
    var clearBtn = $("#clear-results");

    if (!grid) return;

    if (data.status === "error") {
      section.classList.add("hidden");
      empty.classList.remove("hidden");
      title.textContent = "Something went wrong";
      count.textContent = "";
      showToast(data.message || "Search failed", "danger");
      return;
    }

    registry = {};
    (data.top_recipes || []).forEach(function (r) {
      registry[String(r.id)] = r;
    });

    state.lastData = data;
    renderFilterBar(data);

    var total = data.top_recipes ? data.top_recipes.length : 0;
    var shown = mode === 'favorites' ? (data.top_recipes || []) : applyFilter(data.top_recipes);
    section.classList.remove("hidden");
    empty.classList.add("hidden");
    if (mode === 'favorites') {
      title.textContent = "Favorite Recipes";
      count.textContent = total ? total + " saved recipe" + (total > 1 ? "s" : "") + " in this device" : "";
    } else {
      title.textContent = total ? "Matched Recipes" : "No Recipes";
      count.textContent = total
        ? shown.length + " of " + total + " matching recipe" + (total > 1 ? "s" : "") + " for: " + state.query.join(", ")
        : "";
    }
    clearBtn.classList.toggle("hidden", total === 0);

    grid.innerHTML = shown.map(recipeCardHtml).join("");
    attachCardHandlers(grid);

    if (shown.length === 0) {
      section.classList.add("hidden");
      empty.classList.remove("hidden");
    }
  }

  /* ---------- shared card / modal handlers ---------- */

  function attachCardHandlers(grid) {
    grid.addEventListener("click", function (e) {
      var fav = e.target.closest('.fav-btn');
      if (fav) {
        e.stopPropagation();
        toggleFavoriteById(fav.getAttribute('data-id'), grid);
        return;
      }
      var card = e.target.closest(".recipe-card");
      if (!card) return;
      openModal(registry[card.dataset.id]);
    });
  }

  function openModal(recipe) {
    if (!recipe) return;
    var overlay = $("#recipe-modal");
    overlay.innerHTML = modalHtml(recipe);
    overlay.classList.remove("hidden");
    overlay.classList.add("flex");
    document.body.style.overflow = "hidden";

    $$(".modal-close", overlay).forEach(function (btn) {
      btn.addEventListener("click", closeModal);
    });

    overlay.addEventListener("click", function (e) {
      if (e.target === overlay) closeModal();
    });

    $$(".ingredient-item", overlay).forEach(function (item) {
      item.addEventListener("click", function () {
        item.classList.toggle("checked");
      });
    });

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

    document.addEventListener("keydown", onModalKeydown);
  }

  function onModalKeydown(e) {
    if (e.key === "Escape") closeModal();
  }

  function closeModal() {
    var overlay = $("#recipe-modal");
    overlay.classList.add("hidden");
    overlay.classList.remove("flex");
    overlay.innerHTML = "";
    document.body.style.overflow = "";
    document.removeEventListener("keydown", onModalKeydown);
  }

  function modalHtml(recipe) {
    var pct = recipe.score != null ? Math.round(recipe.score * 100) : null;
    var banner = pct != null
      ? '<div class="flex items-center gap-3 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-600 ' +
        'text-white px-4 py-3 shadow-md shadow-emerald-500/20 fade-enter">' +
        '<i class="fa-solid fa-circle-check text-lg"></i>' +
        '<div><p class="text-sm font-bold">' + pct + "% ingredient match</p>" +
        '<p class="text-xs opacity-80">A great recipe for your fridge</p></div></div>'
      : "";

    var haveMap = {};
    state.query.forEach(function (q) { haveMap[q] = true; });
    var missingCount = 0;
    var ingredients = (recipe.ingredients || []).map(function (ing) {
      var missed = !haveMap[ing];
      if (missed) missingCount += 1;
      var rowCls = missed ? 'ingredient-item missing' : 'ingredient-item';
      var missTag = missed ? '<span class="ing-tag">missing</span>' : '';
      return '<li class="' + rowCls + ' flex items-start gap-3 cursor-pointer rounded-lg p-1.5 -m-1.5 hover:bg-amber-50/60 transition">' +
        '<span class="mt-0.5 w-5 h-5 shrink-0 rounded-md border border-slate-200 flex items-center justify-center">' +
        '<i class="fa-solid fa-check text-emerald-500 opacity-0 transition"></i></span>' +
        '<span class="text-sm text-slate-700">' + escapeHtml(ing) + '</span>' + missTag + '</li>';
    }).join("") || '<li class="text-sm text-slate-400">No ingredients listed.</li>';
    var shoppingBar = missingCount
      ? '<div class="shopping-bar"><span>' + missingCount + ' missing item' + (missingCount > 1 ? 's' : '') + ' - buy these:</span><button type="button" id="copy-shopping" class="shopping-copy"><i class="fa-solid fa-clipboard-list"></i> Copy shopping list</button></div>'
      : '';

    var steps = (recipe.instructions || "")
      .split("\n")
      .map(function (s) { return s.trim(); })
      .filter(Boolean)
      .map(function (s, i) {
        return '<li class="flex gap-3"><span class="shrink-0 w-6 h-6 rounded-full bg-amber-100 ' +
          'text-amber-700 text-xs font-bold flex items-center justify-center">' + (i + 1) + "</span>" +
          '<span class="text-sm text-slate-600">' + escapeHtml(s) + "</span></li>";
      }).join("");

    var youtube = recipe.youtube_url
      ? '<a href="' + escapeHtml(recipe.youtube_url) + '" target="_blank" rel="noopener" ' +
        'class="inline-flex items-center gap-2 text-sm font-semibold text-rose-600 hover:text-rose-500 transition">' +
        '<i class="fa-brands fa-youtube"></i> Watch on YouTube</a>'
      : "";

    return '<div class="modal-enter relative bg-white max-w-2xl w-full rounded-3xl overflow-hidden ' +
      "shadow-2xl max-h-[90vh] flex flex-col\">" +
      '<div class="relative h-56 sm:h-64 shrink-0">' +
      imgHtml(recipe.image_url, recipe.name) +
      '<button type="button" class="modal-close absolute top-3 right-3 w-9 h-9 rounded-full ' +
      'bg-white/90 backdrop-blur-md flex items-center justify-center text-slate-600 ' +
      'hover:text-rose-500 hover:rotate-90 transition" aria-label="Close"><i class="fa-solid fa-xmark"></i></button>' +
      '<div class="absolute inset-x-0 bottom-0 bg-gradient-to-t from-slate-900/90 via-slate-900/50 to-transparent p-5 pt-14">' +
      '<h3 class="text-xl sm:text-2xl font-extrabold text-white line-clamp-2">' + escapeHtml(recipe.name) + "</h3>" +
      '<div class="flex items-center gap-2 mt-1 flex-wrap">' +
      '<span class="bg-white/20 backdrop-blur-md text-white text-xs px-2 py-0.5 rounded-full">' +
      escapeHtml(recipe.area || "") + "</span>" +
      '<span class="bg-amber-400/90 text-slate-800 text-xs px-2 py-0.5 rounded-full font-semibold">' +
      escapeHtml(recipe.category || "Recipe") + "</span></div></div></div>" +

      '<div class="overflow-y-auto p-5 space-y-5">' + banner +

      '<div><h4 class="font-bold text-slate-800 mb-3 flex items-center gap-2">' +
      '<i class="fa-solid fa-egg text-amber-500"></i> Ingredients</h4>' +
      '<ul class="grid grid-cols-1 sm:grid-cols-2 gap-2">' + ingredients + '</ul>' + shoppingBar + '</div>' +

      '<div><h4 class="font-bold text-slate-800 mb-3 flex items-center gap-2">' +
      '<i class="fa-solid fa-list-ol text-orange-500"></i> Instructions</h4>' +
      '<ol class="space-y-3">' + (steps || '<li class="text-sm text-slate-400">No instructions available.</li>') +
      '</ol></div>' +
      (youtube ? '<div class="flex justify-center">' + youtube + '</div>' : "") +
      '</div>' +

      '<div class="p-4 border-t border-slate-100 flex justify-end gap-2">' +
      '<button type="button" id="modal-fav" class="modal-fav"><i class="fa-solid fa-heart"></i> <span>Save</span></button>' +
      '<button type="button" class="modal-close px-5 py-3 rounded-xl bg-slate-800 text-white text-sm font-bold ' +
      'hover:bg-slate-700 transition active:scale-95">Close</button></div></div>';
  }

  /* ---------- search / roulette ---------- */

  function collectQuery() {
    return state.query.join(", ");
  }

  function runSearch() {
    if (loading) return;
    setNav('explore');
    if (!state.query.length) {
      showToast("Add at least one ingredient first", "danger");
      return;
    }
    showLoading("Searching recipes...");
    api("/api/search", postPayload({ ingredients: collectQuery() }))
      .then(renderResults)
      .catch(function () {
        showToast("Search failed — is the server running?", "danger");
      })
      .then(hideLoading);
  }

  function spinRoulette() {
    if (loading) return;
    setNav('explore');
    var btn = $("#roulette-btn");
    if (btn) {
      var icon = btn.querySelector(".fa-arrows-spin");
      if (icon) {
        icon.classList.remove("roulette-spin");
        void icon.offsetWidth;
        icon.classList.add("roulette-spin");
      }
    }
    if (!state.query.length) {
      showToast("Add at least one ingredient first", "danger");
      return;
    }
    showLoading("Spinning the roulette...");
    api("/api/search", postPayload({ ingredients: collectQuery() }))
      .then(function (data) {
        renderResults(data);
        if (data.status === "success" && data.selected_recipe) {
          setTimeout(function () {
            openWheel(data);
          }, 400);
        } else if (data.status === "error") {
          showToast(data.message || "Search failed", "danger");
        }
      })
      .catch(function () {
        showToast("Search failed — is the server running?", "danger");
      })
      .then(hideLoading);
  }

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


  /* ---------- page initialisation ---------- */

  function initExplore() {
    var input = $("#ingredient-input");
    var addBtn = $("#add-ingredient");
    var searchBtn = $("#search-btn");
    var rouletteBtn = $("#roulette-btn");
    var clearBtn = $("#clear-results");

    if (input) input.addEventListener("keydown", function (e) {
      if (e.key === "Enter") {
        e.preventDefault();
        addFromInput();
      }
    });
    if (addBtn) addBtn.addEventListener("click", addFromInput);

    $$(".quick-chip").forEach(function (chip) {
      chip.addEventListener("click", function () {
        addSelectedChip(chip.dataset.ingredient);
      });
    });

    if (searchBtn) searchBtn.addEventListener("click", runSearch);
    var favTab = document.getElementById('nav-favorites');
    if (favTab) favTab.addEventListener('click', showFavorites);
    var expTab = document.getElementById('nav-explore');
    if (expTab) expTab.addEventListener('click', function (e) {
      e.preventDefault();
      showExplore();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
    updateFavBadge();

    if (rouletteBtn) rouletteBtn.addEventListener("click", spinRoulette);
    if (clearBtn) clearBtn.addEventListener("click", function () {
      $("#results-section").classList.add("hidden");
      $("#empty-state").classList.add("hidden");
      $("#results-grid").innerHTML = "";
      state.query = [];
      state.filter = { category: '', area: '' };
      state.lastData = null;
      setNav('explore');
      var selected = $("#selected-ingredients");
      if (selected) selected.innerHTML = "";
    });
  }

  document.addEventListener("DOMContentLoaded", initExplore);
})();
