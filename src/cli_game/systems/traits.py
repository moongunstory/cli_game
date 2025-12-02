"""
Trait/perk system with passive abilities
"""

import random
import time


class Trait:
    """Base trait class"""

    def __init__(self, trait_id, name, description):
        self.id = trait_id
        self.name = name
        self.description = description

    def apply(self, player):
        """Apply trait to player (called when trait is acquired)"""
        pass

    def modify_atk(self, atk):
        """Modify attack stat"""
        return atk

    def modify_def(self, defense):
        """Modify defense stat"""
        return defense

    def modify_crit_chance(self, crit_chance):
        """Modify crit chance"""
        return crit_chance

    def modify_incoming_damage(self, damage):
        """Modify incoming damage"""
        return damage

    def on_damage_dealt(self, damage):
        """Called when player deals damage, returns lifesteal amount"""
        return 0

    def update(self, player, delta_time):
        """Called each frame"""
        pass


class LifestealTrait(Trait):
    """Heal for a portion of damage dealt"""

    def __init__(self):
        super().__init__(
            "lifesteal",
            "Lifesteal",
            "Heal 15% of damage dealt"
        )
        self.lifesteal_percent = 0.15

    def on_damage_dealt(self, damage):
        return int(damage * self.lifesteal_percent)


class PredatorInstinctTrait(Trait):
    """Increased damage vs low HP enemies"""

    def __init__(self):
        super().__init__(
            "predator_instinct",
            "Predator Instinct",
            "Deal 25% more damage to enemies below 30% HP"
        )

    def modify_atk(self, atk):
        # This would need context about target HP, simplified for now
        return atk


class ArmorShellTrait(Trait):
    """Flat damage reduction"""

    def __init__(self):
        super().__init__(
            "armor_shell",
            "Armor Shell",
            "Reduce incoming damage by 20%"
        )

    def modify_incoming_damage(self, damage):
        return int(damage * 0.8)


class QuickFuryTrait(Trait):
    """Increased attack speed"""

    def __init__(self):
        super().__init__(
            "quick_fury",
            "Quick Fury",
            "Reduce attack cooldown by 25%"
        )

    def apply(self, player):
        player.attack_cooldown *= 0.75


class RegrowthTrait(Trait):
    """Periodic HP regeneration"""

    def __init__(self):
        super().__init__(
            "regrowth",
            "Regrowth",
            "Regenerate 2 HP per second"
        )
        self.regen_per_second = 2
        self.accumulated_time = 0

    def update(self, player, delta_time):
        self.accumulated_time += delta_time
        if self.accumulated_time >= 1.0:
            player.heal(self.regen_per_second)
            self.accumulated_time = 0


class RuneSurgeTrait(Trait):
    """Increased skill power"""

    def __init__(self):
        super().__init__(
            "rune_surge",
            "Rune Surge",
            "Skills deal 30% more damage"
        )

    # This would need integration with skill damage calculation


class IronHideTrait(Trait):
    """Increased defense"""

    def __init__(self):
        super().__init__(
            "iron_hide",
            "Iron Hide",
            "+5 Defense"
        )
        self.defense_bonus = 5

    def modify_def(self, defense):
        return defense + self.defense_bonus


class BerserkerRageTrait(Trait):
    """Increased attack"""

    def __init__(self):
        super().__init__(
            "berserker_rage",
            "Berserker Rage",
            "+8 Attack"
        )
        self.attack_bonus = 8

    def modify_atk(self, atk):
        return atk + self.attack_bonus


class DeadlyPrecisionTrait(Trait):
    """Increased crit chance"""

    def __init__(self):
        super().__init__(
            "deadly_precision",
            "Deadly Precision",
            "+10% Critical Hit Chance"
        )

    def modify_crit_chance(self, crit_chance):
        return crit_chance + 0.10


class VitalityBoostTrait(Trait):
    """Increased max HP"""

    def __init__(self):
        super().__init__(
            "vitality_boost",
            "Vitality Boost",
            "+30 Max HP"
        )
        self.hp_bonus = 30

    def apply(self, player):
        player.max_hp += self.hp_bonus
        player.hp += self.hp_bonus


# Registry of all available traits
TRAIT_REGISTRY = [
    LifestealTrait,
    ArmorShellTrait,
    QuickFuryTrait,
    RegrowthTrait,
    IronHideTrait,
    BerserkerRageTrait,
    DeadlyPrecisionTrait,
    VitalityBoostTrait,
]


def get_random_traits(count=3, exclude_ids=None):
    """
    Get random traits for selection
    exclude_ids: list of trait IDs to exclude (already owned)
    """
    if exclude_ids is None:
        exclude_ids = set()
    else:
        exclude_ids = set(exclude_ids)

    available = [t for t in TRAIT_REGISTRY if t().id not in exclude_ids]

    if len(available) <= count:
        return [t() for t in available]

    selected_classes = random.sample(available, count)
    return [t() for t in selected_classes]
