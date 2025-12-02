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


class AttackEffect:
    """Visual effect for player attacks"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.lifetime = 0.0
        self.max_lifetime = ATTACK_EFFECT_DURATION
        self.size = ATTACK_EFFECT_SIZE
        self.color = COLOR_ATTACK_EFFECT

    def update(self, delta_time):
        """Update effect lifetime"""
        self.lifetime += delta_time

    def is_expired(self):
        """Check if effect should be removed"""
        return self.lifetime >= self.max_lifetime

    def draw(self):
        """Draw the attack effect"""
        # Fade out over time
        alpha = int(255 * (1 - self.lifetime / self.max_lifetime))
        color = (*self.color[:3], alpha)

        # Draw expanding circle
        current_size = self.size * (1 + self.lifetime / self.max_lifetime)
        arcade.draw_circle_filled(self.x, self.y, current_size, color)


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

        # Visual effects
        self.attack_effects = []

        # UI
        self.hud = HUD()
        self.current_menu = None

        # Cameras
        self.world_camera = None   # 월드(맵, 플레이어, 적)용
        self.ui_camera = None      # HUD/메뉴용

        # Pending level ups
        self.pending_level_ups = 0

        # Contact damage cooldown
        self.contact_damage_cooldown = CONTACT_DAMAGE_COOLDOWN
        self.contact_damage_timer = 0.0

        # Camera shake
        self.camera_shake_timer = 0.0
        self.camera_shake_duration = CAMERA_SHAKE_DURATION
        self.camera_shake_magnitude = CAMERA_SHAKE_MAGNITUDE
        self.base_camera_x = 0
        self.base_camera_y = 0

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
        self.player.game_window = self  # Set reference for screen shake

        # Give player initial skills based on form
        self._update_player_skills()

        # Reset state
        self.state = GameState.PLAYING
        self.current_menu = None
        self.pending_level_ups = 0
        self.contact_damage_timer = 0.0
        self.camera_shake_timer = 0.0

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
        # Fullscreen toggle (works in any state)
        if key == arcade.key.F11:
            self.set_fullscreen(not self.fullscreen)
            return

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

        # Create attack effect at player position
        effect = AttackEffect(self.player.center_x, self.player.center_y)
        self.attack_effects.append(effect)

        # Find enemies in range
        for enemy in self.current_floor.enemies:
            distance = (
                (enemy.center_x - self.player.center_x) ** 2 +
                (enemy.center_y - self.player.center_y) ** 2
            ) ** 0.5

            if distance <= ATTACK_RANGE:
                damage = self.player.perform_attack(enemy)
                # Apply damage to enemy
                enemy.take_damage(damage)

                if not enemy.is_alive():
                    # Enemy died
                    xp_gained = enemy.xp_value
                    level_ups = self.player.gain_xp(xp_gained)
                    self.pending_level_ups += level_ups

                    self.current_floor.enemies.remove(enemy)

                # Only attack one enemy per press
                break

    def trigger_camera_shake(self):
        """Trigger camera shake effect"""
        self.camera_shake_timer = self.camera_shake_duration

    def _check_player_enemy_collision(self):
        """Check if player is touching enemies (contact damage)"""
        hit_list = arcade.check_for_collision_with_list(
            self.player,
            self.current_floor.enemies
        )

        # Only deal contact damage if cooldown expired
        if hit_list and self.contact_damage_timer <= 0:
            enemy = hit_list[0]  # Take damage from first enemy in list
            self.player.take_damage(enemy.atk)
            self.contact_damage_timer = self.contact_damage_cooldown

    def on_update(self, delta_time):
        """Update game logic"""
        if self.state == GameState.PLAYING:
            # Decrement contact damage timer
            if self.contact_damage_timer > 0:
                self.contact_damage_timer -= delta_time
                if self.contact_damage_timer < 0:
                    self.contact_damage_timer = 0

            # Decrement camera shake timer
            if self.camera_shake_timer > 0:
                self.camera_shake_timer -= delta_time
                if self.camera_shake_timer < 0:
                    self.camera_shake_timer = 0

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

            # Update attack effects
            for effect in self.attack_effects:
                effect.update(delta_time)
            # Remove expired effects
            self.attack_effects = [e for e in self.attack_effects if not e.is_expired()]

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

    def on_resize(self, width, height):
        """Handle window resize events"""
        super().on_resize(width, height)

        # Recreate cameras with new window dimensions
        if self.world_camera:
            self.world_camera = arcade.camera.Camera2D()
        if self.ui_camera:
            self.ui_camera = arcade.camera.Camera2D()

        # Update HUD to use new screen dimensions
        if hasattr(self, 'hud') and self.hud:
            self.hud.hud_y_start = height - 30

        # Recenter camera on player
        if hasattr(self, 'player') and self.player:
            self._center_camera_on_player()

    def _center_camera_on_player(self):
        """Center the camera on the player (Camera2D semantics)"""
        import random

        # Camera2D.position is the world-space center of the camera, not bottom-left
        half_w = self.width / 2
        half_h = self.height / 2

        map_w = MAP_WIDTH * TILE_SIZE
        map_h = MAP_HEIGHT * TILE_SIZE

        # Clamp camera center so viewport never goes outside map bounds
        target_x = max(half_w, min(self.player.center_x, map_w - half_w))
        target_y = max(half_h, min(self.player.center_y, map_h - half_h))

        # Store base position
        self.base_camera_x = target_x
        self.base_camera_y = target_y

        # Apply camera shake if active
        if self.camera_shake_timer > 0:
            shake_x = random.uniform(-self.camera_shake_magnitude, self.camera_shake_magnitude)
            shake_y = random.uniform(-self.camera_shake_magnitude, self.camera_shake_magnitude)
            target_x += shake_x
            target_y += shake_y

        if self.world_camera:
            self.world_camera.position = (target_x, target_y)

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

    def _draw_enemy_hp_bars(self):
        """Draw HP bars above enemies"""
        bar_width = 30
        bar_height = 4
        bar_offset_y = 8  # Pixels above enemy

        for enemy in self.current_floor.enemies:
            # Calculate HP ratio
            hp_ratio = max(0, min(1, enemy.hp / enemy.max_hp))

            # Bar position
            bar_x = enemy.center_x
            bar_y = enemy.top + bar_offset_y

            # Background (empty HP)
            arcade.draw_rect_filled(
                arcade.XYWH(bar_x, bar_y, bar_width, bar_height),
                COLOR_HP_EMPTY
            )

            # Foreground (current HP)
            if hp_ratio > 0:
                fill_width = bar_width * hp_ratio
                fill_x = bar_x - (bar_width - fill_width) / 2
                arcade.draw_rect_filled(
                    arcade.XYWH(fill_x, bar_y, fill_width, bar_height),
                    COLOR_HP_FILL
                )

            # Border
            arcade.draw_rect_outline(
                arcade.XYWH(bar_x, bar_y, bar_width, bar_height),
                COLOR_UI_BORDER,
                1
            )

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

        # Draw attack effects
        for effect in self.attack_effects:
            effect.draw()

        # Draw enemy HP bars
        self._draw_enemy_hp_bars()

        # --- UI 카메라: HUD / 메뉴 ---
        if self.ui_camera:
            self.ui_camera.use()

        # Draw HUD
        if self.state in (GameState.PLAYING, GameState.STAT_UPGRADE):
            self.hud.draw(self.player, self.width, self.height)

        # Draw menus
        if self.current_menu:
            self.current_menu.draw()


def main():
    """Main entry point"""
    game = MonsterEvolutionGame()
    arcade.run()


if __name__ == "__main__":
    main()
