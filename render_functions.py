import tcod as libtcod

# Go through all entities and call putEntity
def render_all(con, entities, game_map, screen_width, screen_height, colors):

    # Draw the map
    for y in range(game_map.height):
        for x in range(game_map.width):
            wall = game_map.tiles[x][y].block_sight
            
            if wall:
                libtcod.console_set_char_background(con, x, y, colors.get('dark_wall'), libtcod.BKGND_SET)
            else:
                libtcod.console_set_char_background(con, x, y, colors.get('dark_ground'), libtcod.BKGND_SET)
    
    # Draw the entities
    for entity in entities:
        draw_entity(con, entity)
    
    #Remember, you're drawing these but you need to blit the screen
    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

# Go through all the entities and call clearEntity
def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)

# Put a single entity onto the screen
def draw_entity(con, entity):
    libtcod.console_set_default_foreground(con, entity.color)
    libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)

# Clear a single entity from the screen
def clear_entity(con, entity):
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)