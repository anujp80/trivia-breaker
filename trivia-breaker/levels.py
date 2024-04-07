import random
from game_objects import Brick

class Level:
    def __init__(self, level_number, screen_width):
        self.level_number = level_number
        self.bricks = []
        self.screen_width = screen_width
        self.brick_width = 75
        self.brick_height = 20
        self.spacing = 5  # Space between bricks
        self.setup_bricks()

    def setup_bricks(self):
        rows = self.level_number
        cols = self.screen_width // (self.brick_width + self.spacing)
        
        # Determine the position for the trivia brick
        trivia_brick_row = rows - 1  # Last row
        trivia_brick_col = cols // 2  # Middle column

        for row in range(rows):
            for col in range(cols):
                x = col * (self.brick_width + self.spacing)
                y = row * (self.brick_height + self.spacing) + 50  # Offset from top

                # Places the trivia brick in the bottom middle
                if row == trivia_brick_row and col == trivia_brick_col:
                    self.bricks.append(Brick(x, y, color='orange', hits=1, is_trivia=True))
                else:
                    self.bricks.append(Brick(x, y, color='blue', hits=1))

    def draw(self, screen):
        for brick in self.bricks:
            brick.draw(screen)
