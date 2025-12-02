"""
Evolution system with branching evolution tree
"""

from ..config import EVOLUTION_STAGE_1_LEVEL, EVOLUTION_STAGE_2_LEVEL, EVOLUTION_STAGE_3_LEVEL


# Evolution tree structure
# Each form has: name, stage, stats (modifiers), skills, description, color
EVOLUTION_TREE = {
    # Stage 0 - Starting form
    "larva": {
        "name": "Larva",
        "stage": 0,
        "hp_mult": 1.0,
        "atk_mult": 1.0,
        "def_mult": 1.0,
        "speed_mult": 1.0,
        "skills": [],
        "description": "A weak creature waiting to evolve",
        "color": (150, 150, 150),
        "evolves_to": ["beastling", "drakelet", "rockcore"]
    },

    # Stage 1 - First evolution choices
    "beastling": {
        "name": "Beastling",
        "stage": 1,
        "hp_mult": 1.3,
        "atk_mult": 1.5,
        "def_mult": 1.1,
        "speed_mult": 1.2,
        "skills": [],
        "description": "A fierce melee predator",
        "color": (200, 100, 50),
        "evolves_to": ["direwolf"]
    },

    "drakelet": {
        "name": "Drakelet",
        "stage": 1,
        "hp_mult": 1.2,
        "atk_mult": 1.4,
        "def_mult": 1.0,
        "speed_mult": 1.1,
        "skills": ["fire_breath"],
        "description": "A young dragon with fire powers",
        "color": (255, 100, 100),
        "evolves_to": ["youngdragon"]
    },

    "rockcore": {
        "name": "Rock Core",
        "stage": 1,
        "hp_mult": 1.5,
        "atk_mult": 1.1,
        "def_mult": 1.5,
        "speed_mult": 0.9,
        "skills": ["stone_punch"],
        "description": "A defensive stone creature",
        "color": (100, 100, 120),
        "evolves_to": ["stonegolem"]
    },

    # Stage 2 - Second evolution
    "direwolf": {
        "name": "Dire Wolf",
        "stage": 2,
        "hp_mult": 1.6,
        "atk_mult": 2.0,
        "def_mult": 1.3,
        "speed_mult": 1.5,
        "skills": [],
        "description": "A massive predator",
        "color": (180, 80, 30),
        "evolves_to": ["fenrir"]
    },

    "youngdragon": {
        "name": "Young Dragon",
        "stage": 2,
        "hp_mult": 1.5,
        "atk_mult": 1.8,
        "def_mult": 1.2,
        "speed_mult": 1.3,
        "skills": ["fire_breath", "wing_buffet"],
        "description": "A maturing dragon with more power",
        "color": (255, 50, 50),
        "evolves_to": ["ancientdragon", "skywhale"]
    },

    "stonegolem": {
        "name": "Stone Golem",
        "stage": 2,
        "hp_mult": 2.0,
        "atk_mult": 1.4,
        "def_mult": 2.0,
        "speed_mult": 0.8,
        "skills": ["stone_punch", "earthquake"],
        "description": "A massive stone guardian",
        "color": (80, 80, 100),
        "evolves_to": ["titangolem"]
    },

    # Stage 3 - Final evolutions
    "fenrir": {
        "name": "Fenrir",
        "stage": 3,
        "hp_mult": 2.0,
        "atk_mult": 2.5,
        "def_mult": 1.5,
        "speed_mult": 1.8,
        "skills": [],
        "description": "Legendary wolf of destruction",
        "color": (150, 50, 20),
        "evolves_to": []
    },

    "ancientdragon": {
        "name": "Ancient Dragon",
        "stage": 3,
        "hp_mult": 2.2,
        "atk_mult": 2.3,
        "def_mult": 1.8,
        "speed_mult": 1.5,
        "skills": ["fire_breath", "wing_buffet"],
        "description": "Elder dragon of immense power",
        "color": (200, 20, 20),
        "evolves_to": []
    },

    "skywhale": {
        "name": "Sky Whale",
        "stage": 3,
        "hp_mult": 3.0,
        "atk_mult": 1.8,
        "def_mult": 2.0,
        "speed_mult": 1.2,
        "skills": ["tidal_crash", "leviathan_roar"],
        "description": "Leviathan of the skies",
        "color": (100, 150, 255),
        "evolves_to": []
    },

    "titangolem": {
        "name": "Titan Golem",
        "stage": 3,
        "hp_mult": 3.5,
        "atk_mult": 2.0,
        "def_mult": 2.5,
        "speed_mult": 0.7,
        "skills": ["stone_punch", "earthquake"],
        "description": "Colossal stone titan",
        "color": (60, 60, 80),
        "evolves_to": []
    }
}


def get_evolution_options(player):
    """
    Get available evolution options for the player
    Returns list of form IDs that player can evolve into
    """
    current_form_data = EVOLUTION_TREE.get(player.current_form)
    if not current_form_data:
        return []

    evolves_to = current_form_data.get("evolves_to", [])

    # Check level requirements
    stage = current_form_data["stage"]
    required_level = 0

    if stage == 0:
        required_level = EVOLUTION_STAGE_1_LEVEL
    elif stage == 1:
        required_level = EVOLUTION_STAGE_2_LEVEL
    elif stage == 2:
        required_level = EVOLUTION_STAGE_3_LEVEL

    if player.level >= required_level and evolves_to:
        return evolves_to

    return []


def evolve_player(player, new_form_id):
    """
    Evolve the player to a new form
    Updates stats, appearance, and skills
    """
    new_form = EVOLUTION_TREE.get(new_form_id)
    if not new_form:
        return False

    old_form = EVOLUTION_TREE.get(player.current_form)

    # Update form
    player.current_form = new_form_id
    player.evolution_stage = new_form["stage"]

    # Calculate stat changes
    # Remove old multipliers, apply new ones
    if old_form:
        player.max_hp = int(player.max_hp / old_form["hp_mult"] * new_form["hp_mult"])
        player.base_atk = int(player.base_atk / old_form["atk_mult"] * new_form["atk_mult"])
        player.base_def = int(player.base_def / old_form["def_mult"] * new_form["def_mult"])
        player.speed = player.speed / old_form["speed_mult"] * new_form["speed_mult"]
    else:
        player.max_hp = int(player.max_hp * new_form["hp_mult"])
        player.base_atk = int(player.base_atk * new_form["atk_mult"])
        player.base_def = int(player.base_def * new_form["def_mult"])
        player.speed = player.speed * new_form["speed_mult"]

    # Heal to full on evolution
    player.hp = player.max_hp

    # Update appearance
    player.update_color(new_form["color"])

    # Update skills (will be set by main game when skills are loaded)
    return True
