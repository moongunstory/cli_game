"""
Combat system with damage calculation
"""

import random
from ..config import BASE_CRIT_MULTIPLIER


def calculate_damage(attacker, defender):
    """
    Calculate damage from attacker to defender
    Takes into account: base attack, defense, crit chance
    """
    # Base damage with some variance
    base_damage = attacker.atk + random.randint(-2, 2)

    # Critical hit check
    is_crit = random.random() < attacker.crit_chance
    if is_crit:
        base_damage = int(base_damage * BASE_CRIT_MULTIPLIER)

    # Apply defense
    final_damage = max(1, base_damage - defender.defense)

    return final_damage
