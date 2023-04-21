import cx_Freeze
import pygame
import os
import sys
import random

# Set the screen dimensions
winWidth = 1600
winHeight = 900
FPS = 60

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
knight_dir =os.path.join(graphics_dir, "knight")
monster_dir =os.path.join(graphics_dir, "monster")
cloud_dir = os.path.join(graphics_dir, "cloud")
ghost_dir = os.path.join(graphics_dir, "ghost")
snd_dir = os.path.join(assets_dir, "music")
font_dir = os.path.join(assets_dir, "fonts")

def gameExit():
    pygame.quit()
    sys.exit()

class Pad(pygame.sprite.Sprite):
    def __init__(self,skin):
        pygame.sprite.Sprite.__init__(self)
        self.image_original = pygame.transform.scale(skin, (120, 40))
        # set colour key for original image
        self.image_original.set_colorkey(BLACK)
        # set copy image for sprite rendering
        self.image = self.image_original.copy()
        # specify bounding rect for sprite
        self.rect = self.image.get_rect()
        self.rect.x = 110
        self.rect.y = 120
        self.changetime =0
    def flashSkin(self):
        self.image = pygame.transform.scale(padflash_img, (120, 40))
        self.changetime = pygame.time.get_ticks()
    def update(self):
        currtime= pygame.time.get_ticks()
        if currtime-self.changetime > 250:
            self.image = self.image_original
   
class padBorder(pygame.sprite.Sprite):
    def __init__(self,x,y,img):
        pygame.sprite.Sprite.__init__(self)
        self.image_original = pygame.transform.scale(img, (140, 60))
        # set colour key for original image
        self.image_original.set_colorkey(BLACK)
        # set copy image for sprite rendering
        self.image = self.image_original.copy()
        # specify bounding rect for sprite
        self.rect = self.image.get_rect()
        self.rect.x = x-10
        self.rect.y = y-10
        self.alpha = 255
        self.alpha_change = 5
    def update(self):
        #fade out
        self.alpha -= self.alpha_change
        self.image.set_alpha(self.alpha)
        if(self.alpha<=0):
            self.kill()

class movingtext(pygame.sprite.Sprite):
    def __init__(self,x,img):
        pygame.sprite.Sprite.__init__(self)
        self.image_original = pygame.transform.scale(img, (120, 40))
        # set colour key for original image
        self.image_original.set_colorkey(BLACK)
        # set copy image for sprite rendering
        self.image = self.image_original.copy()
        # specify bounding rect for sprite
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 95
        self.velocity= .5
        self.alpha = 255
        self.alpha_change = 5
        self.fade = False
    def update(self):
        self.rect.y-=self.velocity
        self.alpha -= self.alpha_change
        #this would be for fading in and out
        #if not 0 <= self.alpha <= 255:
        #    self.alpha_change *= -1
        self.image.set_alpha(self.alpha)
        if(self.alpha<=0):
            self.kill()

