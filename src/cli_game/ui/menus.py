"""
Game menus for selections and game over
"""

import arcade
from ..config import *
from ..systems.evolution import EVOLUTION_TREE


class StatUpgradeMenu:
    """Menu for choosing stat upgrades on level up"""

    def __init__(self, on_select_callback):
        self.on_select = on_select_callback
        self.options = [
            {"id": "hp", "name": "Max HP +20", "description": "Increase maximum health"},
            {"id": "atk", "name": "Attack +5", "description": "Increase attack damage"},
            {"id": "def", "name": "Defense +3", "description": "Increase damage reduction"},
        ]
        self.selected_index = 0

    def handle_key_press(self, key):
        """Handle keyboard input"""
        if key == arcade.key.UP or key == arcade.key.W:
            self.selected_index = (self.selected_index - 1) % len(self.options)
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.selected_index = (self.selected_index + 1) % len(self.options)
        elif key == arcade.key.ENTER or key == arcade.key.SPACE:
            self.on_select(self.options[self.selected_index]["id"])

    def draw(self):
        """Draw the stat upgrade menu"""
        # Background
        arcade.draw_rectangle_filled(
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            500,
            400,
            COLOR_UI_BG
        )
        arcade.draw_rectangle_outline(
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            500,
            400,
            COLOR_UI_BORDER,
            3
        )

        # Title
        arcade.draw_text(
            "LEVEL UP! Choose an Upgrade:",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 150,
            COLOR_TEXT,
            20,
            anchor_x="center",
            bold=True
        )

        # Options
        y = SCREEN_HEIGHT / 2 + 80
        for i, option in enumerate(self.options):
            is_selected = i == self.selected_index

            # Highlight selected
            if is_selected:
                arcade.draw_rectangle_filled(
                    SCREEN_WIDTH / 2,
                    y,
                    450,
                    60,
                    (80, 80, 100)
                )

            # Option name
            arcade.draw_text(
                option["name"],
                SCREEN_WIDTH / 2,
                y + 10,
                COLOR_TEXT if is_selected else COLOR_TEXT_DARK,
                16,
                anchor_x="center",
                bold=is_selected
            )

            # Description
            arcade.draw_text(
                option["description"],
                SCREEN_WIDTH / 2,
                y - 10,
                COLOR_TEXT_DARK,
                12,
                anchor_x="center"
            )

            y -= 90

        # Instructions
        arcade.draw_text(
            "W/S to select | ENTER to confirm",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 150,
            COLOR_TEXT_DARK,
            12,
            anchor_x="center"
        )


class TraitSelectionMenu:
    """Menu for selecting traits after clearing a floor"""

    def __init__(self, traits, on_select_callback):
        self.traits = traits
        self.on_select = on_select_callback
        self.selected_index = 0

    def handle_key_press(self, key):
        """Handle keyboard input"""
        if key == arcade.key.UP or key == arcade.key.W:
            self.selected_index = (self.selected_index - 1) % len(self.traits)
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.selected_index = (self.selected_index + 1) % len(self.traits)
        elif key == arcade.key.ENTER or key == arcade.key.SPACE:
            self.on_select(self.traits[self.selected_index])

    def draw(self):
        """Draw the trait selection menu"""
        # Background
        arcade.draw_rectangle_filled(
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            600,
            500,
            COLOR_UI_BG
        )
        arcade.draw_rectangle_outline(
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            600,
            500,
            COLOR_UI_BORDER,
            3
        )

        # Title
        arcade.draw_text(
            "FLOOR CLEARED! Choose a Trait:",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 200,
            COLOR_TEXT,
            20,
            anchor_x="center",
            bold=True
        )

        # Traits
        y = SCREEN_HEIGHT / 2 + 120
        for i, trait in enumerate(self.traits):
            is_selected = i == self.selected_index

            # Highlight selected
            if is_selected:
                arcade.draw_rectangle_filled(
                    SCREEN_WIDTH / 2,
                    y,
                    550,
                    80,
                    (80, 80, 100)
                )

            # Trait name
            arcade.draw_text(
                trait.name,
                SCREEN_WIDTH / 2,
                y + 20,
                COLOR_TEXT if is_selected else COLOR_TEXT_DARK,
                18,
                anchor_x="center",
                bold=is_selected
            )

            # Description
            arcade.draw_text(
                trait.description,
                SCREEN_WIDTH / 2,
                y - 10,
                COLOR_TEXT_DARK,
                13,
                anchor_x="center"
            )

            y -= 110

        # Instructions
        arcade.draw_text(
            "W/S to select | ENTER to confirm",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 210,
            COLOR_TEXT_DARK,
            12,
            anchor_x="center"
        )


