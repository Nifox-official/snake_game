from pygame import *
from random import choice, randint

window=display.set_mode((700,500))
display.set_caption('Snake')

class GameSprite(sprite.Sprite):
    def __init__(self, img, x,y, w,h):
        super().__init__()
        self.image = transform.scale(image.load(img),(w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))
    def collidepoint(self,x,y):
        return self.rect.collidepoint(x,y)


class Snake(GameSprite):
    def __init__(self,img,x,y,w,h,t):
        super().__init__(img,x,y,w,h)
        self.type=t
        self.speed=25
        self.direction='0'
        self.cur_image=self.image
        self.wait = 10
    def update(self):
        if self.direction == 'l':
            self.rect.x -= self.speed
        elif self.direction == 'r':
            self.rect.x += self.speed
        elif self.direction == 'u':
            self.rect.y -= self.speed
        elif self.direction == 'd':
            self.rect.y += self.speed
    def get_direction(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.direction != 'r':
            self.direction = 'l'
            self.image = transform.rotate(self.cur_image, -90)
        if keys[K_RIGHT] and self.direction != 'l':
            self.direction = 'r'
            self.image = transform.rotate(self.cur_image, 90)
        if keys[K_UP] and self.direction != 'd':
            self.direction = 'u'
            self.image = transform.rotate(self.cur_image, 180)
        if keys[K_DOWN] and self.direction != 'u':
            self.direction = 'd'
            self.image = transform.rotate(self.cur_image, 0)

    def eat(self,food):
        global speed
        speed+=1
        food.position()

    def set_direct(self):
        if self.direction == 'l': 
            self.image = transform.rotate(self.cur_image, -90)
        if self.direction == 'r':
            self.image = transform.rotate(self.cur_image, 90)
        if self.direction == 'u':
            self.image = transform.rotate(self.cur_image, 180)
        if self.direction == 'd':
            self.image = transform.rotate(self.cur_image, 0)

class Food(GameSprite):
    def __init__(self,imgs,x,y,w,h):
        super().__init__(imgs[0],x,y,w,h)
        self.costumes = []
        self.costumes.append(self.image)
        for i in range(len(imgs)-1):
            self.image=transform.scale(image.load(imgs[i+1]),(w,h))
            self.costumes.append(self.image)

    def set_costume(self,n):
        self.image=self.costumes[n]

    def rand_costumes(self):
        self.image = choice(self.costumes)

    def position(self):
        self.rect.x=int(randint(0,700-self.rect.width)/25)*25
        self.rect.y=int(randint(0,500-self.rect.width)/25)*25
        self.rand_costumes()        

clock = time.Clock()
FPS=60
head=Snake('snake.png',350,250,25,25,0)
speed=1
food=Food(['apple.png','arbuz.png','orange.png'], -100,-100,25,25)
tail=Snake('tail.png', 350,275,25,25,0)
title=GameSprite('title.png', 200,100,300,200)
btn_play=GameSprite('btn_play.png', 250,300,200,100)
title_lose=GameSprite('lose.png', 200,100,300,200)
snake=[head,tail]
food.position()
game=True
menu=True
finish=True
lose=False
global_wait=0
font.init()
font1=font.SysFont('Arial',30)
score=0

while game:
    for e in event.get():
            if e.type == QUIT:
                game = False
    window.fill((0,102,160))
    if menu == True:
        title.reset()
        btn_play.reset()
        pressed = mouse.get_pressed()
        pos=mouse.get_pos()
        if pressed[0]:
            if btn_play.rect.collidepoint(pos[0],pos[1]):
                menu=False
                finish=False

    if finish==False:      
        head.get_direction()
        if global_wait==0:
            global_wait=head.wait
            for e in range(len(snake)-1,0,-1):
                snake[e].direction=snake[e-1].direction
                snake[e].set_direct()
                snake[e].rect.x=snake[e-1].rect.x
                snake[e].rect.y=snake[e-1].rect.y
            head.update()
        else:
            global_wait-=1
        head.reset()
        food.reset()
        
        for s in snake:
            s.reset()
        if head.rect.colliderect(food):
            head.eat(food)
            s=Snake('tail.png', head.rect.x, head.rect.y,25,25,0)
            snake.insert(1,s)
            if speed %5==0:
                head.wait-=2
            if head.wait<10:
                head.wait=10

        if head.rect.x <0:
            head.rect.x=700

        if head.rect.x >700:
            head.rect.x=0

        if head.rect.y <0:
            head.rect.y=500

        if head.rect.y >500:
            head.rect.y=0

        if speed>1:
            for i in range(2,len(snake)):
                if head.rect.colliderect(snake[i]):
                    lose=True
                    finish=True
                    print(i)


    if lose==True:
        title_lose.reset()



        score_text=font1.render('Счёт: '+str(speed),1,(0,0,0))
        window.blit(score_text,(10,10))
    display.update()
    clock.tick(FPS)