class Note(pygame.sprite.Sprite):
    def __init__(self, beat, xpos, img):
        pygame.sprite.Sprite.__init__(self)
        self.image_original = pygame.transform.scale(img, (120, 40))
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
        self.bmp = 160   #beats per min
        self.finishLine=120 #perfect end position of note
        self.hitOffset =50 #largest accepted offset for hit
        self.secPerBeat= 0 #duration of a beat in seconds
        self.songStartOffset = 0  #offset of song beginning
        self.songPosition = 0 #curr position of song in sec
        self.songPositionBeats = 0 #curr position of song in beats
        self.songTimeStart = 0 #time the song starts
        self.beatsinAdvance = 4 #how many shown beats before finish line
        pygame.mixer.music.load(os.path.join(snd_dir,"pyry.wav")) #load the song
        self.noteSkins= [noteblue_img, noteoran_img, notepurp_img, noteyell_img]
        self.padSkins = [padblue_img, padoran_img, padpurp_img, padyell_img]

        #interlude starts at 105

        self.notesD = [5,9,10.5,12,12.5,13,14.5,17,18.5,20,20.5,21,22.5,25,26.5,28,28.5,29,30.5,33,
            34.5,36,36.5,37,38.5,41,41.5,43.5,45,45.5,47.5,49,49.5,51.5,53,53.5,55.5,72,73,75.5,77.5,79,
            83.5,87,89,91.5,93.5,95,97,98.5,100.5,102.5,104,105,112,113,120,121,128,129,130,131,132,133,134,135,136,137,
            137.5,138.5,139,139.5,140.5,141,141.5,142.5,143,143.5,153,153.5,155,157,157.5,159,169,173,174,185,189,190,
            199,199.5,200,201,201.5,203.5,209,213,214,217,217.5,219.5,221,221.5,223.5,225,225.5,227.5,229.5,232.75
            ]   #struct to hold notes
        self.notesShownD =[] #queue to keep track of notes shown
        self.indexD= 0  #traverses through note structure

        self.notesF= [6,57,57.5,59.5,61,61.5,63.5,65,65.5,67.5,69,69.5,72.25,73.5,79,81.5,87,89.5,95,
            97.5,104.25,106,111,114,119,122,127,137,138,140,142,144,154,154.5,155.5,156,158,158.5,159.5,160,177,181,182
            ,193,197,198,199,199.5,200,205,205.5,207.5,232.75]
        self.notesShownF = []
        self.indexF =0 

        self.notesJ =[7,24,40,42,42.5,46,50,50.5,54,56,58,58.5,62,66,66.5,70,72.5,74,76,78,79,82,84,86,87
            ,90,92,94,95,98,100,102,104.5,107,110,115,118,123,126,137,145,145.5,146.5,147,147.5,148.5,149,149.5,150.5
            ,151,151.5,152.5,161,161.5,163,165,165.5,167,178,179.5,183,183.5,184,194,195.5,199,199.5,200
            ,202,202.5,204,210,211.5,232.5,233]
        self.notesShownJ =[]
        self.indexJ =0

        self.notesK= [8,16,32,44,48,52,56,60,64,68,72.75,79,87,95,104.75,108,109,116,117,124,125,137,146,
            148,150,152,152.75,162,162.5,163.5,164,166,166.5,167.5,168,170,171.5,175,175.5,176,186,187.5,191,191.5,192
            ,199,199.5,200,206,208,215,215.5,216,218,218.5,220,222,224,226,228,230,232,232.5,233]
        self.notesShownK = []
        self.indexK=0

        self.padArray=[]

    def start(self):
        #create ending pads to draw
        #array of skins to iterate through
        
        x=130
        for i in range(4):
            pad = Pad(self.padSkins[i])
            pad.rect.x=x
            # add sprite to game's sprite group
            game_sprites.add(pad)
            self.padArray.append(pad)
            x=x+155
        self.secPerBeat = 60/self.bmp
        #hopefully clock keeps up  
        #record time song starts
        self.songTimeStart = pygame.time.get_ticks()/1650
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
            note = Note(self.notesD[self.indexD],self.padArray[0].rect.x, self.noteSkins[0])
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
                self.missHandler("D")

        #UPDATE F
        #check if there are notes left in the queue and check if the next note has reached the beat 
        if(self.indexF<len(self.notesF) and self.notesF[self.indexF]<self.songPositionBeats+self.beatsinAdvance):
            #make a note
            #giving it the beat in the notes list
            note = Note(self.notesF[self.indexF],self.padArray[1].rect.x,self.noteSkins[1])
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
                self.missHandler("F")
        
        #UPDATE J
        #check if there are notes left in the queue and check if the next note has reached the beat 
        if(self.indexJ<len(self.notesJ) and self.notesJ[self.indexJ]<self.songPositionBeats+self.beatsinAdvance):
            #make a note
            #giving it the beat in the notes list
            note = Note(self.notesJ[self.indexJ],self.padArray[2].rect.x,self.noteSkins[2])
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
                self.missHandler("J")

        #UPDATE K
        #check if there are notes left in the queue and check if the next note has reached the beat 
        if(self.indexK<len(self.notesK) and self.notesK[self.indexK]<self.songPositionBeats+self.beatsinAdvance):
            #make a note
            #giving it the beat in the notes list
            note = Note(self.notesK[self.indexK],self.padArray[3].rect.x,self.noteSkins[3])
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
                self.missHandler("K")

    
    #maybe a handle input method for each track
    def handleD(self, monster):
        #if there are notes present,
        if len(self.notesShownD)>0:
            #find how far note is from desired line
            offset= abs(self.notesShownD[0].rect.y - self.finishLine)
            #check if it is close enough
            if(offset<=self.hitOffset):
                self.hitHandler("D")
                #kill the sprite and remove it from the shown queue
                toKill=self.notesShownD.pop(0)
                toKill.kill()


    def handleF(self, monster):
        #if there are notes present,
        if len(self.notesShownF)>0:
            #find how far note is from desired line
            offset= abs(self.notesShownF[0].rect.y - self.finishLine)
            #check if it is close enough
            if(offset<=self.hitOffset):
                self.hitHandler("F")
                #kill the sprite and remove it from the shown queue
                toKill=self.notesShownF.pop(0)
                toKill.kill()

    def handleJ(self, monster):
        #if there are notes present,
        if len(self.notesShownJ)>0:
            #find how far note is from desired line
            offset= abs(self.notesShownJ[0].rect.y - self.finishLine)
            #check if it is close enough
            if(offset<=self.hitOffset):
                self.hitHandler("J")
                #kill the sprite and remove it from the shown queue
                toKill=self.notesShownJ.pop(0)
                toKill.kill()

    def handleK(self, monster):
        #if there are notes present,
        if len(self.notesShownK)>0:
            #find how far note is from desired line
            offset= abs(self.notesShownK[0].rect.y - self.finishLine)
            #check if it is close enough
            if(offset<=self.hitOffset):
                self.hitHandler("K")
                #kill the sprite and remove it from the shown queue
                toKill=self.notesShownK.pop(0)
                toKill.kill()

    #miss and hit handlers manage the animations missing and hitting notes
    def missHandler(self, note):
        if note=="D":
            #the positions of flashing borders and text depend on the array that holds the pads
            #access the positions of the pads using the array
            miss=movingtext(self.padArray[0].rect.x,miss_img)
            game_sprites.add(miss)
            missborder= padBorder(self.padArray[0].rect.x,self.padArray[0].rect.y,padmiss_img)
            game_sprites.add(missborder)
        if note=="F":
            miss=movingtext(self.padArray[1].rect.x,miss_img)
            game_sprites.add(miss)
            missborder= padBorder(self.padArray[1].rect.x,self.padArray[1].rect.y,padmiss_img)
            game_sprites.add(missborder)
        if note=="J":
            miss=movingtext(self.padArray[2].rect.x,miss_img)
            game_sprites.add(miss)
            missborder= padBorder(self.padArray[2].rect.x,self.padArray[2].rect.y,padmiss_img)
            game_sprites.add(missborder)
        if note=="K":
            miss=movingtext(self.padArray[3].rect.x,miss_img)
            game_sprites.add(miss)
            missborder= padBorder(self.padArray[3].rect.x,self.padArray[3].rect.y,padmiss_img)
            game_sprites.add(missborder)
    
    def hitHandler(self, note):
        cloud=Cloud()
        cloudsprites.add(cloud)

        monster.decrease_health(5)
        if note=="D":
            hit=movingtext(self.padArray[0].rect.x,hit_img)
            game_sprites.add(hit)
            hitborder= padBorder(self.padArray[0].rect.x,self.padArray[0].rect.y,padhit_img)
            game_sprites.add(hitborder)
            self.padArray[0].flashSkin()
            window.blit( cloud_img, (500, 500),)
        if note=="F":
            hit=movingtext(self.padArray[1].rect.x,hit_img)
            game_sprites.add(hit)
            hitborder= padBorder(self.padArray[1].rect.x,self.padArray[1].rect.y,padhit_img)
            game_sprites.add(hitborder)
            self.padArray[1].flashSkin()
            window.blit( cloud_img2, (500, 50),)
        if note=="J":
            hit=movingtext(self.padArray[2].rect.x,hit_img)
            game_sprites.add(hit)
            hitborder= padBorder(self.padArray[2].rect.x,self.padArray[2].rect.y,padhit_img)
            game_sprites.add(hitborder)
            self.padArray[2].flashSkin()
            window.blit( cloud_img3, (550,60),)

        if note=="K":
            hit=movingtext(self.padArray[3].rect.x,hit_img)
            game_sprites.add(hit)
            hitborder= padBorder(self.padArray[3].rect.x,self.padArray[3].rect.y,padhit_img)
            game_sprites.add(hitborder)
            self.padArray[3].flashSkin()
            window.blit( cloud_img4, (700, 700),)

