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
  };

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

  function renderResults(data) {
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

    var total = data.top_recipes ? data.top_recipes.length : 0;
    section.classList.remove("hidden");
    empty.classList.add("hidden");
    title.textContent = total ? "Matched Recipes" : "No Recipes";
    count.textContent = total
      ? total + " matching recipe" + (total > 1 ? "s" : "") + " for: " + state.query.join(", ")
      : "";
    clearBtn.classList.toggle("hidden", total === 0);

    grid.innerHTML = (data.top_recipes || []).map(recipeCardHtml).join("");
    attachCardHandlers(grid);

    if (total === 0) {
      section.classList.add("hidden");
      empty.classList.remove("hidden");
    }
  }

  /* ---------- shared card / modal handlers ---------- */

  function attachCardHandlers(grid) {
    grid.addEventListener("click", function (e) {
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

    var ingredients = (recipe.ingredients || []).map(function (ing) {
      return '<li class="ingredient-item flex items-start gap-3 cursor-pointer rounded-lg p-1.5 -m-1.5 hover:bg-amber-50/60 transition">' +
        '<span class="mt-0.5 w-5 h-5 shrink-0 rounded-md border border-slate-200 flex items-center justify-center">' +
        '<i class="fa-solid fa-check text-emerald-500 opacity-0 transition"></i></span>' +
        '<span class="text-sm text-slate-700">' + escapeHtml(ing) + "</span></li>";
    }).join("") || '<li class="text-sm text-slate-400">No ingredients listed.</li>';

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
      '<ul class="grid grid-cols-1 sm:grid-cols-2 gap-2">' + ingredients + "</ul></div>" +

      '<div><h4 class="font-bold text-slate-800 mb-3 flex items-center gap-2">' +
      '<i class="fa-solid fa-list-ol text-orange-500"></i> Instructions</h4>' +
      '<ol class="space-y-3">' + (steps || '<li class="text-sm text-slate-400">No instructions available.</li>') +
      "</ol></div>" +
      (youtube ? '<div class="flex justify-center">' + youtube + "</div>" : "") +
      "</div>" +

      '<div class="p-4 border-t border-slate-100 flex justify-end">' +
      '<button type="button" class="modal-close px-5 py-3 rounded-xl bg-slate-800 text-white text-sm font-bold ' +
      'hover:bg-slate-700 transition active:scale-95">Close</button></div></div>';
  }

  /* ---------- search / roulette ---------- */

  function collectQuery() {
    return state.query.join(", ");
  }

  function runSearch() {
    if (loading) return;
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
            openModal(data.selected_recipe);
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
    if (rouletteBtn) rouletteBtn.addEventListener("click", spinRoulette);
    if (clearBtn) clearBtn.addEventListener("click", function () {
      $("#results-section").classList.add("hidden");
      $("#empty-state").classList.add("hidden");
      $("#results-grid").innerHTML = "";
      state.query = [];
      var selected = $("#selected-ingredients");
      if (selected) selected.innerHTML = "";
    });
  }

  document.addEventListener("DOMContentLoaded", initExplore);
})();