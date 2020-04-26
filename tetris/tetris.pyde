
import random

rows = 20
cols = 10

screen_width = 200
screen_height = 400

BLOCK_COLORS = [[255, 51, 52],[12, 150, 228],[30, 183, 66], [246, 187, 0],[76, 0, 153], [255, 255, 255], [0, 0, 0]]

grey_color = (210, 210, 210)
          
class Game:
    
    def __init__(self):
        self.colors = [[grey_color  for _ in range(cols)] for _ in range(rows)]
        self.w = screen_width / cols
        self.color = [0, 0, 0]
        self.game_score = 0
        self.game_is_active = True
        self.speed = 0

    def display_grid(self):
        stroke(180)
        for j in range(1, cols):
            line(j*rows, 0, j*rows, screen_height)
        
        for j in range(1, rows):
            line(0, j*rows, screen_width, j*rows)
    
    def display_background(self):
        for i in range(cols):
            for j in range(rows):
                r, g, b = self.colors[j][i]
                fill(r, g, b)
                rect(i * self.w, j * self.w, self.w, self.w)
                
    def display_score(self):
        textSize(15)
        fill(50)
        text("Score : {}".format(self.game_score), 120, 20)
    
    def write_block(self, block):
        x, y = block.x, block.y
        self.colors[y][x] = block.color
        
    def check_for_combination(self, last_block):
        
        x, y = block.x, block.y # (x,y) coordinates of last block
        block_color = block.color
            
        # check if 4 blocks have the same color
        for i in range(1, 4):
            nx, ny = x, y+i
            
            # check if y is out of bounds
            if ny >= rows:
                return False
        
            if block_color != list(self.colors[ny][nx]):
                return False
        
        # if all is valid, we have a combination
        for i in range(0, 4): # todo : fix this
            self.colors[y+i][x] = grey_color
            
        return True
    
    def check_all_columns_are_filled(self):
        for i in range(1, rows):
            for j in range(cols):
                if self.colors[i][j] == grey_color: # if there is still a gray cell left
                    return False
        return True
            

class Block:
    
    def __init__(self):
    
        self.w = screen_width / cols
        self.shapes = [[0, 0]]
        
        self.current_block = None
        self.is_active = False
        
        self.color = random.choice(BLOCK_COLORS)
        self.x, self.y = random.randint(0, cols - 1), 0 # (x,y) coordinates of current block
        self.R, self.G, self.B = self.color
        
    def display(self):
        fill(self.R, self.G, self.B)
        rect(
             self.x * self.w, 
             self.y * self.w, 
             self.w, 
             self.w
        )
        
    def move(self, direction):
        if direction == "RIGHT":
            if self.x < 10 - 1: # check right boundary
               if game.colors[self.y][self.x+1] == grey_color: # check right box color
                   self.x += 1
                   
        if direction == "LEFT":
            if self.x > 0: # check left boundary
               if game.colors[self.y][self.x-1] == grey_color: # check left box color
                   self.x -= 1
        
            
    def move_down(self):
        if self.y < rows - 1:
            self.y += 1
            
        if self.y >= rows : # block has reached the floor
            self.is_active = False 
            
    def block_is_on_top_of_something(self, game):
        
        # if block has reached the floor
        if self.y >= (rows-1):
            return True
        
        # if block is on top of another block
        y = self.y + 1 
        x = self.x 
        
        if game.colors[y][x] != grey_color: 
            return True
        
        # block is not on top of another block
        return False

block, upcoming_block, game = None, None, None

def start_new_game():
    global block, upcoming_block, game
    
    block = Block()
    upcoming_block = Block()
    game = Game()
    
    block.is_active = True

def setup():
    
    size(screen_width, screen_height)
    # frameRate(200)
    
    start_new_game()
    
def draw():
    
    global block, upcoming_block, game
    
    if game.game_is_active:
        if frameCount%(max(1, int(8 - game.speed)))==0 or frameCount==1:
            background(210)
            game.display_grid()
            game.display_background()
            game.display_score()
            block_movement_manager()
    else:
        show_game_over()
    
def show_game_over():
    background(0)
    fill(255, 255, 255)
    textSize(24)
    text("Game Over", 35, 200)
    
def block_movement_manager():
    
    global block, upcoming_block
    
    block.display()

    if block.is_active:
        
        # check background, if the next lower cell color is equal to background color or not
        if block.block_is_on_top_of_something(game):

            # disable this block
            block.is_active = False
            
            # make an imprint
            game.write_block(block)
            
            # check if 3 blocks below this are of the same color
            if game.check_for_combination(block):
                game.speed = 0
                game.game_score += 1
                
            # spawn a new block
            game.speed = min(game.speed + 0.25, 4.0)
            block = upcoming_block
            block.is_active = True
            upcoming_block = Block()
            
            if game.check_all_columns_are_filled():
                # game over
                game.game_is_active = False
                # print("Game Over")
        
        else: # there is place for the block to move, so lets move it down
            block.move_down()
            
    
def keyPressed():
    if keyCode == RIGHT:
        block.move("RIGHT")
    elif keyCode == LEFT:
        block.move("LEFT")
        
def mousePressed():
    global game
    
    if game.game_is_active == False:
        start_new_game()
        

    
    
    
