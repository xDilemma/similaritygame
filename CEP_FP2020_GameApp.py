import pygame as pg
import torch
import torchtext
import fastai
from fastai.vision import *
from fastai.metrics import error_rate
from fastai.text import *
import time
import random
import sys
from os import path
import classes
from CEP_FP2020_Settings import *

pg.init()

#CONVENIENT FUNCTIONS
def add_menubuttons(x,y,type,group):
    button = classes.MenuButton(x,y,type)
    group.add(button)

def add_soundbuttons(type,x,y):
    button = classes.SoundButton(x,y,type)
    sound_buttons.add(button)

#BUTTONS
pause_buttons = pg.sprite.Group()
gameover_buttons = pg.sprite.Group()
mode_buttons = pg.sprite.Group()
difficulty_buttons = pg.sprite.Group()
intro_buttons = pg.sprite.Group()
sound_buttons = pg.sprite.Group()
add_menubuttons(MIDWIDTH,300,"Continue",pause_buttons)
add_menubuttons(MIDWIDTH,450,"Restart",pause_buttons)
add_menubuttons(MIDWIDTH,600,"Menu",pause_buttons)
add_menubuttons(350,700,"Restart",gameover_buttons)
add_menubuttons(700,700,"Menu",gameover_buttons)
add_menubuttons(695,475,"Start!",intro_buttons)
add_menubuttons(695,595,"Instructions",intro_buttons)
add_menubuttons(695,715,"Sound Settings",intro_buttons)
add_menubuttons(300,650,"Menu",difficulty_buttons)
add_menubuttons(700,650,"GO!",difficulty_buttons)
add_menubuttons(300,650,"Menu",mode_buttons)
add_menubuttons(700,650,"GO!",mode_buttons)
add_soundbuttons("Silver Scrapes",650,375)
add_soundbuttons("Piercing Light",650,475)
add_soundbuttons("The Glory",650,575)
add_soundbuttons("Worlds Collide",650,675)

submit_button = classes.GameButton(860,725,"Submit")
next_button = classes.GameButton(940,725,"Next")

#GAME FUNCTIONS
def Unpause():
    global elapsed_time
    global full_elapsed_time_lst
    global elapsed_time_lst
    global add

    if len(full_elapsed_time_lst) == 0:
        full_elapsed_time_lst.append(int(time.time()-p_time))
    else:
        if int(time.time()-p_time) not in full_elapsed_time_lst:
            full_elapsed_time_lst.append(int(time.time()-p_time))
    if add == 0:
        elapsed_time_lst.append(max(full_elapsed_time_lst))
        add = 1
        full_elapsed_time_lst = []
    if add == 1:
        for i in elapsed_time_lst:
            elapsed_time += i
            add = 2

    global paused
    p_button.pause = False
    pg.mixer.music.unpause()
    paused = False

def Pause():
    global p_time
    p_time = time.time()
    global add
    add = 0
    global elapsed_time
    elapsed_time = 0

    while paused == True:
        screen.blit(gbackground_img,[0,0])

        for event in pg.event.get():
            coord = pg.mouse.get_pos()
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                for i in pause_buttons:
                    if i.rect.collidepoint(coord):
                        if i.function == "Menu":
                            Game_Intro()
                        elif i.function == "Continue":
                            Unpause()
                        else:
                            Unpause()
                            Restart()
                            ChooseMode()

        text = arial120.render("Game Paused", True, [0,102,204])
        screen.blit(text,text_centering(text,WIDTH,80,"x"))

        for i in pause_buttons:
            i.drawbutton(screen)
            i.hover()

        pg.display.flip()
        clock.tick(FPS)

def Restart():
    global elapsed_time
    global full_elapsed_time_lst
    global elapsed_time_lst
    global add
    global question_dict
    global hint_left
    global hint_left_2
    elapsed_time = 0
    full_elapsed_time_lst = []
    elapsed_time_lst = []
    question_dict = full_question_dict
    add = 0
    hint_left = 3
    hint_left_2 = 3
    pg.mixer.music.stop()

def choose_question():
    question = classes.Question(30,100,question_dict)
    return question

