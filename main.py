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
        self.image_original = pygame.transform.scale(pad_img, (120, 80))
        # set colour key for original image
        self.image_original.set_colorkey(BLACK)
        # set copy image for sprite rendering
        self.image = self.image_original.copy()
        # specify bounding rect for sprite
        self.rect = self.image.get_rect()
        self.rect.x = 120
        self.rect.y = 120
    
    #def update(self):
        #print("prob animation")

class Note(pygame.sprite.Sprite):
    def __init__(self, beat, xpos):
        pygame.sprite.Sprite.__init__(self)
        self.image_original = pygame.transform.scale(note_img, (120, 80))
        # set colour key for original image
        self.image_original.set_colorkey(BLACK)
        # set copy image for sprite rendering
        self.image = self.image_original.copy()
        # specify bounding rect for sprite
        self.rect = self.image.get_rect()
        #initial position
        self.startY =900
        self.rect.x = xpos
        self.rect.y = self.startY
        # what beat this slated to arrive 
        self.beat=beat

    def moveUp(self):
        #interpolate y
        self.rect.y= self.startY - (self.startY-conductor.finishLine)*(1-((self.beat-conductor.songPositionBeats)/conductor.beatsinAdvance))
            
    def update(self):
        # call movement update
        self.moveUp()
        #die at top
        if self.rect.top > winHeight + 15:
            self.kill()

#manages the song
class Conductor():
    def __init__(self):
        self.bmp = 70   #beats per min
        self.finishLine=120 #perfect end position of note
        self.hitOffset =50 #largest accepted offset for hit
        self.secPerBeat= 0 #duration of a beat in seconds
        self.songStartOffset = 0  #offset of song beginning
        self.songPosition = 0 #curr position of song in sec
        self.songPositionBeats = 0 #curr position of song in beats
        self.songTimeStart = 0 #time the song starts
        self.beatsinAdvance = 4 #how many shown beats before finish line
        pygame.mixer.music.load(os.path.join(snd_dir,"music.wav")) #load the song
        self.notesD = [4,5,6,6.5,8,10]   #struct to hold notes
        self.notesShownD =[]             #queue to keep track of notes shown
        self.indexD= 0  #traverses through note structure

        self.notesF= [4,4.5,6,7,8,9,10]
        self.notesShownF = []
        self.indexF =0 

        self.notesJ =[5,6,7,10.5]
        self.notesShownJ =[]
        self.indexJ =0

        self.notesK= [4,5,6,6.5,7.6,7.7,7.8,7.9]
        self.notesShownK = []
        self.indexK=0

    def start(self):
        self.secPerBeat = 60/self.bmp
        #hopefully clock keeps up  
        #record time song starts
        self.songTimeStart = pygame.time.get_ticks()/1000
        #start song
        pygame.mixer.music.play()

    def update(self):
        #position in sec
        self.songPosition= pygame.time.get_ticks()/1000-self.songTimeStart
        #current position in beats
        self.songPositionBeats= self.songPosition/self.secPerBeat
        
        #UPDATE D
        #check if there are notes left in the queue and check if the next note has reached the beat 
        if(self.indexD<len(self.notesD) and self.notesD[self.indexD]<self.songPositionBeats+self.beatsinAdvance):
            #make a note
            #giving it the beat in the notes list
            note = Note(self.notesD[self.indexD],120)
            #put it in queue to keep track of what is playable
            self.notesShownD.append(note)
            #adding to sprite group for updating and drawing
            note_sprites.add(note)
            #increment idx
            self.indexD= self.indexD+1
        if(len(self.notesShownD)>0):
            #grab current note
            currNote= self.notesShownD[0]

            #if the current note has passed finish line and offset, delete
            if currNote.rect.y<= self.finishLine - self.hitOffset:
                self.notesShownD.pop(0)
                print("miss")

        #UPDATE F
        #check if there are notes left in the queue and check if the next note has reached the beat 
        if(self.indexF<len(self.notesF) and self.notesF[self.indexF]<self.songPositionBeats+self.beatsinAdvance):
            #make a note
            #giving it the beat in the notes list
            note = Note(self.notesF[self.indexF],300)
            #put it in queue to keep track of what is playable
            self.notesShownF.append(note)
            #adding to sprite group for updating and drawing
            note_sprites.add(note)
            #increment idx
            self.indexF= self.indexF+1
        if(len(self.notesShownF)>0):
            #grab current note
            currNote= self.notesShownF[0]

            #if the current note has passed finish line and offset, delete
            if currNote.rect.y<= self.finishLine - self.hitOffset:
                self.notesShownF.pop(0)
                print("miss")
        
        #UPDATE J
        #check if there are notes left in the queue and check if the next note has reached the beat 
        if(self.indexJ<len(self.notesJ) and self.notesJ[self.indexJ]<self.songPositionBeats+self.beatsinAdvance):
            #make a note
            #giving it the beat in the notes list
            note = Note(self.notesJ[self.indexJ],480)
            #put it in queue to keep track of what is playable
            self.notesShownJ.append(note)
            #adding to sprite group for updating and drawing
            note_sprites.add(note)
            #increment idx
            self.indexJ= self.indexJ+1
        if(len(self.notesShownJ)>0):
            #grab current note
            currNote= self.notesShownJ[0]

            #if the current note has passed finish line and offset, delete
            if currNote.rect.y<= self.finishLine - self.hitOffset:
                self.notesShownJ.pop(0)
                print("miss")

        #UPDATE K
        #check if there are notes left in the queue and check if the next note has reached the beat 
        if(self.indexK<len(self.notesK) and self.notesK[self.indexK]<self.songPositionBeats+self.beatsinAdvance):
            #make a note
            #giving it the beat in the notes list
            note = Note(self.notesK[self.indexK],660)
            #put it in queue to keep track of what is playable
            self.notesShownK.append(note)
            #adding to sprite group for updating and drawing
            note_sprites.add(note)
            #increment idx
            self.indexK= self.indexK+1
        if(len(self.notesShownK)>0):
            #grab current note
            currNote= self.notesShownK[0]

            #if the current note has passed finish line and offset, delete
            if currNote.rect.y<= self.finishLine - self.hitOffset:
                self.notesShownK.pop(0)
                print("miss")

    
    #maybe a handle input method for each track
    def handleD(self):
        #if there are notes present,
        if len(self.notesShownD)>0:
            #find how far note is from desired line
            offset= abs(self.notesShownD[0].rect.y - self.finishLine)
            #check if it is close enough
            if(offset<=self.hitOffset):
                print("hit")
                #kill the sprite and remove it from the shown queue
                toKill=self.notesShownD.pop(0)
                toKill.kill()

    def handleF(self):
        #if there are notes present,
        if len(self.notesShownF)>0:
            #find how far note is from desired line
            offset= abs(self.notesShownF[0].rect.y - self.finishLine)
            #check if it is close enough
            if(offset<=self.hitOffset):
                print("hit")
                #kill the sprite and remove it from the shown queue
                toKill=self.notesShownF.pop(0)
                toKill.kill()

    def handleJ(self):
        #if there are notes present,
        if len(self.notesShownJ)>0:
            #find how far note is from desired line
            offset= abs(self.notesShownJ[0].rect.y - self.finishLine)
            #check if it is close enough
            if(offset<=self.hitOffset):
                print("hit")
                #kill the sprite and remove it from the shown queue
                toKill=self.notesShownJ.pop(0)
                toKill.kill()

    def handleK(self):
        #if there are notes present,
        if len(self.notesShownK)>0:
            #find how far note is from desired line
            offset= abs(self.notesShownK[0].rect.y - self.finishLine)
            #check if it is close enough
            if(offset<=self.hitOffset):
                print("hit")
                #kill the sprite and remove it from the shown queue
                toKill=self.notesShownK.pop(0)
                toKill.kill()

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
#loading music
pygame.mixer.music.load(os.path.join(snd_dir,"music.wav"))
pygame.mixer.music.set_volume(1)

