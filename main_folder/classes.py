import sys
import time
import pygame as pg
from time import time
from constns import *


class Animation:
    def __init__(self, images, duration):
        # images - кадры в анимации, duration - длительность одного кадра анимации
        self.images = images
        self.duration = duration
        self.timer = 0
        self.max_index = len(self.images) - 1
        self.index = 0

    def next(self):
        # функция возвращает следующий кадр анимации
        if time() - self.timer >= self.duration:
            self.index += 1
            self.timer = time()
            if self.index > self.max_index:
                self.index = 0
        return self.images[self.index]

    def clear(self):
        self.index = 0
        self.timer = time()


class Bullet:
    def __init__(self, x, y, animations, damage, player, mob_list, bullet_list, enemy=False, rotation_right=True):
        # damage - урон от попадания пули, rotation_right - пуля выпущена вправо (True -> вправо)
        # enemy - враг выпустил эту пулю, или игрок (True -> враг)
        self.x, self.y = x, y
        self.animations = animations
        self.rotation_right = rotation_right
        self.damage = damage
        self.enemy = enemy
        self.mob_list = mob_list
        self.player = player
        self.bullet_list = bullet_list

    def update(self, delta):
        if self.rotation_right:
            self.x += 12 * delta * DELTA_MOD
        else:
            self.x -= 12 * delta * DELTA_MOD
        if self.x >= WIDTH * 2 or self.x <= 0:
            pass
        else:
            if not self.enemy:
                for mob in self.mob_list:
                    if (mob.x >= self.x and abs(self.x - mob.x) <= 40) or \
                            (mob.x <= self.x and abs(self.x - (mob.x + 85)) <= 40):
                        mob.hp -= min(self.damage, mob.hp)
                        if mob.hp <= 0:
                            self.mob_list.remove(mob)
                        self.bullet_list.remove(self)
                        break
            else:
                pass

    def render(self, screen, camera):
        screen.blit(self.animations[0].next(), (self.x - camera.x, real_y(self.y, 90)))


class Mob:
    def __init__(self, x, y, animations, player, mob_list, bullet_list, images, max_hp=5, cooldown=5, damage=1):
        self.x, self.y = x, y
        self.sx, self.sy = x, y
        self.images = images
        self.speed_y = 0
        self.animations = animations
        self.rotation_right = False
        self.task = TASK_STAY
        self.freeze_timer = 0
        self.player = player
        self.mob_list = mob_list
        self.hp = self.max_hp = max_hp
        self.bullet_list = bullet_list
        self.cooldown = cooldown
        self.shoot_timer = 0
        self.damage = damage

    def init(self):
        # сброс состояния моба (или игрока)
        for animation in self.animations:
            animation.clear()
        self.speed_y = 0
        self.rotation_right = False
        self.task = TASK_STAY
        self.freeze_timer = time()
        self.hp = self.max_hp
        self.x, self.y = self.sx, self.sy

    def set_task(self, task):
        if not self.freeze():
            self.task = task

    def landed(self):
        return self.y == LAND_POINT_Y

    def freeze(self):
        return time() - self.freeze_timer <= 1

    def hit(self):
        self.task = TASK_HIT
        self.freeze_timer = time()
        self.player.hp -= self.damage

    def update(self, delta):
        # обработка логики моба
        if not self.freeze():
            if self.player.x >= self.x:
                self.rotation_right = True
            else:
                self.rotation_right = False
            if self.rotation_right:
                self.x += 2 * delta * DELTA_MOD
            else:
                self.x -= 2 * delta * DELTA_MOD
            self.task = TASK_GO
            if ((self.player.x >= self.x and self.rotation_right and abs(self.x + 20 - self.player.x) <= 40) or (self.player.x <= self.x and not self.rotation_right and abs(self.x - self.player.x - 40) <= 40)) and \
                    self.player.y <= LAND_POINT_Y + 80:
                self.hit()

    def render(self, screen, camera):
        # отрисовка моба
        if self.task == TASK_GO:
            screen.blit(self.animations[self.rotation_right].next(), (self.x - camera.x, real_y(self.y, 90)))
        elif self.task == TASK_HIT:
            screen.blit(self.animations[2 + int(self.rotation_right)].next(), (self.x - camera.x, real_y(self.y, 90)))
        pg.draw.rect(screen, (50, 0, 0), (self.x - camera.x, real_y(self.y + 70, 52), 52, 8))
        if self.hp <= 1:
            pg.draw.rect(screen, (255, 0, 0), (self.x - camera.x, real_y(self.y + 70, 52), 52 / self.max_hp, 8))
        else:
            pg.draw.rect(screen, (0, 255, 0),
                         (self.x - camera.x, real_y(self.y + 70, 52), 52 * self.hp / self.max_hp, 8))


