from graphics import *
import random
import time

############################################################
# BLOCK CLASS
############################################################

class Block(Rectangle):
    ''' Block class:
        Attributes: x - type: int
                    y - type: int
    '''

    BLOCK_SIZE = 120
    OUTLINE_WIDTH = 3

    def __init__(self, pos, color):
        self.x = pos.x
        self.y = pos.y
        
        p1 = Point(pos.x*Block.BLOCK_SIZE + Block.OUTLINE_WIDTH,
                   pos.y*Block.BLOCK_SIZE + Block.OUTLINE_WIDTH)
        p2 = Point(p1.x + Block.BLOCK_SIZE, p1.y + Block.BLOCK_SIZE)

        Rectangle.__init__(self, p1, p2)
        self.setWidth(Block.OUTLINE_WIDTH)
        self.setFill(color)

    def is_block_there(self, board):
        ''' Parameters: x - type: int
                        y - type: int

            Return value: type: bool
                        
            checks if there is a block is at the coordinates x,y
            return true if there is
            return false if there is not
        '''
        if board.is_block_there(self.x,self.y):
            return True
        else:
            return False
    
    def move(self, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int
                        
            moves the block dx squares in the x direction
            and dy squares in the y direction
        '''

        self.x += dx
        self.y += dy

        Rectangle.move(self, dx*Block.BLOCK_SIZE, dy*Block.BLOCK_SIZE)

############################################################
# BOARD CLASS
############################################################
game_over_msg = ''

class Board():

    def __init__(self, win, width, height):
        self.width = width
        self.height = height

        # create a canvas to draw the tetris shapes on
        self.canvas = CanvasFrame(win, self.width * Block.BLOCK_SIZE,
                                        self.height * Block.BLOCK_SIZE)
        self.canvas.setBackground('light gray')
        
        # create an empty dictionary
        # currently we have no shapes on the board
        self.grid = {}

    def draw_block(self, block):
        ''' Parameters: block - type: Block
            Return value: type: bool
        '''

        ## add timer code here
        block.draw(self.canvas)
        self.add_block(block)
        return False

    def is_block_there(self, x, y):
        ''' Parameters: x - type:int
                        y - type:int
            Return value: type: bool

            Check if there is a block in position (x,y) if there is
            return True
            if not
            return False            
        '''
            
        if (x,y) in self.grid:
            return True
        else:
            return False


    def add_block(self, block):   
        self.grid[(block.x,block.y)] = block

    def delete_row(self, y):       
        for x in range(self.width):
            if (x,y) in self.grid:
                self.grid[(x,y)].undraw()
                del self.grid[(x,y)]
          
    
    def move_down_rows(self, y_start):
        for y in range(y_start,-1,-1):
            for x in range(0,self.width):
                if (x,y) in self.grid:
                    block = self.grid[(x,y)]
                    del self.grid[(x,y)]
                    block.move(0,1)
                    self.grid[(x,y+1)] = block
    
    def update_board(self):
        self.delete_row(self.height - 1)
        self.move_down_rows(self.height - 2)

    def game_over(self):
        self.game_over_msg = Text(Point(self.width * Block.BLOCK_SIZE/2,self.height * Block.BLOCK_SIZE/2),"FINISHED!!!")
        self.game_over_msg.draw(self.canvas)

    def undraw_game_over(self):
        self.game_over_msg.undraw()

        
    def begin_game(self,delay=1000):
        start_msg = Text(Point(self.width * Block.BLOCK_SIZE/2,self.height * Block.BLOCK_SIZE/2),"START!!")
        start_msg.draw(self.canvas)
        self.canvas.after(int(delay/2),start_msg.undraw)
        

    def count_down(self,seconds,delay=1000):
        if seconds > 0:
            countdown_msg = Text(Point(self.width * Block.BLOCK_SIZE/2,self.height * Block.BLOCK_SIZE/2),str(seconds))
            countdown_msg.draw(self.canvas)
            self.canvas.after(delay,countdown_msg.undraw)
        else:
            self.begin_game(delay)
        
############################################################
# Timer CLASS
############################################################

class Timer():

    SECONDS = 10
    
    def __init__(self, x, y):
        self.time = 0

        self.tenth = 0
        self.sec = 0

        self.elapsed_time = 0

        self.time_msg = Text(Point(x,y),str(self.sec)+':'+str(self.tenth))
        self.time_msg.setTextColor('white')

    def draw_time(self,canvas):
        self.time_msg.draw(canvas)

    def update_time(self,mistakes = 0):
        self.get_time(mistakes) 
        self.tenth = int((self.get_time(mistakes) *10) % 10)
        self.sec = int(self.get_time(mistakes))
        self.time_msg.setText(str(self.sec)+':'+str(self.tenth))

    def get_time(self,mistakes = 0):
        if self.time == 0:
            return 0
        else:
            return time.time() - self.time + .5 * mistakes

    def start_time(self):
        self.time = time.time()

    def reset_time(self):
        self.time = 0
        

############################################################
# SCOREBOARD CLASS
############################################################

class Scoreboard():
    def __init__(self, win, width, height):
        self.width = width
        self.height = height

        # create a canvas for the score
        self.canvas = CanvasFrame(win, self.width * Block.BLOCK_SIZE,
                                        self.height * Block.BLOCK_SIZE)
        self.canvas.setBackground('black')

        self.score_msg = Text(Point(Block.BLOCK_SIZE/2,int(self.height*Block.BLOCK_SIZE/3)),"Score: 0")
        self.score_msg.setTextColor('white')
        self.mistakes_msg = Text(Point(Block.BLOCK_SIZE/2,int(2*self.height*Block.BLOCK_SIZE/3)),"Mistakes: 0")
        self.mistakes_msg.setTextColor('white')

        self.timer = Timer((2*Block.BLOCK_SIZE),int(2*self.height*Block.BLOCK_SIZE/3))
        
    def draw_score_board(self):
        self.score_msg.draw(self.canvas)
        self.mistakes_msg.draw(self.canvas)
        self.timer.draw_time(self.canvas)
        
    def update_score_board(self,score,mistakes):
        self.score_msg.setText("Score:"+" " + str(score))
        self.mistakes_msg.setText("Mistakes:"+" " + str(mistakes))

    def update_time(self,mistakes):
        self.timer.update_time(mistakes)

    def start_time(self):
        self.timer.start_time()
        self.timer.update_time()

    def reset_time(self):
        self.timer.reset_time()
        self.timer.update_time()


############################################################
# BLOCKGAME CLASS
############################################################

class Blockgame():
   
    DIRECTION = {'Left':(0, 3), 'Right':(2, 3), 'Down':(1, 3)}
    
    BOARD_WIDTH = 3
    BOARD_HEIGHT = 4
    SCOREBOARD_WIDTH = 3
    SCOREBOARD_HEIGHT = 1

    active_game = False
    is_restarting = False
    
    setup_rows = 0
    score = 0
    mistakes = 0
    
    def __init__(self, win):
        self.scoreboard = Scoreboard(win, self.SCOREBOARD_WIDTH, self.SCOREBOARD_HEIGHT)
        self.board = Board(win, self.BOARD_WIDTH, self.BOARD_HEIGHT)
        
        self.win = win
        self.delay = 1000 #ms

        # sets up the keyboard events
        # when a key is called the method key_pressed will be called
        self.win.bind_all('<Key>', self.key_pressed)

        # set the current shape to a random new shape
        self.scoreboard.draw_score_board()
        self.end_game()
        self.restart()

        
    def time_up(self):
        if self.scoreboard.timer.get_time(self.mistakes) < 10.1:
            return False
        else:
            return True

        
    def animate_time(self):
        if self.scoreboard.timer.time == 0:
            self.scoreboard.start_time()
        if not self.time_up() and self.active_game:
            self.scoreboard.update_time(self.mistakes)
            self.win.after(10,self.animate_time)
        elif self.active_game:
            self.end_game()

    def create_new_block(self):
        return Block(Point(random.randint(0,self.BOARD_WIDTH-1),0),'white')
    
    def update_board(self):
        self.board.update_board()
        self.current_block = self.create_new_block()
        self.board.draw_block(self.current_block)
        
    def set_up_board(self):
        ''' Initializes the first 4 rows on the board'''
        if self.setup_rows < self.BOARD_HEIGHT and self.active_game:
            self.board.count_down(self.BOARD_HEIGHT - 1 - self.setup_rows,self.delay)
            self.setup_rows += 1
            self.update_board()
            self.win.after(self.delay,self.set_up_board)
    
    def end_game(self):
        self.active_game = False
        self.board.game_over()
        
        for rows in range(0,self.BOARD_HEIGHT):
            self.board.delete_row(rows)


    def change_restarting(self):
        if self.is_restarting:
            self.is_restarting = False
        else:
            self.is_restarting = True

    def restart(self):
        if not self.is_restarting:    
            self.is_restarting = True

            self.board.undraw_game_over()
            self.setup_rows = 0
            self.score = 0
            self.mistakes = 0
            self.scoreboard.reset_time()

            self.active_game = True

            self.set_up_board()

            self.win.after(3000,self.animate_time)
            self.win.after(3000,self.change_restarting)
 
        
    def do_move(self, direction):
        if direction in self.DIRECTION:
            if self.DIRECTION[direction] in self.board.grid:
                self.update_board()
                self.score += 1
                self.scoreboard.update_score_board(self.score,self.mistakes)
                return True
            else:
                self.mistakes += 1
                self.scoreboard.update_score_board(self.score,self.mistakes)
                self.scoreboard.update_time(self.mistakes)
                return False
        elif direction == 'space' and not self.is_restarting:
            self.end_game()

        
    def key_pressed(self, event):            
        key = event.keysym
        if (key in self.DIRECTION or key == 'space') and self.active_game and not self.time_up():
            self.do_move(key)
        elif key == 'space'and not self.active_game:
            self.restart()
            


################################################################
# Start the game
################################################################

win = Window("Block Game")
game = Blockgame(win)
win.mainloop()

