import pygame
import math
import random
from pyvidplayer2 import Video



pygame.joystick.init()
JOYSTICKS = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
CAPTION = "Animation Probleme des partis"
BACKGROUND = pygame.image.load('Accueil.png')
DEFAULT_PLAYER_WIDTH = 23
DEFAULT_PLAYER_HEIGHT = 47
DEFAULT_PROJ_WIDTH = 60
PLAYER_SIZE = 8
PROJ_VITESSE = 3
ATTACK_CHARGE_DURATION = 100
DEFAULT_HP_BAR_WIDTH = 720
DEFAULT_HP_BAR_HEIGHT = 45
(width, height) = (300, 200)

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

class Bouton(object):
  """Boutons selectionnable permettant de naviguer dans les menus."""
  def __init__(self,x,y,imagePath,imagePathS,ImagePathP,scale=1,selected=False):
    self.x = x
    self.y = y
    self.image = pygame.image.load(imagePath)
    image_rect = self.image.get_rect()
    new_width = image_rect.width*scale
    new_height = image_rect.height*scale
    self.image = pygame.transform.scale(self.image, (new_width, new_height))
    self.imageSelected = pygame.transform.scale(pygame.image.load(imagePathS), (new_width, new_height))
    self.imagePressed = pygame.transform.scale(pygame.image.load(ImagePathP), (new_width, new_height))
    self.selected = selected
    self.pressed = False
  
  def draw(self):
    if self.selected:
      if self.pressed:
        screen.blit(self.imagePressed,(self.x,self.y))
      else:
        screen.blit(self.imageSelected,(self.x,self.y))
    else:
      screen.blit(self.image,(self.x,self.y))



class Player():
  """Sprites controlled by the player"""
  def __init__(self,x,y,direction,scale=1):
    self.x = x
    self.y = y
    self.hp = 10
    self.dir = direction
    self.blocking = 0
    self.pretABloquer = True
    self.attacking = False
    self.blesse = 0
    if self.dir > 0:
      self.imagesHP = {i:pygame.transform.scale(pygame.image.load("hpFermat"+str(i)+".png"),(DEFAULT_HP_BAR_WIDTH,DEFAULT_HP_BAR_HEIGHT)) for i in range(11)}
      names = ["EFA","EFF","EFH","DFA","DFF","DFH","VFA","VFF","VFH"]
    else:
      self.imagesHP = {i:pygame.transform.scale(pygame.image.load("hpPascal"+str(i)+".png"),(DEFAULT_HP_BAR_WIDTH,DEFAULT_HP_BAR_HEIGHT)) for i in range(11)}
      names = ["DPA","DPF","DPH","EPA","EPF","EPH","VPA","VPF","VPH"]
    self.images = {name[0]+name[2]:pygame.transform.scale(pygame.image.load(name+".png"), (DEFAULT_PLAYER_WIDTH*scale, DEFAULT_PLAYER_HEIGHT*scale)) for name in names}
  
  def block(self):
    self.blocking = 20
    self.pretABloquer = False

  def draw(self):
    if self.dir > 0:
      screen.blit(self.imagesHP[self.hp],(1000,40))
    else:
      screen.blit(self.imagesHP[self.hp],(200,40))
    if self.blocking > 0:
      screen.blit(self.images['VA'],(self.x,self.y))
      self.blocking-=1
    elif self.blesse > 0:
      screen.blit(self.images['EA'],(self.x,self.y))
      self.blesse-=1
    elif self.attacking:
      screen.blit(self.images['DF'],(self.x,self.y))
    else:
      screen.blit(self.images['VH'],(self.x,self.y))
    
class Projectile(object):
  """Projectiles thrown by attacks"""
  def __init__(self,image,x,y,direction):
    self.x = x
    self.y = y
    self.dir = direction
    self.vitesse = 1
    self.image = image
  
  def draw(self):
    screen.blit(self.image,(self.x,self.y))
  
  def move(self):
    self.x -= self.dir*PROJ_VITESSE*self.vitesse
  
  def checkCollision(self,other):
    return (distance(self.x,self.y,other.x+DEFAULT_PLAYER_WIDTH*PLAYER_SIZE/2,other.y) <= 50)

