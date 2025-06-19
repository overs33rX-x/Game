import os.path
import time
import pygame as pg
from time import time
import sys
from classes import Animation, Bullet, Mob, Camera, Player, Menu, Button, Bar
from time import time
from classes import Mob, Animation, Bonus
from random import randint
from constns import *


def one_mob(game, damage):
    return Mob(randint(500, WIDTH * 2 - 500), LAND_POINT_Y, [
        Animation([game.images["ork_left_1"], game.images["ork_left_2"]], 0.1),
        Animation([game.images["ork_right_1"], game.images["ork_right_2"]], 0.1),
        Animation([game.images["ork_hit_left_1"], game.images["ork_hit_left_2"]], 0.1),
        Animation([game.images["ork_hit_right_1"], game.images["ork_hit_right_2"]], 0.1)],
               game.player, game.mobs, game.bullets, game.images, damage=damage)


def generate(game, damage=1.0):
    mob = one_mob(game, damage)
    while abs(mob.x - game.player.x) <= 200:
        mob = one_mob(game, damage)
    return mob


class Level:
    def __init__(self, mobs_query, game):
        self.query = mobs_query
        self.index = -1
        self.timer = 0
        self.start_player_x = 0
        self.game = game

    def generate_bonus(self, bonus_list):
        bonus_list.append(Bonus(randint(500, WIDTH * 2 - 500), 2, self.game.images["bonus"]))

    def generate_mob(self, mobs_list):
        mobs_list.append(self.query[self.index])
        self.timer = time()
        self.index += 1


class Level1(Level):
    def __init__(self, game):
        super().__init__([generate(game), generate(game), generate(game), generate(game), generate(game)], game)

    def next_trigger(self, player, mobs_list, bonus_list):
        if self.index == -1:
            self.index = 0
            self.start_player_x = player.x
        if self.index == 0:
            if player.x != self.start_player_x:
                self.generate_mob(mobs_list)
        elif self.index == 1:
            if len(mobs_list) == 0:
                self.generate_mob(mobs_list)
                self.generate_bonus(bonus_list)
        elif self.index == 2:
            if len(mobs_list) == 0:
                self.generate_mob(mobs_list)
        elif self.index == 3:
            if time() - self.timer >= 5:
                self.generate_mob(mobs_list)
        else:
            if len(mobs_list) == 0 and player.x >= WIDTH * 2 - 140:
                return True


class Level2(Level):
    def __init__(self, game):
        super().__init__([generate(game), generate(game), generate(game), generate(game, 1.5), generate(game, 1.5), generate(game, 1.5)], game)

    def next_trigger(self, player, mobs_list, bonus_list):
        if self.index == -1:
            self.index = 0
            self.start_player_x = player.x
        if self.index == 0:
            if player.x != self.start_player_x:
                self.generate_mob(mobs_list)
                self.generate_bonus(bonus_list)
        elif self.index == 1:
            if len(mobs_list) == 0:
                self.generate_mob(mobs_list)
                self.generate_mob(mobs_list)
        elif self.index == 3:
            if len(mobs_list) == 0:
                self.generate_mob(mobs_list)
        elif self.index == 4:
            if len(mobs_list) == 0:
                self.generate_mob(mobs_list)
                self.generate_mob(mobs_list)
                self.generate_bonus(bonus_list)
        else:
            if len(mobs_list) == 0 and player.x >= WIDTH * 2 - 140:
                return True



