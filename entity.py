class Entity:
    """
    A generic object that can be used to represent players, NPCs, or other objects
    """
    def __init__(self, x, y, char, color):
        #Construct with values here
        self.x = x
        self.y = y
        self.char = char
        self.color = color
    
    def move(self, dx, dy):
        # Move the entity by an x or y amount
        self.x += dx
        self.y += dy
