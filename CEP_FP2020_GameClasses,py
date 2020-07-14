import pygame as pg
import time
import random
import sys
from os import path
from CEP_FP2020_Settings import *

pg.init()

class Score(pg.sprite.Sprite):
    def __init__(self,x,y,mode):
        pg.sprite.Sprite.__init__(self)
        self.bscore = 0
        self.pscore = 0
        self.mode = mode
        self.image = self.drawImage()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def drawImage(self):
        surface = pg.Surface((300,60))
        surface.fill(RED)
        surface.set_colorkey(RED)
        if self.mode == "bot":
            player = arial20.render("Player: " + str(round(self.pscore)),True,BLACK)
            bot = arial20.render("Bot: " + str(round(self.bscore)),True,BLACK)
        else:
            player = arial20.render("Player 1: " + str(round(self.pscore)),True,BLACK)
            bot = arial20.render("Player 2: " + str(round(self.bscore)),True,BLACK)
        pg.draw.rect(surface,[255,102,102],[0,0,150,60])
        pg.draw.rect(surface,[102,255,255],[150,0,300,60])
        pg.draw.rect(surface,LIGHTGREY,[0,0,300,60],5)
        pg.draw.line(surface,LIGHTGREY,[150,0],[150,300],5)
        surface.blit(player,text_centering(player,150,60,"both"))
        surface.blit(bot,text_centering(player,450,60,"both"))
        return surface.convert_alpha()

    def update(self,correct,correct2):
        global add_score
        global add_bscore
        if correct == True:
            if add_score == 0:
                self.pscore +=1
                add_score = 1
        if correct2 == True:
            if add_bscore == 0:
                self.bscore +=1
                add_bscore = 1
        self.image = self.drawImage()

    def next_q(self):
        global add_score
        global add_bscore
        add_score = 0
        add_bscore = 0

    def draw(self,screen):
        screen.blit(self.image,self.rect)

    def draw_gameover(self,screen):
        self.rect.centery = 415
        screen.blit(self.image,self.rect)

class Turn(pg.sprite.Sprite):
    def __init__(self,x,y,player):
        pg.sprite.Sprite.__init__(self)
        self.player = player
        self.image = self.drawImage()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.centery = y

    def drawImage(self):
        surface = pg.Surface((140,50))
        surface.fill(RED)
        surface.set_colorkey(RED)
        pg.draw.rect(surface,WHITE,[0,0,140,50])
        pg.draw.rect(surface,LIGHTGREY,[0,0,140,50],2)
        player = arial20.render(self.player,True,BLACK)
        surface.blit(player,text_centering(player,120,50,"both"))
        return surface.convert_alpha()

    def draw(self,screen):
        screen.blit(self.image,self.rect)

class Mode(pg.sprite.Sprite):
    def __init__(self,x,y,text,mode):
        pg.sprite.Sprite.__init__(self)
        self.width = 500
        self.height = 150
        self.color = [153,204,255]
        self.choice = text
        self.mode = mode
        self.image = self.drawImage()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.color2 = [102,178,255]

    def drawImage(self):
        button_surface = pg.Surface((self.width,self.height))
        button_surface.fill(RED)
        button_surface.set_colorkey(RED)
        pg.draw.rect(button_surface,self.color,[0,0,self.width,self.height])
        key = arial25.render(self.choice,True,WHITE)
        button_surface.blit(key,text_centering(key,self.width,self.height,"both"))
        return button_surface.convert()

    def draw(self,screen):
        screen.blit(self.image,self.rect)

    def update(self,choice):
        if choice == self.mode:
            self.color = self.color2
            self.image = self.drawImage()
        else:
            self.color = [153,204,255]
            self.image = self.drawImage()

class MenuButton(pg.sprite.Sprite):
    def __init__(self,x,y,function):
        pg.sprite.Sprite.__init__(self)
        self.color = mb_colour
        self.width = 200
        self.height = 100
        self.function = function
        self.image = self.drawImage()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.color2 = mb_colour2

    def drawImage(self):
        bsurface = pg.Surface((self.width,self.height))
        bsurface.fill(RED)
        bsurface.set_colorkey(RED)
        pg.draw.rect(bsurface,self.color,[0,0,self.width,self.height])
        key = arial20.render(self.function,True,DARKGREY)
        bsurface.blit(key,text_centering(key,self.width,self.height,"both"))
        return bsurface.convert()

    def drawbutton(self,screen):
        screen.blit(self.image,self.rect)

    def hover(self):
        coord = pg.mouse.get_pos()
        if self.rect.collidepoint(coord):
            self.color = self.color2
            self.image = self.drawImage()
        else:
            self.color = mb_colour
            self.image = self.drawImage()

