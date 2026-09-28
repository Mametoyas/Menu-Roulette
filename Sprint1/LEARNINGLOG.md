<a id="top"></a>

[README](../README.md) | [Members](../MEMBERS.md) | [Plan](../PLAN.md) | [Design](../DESIGN.md) | [Sprint1](../Sprint1/README.md) | [Sprint2](../Sprint2/README.md) | [Sprint3](../Sprint3/README.md) | [Changelog](../CHANGELOG.md) | [Review](../SPRINT_REVIEW.md) | [Peer Eval](../PEER_EVALUATION.md)

# ประวัติการใช้ AI - Sprint 1 (AI Usage Log)

โปรเจกต์: Recipe Roulette (TheMealDB) | ช่วงงาน: 14-15/09/2569 | ทีม: Benz / Toey / Ter / Khong

## หมายเหตุด้านความถูกต้อง

- โค้ดในทุก AI Response ตรงกับไฟล์ที่ commit d261127 (Update Sprint1.md) ทุกตัวอักษร
- บทสนทนา User Prompt เป็นการเรียบเรียงใหม่จากหลักฐานในไฟล์ + git log + Sprint1.md ทุก Step จึงติดป้าย (เรียบเรียงใหม่)
- ขั้นตอนไหนหลักฐานไม่ระบุผู้ทำ จะเขียนว่าไม่ระบุชัด ไม่เดา

### Step 1: วางแผน Sprint 1 และแบ่งบทบาท (ผู้รับผิดชอบ: Benz, Planner) (เรียบเรียงใหม่)

**User Prompt:**
> ช่วยวางโครง Sprint 1 ของ Recipe Roulette หน่อย โจทย์คือรับวัตถุดิบจากผู้ใช้แล้วสุ่มแนะนำเมนู ยังไม่ต่อ API จริง ใช้ Mock Data ก่อน ขอ architecture แยก input/engine/test และ Definition of Done ที่ตรวจได้ ทีมมี Benz (planner), Toey/Ter (coder), Khong (debugger)

**AI Response:**
AI เสนอ layered แยก utils (clean input) / recipe_engine (mock + filter + random) / main (pipeline) / tests พร้อม DoD 4 ข้อ: input normalize, mock 5 เมนู, custom exception, PEP8 + pytest ผ่าน ทีมนำไปเขียน PLAN.md เอง

**สิ่งที่ทีมตรวจสอบ/ปรับเอง:** Planner เขียน PLAN.md และ DoD เอง, coder ทบทวนแผนจนตรงกันก่อนลงมือ (ตาม PLAN.md Phase 1)

### Step 2: เขียน src/utils.py (ผู้รับผิดชอบ: Toey, Coder) (เรียบเรียงใหม่)

**User Prompt:**
> เขียน src/utils.py ให้หน่อย มี clean_ingredient_input(raw_input) รับสตริงคั่นจุลภาค ตัดช่องว่าง ตัวพิมพ์เล็ก ตัดสัญลักษณ์ ตัดค่าว่าง/ซ้ำ เจอตัวเลขหรือค่าว่างให้ raise InvalidIngredientError ( subclass ของ ValueError) ใส่ docstring + type hints ด้วย

**AI Response:**
AI อธิบายว่าจะ validate 2 ชั้น (empty/numbers) แล้ว split-clean-dedup พร้อมโค้ดด้านล่าง

```python
"""Utility functions for string manipulation and input validation."""

import re


class InvalidIngredientError(ValueError):
    """Raised when the input contains invalid characters or numbers."""

    pass


def clean_ingredient_input(raw_input: str) -> list[str]:
    """Cleans and parses raw ingredient inputs from user.

    Args:
        raw_input (str): Raw comma-separated string (e.g., " Pork , Egg! ")

    Returns:
        list[str]: Cleaned list of unique ingredient names in lowercase.

    Raises:
        InvalidIngredientError: If input is empty or contains numbers.
    """
    if not raw_input or not raw_input.strip():
        raise InvalidIngredientError("Input cannot be empty.")

    # Reject numbers in ingredient strings
    if re.search(r"\d", raw_input):
        raise InvalidIngredientError("Ingredients must not contain numbers.")

    # Split by comma, strip whitespace, remove empty elements,
    # and convert to lowercase
    raw_list = raw_input.split(",")
    cleaned = []

    for item in raw_list:
        # Remove non-alphanumeric trailing/leading characters except spaces
        item_clean = re.sub(r"[^\w\s]", "", item).strip().lower()
        if item_clean and item_clean not in cleaned:
            cleaned.append(item_clean)

    if not cleaned:
        err_msg = "No valid ingredients found after sanitization."
        raise InvalidIngredientError(err_msg)

    return cleaned
```