def Question_Loop(mode):
    done = False

    global paused
    global elapsed_time
    global elapsed_time_lst
    global hint_minus
    global hint_left
    global model
    global p1_answer
    global question
    global qinfo_list
    hint_minus = 0

    start_time = time.time()
    score.next_q()

    textinput = classes.InputText(15,688,BLACK,arial20)

    if len(question_dict) != 3:
        question = choose_question()
    else:
        GameOver(score.pscore,score.bscore)

    qinfo_list = question_info(question.topic)

    if mode == "bot":
        if check_qtype(question.topic) == True:
            bot_img = question_img(question.topic)
            plst = []
            for i in bot_img:
                image = open_image(i)
                plst.append(str(image_model.predict(image)[0]))
            bot_answer = bot_ans(most_frequent(plst))
        else:
            bot_text = question_txts(question.topic)
            plst = []
            for i in bot_text:
                plst.append(str(text_model.predict(i)[0]))
            bot_answer = most_frequent(plst)
    else:
        turn = classes.Turn(30,180,"Player 1's Turn")

    if sound == "ON":
        if soundchoice == "":
            pass
        elif soundchoice == "Silver Scrapes":
            play_music("Warsongs_SilverScrapes.mp3")
        elif soundchoice == "Piercing Light":
            play_music("Warsongs_PiercingLight.mp3")
        elif soundchoice == "Worlds Collide":
            play_music("Warsongs_WorldsCollide.mp3")
            pg.mixer.music.set_volume(0.5)
        else:
            play_music("Warsongs_TheGlory.mp3")

    while not done:
        screen.blit(gbackground_img,[0,0])

        hint = classes.Hint(930,120,question_dict[question.topic][2],hint_left)
        hint.draw(screen,hint_minus)

        for event in pg.event.get():
            coord = pg.mouse.get_pos()
            if event.type == pg.QUIT:
                done = True
                pg.quit()
                quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if hint.rect.collidepoint(coord) and hint_minus == 0 and hint_left > 0:
                    hint_left -=1
                    hint_minus = 1
                if submit_button.rect.collidepoint(coord):
                    textinput.submit = True
                if textinput.submit == True and next_button.rect.collidepoint(coord):
                    if mode == "bot":
                        question_dict.pop(question.topic)
                        elapsed_time_lst = []
                        elapsed_time = 0
                        Question_Loop(modechoice)
                    else:
                        elapsed_time_lst = []
                        elapsed_time = 0
                        Question_Loop2()
            textinput.handle_event(event)

        if textinput.submit == False:
            timer = classes.Timer(20,20,str(20-int(time.time()-start_time)+elapsed_time))
        else:
            timer = classes.Timer(20,20,0)
        timer.update()
        timer.draw(screen)

        textinput.update(int(timer.time))
        textinput.draw(screen)

        submit_button.drawbutton(screen)

        if mode == "bot":
            check = classes.check_ans(MIDWIDTH,MIDHEIGHT,textinput.text[len(textinput.text)-1],bot_answer,question_dict[question.topic][1],mode)
        else:
            p1_answer = textinput.text[len(textinput.text)-1]
            turn.draw(screen)


        for i in qinfo_list:
            screen.blit(i[0],i[1])

        if textinput.submit == True:
            if mode == "bot":
                check.draw(screen)
                score.update(check.correct,check.correct2)
                if int(timer.time) == 0:
                    next_button.drawbutton(screen)
            else:
                if int(timer.time) == 0:
                    next_button.drawbutton(screen)

        score.draw(screen)
        question.draw(screen)

        p_button.drawbutton(screen)
        p_button.update()
        if p_button.pause == True:
            paused = True
            pg.mixer.music.pause()
            Pause()

        pg.display.flip()
        clock.tick(FPS)

