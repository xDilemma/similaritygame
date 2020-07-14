import pygame as pg
import sys
from os import path
import random
from fastai.vision import *
from fastai.metrics import error_rate
from fastai.text import *

pg.init()

#Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0,0,255)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)
mb_colour = (204,153,255)
mb_colour2 = (178,102,255)

#Fonts
arial20 = pg.font.SysFont('Arial', 20, True, False)
arial25 = pg.font.SysFont('Arial', 25, True, False)
arial55 = pg.font.SysFont('Arial', 55, True, False)
arial35 = pg.font.SysFont('Arial', 35, True, False)
arial120 = pg.font.SysFont('Arial', 120, True, False)

#Game Settings
clock = pg.time.Clock()
WIDTH =  1000
HEIGHT = 800
MIDWIDTH = 500
MIDHEIGHT = 400
FPS = 120
screen = pg.display.set_mode((WIDTH,HEIGHT))

#Files
game_folder = path.dirname(__file__)
assets_folder = path.join(game_folder, 'assets')
felines_folder = path.join(game_folder, 'felines')
water_folder = path.join(game_folder, 'water')
ballsports_folder = path.join(game_folder, 'ballsports')
esports_folder = path.join(game_folder, 'esports')
nature_folder = path.join(game_folder, 'nature')
martialarts_folder = path.join(game_folder, 'martialarts')
wrestling_folder = path.join(game_folder, 'wrestling')
light_folder = path.join(game_folder, 'light')
music_folder = path.join(game_folder, 'music')
celebrities_folder = path.join(game_folder, 'celebrities')
cartoon_folder = path.join(game_folder,'cartoon')
models_folder = path.join(game_folder,'models')

#Text Questions
joy = ["When I finally recovered from the virus","When my idol recognised me","I bought a huge piece of land","I got married to the love of my life","When I saw the smiles on my parents"]
disgust = ["The toilet was full of dump","The room was filled with spider webs and dust","When I saw a naked person","I saw a dead body with the head gone ","When I knew my friend did not shower for weeks"]
anger = ["The judge was biased against me","I had to do his task while he was slacking","When I get punished for no reason","Shut up, you annoying basket","Don't piss me off."]
fear = ["I was surrounded by tall and big men","I was alone in the jungle","I screamed in my nightmare","Get me out!!","My teacher stared and walked towards me"]
shame = ["I accidentally walked into the wrong restroom","I got scolded out in public","My younger brother scored higher than me","I got called out in front of the whole school","I was the only fat guy in class"]
sadness = ["My friend broke my most precious things","When my best friend ignored me","When my girlfriend and I broke up during our anniversary","My pet died","Life sucks so much","I became handicapped after an accident"]
guilt = ["I got caught watching dirty videos","When I did not admit my mistake","I knocked a person down due to reckless driving","Do you even have a conscience?","I lost my friend's wallet"]

#Convenient functions
def text_centering(text,x,y,type):
    textrect = text.get_rect()
    if type == "both":
        textrect.centerx = x//2
        textrect.centery = y//2
    elif type == "x":
        textrect.centerx = x//2
        textrect.y = y
    elif type == "y":
        textrect.x = x
        textrect.centery = y//2
    else:
        pass
    return textrect

def scaling_images(x,y,img_name,filename,angle):
    image = pg.transform.rotate(pg.image.load(path.join(filename, img_name)).convert_alpha(),angle)
    image = pg.transform.scale(image, (x, y))
    return image

def most_frequent(List):
    counter = 0
    num = List[0]

    for i in List:
        curr_frequency = List.count(i)
        if(curr_frequency> counter):
            counter = curr_frequency
            num = i

    return num

def bot_ans(ans):
    if ans == "martialarts":
        return "martial arts"
    elif ans == "ballsports":
        return "ball sports"
    elif ans == "cartoons":
        return "cartoon"
    else:
        return ans

