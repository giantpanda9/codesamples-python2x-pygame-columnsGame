import pygame, os, random, json, operator

SCREEN_SIZE = WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = pygame.Color('white');
FPS = 30

os.environ['SDL_VIDEO_CENTERED']='1'

class keepScore():
  def __init__(self,initialScoreValue):
    self.countScore = initialScoreValue
  def addScore(self,currentScoreValue):
    self.countScore += currentScoreValue
  def getScoreValue(self):
    return self.countScore
  def loadScore(self):
    scores = {}        
    scoresJson = "";
    fin = open("data/scores.json", "rt")
    scoresJson = fin.read()
    fin.close()
    if scoresJson:
      scores = (json.loads(scoresJson))
    return scores
  def saveScore(self,name):
    scores = {}
    scores = self.loadScore()
    scores[name] = self.getScoreValue()
    scoresJson = json.dumps(scores)
    fout = open("data/scores.json", "wt")
    fout.write(scoresJson)
    fout.close()
    return 1
  def loadTopTen(self):
    scores = {}
    scores = self.loadScore()
    returned = []
    if scores:
      scoresSorted = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)
      count = 0
      for sortedScore in scoresSorted:
        count = count + 1
        displayCount = str(count)
        if len(str(count)) < 2:
          displayCount = "0" + str(count)
        returned.append(displayCount + " " + str(sortedScore[0]) + ", " + str(sortedScore[1]))
        if count == 10:
          break
    return returned
    
class preserveInitials():
  def __init__(self,initial1,initial2,initial3):
    self.initName = initial1.upper()
    self.initName2 = initial2.upper()
    self.initName3 = initial3.upper()
  def setInitial1(self,initial1):
    self.initName = initial1.upper()
  def setInitial2(self,initial2):
    self.initName2 = initial2.upper()
  def setInitial3(self,initial3):
    self.initName3 = initial3.upper()
  def getInitial1(self):
    return self.initName.upper()
  def getInitial2(self):
    return self.initName2.upper()
  def getInitial3(self):
    return self.initName3.upper()
  def getInitialsAsString(self):
    returned = self.initName.upper() + " " +self.initName2.upper() + " "+ self.initName3.upper()
    return returned

class operateData():
  def __init__(self):
    pass
  def openSettings(self):
    settings = {}
    
    settingsJson = "";
    fin = open("data/settings.json", "rt")
    settingsJson = fin.read()
    fin.close()
    if settingsJson:
      settings = (json.loads(settingsJson))
    return settings
    
  def saveSettings(self,PlayerName,PlayerSpeed):
    settings = {}
    settings = self.openSettings()
    settings[PlayerName] = PlayerSpeed
    
    settingsJson = json.dumps(settings)
    fout = open("data/settings.json", "wt")
    fout.write(settingsJson)
    fout.close()
  
class speedControl():
  def __init__(self,initialSpeedValue):
    self.speedValue = initialSpeedValue
  def changeSpeed(self,currentSpeedValue):
    self.speedValue = currentSpeedValue
  def getSpeedValue(self):
    return self.speedValue
  def getSpeedText(self):
    speedText = "Slow"
    if (self.speedValue == 1000):
      speedText = "Slow"
    if (self.speedValue == 500):
      speedText = "Normal"
    if (self.speedValue == 100):
      speedText = "Fast"
    return speedText