def Question_Loop2():
    done = False

    global paused
    global elapsed_time
    global elapsed_time_lst
    global hint_minus_2
    global hint_left_2
    hint_minus_2 = 0

    start_time = time.time()
    score.next_q()

    textinput = classes.InputText(15,688,BLACK,arial20)

    if len(question_dict) == 3:
        GameOver(score.pscore,score.bscore)

    turn = classes.Turn(30,180,"Player 2's Turn")

    if sound == "ON":
        if soundchoice == "":
            pass
        elif soundchoice == "Silver Scrapes":
            play_music("Warsongs_SilverScrapes.mp3")
        elif soundchoice == "Piercing Light":
            play_music("Warsongs_PiercingLight.mp3")
        elif soundchoice == "Worlds Collide":
            play_music("Warsongs_WorldsCollide.mp3")
            pg.mixer.music.set_volume(0.5)
        else:
            play_music("Warsongs_TheGlory.mp3")

    while not done:
        screen.blit(gbackground_img,[0,0])

        hint = classes.Hint(930,120,question_dict[question.topic][2],hint_left_2)
        hint.draw(screen,hint_minus_2)

        for event in pg.event.get():
            coord = pg.mouse.get_pos()
            if event.type == pg.QUIT:
                done = True
                pg.quit()
                quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if hint.rect.collidepoint(coord) and hint_minus_2 == 0 and hint_left_2 > 0:
                    hint_left_2 -=1
                    hint_minus_2 = 1
                if submit_button.rect.collidepoint(coord):
                    textinput.submit = True
                if textinput.submit == True and next_button.rect.collidepoint(coord):
                    question_dict.pop(question.topic)
                    elapsed_time_lst = []
                    elapsed_time = 0
                    Question_Loop(modechoice)
            textinput.handle_event(event)

        if textinput.submit == False:
            timer = classes.Timer(20,20,str(20-int(time.time()-start_time)+elapsed_time))
        else:
            timer = classes.Timer(20,20,0)
        timer.update()
        timer.draw(screen)

        textinput.update(int(timer.time))
        textinput.draw(screen)

        submit_button.drawbutton(screen)

        check = classes.check_ans(MIDWIDTH,MIDHEIGHT,p1_answer,textinput.text[len(textinput.text)-1],question_dict[question.topic][1],modechoice)
        for i in qinfo_list:
            screen.blit(i[0],i[1])

        if textinput.submit == True:
            check.draw(screen)
            score.update(check.correct,check.correct2)
            if int(timer.time) == 0:
                next_button.drawbutton(screen)

        score.draw(screen)
        turn.draw(screen)
        question.draw(screen)

        p_button.drawbutton(screen)
        p_button.update()
        if p_button.pause == True:
            paused = True
            pg.mixer.music.pause()
            Pause()

        pg.display.flip()
        clock.tick(FPS)

def GameOver(pscore,bscore):
    game_over = True

    while game_over:
        for event in pg.event.get():
            coord = pg.mouse.get_pos()
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                for i in gameover_buttons:
                    if i.rect.collidepoint(coord):
                        if i.function == "Menu":
                            Game_Intro()
                        else:
                            Unpause()
                            Restart()
                            ChooseMode()

        screen.blit(gbackground_img,[0,0])

        title = arial120.render("GAME OVER",True,[0,102,204])
        screen.blit(title,text_centering(title,WIDTH,70,"x"))

        godisplay = classes.GameOver_Display(MIDWIDTH,MIDHEIGHT,pscore,bscore,modechoice)
        godisplay.draw(screen)

        score.draw_gameover(screen)

        for i in gameover_buttons:
            i.drawbutton(screen)
            i.hover()

        pg.display.flip()
        clock.tick(FPS)

def Game_Intro():
    while True:

        screen.blit(gbackground_img,[0,0])
        screen.blit(dog3_img,[20,20])
        screen.blit(dog2_img,[10,310])
        screen.blit(dog1_img,[205,55])
        screen.blit(question_mark_img,[100,340])

        for event in pg.event.get():
            coord = pg.mouse.get_pos()
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                for i in intro_buttons:
                    if i.rect.collidepoint(coord):
                        if i.function == "Start!":
                            Restart()
                            ChooseMode()
                        elif i.function == "Instructions":
                            Instructions()
                        else:
                            Sound_Settings()

        title1 = arial120.render("FIND THE",True,[0,102,204])
        title2 = arial120.render("SIMILARITY!",True,[0,102,204])
        screen.blit(title1,[485,150])
        screen.blit(title2,[400,270])

        for i in intro_buttons:
            i.drawbutton(screen)
            i.hover()

        pg.display.flip()
        clock.tick(FPS)