class PauseButton(pg.sprite.Sprite):
        def __init__(self,x,y):
            pg.sprite.Sprite.__init__(self)
            self.color = mb_colour
            self.width = 55
            self.height = 50
            self.image = self.drawImage()
            self.rect = self.image.get_rect()
            self.pause = False
            self.rect.centerx = x
            self.rect.centery = y

        def drawImage(self):
            bsurface = pg.Surface((self.width,self.height))
            bsurface.fill(RED)
            bsurface.set_colorkey(RED)
            pg.draw.rect(bsurface,self.color,[0,0,self.width,self.height])
            pg.draw.rect(bsurface,WHITE,[5,5,20,40])
            pg.draw.rect(bsurface,WHITE,[30,5,20,40])
            return bsurface.convert()

        def update(self):
            coord = pg.mouse.get_pos()
            mousestate = pg.mouse.get_pressed()[0]
            if self.rect.collidepoint(coord) and mousestate == 1:
                self.pause = True

        def drawbutton(self,screen):
            screen.blit(self.image,self.rect)

class GameButton(pg.sprite.Sprite):
    def __init__(self,x,y,function):
        pg.sprite.Sprite.__init__(self)
        self.color = [102,102,255]
        self.color2 = [51,51,255]
        self.width = 75
        self.height = 75
        self.function = function
        self.image = self.drawImage()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def drawImage(self):
        bsurface = pg.Surface((self.width,self.height))
        bsurface.fill(RED)
        bsurface.set_colorkey(RED)
        pg.draw.rect(bsurface,self.color,[0,0,self.width,self.height])
        pg.draw.rect(bsurface,self.color2,[0,0,self.width,self.height],4)
        key = arial20.render(self.function,True,WHITE)
        bsurface.blit(key,text_centering(key,self.width,self.height,"both"))
        return bsurface.convert()

    def drawbutton(self,screen):
        screen.blit(self.image,self.rect)

class Timer(pg.sprite.Sprite):
    def __init__(self,x,y,t):
        pg.sprite.Sprite.__init__(self)
        self.width = 160
        self.height = 60
        self.time = t
        self.image = self.drawImage()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def drawImage(self):
        surface = pg.Surface((self.width,self.height))
        surface.fill(RED)
        surface.set_colorkey(RED)
        pg.draw.rect(surface,[50,100,150],[40,7,120,47])
        pg.draw.rect(surface,WHITE,[40,7,118,47],2)
        text = arial20.render("TIME LEFT",True,BLACK)
        surface.blit(text,text_centering(text,65,60,"y"))
        pg.draw.circle(surface,WHITE,[30,30],30)
        if int(self.time) > 0:
            key = arial20.render(self.time,True,BLACK)
            surface.blit(key,text_centering(key,60,60,"both"))
        else:
            key = arial20.render("0",True,BLACK)
            surface.blit(key,text_centering(key,60,60,"both"))
        return surface.convert()

    def update(self):
        if int(self.time) <= 10:
            self.color = RED
        elif int(self.time) > 30:
            self.time = str(30)
        self.image = self.drawImage()

    def draw(self,screen):
        screen.blit(self.image,self.rect)

class InputText():
    def __init__(self, x, y, color, font,text=''):
        self.surface = pg.Surface((1,1))
        self.text = ['']
        self.font = font
        self.color = color
        self.exceed = False
        self.width = 800
        self.height = 75
        self.image = self.drawImage()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.submit = False

    def drawImage(self):
        image = pg.Surface((self.width,self.height))
        image.fill(DARKGREY)
        image.set_colorkey(DARKGREY)
        pg.draw.rect(image,[204,255,255],[0,0,self.width,self.height])
        pg.draw.rect(image,[50,100,150],[0,0,self.width,self.height],2)
        key = arial20.render("Answer:",True,BLACK)
        image.blit(key,text_centering(key,10,self.height,"y"))
        return image.convert_alpha()

    def handle_event(self, event):
        if event.type == pg.KEYDOWN:
            self.cursor_visible = True
            if event.key == pg.K_BACKSPACE:
                if self.text[len(self.text)-1] == '':
                    if len(self.text)-1 == 0:
                        pass
                    else:
                        self.text.pop()
                self.text[len(self.text)-1] = self.text[len(self.text)-1][:-1]
            else:
                if self.max == False and self.submit == False:
                    if event.unicode.isalpha() or event.unicode == " " or event.unicode.isdigit():
                        self.text[len(self.text)-1] += event.unicode
        self.surface = self.font.render(self.text[len(self.text)-1], True, self.color)

    def update(self,time):
        words = self.text[len(self.text)-1].split()
        if self.surface.get_width() > 700:
            self.max = True
        else:
            self.max = False
        if time <= 0:
            self.submit = True

    def draw(self, screen):
        screen.blit(self.image,self.rect)
        screen.blit(self.surface,[95,713,600,75])