**สิ่งที่ทีมตรวจสอบ/ปรับเอง:** รัน pytest เคส Pork/Egg/garlic แล้ว ต่อมาแก้ regex ให้คงช่องว่างในชื่อหลายคำ (ดู Step 6)

### Step 3: เขียน src/recipe_engine.py (ผู้รับผิดชอบ: Ter, Coder) (เรียบเรียงใหม่)

**User Prompt:**
> เขียน src/recipe_engine.py ให้หน่อย สร้าง MOCK_RECIPES 5 เมนู (idMeal/strMeal/strCategory/ingredients) เลียนโครง TheMealDB มีเมนูไก่ หมู ของหวาน มังสวิรัติ แล้วเขียน filter_recipes_by_ingredients (เจออย่างน้อย 1 อย่าง) กับ pick_random_recipe (ลิสต์ว่างคืน None)

**AI Response:**
AI อธิบายว่า mock 5 เมนูตาม schema แล้ว filter ด้วย any-match พร้อมโค้ดด้านล่าง

```python
"""Recipe search engine and mock dataset handling."""

import random
from typing import Dict, List, Optional

# Mock Data simulating TheMealDB API response structure[cite: 1, 3]
MOCK_RECIPES: List[Dict] = [
    {
        "idMeal": "52772",
        "strMeal": "Teriyaki Chicken Casserole",
        "strCategory": "Chicken",
        "ingredients": ["chicken", "rice", "soy sauce", "egg"],
    },
    {
        "idMeal": "52968",
        "strMeal": "Pork Souvlaki",
        "strCategory": "Pork",
        "ingredients": ["pork", "lemon", "olive oil", "garlic"],
    },
    {
        "idMeal": "52855",
        "strMeal": "Banana Pancakes",
        "strCategory": "Dessert",
        "ingredients": ["banana", "egg", "flour", "milk"],
    },
    {
        "idMeal": "52907",
        "strMeal": "Egg Fried Rice",
        "strCategory": "Vegetarian",
        "ingredients": ["rice", "egg", "garlic", "soy sauce"],
    },
    {
        "idMeal": "53013",
        "strMeal": "Garlic Butter Pork Chop",
        "strCategory": "Pork",
        "ingredients": ["pork", "garlic", "butter"],
    },
]


def filter_recipes_by_ingredients(
    user_ingredients: List[str], recipes: Optional[List[Dict]] = None
) -> List[Dict]:
    """
    Finds recipes containing at least one of the provided ingredients.
    """
    dataset = recipes if recipes is not None else MOCK_RECIPES
    matched = []

    for recipe in dataset:
        recipe_ingr = [ing.lower() for ing in recipe.get("ingredients", [])]
        # Check intersection between user query and recipe ingredients
        if any(ing in recipe_ingr for ing in user_ingredients):
            matched.append(recipe)

    return matched


def pick_random_recipe(matched_recipes: List[Dict]) -> Optional[Dict]:
    """Returns a random recipe from matched list, or None if list is empty."""
    if not matched_recipes:
        return None
    return random.choice(matched_recipes)
```

**สิ่งที่ทีมตรวจสอบ/ปรับเอง:** ตรวจว่า pork ได้ 2 เมนู, avocado ได้ 0 เมนู (ตาม test_sprint1.py)

### Step 4: เขียน src/main.py รวม pipeline (ผู้รับผิดชอบ: ทีม Coder - commit 1e70283 ไม่ระบุคนชัด) (เรียบเรียงใหม่)