def Difficulty():
    done = False

    difficultyline = classes.DifficultyLvl(MIDWIDTH,MIDHEIGHT)

    while not done:
        coord = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                for i in difficulty_buttons:
                    if i.rect.collidepoint(coord):
                        if i.function == "Menu":
                            Game_Intro()
                        else:
                            Game_Loop()

        screen.blit(gbackground_img,[0,0])

        title = arial55.render("Make the right choice...",True,[0,102,204])
        screen.blit(title,text_centering(title,WIDTH,100,"x"))

        for i in difficulty_buttons:
            i.drawbutton(screen)
            i.hover()

        difficultyline.draw(screen)
        difficultyline.update()

        global image_model
        global text_model
        if difficultyline.difficulty == "EASY":
            image_model = load_learner(path=r"C:/Users/Razer/Desktop/CEPSTUFF/CEP2020/models/img_easy_model")
            text_model = load_learner(path=r"C:/Users/Razer/Desktop/CEPSTUFF/CEP2020/models/text_easy_model")
        elif difficultyline.difficulty == "MEDIUM":
            image_model = load_learner(path=r"C:/Users/Razer/Desktop/CEPSTUFF/CEP2020/models/img_medium_model")
            text_model  = load_learner(path=r"C:/Users/Razer/Desktop/CEPSTUFF/CEP2020/models/text_medium_model")
        else:
            image_model = load_learner(path=r"C:/Users/Razer/Desktop/CEPSTUFF/CEP2020/models/img_hard_model")
            text_model = load_learner(path=r"C:/Users/Razer/Desktop/CEPSTUFF/CEP2020/models/text_hard_model")

        pg.display.flip()
        clock.tick(FPS)

def ChooseMode():
    done = False

    global modechoice
    pvp = classes.Mode(MIDWIDTH,300,"PVP","pvp")
    bot = classes.Mode(MIDWIDTH,475,"Co-op VS AI","bot")
    while not done:
        coord = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                for i in mode_buttons:
                    if i.rect.collidepoint(coord):
                        if i.function == "Menu":
                            Game_Intro()
                        else:
                            if modechoice == "":
                                pass
                            elif modechoice == "bot":
                                Difficulty()
                            else:
                                Game_Loop()
                if pvp.rect.collidepoint(coord):
                    modechoice = "pvp"
                elif bot.rect.collidepoint(coord):
                    modechoice = "bot"

        screen.blit(gbackground_img,[0,0])

        title = arial55.render("What mode would you like to play?",True,[0,102,204])
        screen.blit(title,text_centering(title,WIDTH,100,"x"))

        for i in difficulty_buttons:
            i.drawbutton(screen)
            i.hover()

        pvp.draw(screen)
        pvp.update(modechoice)
        bot.draw(screen)
        bot.update(modechoice)

        pg.display.flip()
        clock.tick(FPS)

def Game_Loop():
    done = False

    global paused

    global score
    score = classes.Score(MIDWIDTH,30,modechoice)
    full_question_dict = {"felines":["What is common among the pictures? (1 word)",["felines","cats"],"Animal family"],"light":["What do these pictures have in common? (1 word)",["light"],"_i_gh_"],"celebrities":["What do these people have in common? (1 word)",["celebrities","celebrity"],"Famous"],"esports":["What common thing does these pictures show? (1 word)",["esports","gaming"],"Type of sport"],"ballsports":["What is common between these sports? (2 words)",["ball sports","ball sport"],"Equipment"],"wrestling":["What do these pictures show? (1 word)",["wrestling"],"WWE"],"martialarts":["What do these pictures have in common? (1 or 2 words)",["martial arts","fighting","martial art"],"different forms of ___"],"water":["What is common in these pictures? (1 word)",["water"],"made of ___"],"nature":["What is the common theme shown by these pictures? (1 word)",["nature","environment"],"mother ___"],"music":["What do these pictures have in common?",["music"],"form of art"],"cartoon":["What do these characters have in common? (1 word)",["cartoon","animation"],"_____ Network"],"joy":["What emotion do these sentences evoke? (1 word)",["joy","happiness"],"Basic positive emotion"],"disgust":["What kind of emotion do these sentences evoke? (1 word)",["disgust","disgusted"],"Synonym of distaste"],"anger":["What kind of emotions do these sentences evoke? (1 word)",["anger","frustration"],"Strong displeasure"],"shame":["What kind of emotion do these sentences evoke? (1 word)",["shame","ashamed","embarrassment"],"Synonym for disgrace"],"fear":["What kind of emotions do these sentences evoke? (1 word)",["fear","scared"],"Feeling threatened"],"sadness":["What kind of emotion do these sentences evoke? (1 word)",["depression","sadness"],"Basic negative emotion"],"guilt":["What kind of emotion do these sentences evoke? (1 word)",["guilt","regret"],"Synonym of remorse"]}
    global question_dict
    question_dict = full_question_dict

    global p_button
    p_button = classes.PauseButton(965,40)

    while not done:
        screen.fill(BLUE)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
                pg.quit()
                quit()

        Question_Loop(modechoice)

        pg.display.flip()
        clock.tick(FPS)