class check_ans(pg.sprite.Sprite):
    def __init__(self,x,y,ans,ans2,c_ans,type):
        pg.sprite.Sprite.__init__(self)
        self.ans = ans
        self.ans2 = ans2
        self.type = type
        self.correct_ans = c_ans
        self.image = cross_img
        self.correct = False
        self.correct2 = False
        self.message = "wrong!"
        self.message2 = "wrong!"
        if len(self.correct_ans) > 1:
            for i in self.correct_ans:
                if i.lower() == self.ans.lower():
                    self.image = tick_img
                    self.correct = True
                    self.message = "right!"
                if i.lower() == self.ans2.lower():
                    self.correct2= True
                    self.message2 = "right!"
        else:
            if self.ans.lower() == self.correct_ans[0].lower():
                self.image = tick_img
                self.correct = True
                self.message = "right!"
            if self.ans2.lower() == self.correct_ans[0].lower():
                self.correct2= True
                self.message2 = "right!"
        self.rect = self.image.get_rect()
        self.rect.x = 770
        self.rect.y = 725
        self.image2 = self.drawImage()
        self.rect2 = self.image2.get_rect()
        self.rect2.centerx = x
        self.rect2.centery = y

    def drawImage(self):
        surface = pg.Surface((600,115))
        surface.fill(RED)
        surface.set_colorkey(RED)
        pg.draw.rect(surface,YELLOW,[0,0,600,115])
        pg.draw.rect(surface,WHITE,[0,0,598,113],2)
        if self.type == "bot":
            key = arial20.render("You got it " + self.message,True,BLACK)
            key3 = arial20.render("The bot's answer is " + self.ans2 + ". It got it " +self.message2,True,BLACK)
        else:
            key = arial20.render("Player 1's answer is "+ self.ans + ". It is " +self.message,True,BLACK)
            key3 = arial20.render("Player 2's answer is " + self.ans2 + ". It is " +self.message2,True,BLACK)
        if self.correct == True and self.correct2 == True:
            if self.ans != self.ans2:
                key2 = arial20.render("The correct answers are " + self.ans.lower() + " or " +self.ans2.lower() + ".",True,BLACK)
            else:
                key2 = arial20.render("The correct answer is " + self.ans.lower() +  ".",True,BLACK)
        elif self.correct == True and self.correct2 == False:
            key2 = arial20.render("The correct answer is " + self.ans.lower() + ".",True,BLACK)
        elif self.correct == False and self.correct2 == True:
            key2 = arial20.render("The correct answer is " + self.ans2.lower() + ".",True,BLACK)
        elif self.correct == False and self.correct2 == False:
            key2 = arial20.render("The correct answer is " + self.correct_ans[0].lower() + ".",True,BLACK)
        surface.blit(key,text_centering(key,600,10,"x"))
        surface.blit(key3,text_centering(key3,600,50,"x"))
        surface.blit(key2,text_centering(key2,600,90,"x"))
        return surface.convert_alpha()

    def draw(self,screen):
        if self.type == "bot":
            screen.blit(self.image,self.rect)
        screen.blit(self.image2,self.rect2)

