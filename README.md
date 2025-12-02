# Monster Evolution RPG

A 2D roguelite monster-evolution RPG built with Python and Arcade.

## Overview

Start as a weak larva and evolve into powerful legendary creatures like Ancient Dragons, Sky Whales, or Titan Golems. Fight through procedurally generated dungeons, collect traits, unlock skills, and build unique character combinations.

## Features

- **Evolution System**: Branch through a multi-stage evolution tree with unique forms
- **Trait System**: Collect passive abilities like Lifesteal, Armor Shell, and Regrowth
- **Active Skills**: Unlock powerful abilities based on your evolution path
- **Roguelite Gameplay**: Permadeath with procedurally generated floors
- **Build Diversity**: Combine evolutions, traits, and stats for varied playstyles

## Installation

### Prerequisites

- Python 3.7 or higher
- Linux operating system (Kali or similar)

### Setup

1. Clone the repository:
```bash
cd /home/moon/Projects/game
```

2. Create a virtual environment (recommended):
```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Game

### Option 1: Bash launcher (recommended)
```bash
./run_game
```

Make sure the script is executable:
```bash
chmod +x run_game
```

### Option 2: Python wrapper
```bash
python run_game.py
```

### Option 3: Direct module execution
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
python -m cli_game.main
```

## Controls

### Movement
- **WASD** or **Arrow Keys**: Move your monster
- **SPACE**: Basic attack

### Skills
- **Q**: Use first skill
- **E**: Use second skill

### Menus
- **W/S** or **Up/Down**: Navigate options
- **A/D** or **Left/Right**: Navigate evolution choices (horizontal)
- **ENTER** or **SPACE**: Confirm selection
- **R**: Restart after game over

## Gameplay Guide

### Evolution Stages

**Stage 0: Larva**
- Starting form, weak stats
- Evolve at level 3

**Stage 1: First Evolution**
- **Beastling**: Melee predator (high attack, speed)
- **Drakelet**: Fire dragon (balanced, gains Fire Breath skill)
- **Rock Core**: Defensive tank (high HP/defense, gains Stone Punch skill)

**Stage 2: Second Evolution**
- **Dire Wolf**: From Beastling, massive damage dealer
- **Young Dragon**: From Drakelet, gains Wing Buffet skill
- **Stone Golem**: From Rock Core, gains Earthquake skill

**Stage 3: Final Evolution**
- **Fenrir**: Ultimate wolf predator
- **Ancient Dragon**: Elder dragon of immense power
- **Sky Whale**: Leviathan with Tidal Crash and roar abilities
- **Titan Golem**: Colossal stone fortress

### Traits

Traits are passive abilities chosen after clearing each floor:

- **Lifesteal**: Heal 15% of damage dealt
- **Armor Shell**: Reduce incoming damage by 20%
- **Quick Fury**: 25% faster attack speed
- **Regrowth**: Regenerate 2 HP per second
- **Iron Hide**: +5 Defense
- **Berserker Rage**: +8 Attack
- **Deadly Precision**: +10% Critical Hit Chance
- **Vitality Boost**: +30 Max HP

### Progression

1. Kill enemies to gain XP
2. Level up to choose stat upgrades (HP/ATK/DEF)
3. Reach level thresholds (3, 6, 10) to evolve
4. Clear floors to choose traits
5. Floors get progressively harder with scaling enemy stats

## Project Structure

```
cli_game/
├── src/
│   └── cli_game/           # Main game package
│       ├── main.py         # Game loop and window
│       ├── config.py       # Configuration constants
│       ├── entities/       # Player and enemy classes
│       │   ├── player.py
│       │   └── enemies.py
│       ├── systems/        # Game systems
│       │   ├── evolution.py
│       │   ├── traits.py
│       │   ├── skills.py
│       │   ├── combat.py
│       │   └── world.py
│       └── ui/             # HUD and menus
│           ├── hud.py
│           └── menus.py
├── run_game               # Bash launcher script
├── run_game.py           # Python launcher wrapper
└── requirements.txt      # Dependencies
```

## Extending the Game

### Adding New Evolutions

Edit `src/cli_game/systems/evolution.py` and add entries to `EVOLUTION_TREE`:

```python
"new_form": {
    "name": "Display Name",
    "stage": 2,
    "hp_mult": 1.5,
    "atk_mult": 1.8,
    # ... other stats
}
```

### Adding New Traits

Edit `src/cli_game/systems/traits.py`:

1. Create a new class inheriting from `Trait`
2. Override methods like `modify_atk()`, `modify_def()`, etc.
3. Add the class to `TRAIT_REGISTRY`

### Adding New Skills

Edit `src/cli_game/systems/skills.py`:

1. Create a new class inheriting from `Skill`
2. Implement `_execute()` method
3. Add to `SKILL_REGISTRY`
4. Reference in evolution forms

### Adding New Enemies

Edit `src/cli_game/entities/enemies.py`:

1. Create a new class inheriting from `Enemy`
2. Set stats in `__init__`
3. Add to spawn pool in `src/cli_game/systems/world.py`

## Configuration

Game constants can be adjusted in `src/cli_game/config.py`:

- Screen resolution
- Tile sizes and map dimensions
- Player starting stats
- Combat parameters
- XP and evolution thresholds
- Enemy spawn counts
- Floor scaling factors

## Troubleshooting

### Game won't start
- Ensure Python 3.7+ is installed: `python --version`
- Verify Arcade is installed: `pip list | grep arcade`
- Check that you're in the repo root directory

### Import errors
- Make sure you're running from the repo root
- Try: `export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"`

### Permission denied on run_game
- Make executable: `chmod +x run_game`

## License

This is a prototype/educational project. Feel free to extend and modify.

## Credits

Built with Python and the Arcade library.
