"""
Player entity with stats, evolution, and combat
"""

import arcade
import time
from ..config import *
from ..systems.combat import calculate_damage


class MonsterPlayer(arcade.Sprite):
    """The player-controlled monster with evolution capabilities"""

    def __init__(self, x, y):
        super().__init__()

        # Visual
        self.center_x = x
        self.center_y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.color = COLOR_PLAYER
        self._create_texture()

        # Core stats
        self.max_hp = PLAYER_START_HP
        self.hp = self.max_hp
        self.base_atk = PLAYER_START_ATK
        self.base_def = PLAYER_START_DEF
        self.speed = PLAYER_SPEED
        self.base_crit_chance = BASE_CRIT_CHANCE
        self.evo_power = 1.0

        # Progression
        self.xp = 0
        self.level = 1
        self.xp_to_next_level = XP_PER_LEVEL
        self.evolution_stage = 0
        self.current_form = "larva"

        # Combat
        self.last_attack_time = 0
        self.attack_cooldown = ATTACK_COOLDOWN

        # Collections
        self.traits = []
        self.skills = []

        # Movement
        self.velocity_x = 0
        self.velocity_y = 0

    def _create_texture(self):
        """Create a simple colored rectangle as texture"""
        self.texture = arcade.make_soft_square_texture(
            int(self.width), self.color, outer_alpha=255
        )

    def update_color(self, color):
        """Update player color (used when evolving)"""
        self.color = color
        self._create_texture()

    @property
    def atk(self):
        """Calculate total attack with trait modifiers"""
        total = self.base_atk
        for trait in self.traits:
            total = trait.modify_atk(total)
        return total

    @property
    def defense(self):
        """Calculate total defense with trait modifiers"""
        total = self.base_def
        for trait in self.traits:
            total = trait.modify_def(total)
        return total

    @property
    def crit_chance(self):
        """Calculate total crit chance with trait modifiers"""
        total = self.base_crit_chance
        for trait in self.traits:
            total = trait.modify_crit_chance(total)
        return min(total, 1.0)  # Cap at 100%

    def gain_xp(self, amount):
        """Add XP and handle leveling"""
        self.xp += amount
        level_ups = 0

        while self.xp >= self.xp_to_next_level:
            self.xp -= self.xp_to_next_level
            self.level += 1
            level_ups += 1
            self.xp_to_next_level = int(XP_PER_LEVEL * (XP_LEVEL_MULTIPLIER ** (self.level - 1)))

        return level_ups

    def add_trait(self, trait):
        """Add a trait to the player"""
        self.traits.append(trait)
        trait.apply(self)

    def add_skill(self, skill):
        """Add a skill to the player"""
        if skill not in self.skills:
            self.skills.append(skill)

    def can_attack(self):
        """Check if attack cooldown has passed"""
        return time.time() - self.last_attack_time >= self.attack_cooldown

    def perform_attack(self, target):
        """Attack an enemy"""
        if not self.can_attack():
            return 0

        self.last_attack_time = time.time()
        damage = calculate_damage(self, target)

        # Apply lifesteal from traits
        lifesteal_amount = 0
        for trait in self.traits:
            lifesteal_amount += trait.on_damage_dealt(damage)

        if lifesteal_amount > 0:
            self.heal(lifesteal_amount)

        return damage

    def take_damage(self, damage):
        """Take damage after defense calculation"""
        actual_damage = max(1, damage - self.defense)

        # Apply trait damage reduction
        for trait in self.traits:
            actual_damage = trait.modify_incoming_damage(actual_damage)

        self.hp -= actual_damage
        return actual_damage

    def heal(self, amount):
        """Heal the player"""
        old_hp = self.hp
        self.hp = min(self.hp + amount, self.max_hp)
        return self.hp - old_hp

    def is_alive(self):
        """Check if player is alive"""
        return self.hp > 0

    def update_movement(self, delta_time):
        """Update player position based on velocity"""
        self.center_x += self.velocity_x * self.speed
        self.center_y += self.velocity_y * self.speed

    def update_traits(self, delta_time):
        """Update trait effects (e.g., regen)"""
        for trait in self.traits:
            trait.update(self, delta_time)

    def update(self):
        """Called each frame"""
        pass
