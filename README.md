# Recipe Roulette

## Introduction

Recipe Roulette is a Python-based recipe recommendation system that helps users decide what to cook based on the ingredients they have.

The system uses the TheMealDB API as an external recipe data source to retrieve information such as meal names, categories, areas, ingredients, measurements, and cooking instructions.

Instead of manually searching through many recipes, users can provide their available ingredients and let Recipe Roulette find suitable meals and randomly recommend one.

---

## Objective

The objectives of Recipe Roulette are:

* Reduce the difficulty of deciding what to cook.
* Recommend recipes based on ingredients available to the user.
* Retrieve recipe information from an external API.
* Apply searching, filtering, sorting, and ranking algorithms to recipe data.
* Validate user input and handle invalid input or API errors.
* Demonstrate modular programming and layered software architecture.
* Prepare the system for future additional features.

---

## Problem

People often have ingredients at home but do not know what meals they can make with them.

The main problems are:

1. **Difficulty deciding what to cook**

   Users may have several ingredients but cannot think of suitable recipes.

2. **Time-consuming recipe searching**

   Manually searching for recipes for each available ingredient can take a significant amount of time.

3. **Ingredient mismatch**

   A recipe may require ingredients that the user does not have.

4. **Too many choices**

   Searching through a large number of recipes can make decision-making more difficult.

5. **Lack of variety**

   Users may repeatedly choose familiar meals instead of discovering new recipes.

---

## Solution

Recipe Roulette provides a simple solution:

> Enter your available ingredients, search for suitable recipes, process the results, and randomly recommend a recipe.

The system uses TheMealDB API as the external recipe data source.

### Basic Workflow

```text
User
  |
  v
Enter Ingredients
  |
  v
Input Validation
  |
  v
Recipe Search
  |
  v
TheMealDB API
  |
  v
Recipe Data
  |
  v
Filter / Score Recipes
  |
  v
Random Selection
  |
  v
Recommended Recipe
```

---

# Project Architecture

Recipe Roulette follows a layered architecture that separates the user interface, business logic, and data access.

```text
+-------------------------------------+
|         Presentation Layer          |
|            (Web UI / Flask)         |
+------------------+------------------+
                   |
                   v
+-------------------------------------+
|         Business Logic Layer        |
|      (Validation / Scoring /        |
|       Filtering / Selection)        |
+------------------+------------------+
                   |
                   v
+-------------------------------------+
|           Data Access Layer         |
|         (TheMealDB API Client)      |
+------------------+------------------+
                   |
                   v
+-------------------------------------+
|             TheMealDB               |
|          External Recipe API        |
+-------------------------------------+
```

### 1. Presentation Layer

Responsibilities include:

* Display menus
* Receive ingredient input
* Display search results
* Display recommended recipes
* Handle user commands

### 2. Business Logic Layer

Responsibilities include:

* Validate ingredients
* Search recipes
* Filter recipes
* Calculate recipe scores
* Sort recipes
* Select a random recipe
* Apply recommendation rules

### 3. Data Access Layer

Responsibilities include:

* Send HTTP requests
* Receive API responses
* Parse JSON data
* Extract recipe information
* Handle API connection errors

---

# TheMealDB API

Recipe Roulette uses TheMealDB API as its external recipe data source.
Official API documentation: https://www.themealdb.com/api.php

## API Endpoints

| Endpoint                      | Purpose                      |
| ----------------------------- | ---------------------------- |
| `search.php?s=meal`           | Search for a meal by name    |
| `search.php?f=a`              | Search meals by first letter |
| `lookup.php?i=52772`          | Get a meal by ID             |
| `random.php`                  | Get a random meal            |
| `categories.php`              | Get meal categories          |
| `filter.php?i=chicken_breast` | Filter meals by ingredient   |
| `filter.php?c=Seafood`        | Filter meals by category     |
| `filter.php?a=Thai`           | Filter meals by area         |

---

# Algorithm

## 1. Input Validation

1. Removes unnecessary whitespace.
2. Normalizes ingredient names.
3. Removes empty values.
4. Removes duplicate ingredients.
5. Checks whether at least one ingredient was provided.

## 2. Recipe Search

For each ingredient, Recipe Roulette requests matching recipes from TheMealDB and combines the results into a candidate recipe set.

## 3. Remove Duplicate Recipes

The system removes duplicate recipes using the recipe ID to prevent the same recipe from receiving an unfair advantage.

## 4. Recipe Scoring

```text
Score = Number of matched user ingredients / Number of user ingredients
```

## 5. Filtering

Recipes are filtered by minimum ingredient match, category, area, and available recipe information.

## 6. Random Recommendation

After filtering and ranking, the system randomly selects one recipe from the best-matching candidates.

---

# Overall Algorithm

```text
START
  |
  v
Get ingredients from user
  |
  v
Validate and normalize input
  |
  v
For each ingredient
  |
  +--> Request TheMealDB
  |
  +--> Collect recipe IDs
  |
  v
Remove duplicate recipes
  |
  v
Retrieve recipe details
  |
  v
Calculate ingredient-match score
  |
  v
Filter candidates
  |
  v
Sort candidates by score
  |
  v
Randomly select from suitable candidates
  |
  v
Display recommended recipe
  |
  v
END
```

---

# Technology Stack

| Component | Technology |
| :--- | :--- |
| Language | Python 3.11 |
| API | TheMealDB API |
| Data Format | JSON |
| Architecture | Layered Architecture |
| Interface | CLI / Web (Flask + HTML/CSS/JS) |
| Version Control | Git / GitHub |

