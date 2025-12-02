"""
Enemy entities with AI
"""

import arcade
import random
import math
from ..config import *


class Enemy(arcade.Sprite):
    """Base enemy class"""

    def __init__(self, x, y, hp, atk, defense, xp_value, color, speed=ENEMY_SPEED_BASE):
        super().__init__()

        # Visual
        self.center_x = x
        self.center_y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.color = color
        self._create_texture()

        # Stats
        self.max_hp = hp
        self.hp = hp
        self.atk = atk
        self.defense = defense
        self.speed = speed
        self.xp_value = xp_value

        # AI
        self.target = None
        self.detection_range = ENEMY_DETECTION_RANGE
        self.wander_timer = 0
        self.wander_direction = random.uniform(0, 2 * math.pi)
        self.aggro = False

    def _create_texture(self):
        """Create a simple colored rectangle as texture"""
        self.texture = arcade.make_soft_square_texture(
            int(self.width), self.color, outer_alpha=255
        )

    def take_damage(self, damage):
        """Take damage after defense calculation"""
        actual_damage = max(1, damage - self.defense)
        self.hp -= actual_damage
        return actual_damage

    def is_alive(self):
        """Check if enemy is alive"""
        return self.hp > 0

    def distance_to(self, target):
        """Calculate distance to target"""
        dx = self.center_x - target.center_x
        dy = self.center_y - target.center_y
        return math.sqrt(dx * dx + dy * dy)

    def update_ai(self, player, walls, delta_time):
        """Update enemy AI behavior"""
        distance = self.distance_to(player)

        # Check if player is in detection range
        if distance < self.detection_range:
            self.aggro = True

        if self.aggro:
            # Chase player
            dx = player.center_x - self.center_x
            dy = player.center_y - self.center_y
            distance = math.sqrt(dx * dx + dy * dy)

            if distance > 0:
                # Normalize and move
                dx /= distance
                dy /= distance
                self.center_x += dx * self.speed
                self.center_y += dy * self.speed
        else:
            # Wander randomly
            self.wander_timer -= delta_time
            if self.wander_timer <= 0:
                self.wander_direction = random.uniform(0, 2 * math.pi)
                self.wander_timer = random.uniform(1, 3)

            dx = math.cos(self.wander_direction)
            dy = math.sin(self.wander_direction)
            self.center_x += dx * self.speed * 0.5
            self.center_y += dy * self.speed * 0.5

        # Check wall collision
        if arcade.check_for_collision_with_list(self, walls):
            # Revert movement
            if self.aggro:
                dx = player.center_x - self.center_x
                dy = player.center_y - self.center_y
                distance = math.sqrt(dx * dx + dy * dy)
                if distance > 0:
                    dx /= distance
                    dy /= distance
                    self.center_x -= dx * self.speed
                    self.center_y -= dy * self.speed
            else:
                dx = math.cos(self.wander_direction)
                dy = math.sin(self.wander_direction)
                self.center_x -= dx * self.speed * 0.5
                self.center_y -= dy * self.speed * 0.5
                self.wander_direction = random.uniform(0, 2 * math.pi)


class Slime(Enemy):
    """Weak starting enemy"""

    def __init__(self, x, y, floor_level=1):
        scaling = FLOOR_SCALING_FACTOR ** (floor_level - 1)
        hp = int(30 * scaling)
        atk = int(5 * scaling)
        defense = int(1 * scaling)
        xp = int(20 * scaling)

        super().__init__(x, y, hp, atk, defense, xp, (100, 255, 100), speed=1.0)


class Goblin(Enemy):
    """Medium strength enemy"""

    def __init__(self, x, y, floor_level=1):
        scaling = FLOOR_SCALING_FACTOR ** (floor_level - 1)
        hp = int(50 * scaling)
        atk = int(8 * scaling)
        defense = int(3 * scaling)
        xp = int(35 * scaling)

        super().__init__(x, y, hp, atk, defense, xp, (255, 200, 100), speed=1.5)


class OrcWarrior(Enemy):
    """Strong enemy"""

    def __init__(self, x, y, floor_level=1):
        scaling = FLOOR_SCALING_FACTOR ** (floor_level - 1)
        hp = int(80 * scaling)
        atk = int(12 * scaling)
        defense = int(5 * scaling)
        xp = int(50 * scaling)

        super().__init__(x, y, hp, atk, defense, xp, (255, 100, 100), speed=1.8)
