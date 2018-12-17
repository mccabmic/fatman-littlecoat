import tcod as libtcod
from entity import Entity
from map_objects import Tile
from map_objects import Rect
from random import randint

class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initalizeTiles() # 2d array for the tiles

    def initalizeTiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]
        return tiles
    
    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities,
                max_monsters_per_room):
        rooms = []
        num_rooms = 0

        for i in range(max_rooms):
            #random width and height
            room_width = randint(room_min_size, room_max_size)
            room_height = randint(room_min_size, room_max_size)
            #random position within boundries
            room_x = randint(0, map_width - room_width - 1)
            room_y = randint(0, map_height - room_height - 1)

            # Make the room
            new_room = Rect(room_x, room_y, room_width, room_height)

            # run through and see if rooms intersect
            for otherRoom in rooms:
                if new_room.intersect(otherRoom):
                    break
            else:
                #no rooms intersect

                #create new room to the map's tiles
                self.create_room(new_room)

                #use the center coordinates to determine collisions
                (new_x, new_y) = new_room.center()

                if num_rooms == 0:
                    #place player in first room
                    player.x = new_x
                    player.y = new_y
                else:
                    #all rooms after the first
                    # must be connected with a tunnel

                    # center previous rooms coordinates
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()
                    if (randint(0, 1) == 1):
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)

                self.place_entities(new_room, entities, max_monsters_per_room)
                rooms.append(new_room)
                num_rooms += 1

    def create_room(self, room):
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False
    
    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
         for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def place_entities(self, room, entities, max_monsters_per_room):
        num_monsters = randint(0, max_monsters_per_room)

        for i in range (num_monsters):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                if randint(0, 100) < 80:
                    monster = Entity(x, y, 'o', libtcod.desaturated_green, 'Orc', blocks=True)
                else:
                    monster = Entity(x, y, 'T', libtcod.darker_green, 'Troll', blocks=True)

                entities.append(monster)

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True
        
        return False