def question_img(topic):
    if topic == "felines":
        filename = felines_folder
    elif topic == "light":
        filename = light_folder
    elif topic == "celebrities":
        filename = celebrities_folder
    elif topic == "wrestling":
        filename = wrestling_folder
    elif topic == "martialarts":
        filename = martialarts_folder
    elif topic == "water":
        filename =water_folder
    elif topic == "ballsports":
        filename = ballsports_folder
    elif topic == "esports":
        filename = esports_folder
    elif topic == "music":
        filename = music_folder
    elif topic == "nature":
        filename = nature_folder
    elif topic == "cartoon":
        filename = cartoon_folder
    image1 = path.join(filename,"1.jpg")
    image2 = path.join(filename,"2.jpg")
    image3 = path.join(filename,"3.jpg")
    image4 = path.join(filename,"4.jpg")
    image5 = path.join(filename,"5.jpg")
    image6 = path.join(filename,"6.jpg")
    image7 = path.join(filename,"7.jpg")
    image8 = path.join(filename,"8.jpg")
    lst =[path.join(filename,"1.jpg"),path.join(filename,"2.jpg"),path.join(filename,"3.jpg"),path.join(filename,"4.jpg"),
    path.join(filename,"5.jpg"),path.join(filename,"6.jpg"),path.join(filename,"7.jpg"),path.join(filename,"8.jpg")]
    flst =[]
    for i in range(5):
        a = random.choice(lst)
        flst.append(a)
        lst.remove(a)
    return flst

def question_images(filename,lst):
    alst = []
    slst = []
    for i in lst:
        alst.append(i[-5:])
    for i in alst:
        image = scaling_images(250,215,str(i),filename,0)
        slst.append(image)
    flst = []
    hlst1 = []
    hlst2 = []
    for i in range(3):
        hlst1.append([slst[i],[30+i*340,210]])
    for i in range(2):
        hlst2.append([slst[i+3],[195+i*375,440]])
    for i in hlst1:
        flst.append(i)
    for i in hlst2:
        flst.append(i)
    return flst

def question_texts(topic):
    lst = []
    if topic == "joy":
        for i in range(5):
            surface = pg.Surface((750,50))
            key = arial25.render(str(i+1) + ". " +joy[i],True,WHITE)
            surface.blit(key,text_centering(key,10,50,"y"))
            lst.append([surface,[150,210+i*100]])
    if topic == "disgust":
        for i in range(5):
            surface = pg.Surface((750,50))
            key = arial25.render(str(i+1) + ". " +disgust[i],True,WHITE)
            surface.blit(key,text_centering(key,10,50,"y"))
            lst.append([surface,[150,210+i*100]])
    if topic == "anger":
        for i in range(5):
            surface = pg.Surface((750,50))
            key = arial25.render(str(i+1) + ". " +anger[i],True,WHITE)
            surface.blit(key,text_centering(key,10,50,"y"))
            lst.append([surface,[150,210+i*100]])
    if topic == "fear":
        for i in range(5):
            surface = pg.Surface((750,50))
            key = arial25.render(str(i+1) + ". " +fear[i],True,WHITE)
            surface.blit(key,text_centering(key,10,50,"y"))
            lst.append([surface,[150,210+i*100]])
    if topic == "sadness":
        for i in range(5):
            surface = pg.Surface((750,50))
            key = arial25.render(str(i+1) + ". " +sadness[i],True,WHITE)
            surface.blit(key,text_centering(key,10,50,"y"))
            lst.append([surface,[150,210+i*100]])
    if topic == "shame":
        for i in range(5):
            surface = pg.Surface((750,50))
            key = arial25.render(str(i+1) + ". " +shame[i],True,WHITE)
            surface.blit(key,text_centering(key,10,50,"y"))
            lst.append([surface,[150,210+i*100]])
    if topic == "guilt":
        for i in range(5):
            surface = pg.Surface((750,50))
            key = arial25.render(str(i+1) + ". " +guilt[i],True,WHITE)
            surface.blit(key,text_centering(key,10,50,"y"))
            lst.append([surface,[150,210+i*100]])
    return lst

def question_txts(topic):
    lst = []
    if topic == "joy":
        lst = joy
    if topic == "disgust":
        lst = disgust
    if topic == "anger":
        lst = anger
    if topic == "fear":
        lst = fear
    if topic == "sadness":
        lst = sadness
    if topic == "shame":
        lst = shame
    if topic == "guilt":
        lst = guilt
    return lst

