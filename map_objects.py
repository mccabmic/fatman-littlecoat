class Tile:
    """
        A tile on the map.  It may or may not be blocked, and may or may not block sight.
    """
    def __init__(self, blocked, block_sight= None):
        self.blocked = blocked

        if block_sight is None:
            block_sight = blocked
        
        self.block_sight = block_sight
        self.explored = False

class Rect:
    """
        A rectangle object that can be placed on the map
    """
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h
    
    def center(self):
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return (center_x, center_y)

    def intersect(self, otherRect):
        return (self.x1 <= otherRect.x2 and self.x2 >= otherRect.x1 and
                self.y1 <= otherRect.y2 and self.y2 >= otherRect.y1)