class oneBlock(pygame.sprite.Sprite):
  def __init__(self,image,pos_x,pos_y, speed, firstInGroup):
    super(oneBlock,self).__init__()
    self.images = []
    self.images.append(pygame.image.load('data/pic/1.png'))
    self.images.append(pygame.image.load('data/pic/2.png'))
    self.images.append(pygame.image.load('data/pic/3.png'))
    self.images.append(pygame.image.load('data/pic/4.png'))
    self.images.append(pygame.image.load('data/pic/5.png'))
    self.images.append(pygame.image.load('data/pic/6.png'))
    
    self.index = image
    
    self.image=self.images[self.index]
       
    self.x=pos_x
    self.y=pos_y
    self.pos = self.image.get_rect().move(0,10)
    self.rect = pygame.Rect(self.x, self.y, self.image.get_rect()[2], self.image.get_rect()[3])
    self.next_move = pygame.time.get_ticks() + speed
    self.speed = speed
    self.keepMoving = 1
    self.controllable = 1
    self.firstInGroup = firstInGroup
    
  def changeImage(self, image):
    self.index = image    
    self.image=self.images[self.index]
  
  def changeGrouping(self, firstInGroup):
    self.firstInGroup = firstInGroup
    
  def moveSides(self,direction):
    if ((self.keepMoving != 1) and (self.controllable != 1)):
      return 0;
    elif (direction == 'LEFT'):
      self.x -= self.image.get_rect()[2]
    elif (direction == 'RIGHT'):
      self.x += self.image.get_rect()[2]
      
    self.rect = pygame.Rect(self.x, self.y, self.image.get_rect()[2], self.image.get_rect()[3])
   
  def moveDown(self):
    if (self.keepMoving != 1):
      return 0
    elif pygame.time.get_ticks() >= self.next_move: 
      self.next_move = pygame.time.get_ticks() + self.speed
      self.y += self.image.get_rect()[2]
      self.rect = pygame.Rect(self.x, self.y, self.image.get_rect()[2], self.image.get_rect()[3])
  
  def stepDown(self):
    if ((self.keepMoving != 1) and (self.controllable != 1)):
      return 0   
    self.y += self.image.get_rect()[2]
    self.rect = pygame.Rect(self.x, self.y, self.image.get_rect()[2], self.image.get_rect()[3])

  def warpDown(self):
     
    self.y += self.image.get_rect()[2]
    self.rect = pygame.Rect(self.x, self.y, self.image.get_rect()[2], self.image.get_rect()[3])
  
  def moveUp(self):
    if (self.keepMoving != 1):
      return 0
    else:
      self.y -= self.image.get_rect()[2]
    self.rect = pygame.Rect(self.x, self.y, self.image.get_rect()[2], self.image.get_rect()[3])
    
  def standStill(self):
    self.keepMoving = 0
    self.controllable = 0
    self.firstInGroup = 0
  
  def setMoving(self):
    self.keepMoving = 1
  
  def isControllable(self):
    return self.controllable
    
  def isMoving(self):
    return self.keepMoving
  
  def isFirst(self):
    return self.firstInGroup
  
  def collided(self,target):    
    return self.rect.inflate(-5, -5).colliderect(target.rect)
    
  def blocks_collided_topbottom(self,targets):
    if (self.isMoving() != 1):
      return 0
    collision_detected = 0
    for target in targets: 
      if (target.isMoving() != 1):
        if (target.rect.collidepoint(self.rect.center)):
          collision_detected = 1
          break
    return collision_detected

  def blocks_collided_leftright(self,targets):
    if (self.isMoving() != 1):
      return 0
    collision_detected = 0
    for target in targets: 
      if (target.isMoving() != 1):
        if (self.rect.inflate(-5, -5).colliderect(target.rect)):
          collision_detected = 1
          break
    return collision_detected   
  
class pavement(pygame.sprite.Sprite):
  def __init__(self,position,screen_size):
    super(pavement,self).__init__()
    
    img = pygame.Surface((260,screen_size[1]))
    
    img = img.convert()
    img.fill((240, 240, 240))
    self.image=img
    self.rect = pygame.Rect(position, 0, self.image.get_rect()[2], self.image.get_rect()[3])
    
class bottom_pawl(pygame.sprite.Sprite):
  def __init__(self,position,screen_size):
    super(bottom_pawl,self).__init__()
   
    
    img = pygame.Surface((310, 43))
    
    img = img.convert()
    img.fill((240, 240, 240))
    self.image=img
    self.rect = pygame.Rect(239, position, self.image.get_rect()[2], self.image.get_rect()[3])
  
def blocks_gen(blocks,allsprites, speed):
  startPositionsX = [240,283,326,369,412,455,498]
  startPostionX = startPositionsX[random.randint(0,6)]
  Block = oneBlock(random.randint(0,5),startPostionX,0, speed, 0)
  blocks.append(Block)
  allsprites.add(Block)
  Block = oneBlock(random.randint(0,5),startPostionX,43, speed, 0)
  blocks.append(Block)
  allsprites.add(Block)
  Block = oneBlock(random.randint(0,5),startPostionX,86, speed, 1)
  blocks.append(Block)
  allsprites.add(Block)
  Block = "";
  return (blocks, allsprites)
  
