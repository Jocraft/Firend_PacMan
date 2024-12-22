import pygame
import os
import sys
# pyinstaller --clean --onefile --noconsole --name "Belal PacMan" --icon="Belal.ico" --add-data "images;images" --add-data "Music;Music" --add-data "text;text" main.py
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller."""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# ---------------------------
# 1) Define a global SCALE
# ---------------------------
SCALE = 1.6

black    = (0,0,0)
white    = (255,255,255)
blue     = (0,0,255)
green    = (0,255,0)
red      = (255,0,0)
purple   = (255,0,255)
yellow   = (255,255,0)
player=pygame.image.load(resource_path('images/player.png'))
pygame.display.set_icon(player)

pygame.init()

# Double the original 606
screen = pygame.display.set_mode([606 * SCALE, 606 * SCALE])
pygame.display.set_caption('Belal Pacman')

clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.Font(resource_path("text/freesansbold.ttf"), 24)
#Add music
pygame.mixer.init()
pygame.mixer.music.load(resource_path('music/pacman.mp3'))
pygame.mixer.music.play(-1, 0.0)
# ---------------------------
# 2) Scale the wall data
# ---------------------------
def setupRoomOne(all_sprites_list):
    original_walls = [ [0,0,6,600],
                    [0,0,600,6],
                    [0,600,606,6],
                    [600,0,6,606],
                    [300,0,6,66],
                    [60,60,186,6],
                    [360,60,186,6],
                    [60,120,66,6],
                    [60,120,6,126],
                    [180,120,246,6],
                    [300,120,6,66],
                    [480,120,66,6],
                    [540,120,6,126],
                    [120,180,126,6],
                    [120,180,6,126],
                    [360,180,126,6],
                    [480,180,6,126],
                    [180,240,6,126],
                    [180,360,246,6],
                    [420,240,6,126],
                    [240,240,42,6],
                    [324,240,42,6],
                    [240,240,6,66],
                    [240,300,126,6],
                    [360,240,6,66],
                    [0,300,66,6],
                    [540,300,66,6],
                    [60,360,66,6],
                    [60,360,6,186],
                    [480,360,66,6],
                    [540,360,6,186],
                    [120,420,366,6],
                    [120,420,6,66],
                    [480,420,6,66],
                    [180,480,246,6],
                    [300,480,6,66],
                    [120,540,126,6],
                    [360,540,126,6]
                    ]
    scaled_walls = []
    for item in original_walls:
        scaled_walls.append([
            item[0]*SCALE,
            item[1]*SCALE,
            item[2]*SCALE,
            item[3]*SCALE
        ])
    wall_list = pygame.sprite.RenderPlain()
    for item in scaled_walls:
        wall = Wall(item[0], item[1], item[2], item[3], blue)
        wall_list.add(wall)
        all_sprites_list.add(wall)
    return wall_list

def setupGate(all_sprites_list):
    gate = pygame.sprite.RenderPlain()
    # scale this too
    gate.add(Wall(282*SCALE, 242*SCALE, 42*SCALE, 2*SCALE, white))
    all_sprites_list.add(gate)
    return gate


class Wall(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height,color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width,height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x

class Block(pygame.sprite.Sprite):
    def __init__(self, image_path, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_path).convert_alpha()  # Load the image
        self.image = pygame.transform.scale(self.image, (width, height))  # Scale the image
        self.rect = self.image.get_rect()

class Player(pygame.sprite.Sprite):
    change_x = 0
    change_y = 0

    def __init__(self, x, y, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect  = self.image.get_rect()
        self.rect.top  = y
        self.rect.left = x

    def changespeed(self, x, y):
        self.change_x += x
        self.change_y += y

    def update(self, walls, gate):
        # same collision logic; no change
        old_x = self.rect.left
        old_y = self.rect.top
        self.rect.left = old_x + self.change_x
        x_collide = pygame.sprite.spritecollide(self, walls, False)
        if x_collide:
            self.rect.left = old_x
        self.rect.top = old_y + self.change_y
        y_collide = pygame.sprite.spritecollide(self, walls, False)
        if y_collide:
            self.rect.top = old_y
        # Gate collision
        if gate:
            g_collide = pygame.sprite.spritecollide(self, gate, False)
            if g_collide:
                self.rect.left = old_x
                self.rect.top  = old_y

class Ghost(Player):
    def changespeed(self, moves, ghost, turn, steps, length):
        try:
            z = moves[turn][2]
            if steps < z:
                self.change_x = moves[turn][0]
                self.change_y = moves[turn][1]
                steps += 1
            else:
                if turn < length:
                    turn += 1
                elif ghost == "clyde":
                    turn = 2
                else:
                    turn = 0
                self.change_x = moves[turn][0]
                self.change_y = moves[turn][1]
                steps = 0
            return [turn, steps]
        except IndexError:
            return [0,0]

def scale_directions(dirs):
    scaled = []
    for (dx, dy, st) in dirs:
        scaled.append([dx*SCALE, dy*SCALE, st])
    return scaled

# Original directions each used 15, 30, etc. --> scale dx, dy
Pinky_directions  = scale_directions([
[0,-30,4],
[15,0,9],
[0,15,11],
[-15,0,23],
[0,15,7],
[15,0,3],
[0,-15,3],
[15,0,19],
[0,15,3],
[15,0,3],
[0,15,3],
[15,0,3],
[0,-15,15],
[-15,0,7],
[0,15,3],
[-15,0,19],
[0,-15,11],
[15,0,9]
])
Blinky_directions = scale_directions([
[0,-15,4],
[15,0,9],
[0,15,11],
[15,0,3],
[0,15,7],
[-15,0,11],
[0,15,3],
[15,0,15],
[0,-15,15],
[15,0,3],
[0,-15,11],
[-15,0,3],
[0,-15,11],
[-15,0,3],
[0,-15,3],
[-15,0,7],
[0,-15,3],
[15,0,15],
[0,15,15],
[-15,0,3],
[0,15,3],
[-15,0,3],
[0,-15,7],
[-15,0,3],
[0,15,7],
[-15,0,11],
[0,-15,7],
[15,0,5]
])
Inky_directions   = scale_directions([
    [30,0,2],
[0,-15,4],
[15,0,10],
[0,15,7],
[15,0,3],
[0,-15,3],
[15,0,3],
[0,-15,15],
[-15,0,15],
[0,15,3],
[15,0,15],
[0,15,11],
[-15,0,3],
[0,-15,7],
[-15,0,11],
[0,15,3],
[-15,0,11],
[0,15,7],
[-15,0,3],
[0,-15,3],
[-15,0,3],
[0,-15,15],
[15,0,15],
[0,15,3],
[-15,0,15],
[0,15,11],
[15,0,3],
[0,-15,11],
[15,0,11],
[0,15,3],
[15,0,1],
])
Clyde_directions  = scale_directions([
    [-30,0,2],
[0,-15,4],
[15,0,5],
[0,15,7],
[-15,0,11],
[0,-15,7],
[-15,0,3],
[0,15,7],
[-15,0,7],
[0,15,15],
[15,0,15],
[0,-15,3],
[-15,0,11],
[0,-15,7],
[15,0,3],
[0,-15,11],
[15,0,9],
])
pl = len(Pinky_directions)-1
bl = len(Blinky_directions)-1
il = len(Inky_directions)-1
cl = len(Clyde_directions)-1
# For clarity, define bigger tile-based movement
MOV_STEP = 30 * SCALE  # so that the arrow keys can move 60 px if scale=2

# Example of scaled spawn positions
w    = (303 - 16) * SCALE
p_h  = ((7 * 60) + 19) * SCALE
m_h  = ((4 * 60) + 19) * SCALE
b_h  = ((3 * 60) + 19) * SCALE
i_w  = (303 - 16 - 32) * SCALE
c_w  = (303 + (32 - 16)) * SCALE

def startGame():
    all_sprites_list = pygame.sprite.RenderPlain()
    block_list       = pygame.sprite.RenderPlain()
    monsta_list      = pygame.sprite.RenderPlain()
    pacman_collide   = pygame.sprite.RenderPlain()
    wall_list        = setupRoomOne(all_sprites_list)
    gate             = setupGate(all_sprites_list)

    Pacman = Player(w, p_h, resource_path("images/player.png"))
    all_sprites_list.add(Pacman)
    pacman_collide.add(Pacman)

    Blinky = Ghost(w, b_h,resource_path ("images/Blinky.png"))
    monsta_list.add(Blinky)
    all_sprites_list.add(Blinky)

    Pinky=Ghost( w, m_h, resource_path("images/Pinky.png") )
    monsta_list.add(Pinky)
    all_sprites_list.add(Pinky)
    
    Inky=Ghost( i_w, m_h,resource_path( "images/Inky.png") )
    monsta_list.add(Inky)
    all_sprites_list.add(Inky)
    
    Clyde=Ghost( c_w, m_h, resource_path("images/Clyde.png") )
    monsta_list.add(Clyde)
    all_sprites_list.add(Clyde)

    # Scale the block size from 4×4 to 8×8
    for row in range(19):
        for column in range(19):
            if (row in [7,8]) and (column in [8,9,10]):
                continue
            block = Block((resource_path("images/shawrma.png")), 14*SCALE, 14*SCALE)  # Use the path to your image file
            # x,y positions
            block.rect.x = (30*SCALE)*column + 6*SCALE + 26*SCALE
            block.rect.y = (30*SCALE)*row    + 6*SCALE + 26*SCALE
            # check collisions etc.
            b_collide = pygame.sprite.spritecollide(block, wall_list, False)
            p_collide = pygame.sprite.spritecollide(block, pacman_collide, False)
            if b_collide:
              continue
            elif p_collide:
              continue
            else:
              # Add the block to the list of objects
              block_list.add(block)
              all_sprites_list.add(block)

    score = 0
    bll   = len(block_list)
    done  = False

    # ghost direction indexes
    p_turn = 0
    p_steps = 0

    b_turn = 0
    b_steps = 0

    i_turn = 0
    i_steps = 0

    c_turn = 0
    c_steps = 0

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    Pacman.changespeed(-MOV_STEP, 0)
                elif event.key == pygame.K_RIGHT:
                    Pacman.changespeed(MOV_STEP, 0)
                elif event.key == pygame.K_UP:
                    Pacman.changespeed(0, -MOV_STEP)
                elif event.key == pygame.K_DOWN:
                    Pacman.changespeed(0, MOV_STEP)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    Pacman.changespeed(+MOV_STEP, 0)
                elif event.key == pygame.K_RIGHT:
                    Pacman.changespeed(-MOV_STEP, 0)
                elif event.key == pygame.K_UP:
                    Pacman.changespeed(0, +MOV_STEP)
                elif event.key == pygame.K_DOWN:
                    Pacman.changespeed(0, -MOV_STEP)

        # Updates
        Pacman.update(wall_list, gate)
        returned = Pinky.changespeed(Pinky_directions,False,p_turn,p_steps,pl)
        p_turn = returned[0]
        p_steps = returned[1]
        Pinky.changespeed(Pinky_directions,False,p_turn,p_steps,pl)
        Pinky.update(wall_list,False)

        returned = Blinky.changespeed(Blinky_directions,False,b_turn,b_steps,bl)
        b_turn = returned[0]
        b_steps = returned[1]
        Blinky.changespeed(Blinky_directions,False,b_turn,b_steps,bl)
        Blinky.update(wall_list,False)

        returned = Inky.changespeed(Inky_directions,False,i_turn,i_steps,il)
        i_turn = returned[0]
        i_steps = returned[1]
        Inky.changespeed(Inky_directions,False,i_turn,i_steps,il)
        Inky.update(wall_list,False)

        returned = Clyde.changespeed(Clyde_directions,"clyde",c_turn,c_steps,cl)
        c_turn = returned[0]
        c_steps = returned[1]
        Clyde.changespeed(Clyde_directions,"clyde",c_turn,c_steps,cl)
        Clyde.update(wall_list,False)

        
        # Check collisions
        blocks_hit_list = pygame.sprite.spritecollide(Pacman, block_list, True)
        score += len(blocks_hit_list)

        screen.fill(black)
        wall_list.draw(screen)
        gate.draw(screen)
        all_sprites_list.draw(screen)
        monsta_list.draw(screen)

        text = font.render("Score: "+str(score)+"/"+str(bll), True, red)
        screen.blit(text, [10, 10])
        if score == bll:
            doNext(True,"Congratulations, Belal is filled!",145,all_sprites_list,block_list,monsta_list,pacman_collide,wall_list,gate)

        monsta_hit_list = pygame.sprite.spritecollide(Pacman, monsta_list, False)

        if monsta_hit_list:
            doNext(False,["Game Over","Belal is still hungry"],235,all_sprites_list,block_list,monsta_list,pacman_collide,wall_list,gate)

        pygame.display.flip()
        clock.tick(10)
def doNext(didwin,message, left, all_sprites_list, block_list, monsta_list, pacman_collide, wall_list, gate):
    while True:
        # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_RETURN:
                    del all_sprites_list
                    del block_list
                    del monsta_list
                    del pacman_collide
                    del wall_list
                    del gate
                    startGame()

        # Grey background
        window_width, window_height = pygame.display.get_window_size()
        rect_width, rect_height = 400, 300
        rect_x = (window_width - rect_width) / 2  # Center horizontally
        rect_y = (window_height - rect_height) / 2  # Center vertically
        w = pygame.Surface((rect_width, rect_height))  # the size of your rect
        w.set_alpha(10)                # alpha level
        w.fill((128, 128, 128))        # this fills the entire surface
        screen.blit(w, (rect_x, rect_y))  # Center the rectangle
        if  (not didwin):
        # Center texts horizontally
            text1 = font.render(message[0], True, white)
            text1_rect = text1.get_rect(center=(window_width / 2, rect_y + 30))
            screen.blit(text1, text1_rect)

            text2 = font.render(message[1], True, white)
            text2_rect = text2.get_rect(center=(window_width / 2, rect_y + 70))
            screen.blit(text2, text2_rect)
        elif didwin:
            text1 = font.render(message, True, white)
            text1_rect = text1.get_rect(center=(window_width / 2, rect_y + 30))
            screen.blit(text1, text1_rect)

        text3 = font.render("if you want more order form", True, white)
        text3_rect = text3.get_rect(center=(window_width / 2, rect_y + 100))
        screen.blit(text3, text3_rect)

        text4 = font.render("Elevenshawerma 01211113174", True, white)
        text4_rect = text4.get_rect(center=(window_width / 2, rect_y + 130))
        screen.blit(text4, text4_rect)

        text5 = font.render("To play again, press ENTER.", True, white)
        text5_rect = text5.get_rect(center=(window_width / 2, rect_y + 230))
        screen.blit(text5, text5_rect)

        text6 = font.render("To quit, press ESCAPE.", True, white)
        text6_rect = text6.get_rect(center=(window_width / 2, rect_y + 260))
        screen.blit(text6, text6_rect)

        pygame.display.flip()
        clock.tick(10)

startGame()

pygame.quit()
sys.exit()