class Player(Mob):
    def __init__(self, animations, mob_list, bullet_list, images):
        super().__init__(120, LAND_POINT_Y, animations, self, mob_list, bullet_list, images)
        self.rotation_right = True
        self.max_hp = 5
        self.hp = 5

    def init(self):
        # сброс состояния моба (или игрока)
        for animation in self.animations:
            animation.clear()
        self.speed_y = 0
        self.rotation_right = True
        self.task = TASK_STAY
        self.freeze_timer = time()
        self.hp = self.max_hp
        self.x, self.y = self.sx, self.sy

    # def freeze(self):
    #     return time() - self.freeze_timer <= 0.25

    def update(self, delta):
        # обработка действий игрока, нажатий на клавиши и управление игроком
        if not self.freeze():
            keys = pg.key.get_pressed()
            if keys[pg.K_d] and self.x + PLAYER_SPEED < WIDTH * 2 - 120:
                self.x += PLAYER_SPEED * delta * DELTA_MOD
                self.rotation_right = True
                self.set_task(TASK_GO)
            elif keys[pg.K_a] and self.x - 120 - PLAYER_SPEED > 0:
                self.x -= PLAYER_SPEED * delta * DELTA_MOD
                self.rotation_right = False
                self.set_task(TASK_GO)
            else:
                self.set_task(TASK_STAY)

            if self.y < LAND_POINT_Y:
                self.speed_y = 0
                self.y = LAND_POINT_Y
            elif self.y > HEIGHT - 120:
                self.speed_y = 0
                self.y = HEIGHT - 120
            elif self.y == LAND_POINT_Y and self.speed_y == 0:
                if keys[pg.K_w]:
                    self.speed_y = PLAYER_JUMP
            else:
                self.speed_y -= GRAVITY * delta * DELTA_MOD
                self.y += self.speed_y * delta * DELTA_MOD

            if keys[pg.K_s] and self.landed():
                self.hit()

    def hit(self):
        # удар мечом
        self.task = TASK_HIT
        self.freeze_timer = time()
        for mob in self.mob_list:
            if (mob.x >= self.x and self.rotation_right and abs(self.x + 100 - mob.x) <= 80) or \
                    (mob.x <= self.x and not self.rotation_right and abs(self.x - (mob.x + 40)) <= 40):
                mob.hp -= 1
                if mob.hp <= 0:
                    self.mob_list.remove(mob)

    def shoot(self):
        # метание топора
        self.bullet_list.append(
            Bullet(self.x + 120 * self.rotation_right, self.y, [Animation([self.images["axe_right"]], 1)], 3, self,
                   self.mob_list, self.bullet_list, rotation_right=self.rotation_right))

    def control(self, event):
        # обработчик ЛКМ для топора
        if not self.freeze():
            if event.button == pg.BUTTON_LEFT and time() - self.shoot_timer >= self.cooldown:
                self.shoot()
                self.shoot_timer = time()

    def render(self, screen, camera):
        # отрисовка игрока
        if self.task == TASK_GO:
            screen.blit(self.animations[1 - int(self.rotation_right)].next(), (self.x - camera.x, real_y(self.y, 115)))
        elif self.task == TASK_STAY:
            screen.blit(self.animations[3 - int(self.rotation_right)].next(), (self.x - camera.x, real_y(self.y, 115)))
        elif self.task == TASK_HIT:
            screen.blit(self.animations[5 - int(self.rotation_right)].next(),
                        (self.x - camera.x - 45 * (1 - int(self.rotation_right)), real_y(self.y, 115)))


class Bonus:
    def __init__(self, x, hp, image):
        self.x = x
        self.hp = hp
        self.image = image

    def update(self, player, bonus_list):
        if abs(player.x - self.x) <= 80 and player.y <= LAND_POINT_Y + 80:
            player.hp += min(self.hp, player.max_hp - player.hp)
            bonus_list.remove(self)

    def render(self, screen, camera):
        screen.blit(self.image, (self.x - camera.x, real_y(LAND_POINT_Y, 80)))


class Camera:
    # игровая камера для отслеживания цели и правильной отрисовки объекта
    def __init__(self, background):
        self.x, self.y = 0, 0
        self.background = background

    def update(self, target):
        self.x = max(120, min(target.x + CAMERA_OFFSET_X + 70, WIDTH))

    def render(self, screen):
        screen.blit(self.background, (-self.x, self.y))
        

class Bar:
    def __init__(self, x, y, width, height, background, line, overlay, min_value, max_value):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.background = background
        self.overlay = overlay
        self.min_value, self.max_value = min_value, max_value
        self.scale = self.max_value - self.min_value
        self.value = min_value

    def update(self, value):
        self.value = value

    def render(self, screen):
        screen.blit(self.background, (self.x, real_y(self.y, self.height)))
        pg.draw.rect(screen, (255, 0, 0), (self.x + 58, real_y(self.y + 70, self.height // 3), int(self.width * self.value / self.scale * 0.8 - 10), self.height // 3 - 2))
        screen.blit(self.overlay, (self.x, real_y(self.y, self.height)))


class Menu:
    def __init__(self, background, buttons):
        self.background = background
        self.buttons = buttons
        self.active = True

    def set_active(self, active):
        self.active = active

    def update(self):
        for button in self.buttons:
            button.update()

    def render(self, screen):
        screen.blit(self.background, (0, 0))
        for button in self.buttons:
            button.render(screen)


class Button:
    def __init__(self, x, y, width, height, image, function):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.image = image
        self.function = function

    def update(self):
        mouse_pos = pg.mouse.get_pos()
        if in_rect(self.x, real_y(self.y, self.height), self.width, self.height, mouse_pos[0], mouse_pos[1]):
            self.function()

    def render(self, screen):
        screen.blit(self.image, (self.x, real_y(self.y, self.height)))