def Instructions():
    done = False

    mbutton = classes.MenuButton(MIDWIDTH,700,"Menu")

    while not done:
        coord = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if mbutton.rect.collidepoint(coord):
                    Game_Intro()

        screen.blit(gbackground_img,[0,0])
        title = arial120.render("INSTRUCTIONS",True,[0,102,204])
        screen.blit(title,text_centering(title,WIDTH,35,"x"))

        text = arial25.render("The objective of this game is to find the similarity between the images/texts given to you.",True,WHITE)
        text2 = arial25.render("There will be 15 questions for you to answer and you only have 20 seconds to answer them.",True,WHITE)
        text3 = arial25.render("There will be 2 game modes, one being PVP where you take turns with your opponent to answer",True,WHITE)
        text4 = arial25.render("and the other being Co-op vs AI where you compete against the bot.",True,WHITE)
        text5 = arial25.render("To win the game, you have to get more correct answers than your opponent or the bot.",True,WHITE)
        text6 = arial25.render("There will be hints to help you but you can only use a maximum of 3 hints for the 10 questions.",True,WHITE)
        text7 = arial25.render("There will be a scoreboard displayed on the top for you to monitor the scores.",True,WHITE)
        text8 = arial25.render("If you choose the Co-op vs AI mode, you can choose the difficulty of the game when you start.",True,WHITE)
        text9 = arial25.render("A higher difficulty means that the bot is better-trained and hence smarter.",True,WHITE)
        screen.blit(text,[25,205])
        screen.blit(text2,[25,255])
        screen.blit(text3,[25,305])
        screen.blit(text4,[25,335])
        screen.blit(text5,[25,385])
        screen.blit(text6,[25,435])
        screen.blit(text7,[25,485])
        screen.blit(text8,[25,535])
        screen.blit(text9,[25,575])

        mbutton.drawbutton(screen)
        mbutton.hover()

        pg.display.flip()

def Sound_Settings():
    global sound
    global soundchoice

    onoffline = classes.OnOffLine(650,285)

    mbutton = classes.MenuButton(200,700,"Menu")

    while True:
        coord = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if mbutton.rect.collidepoint(coord):
                    Game_Intro()
                for i in sound_buttons:
                    if i.rect.collidepoint(coord):
                        soundchoice = i.choice

        screen.blit(gbackground_img,[0,0])
        title = arial120.render("SOUND SETTINGS",True,[0,102,204])
        screen.blit(title,text_centering(title,WIDTH,35,"x"))
        onoff = arial35.render("Sound Effect",True,WHITE)
        screen.blit(onoff,[75,260])
        mchoice = arial35.render("Select Music Choice",True,WHITE)
        screen.blit(mchoice,[75,345])

        onoffline.update()
        onoffline.draw(screen)

        sound = onoffline.givesound()

        mbutton.drawbutton(screen)
        mbutton.hover()

        for i in sound_buttons:
            i.drawbutton(screen)
            if sound == "ON":
                i.update(soundchoice)

        pg.display.flip()

#RUN GAME
Game_Intro()