class EvolutionSelectionMenu:
    """Menu for choosing evolution path"""

    def __init__(self, evolution_options, on_select_callback):
        self.evolution_options = evolution_options
        self.on_select = on_select_callback
        self.selected_index = 0

    def handle_key_press(self, key):
        """Handle keyboard input"""
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.selected_index = (self.selected_index - 1) % len(self.evolution_options)
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.selected_index = (self.selected_index + 1) % len(self.evolution_options)
        elif key == arcade.key.ENTER or key == arcade.key.SPACE:
            self.on_select(self.evolution_options[self.selected_index])

    def draw(self):
        """Draw the evolution selection menu"""
        # Background
        arcade.draw_rectangle_filled(
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            700,
            500,
            COLOR_UI_BG
        )
        arcade.draw_rectangle_outline(
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            700,
            500,
            COLOR_UI_BORDER,
            3
        )

        # Title
        arcade.draw_text(
            "EVOLUTION TIME! Choose Your Path:",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 200,
            COLOR_TEXT,
            22,
            anchor_x="center",
            bold=True
        )

        # Evolution options in a row
        num_options = len(self.evolution_options)
        spacing = 200
        start_x = SCREEN_WIDTH / 2 - (num_options - 1) * spacing / 2

        for i, form_id in enumerate(self.evolution_options):
            x = start_x + i * spacing
            y = SCREEN_HEIGHT / 2 + 50

            form_data = EVOLUTION_TREE.get(form_id)
            is_selected = i == self.selected_index

            # Highlight selected
            if is_selected:
                arcade.draw_rectangle_filled(
                    x,
                    y,
                    180,
                    300,
                    (80, 80, 100)
                )

            # Form preview (colored box)
            arcade.draw_rectangle_filled(
                x,
                y + 80,
                100,
                100,
                form_data["color"]
            )
            arcade.draw_rectangle_outline(
                x,
                y + 80,
                100,
                100,
                COLOR_TEXT,
                2
            )

            # Form name
            arcade.draw_text(
                form_data["name"],
                x,
                y - 10,
                COLOR_TEXT if is_selected else COLOR_TEXT_DARK,
                16,
                anchor_x="center",
                bold=is_selected
            )

            # Stats preview
            stats_text = f"HP: x{form_data['hp_mult']:.1f}\n"
            stats_text += f"ATK: x{form_data['atk_mult']:.1f}\n"
            stats_text += f"DEF: x{form_data['def_mult']:.1f}"

            lines = stats_text.split('\n')
            stat_y = y - 40
            for line in lines:
                arcade.draw_text(
                    line,
                    x,
                    stat_y,
                    COLOR_TEXT_DARK,
                    11,
                    anchor_x="center"
                )
                stat_y -= 18

            # Description
            arcade.draw_text(
                form_data["description"][:30],
                x,
                y - 110,
                COLOR_TEXT_DARK,
                10,
                anchor_x="center",
                width=160,
                align="center"
            )

        # Instructions
        arcade.draw_text(
            "A/D to select | ENTER to confirm",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 210,
            COLOR_TEXT_DARK,
            12,
            anchor_x="center"
        )


class GameOverMenu:
    """Game over screen"""

    def __init__(self, player_stats, on_restart_callback):
        self.player_stats = player_stats
        self.on_restart = on_restart_callback

    def handle_key_press(self, key):
        """Handle keyboard input"""
        if key == arcade.key.SPACE or key == arcade.key.ENTER or key == arcade.key.R:
            self.on_restart()

    def draw(self):
        """Draw the game over screen"""
        # Dark overlay
        arcade.draw_rectangle_filled(
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            (0, 0, 0, 200)
        )

        # Main box
        arcade.draw_rectangle_filled(
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            500,
            400,
            COLOR_UI_BG
        )
        arcade.draw_rectangle_outline(
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            500,
            400,
            COLOR_UI_BORDER,
            3
        )

        # Title
        arcade.draw_text(
            "GAME OVER",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 150,
            (255, 100, 100),
            28,
            anchor_x="center",
            bold=True
        )

        # Stats
        y = SCREEN_HEIGHT / 2 + 80
        stats_display = [
            f"Final Form: {self.player_stats['form'].replace('_', ' ').title()}",
            f"Level Reached: {self.player_stats['level']}",
            f"Floor Reached: {self.player_stats['floor']}",
            f"Traits Collected: {self.player_stats['trait_count']}",
        ]

        for stat in stats_display:
            arcade.draw_text(
                stat,
                SCREEN_WIDTH / 2,
                y,
                COLOR_TEXT,
                16,
                anchor_x="center"
            )
            y -= 40

        # Instructions
        arcade.draw_text(
            "Press SPACE or R to Restart",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 140,
            COLOR_TEXT,
            16,
            anchor_x="center",
            bold=True
        )