class Hint(pg.sprite.Sprite):
    def __init__(self,x,y,hint,hint_left):
        pg.sprite.Sprite.__init__(self)
        self.hint = hint
        self.hint_left = hint_left
        self.image = self.drawImage1()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.image2 = self.drawImage2()
        self.rect2 = self.image2.get_rect()
        self.rect2.centerx = x-90
        self.rect2.centery = y+60

    def drawImage1(self):
        surface = pg.Surface((120,60))
        surface.fill(RED)
        surface.set_colorkey(RED)
        pg.draw.rect(surface,LIGHTGREY,[0,0,120,60],0)
        pg.draw.rect(surface,YELLOW,[0,0,118,58],2)
        surface.blit(hint_img,[10,5])
        key = arial20.render("X " + str(self.hint_left),True,BLACK)
        surface.blit(key,text_centering(key,70,60,"y"))
        return surface.convert_alpha()

    def drawImage2(self):
        surface = pg.Surface((300,45))
        surface.fill(RED)
        surface.set_colorkey(RED)
        pg.draw.rect(surface,WHITE,[0,0,300,45])
        pg.draw.rect(surface,YELLOW,[0,0,298,43],2)
        key = arial20.render("Hint: " + str(self.hint),True,BLACK)
        surface.blit(key,text_centering(key,10,45,"y"))
        return surface.convert_alpha()

    def draw(self,screen,hint_minus):
        screen.blit(self.image,self.rect)
        if hint_minus == 1:
            screen.blit(self.image2,self.rect2)

class GameOver_Display(pg.sprite.Sprite):
    def __init__(self,x,y,pscore,bscore,mode):
        pg.sprite.Sprite.__init__(self)
        self.width = 800
        self.height = 400
        self.pscore = pscore
        self.bscore = bscore
        self.mode = mode
        self.image = self.drawImage()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def drawImage(self):
        dsurface = pg.Surface((self.width,self.height))
        dsurface.fill(RED)
        dsurface.set_colorkey(RED)
        pg.draw.rect(dsurface,(0,128,255),[0,0,self.width,self.height],3)
        line1 = arial55.render("Final Score:",True,WHITE)
        if self.mode == "bot":
            if self.pscore == self.bscore:
                line2 = arial35.render("It's a draw!",True,WHITE)
            elif self.pscore > self.bscore:
                line2 = arial35.render("Congratulations! You have defeated the bot!",True,WHITE)
            else:
                line2 = arial35.render("Unfortunately, you lost! Better luck next time!",True,WHITE)
        else:
            if self.pscore == self.bscore:
                line2 = arial35.render("It's a draw!",True,WHITE)
            elif self.pscore > self.bscore:
                line2 = arial35.render("Congratulations Player 1! You have defeated Player 2!",True,WHITE)
            else:
                line2 = arial35.render("Congratulations Player 2! You have defeated Player 1!",True,WHITE)
        dsurface.blit(line1,text_centering(line1,self.width,50,"x"))
        dsurface.blit(line2,text_centering(line2,self.width,310,"x"))
        return dsurface.convert()

    def draw(self,screen):
        screen.blit(self.image,self.rect)

class DifficultyLvl(pg.sprite.Sprite):
    def __init__(self,x,y):
        pg.sprite.Sprite.__init__(self)
        self.color = [153,153,255]
        self.width = 700
        self.height = 300
        self.radius = 15
        self.default_circle = [350,150]
        self.image = self.drawImage()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.difficulty = "MEDIUM"

    def drawImage(self):
        difficulty_surface = pg.Surface((self.width,self.height))
        difficulty_surface.fill(BLUE)
        difficulty_surface.set_colorkey(BLUE)
        pg.draw.rect(difficulty_surface,self.color,[0,0,self.width,self.height],5)
        pg.draw.line(difficulty_surface,self.color,[75,150],[625,150],15)
        pg.draw.circle(difficulty_surface,self.color,self.default_circle,self.radius)
        title = arial35.render("CHOOSE A DIFFICULTY LEVEL", True, WHITE)
        key = arial35.render("MEDIUM",True,WHITE)
        key2 = arial35.render("EASY",True,WHITE)
        key3 = arial35.render("HARD",True,WHITE)
        difficulty_surface.blit(key,text_centering(key,self.width,210,"x"))
        difficulty_surface.blit(key2,text_centering(key2,160,210,"x"))
        difficulty_surface.blit(key3,text_centering(key3,1240,210,"x"))
        difficulty_surface.blit(title,text_centering(title,self.width,50,"x"))
        return difficulty_surface.convert()

    def draw(self,screen):
        screen.blit(self.image,self.rect)

    def update(self):
        coord = pg.mouse.get_pos()
        mousestate = pg.mouse.get_pressed()[0]
        if mousestate == 1:
            if coord[0] < 275 and coord[0] > 225 and coord[1] > 390 and coord[1] < 410:
                self.default_circle = [85,150]
                self.image = self.drawImage()
                self.difficulty = "EASY"
            elif coord[0] > 725 and coord[0] < 775 and coord[1] > 390 and coord[1] < 410:
                self.default_circle = [620,150]
                self.image = self.drawImage()
                self.difficulty = "HARD"
            elif coord[0] > 480 and coord[1] <520 and coord[1] > 390 and coord[1] < 410:
                self.default_circle = [350,150]
                self.image = self.drawImage()
                self.difficulty = "MEDIUM"
            else:
                pass

    def give_difficulty_lvl(self):
        difficulty_lvl = "MEDIUM"
        if self.default_circle == [550,150]:
            difficulty_lvl = "HARD"
        elif self.default_circle == [50,150]:
            difficulty_lvl = "EASY"
        else:
            difficulty_lvl = "MEDIUM"
        return difficulty_lvl

