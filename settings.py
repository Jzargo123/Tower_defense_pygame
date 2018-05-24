"""
Файлик с константами и основными параметрами игры. Менять очень осторожно!!!
"""

#размеры и цвета
(WIDTH, HEIGHT) = (1200, 700)   # константный кортеж с размером
PLAYER_HEALTHBAR_HEIGHT = 60  #высота хп и опыта
SIZE = (WIDTH, HEIGHT + PLAYER_HEALTHBAR_HEIGHT)          # размер игрового пространства (окно + мобы + игрок)

WHITE = (255, 255, 255)  # цвета в RGB
FPS = 100     # FPS * COOLDOWN / 1000 = количество секунд между событиями
SOUND_ON = True     # включен ли звук в игре?

#Шрифты
FONTSIZE = 36
SMALLFONTSIZE = 22


#всё связанное с мобами
TEST_MOB_LIST = [5, 5, 5, 2, 2, 2, 2, 5, 1, 1, 2, 5, 2, 0, 2, 3, 1, 3, 0, 0, 1, 2, 3, 4, 5, 4, 5]
MOB_SPAWN_COOLDOWN = 200
MOB_DAMAGE_COOLDOWN = 50
HEALTHBAR_HEIGHT = 15


#всё связанное с героем
ARROW_SPEED = 15
SHOOTING_RATE = 40   # чем меньше, тем быстрее
SUNSTRIKE_CD = 400
DIFFICULTY = 1
ALACRITY_CD = 400
ALACRITY_TIME = 200
ALACRITY_ON = 1
SUNSTRIKE_DMG = 5



#Опыт и уровни
EXP_MULT = 2 #мультипликатор опыта от здоровья убитого моба
EXP_TO_LVL = [0, 0, 200, 500, 900, 1400, 2000, 2615, 3425, 3890, 4550, 5225, 6000, 7175, 8375, 9600, 10850, 12125, 13500, 14900,
              1000000]  #общий опыт уровня

EXP_DIFF = []  #разница опыта для перехода на следующий уровень (вычисляем автоматически)
for i in range(len(EXP_TO_LVL) - 1):
    EXP_DIFF.append(EXP_TO_LVL[i+1] - EXP_TO_LVL[i])