---

# Setup

### Option 1: venv

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### Option 2: Anaconda

```bash
conda create -n menu-roulette python=3.11
conda activate menu-roulette
pip install -r requirements.txt
```

# Run

### CLI (Sprints 1–2)

```bash
python src/main.py
```

### Web App (Sprint 3)

**Live deployment:** https://recipe-roulette-seven.vercel.app/

```bash
python src/web_app.py
# open http://127.0.0.1:5000 in your browser
```

# Deploy (Vercel)

Recipe Roulette runs on Vercel as a Python (Flask) application under a single
Vercel Function.

Live URL: https://recipe-roulette-seven.vercel.app/


# Test

```bash
pytest
```

---

# Project Status

## Sprint 1 — Base Logic & Engine ✅

**Focus:** Core modular functions, mock data engine, and input sanitization.

| Role | Member | Deliverable |
| :--- | :--- | :--- |
| Planner | Benz | Architecture specification, DoD definition, PLAN.md |
| Coder | Toey | Text utilities, data cleaning, input validation (`src/utils.py`) |
| Coder | Ter | Mock recipe dataset and matching engine (`src/recipe_engine.py`) |
| Debugger | Khong | Unit testing, edge-case validation, QA report (`tests/test_sprint1.py`) |

**Definition of Done:**
1. Input string correctly trimmed, lowercased, and converted into clean lists.
2. Mock dataset contains at least 5 structured recipes matching TheMealDB schema.
3. Edge cases (empty input, numeric symbols, no matching recipe) handled with custom exceptions.
4. PEP 8 compliant code passing all `pytest` test cases.

---

## Sprint 2 — Back-End & API Integration ✅

**Focus:** Transition from mock data to real-time TheMealDB API, CI/CD Automation, and Kanban Execution.

**Architecture & Tech Stack:**
- **HTTP Client**: `requests` package
- **Testing**: `pytest` + `unittest.mock`
- **CI/CD**: GitHub Actions (`.github/workflows/test.yml`)
- **Project Management**: GitHub Projects (Kanban Board)

```text
src/
├── api_client.py      # TheMealDB API requests, JSON parsing & error handling
├── recipe_engine.py   # Match scoring, filtering & random recommendation
├── main.py            # CLI application entry point
└── utils.py           # Input cleaning & validation (from Sprint 1)
tests/
├── test_utils.py      # Input validation tests
├── test_api.py        # API client tests using unittest.mock
└── test_engine.py     # Business logic & recommendation engine tests
```

| Role | Member | Deliverable |
| :--- | :--- | :--- |
| Planner | Toey | Kanban Board management, Sprint plan, README/PLAN updates, Git branching strategy |
| Coder | Khong | `src/api_client.py` — TheMealDB API client, `.env` config, and error handling |
| Coder | Benz | `src/recipe_engine.py` — match score, filtering & random recommendation |
| Debugger | Ter | Unit tests (`tests/`), CI/CD workflow, QA report |

---

## Sprint 3 — Web Application Development & Full-Stack Integration ✅

**Focus:** Develop a Web Application (Flask) and integrate it with the back-end engine from Sprints 1 & 2. The UI follows the `DESIGN.md` design system.

**Architecture & Tech Stack:**

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| Web Framework | `Flask` | HTTP server, routing, request handling |
| Templating | Jinja2 (Flask) | Server-side HTML rendering |
| Frontend | HTML5 + CSS (Tailwind CDN) + JS (`fetch`) | Responsive UI, detail modal, loading bar, roulette spin |
| State | In-Memory module store | Selected ingredients & favorites persistence |
| Testing | `pytest` + Flask test client | Route & full-flow tests |

```text
src/
├── web_app.py          # Flask app, routes & app entry point
templates/
├── base.html           # Shared layout: header nav, footer, modal container
├── index.html          # Explore — ingredient input, chips, search/roulette, loading bar
└── _results_section.html  # Shared results grid + empty state partial
static/
├── css/style.css       # Custom styles layered on top of Tailwind
└── js/app.js           # Client interactivity: fetch search, modal, loading, spin
tests/
└── test_web.py         # Flask route & end-to-end integration tests
```

| Endpoint | Purpose |
| :--- | :--- |
| `GET /` | Explore page (hero, ingredient input, results) |
| `POST /api/search` | `{ingredients}` → back-end engine → JSON result (async `fetch`) |
| `GET /recipe/<id>` | Full recipe detail JSON (modal data) |

| Role | Member | Deliverable |
| :--- | :--- | :--- |
| Planner | Jane | Sprint plan, architecture diagram, DoD, README update |
| Coder | Toey | `web_app.py` routes, search flow binding, back-end integration |
| Coder | Ter | `templates/` + `static/` UI: recipe cards, detail modal, loading bar |
| Debugger | Khong | `test_web.py` tests, CI workflow update, QA report (`Sprint3.md`) |

**Definition of Done:**
1. Web app launches without errors via `python src/web_app.py` and opens at `http://127.0.0.1:5000`.
2. Ingredient search on the web page triggers a real TheMealDB API call and renders results as recipe cards; a loading progress bar appears below the Search bar while fetching.
3. Clicking a recipe card opens a detail modal with full information (ingredients, measurements, instructions).
4. The roulette button randomly recommends one recipe and opens it in the modal.
5. API calls run server-side in Flask routes; the page stays responsive via async `fetch` without full-page reloads.
6. PEP 8 compliant code passing all `pytest` unit test cases (including new `test_web.py`).
