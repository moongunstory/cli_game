"""
Main game loop and window
"""

import arcade
from .config import *
from .entities import MonsterPlayer
from .systems import (
    DungeonFloor,
    get_evolution_options,
    evolve_player,
    EVOLUTION_TREE,
    get_random_traits,
    SKILL_REGISTRY,
)
from .systems.skills import get_skill_by_id
from .ui import HUD, TraitSelectionMenu, EvolutionSelectionMenu, GameOverMenu, StatUpgradeMenu


class GameState:
    """Game state enum"""
    PLAYING = "playing"
    STAT_UPGRADE = "stat_upgrade"
    TRAIT_SELECTION = "trait_selection"
    EVOLUTION_SELECTION = "evolution_selection"
    GAME_OVER = "game_over"


class MonsterEvolutionGame(arcade.Window):
    """Main game window"""

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(COLOR_BACKGROUND)

        # Game state
        self.state = GameState.PLAYING

        # Core objects
        self.player = None
        self.current_floor = None
        self.floor_number = 1

        # UI
        self.hud = HUD()
        self.current_menu = None

        # Cameras
        self.world_camera = None   # 월드(맵, 플레이어, 적)용
        self.ui_camera = None      # HUD/메뉴용

        # Pending level ups
        self.pending_level_ups = 0

        # Setup
        self.setup()

    def setup(self):
        """Initialize/reset the game"""
        # Create cameras
        self.world_camera = arcade.camera.Camera2D()
        self.ui_camera = arcade.camera.Camera2D()

        # Reset floor
        self.floor_number = 1
        self.current_floor = DungeonFloor(self.floor_number)

        # Create player
        spawn_x, spawn_y = self.current_floor.get_player_spawn_position()
        self.player = MonsterPlayer(spawn_x, spawn_y)

        # Give player initial skills based on form
        self._update_player_skills()

        # Reset state
        self.state = GameState.PLAYING
        self.current_menu = None
        self.pending_level_ups = 0

    def _update_player_skills(self):
        """Update player skills based on current form"""
        form_data = EVOLUTION_TREE.get(self.player.current_form)
        if form_data:
            skill_ids = form_data.get("skills", [])
            self.player.skills = []
            for skill_id in skill_ids:
                skill = get_skill_by_id(skill_id)
                if skill:
                    self.player.add_skill(skill)

    def on_key_press(self, key, modifiers):
        """Handle key press events"""
        # Menu handling
        if self.state == GameState.STAT_UPGRADE:
            self.current_menu.handle_key_press(key)
            return
        elif self.state == GameState.TRAIT_SELECTION:
            self.current_menu.handle_key_press(key)
            return
        elif self.state == GameState.EVOLUTION_SELECTION:
            self.current_menu.handle_key_press(key)
            return
        elif self.state == GameState.GAME_OVER:
            self.current_menu.handle_key_press(key)
            return

        # Playing state controls
        if self.state == GameState.PLAYING:
            # Movement
            if key == arcade.key.W or key == arcade.key.UP:
                self.player.velocity_y = 1
            elif key == arcade.key.S or key == arcade.key.DOWN:
                self.player.velocity_y = -1
            elif key == arcade.key.A or key == arcade.key.LEFT:
                self.player.velocity_x = -1
            elif key == arcade.key.D or key == arcade.key.RIGHT:
                self.player.velocity_x = 1

            # Attack
            elif key == arcade.key.SPACE:
                self._player_attack()

            # Skills
            elif key == arcade.key.Q:
                if len(self.player.skills) > 0:
                    self.player.skills[0].activate(
                        self.player,
                        self.current_floor.enemies,
                        self.current_floor.walls
                    )
            elif key == arcade.key.E:
                if len(self.player.skills) > 1:
                    self.player.skills[1].activate(
                        self.player,
                        self.current_floor.enemies,
                        self.current_floor.walls
                    )

    def on_key_release(self, key, modifiers):
        """Handle key release events"""
        if self.state == GameState.PLAYING:
            if key in (arcade.key.W, arcade.key.UP):
                if self.player.velocity_y > 0:
                    self.player.velocity_y = 0
            elif key in (arcade.key.S, arcade.key.DOWN):
                if self.player.velocity_y < 0:
                    self.player.velocity_y = 0
            elif key in (arcade.key.A, arcade.key.LEFT):
                if self.player.velocity_x < 0:
                    self.player.velocity_x = 0
            elif key in (arcade.key.D, arcade.key.RIGHT):
                if self.player.velocity_x > 0:
                    self.player.velocity_x = 0

    def _player_attack(self):
        """Handle player basic attack"""
        if not self.player.can_attack():
            return

        # Find enemies in range
        for enemy in self.current_floor.enemies:
            distance = (
                (enemy.center_x - self.player.center_x) ** 2 +
                (enemy.center_y - self.player.center_y) ** 2
            ) ** 0.5

            if distance <= ATTACK_RANGE:
                damage = self.player.perform_attack(enemy)
                if not enemy.is_alive():
                    # Enemy died
                    xp_gained = enemy.xp_value
                    level_ups = self.player.gain_xp(xp_gained)
                    self.pending_level_ups += level_ups

                    self.current_floor.enemies.remove(enemy)

                # Only attack one enemy per press
                break

    def _check_player_enemy_collision(self):
        """Check if player is touching enemies (contact damage)"""
        hit_list = arcade.check_for_collision_with_list(
            self.player,
            self.current_floor.enemies
        )

        for enemy in hit_list:
            # Enemy deals damage to player
            self.player.take_damage(enemy.atk)

    def on_update(self, delta_time):
        """Update game logic"""
        if self.state == GameState.PLAYING:
            # Update player movement
            old_x = self.player.center_x
            old_y = self.player.center_y

            self.player.update_movement(delta_time)

            # Check wall collision
            if arcade.check_for_collision_with_list(self.player, self.current_floor.walls):
                self.player.center_x = old_x
                self.player.center_y = old_y

            # Update traits
            self.player.update_traits(delta_time)

            # Update floor (enemy AI)
            self.current_floor.update(self.player, delta_time)

            # Check player-enemy collision
            self._check_player_enemy_collision()

            # Check if player died
            if not self.player.is_alive():
                self._game_over()
                return

            # Check if floor cleared
            if self.current_floor.is_cleared():
                self._floor_cleared()

            # Check for pending level ups
            if self.pending_level_ups > 0 and self.state == GameState.PLAYING:
                self.pending_level_ups -= 1
                self._show_stat_upgrade()

            # Center camera on player
            self._center_camera_on_player()

    def _center_camera_on_player(self):
        """Center the camera on the player"""
        screen_center_x = self.player.center_x - (SCREEN_WIDTH / 2)
        screen_center_y = self.player.center_y - (SCREEN_HEIGHT / 2)

        # Clamp to map bounds
        screen_center_x = max(0, min(screen_center_x, MAP_WIDTH * TILE_SIZE - SCREEN_WIDTH))
        screen_center_y = max(0, min(screen_center_y, MAP_HEIGHT * TILE_SIZE - SCREEN_HEIGHT))

        if self.world_camera:
            self.world_camera.position = (screen_center_x, screen_center_y)

    def _show_stat_upgrade(self):
        """Show stat upgrade menu"""
        self.state = GameState.STAT_UPGRADE
        self.current_menu = StatUpgradeMenu(self._on_stat_upgrade_selected)

    def _on_stat_upgrade_selected(self, stat_id):
        """Handle stat upgrade selection"""
        if stat_id == "hp":
            self.player.max_hp += 20
            self.player.hp += 20
        elif stat_id == "atk":
            self.player.base_atk += 5
        elif stat_id == "def":
            self.player.base_def += 3

        self.state = GameState.PLAYING
        self.current_menu = None

        # Check if player can evolve
        self._check_evolution()

    def _check_evolution(self):
        """Check if player can evolve and show menu if so"""
        evolution_options = get_evolution_options(self.player)
        if evolution_options:
            self.state = GameState.EVOLUTION_SELECTION
            self.current_menu = EvolutionSelectionMenu(
                evolution_options,
                self._on_evolution_selected
            )

    def _on_evolution_selected(self, form_id):
        """Handle evolution selection"""
        evolve_player(self.player, form_id)
        self._update_player_skills()

        self.state = GameState.PLAYING
        self.current_menu = None

    def _floor_cleared(self):
        """Handle floor cleared"""
        # Show trait selection
        owned_trait_ids = [t.id for t in self.player.traits]
        available_traits = get_random_traits(3, owned_trait_ids)

        if available_traits:
            self.state = GameState.TRAIT_SELECTION
            self.current_menu = TraitSelectionMenu(
                available_traits,
                self._on_trait_selected
            )
        else:
            # No traits available, go to next floor
            self._next_floor()

    def _on_trait_selected(self, trait):
        """Handle trait selection"""
        self.player.add_trait(trait)

        # Go to next floor
        self._next_floor()

    def _next_floor(self):
        """Generate next floor"""
        self.floor_number += 1
        self.current_floor = DungeonFloor(self.floor_number)

        # Spawn player at start
        spawn_x, spawn_y = self.current_floor.get_player_spawn_position()
        self.player.center_x = spawn_x
        self.player.center_y = spawn_y

        self.state = GameState.PLAYING
        self.current_menu = None

    def _game_over(self):
        """Handle game over"""
        stats = {
            "form": self.player.current_form,
            "level": self.player.level,
            "floor": self.floor_number,
            "trait_count": len(self.player.traits)
        }

        self.state = GameState.GAME_OVER
        self.current_menu = GameOverMenu(stats, self._restart_game)

    def _restart_game(self):
        """Restart the game"""
        self.setup()

    def on_draw(self):
        """Draw the game"""
        self.clear()

        # --- 월드 카메라: 맵 / 적 / 플레이어 ---
        if self.world_camera:
            self.world_camera.use()

        # Draw world
        self.current_floor.walls.draw()
        self.current_floor.enemies.draw()
        self.player.draw()

        # --- UI 카메라: HUD / 메뉴 ---
        if self.ui_camera:
            self.ui_camera.use()

        # Draw HUD
        if self.state in (GameState.PLAYING, GameState.STAT_UPGRADE):
            self.hud.draw(self.player)

        # Draw menus
        if self.current_menu:
            self.current_menu.draw()


def main():
    """Main entry point"""
    game = MonsterEvolutionGame()
    arcade.run()


if __name__ == "__main__":
    main()
