from pygame import *
import random
from time import time as tm 

window = display.set_mode((1000,500))
display.set_caption("Шутер")
#создай окно игры
background = transform.scale(image.load('fon.png'), (1000,500))
#задай фон сцены
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y,player_speed,w,h):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(w,h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))


class Player(GameSprite):
    def wasd(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= 5
        if keys_pressed[K_d] and self.rect.x < 930:
            self.rect.x += 5
    def fire(self):
        bullet = Shaiba('shaiba.png',self.rect.centerx,self.rect.top,20,10,10)
        shaiba_group.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 450:
            global missed
            missed += 1
            self.rect.y = -50
            self.rect.x = random.randint(0,920)
class Shaiba(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
class Enemy2(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 450:
            self.rect.y = -50
            self.rect.x = random.randint(0,950)

font.init()
mixer.init()
game_font = font.Font(None,36)
font_2 = font.Font(None,150)
win_text = game_font.render('YOU WIN!!!',True,(0,250,0))
lose_text = game_font.render('YOU LOSE!',True,(250,0,0))


shaiba_group = sprite.Group()
referys_group = sprite.Group()
for i in range(3):
    referi = Enemy2('referi.png',random.randint(0,950),-50,random.randint(1,3,),50,90)
    referys_group.add(referi)
player = Player('hockeist.png',500,430,2,60,70)
monsters = sprite.Group()
for i in range(5):
    enemy = Enemy('vorota.png',random.randint(0,920),-50,random.randint(1,3),80,45)
    monsters.add(enemy)

mixer.init()
mixer.music.load('space.ogg')
fire_sound = mixer.Sound('fire.ogg')
mixer.music.set_volume(0.2)
mixer.music.play()

clock = time.Clock()
FPS = 60
killed = 0
missed = 0
game = True 
finish = False
rel_time = False
num_fire = 0
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire <= 5 and rel_time == False:
                    player.fire()
                    fire_sound.play()
                    num_fire += 1
                if num_fire > 5 and rel_time == False:
                    rel_time = True
                    start = tm()

    if finish != True:
        window.blit(background,(0,0))
        player.wasd()
        player.reset()
        referys_group.update()
        referys_group.draw(window)
        monsters.update()
        monsters.draw(window)
        shaiba_group.update()
        shaiba_group.draw(window)
        for shaiba in shaiba_group:
            hit_enemies=sprite.spritecollide(shaiba,monsters,False)
            if hit_enemies:
                killed += 1
                shaiba.kill()
                for enemy in hit_enemies:
                    enemy.rect.y = -50
                    enemy.rect.x = random.randint(0,920)
        score_text = game_font.render('Счет:'+str(killed),True,(0,0,0))
        missed_text = game_font.render('Пропущено:'+str(missed),True,(0,0,0))
        window.blit(missed_text,(10,30))
        window.blit(score_text,(10,10))
        if missed >= 3 or sprite.spritecollide(player, monsters,False) or sprite.spritecollide(player,referys_group,False):
            finish = True
            lose_text = font_2.render('You lose!',True,(255,0,0))
            window.blit(lose_text,(300,200))
        if killed >= 10:
            finish = True
            win_text = font_2.render('You WIN!',True,(0,255,0))
            window.blit(win_text,(300,300))
        if rel_time == True:
            new_time = tm()
            if new_time - start < 3:
                reload_text = game_font.render('отдыхаем..',True,(255,0,0))
                window.blit(reload_text,(350,450))
            else:
                num_fire = 0
                rel_time = False
    
    display.update()
    clock.tick(FPS)