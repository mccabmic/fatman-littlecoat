import tcod as libtcod
from entity import Entity, get_blocking_entities_at_location
from render_functions import render_all, clear_all
from input_handlers import handle_keys
from game_map import GameMap
from fov_map import initialize_fov, recompute_fov
from game_states import GameStates

def main():
    screen_width = 80 #x
    screen_height = 50 #y

    # Entities
    player = Entity(0, 0, '@', libtcod.white, 'Player', blocks=True)
    entities = [player]
   
    # Map variables
    map_width = 80
    map_height = 45

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30
    max_monsters_per_room = 3

    colors = {
        'dark_wall': libtcod.Color(0, 0, 100),
        'dark_ground': libtcod.Color(50, 50, 150),
        'light_wall': libtcod.Color(130, 110, 50),
        'light_ground': libtcod.Color(200, 180, 50)
    }

    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room)

    # FOV
    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10
    fov_recompute = True #Render as the game starts, reset on movement
    fov_map = initialize_fov(game_map)

    #Console Setup
    libtcod.console_set_custom_font('./Desktop/Python/Game/arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    libtcod.console_init_root(screen_width, screen_height, "My title", False)
    con = libtcod.console_new(screen_width, screen_height)

    # Input Listeners
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    game_state = GameStates.PLAYERS_TURN

    #Main Loop
    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)
        render_all(con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors)
        fov_recompute = False
        
        libtcod.console_flush()
        clear_all(con, entities)

        # action handlers    
        action = handle_keys(key)
        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move #this is cool, you can do multiline variable mappings
            destination_x = player.x + dx
            destination_y = player.y + dy

            if not game_map.is_blocked(destination_x,  destination_y):
                target = get_blocking_entities_at_location(entities, destination_x, destination_y)

                if target:
                    print("You slam against the " + target.name + " with your fists!")
                else:
                    player.move(dx, dy)
                    fov_recompute = True
                game_state = GameStates.ENEMY_TURN

        if exit:
            return True
        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity != player:
                    print("The " + entity.name + " ponders the meaning of life.")

            game_state = GameStates.PLAYERS_TURN

if __name__ == '__main__':
    main()