**User Prompt:**
> เขียน src/main.py รวม pipeline หน่อย เรียก clean_ingredient_input แล้ว filter_recipes_by_ingredients แล้ว pick_random_recipe คืน dict มี status/query/match_count/selected_recipe ถ้า input ผิดให้ status error พร้อม message มีโหมด input/print ทดสอบด้วย

**AI Response:**
AI อธิบาย pipeline Clean -> Filter -> Random Pick ห่อ try-except InvalidIngredientError พร้อมโค้ดด้านล่าง

```python
"""Sprint 1 entry point verifying engine logic without GUI/CLI dependency."""

from utils import clean_ingredient_input, InvalidIngredientError
from recipe_engine import filter_recipes_by_ingredients, pick_random_recipe


def run_roulette_simulation(raw_input: str) -> dict:
    """Executes the pipeline: Clean -> Filter -> Random Pick."""
    try:
        cleaned_ingredients = clean_ingredient_input(raw_input)
        matches = filter_recipes_by_ingredients(cleaned_ingredients)
        selected = pick_random_recipe(matches)

        return {
            "status": "success",
            "query": cleaned_ingredients,
            "match_count": len(matches),
            "selected_recipe": selected,
        }
    except InvalidIngredientError as e:
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    # Test sample run
    sample_query = input("Enter the ingredients (example: 'Pork, Garlic'):")
    result = run_roulette_simulation(sample_query)
    print("Execution Result:", result)
```

**สิ่งที่ทีมตรวจสอบ/ปรับเอง:** รันตัวอย่าง Pork, Garlic แล้วได้ dict ครบ status/query/match_count/selected_recipe

### Step 5: เขียน tests/test_sprint1.py (ผู้รับผิดชอบ: Khong, Debugger) (เรียบเรียงใหม่)

**User Prompt:**
> เขียน tests/test_sprint1.py ให้หน่อย เทส clean_ingredient_input (ถูก/ตัวเลข/ค่าว่าง) กับ filter (เจอ pork 2 เมนู, avocado ไม่เจอ + pick คืน None) ใช้ pytest.raises จับ InvalidIngredientError

**AI Response:**
AI อธิบาย 5 เคส: valid/numeric/empty/filter-match/no-match พร้อมโค้ดด้านล่าง

```python
"""Automated unit tests for Sprint 1 logic validation."""

import pytest
from src.recipe_engine import (
    filter_recipes_by_ingredients,
    pick_random_recipe,
)
from src.utils import InvalidIngredientError, clean_ingredient_input


def test_clean_ingredient_input_valid():
    """Verify normalization of valid mixed case strings."""
    result = clean_ingredient_input(" Pork , Egg! , garlic ")
    assert result == ["pork", "egg", "garlic"]


def test_clean_ingredient_input_numeric_error():
    """Verify exception handling when numbers are passed."""
    with pytest.raises(InvalidIngredientError):
        clean_ingredient_input("pork, egg123")


def test_clean_ingredient_empty_error():
    """Verify exception on whitespace/empty inputs."""
    with pytest.raises(InvalidIngredientError):
        clean_ingredient_input("   ,  ")


def test_filter_recipes_success():
    """Verify correct recipe filtering logic."""
    matches = filter_recipes_by_ingredients(["pork"])
    assert len(matches) == 2
    assert all("pork" in r["ingredients"] for r in matches)


def test_filter_recipes_no_match():
    """Verify output when no ingredients match dataset."""
    matches = filter_recipes_by_ingredients(["avocado"])
    assert len(matches) == 0
    assert pick_random_recipe(matches) is None
```

**สิ่งที่ทีมตรวจสอบ/ปรับเอง:** รัน pytest ผ่าน 5 เทส (ดู Sprint1.md ตาราง QA)

### Step 6: แก้บั๊ก regex ตัดช่องว่างในวัตถุดิบหลายคำ (ผู้รับผิดชอบ: ทีม Coder - Sprint1.md ไม่ระบุคนชัด) (เรียบเรียงใหม่)

