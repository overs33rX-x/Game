
import os.path
import time
import pygame as p

jump = False
quit = False
width = 1400
height = 787
fps = 30 #если поставить ниже, то плавности почти не будет
p.init() 
p.mixer.init()  

screen = p.display.set_mode((width, height))  
p.display.set_caption("ИГРА")
clock = p.time.Clock()

f_game = os.path.dirname(__file__)  # автоопределения корневой папки игры
f_image = os.path.join(f_game, R'C:\Users\Fedor\Desktop\game\Game\image')  # определяем путь до папки с изображениями
f_music = os.path.join(f_game, R'C:\Users\Fedor\Desktop\game\Game\music')  # определяем путь до папки с музыкой

p.mixer.music.load(os.path.join(f_music, 'заставка.mp3'))
p.mixer.music.play()  #проигрывание загруженной мелодии

# convert() - автоконвертация в оптимальное расширение
begin_screen = p.image.load(os.path.join(f_image, 'menu.png'))
buttons = p.image.load(os.path.join(f_image, 'buttons.png'))
knight_left = p.image.load(os.path.join(f_image, 'knight_left.png'))
knight_right = p.image.load(os.path.join(f_image, 'knight_right.png'))

healthbar = p.image.load(os.path.join(f_image, 'healthbar.png'))
bg = p.image.load(os.path.join(f_image, "background.png"))
knight_run_r1 = p.image.load(os.path.join(f_image, "run1_knight_r.png"))
knight_run_r2 = p.image.load(os.path.join(f_image, "run2_knight_r.png"))

knight_run_l1 = p.image.load(os.path.join(f_image, 'run1_knight_l.png'))
knight_run_l2 = p.image.load(os.path.join(f_image, 'run2_knight_l.png'))

knight_standr = p.image.load(os.path.join(f_image, "stand_knight_r.png"))
knight_standl = p.image.load(os.path.join(f_image, "stand_knight_l.png"))

run_right = (knight_run_r1, knight_run_r2)
run_left = (knight_run_l1, knight_run_l2)
stand = (knight_standr, knight_standl)

class LineHealth(p.sprite.Sprite):
    
    def __init__(self):
        p.sprite.Sprite.__init__(self)  
        
        self.image = healthbar
        self.rect = self.image.get_rect()
        self.rect.x = -25
        self.rect.y = height - 820

class User(p.sprite.Sprite):
    
    def __init__(self):
        p.sprite.Sprite.__init__(self)
        self.image = knight_standr
        self.direct = 1
        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.y = height - 205
        self.time = 0
        self.dir = 'right'
        self.f_jump = False  # флаг для прыжка изначально погашен
        self.h = 40  # максимальная высота прыжка
        self.power = 200
        self.loop = 0
        self.f_hit = False

    def update(self):
        global move_bg
        # if self.power < 0:
        #     self.fall()
        #     return
        self.time += 1
        self.speedx = 0
        self.speedy = 0
        keypush = p.key.get_pressed()
        
        if keypush[p.K_d]:
            self.speedx = 6
            self.image = run_right[move_bg % 2]
            if move_bg >= -642:
                move_bg -= 3
            self.dir = 'right'

        if keypush[p.K_a]:
            self.speedx = -6
            self.image = run_left[move_bg % 2]
            if move_bg <= 0:
                move_bg += 3
            self.dir = 'left'

        if keypush[p.K_w]:
            self.f_jump = True  # меняем флаг прыжка
        if self.f_jump:
            self.jump()
        
        if not (keypush[p.K_d] or keypush[p.K_a]):
            if self.dir == 'right':
                self.image = stand[0]
            elif self.dir == 'left':
                self.image = stand[1]

        if not keypush[p.K_s]:
            if self.f_hit:
                self.rect.x += 20
            self.f_hit = False
        
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.right > width:
            self.rect.right = width
        if self.rect.left < 0:
            self.rect.left = 0

        self.power -= 1
        #print(self.power)

    def jump(self):
        if self.h >= -40:
            self.rect.y -= self.h
            self.h -= 5
        else:
            self.f_jump = False
            self.h = 40
   
   
   
class Settings:
    loop = 0
    t0 = time.time()
    level = 1

    def __init__(self):
        pass

    @staticmethod
    def any_key():
        global quit
        for e in p.event.get():
            if e.type == p.KEYDOWN:
                quit = True
                p.quit()

groupUser = p.sprite.Group() 
user1 = User()
groupUser.add(user1)  

groupEnemy = p.sprite.Group() 
groupAxe = p.sprite.Group()

groupHealth = p.sprite.Group()
hbar = LineHealth()
groupHealth.add(hbar)         
            
            
gameloop = True  
x = True
f_begin = True 
is_jumping = False
move_bg = 0

while gameloop:

    screen.blit(bg, (move_bg, 0))
    
    while f_begin:
        screen.blit(begin_screen, [0, 0])
        screen.blit(buttons, [-150, 400])
        p.display.flip() 
        for event in p.event.get():  
            if event.type == p.MOUSEBUTTONDOWN: 
                x, y = event.pos
                print(x, y)
                if 63 < x < 236 and 471 < y < 505:
                    f_begin = False
                elif 195 < x < 306 and 222 < y < 249:
                    pass
                elif 63 < x < 236 and 684 < y < 727:
                    f_begin = False
                    gameloop = False

    groupUser.update()
    groupUser.draw(screen)
    groupHealth.update()
    groupHealth.draw(screen)
    
    p.display.flip()  

    for event in p.event.get():
        if event.type == p.QUIT: 
            gameloop = False
            quit = True

    clock.tick(fps)

while not quit:
    for event in p.event.get():
        if event.type == p.QUIT:
            quit = True
        Settings.any_key()