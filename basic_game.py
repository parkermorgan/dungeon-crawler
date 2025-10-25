import arcade

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Drawing Shapes"

class ShapeWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.LIGHT_GRAY)
        self.circle_x = 300
        self.circle_y = 300
        self.circle_speed = 10
        self.change_x = 0
        self.change_y = 0

        self.wall_x = 300
        self.wall_y = 400
        self.wall_width = 400
        self.wall_height = 20

        self.gap_start = 250
        self.gap_end = 350

    def on_draw(self):
        self.clear() 
        arcade.draw_circle_filled(self.circle_x, self.circle_y, 50, arcade.color.BLUE)
        arcade.draw_rect_filled(arcade.XYWH(self.wall_x, self.wall_y, self.wall_width, self.wall_height), arcade.color.DARK_GRAY)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.change_y = self.circle_speed
        elif key == arcade.key.S:
            self.change_y = -self.circle_speed
        elif key == arcade.key.A:
            self.change_x = -self.circle_speed
        elif key == arcade.key.D:
            self.change_x = self.circle_speed
    
    def on_key_release(self, key, modifiers):
        if key in (arcade.key.W, arcade.key.S):
            self.change_y = 0
        elif key in (arcade.key.A, arcade.key.D):
            self.change_x = 0
    
    def on_update(self, delta_time):
        self.circle_x += self.change_x
        self.circle_y += self.change_y

        if self.circle_x < 50:
            self.circle_x = 50
        elif self.circle_x > SCREEN_WIDTH - 50:
            self.circle_x = SCREEN_WIDTH - 50

        if self.circle_y < 50:
            self.circle_y = 50
        elif self.circle_y > SCREEN_HEIGHT - 50:
            self.circle_y = SCREEN_HEIGHT - 50

def main():
    window = ShapeWindow() 
    arcade.run()

if __name__ == "__main__":
    main()