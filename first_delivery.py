import arcade
import random

# Main_Window
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
# Car_sketch
CAR_WIDTH = 50
CAR_HEIGHT = 30
# Obstacles_sketch
OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = 30
# SPEED
CAR_SPEED = 6
OBSTACLE_SPEED = 3.5


class CarGame(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height, "Panda Crash")

        # Car_position
        self.car_x = SCREEN_WIDTH / 2
        self.car_y = 100

        self.obstacles = []
        self.score = 0
        self.game_over = False
        self.held_keys = []  # Agregar esta línea

    def spawn_obstacle(self):
        x = random.randrange(100, 300)
        y = SCREEN_HEIGHT

        # For don't overlap obstacles
        while any(
            self.check_collision(
                x,
                y,
                OBSTACLE_WIDTH,
                OBSTACLE_HEIGHT,
                obstacle[0],
                obstacle[1],
                OBSTACLE_WIDTH,
                OBSTACLE_HEIGHT,
            )
            for obstacle in self.obstacles
        ):
            x = random.randrange(100, 300)

        self.obstacles.append((x, y))

    def on_draw(self):
        arcade.start_render()

        # Draw_Car
        arcade.draw_rectangle_filled(
            self.car_x, self.car_y, CAR_WIDTH, CAR_HEIGHT, arcade.color.RED
        )

        # Draw_Obstacles
        for obstacle in self.obstacles:
            x, y = obstacle
            arcade.draw_rectangle_filled(
                x + OBSTACLE_WIDTH / 2,
                y - OBSTACLE_HEIGHT / 2,
                OBSTACLE_WIDTH,
                OBSTACLE_HEIGHT,
                arcade.color.GREEN,
            )

        # Score
        arcade.draw_text(
            f"Score: {self.score}",
            10,
            SCREEN_HEIGHT - 20,
            arcade.color.WHITE,
            12,
            font_name="Kenney Future",
        )

        # GameOver
        if self.game_over:
            arcade.draw_text(
                "Game Over",
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2,
                arcade.color.WHITE,
                30,
                font_name="Kenney Blocks",
                anchor_x="center",
            )

    def on_update(self, delta_time):
        if not self.game_over:
            # Move_car
            if arcade.key.LEFT in self.held_keys and self.car_x > 100:
                self.car_x -= CAR_SPEED
            if arcade.key.RIGHT in self.held_keys and self.car_x < 300:
                self.car_x += CAR_SPEED

            # Move_Obstacles
            for i in range(len(self.obstacles)):
                x, y = self.obstacles[i]
                y -= OBSTACLE_SPEED
                self.obstacles[i] = (x, y)

            # Random_Obstacles
            # Probability
            if random.random() < 0.01:
                self.spawn_obstacle()

            # Crash_car
            obstacles2 = 0
            for obstacle in self.obstacles:
                obstacles2 += 1
                if self.check_collision(
                    self.car_x,
                    self.car_y,
                    CAR_WIDTH,
                    CAR_HEIGHT,
                    obstacle[0],
                    obstacle[1],
                    OBSTACLE_WIDTH,
                    OBSTACLE_HEIGHT,
                ):
                    self.game_over = True

            # Delete_obstacles
            self.obstacles = [(x, y) for x, y in self.obstacles if y > 0]

            # Score
            self.score += obstacles2

    def check_collision(self, x1, y1, w1, h1, x2, y2, w2, h2):
        return x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2

    # Key_action
    def on_key_press(self, key, modifiers):
        if key not in self.held_keys:
            self.held_keys.append(key)

    def on_key_release(self, key, modifiers):
        if key in self.held_keys:
            self.held_keys.remove(key)


def main():
    window = CarGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()


if __name__ == "__main__":
    main()