def question_info(topic):
    lst = []
    if topic == "felines":
        lst = question_images(felines_folder,question_img(topic))
    elif topic == "light":
        lst = question_images(light_folder,question_img(topic))
    elif topic == "celebrities":
        lst = question_images(celebrities_folder,question_img(topic))
    elif topic == "wrestling":
        lst = question_images(wrestling_folder,question_img(topic))
    elif topic == "martialarts":
        lst = question_images(martialarts_folder,question_img(topic))
    elif topic == "water":
        lst = question_images(water_folder,question_img(topic))
    elif topic == "ballsports":
        lst = question_images(ballsports_folder,question_img(topic))
    elif topic == "esports":
        lst = question_images(esports_folder,question_img(topic))
    elif topic == "music":
        lst = question_images(music_folder,question_img(topic))
    elif topic == "nature":
        lst = question_images(nature_folder,question_img(topic))
    elif topic == "cartoon":
        lst = question_images(cartoon_folder,question_img(topic))
    else:
        lst = question_texts(topic)
    return lst

def check_qtype(topic):
    if topic == "felines":
        type = True
    elif topic == "light":
        type = True
    elif topic == "celebrities":
        type = True
    elif topic == "wrestling":
        type = True
    elif topic == "martialarts":
        type = True
    elif topic == "water":
        type = True
    elif topic == "ballsports":
        type = True
    elif topic == "esports":
        type = True
    elif topic == "music":
        type = True
    elif topic == "nature":
        type = True
    elif topic == "cartoon":
        type = True
    else:
        type = False
    return type

def play_music(sound_name):
    pg.mixer.music.load(path.join(assets_folder,sound_name))
    pg.mixer.music.set_volume(0.5)
    pg.mixer.music.play()
    pg.mixer.music.rewind()
#Images
tick_img = scaling_images(70,80,"tick.png",assets_folder,-5) 
cross_img = scaling_images(70,80,"cross.png",assets_folder,-5) 
hint_img = scaling_images(50,50,"hint.png",assets_folder,5)
gbackground_img = scaling_images(WIDTH,HEIGHT,"black-background-hd.jpg",assets_folder,0)
dog1_img = scaling_images(200,400,"dog.jpg",assets_folder,-8)
dog2_img = scaling_images(190,320,"dog2.jpg",assets_folder,5)
dog3_img = scaling_images(200,300,"dog3.jpg",assets_folder,5)
question_mark_img = scaling_images(350,500,"questionmark.png",assets_folder,0)

#Game Variables
full_question_dict = {"felines":["What is common among the pictures? (1 word)",["felines","cats"],"Animal family"],"light":["What do these pictures have in common? (1 word)",["light"],"_i_gh_"],"celebrities":["What do these people have in common? (1 word)",["celebrities","celebrity"],"Famous"],"esports":["What common thing does these pictures show? (1 word)",["esports","gaming"],"Type of sport"],"ballsports":["What is common between these sports? (2 words)",["ball sports","ball sport"],"Equipment"],"wrestling":["What do these pictures show? (1 word)",["wrestling"],"WWE"],"martialarts":["What do these pictures have in common? (1 or 2 words)",["martial arts","fighting","martial art"],"different forms of ___"],"water":["What is common in these pictures? (1 word)",["water"],"made of ___"],"nature":["What is the common theme shown by these pictures? (1 word)",["nature","environment"],"mother ___"],"music":["What do these pictures have in common?",["music"],"form of art"],"cartoon":["What do these characters have in common? (1 word)",["cartoon","animation"],"_____ Network"],"joy":["What emotion do these sentences evoke? (1 word)",["joy","happiness"],"Basic positive emotion"],"disgust":["What kind of emotion do these sentences evoke? (1 word)",["disgust","disgusted"],"Synonym of distaste"],"anger":["What kind of emotions do these sentences evoke? (1 word)",["anger","frustration"],"Strong displeasure"],"shame":["What kind of emotion do these sentences evoke? (1 word)",["shame","ashamed","embarrassment"],"Synonym for disgrace"],"fear":["What kind of emotions do these sentences evoke? (1 word)",["fear","scared"],"Feeling threatened"],"sadness":["What kind of emotion do these sentences evoke? (1 word)",["depression","sadness"],"Basic negative emotion"],"guilt":["What kind of emotion do these sentences evoke? (1 word)",["guilt","regret"],"Synonym of remorse"]}
paused = False
elapsed_time = 0
elapsed_time_lst = []
full_elapsed_time_lst = []
p_time = 0
add = 0
add_score = 0
add_bscore =0
modechoice = ""
hint_left = 0
hint_minus = 0
hint_left_2 = 0
hint_minus_2 = 0
sound = ""
soundchoice = ""
