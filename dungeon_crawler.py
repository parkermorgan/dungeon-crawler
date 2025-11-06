# AI Disclaimer: Artificial Intelligence was used in the production of this program.
# AI was used to create boilerplate code, teach concepts due to low amount of online resources,
# and bug fixing. 

# Sprites: Parker Morgan, inspiration from 'The Legend of Zelda: A Link To The Past
# Sound effects: Juhani Junkala
# Music: HydroGene

import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Dungeon Crawler Prototype"

# I've broken up functionality into separate 'setup' functions to clean it up
class ShapeWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.load_font("assets/fonts/PressStart2P.ttf")
        self.setup_player()
        self.setup_sound()
        self.setup_rooms()
        self.play_room_music()

        self.collect = False
        self.collect_timer = 0

        self.message = "You must get into the next room!"
        self.message_timer = 180  
        self.message_coords = (250, 150)

        # Create key count
        self.key = 0
        self.master_key = 0
        self.health = 3
        # SpriteList for health icons
        self.hearts_list = arcade.SpriteList()
        self.player_health(self.health)

        
        self.flash_active = False
        self.flash_timer = 0

    def setup_player(self):

        self.player_list = arcade.SpriteList()

        player_path = "assets/player/player_front.png"
        self.player_textures = {
            "up": arcade.load_texture("assets/player/player_back.png"),
            "down": arcade.load_texture("assets/player/player_front.png"),
            "left": arcade.load_texture("assets/player/player_left.png"),
            "right": arcade.load_texture("assets/player/player_right.png"),
            "attack_up": arcade.load_texture("assets/player/attack/player_attack_up.png"),
            "attack_down": arcade.load_texture("assets/player/attack/player_attack_down.png"),
            "attack_left": arcade.load_texture("assets/player/attack/player_attack_left.png"),
            "attack_right": arcade.load_texture("assets/player/attack/player_attack_right.png"),
            "collect_large": arcade.load_texture("assets/player/action/player_collect_large.png"),
            "game_over": arcade.load_texture("assets/player/action/player_game_over.png"),
            "damage_up": arcade.load_texture("assets/player/action/player_game_over.png"),
            "damage_down": arcade.load_texture("assets/player/player_damage_front.png"),
        }

        self.player = arcade.Sprite(player_path, scale=1)
        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = SCREEN_HEIGHT // 2
        self.player_list.append(self.player)

        # Player movement
        self.change_x = 0
        self.change_y = 0

        # Player attack 
        self.player_attack = False
        self.attack_timer = 0
        self.attack_duration = 10
        self.last_direction = "down"

        self.action = False
        self.action_timer = 0


    def setup_sound(self):
            
            # Sound effects
            self.collect_key_sound = arcade.load_sound("assets/sounds/key.wav")
            self.open_door_sound = arcade.load_sound("assets/sounds/door_open.wav")
            self.collect_master_key_sound = arcade.load_sound("assets/sounds/master_key.wav")
            self.collect_crown_sound = arcade.load_sound("assets/sounds/crown_collect.wav")
            
            # Background music for each room
            self.room_music ={
                0: arcade.load_sound("assets/sounds/room.mp3"),
                1: arcade.load_sound("assets/sounds/final_room.mp3")
            }

            self.background_player = None
    
    def play_room_music(self):

        if self.background_player:
            arcade.stop_sound(self.background_player)
        
        track = self.room_music.get(self.current_room)
        if track:
            self.background_player = arcade.play_sound(track, loop=True, volume=0.1)

    def setup_rooms(self):

        # Initialize rooms list
        self.rooms = []
        self.current_room = 0

        # Empty wall list for testing
        walls_empty = arcade.SpriteList()

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

        # Create crown

        self.crown_list = arcade.SpriteList()
        self.no_crown = arcade.Sprite()

        self.crown = arcade.Sprite("assets/items/crown.png", scale=1)
        self.crown.center_x = SCREEN_WIDTH // 2
        self.crown.center_y = SCREEN_HEIGHT // 2

        self.crown_list.append(self.crown)

        # Create first room

        room_1 = {
            "walls": walls_1,
            "doors": door_list_1,
            "keys": key_list_1,
            "background_color": arcade.color.ARSENIC,
            "crown": self.no_crown
        }

        # Create second room
        room_2 = {
            "walls": walls_2,
            "doors": no_door_list,
            "keys": no_key_list,
            "background_color": arcade.color.COOL_BLACK,
            "crown": self.crown
        }

        # Add rooms to list

        self.rooms.append(room_1)
        self.rooms.append(room_2)

    def update_player_sprite(self, movement):
        if not self.player_attack or movement.startswith("attack_"):
            if movement in self.player_textures:
                self.player.texture = self.player_textures[movement]
            if movement in ["up", "down", "left", "right"]:
                self.last_direction = movement
    
    def start_attack(self):
        self.player_attack = True
        self.attack_timer = self.attack_duration
        self.update_player_sprite(f"attack_{self.last_direction}")

    def player_health(self, health):
        self.health = health

        # Clear old hearts
        self.hearts_list = arcade.SpriteList()

        # Add one heart per health point
        for i in range(self.health):
            heart = arcade.Sprite("assets/gui/heart.png", scale=1.25)
            heart.center_x = 30 + i * 40  # space hearts horizontally
            heart.center_y = SCREEN_HEIGHT - 30
            self.hearts_list.append(heart)
        
 
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

            if self.current_room == 1:
                self.player.center_x = SCREEN_WIDTH // 2
                self.message = "You have reached the final room! Relish in your glory. Collect the crown to quit."
                self.message_timer = 300
                self.message_coords = (250, 400)

            elif self.current_room == 0:
                self.message = "What are you doing back here?"
                self.message_timer = 150
                self.message_coords = (250, 300)

    def text_box(self, text, left, bottom):
        box_width = 300
        box_height = 100
        box_left = left
        box_bottom = bottom

        arcade.draw_lbwh_rectangle_filled(left=box_left, bottom=box_bottom, width=box_width, height=box_height, color=(0, 0, 0, 200))
        arcade.draw_lbwh_rectangle_outline(left=box_left, bottom=box_bottom, width=box_width, height=box_height, color=arcade.color.WHITE)

        # Create an arcade.Text object for wrapped text and draw it
        text_obj = arcade.Text(
            text,
            box_left + 10,
            box_bottom + 40,
            arcade.color.WHITE,
            10,
            width=box_width - 20,
            align='center',
            font_name="Press Start 2P",
            anchor_x="left",
            anchor_y="bottom",
            multiline=True
        )
        text_obj.draw()

    # Begin drawing program
    def on_draw(self):
        self.clear()
        current_room = self.rooms[self.current_room]
        arcade.set_background_color(current_room["background_color"])
        current_room["keys"].draw()
        self.player_list.draw()
        # Draw hearts
        self.hearts_list.draw()
        current_room["walls"].draw()
        current_room["doors"].draw()
        if self.current_room == 1:
            self.crown_list.draw()
        # Draw floating items if they exist
        if hasattr(self, "floating_items"):
            self.floating_items.draw()

        arcade.draw_text(f"Keys: {self.key} | Master Keys: {self.master_key}", 10, 10, arcade.color.WHITE, 12, font_name="Press Start 2P")

        if self.message:
            x, y = getattr(self, 'message_coords', (250, 80))
            self.text_box(self.message, x, y)

    def damage_flash(self, damage_direction, normal_direction):
        if self.flash_active:
            self.flash_timer += 1

            damage_texture = self.player_textures.get(damage_direction)
            normal_texture = self.player_textures.get(normal_direction)

            # Alternate the texture every 5 frames
            if self.flash_timer % 5 == 0:
                if self.player.texture == damage_texture:
                    self.player.texture = normal_texture
                else:
                    self.player.texture = damage_texture

            # End the flash after 45 frames
            if self.flash_timer > 45:
                self.flash_active = False
                self.player.texture = normal_texture

    def on_update(self, delta_time):
        current_room = self.rooms[self.current_room]

        # Handle directional damage flash
        if self.flash_active:
            dir_map = {
                "up": ("damage_up", "up"),
                "down": ("damage_down", "down"),
                "left": ("damage_left", "left"),
                "right": ("damage_right", "right")
            }
            damage_dir, normal_dir = dir_map.get(self.last_direction, ("damage_down", "down"))
            self.damage_flash(damage_dir, normal_dir)

        if self.health == 0:
            if not self.flash_active and self.flash_timer > 0:
                self.update_player_sprite("game_over")
                self.message = "Game over"
                self.message_timer = 120
                arcade.schedule(lambda delta_time: arcade.close_window(), 2.0)

        # Collecting items
        if self.collect:
            self.collect_timer -= 1
            if self.collect_timer <= 0:
                self.collect = False
                self.update_player_sprite("down")
                if hasattr(self, "floating_items"):
                    self.floating_items = arcade.SpriteList()

        # Collision checks
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

        # Attack timing
        if self.player_attack:
            self.attack_timer -= 1
            if self.attack_timer <= 0:
                self.player_attack = False
                self.update_player_sprite(self.last_direction)

        for door in current_room["doors"][:]: 
            if door.door_type == "normal":
                if self.key < 1 and arcade.check_for_collision(self.player, door):
                    self.message = "You need a Key!"
                    self.message_timer = 120
                if self.key > 0 and arcade.check_for_collision(self.player, door):
                    arcade.play_sound(self.open_door_sound)
                    current_room["doors"].remove(door)
                    self.key -= 1

            elif door.door_type == "master":
                if self.master_key < 1 and arcade.check_for_collision(self.player, door):
                    self.message = "You need the Master Key!"
                    self.message_timer = 120
                elif self.master_key >= 1 and arcade.check_for_collision(self.player, door):
                    arcade.play_sound(self.open_door_sound)
                    current_room["doors"].remove(door)
                    self.master_key -= 1
                
                    

        # Check for door collision to block player if door is closed
        for door in current_room["doors"]:
            if arcade.check_for_collision(self.player, door):
                if self.change_x > 0:
                    self.player.right = door.left
                elif self.change_x < 0:
                    self.player.left = door.right
                if self.change_y > 0:
                    self.player.top = door.bottom
                elif self.change_y < 0:
                    self.player.bottom = door.top

        # Collecting keys collision checks
        key_hit_list = arcade.check_for_collision_with_list(self.player, current_room["keys"])
        
        for key in key_hit_list:
            if key.type == "normal":
                key.remove_from_sprite_lists()
                arcade.play_sound(self.collect_key_sound)
                self.key += 1
                self.message = "You picked up a key!"
                self.message_timer = 90  # ~1.5 seconds
            elif key.type == "master":
                key.remove_from_sprite_lists()
                arcade.play_sound(self.collect_master_key_sound)
                self.master_key += 1
                self.message = "You picked up the Master Key!"
                self.message_timer = 120  # ~2 seconds
            
            self.update_player_sprite("collect_large")
            self.change_x = 0
            self.change_y = 0
            self.collect = True
            self.collect_timer = 60

            image_path = "assets/items/key.png" if key.type == "normal" else "assets/items/boss_key.png"
            item = arcade.Sprite(image_path, scale=1)
            item.center_x = self.player.center_x
            item.center_y = self.player.center_y + 50
            if not hasattr(self, "floating_items"):
                self.floating_items = arcade.SpriteList()
            self.floating_items.append(item)

        if self.current_room == 1 and self.crown is not None and arcade.check_for_collision(self.player, self.crown):
            arcade.play_sound(self.collect_crown_sound)
            self.update_player_sprite("collect_large")
            self.message = "Thank you for playing!"
            self.message_timer = 180
            self.collect = True
            # Show the crown above the player
            item = arcade.Sprite("assets/items/crown.png", scale=1)
            item.center_x = self.player.center_x
            item.center_y = self.player.center_y + 50
            if not hasattr(self, "floating_items"):
                self.floating_items = arcade.SpriteList()
            self.floating_items.append(item)
            self.collect_timer = 999
            arcade.schedule(lambda delta_time: arcade.close_window(), 2.0)
            self.crown.remove_from_sprite_lists()
            self.crown = None


            self.change_x = 0
            self.change_y = 0
        
        # Room transitions
        if self.player.left < 0:
            self.move_room("left")
        elif self.player.right > SCREEN_WIDTH:
            self.move_room("right")

        if self.player.bottom < 0:
            self.move_room("down")
        elif self.player.top > SCREEN_HEIGHT:
            self.move_room("up")

        if self.player.left < 0:
            self.player.left = 0
        elif self.player.right > SCREEN_WIDTH:
            self.player.right = SCREEN_WIDTH

        if self.player.bottom < 0:
            self.player.bottom = 0
        elif self.player.top > SCREEN_HEIGHT:
            self.player.top = SCREEN_HEIGHT

    
        if self.message_timer > 0:
            self.message_timer -= 1
        else:
            self.message = ""
    
    # Player movement
    def on_key_press(self, key, modifiers):
        if self.collect:
            return
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
        elif key == arcade.key.SPACE and not self.player_attack:
            self.start_attack()
        elif key == arcade.key.H:
            if self.health > 0:
                self.health = max(0, self.health - 1)
                self.player_health(self.health)
                self.flash_active = True
                self.flash_timer = 0

    def on_key_release(self, key, modifiers):
        if self.collect:
            return
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