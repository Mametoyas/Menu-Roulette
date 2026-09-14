# Menu Roulette

Random recipe suggestion engine based on available ingredients.

## Setup

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

## Run

```bash
python -m src.main
```

## Test

```bash
pytest
```