# create sprite groups
game_sprites = pygame.sprite.Group()
note_sprites = pygame.sprite.Group()

#create ending pads to draw
x=120
for i in range(4):
    pad = Pad()
    pad.rect.x=x
    # add sprite to game's sprite group
    game_sprites.add(pad)
    x=x+180


# play background music
pygame.mixer.music.play(loops=-1)

#create conductor
conductor = Conductor()
conductorStarted = False

#variables for beat counter
timeSinceLastAction =0
beat=0

# Set the game loop
running = True

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
                conductor.handleD()
            if event.key == pygame.K_f:
                conductor.handleF()
            if event.key == pygame.K_j:
                conductor.handleJ()
            if event.key == pygame.K_k:
                conductor.handleK()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                leftDown = False
            if event.key == pygame.K_RIGHT:
                rightDown = False


    #update
    #also start conductor immediately
    if not conductorStarted:
        conductor.start()
        conductorStarted=True
    else:
        conductor.update()

    note_sprites.update()
    game_sprites.update()

    #draw
    #background
    window.blit(bg_img, bg_rect)

    #prints beats in time
    timeSinceLastAction= timeSinceLastAction + timesincelasttick
    if(timeSinceLastAction>(conductor.secPerBeat*1000)):
        beat=beat+1
        timeSinceLastAction=0
    textRender(window, str(beat), 100, 500,500)

        
    game_sprites.draw(window)
    note_sprites.draw(window)
    
    #updates all screen w/ no parameter
    pygame.display.update()