class Question(pg.sprite.Sprite):
    def __init__(self,x,y,question_dict):
        pg.sprite.Sprite.__init__(self)
        self.width = 550
        self.height = 50
        self.color = BLACK
        self.topic = random.choice(list(question_dict.keys()))
        self.question = question_dict[self.topic][0]
        self.image = self.drawImage()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def drawImage(self):
        surface = pg.Surface((self.width,self.height))
        surface.fill(BLUE)
        surface.set_colorkey(BLUE)
        pg.draw.rect(surface,WHITE,[0,0,self.width-2,self.height])
        pg.draw.rect(surface,[50,100,150],[0,0,self.width,self.height],5)
        text = arial20.render("Q: "+self.question,True,BLACK)
        surface.blit(text,text_centering(text,5,self.height,"y"))
        return surface.convert()

    def draw(self,screen):
        screen.blit(self.image,self.rect)

class OnOffLine(pg.sprite.Sprite):
    def __init__(self,x,y):
        pg.sprite.Sprite.__init__(self)
        self.oncolor = [102,178,255]
        self.offcolor = [204,204,255]
        self.width = 500
        self.height = 65
        self.image = self.drawImage()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def drawImage(self):
        line_surface = pg.Surface((self.width,self.height))
        line_surface.fill(RED)
        line_surface.set_colorkey(RED)
        pg.draw.rect(line_surface,self.offcolor,[0,0,250,self.height])
        pg.draw.rect(line_surface,self.oncolor,[250,0,250,self.height])
        on = arial25.render("ON",True,WHITE)
        off = arial25.render("OFF",True,WHITE)
        line_surface.blit(on,[450,30])
        line_surface.blit(off,[15,30])
        return line_surface.convert()

    def draw(self,screen):
        screen.blit(self.image,self.rect)

    def update(self):
        coord = pg.mouse.get_pos()
        mousestate = pg.mouse.get_pressed()[0]
        if mousestate == 1:
            if coord[0] < 650 and coord[0] >= 400 and coord[1]>=250 and coord[1]<=320:
                self.oncolor = [204,204,255]
                self.offcolor = [102,178,255]
                self.image = self.drawImage()
            elif coord[0] > 650 and coord[0] <= 900 and coord[1]>=250 and coord[1]<=320:
                self.offcolor = [204,204,255]
                self.oncolor = [102,178,255]
                self.image = self.drawImage()
            else:
                pass

    def givesound(self):
        if self.oncolor == [102,178,255]:
            sound = "ON"
        else:
            sound = "OFF"
        return sound

class SoundButton(pg.sprite.Sprite):
    def __init__(self,x,y,text):
        pg.sprite.Sprite.__init__(self)
        self.width = 500
        self.height = 70
        self.color = [153,204,255]
        self.choice = text
        self.image = self.drawImage()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.color2 = [102,178,255]

    def drawImage(self):
        button_surface = pg.Surface((self.width,self.height))
        button_surface.fill(RED)
        button_surface.set_colorkey(RED)
        pg.draw.rect(button_surface,self.color,[0,0,self.width,self.height])
        key = arial35.render(self.choice,True,WHITE)
        button_surface.blit(key,text_centering(key,self.width,self.height,"both"))
        return button_surface.convert()

    def drawbutton(self,screen):
        screen.blit(self.image,self.rect)

    def update(self,choice):
        if self.choice == choice:
            self.color = self.color2
            self.image = self.drawImage()
        else:
            self.color = [153,204,255]
            self.image = self.drawImage()
