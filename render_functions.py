import tcod as libtcod

# Go through all entities and call putEntity
def render_all(con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors):
    if fov_recompute:
        # Draw the map
        for y in range(game_map.height):
            for x in range(game_map.width):
                # use libcod fov_map to determine visibility
                visible = libtcod.map_is_in_fov(fov_map, x, y)

                # a wall is something that will block_sight
                wall = game_map.tiles[x][y].block_sight

                #if the player can see the wall render it light it up and mark it as explored
                if visible:
                    if wall:
                        libtcod.console_set_char_background(con, x, y, colors.get('light_wall'), libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(con, x, y, colors.get('light_ground'), libtcod.BKGND_SET)
                    game_map.tiles[x][y].explored = True
                # otherwise don't draw it unless the player already saw it
                
                elif game_map.tiles[x][y].explored:
                    if wall:
                        libtcod.console_set_char_background(con, x, y, colors.get('dark_wall'), libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(con, x, y, colors.get('dark_ground'), libtcod.BKGND_SET)
        
    # Draw the entities
    for entity in entities:
        draw_entity(con, entity, fov_map)
    
    #Remember, you're drawing these but you need to blit the screen
    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

# Go through all the entities and call clearEntity
def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)

# Put a single entity onto the screen
def draw_entity(con, entity, fov_map):
    if libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
        libtcod.console_set_default_foreground(con, entity.color)
        libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)

# Clear a single entity from the screen
def clear_entity(con, entity):
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)