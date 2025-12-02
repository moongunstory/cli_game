"""
Heads-up display (HUD)
"""

import arcade
from ..config import *


class HUD:
    """Game HUD showing player stats and info"""

    def __init__(self):
        self.padding = 20
        self.bar_height = 20
        self.bar_width = 200
        self.hud_x = 20  # Left side positioning
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT

    def draw(self, player, screen_width=None, screen_height=None):
        """Draw the HUD"""
        # Use provided dimensions or defaults
        if screen_width is None:
            screen_width = self.screen_width
        if screen_height is None:
            screen_height = self.screen_height

        # Update stored dimensions
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Background panel (top-left)
        panel_width = 240
        panel_height = 180
        panel_x = self.padding
        panel_y = screen_height - panel_height - self.padding

        arcade.draw_rect_filled(
            arcade.XYWH(
                panel_x + panel_width / 2,
                panel_y + panel_height / 2,
                panel_width,
                panel_height,
            ),
            COLOR_UI_BG,
        )

        arcade.draw_rect_outline(
            arcade.XYWH(
                panel_x + panel_width / 2,
                panel_y + panel_height / 2,
                panel_width,
                panel_height,
            ),
            COLOR_UI_BORDER,
            2,
        )

        # Content positioning
        content_x = panel_x + 10
        y = screen_height - 40

        # Player form
        arcade.draw_text(
            f"Form: {player.current_form.replace('_', ' ').title()}",
            content_x,
            y,
            COLOR_TEXT,
            12,
            bold=True
        )
        y -= 25

        # Level
        arcade.draw_text(
            f"Level: {player.level}",
            content_x,
            y,
            COLOR_TEXT,
            12
        )
        y -= 25

        # HP Bar
        self._draw_bar(
            content_x,
            y,
            self.bar_width,
            self.bar_height,
            player.hp,
            player.max_hp,
            COLOR_HP_BAR,
            f"HP: {int(player.hp)}/{int(player.max_hp)}"
        )
        y -= 30

        # XP Bar
        self._draw_bar(
            content_x,
            y,
            self.bar_width,
            self.bar_height,
            player.xp,
            player.xp_to_next_level,
            COLOR_XP_BAR,
            f"XP: {int(player.xp)}/{int(player.xp_to_next_level)}"
        )
        y -= 30

        # Stats
        arcade.draw_text(
            f"ATK: {int(player.atk)}  DEF: {int(player.defense)}",
            content_x,
            y,
            COLOR_TEXT,
            11
        )
        y -= 20

        arcade.draw_text(
            f"CRIT: {int(player.crit_chance * 100)}%",
            content_x,
            y,
            COLOR_TEXT,
            11
        )

        # Traits (below the main HUD panel)
        if player.traits:
            y = panel_y - 30
            arcade.draw_text(
                "Traits:",
                content_x,
                y,
                COLOR_TEXT,
                11,
                bold=True
            )
            y -= 20
            for trait in player.traits[:3]:  # Show first 3
                arcade.draw_text(
                    f"• {trait.name}",
                    content_x,
                    y,
                    COLOR_TEXT_DARK,
                    10
                )
                y -= 18

        # Skills
        if player.skills:
            self._draw_skills(player)

        # Controls hint
        arcade.draw_text(
            "WASD: Move | SPACE: Attack | Q/E: Skills",
            10,
            10,
            COLOR_TEXT_DARK,
            10
        )

    def _draw_bar(self, x, y, width, height, current, maximum, color, label):
        """Draw a stat bar with label"""
        # Background
        arcade.draw_rect_filled(
            arcade.XYWH(
                x + width / 2,
                y + height / 2,
                width,
                height,
            ),
            (50, 50, 50),
        )

        # Fill
        if maximum > 0:
            fill_width = (current / maximum) * width
            arcade.draw_rect_filled(
                arcade.XYWH(
                    x + fill_width / 2,
                    y + height / 2,
                    fill_width,
                    height,
                ),
                color,
            )

        # Border
        arcade.draw_rect_outline(
            arcade.XYWH(
                x + width / 2,
                y + height / 2,
                width,
                height,
            ),
            COLOR_UI_BORDER,
        )

        # Label
        arcade.draw_text(label, x + 5, y + 4, COLOR_TEXT, 10, bold=True)

    def _draw_skills(self, player):
        """Draw skill cooldown indicators"""
        x_start = 10
        y_pos = 50
        skill_width = 80
        skill_height = 60

        keys = ['Q', 'E']
        for i, skill in enumerate(player.skills[:2]):  # Show first 2 skills
            key = keys[i] if i < len(keys) else '?'
            x = x_start + i * (skill_width + 10)

            # Background
            arcade.draw_rect_filled(
                arcade.XYWH(
                    x + skill_width / 2,
                    y_pos + skill_height / 2,
                    skill_width,
                    skill_height,
                ),
                COLOR_UI_BG,
            )
            arcade.draw_rect_outline(
                arcade.XYWH(
                    x + skill_width / 2,
                    y_pos + skill_height / 2,
                    skill_width,
                    skill_height,
                ),
                COLOR_UI_BORDER,
            )

            # Key binding
            arcade.draw_text(
                key,
                x + 5,
                y_pos + skill_height - 18,
                COLOR_TEXT,
                12,
                bold=True
            )

            # Skill name
            arcade.draw_text(
                skill.name[:8],
                x + 5,
                y_pos + 20,
                COLOR_TEXT,
                9
            )

            # Cooldown
            remaining = skill.get_remaining_cooldown()
            if remaining > 0:
                arcade.draw_text(
                    f"{remaining:.1f}s",
                    x + 5,
                    y_pos + 5,
                    (255, 100, 100),
                    10,
                    bold=True
                )
            else:
                arcade.draw_text(
                    "READY",
                    x + 5,
                    y_pos + 5,
                    (100, 255, 100),
                    9,
                    bold=True
                )
