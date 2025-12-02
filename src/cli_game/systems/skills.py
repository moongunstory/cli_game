"""
Active skill system
"""

import time
import math
import arcade


class Skill:
    """Base skill class"""

    def __init__(self, skill_id, name, description, cooldown):
        self.id = skill_id
        self.name = name
        self.description = description
        self.cooldown = cooldown
        self.last_used = 0

    def can_use(self):
        """Check if skill is off cooldown"""
        return time.time() - self.last_used >= self.cooldown

    def get_remaining_cooldown(self):
        """Get remaining cooldown time"""
        elapsed = time.time() - self.last_used
        remaining = max(0, self.cooldown - elapsed)
        return remaining

    def activate(self, player, enemies, walls):
        """Activate the skill"""
        if not self.can_use():
            return False

        self.last_used = time.time()
        self._execute(player, enemies, walls)
        return True

    def _execute(self, player, enemies, walls):
        """Override this in subclasses"""
        pass


class FireBreath(Skill):
    """Dragon fire breath cone attack"""

    def __init__(self):
        super().__init__(
            "fire_breath",
            "Fire Breath",
            "Breathe fire in front, dealing 2x ATK damage in a cone",
            3.0
        )
        self.range = 150
        self.cone_angle = math.pi / 3  # 60 degrees

    def _execute(self, player, enemies, walls):
        """Deal damage to enemies in front cone"""
        damage = player.atk * 2

        for enemy in enemies:
            dx = enemy.center_x - player.center_x
            dy = enemy.center_y - player.center_y
            distance = math.sqrt(dx * dx + dy * dy)

            if distance <= self.range and distance > 0:
                # Check if in cone (simplified - just check distance for MVP)
                enemy.take_damage(damage)


class WingBuffet(Skill):
    """Dragon wing attack that knocks back"""

    def __init__(self):
        super().__init__(
            "wing_buffet",
            "Wing Buffet",
            "Powerful wing attack around you, 1.5x ATK damage",
            4.0
        )
        self.range = 100

    def _execute(self, player, enemies, walls):
        """Deal damage to nearby enemies"""
        damage = int(player.atk * 1.5)

        for enemy in enemies:
            distance = math.sqrt(
                (enemy.center_x - player.center_x) ** 2 +
                (enemy.center_y - player.center_y) ** 2
            )
            if distance <= self.range:
                enemy.take_damage(damage)


class TidalCrash(Skill):
    """Leviathan wave attack"""

    def __init__(self):
        super().__init__(
            "tidal_crash",
            "Tidal Crash",
            "Launch a wave of water, 2.5x ATK damage",
            4.5
        )
        self.range = 200

    def _execute(self, player, enemies, walls):
        """Linear wave attack"""
        damage = int(player.atk * 2.5)

        for enemy in enemies:
            dx = enemy.center_x - player.center_x
            dy = enemy.center_y - player.center_y
            distance = math.sqrt(dx * dx + dy * dy)

            if distance <= self.range:
                enemy.take_damage(damage)


class LeviathanRoar(Skill):
    """AoE stun/damage"""

    def __init__(self):
        super().__init__(
            "leviathan_roar",
            "Leviathan Roar",
            "Powerful roar, 1.8x ATK damage to all nearby enemies",
            5.0
        )
        self.range = 150

    def _execute(self, player, enemies, walls):
        """AoE damage"""
        damage = int(player.atk * 1.8)

        for enemy in enemies:
            distance = math.sqrt(
                (enemy.center_x - player.center_x) ** 2 +
                (enemy.center_y - player.center_y) ** 2
            )
            if distance <= self.range:
                enemy.take_damage(damage)


class StonePunch(Skill):
    """Heavy melee attack"""

    def __init__(self):
        super().__init__(
            "stone_punch",
            "Stone Punch",
            "Devastating punch, 3x ATK damage to target in front",
            3.5
        )
        self.range = 80

    def _execute(self, player, enemies, walls):
        """Heavy single target damage"""
        damage = int(player.atk * 3)

        # Find closest enemy in front
        closest = None
        closest_dist = self.range

        for enemy in enemies:
            dx = enemy.center_x - player.center_x
            dy = enemy.center_y - player.center_y
            distance = math.sqrt(dx * dx + dy * dy)

            if distance < closest_dist:
                closest = enemy
                closest_dist = distance

        if closest:
            closest.take_damage(damage)


class Earthquake(Skill):
    """AoE ground slam"""

    def __init__(self):
        super().__init__(
            "earthquake",
            "Earthquake",
            "Slam the ground, 2x ATK damage in large area",
            6.0
        )
        self.range = 180

    def _execute(self, player, enemies, walls):
        """Large AoE damage"""
        damage = int(player.atk * 2)

        for enemy in enemies:
            distance = math.sqrt(
                (enemy.center_x - player.center_x) ** 2 +
                (enemy.center_y - player.center_y) ** 2
            )
            if distance <= self.range:
                enemy.take_damage(damage)


# Skill registry
SKILL_REGISTRY = {
    "fire_breath": FireBreath,
    "wing_buffet": WingBuffet,
    "tidal_crash": TidalCrash,
    "leviathan_roar": LeviathanRoar,
    "stone_punch": StonePunch,
    "earthquake": Earthquake,
}


def get_skill_by_id(skill_id):
    """Get a skill instance by ID"""
    skill_class = SKILL_REGISTRY.get(skill_id)
    if skill_class:
        return skill_class()
    return None