class Game:
    def __init__(self):
        # инициализация компонентов
        pg.init()
        pg.display.init()
        pg.font.init()
        pg.mixer.init()
        pg.display.set_caption(NAME)

        # пути к ресурсам
        img_path = os.path.join(os.path.dirname(__file__), R"C:\Users\Fedor\Desktop\game\Game\image")
        bullet_path = os.path.join(img_path, "bullets")
        orc_path = os.path.join(img_path, "orc")
        gui_path = os.path.join(img_path, "gui")

        # загрузка графики
        self.guis = {"menu": pg.image.load(os.path.join(gui_path, "menu.png")),
            "btn_new": pg.image.load(os.path.join(gui_path, "btn_new.png")),
            "btn_load": pg.image.load(os.path.join(gui_path, "btn_load.png")),
            "btn_quit": pg.image.load(os.path.join(gui_path, "btn_quit.png")),
            "health_bar_back": pg.image.load(os.path.join(gui_path, "health_bar_back.png")),
            "health_bar_line": pg.image.load(os.path.join(gui_path, "health_bar_line.png")),
            "health_bar_overlay": pg.image.load(os.path.join(gui_path, "health_bar_overlay.png")),
            "back": pg.image.load(os.path.join(img_path, "background.png"))}
        
        self.guis["health_bar_back"] = pg.transform.scale(self.guis["health_bar_back"], (400, 200))
        self.guis["health_bar_line"] = pg.transform.scale(self.guis["health_bar_line"], (400, 200))
        self.guis["health_bar_overlay"] = pg.transform.scale(self.guis["health_bar_overlay"], (400, 200))

        self.images = {"run_left_1": pg.image.load(os.path.join(img_path, "run1_knight_l.png")),
            "run_left_2": pg.image.load(os.path.join(img_path, "run2_knight_l.png")),
            "run_right_1": pg.image.load(os.path.join(img_path, "run1_knight_r.png")),
            "run_right_2": pg.image.load(os.path.join(img_path, "run2_knight_r.png")),
            "stand_left": pg.image.load(os.path.join(img_path, "stand_knight_l.png")),
            "stand_right": pg.image.load(os.path.join(img_path, "stand_knight_r.png")),
            "hit_left": pg.image.load(os.path.join(img_path, "sword_l.png")),
            "hit_right": pg.image.load(os.path.join(img_path, "sword_r.png")),
            "ork_left_1": pg.image.load(os.path.join(orc_path, "ork_left_1.png")),
            "ork_left_2": pg.image.load(os.path.join(orc_path, "ork_left_2.png")),
            "ork_right_1": pg.image.load(os.path.join(orc_path, "ork_right_1.png")),
            "ork_right_2": pg.image.load(os.path.join(orc_path, "ork_right_2.png")),
            "ork_hit_right_1": pg.image.load(os.path.join(orc_path, "orc_hit_right_1.png")),
            "ork_hit_right_2": pg.image.load(os.path.join(orc_path, "orc_hit_right_2.png")),
            "ork_hit_left_1": pg.image.load(os.path.join(orc_path, "orc_hit_left_1.png")),
            "ork_hit_left_2": pg.image.load(os.path.join(orc_path, "orc_hit_left_2.png")),
            "axe_right": pg.image.load(os.path.join(bullet_path, "axe.png")),
            "bonus": pg.image.load(os.path.join(img_path, "bonus.png"))}

        snd_path = os.path.join(os.path.dirname(__file__), R"D:\vs_code\Mine_Python\Code\PY_GAME\music\sounds")
        self.sounds = {

        }
        pg.mixer.music.load(os.path.join(snd_path, R"C:\Users\Fedor\Desktop\game\Game\music\sounds\music.mp3"))
        pg.mixer.music.play()

        # создание начальных объектов - экран, главное меню, камера, списки с мобами и пулями, игрок, полоска жизни
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.menu = Menu(self.guis["menu"], [
            Button(BTN_X, BTN_NEW_Y, 226, 58, self.guis["btn_new"], self.new_game),
            Button(BTN_X, BTN_LOAD_Y, 226, 58, self.guis["btn_load"], self.load),
            Button(BTN_X, BTN_QUIT_Y, 226, 58, self.guis["btn_quit"], self.exit)
        ])
        self.camera = Camera(self.guis["back"])
        self.mobs = []
        self.bullets = []
        self.bonuses = []
        self.player = Player([
            Animation([self.images["run_right_1"], self.images["run_right_2"]], 0.05),
            Animation([self.images["run_left_1"], self.images["run_left_2"]], 0.05),
            Animation([self.images["stand_right"]], 1),
            Animation([self.images["stand_left"]], 1),
            Animation([self.images["hit_right"]], 1),
            Animation([self.images["hit_left"]], 1)
        ], self.mobs, self.bullets, self.images)
        self.health_bar = Bar(0, HEIGHT - 160, 400, 200,
                              self.guis["health_bar_back"],
                              self.guis["health_bar_line"],
                              self.guis["health_bar_overlay"], 0, self.player.max_hp)

        # делта для того, чтобы fps не зависела от мощности компьютера (видеокарты, процессора и т.д.)
        self.delta = 0.0

        # инициация уровня
        self.level = 0
        self.levels = []

    def new_game(self):
        # установка значений в начале игры
        self.menu.set_active(False)
        self.player.init()
        self.mobs.clear()
        self.bonuses.clear()
        self.player.init()
        self.delta = time()
        self.level = 0
        self.levels.clear()
        self.levels = [Level1(self), Level2(self)]

    def load(self):
        pass

    def exit(self):
        pg.quit()
        sys.exit()

    def mainloop(self):
        # главный цикл
        clock = pg.time.Clock()
        while True:
            self.screen.fill((0, 0, 0))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.exit()
                elif event.type == pg.MOUSEBUTTONUP:
                    if self.menu.active:
                        self.menu.update()
                    else:
                        self.player.control(event)
            clock.tick(FPS)
            delta = time() - self.delta
            self.delta = time()

            if self.menu.active:
                self.menu.render(self.screen)
            else:
                # логика
                for mob in self.mobs:
                    mob.update(delta)
                for bullet in self.bullets:
                    bullet.update(delta)
                for bonus in self.bonuses:
                    bonus.update(self.player, self.bonuses)
                self.player.update(delta)
                self.camera.update(self.player)
                self.health_bar.update(self.player.hp)
                victory = False
                if self.level >= len(self.levels):
                    victory = True
                elif self.levels[self.level].next_trigger(self.player, self.mobs, self.bonuses) is not None:
                    # переход на следующий уровень
                    self.level += 1
                    self.player.x = self.player.sx
                elif self.player.hp <= 0:
                    self.new_game()

                # Отрисовка графики
                self.camera.render(self.screen)
                for mob in self.mobs:
                    mob.render(self.screen, self.camera)
                for bullet in self.bullets:
                    bullet.render(self.screen, self.camera)
                for bonus in self.bonuses:
                    bonus.render(self.screen, self.camera)
                self.player.render(self.screen, self.camera)
                self.health_bar.render(self.screen)
                if victory:
                    text_surface = pg.font.SysFont('Comic Sans MS', 120).render('Victory!', False, (0, 0, 0))
                    self.screen.blit(text_surface, (WIDTH // 2 - 200, HEIGHT - (HEIGHT // 2 + 120)))

            pg.display.update()


Game().mainloop()
