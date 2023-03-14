import pygame
import os
import sys
import random

# Set the screen dimensions
winWidth = 1600
winHeight = 900
FPS = 120

# Initialize Pygame
pygame.init()
pygame.mixer.init()
window = pygame.display.set_mode((winWidth, winHeight))
# Set the caption
pygame.display.set_caption("Rhythm Game")
clock = pygame.time.Clock()

#set common color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#set up asset directory
game_dir = os.path.dirname(__file__)
# relative path to assets dir
assets_dir = os.path.join(game_dir, "assets")
# relative path to image dir
graphics_dir = os.path.join(assets_dir, "graphics")
snd_dir = os.path.join(assets_dir, "music")

def gameExit():
    pygame.quit()
    sys.exit()


class Pad(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # load mob object image & scale to fit game window...use as pristine image for rotation
        self.image_original = pygame.transform.scale(pad_img, (120, 80))
        # set colour key for original image
        self.image_original.set_colorkey(BLACK)
        # set copy image for sprite rendering
        self.image = self.image_original.copy()
        # specify bounding rect for sprite
        self.rect = self.image.get_rect()
        # set radius for circle bounding
        self.radius = int(self.rect.width * 0.9 / 2)
        self.rect.x = 120
        self.rect.y = 120
    
    #def update(self):
        #print("prob animation")

class Note(pygame.sprite.Sprite,):
    def __init__(self, beat):
        pygame.sprite.Sprite.__init__(self)
        # load mob object image & scale to fit game window...use as pristine image for rotation
        self.image_original = pygame.transform.scale(note_img, (120, 80))
        # set colour key for original image
        self.image_original.set_colorkey(BLACK)
        # set copy image for sprite rendering
        self.image = self.image_original.copy()
        # specify bounding rect for sprite
        self.rect = self.image.get_rect()
        self.startY =900
        self.rect.x = 120
        self.rect.y = self.startY
        # what beat this note is on
        self.beat=beat
        # random speed along the y-axis
        self.speed_y = 10
        
        # check timer for last update to move
        self.move_update = pygame.time.get_ticks()

    def moveUp(self):
        #interpolate y
        self.rect.y= self.startY - (self.startY-conductor.finishLine)*(1-((self.beat-conductor.songPositionBeats)/conductor.beatsinAdvance))
            
    
    def update(self):
        # call rotate update
        self.moveUp()
        #die at top
        if self.rect.top > winHeight + 15:
            self.kill()

#manages the song
class Conductor():
    def __init__(self):
        self.bmp = 80   #beats per min
        self.index= 0  #traverses through note structure
        self.finishLine=120 #perfect end position of note
        self.hitOffset =50 #largest accepted offset for hit
        self.secPerBeat= 0 #duration of a beat in seconds
        self.offset = 0  #offset of song beginning
        self.songPosition = 0 #curr position of song in sec
        self.songPositionBeats = 0 #curr position of song in beats
        self.songTimeStart = 0 #time the song starts
        self.beatsinAdvance = 4 #how many beats before finish line
        pygame.mixer.music.load(os.path.join(snd_dir,"music.wav")) #load the song
        self.notes = [4,4.5,5,5.5,6,7,8,9]   #struct to hold notes
        self.notesShown =[]           #to keep track of notes shown

    def start(self):
        self.secPerBeat = 60/self.bmp
        #hopefully clock keeps up  
        self.songTimeStart = pygame.time.get_ticks()/1000
        print(self.songTimeStart)
        pygame.mixer.music.play()

    def update(self):
        #position in sec  in s
        self.songPosition= pygame.time.get_ticks()/1000-self.songTimeStart
        #current position in beats
        self.songPositionBeats= self.songPosition/self.secPerBeat
        #print(self.songPositionBeats)
        #print(self.songPosition)
        
        #check if there are notes left and check if the next note has reached its beat 
        #(accounting for multiple displayed)
        if(self.index<len(self.notes) and self.notes[self.index]<self.songPositionBeats+self.beatsinAdvance):
            #make a note
            #giving it the beat in the notes list
            note = Note(self.notes[self.index])
            self.notesShown.append(note)
            note_sprites.add(note)
            #increment idx
            self.index= self.index+1
        if(len(self.notesShown)>0):
            #grab current note
            currNote= self.notesShown[0]
            #update all the notes  might have to do loop for this one maybe
            #note_sprites.update()
            if currNote.rect.y<= self.finishLine - self.hitOffset:
                self.notesShown.pop(0)
                print("miss")

        #this is so that the list Notesshown can determine which sprites are being drawn
        #for obj in self.notesShown:
        #        note_sprites.add(obj)
    
    #maybe a handle input method for each track
    def handleInput(self, key):
        #if there are notes present,
        if len(self.notesShown)>0:
            #find how far note is from desired line
            offset= abs(self.notesShown[0].rect.y - self.finishLine)
            print(self.notesShown)
            #check if it is close enough
            if(offset<=self.hitOffset):
                print("hit")
                #kill the sprite and remove it from the shown queue
                toKill=self.notesShown.pop(0)
                toKill.kill()
                print(self.notesShown)

font_match = pygame.font.match_font('arial')
# text output and render function - draw to game window
def textRender(surface, text, size, x, y):
    # specify font for text render - uses found font and size of text
    font = pygame.font.Font(font_match, size)
    # surface for text pixels - TRUE = anti-aliased
    text_surface = font.render(text, True, WHITE)
    # get rect for text surface rendering
    text_rect = text_surface.get_rect()
    # specify a relative location for text
    text_rect.midtop = (x, y)
    # add text surface to location of text rect
    surface.blit(text_surface, text_rect)

#SETTING BG
# load graphics/images for the game
bg_img = pygame.image.load(os.path.join(graphics_dir, "forest.jpg")).convert()
# add rect for bg - helps locate background
bg_rect = bg_img.get_rect()
note_img= pygame.image.load(os.path.join(graphics_dir, "note.png")).convert()
pad_img= pygame.image.load(os.path.join(graphics_dir, "square.png")).convert()
pygame.mixer.music.load(os.path.join(snd_dir,"music.wav"))
pygame.mixer.music.set_volume(1)


# game sprite group
game_sprites = pygame.sprite.Group()
note_sprites = pygame.sprite.Group()
# create player object
x=120
for i in range(4):
    pad = Pad()
    #note =Note()
    pad.rect.x=x
    #note.rect.x=x
    # add sprite to game's sprite group
    game_sprites.add(pad)
    #game_sprites.add(note)

    x=x+180


# play background music
pygame.mixer.music.play(loops=-1)
conductor = Conductor()
# Set the game loop
running = True
conductorStarted = False
timeSinceLastAction =0
beat=0
while running:
    timesincelasttick=clock.tick(FPS)
    # Get the current time
    current_time = pygame.time.get_ticks()
    #event variables
    leftDown=False
    rightDown=False
    # Handle events
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit()
        # check keyboard events - keydown
        if event.type == pygame.KEYDOWN:
            if event.key== pygame.K_ESCAPE:
                gameExit()
            if event.key == pygame.K_LEFT:
                leftDown = True
            if event.key == pygame.K_RIGHT:
                rightDown = True
            if event.key == pygame.K_d:
                conductor.handleInput("d")
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                leftDown = False
            if event.key == pygame.K_RIGHT:
                rightDown = False

    if not conductorStarted:
        conductor.start()
        conductorStarted=True
    else:
        conductor.update()

    
    #update
    note_sprites.update()
    game_sprites.update()

    #draw
    #background
    window.blit(bg_img, bg_rect)

    timeSinceLastAction= timeSinceLastAction + timesincelasttick
    if(timeSinceLastAction>(conductor.secPerBeat*1000)):
        beat=beat+1
        timeSinceLastAction=0
    textRender(window, str(beat), 100, 500,500)

        


    game_sprites.draw(window)
    note_sprites.draw(window)
    #updates all screen w/ no parameter
    pygame.display.update()