class Tableau(object):
  """Chalkboards on the scene that display math symbols when the attacks are charged"""
  def __init__(self,x,y,scale=1):
    self.x = x
    self.y = y
    self.symboles = [pygame.transform.scale(pygame.image.load("symbole"+str(i)+".png"),(12,40)) for i in range(14)]
    self.listeSymboles = []
    self.randomizeList()

  def randomizeList(self):
    self.listeSymboles = [random.randint(0,len(self.symboles)-1) for i in range(100)]

  def draw(self,nbSymboles):
    for i in range(nbSymboles):
      screen.blit(self.symboles[self.listeSymboles[i]],(self.x+(i%20)*15,self.y+(i//20)*45))

class Entier(object):
  """Digits drawn to the scene that can be selected, increased or deacresed"""
  def __init__(self,x,y,value,selected=False):
    self.x = x
    self.y = y
    self.value = value
    self.selected = selected
    self.images = [pygame.image.load(str(i)+".png") for i in range(10)]
    self.boutonPlus = Bouton(self.x+7,self.y-20,"UP.png","UPSelect.png","UPPressed.png",scale=2)
    self.boutonMoins = Bouton(self.x+7,self.y+55,"DOWN.png","DOWNSelect.png","DOWNPressed.png",scale=2)
  
  def increase(self):
    self.value = (self.value + 1) % 10
  
  def decrease(self):
    self.value = (self.value - 1) % 10
  
  def set_value(self,value):
    self.value = value

  def draw(self):
    if self.selected:
      self.boutonPlus.draw()
      self.boutonMoins.draw()
    screen.blit(self.images[self.value],(self.x,self.y))

class Nombre(object):
  def __init__(self,x,y,value,selectable=False):
    self.x = x
    self.y = y
    self.value = value
    self.digits = [Entier(x+i*40,y,0) for i in range(4)]
    self.indexOfSelected = 0 if selectable else -1
  
  def updateValue(self):
    v = self.value
    for i in range(4):
      self.digits[3-i].value = v%10
      v=v//10
  
  def select_left(self):
    self.indexOfSelected = (self.indexOfSelected - 1) % 4
  
  def select_right(self):
    self.indexOfSelected = (self.indexOfSelected + 1) % 4
  
  def increase_value(self):
    self.value += 1*(10**(3-self.indexOfSelected)) % 10000
  
  def set_value(self,value):
    self.value = value
  
  def decrease_value(self):
    self.value -= 1*(10**(3-self.indexOfSelected)) % 10000
  def draw(self):
    for i in range(4):
      self.digits[i].selected = True if self.indexOfSelected == i else False
      self.digits[i].draw()

#setup
current_scene=0
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption(CAPTION)
#setup of the first scene (scene=0)
bouton2J = Bouton(1000,800,"boutonja2.png","boutonja2select.png","boutonja2pres.png",5,True)
boutonOrdi = Bouton(300,800,"boutonjao.png","boutonjaoselect.png","boutonjaopres.png",5)
#setup of the second scene (scene=1-> 2 players scene=2 -> 1 player)
fond = pygame.transform.scale(pygame.image.load("Fond.png"),(1920,1080))
pascal = Player(300,600,-1,PLAYER_SIZE)
fermat = Player(1450,600,1,PLAYER_SIZE)
imageProjectile = pygame.transform.scale(pygame.image.load("proj0.png"),(DEFAULT_PROJ_WIDTH,DEFAULT_PROJ_WIDTH))
listeProj = []
numProj = 0
numAtkFermat = 0
numAtkPascal = 0
tableauPascal = Tableau(450,610)
tableauFermat = Tableau(1140,610)
#setup of the third scene(scene=3)
erreur = pygame.image.load("Erreur.png")
timer = 100
#setup of the fourth scene(scene=4)
fond4 = pygame.image.load("prediction.png")
nombre = Nombre(400,950,5000,True)
nombre2 = Nombre(1300,950,5000,False)
nombre.updateValue()
nombre2.updateValue()
score1 = Entier(1000,312,0)
score2 = Entier(1080,312,0)
#setup of the fifth scene(scene=5)
dico_videos={}
for i in range(0,11):
    for j in range(0,11):
        if i+j>=7 and max(i,j) <= 8 and i!=j:
            dico_videos[(i,j)] = Video(f"videos-with-audio/{i}_{j}.mp4")

running = True
while running:




  if current_scene == 0:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      else:
          screen.blit(BACKGROUND,(0,0))
          bouton2J.draw()
          boutonOrdi.draw()
          if bouton2J.pressed:
            current_scene = 1
            pygame.display.flip()
          if boutonOrdi.pressed:
            current_scene = 2
            pygame.display.flip()
          if event.type == pygame.JOYBUTTONDOWN:#BUTTON PRESSED
            if bouton2J.selected:
              bouton2J.pressed = True
            if boutonOrdi.selected:
              boutonOrdi.pressed = True
          if not event.type == pygame.JOYBUTTONDOWN:
            bouton2J.pressed = False
            boutonOrdi.pressed = False
          if event.type == pygame.JOYAXISMOTION and event.axis==0 and round(event.value)>0: #RIGHT PRESSED
            bouton2J.selected = True
            boutonOrdi.selected = False
          if event.type == pygame.JOYAXISMOTION and event.axis==0 and round(event.value)<0: #LEFT PRESSED
            bouton2J.selected = False
            boutonOrdi.selected = True
          pygame.display.flip()





  elif current_scene == 1:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      else:
        if event.type == pygame.JOYBUTTONDOWN and event.button==9:
          current_scene = 0
        if event.type == pygame.JOYBUTTONDOWN and event.button==1:#BUTTON A PRESSED
          if event.joy==0 and not pascal.attacking and pascal.pretABloquer:
            pascal.block()
          elif event.joy==1 and not fermat.attacking and fermat.pretABloquer:
            fermat.block()
        if event.type == pygame.JOYBUTTONDOWN and event.button==0:#BUTTON B PRESSED
          if event.joy==0:
            pascal.attacking = True
          elif event.joy==1:
            fermat.attacking = True
        if event.type == pygame.JOYAXISMOTION and pascal.attacking and event.joy==0:
          numAtkPascal+=1
        if event.type == pygame.JOYAXISMOTION and fermat.attacking and event.joy==1:
          numAtkFermat+=1
    if numAtkFermat >= ATTACK_CHARGE_DURATION:
      listeProj.append(Projectile(imageProjectile,fermat.x,fermat.y,fermat.dir))
      numProj+=1
      numAtkFermat=0
      fermat.attacking = False
      tableauFermat.randomizeList()
    if numAtkPascal >= ATTACK_CHARGE_DURATION:
      listeProj.append(Projectile(imageProjectile,pascal.x,pascal.y,pascal.dir))
      numProj+=1
      pascal.attacking = False
      numAtkPascal=0
      tableauPascal.randomizeList()
    for proj in listeProj:
      if proj.dir < 0:
        target = fermat
      else:
        target = pascal
      if proj.checkCollision(target) and not target.blocking > 0:
        target.hp-=1
        target.blesse = 200
        target.pretABloquer = True
        listeProj.remove(proj)
      elif proj.checkCollision(target):
        proj.dir *= -1
        proj.vitesse *= 1.5
      if proj.x > 2000 or proj.x < 0:
        listeProj.remove(proj)
    if pascal.hp == 2 or fermat.hp == 2:
      score = (10-fermat.hp,10-pascal.hp)
      current_scene = 3
        


    screen.blit(fond,(0,0))
    tableauPascal.draw(numAtkPascal)
    tableauFermat.draw(numAtkFermat)
    pascal.draw()
    fermat.draw()
    for proj in listeProj:
      proj.draw()
      proj.move()
    pygame.display.flip()
  elif current_scene == 2:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      else:
        if event.type == pygame.JOYBUTTONDOWN and event.button==9:
          current_scene = 0
        if event.type == pygame.JOYBUTTONDOWN and event.button==1:#BUTTON A PRESSED
          if not pascal.attacking and pascal.pretABloquer:
            pascal.block()
        if event.type == pygame.JOYBUTTONDOWN and event.button==0:#BUTTON B PRESSED
          pascal.attacking = True
          fermat.attacking = True
        if event.type == pygame.JOYAXISMOTION and pascal.attacking:
          numAtkPascal+=1
        if fermat.attacking:
          numAtkFermat+=random.random()+0.5
      if numAtkFermat >= ATTACK_CHARGE_DURATION:
        listeProj.append(Projectile(imageProjectile,fermat.x,fermat.y,fermat.dir))
        numProj+=1
        numAtkFermat=0
        tableauFermat.randomizeList()
        fermat.attacking = False
      if numAtkPascal >= ATTACK_CHARGE_DURATION:
        listeProj.append(Projectile(imageProjectile,pascal.x,pascal.y,pascal.dir))
        numProj+=1
        pascal.attacking = False
        numAtkPascal=0
        tableauPascal.randomizeList()
    for proj in listeProj:
      if proj.dir < 0:
        target = fermat
      else:
        target = pascal
      if proj.checkCollision(target) and not target.blocking > 0:
        target.hp-=1
        target.blesse = 200
        target.pretABloquer = True
        listeProj.remove(proj)
      elif proj.checkCollision(target):
        proj.dir *= -1
        proj.vitesse *= 1.5
      if proj.x > 2000 or proj.x < 0:
        listeProj.remove(proj)
    if pascal.hp == 2 or fermat.hp == 2:
      score1.set_value(10-fermat.hp)
      score2.set_value(10-pascal.hp)
      current_scene = 3
      pygame.display.flip()
        


    screen.blit(fond,(0,0))
    tableauPascal.draw(numAtkPascal)
    tableauFermat.draw(round(numAtkFermat))
    pascal.draw()
    fermat.draw()
    for proj in listeProj:
      proj.draw()
      proj.move()
    pygame.display.flip()



  elif current_scene == 3:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
    screen.blit(erreur,(0,0))
    timer-=1
    if timer == 0:
      current_scene = 4
    pygame.display.flip()

  elif current_scene == 4:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      else:
        if event.type == pygame.JOYBUTTONDOWN and event.button==9:
          current_scene = 0
        if event.type == pygame.JOYBUTTONDOWN and event.button==8:
          current_scene = 5
        if event.type == pygame.JOYBUTTONDOWN:
          if event.button==1:
            nombre.increase_value()
          else:
            nombre.decrease_value()
          nombre.updateValue()
          nombre2.set_value(10000-nombre.value)
          nombre2.updateValue()
        if event.type == pygame.JOYAXISMOTION and event.axis==0 and round(event.value)>0: #RIGHT PRESSED
          nombre.select_right()
        if event.type == pygame.JOYAXISMOTION and event.axis==0 and round(event.value)<0: #LEFT PRESSED
          nombre.select_left()
    screen.blit(fond4,(0,0))
    nombre.draw()
    nombre2.draw()
    score1.draw()
    score2.draw()
    pygame.display.flip()



  elif current_scene == 5:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      else:
        if event.type == pygame.JOYBUTTONDOWN and event.button==9:
          current_scene = 0
    if dico_videos[score1.value,score2.value].draw(screen, (0, 0), force_draw=False):
      pygame.display.flip()
    