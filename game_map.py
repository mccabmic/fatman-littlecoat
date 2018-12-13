from map_objects import Tile

class GameMap:
    """
    A map made from tiles used to represent the world.
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initalizeTiles() # 2d array for the tiles

    def initalizeTiles(self):
        tiles = [[Tile(False) for y in range(self.height)] for x in range(self.width)]
        
        # test wall
        tiles[30][22].blocked = True
        tiles[30][22].block_sight = True
        tiles[31][22].blocked = True
        tiles[31][22].block_sight = True
        tiles[32][22].blocked = True
        tiles[32][22].block_sight = True

        return tiles

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True
        
        return False
