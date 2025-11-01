import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "The Legend of Parker"

# I've broken up functionality into separate 'setup' functions to clean it up
class ShapeWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.setup_sound()
        self.setup_rooms()
        self.play_room_music()

        self.player_list = arcade.SpriteList()

        self.message = ""
        self.message_timer = 0

        

       
        
        # Create Player

        player_path = "assets/player/player_front.png"
        self.player_sprites = {
        "up": "assets/player/player_back.png",
        "down": "assets/player/player_front.png",
        "left": "assets/player/player_left.png",
        "right": "assets/player/player_right.png"
}
        self.player = arcade.Sprite(player_path, scale=1)
        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = SCREEN_HEIGHT // 2
        self.player_list.append(self.player)

        # Player movement
        self.change_x = 0
        self.change_y = 0

        # Score
        self.norm_key = 0
        self.master_key = 0

    def setup_sound(self):
            
            # Sound effects
            self.collect_key_sound = arcade.load_sound("assets/sounds/item get 1.wav")
            self.collect_master_key_sound = arcade.load_sound("assets/sounds/139-item-catch.mp3")
            self.open_door_sound = arcade.load_sound("assets/sounds/door_open.wav")
            
            # Background music for each room
            self.room_music ={
                0: arcade.load_sound("assets/sounds/hyrule_castle.mp3"),
                1: arcade.load_sound("assets/sounds/triforce_chamber.mp3")
            }

            self.background_player = None
    
    def play_room_music(self):

        if self.background_player:
            arcade.stop_sound(self.background_player)
        
        track = self.room_music.get(self.current_room)
        if track:
            self.background_player = arcade.play_sound(track, loop=True)

    def setup_rooms(self):

        # Initialize rooms list
        self.rooms = []
        self.current_room = 0

        # Room 1 
        walls_1 = arcade.SpriteList()

        # Vertical wall
        for i in range(7):
            wall = arcade.SpriteSolidColor(70, 70, 150, i * 55 + 100, arcade.color.JET )
            wall.center_x = 150  
            walls_1.append(wall)

        # Horizontal walls
        for i in range(7):
            wall = arcade.SpriteSolidColor(70, 70, i * 55, 450, arcade.color.JET)
            walls_1.append(wall)

        for i in range(7):
            wall2 = arcade.SpriteSolidColor(70, 70, 800 - i * 55, 450, arcade.color.JET)
            walls_1.append(wall2)

        # Room 2 
        walls_2 = arcade.SpriteList()

        # Top-border wall
        for i in range(15):
            wall = arcade.SpriteSolidColor(70, 70, i * 70, 570, arcade.color.JET)
            walls_2.append(wall)
        
        # Left and right border walls
        for i in range(15):
            wall2 = arcade.SpriteSolidColor(70, 70, 30, i * 55, arcade.color.JET)
            walls_2.append(wall2)
        
        for i in range(15):
            wall3 = arcade.SpriteSolidColor(70, 70, 770, i * 55, arcade.color.JET)
            walls_2.append(wall3)

        # Bottom-border walls
        for i in range(7):
            wall4 = arcade.SpriteSolidColor(70, 70, i * 55, 30, arcade.color.JET)
            walls_2.append(wall4)

        for i in range(7):
            wall5 = arcade.SpriteSolidColor(70, 70, 800 - i * 55, 30, arcade.color.JET)
            walls_2.append(wall5)
            
         # Calculate door width to fill the gap between two wall ends
        left_wall_right_edge = max(wall.center_x + wall.width / 2 for wall in walls_1 if wall.center_x < SCREEN_WIDTH / 2)
        right_wall_left_edge = min(wall.center_x - wall.width / 2 for wall in walls_1 if wall.center_x > SCREEN_WIDTH / 2)
        door_width = right_wall_left_edge - left_wall_right_edge

        # Empty list for rooms with no doors
        no_door_list = arcade.SpriteList()

        door_list_1 = arcade.SpriteList()
        door1 = arcade.SpriteSolidColor(70, 70, (left_wall_right_edge + right_wall_left_edge) / 2, 450, arcade.color.BISTRE)
        door1.width = door_width
        door1.center_x = (left_wall_right_edge + right_wall_left_edge) / 2
        door1.center_y = 450 
        door1.door_type = "master"
        door_list_1.append(door1)

        door2 = arcade.SpriteSolidColor(70, 70, 150, 35, arcade.color.BISTRE)
        door2.door_type = "normal"
        door_list_1.append(door2)

        # Empty list for rooms with no keys
        no_key_list = arcade.SpriteList()

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

        # Create second room for testing
        
        room_2 = {
            "walls": walls_2,
            "doors": no_door_list,
            "keys": no_key_list,
            "background_color": arcade.color.DARK_SLATE_GRAY
        }

        self.rooms.append(room_1)
        self.rooms.append(room_2)



    def update_player_sprite(self, direction):
        self.player.texture = arcade.load_texture(self.player_sprites[direction])

    def move_room(self, direction):
        # direction is 'left', 'right', 'up', or 'down'
        next_room = None
        if direction == "up" and self.current_room < len(self.rooms) - 1:
            next_room = self.current_room + 1
            self.player.center_y = 5  # Appear on bottom edge of next room
        elif direction == "down" and self.current_room > 0:
            next_room = self.current_room - 1
            self.player.center_y = SCREEN_HEIGHT - 5  # Appear on top edge of next room

        if next_room is not None:
            self.current_room = next_room
            self.play_room_music()
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
            self.move_room("left")
        elif self.player.right > SCREEN_WIDTH:
            self.move_room("right")

        # Keep player on screen vertically and handle room transitions
        if self.player.bottom < 0:
            self.move_room("down")
        elif self.player.top > SCREEN_HEIGHT:
            self.move_room("up")

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
                arcade.play_sound(self.collect_key_sound)
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
            self.update_player_sprite("right")
        elif key == arcade.key.A:
            self.change_x = -5
            self.update_player_sprite("left")
        elif key == arcade.key.W:
            self.change_y = 5
            self.update_player_sprite("up")
        elif key == arcade.key.S:
            self.change_y = -5
            self.update_player_sprite("down")

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