class Knight(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images= knightSkins
        self.rect= self.images[0].get_rect()
        self.rect.x = 800
        self.rect.y = 220
        self.index=0
        self.image=self.images[self.index]
        self.animation_time = 50
        self.current_time = 0
        self.notReverse=True
    def update(self):
        self.index+=1
        if(self.index>=len(self.images)): 
            self.index=0 
        self.image = self.images[self.index]

class Monster(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images= monsterSkins
        self.rect= self.images[0].get_rect()
        self.rect.x = 1100
        self.rect.y = 0
        self.index=0
        self.image=self.images[self.index]
        self.animation_time = 50
        self.current_time = 0
        self.notReverse=True
        self.max_health = 1000
        self.current_health = self.max_health
        self.dead = False

    def update(self):
        self.index+=1
        if(not self.dead):
            if(self.index>=len(self.images)-6): 
                self.index=0 
            self.image = self.images[self.index]
        if(self.dead):
            if(self.index>=len(self.images)):
                self.index=len(self.images)-6
            self.image = self.images[self.index]
            self.image.set_colorkey(WHITE)
            print(self.index)

        
    def draw_health_bar(self, surface):
        health_bar_width = 200
        health_bar_height = 40
        health_ratio = self.current_health / self.max_health
        health_bar_fill = health_bar_width * health_ratio

        # Position the health bar above the monster sprite
        health_bar_x = self.rect.x + 10 + (self.rect.width - health_bar_width) / 2
        health_bar_y = self.rect.y + 45

        outline_rect = pygame.Rect(health_bar_x-5, health_bar_y-5, health_bar_width+10, health_bar_height+10)
        fill_rect = pygame.Rect(health_bar_x, health_bar_y, health_bar_fill, health_bar_height)

        pygame.draw.rect(surface, BLACK, outline_rect, 5)
        pygame.draw.rect(surface, (255, 0, 0), fill_rect)

    def decrease_health(self, amount):
        self.current_health -= amount
        if self.current_health < 0:
            self.current_health = 0
        if self.current_health == 0:
            ghost=Ghost()
            ghostgroup.add(ghost)
            self.dead=True
            self.index= len(self.images)-6


class Cloud(pygame.sprite.Sprite):
    def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.images = [cloud_img,cloud_img2,cloud_img3,cloud_img4]
            image= self.images[random.randrange(0,3)]
            sizepx= random.randrange(200,450)
            xcoord= random.randrange(1000,1250)
            ycoord= random.randrange(100,250)
            self.image_original = pygame.transform.scale(image, (sizepx, sizepx))
            # set colour key for original image
            self.image_original.set_colorkey(WHITE)
            # set copy image for sprite rendering
            self.image = self.image_original.copy()
            # specify bounding rect for sprite
            self.rect = self.image.get_rect()
            self.rect.x = xcoord
            self.rect.y = ycoord
            self.alpha = 220
            self.alpha_change = 5
    def update(self):
            self.alpha -= self.alpha_change
            #this would be for fading in and out
            #if not 0 <= self.alpha <= 255:
            #    self.alpha_change *= -1
            self.image.set_alpha(self.alpha)
            if(self.alpha<=0):
                self.kill()

class Ghost(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_original = pygame.transform.scale(ghostSkins[0], (200, 200))
        # set colour key for original image
        self.image_original.set_colorkey(WHITE)
        # set copy image for sprite rendering
        self.image = self.image_original.copy()
        # specify bounding rect for sprite
        self.rect = self.image.get_rect()
        self.rect.x = 1230
        self.rect.y = 100
        self.velocity= .2
        self.alpha = 255
        self.alpha_change = 1
        self.fade = False
    def update(self):
        self.rect.y-=self.velocity
        self.alpha -= self.alpha_change
        self.image.set_alpha(self.alpha)
        if(self.alpha<=0):
            self.kill()
    

font_match = pygame.font.match_font('arial')
# text output and render function- draw to game window
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
bg_img = pygame.image.load(os.path.join(graphics_dir, "forestdivide.png")).convert()
# add rect for bg - helps locate background
bg_rect = bg_img.get_rect()
note_img= pygame.image.load(os.path.join(graphics_dir, "note.png")).convert()
pad_img= pygame.image.load(os.path.join(graphics_dir, "pad.png")).convert()
padflash_img= pygame.image.load(os.path.join(graphics_dir, "padflash.png")).convert_alpha()
padmiss_img= pygame.image.load(os.path.join(graphics_dir, "padmiss.png")).convert()
padhit_img= pygame.image.load(os.path.join(graphics_dir, "padhit.png")).convert()
miss_img= pygame.image.load(os.path.join(graphics_dir, "miss.png")).convert()
hit_img= pygame.image.load(os.path.join(graphics_dir, "hit.png")).convert()
sword_img= pygame.image.load(os.path.join(graphics_dir, "sword.png")).convert_alpha()
sword_rect = sword_img.get_rect()
padblue_img = pygame.image.load(os.path.join(graphics_dir, "padblue.png")).convert()
padoran_img = pygame.image.load(os.path.join(graphics_dir, "padoran.png")).convert()
padpurp_img = pygame.image.load(os.path.join(graphics_dir, "padpurp.png")).convert()
padyell_img = pygame.image.load(os.path.join(graphics_dir, "padyell.png")).convert()
noteblue_img = pygame.image.load(os.path.join(graphics_dir, "noteblue.png")).convert()
noteoran_img = pygame.image.load(os.path.join(graphics_dir, "noteoran.png")).convert()
notepurp_img = pygame.image.load(os.path.join(graphics_dir, "notepurp.png")).convert()
noteyell_img = pygame.image.load(os.path.join(graphics_dir, "noteyell.png")).convert()
cloud_img = pygame.image.load(os.path.join(cloud_dir, "cloud.png")).convert()
cloud_img2 = pygame.image.load(os.path.join(cloud_dir, "cloud2.png")).convert()
cloud_img3 = pygame.image.load(os.path.join(cloud_dir, "cloud3.png")).convert()
cloud_img4 = pygame.image.load(os.path.join(cloud_dir, "cloud4.png")).convert()

knightSkins=[]
for i in range(10):
    knightSkins.append(pygame.image.load(os.path.join(knight_dir, "knight"+str(i+1)+".png")).convert_alpha())
for i in reversed(range(10)):
    knightSkins.append(pygame.image.load(os.path.join(knight_dir, "knight"+str(i+1)+".png")).convert_alpha())
monsterSkins=[]
for i in range(11):
    monsterSkins.append(pygame.image.load(os.path.join(monster_dir, "monster"+str(i+1)+".png")).convert_alpha())
for i in reversed(range(11)):
    monsterSkins.append(pygame.image.load(os.path.join(monster_dir, "monster"+str(i+1)+".png")).convert_alpha())
for i in range(3):
    monsterSkins.append(pygame.image.load(os.path.join(monster_dir, "monsterdead"+str(i+1)+".png")).convert_alpha())
for i in reversed(range(3)):
    monsterSkins.append(pygame.image.load(os.path.join(monster_dir, "monsterdead"+str(i+1)+".png")).convert_alpha())

ghostSkins=[]
for i in range(3):
    ghostSkins.append(pygame.image.load(os.path.join(ghost_dir, "ghost"+ str(i+1)+".png")).convert_alpha())
for i in reversed(range(3)):
     ghostSkins.append(pygame.image.load(os.path.join(ghost_dir, "ghost"+str(i+1)+".png")).convert_alpha())

#loading music
pygame.mixer.music.load(os.path.join(snd_dir,"music.wav"))
pygame.mixer.music.set_volume(1)

# create sprite groups
game_sprites = pygame.sprite.Group()
note_sprites = pygame.sprite.Group()
knightgroup= pygame.sprite.Group()
monstergroup=pygame.sprite.Group()
cloudsprites = pygame.sprite.Group()
ghostgroup= pygame.sprite.Group()

# play background music
pygame.mixer.music.play(loops=-1)

#create conductor
conductor = Conductor()
conductorStarted = False

#variables for beat counter
timeSinceLastAction =0
timeSinceLastKnightFrame=0
timeSinceLastMonsterFrame=0
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
                conductor.handleD(monster)
            if event.key == pygame.K_f:
                conductor.handleF(monster)
            if event.key == pygame.K_j:
                conductor.handleJ(monster)
            if event.key == pygame.K_k:
                conductor.handleK(monster)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                leftDown = False
            if event.key == pygame.K_RIGHT:
                rightDown = False


    #update
    
    #also start conductor immediately
    if not conductorStarted:
        conductor.start()
        monster=Monster()
        monstergroup.add(monster)
        knight=Knight()
        knightgroup.add(knight)
        conductorStarted=True
    else:
        conductor.update()
    game_sprites.update()
    note_sprites.update()
    cloudsprites.update()
    ghostgroup.update()

    #draw
    #background
    window.blit(bg_img, bg_rect)
    window.blit(sword_img, (10,40))


    #prints beats in time
    timeSinceLastAction= timeSinceLastAction + timesincelasttick
    if(timeSinceLastAction>(conductor.secPerBeat*1000)):
        beat=beat+1
        timeSinceLastAction=0
    
    #animates knight in time hopefully
    timeSinceLastKnightFrame=timeSinceLastKnightFrame +timesincelasttick
    secperFrameK = (conductor.secPerBeat/(len(knight.images)))*1000
    if(timeSinceLastKnightFrame/2>secperFrameK):
        knightgroup.update()
        timeSinceLastKnightFrame =0

    #animates monster
    timeSinceLastMonsterFrame=timeSinceLastMonsterFrame +timesincelasttick
    secperFrameM = (conductor.secPerBeat/(len(monster.images)))*1000
    if(timeSinceLastMonsterFrame/4>secperFrameM):
        monstergroup.update()
        timeSinceLastMonsterFrame =0
        
    textRender(window, str(beat), 100, 500,500)

    game_sprites.draw(window)
    note_sprites.draw(window)
    knightgroup.draw(window)
    monstergroup.draw(window)
    cloudsprites.draw(window)
   
    # draw health bar
    for monster in monstergroup:
        monster.draw_health_bar(window)

    ghostgroup.draw(window)

    #updates all screen w/ no parameter
    pygame.display.update()