def swapBlocks(targets):
  firstBlockNumber = 0
  blockSwapNum = 0
  countBlocks = 0
  swappyBlocks = []
  
  for target in targets:    
    if ((target.isMoving() == 1) and (target.isControllable() == 1)):
      swappyBlocks.append(countBlocks)
      if (target.isFirst() == 1):        
        firstBlockNumber = countBlocks
      else:
        pass
    countBlocks = countBlocks + 1
  for i in range(0, (int(len(swappyBlocks))-1)):
    currentBlock = swappyBlocks[i]
    if (currentBlock != firstBlockNumber):
      blockSwapNum = currentBlock
      tempImg = targets[blockSwapNum].index
      tempFirstInGroup = targets[blockSwapNum].firstInGroup
      targets[blockSwapNum].changeImage(targets[firstBlockNumber].index)
      targets[firstBlockNumber].changeImage(tempImg)
      
def shuffleBlocks(targets):
  firstBlockNumber = 0
  blockSwapNum = 0
  countBlocks = 0
  swappyBlocks = []
  for target in targets:
    if ((target.isMoving() == 1) and (target.isControllable() == 1)):
      
      if (target.isFirst() == 1):        
        firstBlockNumber = countBlocks
      else:
        swappyBlocks.append(countBlocks)
    countBlocks = countBlocks + 1

  blockSwapNum = swappyBlocks[random.randint(0,1)]

  tempImg = targets[blockSwapNum].index
  tempFirstInGroup = targets[blockSwapNum].firstInGroup
  targets[blockSwapNum].changeImage(targets[firstBlockNumber].index)
  targets[firstBlockNumber].changeImage(tempImg)

def searchAndDrop(targets):
  XsList = [240,283,326,369,412,455,498]
  YsList = [473,430,387,344,301,258,215,172,129,86,43,0]
  for AYs in YsList:
    for AXs in reversed(XsList):
      BYs = AYs + 43
      blockObject = blockByPosition(targets,(AXs,BYs))
      if (blockObject == -1):
        blockObject = blockByPosition(targets,(AXs,AYs))
        if (blockObject != -1):
          blockObject.setMoving()
  return 1

def verticalSearch(targets,allsprites,keepScoreInstance):
    XsList = [240,283,326,369,412,455,498]
    YsList = [516,473,430,387,344,301,258,215,172,129,86,43,0]
    
    for AXs in XsList:
      BCount = 0
      for AYs in YsList:
        BCount = BCount + 1
        verticalBlocksFound = []
        AIndex = indexByPosition(targets,AXs,AYs)
        verticalBlocksFound.append((AXs,AYs))
        if (AIndex != -1):
          for x in range(BCount, len(YsList)):
            BYs = YsList[x]
            BIndex = indexByPosition(targets,AXs,BYs)
            if (AIndex == BIndex):            
              verticalBlocksFound.append((AXs,BYs))
            else:
              break
        if (len(verticalBlocksFound) >= 3):
          lastBlockX = -1
          lastBlockY = -1
          keepScoreInstance.addScore(len(verticalBlocksFound))          
          for removedBlockTuple in verticalBlocksFound:
            globalCount = globalCountByPosition(targets,removedBlockTuple)
            blockObject = blockByPosition(targets,removedBlockTuple)
            lastBlockX = removedBlockTuple[0]
            lastBlockY = removedBlockTuple[1]
            allsprites.remove(blockObject)
            targets.pop(int(globalCount))
          for lastY in range(0, lastBlockY, 43):
            blockObject = blockByPosition(targets,(lastBlockX,lastY))
          return 1
    return 0 
    
def horizontalSearch(targets,allsprites,keepScoreInstance):
    XsList = [240,283,326,369,412,455,498]
    YsList = [516,473,430,387,344,301,258,215,172,129,86,43,0]
    for AYs in YsList:    
      BCount = 0
      for AXs in XsList:
        BCount = BCount + 1
        horizontalBlocksFound = []
        AIndex = indexByPosition(targets,AXs,AYs)
        horizontalBlocksFound.append((AXs,AYs))
        if (AIndex != -1):
          for x in range(BCount, len(XsList)):            
            BXs = XsList[x]            
            BIndex = indexByPosition(targets,BXs,AYs)
            if (AIndex == BIndex):            
              horizontalBlocksFound.append((BXs,AYs))
            else:
              break
        if (len(horizontalBlocksFound) >= 3):
          lastBlockX = []
          lastBlockY = -1
          keepScoreInstance.addScore(len(horizontalBlocksFound))          
          for removedBlockTuple in horizontalBlocksFound:
            globalCount = globalCountByPosition(targets,removedBlockTuple)
            blockObject = blockByPosition(targets,removedBlockTuple)
            lastBlockX.append(removedBlockTuple[0])
            lastBlockY = removedBlockTuple[1]
            allsprites.remove(blockObject)
            targets.pop(int(globalCount))
          for lastX in lastBlockX:
            for lastY in range(0,lastBlockY, 43):
              blockObject = blockByPosition(targets,(lastX,lastY))
          return 1
    return 0
    
