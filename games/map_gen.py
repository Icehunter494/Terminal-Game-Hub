import random

class MapGenerator:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.grid = [['#' for _ in range(width)] for _ in range(height)]

    def generate(self, max_rooms=6):
        rooms = []
        for _ in range(max_rooms):
            w, h = random.randint(4, 8), random.randint(4, 8)
            x, y = random.randint(1, self.width-w-1), random.randint(1, self.height-h-1)
            for i in range(y, y + h):
                for j in range(x, x + w):
                    if 0 < i < self.height-1 and 0 < j < self.width-1:
                        self.grid[i][j] = '.'
            rooms.append((x + w//2, y + h//2))
        
        for i in range(len(rooms) - 1):
            x1, y1 = rooms[i]
            x2, y2 = rooms[i+1]
            for x in range(min(x1, x2), max(x1, x2) + 1): self.grid[y1][x] = '.'
            for y in range(min(y1, y2), max(y1, y2) + 1): self.grid[y][x2] = '.'
        return self.grid, rooms
