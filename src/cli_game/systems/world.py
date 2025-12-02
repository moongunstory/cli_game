"""
Dungeon/world generation system
"""

import arcade
import random
from ..config import *
from ..entities.enemies import Slime, Goblin, OrcWarrior


class DungeonFloor:
    """Represents a single dungeon floor"""

    def __init__(self, floor_number):
        self.floor_number = floor_number
        self.walls = arcade.SpriteList(use_spatial_hash=True)
        self.floor_tiles = arcade.SpriteList(use_spatial_hash=True)
        self.enemies = arcade.SpriteList()

        self.width = MAP_WIDTH
        self.height = MAP_HEIGHT

        # Generate the floor
        self.generate()

    def generate(self):
        """Generate floor layout and spawn enemies"""
        self._create_walls()
        self._spawn_enemies()

    def _create_walls(self):
        """Create wall boundaries and some obstacles"""
        # Create border walls
        for x in range(self.width):
            for y in range(self.height):
                # Border walls
                if x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1:
                    wall = arcade.SpriteSolidColor(TILE_SIZE, TILE_SIZE, COLOR_WALL)
                    wall.center_x = x * TILE_SIZE + TILE_SIZE / 2
                    wall.center_y = y * TILE_SIZE + TILE_SIZE / 2
                    self.walls.append(wall)

        # Add some random interior obstacles
        num_obstacles = 10 + self.floor_number * 2
        for _ in range(num_obstacles):
            x = random.randint(2, self.width - 3)
            y = random.randint(2, self.height - 3)

            # Create small wall clusters
            for dx in range(random.randint(1, 3)):
                for dy in range(random.randint(1, 2)):
                    if x + dx < self.width - 1 and y + dy < self.height - 1:
                        wall = arcade.SpriteSolidColor(TILE_SIZE, TILE_SIZE, COLOR_WALL)
                        wall.center_x = (x + dx) * TILE_SIZE + TILE_SIZE / 2
                        wall.center_y = (y + dy) * TILE_SIZE + TILE_SIZE / 2
                        self.walls.append(wall)

    def _spawn_enemies(self):
        """Spawn enemies for this floor"""
        base_count = ENEMY_SPAWN_COUNT + self.floor_number
        enemy_count = random.randint(base_count, base_count + 3)

        # Determine enemy types based on floor
        enemy_types = []
        if self.floor_number <= 2:
            enemy_types = [Slime, Slime, Goblin]
        elif self.floor_number <= 5:
            enemy_types = [Slime, Goblin, Goblin, OrcWarrior]
        else:
            enemy_types = [Goblin, Goblin, OrcWarrior, OrcWarrior]

        for _ in range(enemy_count):
            # Find valid spawn position
            valid_position = False
            attempts = 0
            while not valid_position and attempts < 50:
                x = random.randint(3, self.width - 4) * TILE_SIZE
                y = random.randint(3, self.height - 4) * TILE_SIZE

                # Check if position is clear
                test_sprite = arcade.Sprite()
                test_sprite.center_x = x
                test_sprite.center_y = y
                test_sprite.width = TILE_SIZE
                test_sprite.height = TILE_SIZE

                if not arcade.check_for_collision_with_list(test_sprite, self.walls):
                    valid_position = True

                attempts += 1

            if valid_position:
                enemy_class = random.choice(enemy_types)
                enemy = enemy_class(x, y, self.floor_number)
                self.enemies.append(enemy)

    def get_player_spawn_position(self):
        """Get a safe spawn position for the player"""
        # Try to find a clear spot
        for _ in range(100):
            x = random.randint(2, 5) * TILE_SIZE
            y = random.randint(2, self.height - 3) * TILE_SIZE

            test_sprite = arcade.Sprite()
            test_sprite.center_x = x
            test_sprite.center_y = y
            test_sprite.width = TILE_SIZE
            test_sprite.height = TILE_SIZE

            if not arcade.check_for_collision_with_list(test_sprite, self.walls):
                return x, y

        # Fallback
        return TILE_SIZE * 2, TILE_SIZE * 2

    def update(self, player, delta_time):
        """Update floor elements"""
        # Update enemy AI
        for enemy in self.enemies:
            enemy.update_ai(player, self.walls, delta_time)

    def is_cleared(self):
        """Check if floor is cleared (all enemies dead)"""
        return len(self.enemies) == 0
