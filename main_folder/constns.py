#Магические переменные
WIDTH = 1400
HEIGHT = 787
FPS = 70
DELTA_MOD = 50
NAME = "Knight VS Orks"

# параметры для графического интерфейса - расположение кнопок и т.п.
BTN_X = 200
BTN_NEW_Y = 400
BTN_LOAD_Y = 300
BTN_QUIT_Y = 200
HEALTH_BAR_EXTRA_SCALE = 1

# параметры физики игры - гравитация, точки земли и т.п.
LAND_POINT_Y = 90
CAMERA_OFFSET_X = -WIDTH // 2
PLAYER_SPEED = 6
PLAYER_JUMP = 22
GRAVITY = 0.9

# константы состояний
TASK_STAY = 0
TASK_GO = 1
TASK_HIT = 2


def in_rect(x, y, width, height, x0, y0):
    return x <= x0 <= x + width and y <= y0 <= y + height


def real_y(y, height):
    return HEIGHT - y - height