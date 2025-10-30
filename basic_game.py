import arcade
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Coin Collector Collision Example"

class ShapeWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        
        # Sound functionality
        self.background_music = arcade.load_sound("assets/sounds/hyrule_castle.mp3")
        self.background_player = None
        self.collect_key_sound = arcade.load_sound("assets/sounds/item get 1.wav")
        self.collect_master_key_sound = arcade.load_sound("assets/sounds/139-item-catch.mp3")
        self.open_door_sound = arcade.load_sound("assets/sounds/door_open.wav")

        self.background_player = arcade.play_sound(self.background_music, loop=True)

        self.player_list = arcade.SpriteList()

        self.background_color = arcade.color.ARSENIC

        self.message = ""
        self.message_timer = 0

        # Initialize rooms list
        self.rooms = []
        self.current_room = 0

        # Room 1 setup
        walls_1 = arcade.SpriteList()
        for i in range(7):
            wall = arcade.Sprite(":resources:/images/tiles/brickGrey.png", scale=0.5)
            wall.center_x = 150  
            wall.center_y = i * 55 + 100 
            walls_1.append(wall)

        # Horizontal wall 7 blocks long
        for i in range(7):
            wall = arcade.Sprite(":resources:/images/tiles/brickGrey.png", scale=0.5)
            wall.center_x = i * 55
            wall.center_y = 450
            walls_1.append(wall)

        for i in range(7):
            wall2 = arcade.Sprite(":resources:/images/tiles/brickGrey.png", scale=0.5)
            wall2.center_x = 800 - i * 55
            wall2.center_y = 450
            walls_1.append(wall2)

        # Calculate door width to fill the gap between two wall ends
        left_wall_right_edge = max(wall.center_x + wall.width / 2 for wall in walls_1 if wall.center_x < SCREEN_WIDTH / 2)
        right_wall_left_edge = min(wall.center_x - wall.width / 2 for wall in walls_1 if wall.center_x > SCREEN_WIDTH / 2)
        door_width = right_wall_left_edge - left_wall_right_edge

        door_list_1 = arcade.SpriteList()
        door1 = arcade.Sprite(":resources:/images/tiles/boxCrate_double.png", scale=0.5)
        door1.width = door_width
        door1.center_x = (left_wall_right_edge + right_wall_left_edge) / 2
        door1.center_y = 450  # same height as your horizontal wall
        door1.door_type = "master"
        door_list_1.append(door1)

        door2 = arcade.Sprite(":resources:/images/tiles/boxCrate_double.png", scale=0.5)
        door2.width = 70
        door2.center_x = 150
        door2.center_y = 35
        door2.door_type = "normal"
        door_list_1.append(door2)

        key_list_1 = arcade.SpriteList()
        key = arcade.Sprite("assets/items/key.png", scale=1)
        key.center_x = 700
        key.center_y = 100
        key.type = "normal"
        key_list_1.append(key)

        mas_key = arcade.Sprite("assets/items/boss_key.png", scale=1)
        mas_key.center_x = 50
        mas_key.center_y = 350
        mas_key.type = "master"
        key_list_1.append(mas_key)

        room_1 = {
            "walls": walls_1,
            "doors": door_list_1,
            "keys": key_list_1,
            "background_color": arcade.color.ARSENIC
        }

        # Room 2 setup (different layout)
        walls_2 = arcade.SpriteList()
        for i in range(10):
            wall = arcade.Sprite(":resources:/images/tiles/brickGrey.png", scale=0.5)
            wall.center_x = i * 80 + 40
            wall.center_y = 550
            walls_2.append(wall)

        for i in range(8):
            wall = arcade.Sprite(":resources:/images/tiles/brickGrey.png", scale=0.5)
            wall.center_x = 40
            wall.center_y = i * 70 + 50
            walls_2.append(wall)

        door_list_2 = arcade.SpriteList()
        door3 = arcade.Sprite(":resources:/images/tiles/boxCrate_double.png", scale=0.5)
        door3.width = 70
        door3.center_x = 760
        door3.center_y = 100
        door3.door_type = "normal"
        door_list_2.append(door3)

        key_list_2 = arcade.SpriteList()
        key2 = arcade.Sprite("assets/items/key.png", scale=1)
        key2.center_x = 400
        key2.center_y = 300
        key2.type = "normal"
        key_list_2.append(key2)

        room_2 = {
            "walls": walls_2,
            "doors": door_list_2,
            "keys": key_list_2,
            "background_color": arcade.color.DARK_SLATE_GRAY
        }

        self.rooms.append(room_1)
        self.rooms.append(room_2)

        # Player setup
        self.player = arcade.Sprite("assets/player/link.png", scale=0.05)
        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = SCREEN_HEIGHT // 2
        self.player_list.append(self.player)

        # Player movement
        self.change_x = 0
        self.change_y = 0

        # Score
        self.norm_key = 0
        self.master_key = 0

    def transition_to_next_room(self, direction):
        # direction is 'left', 'right', 'up', or 'down'
        next_room = None
        if direction == "right" and self.current_room < len(self.rooms) - 1:
            next_room = self.current_room + 1
            self.player.center_x = 5  # Appear on left edge of next room
        elif direction == "left" and self.current_room > 0:
            next_room = self.current_room - 1
            self.player.center_x = SCREEN_WIDTH - 5  # Appear on right edge of next room
        elif direction == "up" and self.current_room < len(self.rooms) - 1:
            next_room = self.current_room + 1
            self.player.center_y = 5  # Appear on bottom edge of next room
        elif direction == "down" and self.current_room > 0:
            next_room = self.current_room - 1
            self.player.center_y = SCREEN_HEIGHT - 5  # Appear on top edge of next room

        if next_room is not None:
            self.current_room = next_room
            # Reset movement to prevent immediate re-transition
            self.change_x = 0
            self.change_y = 0

    def on_draw(self):
        self.clear()
        current_room = self.rooms[self.current_room]
        arcade.set_background_color(current_room["background_color"])
        current_room["keys"].draw()
        self.player_list.draw()
        current_room["walls"].draw()
        current_room["doors"].draw()
    

        arcade.draw_text(f"Keys: {self.norm_key} | Master Keys: {self.master_key}", 10, 10, arcade.color.WHITE, 16)

        if self.message:
            alpha = int(255 * (self.message_timer / 120))
            arcade.draw_text(self.message, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                            (255, 255, 255, alpha), 20, anchor_x="center")

    def on_update(self, delta_time):
        current_room = self.rooms[self.current_room]

        # Move player
        self.player.center_x += self.change_x
        hit_list = arcade.check_for_collision_with_list(self.player, current_room["walls"])
        if hit_list:
            if self.change_x > 0:
                self.player.right = min(w.left for w in hit_list)
            elif self.change_x < 0:
                self.player.left = max(w.right for w in hit_list)

        self.player.center_y += self.change_y
        hit_list = arcade.check_for_collision_with_list(self.player, current_room["walls"])
        if hit_list:
            if self.change_y > 0:
                self.player.top = min(w.bottom for w in hit_list)
            elif self.change_y < 0:
                self.player.bottom = max(w.top for w in hit_list)

        for door in current_room["doors"][:]:  # use a copy since we might remove items
            if door.door_type == "normal":
                if self.norm_key < 1 and arcade.check_for_collision(self.player, door):
                    self.message = "You need a Key!"
                    self.message_timer = 120
                if self.norm_key > 0 and arcade.check_for_collision(self.player, door):
                    arcade.play_sound(self.open_door_sound)
                    current_room["doors"].remove(door)
                    self.norm_key -= 1
                    self.message = "You used a key!"
                    self.message_timer = 60

            elif door.door_type == "master":
                if self.master_key < 1 and arcade.check_for_collision(self.player, door):
                    self.message = "You need the Master Key!"
                    self.message_timer = 120
                elif self.master_key >= 1 and arcade.check_for_collision(self.player, door):
                    arcade.play_sound(self.open_door_sound)
                    current_room["doors"].remove(door)
                    self.master_key -= 1
                    self.message = "You used the Master Key!"
                    self.message_timer = 60
                    

        # Check for door collision to block player if door is closed
        for door in current_room["doors"]:
            if arcade.check_for_collision(self.player, door):
                # Push player back (simple example)
                if self.change_x > 0:
                    self.player.right = door.left
                elif self.change_x < 0:
                    self.player.left = door.right
                if self.change_y > 0:
                    self.player.top = door.bottom
                elif self.change_y < 0:
                    self.player.bottom = door.top
        
        # Keep player on screen horizontally and handle room transitions
        if self.player.left < 0:
            self.transition_to_next_room("left")
        elif self.player.right > SCREEN_WIDTH:
            self.transition_to_next_room("right")

        # Keep player on screen vertically and handle room transitions
        if self.player.bottom < 0:
            self.transition_to_next_room("down")
        elif self.player.top > SCREEN_HEIGHT:
            self.transition_to_next_room("up")

        # Clamp player position in current room if no transition
        if self.player.left < 0:
            self.player.left = 0
        elif self.player.right > SCREEN_WIDTH:
            self.player.right = SCREEN_WIDTH

        if self.player.bottom < 0:
            self.player.bottom = 0
        elif self.player.top > SCREEN_HEIGHT:
            self.player.top = SCREEN_HEIGHT

        key_hit_list = arcade.check_for_collision_with_list(self.player, current_room["keys"])
        for key in key_hit_list:
            if key.type == "normal":
                key.remove_from_sprite_lists()
                arcade.play_sound(self.collect_key_sound)
                self.norm_key += 1
                self.message = "You picked up a key!"
                self.message_timer = 90  # ~1.5 seconds
            elif key.type == "master":
                key.remove_from_sprite_lists()
                arcade.play_sound(self.collect_master_key_sound)
                self.master_key += 1
                self.message = "You picked up the Master Key!"
                self.message_timer = 120  # ~2 seconds
    
        if self.message_timer > 0:
            self.message_timer -= 1
        else:
            self.message = ""

    def on_key_press(self, key, modifiers):
        if key == arcade.key.D:
            self.change_x = 5
        elif key == arcade.key.A:
            self.change_x = -5
        elif key == arcade.key.W:
            self.change_y = 5
        elif key == arcade.key.S:
            self.change_y = -5

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.D, arcade.key.A):
            self.change_x = 0
        elif key in (arcade.key.W, arcade.key.S):
            self.change_y = 0

    def on_close(self):
        if self.background_player:
            arcade.stop_sound(self.background_player)
        super().on_close()

def main():
    window = ShapeWindow()
    arcade.run()

if __name__ == "__main__":
    main()