**User Prompt:**
> เจอบั๊ก: พิมพ์ soy sauce แล้ว regex ตัดช่องว่างในกลายเป็น soysauce ทำให้ filter ไม่เจอ ช่วยแก้ clean_ingredient_input ให้คงช่องว่างในชื่อ (ตัดเฉพาะสัญลักษณ์) แล้วยืนยันว่า soy sauce ยัง match เมนู Egg Fried Rice

**AI Response:**
AI ชี้ว่า regex เดิมลบช่องว่างในด้วย ต้องใช้ re.sub(r"[^\w\s]", "", item) คง \s ไว้ โค้ดหลังแก้คือเวอร์ชันใน Step 2 บรรทัด item_clean (ไฟล์สุดท้ายที่ commit ผ่านเทสแล้ว)

**สิ่งที่ทีมตรวจสอบ/ปรับเอง:** บันทึกใน Sprint1.md หัวข้อ Whoops ว่าแก้ regex ใน utils.py แล้ว

หลักฐาน: Sprint1.md ระบุว่า regex แรกทำ soysauce แล้วแก้ให้คงช่องว่าง โค้ด regex ต้นฉบับก่อนแก้ไม่มีใน git history จึงอ้างได้เฉพาะผลลัพธ์หลังแก้

### Step 7: ขอ requirements.txt + เวอร์ชัน Python (ผู้รับผิดชอบ: ทีม - commit 6beaa98 add how to install) (เรียบเรียงใหม่)

**User Prompt:**
> ขอ requirements.txt สำหรับ Sprint 1 หน่อย เอาแค่เทสกับคุณภาพโค้ด (pytest, coverage, flake8, black) ระบุเวอร์ชันขั้นต่ำ และบอกเวอร์ชัน Python ที่ใช้ (README ใช้ 3.11)

**AI Response:**
AI ให้ requirements 5 บรรทัด (รวม requests ที่เผื่อ Sprint 2-3) และย้ำว่า Sprint 1 ยังไม่มี .python-version ใน git (ไฟล์นี้เกิดทีหลัง) เวอร์ชันอ้างอิงจาก README/CI คือ Python 3.11 พร้อมโค้ดด้านล่าง

```text
# Testing & Code Quality (Sprint 1)
pytest>=7.4.0
pytest-cov>=4.1.0
flake8>=6.1.0
black>=23.9.0

# API & Data Handling (สำหรับ Sprint 2 และ 3)
requests>=2.31.0
```

**สิ่งที่ทีมตรวจสอบ/ปรับเอง:** pip install แล้วรัน pytest + flake8 ผ่านก่อนส่ง 18/09/2569

## ตารางสรุป

| ขั้นตอน | ไฟล์ | ผู้รับผิดชอบ | สิ่งที่ AI ช่วย | สิ่งที่ทีมทำเอง |
|---|---|---|---|---|
| 1 วางแผน | PLAN.md (ไม่รวมใน log) | Benz | เสนอโครง utils/engine/main/test + DoD | เขียน PLAN.md/DoD เอง |
| 2 input utils | src/utils.py | Toey | โค้ด clean + exception + docstring | รันเทส + แก้ regex (Step 6) |
| 3 mock engine | src/recipe_engine.py | Ter | mock 5 เมนู + filter + random | ตรวจเคส pork/avocado |
| 4 pipeline | src/main.py | ทีม Coder (ไม่ระบุชัด) | โค้ด pipeline + dict ผลลัพธ์ | รันตัวอย่าง Pork, Garlic |
| 5 tests | tests/test_sprint1.py | Khong | 5 เคส valid/numeric/empty/match/nomatch | รัน pytest บันทึก QA |
| 6 bugfix | src/utils.py | ทีม Coder (ไม่ระบุชัด) | ชี้สาเหตุ regex + วิธีคง \s | แก้โค้ด + บันทึก Whoops |
| 7 env | requirements.txt | ทีม (ไม่ระบุชัด) | ลิสต์ dependency + เวอร์ชัน | pip install + รัน QA |

---

[Back to top](#top) | [README](../README.md)