def horizontalSearchZeroLine(targets,allsprites,keepScoreInstance):
    XsList = [240,283,326,369,412,455,498]
    BCount = 0
    for AXs in XsList:
      BCount = BCount + 1
      horizontalBlocksFound = []
      AIndex = indexByPosition(targets,AXs,0)
      if (AIndex != -1):
        return 1
    return 0 


def dropBlocks(targets):
  for target in targets:
    target.setMoving()
def globalCountByPosition(targets,pos):  
  returned = -1
  targetFound = 0
  count = 0
  for target in targets:
    if (((target.x, target.y) == pos) and (target.isMoving() != 1)):
      returned = count
      targetFound = 1
      break
    count = count + 1
  
  return returned

def blockByPosition(targets,pos):  
  returned = -1
  targetFound = 0
  count = 0
  for target in targets:
    if (((target.x, target.y) == pos) and (target.isMoving() != 1)):
      returned = target
      targetFound = 1
      break
    count = count + 1
  
  return returned

def indexByPosition(targets,posX,posY):  
  returned = -1
  targetFound = 0
  count = 0
  for target in targets:
    if ((target.x == posX) and (target.y == posY) and (target.isMoving() != 1)):
      returned = target.index
      targetFound = 1
      break
    count = count + 1
  
  return returned
# To demonstrate functional programming style alongside with class-oriented/OOP style 
def displayGameSpeed(surf, text, size, x, y):
  fontName = pygame.font.match_font('arial')
  scoreText = "Game Speed: " + " " + text
  font = pygame.font.Font(fontName, size)
  textSurface = font.render(scoreText, True, (0, 0, 0))
  textRect = textSurface.get_rect()
  textRect.midtop = (x, y)
  surf.blit(textSurface, textRect)


def displayScore(surf, text, size, x, y):
  fontName = pygame.font.match_font('arial')
  scoreText = "Score: " + " " + text
  font = pygame.font.Font(fontName, size)
  textSurface = font.render(scoreText, True, (0, 0, 0))
  textRect = textSurface.get_rect()
  textRect.midtop = (x, y)
  surf.blit(textSurface, textRect)

def displayButton(surf, text, size, x, y):
  fontName = pygame.font.match_font('arial')
  scoreText = text
  font = pygame.font.Font(fontName, size)
  font.set_underline(1)
  textSurface = font.render(scoreText, True, (0, 0, 0))
  textRect = textSurface.get_rect()
  textRect.midtop = (x, y)
  surf.blit(textSurface, textRect)
  return textRect

def displayText(surf, text, size, x, y):
  fontName = pygame.font.match_font('arial')

  font = pygame.font.Font(fontName, size)
  textSurface = font.render(text, True, (0,0,0))
  textRect = textSurface.get_rect()
  textRect.midtop = (x, y)
  surf.blit(textSurface, textRect)

def inputBox(surf,x,y,text,size):
  fontName = pygame.font.match_font('arial')
  font = pygame.font.Font(fontName, size)
  textSurface = font.render(text, True, (0, 0, 0))
  textRect = pygame.draw.rect(surf,(255,255,255),(x,y,20,20)) 
  surf.blit(textSurface,textRect)
  return textRect

def getEventKey(event):
  returned = ""
  if event.type == pygame.KEYDOWN:
    if event.key <= 256:
      returned = chr(event.key)
  return returned
#PyGame insists on rendering each line separatelly
def displayTopTen(surf,topTenArray):
  positionTopTen = 95
  for topTenScoreItem in topTenArray:
    displayText(surf, topTenScoreItem, 18,650, positionTopTen)
    positionTopTen = positionTopTen + 30
  return 1
#PyGame insists on rendering each line separatelly - end
  
