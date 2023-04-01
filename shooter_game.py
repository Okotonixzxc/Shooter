from pygame import *
from random import *

class GameSprite(sprite.Sprite):
    def __init__(self, coord_x, coord_y, player_speed, width, height, player_image):
        sprite.Sprite.__init__(self)
        self.speed = player_speed
        self.image = transform.scale(image.load(player_image), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = coord_x
        self.rect.y = coord_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top, 15, 20, 15, 'bullet.png')
        bullets.add(bullet)
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 720:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < 500:
            self.rect.y += self.speed
        
class Enemy (GameSprite):
    def update(self):
        self.rect.y += self.speed 
        #self.rect.x += randint(-30, 30)
        global lost
        if self.rect.y > 575:
            self.rect.y = randint(-30, 0)
            self.rect.x = randint(30, 700)
            lost += 1
        
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

window = display.set_mode((800,600))
display.set_caption('Руслан')
background = transform.scale(image.load('galaxy.jpg'), (800,600))

clock = time.Clock()
game = True
lost = 0
kills = 0 
lives = 3

ship = Player(315, 500, 10, 80, 100, 'rocket.png')

font.init()
font1 = font.SysFont('Times New Roman', 36)

monsters = sprite.Group()
for i in range(5):
    monster = Enemy(randint(30, 670), randint(-30, 0), randint(5, 10), 80, 50, 'ufo.png')
    monsters.add(monster)

bullets = sprite.Group()

while game:
    for ev in event.get():
        if ev.type == QUIT:
            game = False

        if ev.type == KEYDOWN:
            if ev.key == K_SPACE:
                ship.shoot()
    
    window.blit(background, (0,0))
    ship.reset()
    ship.update()

    
    text_lost = font1.render('Пропущено:' + str(lost), 1, (255,255,255))
    window.blit(text_lost, (10,50))

    text_kills = font1.render('Сбито:' + str(kills), 1, (255,255,255))
    window.blit(text_kills, (10,90))

    text_lives = font1.render('Жизни:' + str(lives), 1, (255,255,255))
    window.blit(text_lives, (10,130))

    if sprite.spritecollide(ship, monsters, True):
        lives -= 1

    if lives == 0:
        game = False

    collides = sprite.groupcollide(monsters, bullets, True, True)
    for c in collides:
        kills += 1
        monster = Enemy(randint(30,770), randint(-30, 0), randint(5, 10), 80, 50, 'ufo.png')
        monsters.add(monster)
    
    ship.update()
    monsters.update()
    bullets.update()

    monsters.draw(window)
    bullets.draw(window)


    display.update()
    time.delay(50)