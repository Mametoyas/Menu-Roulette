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
|              (CLI UI)               |
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
| Interface | CLI / GUI (Tkinter) |
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

```bash
python src/main.py
```

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

## Sprint 2 — Back-End & API Integration 🔄

**Focus:** Transition from mock data to real-time TheMealDB API.

**Architecture & Tech Stack:**
- **HTTP Client**: `requests` package
- **Testing**: `pytest` + `unittest.mock` / `requests-mock`

```text
src/
├── api_client.py      # TheMealDB API requests & JSON parsing
└── recipe_engine.py   # Business logic connecting API and Filtering
tests/
└── test_api.py        # Mock unit tests for API calls and error handling
```

---

## Sprint 3 — GUI Development & Full-Stack Integration 📋

**Focus:** Develop a GUI and integrate it with the back-end engine from Sprints 1 & 2.

**Architecture & Tech Stack:**

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| GUI Framework | `Tkinter` / `CustomTkinter` | Main UI rendering |
| Threading | `threading` (stdlib) | Non-blocking API calls |
| Presentation | Views & Modals | Search, Recipe Card, Detail, Favorites |

```text
src/
├── gui/
│   ├── app.py             # Main window & app entry point
│   ├── search_view.py     # Ingredient input & search bar
│   ├── recipe_card.py     # Recipe result card component
│   ├── detail_modal.py    # Full recipe detail popup
│   └── favorites_view.py  # Saved/favourites management screen
tests/
└── test_gui.py            # GUI integration & interaction tests
```

| Role | Member | Deliverable |
| :--- | :--- | :--- |
| Planner | Jane | Sprint plan, architecture diagram, DoD |
| Coder | Toey | `search_view.py`, input binding, threading |
| Coder | Ter | `recipe_card.py`, `detail_modal.py`, `favorites_view.py` |
| Debugger | Khong | GUI tests, QA report (`Sprint3.md`) |

**Definition of Done:**
1. GUI launches without errors via `python src/main.py`.
2. Ingredient search triggers real API call and displays results as recipe cards.
3. Clicking a recipe card opens a detail modal with full information.
4. Favorites can be saved, viewed, and removed.
5. All API calls run on background threads — UI remains responsive at all times.
6. PEP 8 compliant code passing all `pytest` test cases.