def main():

  pygame.init()
  fullscreen = 0
  screendepth = pygame.display.mode_ok(SCREEN_SIZE, fullscreen, 32)
  screen = pygame.display.set_mode(SCREEN_SIZE, fullscreen, screendepth)
  restartGame = 0
  pygame.display.set_caption('InfiniteColumns')
  
  pavement_left = pavement(-20,screen.get_size())
  pavement_right = pavement(543,screen.get_size())
  floor = bottom_pawl(560,screen.get_size())
  clock = pygame.time.Clock()
  allsprites = pygame.sprite.RenderUpdates()
  allsprites.add(pavement_left)
  allsprites.add(pavement_right)
  allsprites.add(floor)  
  background = pygame.Surface(screen.get_size())
  background = background.convert()
  background.fill((250, 250, 250))
  blocks = []
  generate_new = 1
  keepScoreInstance = keepScore(0)
  operateDataInstance = operateData()
  settingsObject = operateDataInstance.openSettings()
  speedControlInstance = speedControl(settingsObject['M R X'])
  preserveInitialsInstance = preserveInitials('m','r','x')
  topTenScore = keepScoreInstance.loadTopTen()  
  while 1:    
    verticalSearch(blocks,allsprites,keepScoreInstance)
    horizontalSearch(blocks,allsprites,keepScoreInstance)
    if horizontalSearchZeroLine(blocks,allsprites,keepScoreInstance) == 1:
      #Save score
      keepScoreInstance.saveScore(preserveInitialsInstance.getInitialsAsString())
      #Restart
      pygame.quit()
      restartGame = 1
      break
    searchAndDrop(blocks)
    stil_moving_some = 0 
    for Block in blocks:
      if (Block.isMoving() == 1):
        stil_moving_some = 1
        break
    if ((generate_new == 1) and (stil_moving_some == 0)):
      stil_moving_some = 0
      generate_new = 0
      blocks_gen(blocks, allsprites, speedControlInstance.getSpeedValue())    
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        shuffleBlocks(blocks) # If Space is pressed - shuffle droppping blocks randomly      
      if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
          swapBlocks(blocks) # If KeyUP is pressed move the first block up and down - first goes up
      for Block in blocks:
        if event.type == pygame.QUIT:
          pygame.quit()
          quit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
          pygame.quit()
          quit()
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:                
          Block.moveSides("RIGHT")
          if Block.blocks_collided_leftright(blocks):
            for Block in blocks: Block.moveSides("LEFT")
          if Block.collided(pavement_right):
            for Block in blocks: Block.moveSides("LEFT")
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
          Block.moveSides("LEFT")          
          if Block.blocks_collided_leftright(blocks):
            for Block in blocks: Block.moveSides("RIGHT")
          if Block.collided(pavement_left):
            for Block in blocks:  Block.moveSides("RIGHT")
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:          
          if Block.collided(floor):
            for Block in reversed(blocks):
              Block.moveUp()
              Block.standStill()
            generate_new = 1
          elif (Block.blocks_collided_topbottom(blocks)):
            for Block in reversed(blocks):
              if ((Block.isMoving() == 1) and (Block.isControllable() == 1)):
               Block.moveUp()
               Block.standStill()
            generate_new = 1
          else:
             Block.stepDown()

    for Block in blocks:      
      if (Block.collided(floor)):
        for Block in reversed(blocks):
          Block.moveUp()
          Block.standStill()
        generate_new = 1
      elif (Block.blocks_collided_topbottom(blocks)):
        for Block in reversed(blocks):
          if (Block.isMoving() == 1):
            Block.moveUp()
            Block.standStill()
        generate_new = 1
      else:
        Block.moveDown()
    
    allsprites.update()

    #Draw Everything
    screen.blit(background, (0, 0))
    allsprites.draw(screen)
    displayScore(screen, str(keepScoreInstance.getScoreValue()), 18,600, 10)
    displayGameSpeed(screen, str(speedControlInstance.getSpeedText()), 18,120, 70)
    displayText(screen, "Main Menu:", 18,120, 10)
    restartButtonRect = displayButton(screen, "Start New Game", 18, 80, 40)
    slowButtonRect = displayButton(screen, "Slow Speed", 18, 62, 100)
    normalButtonRect = displayButton(screen, "Normal Speed", 18, 72, 130)
    fastButtonRect = displayButton(screen, "Fast Speed", 18, 60, 160)
    exitButtonRect = displayButton(screen, "Exit Game", 18, 55, 200)
    displayText(screen, "Score Settings:", 18,70, 250)
    displayText(screen, "Scores being stored ", 15,90, 290)
    displayText(screen, "against player initials", 15,90, 320)
    displayText(screen, "To change player initial ", 15,100, 350)
    displayText(screen, "1.Hover the mouse cursor over it", 15,112, 380)
    displayText(screen, "2.Hit the button with expected letter", 15,120, 410)
    displayText(screen, "Top 10 Score:", 18,650, 60)   
    displayTopTen(screen,topTenScore)
    displayText(screen, "Developed by", 18,650, 450)
    displayText(screen, "Nikolay Chegodaev (c) 2020", 18,670, 475)
    initialTextBox1 = inputBox(screen,30,440,preserveInitialsInstance.getInitial1(),18)
    initialTextBox2 = inputBox(screen,70,440,preserveInitialsInstance.getInitial2(),18)
    initialTextBox3 = inputBox(screen,110,440,preserveInitialsInstance.getInitial3(),18)
    if restartButtonRect.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONUP:
      pygame.quit()
      restartGame = 1
      # For now the code does not seem to complicated to rework it as a seprate function and nto to use breaks
      # so see no reason to invent the wheel again and again and for now just using break and recall to main() recursively
      # TODO should be reworked in the future, if additional functionality would turn this into necessity
      break
    if initialTextBox1.collidepoint(pygame.mouse.get_pos()):
      inputInitial1 = getEventKey(event)
      if inputInitial1:
        preserveInitialsInstance.setInitial1(inputInitial1)
        operateDataInstance.saveSettings(str(preserveInitialsInstance.getInitialsAsString()),int(speedControlInstance.getSpeedValue()))
        initialTextBox1 = inputBox(screen,30,440,preserveInitialsInstance.getInitial1(),18)
        if str(preserveInitialsInstance.getInitialsAsString()) in settingsObject:
          speedControlInstance = speedControl(settingsObject[str(preserveInitialsInstance.getInitialsAsString())])
    if initialTextBox2.collidepoint(pygame.mouse.get_pos()):
      inputInitial2 = getEventKey(event)
      if inputInitial2:
        preserveInitialsInstance.setInitial2(inputInitial2)
        operateDataInstance.saveSettings(str(preserveInitialsInstance.getInitialsAsString()),int(speedControlInstance.getSpeedValue()))
        initialTextBox2 = inputBox(screen,70,440,preserveInitialsInstance.getInitial2(),18)
        if str(preserveInitialsInstance.getInitialsAsString()) in settingsObject:
          speedControlInstance = speedControl(settingsObject[str(preserveInitialsInstance.getInitialsAsString())])
    if initialTextBox3.collidepoint(pygame.mouse.get_pos()):
      inputInitial3 = getEventKey(event)
      if inputInitial3:
        preserveInitialsInstance.setInitial3(inputInitial3)
        operateDataInstance.saveSettings(str(preserveInitialsInstance.getInitialsAsString()),int(speedControlInstance.getSpeedValue()))
        initialTextBox3 = inputBox(screen,110,440,preserveInitialsInstance.getInitial3(),18)
        if str(preserveInitialsInstance.getInitialsAsString()) in settingsObject:
          speedControlInstance = speedControl(settingsObject[str(preserveInitialsInstance.getInitialsAsString())])        
    if slowButtonRect.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONUP:
      speedControlInstance.changeSpeed(1000)
      operateDataInstance.saveSettings(str(preserveInitialsInstance.getInitialsAsString()),int(speedControlInstance.getSpeedValue()))
      displayGameSpeed(screen, str(speedControlInstance.getSpeedText()), 18,120, 70)
    if normalButtonRect.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONUP:
      speedControlInstance.changeSpeed(500)
      operateDataInstance.saveSettings(str(preserveInitialsInstance.getInitialsAsString()),int(speedControlInstance.getSpeedValue()))
      displayGameSpeed(screen, str(speedControlInstance.getSpeedText()), 18,120, 70)
    if fastButtonRect.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONUP:
      speedControlInstance.changeSpeed(100)
      operateDataInstance.saveSettings(str(preserveInitialsInstance.getInitialsAsString()),int(speedControlInstance.getSpeedValue()))
      displayGameSpeed(screen, str(speedControlInstance.getSpeedText()), 18,120, 70)
    if exitButtonRect.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONUP:
      pygame.quit()
      quit()
    pygame.display.flip()     
    clock.tick(60)


  if restartGame == 1:
    main()
  else:
    quit()
if __name__=='__main__': main()
