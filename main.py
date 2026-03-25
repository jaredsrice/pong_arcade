import random
import arcade
import math

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 576
WINDOW_TITLE = "Ping"

BASE_WIDTH = 1280
BASE_HEIGHT = 720
SCALE_X = WINDOW_WIDTH / BASE_WIDTH
SCALE_Y = WINDOW_HEIGHT / BASE_HEIGHT
SCALE = min(SCALE_X, SCALE_Y)


class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        self.background_color = arcade.color.BLACK
        arcade.load_font("Fonts/pong-score.otf")
        arcade.load_font("Fonts/bit5x3.ttf")

        self.game_state = "menu"

        # Paddle properties
        self.paddle_width = round(20 * SCALE_X)
        self.paddle_height = round(150 * SCALE_Y)
        self.paddle_speed = 420
        self.max_bounce_angle = math.radians(75)

        # Paddle positions
        self.paddle_margin_x = round(32 * SCALE_X)
        self.paddle1_x = self.paddle_margin_x
        self.paddle1_y = WINDOW_HEIGHT / 2
        self.paddle2_x = WINDOW_WIDTH - self.paddle_margin_x
        self.paddle2_y = WINDOW_HEIGHT / 2

        # Paddle input state
        self.paddle1_up_pressed = False
        self.paddle1_down_pressed = False
        self.paddle2_up_pressed = False
        self.paddle2_down_pressed = False

        # Ball state
        self.ball_size = round(20 * SCALE)
        self.ball_half_size = self.ball_size / 2
        self.ball_x = WINDOW_WIDTH / 2
        self.ball_y = WINDOW_HEIGHT / 2

        # Ball movement
        self.serve_speed = 210
        self.base_speed = 630
        self.ball_speed = self.serve_speed
        self.ball_change_x = -self.ball_speed
        self.ball_change_y = 0

        # Score state
        self.player1_score = 0
        self.player2_score = 0
        self.last_scoring_player = 1

        # Text sizes
        self.score_font_size = round(50 * SCALE)
        self.title_font_size = round(60 * SCALE)
        self.winner_font_size = round(45 * SCALE)
        self.prompt_font_size = round(20 * SCALE)
        self.menu_font_size = round(25 * SCALE)

        # Score text
        self.player1_score_text = arcade.Text(
            f"{self.player1_score}",
            WINDOW_WIDTH / 2 - (65 * SCALE_X),
            WINDOW_HEIGHT - (90 * SCALE_Y),
            color=arcade.color.WHITE_SMOKE,
            font_size=self.score_font_size,
            font_name="Pong Score",
            anchor_x="right",
        )

        self.player2_score_text = arcade.Text(
            f"{self.player2_score}",
            WINDOW_WIDTH / 2 + (85 * SCALE_X),
            WINDOW_HEIGHT - (90 * SCALE_Y),
            color=arcade.color.WHITE_SMOKE,
            font_size=self.score_font_size,
            font_name="Pong Score",
            anchor_x="left",
        )

        # Menu / state text
        self.title_text = arcade.Text(
            "PING",
            WINDOW_WIDTH / 2,
            WINDOW_HEIGHT / 2 + (100 * SCALE_Y),
            color=arcade.color.WHITE_SMOKE,
            font_size=self.title_font_size,
            font_name="Bit5x3",
            anchor_x="center",
        )

        self.play_text = arcade.Text(
            "Press SPACE to Play",
            WINDOW_WIDTH / 2,
            WINDOW_HEIGHT / 2,
            color=arcade.color.WHITE_SMOKE,
            font_size=self.menu_font_size,
            font_name="Bit5x3",
            anchor_x="center",
        )

        self.winner_text = arcade.Text(
            "",
            WINDOW_WIDTH / 2,
            WINDOW_HEIGHT / 2,
            color=arcade.color.WHITE_SMOKE,
            font_size=self.winner_font_size,
            font_name="Bit5x3",
            anchor_x="center",
        )

        self.space_to_continue_text = arcade.Text(
            "Press SPACE to Continue",
            WINDOW_WIDTH / 2,
            WINDOW_HEIGHT / 2 - (50 * SCALE_Y),
            color=arcade.color.WHITE_SMOKE,
            font_size=self.prompt_font_size,
            font_name="Bit5x3",
            anchor_x="center",
        )

        self.space_to_serve_text = arcade.Text(
            "Press SPACE to Serve",
            WINDOW_WIDTH / 2,
            WINDOW_HEIGHT / 2 + (50 * SCALE_Y),
            color=arcade.color.WHITE_SMOKE,
            font_size=self.prompt_font_size,
            font_name="Bit5x3",
            anchor_x="center",
        )

    # -----------------------------
    # Reset / state helpers
    # -----------------------------
    def reset_on_point(self):
        self.ball_x = WINDOW_WIDTH / 2
        self.ball_y = WINDOW_HEIGHT / 2
        self.ball_speed = self.serve_speed

        if self.last_scoring_player == 1:
            self.ball_change_x = -self.serve_speed
        else:
            self.ball_change_x = self.serve_speed

        self.ball_change_y = random.choice([-150, 150])
        self.game_state = "serve"

    def _reset_game(self):
        self.winner_text.text = ""

        self.player1_score = 0
        self.player2_score = 0
        self.player1_score_text.text = f"{self.player1_score}"
        self.player2_score_text.text = f"{self.player2_score}"

        self.last_scoring_player = 1

        self.paddle1_y = WINDOW_HEIGHT / 2
        self.paddle2_y = WINDOW_HEIGHT / 2

        self.paddle1_up_pressed = False
        self.paddle1_down_pressed = False
        self.paddle2_up_pressed = False
        self.paddle2_down_pressed = False

        self.ball_x = WINDOW_WIDTH / 2
        self.ball_y = WINDOW_HEIGHT / 2
        self.ball_speed = self.serve_speed
        self.ball_change_x = -self.serve_speed
        self.ball_change_y = 0

    def point_scored(self, scoring_player):
        if scoring_player == 1:
            self.player1_score += 1
            self.player1_score_text.text = f"{self.player1_score}"
            self.last_scoring_player = 1
        else:
            self.player2_score += 1
            self.player2_score_text.text = f"{self.player2_score}"
            self.last_scoring_player = 2

        if self.player1_score >= 2:
            self.game_state = "game_over"
            self.winner_text.text = "Player 1 Wins!"
        elif self.player2_score >= 2:
            self.game_state = "game_over"
            self.winner_text.text = "Player 2 Wins!"

    # -----------------------------
    # Draw helpers
    # -----------------------------
    def _draw_game_objects(self):
        arcade.draw_rect_filled(
            arcade.rect.XYWH(
                self.paddle1_x,
                self.paddle1_y,
                self.paddle_width,
                self.paddle_height,
            ),
            arcade.color.WHITE_SMOKE,
        )

        arcade.draw_rect_filled(
            arcade.rect.XYWH(
                self.paddle2_x,
                self.paddle2_y,
                self.paddle_width,
                self.paddle_height,
            ),
            arcade.color.WHITE_SMOKE,
        )

        arcade.draw_rect_filled(
            arcade.rect.XYWH(
                self.ball_x,
                self.ball_y,
                self.ball_size,
                self.ball_size,
            ),
            arcade.color.WHITE_SMOKE
        )

    def _draw_center_line(self):
        center_x = WINDOW_WIDTH / 2
        dash_gap = round(20 * SCALE_Y)
        dash_len = round(10 * SCALE_Y)
        thickness = max(1, round(2 * SCALE))

        for y in range(0, WINDOW_HEIGHT, dash_gap):
            arcade.draw_line(center_x, y, center_x, y + dash_len, arcade.color.WHITE_SMOKE, thickness)

    def _draw_state_text(self):
        if self.game_state == "menu":
            self.title_text.draw()
            self.play_text.draw()
        elif self.game_state == "game_over":
            self.winner_text.draw()
            self.space_to_continue_text.draw()
        elif self.game_state == "serve":
            self.space_to_serve_text.draw()

    def on_draw(self):
        self.clear()

        if self.game_state == "menu":
            self._draw_state_text()
            return

        self.player1_score_text.draw()
        self.player2_score_text.draw()
        self._draw_game_objects()
        self._draw_center_line()
        self._draw_state_text()

    # -----------------------------
    # Update helpers
    # -----------------------------
    def _move_paddle(self, y_value, up_pressed, down_pressed, delta_time):
        if up_pressed and not down_pressed:
            y_value += self.paddle_speed * delta_time
        elif down_pressed and not up_pressed:
            y_value -= self.paddle_speed * delta_time

        paddle_bottom = y_value - self.paddle_height / 2
        paddle_top = y_value + self.paddle_height / 2

        if paddle_bottom < 0:
            y_value = self.paddle_height / 2
        elif paddle_top > WINDOW_HEIGHT:
            y_value = WINDOW_HEIGHT - self.paddle_height / 2

        return y_value

    def _update_paddles(self, delta_time):
        self.paddle1_y = self._move_paddle(
            self.paddle1_y,
            self.paddle1_up_pressed,
            self.paddle1_down_pressed,
            delta_time,
        )

        self.paddle2_y = self._move_paddle(
            self.paddle2_y,
            self.paddle2_up_pressed,
            self.paddle2_down_pressed,
            delta_time,
        )

    def _update_ball(self, delta_time):
        self.ball_x += self.ball_change_x * delta_time
        self.ball_y += self.ball_change_y * delta_time

    def _handle_wall_collision(self):
        ball_top = self.ball_y + self.ball_half_size
        ball_bottom = self.ball_y - self.ball_half_size

        if ball_bottom < 0:
            self.ball_change_y *= -1
            self.ball_y = self.ball_half_size
        elif ball_top > WINDOW_HEIGHT:
            self.ball_change_y *= -1
            self.ball_y = WINDOW_HEIGHT - self.ball_half_size

    def _promote_or_ramp_speed(self):
        if self.ball_speed < self.base_speed:
            self.ball_speed = self.base_speed
        else:
            self.ball_speed += 24

        if self.ball_speed > 1000:
            self.ball_speed = 1000

    def _handle_paddle_collision(self, paddle_x, paddle_y, ball_moving_left):
        paddle_top = paddle_y + self.paddle_height / 2
        paddle_bottom = paddle_y - self.paddle_height / 2
        paddle_left = paddle_x - self.paddle_width / 2
        paddle_right = paddle_x + self.paddle_width / 2

        ball_top = self.ball_y + self.ball_half_size
        ball_bottom = self.ball_y - self.ball_half_size
        ball_left = self.ball_x - self.ball_half_size
        ball_right = self.ball_x + self.ball_half_size

        collided = (
            ball_top > paddle_bottom and
            ball_bottom < paddle_top and
            ball_left < paddle_right and
            ball_right > paddle_left
        )

        if not collided:
            return

        if ball_moving_left and self.ball_change_x >= 0:
            return

        if not ball_moving_left and self.ball_change_x <= 0:
            return

        self._promote_or_ramp_speed()

        hit_offset = self.ball_y - paddle_y
        normalized = hit_offset / (self.paddle_height / 2)
        bounce_angle = normalized * self.max_bounce_angle

        self.ball_change_y = self.ball_speed * math.sin(bounce_angle)

        if ball_moving_left:
            self.ball_change_x = self.ball_speed * math.cos(bounce_angle)
            self.ball_x = paddle_right + self.ball_half_size
        else:
            self.ball_change_x = -self.ball_speed * math.cos(bounce_angle)
            self.ball_x = paddle_left - self.ball_half_size

    def _handle_scoring(self):
        ball_left = self.ball_x - self.ball_half_size
        ball_right = self.ball_x + self.ball_half_size

        if ball_right < 0:
            self.point_scored(2)
            if self.game_state == "playing":
                self.reset_on_point()

        elif ball_left > WINDOW_WIDTH:
            self.point_scored(1)
            if self.game_state == "playing":
                self.reset_on_point()

    def on_update(self, delta_time):
        if self.game_state != "playing":
            return

        self._update_paddles(delta_time)
        self._update_ball(delta_time)
        self._handle_wall_collision()

        self._handle_paddle_collision(
            paddle_x=self.paddle1_x,
            paddle_y=self.paddle1_y,
            ball_moving_left=True,
        )

        self._handle_paddle_collision(
            paddle_x=self.paddle2_x,
            paddle_y=self.paddle2_y,
            ball_moving_left=False,
        )

        self._handle_scoring()

    # -----------------------------
    # Input
    # -----------------------------
    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.W:
            self.paddle1_up_pressed = True
        elif key == arcade.key.S:
            self.paddle1_down_pressed = True

        if key == arcade.key.UP:
            self.paddle2_up_pressed = True
        elif key == arcade.key.DOWN:
            self.paddle2_down_pressed = True

        if key == arcade.key.SPACE:
            if self.game_state == "menu":
                self.reset_on_point()
            elif self.game_state == "serve":
                self.game_state = "playing"
            elif self.game_state == "game_over":
                self._reset_game()
                self.game_state = "menu"

    def on_key_release(self, key, key_modifiers):
        if key == arcade.key.W:
            self.paddle1_up_pressed = False
        elif key == arcade.key.S:
            self.paddle1_down_pressed = False

        if key == arcade.key.UP:
            self.paddle2_up_pressed = False
        elif key == arcade.key.DOWN:
            self.paddle2_down_pressed = False


def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    game = GameView()
    window.show_view(game)
    arcade.run()


if __name__ == "__main__":
    main()