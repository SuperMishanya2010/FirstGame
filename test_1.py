import pygame
import random
import time
import sqlite3


from os import path
pygame.init()


class Player:
    def __init__(self, x,y, size, img):
        self.x =x 
        self.y =y 
        self.size = size
        self.img = img


    def _draw_(self, sc, H):
        sc.blit(self.img, (self.x,self.y ))


    def _move_right_(self):
            self.x += 5
    def _move_left_(self):
            self.x -= 5
    def _move_up_(self):
            self.y-=1
    def _move_down_(self):
            self.y+=1
    def _rotate_(self):
        self.img = pygame.transform.rotate(self.img, 2)


    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
                self._move_left_()
        if keys[pygame.K_RIGHT]:
                self._move_right_()


class Enemy:
    def __init__(self, x,img, damage, size,rev):
        self.x = x 
        self.img=img
        self.damage = damage
        self.size = size
        self.rev = rev


    def draw(self, sc, H):
        sc.blit(self.img, (self.x,H-self.size ))


    def move(self,W):
            if self.rev==0:
                if self.x==0:
                    self.x=W
                self.x +=-1
            if self.rev==1 or self.rev==-1:
                if self.x==0:
                    self.rev=-1
                if self.x+self.size==W:
                    self.rev=1
                if self.rev==-1:
                    self.x+=1
                if self.rev==1:
                    self.x-=1


    def live(self):
        self._move_()
        self._draw_()


W = 1250 # width - ширина
H = 700 # height - высота


x = W // 2
y = H // 2


path_file = path.dirname(__file__)
fps = pygame.time.Clock()
gamer = str(input('Назовись:'))


music = pygame.mixer.music.load( path_file + '/' +'zigota.mp3')
pygame.mixer.music.play(-1, 0.0)


sc = pygame.display.set_mode((W, H))
pygame.display.set_caption("Игра")
img = pygame.image.load(path_file + '/' + 'dan.jpg')
img1 = pygame.image.load(path_file + '/' + 'krol.png')
img2= pygame.image.load(path_file + '/' + 'dedd.jpg')
img3= pygame.image.load(path_file + '/' + 'game_over.png')


connect = sqlite3.connect('players.db')
cursor = connect.cursor()
#cursor.execute('CREATE TABLE players(name TEXT,score INT)')
#cursor.execute("INSERT INTO players VALUES('Abf', 0)")


Black_E=Enemy(W, img , 20, 85, 0)
Red_E=Enemy(W,img1,10,85,1)
Pl=Player(500,H-100,95,img2)
print(H-Red_E.size)

def score(gamer , time):
    cursor.execute(f"INSERT INTO players VALUES('{gamer}',{time})")
    cursor.execute('''SELECT * FROM players''')
    data_from_db = cursor.fetchall()
    connect.commit()

    return(max(data_from_db, key=lambda x: x[1])[0] + ' ' + str(max(data_from_db, key=lambda x: x[1])[1]))


def hit(Enemy,Player):
    if Player.y+Player.size>H-Enemy.size and Player.x+Player.size>Enemy.x and Player.x<Enemy.x+Enemy.size:
        sc.blit(img3,(W/2-435,100 ))

        music = pygame.mixer.music.load(path_file + '/' + 'orrr.mp3')
        pygame.mixer.music.play(-1, 0.0)

        font = pygame.font.Font(None, 50)
        r = pygame.time.get_ticks()/1000
        strin="Ваше время: " + str(r)+ ' секунды'
        strin_1="Рекорд: " + score(gamer,r) + ' секунды'
        text = font.render(strin,True,[0,0,0])
        text_1 = font.render(strin_1,True,[0,0,0])
        sc.blit(text, [450,H-95])
        sc.blit(text_1, [450,H-57])

        pygame.display.update()
        time.sleep(4)
        exit()


def draw():
    sc.fill((255, 255, 255))
    Black_E.draw(sc,H)
    Red_E.draw(sc,H)
    Pl._draw_(sc,H)
    pygame.display.update()


jump = pygame.mixer.Sound(path_file + '/' + 'jump.wav')

j = 0
r = 0
nn = 0

while True:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        if j != 1:
            jump.play()
            j = 1
    if j == 1:
        Pl.y -= 5-r//10
        r += 1
    if r == 110:
        j = 0
        r = 0

    Pl.move()
    draw()
    Red_E.move(W)
    if nn>1000:
        Black_E.move(W)
    hit(Black_E,Pl)
    hit(Red_E,Pl)

    #connect.commit()

    fps.tick(120)

connect.commit()
connect.close()