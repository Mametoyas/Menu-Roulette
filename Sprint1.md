# Sprint 1 Quality Assurance Report

**Project**: Recipe Roulette  
**Lead QA**: Khong  

### Edge Case Test Results

| Test Case | Input | Expected Output | Actual Output | Status |
| :--- | :--- | :--- | :--- | :--- |
| Valid Input | `" Pork , Egg! , garlic "` | `['pork', 'egg', 'garlic']` | `['pork', 'egg', 'garlic']` returned | PASSED |
| Numeric Input | `"pork, egg123"` | Raise `InvalidIngredientError` | `InvalidIngredientError` raised | PASSED |
| Empty Input | `"   ,  "` | Raise `InvalidIngredientError` | `InvalidIngredientError` raised | PASSED |
| Filter Match | `["pork"]` | 2 recipes containing `pork` | 2 matches returned | PASSED |
| No Match | `["avocado"]` | 0 matches, `pick_random_recipe` returns `None` | `[]` and `None` returned | PASSED |

![Sprint 1 Report](img/Sprint1_report.png)

### Retrospective (Wow! & Whoops!)
- **Wow!**: Base engine pipeline runs completely decoupled from UI, making pytest mocking fast and reliable.
- **Whoops!**: Initial regex stripped valid inner spaces in multi-word ingredients (e.g., "soy sauce" became "soysauce"). Fixed by refining regex in `utils.py`.