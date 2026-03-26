import random
import arcade
import math

# -----------------------------
# Window
# -----------------------------
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 576
WINDOW_TITLE = "Ping"

# -----------------------------
# Base layout
# -----------------------------
BASE_WIDTH = 1280
BASE_HEIGHT = 720

# Design choice:
# Scaling is based on a 1280x720 reference layout instead of manually rewriting
# every size and speed value. This keeps proportions and gameplay feel consistent
# when resizing the window.

# -----------------------------
# Scaling
# -----------------------------
SCALE_X = WINDOW_WIDTH / BASE_WIDTH
SCALE_Y = WINDOW_HEIGHT / BASE_HEIGHT
SCALE = min(SCALE_X, SCALE_Y)

# -----------------------------
# Base speeds
# -----------------------------
BASE_SERVE_SPEED = 240
BASE_RALLY_SPEED = 720
BASE_PADDLE_SPEED = 480
BASE_VERTICAL_SPEED = 150
BASE_SPEED_RAMP = 24
BASE_MAX_SPEED = BASE_RALLY_SPEED * 1.6


class GameView(arcade.View):

    def __init__(self):
        super().__init__()

        # -----------------------------
        # Visual / window setup
        # -----------------------------
        self.background_color = arcade.color.BLACK
        arcade.load_font("Fonts/pong-score.otf")
        arcade.load_font("Fonts/bit5x3.ttf")

        # -----------------------------
        # Shared layout values
        # -----------------------------
        self.screen_center_x = WINDOW_WIDTH / 2
        self.screen_center_y = WINDOW_HEIGHT / 2

        # -----------------------------
        # Game state
        # -----------------------------
        self.game_state = "menu"

        # Design choice:
        # Defining explicit game flow; menu -> serve -> playing -> game over

        # -----------------------------
        # Paddle properties
        # -----------------------------
        self.paddle_width = round(20 * SCALE_X)
        self.paddle_height = round(150 * SCALE_Y)
        self.paddle_speed = BASE_PADDLE_SPEED * SCALE
        self.max_bounce_angle = math.radians(75)

        # -----------------------------
        # Paddle positions
        # -----------------------------
        self.paddle_margin_x = round(32 * SCALE_X)
        self.paddle1_x = self.paddle_margin_x
        self.paddle1_y = self.screen_center_y
        self.paddle2_x = WINDOW_WIDTH - self.paddle_margin_x
        self.paddle2_y = self.screen_center_y

        # Design choice:
        # Paddle size, spacing, and speed are all scaled from base layout, to again preserve proportions and feel when resizing window.

        # -----------------------------
        # Paddle input state
        # -----------------------------
        self.paddle1_up_pressed = False
        self.paddle1_down_pressed = False
        self.paddle2_up_pressed = False
        self.paddle2_down_pressed = False

        # Design choice:
        # # Using booleans instead of one movement variable for smoother input

        # -----------------------------
        # Ball state
        # -----------------------------
        self.ball_size = round(20 * SCALE)
        self.ball_half_size = self.ball_size / 2
        self.ball_x = self.screen_center_x
        self.ball_y = self.screen_center_y

        # -----------------------------
        # Ball movement
        # -----------------------------
        self.serve_speed = BASE_SERVE_SPEED * SCALE
        self.base_speed = BASE_RALLY_SPEED * SCALE
        self.speed_ramp = BASE_SPEED_RAMP * SCALE
        self.max_speed = BASE_MAX_SPEED * SCALE

        self.ball_speed = self.serve_speed
        self.ball_change_x = -self.ball_speed
        self.ball_change_y = 0

        # Design choice:
        # Went with different ball speeds depending on the game. Serve speed is slower to allow players to react, 
        # while rally speed is faster for better gameplay. 
        # Speed ramp increases rally speed after each paddle hit, up to a max speed, to keep gameplay from stagnating.

        # -----------------------------
        # Score state
        # -----------------------------
        self.player1_score = 0
        self.player2_score = 0
        self.last_scoring_player = 1

        # -----------------------------
        # Text sizes
        # -----------------------------
        self.score_font_size = round(50 * SCALE)
        self.title_font_size = round(60 * SCALE)
        self.winner_font_size = round(45 * SCALE)
        self.prompt_font_size = round(20 * SCALE)
        self.menu_font_size = round(25 * SCALE)

        # -----------------------------
        # Text objects
        # -----------------------------
        self._create_text_objects()

    # -----------------------------
    # Text helpers
    # -----------------------------
    def _create_text_objects(self):
        self.player1_score_text = arcade.Text(
            f"{self.player1_score}",
            self.screen_center_x - (65 * SCALE_X),
            WINDOW_HEIGHT - (90 * SCALE_Y),
            color=arcade.color.WHITE_SMOKE,
            font_size=self.score_font_size,
            font_name="Pong Score",
            anchor_x="right",
        )

        self.player2_score_text = arcade.Text(
            f"{self.player2_score}",
            self.screen_center_x + (85 * SCALE_X),
            WINDOW_HEIGHT - (90 * SCALE_Y),
            color=arcade.color.WHITE_SMOKE,
            font_size=self.score_font_size,
            font_name="Pong Score",
            anchor_x="left",
        )

        self.menu_title_text = arcade.Text(
            "PING",
            self.screen_center_x,
            self.screen_center_y + (100 * SCALE_Y),
            color=arcade.color.WHITE_SMOKE,
            font_size=self.title_font_size,
            font_name="Bit5x3",
            anchor_x="center",
        )

        self.menu_prompt_text = arcade.Text(
            "Press SPACE to Play",
            self.screen_center_x,
            self.screen_center_y,
            color=arcade.color.WHITE_SMOKE,
            font_size=self.menu_font_size,
            font_name="Bit5x3",
            anchor_x="center",
        )

        self.game_over_title_text = arcade.Text(
            "",
            self.screen_center_x,
            self.screen_center_y,
            color=arcade.color.WHITE_SMOKE,
            font_size=self.winner_font_size,
            font_name="Bit5x3",
            anchor_x="center",
        )

        self.game_over_prompt_text = arcade.Text(
            "Press SPACE to Continue",
            self.screen_center_x,
            self.screen_center_y - (50 * SCALE_Y),
            color=arcade.color.WHITE_SMOKE,
            font_size=self.prompt_font_size,
            font_name="Bit5x3",
            anchor_x="center",
        )

        self.serve_prompt_text = arcade.Text(
            "Press SPACE to Serve",
            self.screen_center_x,
            self.screen_center_y + (50 * SCALE_Y),
            color=arcade.color.WHITE_SMOKE,
            font_size=self.prompt_font_size,
            font_name="Bit5x3",
            anchor_x="center",
        )

    def _update_score_text(self):
        self.player1_score_text.text = f"{self.player1_score}"
        self.player2_score_text.text = f"{self.player2_score}"

    # -----------------------------
    # Reset helpers
    # -----------------------------
    def _reset_scores(self):
        self.player1_score = 0
        self.player2_score = 0
        self._update_score_text()

    def _reset_paddles(self):
        self.paddle1_y = self.screen_center_y
        self.paddle2_y = self.screen_center_y

        self.paddle1_up_pressed = False
        self.paddle1_down_pressed = False
        self.paddle2_up_pressed = False
        self.paddle2_down_pressed = False

    def _reset_ball(self):
        self.ball_x = self.screen_center_x
        self.ball_y = self.screen_center_y
        self.ball_speed = self.serve_speed
        self.ball_change_x = -self.serve_speed
        self.ball_change_y = 0

    def _reset_on_point(self):
        self.ball_x = self.screen_center_x
        self.ball_y = self.screen_center_y
        self.ball_speed = self.serve_speed

        if self.last_scoring_player == 1:
            self.ball_change_x = -self.serve_speed
        else:
            self.ball_change_x = self.serve_speed

        self.ball_change_y = random.choice([-BASE_VERTICAL_SPEED, BASE_VERTICAL_SPEED]) * SCALE
        self.game_state = "serve"

    def _reset_game(self):
        self.game_over_title_text.text = ""
        self.last_scoring_player = 1

        self._reset_scores()
        self._reset_paddles()
        self._reset_ball()

    # -----------------------------
    # Score / game state helpers
    # -----------------------------
    def _award_point(self, scoring_player):
        if scoring_player == 1:
            self.player1_score += 1
            self.last_scoring_player = 1
        else:
            self.player2_score += 1
            self.last_scoring_player = 2

        self._update_score_text()

        if self.player1_score >= 2:
            self.game_state = "game_over"
            self.game_over_title_text.text = "Player 1 Wins!"
        elif self.player2_score >= 2:
            self.game_state = "game_over"
            self.game_over_title_text.text = "Player 2 Wins!"

    # -----------------------------
    # Geometry helpers
    # -----------------------------
    def _get_ball_edges(self):
        return (
            self.ball_y + self.ball_half_size,
            self.ball_y - self.ball_half_size,
            self.ball_x - self.ball_half_size,
            self.ball_x + self.ball_half_size,
        )

    def _get_paddle_edges(self, paddle_x, paddle_y):
        return (
            paddle_y + self.paddle_height / 2,
            paddle_y - self.paddle_height / 2,
            paddle_x - self.paddle_width / 2,
            paddle_x + self.paddle_width / 2,
        )

    # -----------------------------
    # Draw helpers
    # -----------------------------
    def _draw_score(self):
        self.player1_score_text.draw()
        self.player2_score_text.draw()

    def _draw_game_objects(self):
        arcade.draw_rect_filled(
            arcade.rect.XYWH(self.paddle1_x, self.paddle1_y, self.paddle_width, self.paddle_height),
            arcade.color.WHITE_SMOKE,
        )
        arcade.draw_rect_filled(
            arcade.rect.XYWH(self.paddle2_x, self.paddle2_y, self.paddle_width, self.paddle_height),
            arcade.color.WHITE_SMOKE,
        )
        arcade.draw_rect_filled(
            arcade.rect.XYWH(self.ball_x, self.ball_y, self.ball_size, self.ball_size),
            arcade.color.WHITE_SMOKE,
        )

    def _draw_center_line(self):
        dash_gap = round(20 * SCALE_Y)
        dash_len = round(10 * SCALE_Y)
        thickness = max(1, round(2 * SCALE))

        for y in range(0, WINDOW_HEIGHT, dash_gap):
            arcade.draw_line(self.screen_center_x, y, self.screen_center_x, y + dash_len, arcade.color.WHITE_SMOKE, thickness)

    def _draw_menu(self):
        self.menu_title_text.draw()
        self.menu_prompt_text.draw()

    def _draw_serve_screen(self):
        self.serve_prompt_text.draw()

    def _draw_game_over_screen(self):
        self.game_over_title_text.draw()
        self.game_over_prompt_text.draw()

    def _draw_gameplay(self):
        self._draw_score()
        self._draw_game_objects()
        self._draw_center_line()

    def on_draw(self):
        self.clear()

        if self.game_state == "menu":
            self._draw_menu()
            return

        self._draw_gameplay()

        if self.game_state == "serve":
            self._draw_serve_screen()
        elif self.game_state == "game_over":
            self._draw_game_over_screen()

    # -----------------------------
    # Update helpers
    # -----------------------------
    def _move_paddle(self, y_value, up_pressed, down_pressed,delta_time):
        if up_pressed and not down_pressed:
            y_value += self.paddle_speed * delta_time
        elif down_pressed and not up_pressed:
            y_value -= self.paddle_speed * delta_time

        if y_value - self.paddle_height / 2 < 0:
            return self.paddle_height / 2
        if y_value + self.paddle_height / 2 > WINDOW_HEIGHT:
            return WINDOW_HEIGHT - self.paddle_height / 2

        return y_value

    def _update_paddles(self, delta_time):
        self.paddle1_y = self._move_paddle(self.paddle1_y, self.paddle1_up_pressed, self.paddle1_down_pressed, delta_time)
        self.paddle2_y = self._move_paddle(self.paddle2_y, self.paddle2_up_pressed, self.paddle2_down_pressed, delta_time)

    # Design choice:
    # Using delta time for ball movement so speed is consistent across frame rates.
    # Prevents the ball from moving faster/slower depending on FPS and improves smoothness.

    def _update_ball(self, delta_time):
        self.ball_x += self.ball_change_x * delta_time
        self.ball_y += self.ball_change_y * delta_time

    def _handle_wall_collision(self):
        top, bottom, _, _ = self._get_ball_edges()

        if bottom < 0:
            self.ball_change_y *= -1
            self.ball_y = self.ball_half_size
        elif top > WINDOW_HEIGHT:
            self.ball_change_y *= -1
            self.ball_y = WINDOW_HEIGHT - self.ball_half_size

    def _promote_or_ramp_speed(self):
        if self.ball_speed < self.base_speed:
            self.ball_speed = self.base_speed
        else:
            self.ball_speed += self.speed_ramp

        if self.ball_speed > self.max_speed:
            self.ball_speed = self.max_speed

    def _handle_paddle_collision(self, paddle_x, paddle_y, ball_moving_left):
        p_top, p_bot, p_left, p_right = self._get_paddle_edges(paddle_x, paddle_y)
        b_top, b_bot, b_left, b_right = self._get_ball_edges()

        if not (b_top > p_bot and b_bot < p_top and b_left < p_right and b_right > p_left):
            return

        if ball_moving_left and self.ball_change_x >= 0:
            return
        if not ball_moving_left and self.ball_change_x <= 0:
            return

        self._promote_or_ramp_speed()

        offset = self.ball_y - paddle_y
        normalized = offset / (self.paddle_height / 2)
        angle = normalized * self.max_bounce_angle

        self.ball_change_y = self.ball_speed * math.sin(angle)

        if ball_moving_left:
            self.ball_change_x = self.ball_speed * math.cos(angle)
            self.ball_x = p_right + self.ball_half_size
        else:
            self.ball_change_x = -self.ball_speed * math.cos(angle)
            self.ball_x = p_left - self.ball_half_size

    def _handle_scoring(self):
        _, _, left, right = self._get_ball_edges()

        if right < 0:
            self._award_point(2)
            if self.game_state == "playing":
                self._reset_on_point()
        elif left > WINDOW_WIDTH:
            self._award_point(1)
            if self.game_state == "playing":
                self._reset_on_point()

    def on_update(self, delta_time):
        if self.game_state != "playing":
            return

        self._update_paddles(delta_time)
        self._update_ball(delta_time)
        self._handle_wall_collision()

        self._handle_paddle_collision(self.paddle1_x, self.paddle1_y, True)
        self._handle_paddle_collision(self.paddle2_x, self.paddle2_y, False)

        self._handle_scoring()

    # -----------------------------
    # Input
    # -----------------------------
    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.paddle1_up_pressed = True
        elif key == arcade.key.S:
            self.paddle1_down_pressed = True
        elif key == arcade.key.UP:
            self.paddle2_up_pressed = True
        elif key == arcade.key.DOWN:
            self.paddle2_down_pressed = True

        if key == arcade.key.SPACE:
            if self.game_state == "menu":
                self._reset_on_point()
            elif self.game_state == "serve":
                self.game_state = "playing"
            elif self.game_state == "game_over":
                self._reset_game()
                self.game_state = "menu"

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:
            self.paddle1_up_pressed = False
        elif key == arcade.key.S:
            self.paddle1_down_pressed = False
        elif key == arcade.key.UP:
            self.paddle2_up_pressed = False
        elif key == arcade.key.DOWN:
            self.paddle2_down_pressed = False


def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    window.show_view(GameView())
    arcade.run()


if __name__ == "__main__":
    main()