# здесь будут все объявления игровых объектов
import pygame
import cmath, math
import random
import sys  # нужно для часиков и fps

from settings import  * #SIZE, FPS, WHITE, WIDTH, HEIGHT, ARROW_SPEED, SHOOTING_RATE, TEST_MOB_LIST, MOB_SPAWN_COOLDOWN


pygame.init()


clock = pygame.time.Clock()

# Groups
all_objects = pygame.sprite.Group()         # группа объектов (игрок, бэкграунд)
arrows = pygame.sprite.Group()              # группа стрел
mobs = pygame.sprite.Group()                # группа мобов
healthbars = pygame.sprite.Group()          # группа панелек здоровья мобов
coins = pygame.sprite.Group()               # группа монеток
player_healthbar = pygame.sprite.Group()    # здоровье игрока
spells = pygame.sprite.Group()              # группа спеллов
spells_damage = pygame.sprite.Group()       # группа наносящих урон спрайтов от спеллов
player_singlegroup = pygame.sprite.Group()  # группа из одного игрока
main_menu_background = pygame.sprite.Group()# группа из заднего фона главного меню


buttons = pygame.sprite.Group()

# работа с поверхностями и окнами
window = pygame.display.set_mode(SIZE) # окно игры
pygame.display.set_caption("Jzargo's Sentry Knight")
#screen = pygame.Surface((WIDTH-100, HEIGHT-100)) # холст


# холст
screen = pygame.Surface((WIDTH,HEIGHT+PLAYER_HEALTHBAR_HEIGHT)) # строка состояния внизу экрана
info_string = pygame.Surface((WIDTH / 3,HEIGHT / 3))
# работа со шрифтами
pygame.font.init()

font_player_healthbar = pygame.font.Font("assets\OpenSans-CondBold.ttf", SMALLFONTSIZE)

#pygame.font.SysFont("Cooper Black" ,22)
# инициализируем первый шрифт. вместо None можно дать .ttf файл шрифта
#pygame.font.SysFont(Arial, 14,)


# глобальные переменные:
total_gold = 0
total_exp = 0
total_lvl = 1

class Menu():
    def __init__(self, items):
        self.items = items

    def render(self, surface, font, item_num):
        for i in self.items:
            if item_num == i[5]: #если получили нужны, закрашиваем пункт выделенным цветом
                surface.blit(font.render(i[2], 1, i[4]), (i[0], i[1] + FONTSIZE/2))
            else:
                surface.blit(font.render(i[2], 1, i[3]), (i[0], i[1] + FONTSIZE/2))

    def menu(self):
        done = True  #показывать ли меню?
        #шрифты меню
        font_menu = pygame.font.Font("assets\IntervalSansProCondensedLight.otf" ,FONTSIZE)
        item = 0

        pygame.key.set_repeat()# залипание клавиш
        pygame.mouse.set_visible(True)

        menu_back = pygame.sprite.Sprite()
        main_menu_background.add(menu_back)
        # подгоняем под размер экрана
        menu_back.image = pygame.transform.scale(pygame.image.load('assets/menu_background.png'),
                                                 (WIDTH, HEIGHT + PLAYER_HEALTHBAR_HEIGHT))
        menu_back.rect = menu_back.image.get_rect()  # берём его собственный прямоугольник за размер


        #bu = Healthbar(self)
     #   button_quit = Button((WIDTH, HEIGHT /3))
    #    buttons.add(button_quit)



        while done:

            main_menu_background.update()
            main_menu_background.draw(screen)
            all_objects.draw(screen)
            # info_string.fill((0, 100, 200))
            # screen.fill((0, 100, 200))

            mp = pygame.mouse.get_pos()
            #проверяем на столкновение мышки и пункта меню. Это надо переделеать через collide
            for i in self.items:
                if mp[0] > i[0] and \
                        mp[0] < i[0] + 70 and \
                        mp[1] > i[1] + FONTSIZE  and \
                        mp[1] < i[1] + FONTSIZE*2 :
                    item = i[5]
            self.render(screen, font_menu, item)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    print(e)
                    if e.key == pygame.K_RETURN:
                        if item == 0:
                            done = False
                        if item == 1:
                            sys.exit()
                    if e.key == pygame.K_ESCAPE: #выход по ESC
                        sys.exit()

                # выбор пунктов клавишами
                    if e.key == pygame.K_UP:
                        if item > 0:
                            item -= 1
               #         else: item = len(self.items) - 1
                    if e.key == pygame.K_DOWN:
                        if item < len(self.items) - 1:
                            item += 1
                 #       else:  item = 0

                # активация пунктов
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if item == 0:
                        done = False
                    if item == 1:
                        sys.exit()
                    if item == 2:
                        print("Results are coming soon")
                    if item == 3:
                        print("i will make settings soon")
            window.blit(info_string, (0, 0))
            window.blit(screen, (0, 0))
            pygame.display.update()

        if not done:
            # если начинаем игру, то фон меняется и воспроизводится музыка начала игры
            menu_back.image = pygame.transform.scale(pygame.image.load('assets/menu_background2.png'),
                                                     (WIDTH, HEIGHT + PLAYER_HEALTHBAR_HEIGHT))
            menu_back.rect = menu_back.image.get_rect()  # берём его собственный прямоугольник за размер
            main_menu_background.update()
            main_menu_background.draw(screen)
            all_objects.draw(screen)
            if SOUND_ON:
                pygame.mixer.music.load("assets/game_ready.mp3")  # загружаем музыку на бэкграунд
                pygame.mixer.music.play(0, 0.1)

            window.blit(screen, (0, 0))
            pygame.display.update()
            pygame.time.delay(3000)

class Player(pygame.sprite.Sprite):
    max_speed = 5
    damage = 1
    shooting_rate = int(SHOOTING_RATE / (1 + 1/4 * total_lvl))
    player_healthbar = pygame.sprite.Sprite()
    cur_hp = 100
    max_hp = 100
    def __init__(self, clock, arrows):
        super(Player, self).__init__()

        self.clock = clock  # храним как внутренние атрибуты
        self.arrows = arrows

        self.image = pygame.image.load('assets/player.png')
        self.rect = self.image.get_rect()   # берём его собственный прямоугольник за размер
        #self.rect.width =
        self.rect.top = HEIGHT / 2
        self.rect.left = 0

        self.current_speed = 0  # текущая скорость игрока
        self.current_shooting_cooldown = 0 # текущий кулдаун выстрелов
        self.draw_healthbar()
        self.draw_exp()

    def draw_exp(self):
        # рисуем серый задник опыта

        global total_exp # чтобы не вычислять по куче раз
        global total_lvl

        pygame.draw.rect(window, (100,100,100), (0, PLAYER_HEALTHBAR_HEIGHT // 2, WIDTH, PLAYER_HEALTHBAR_HEIGHT // 2))
        player_healthbar.draw(window)
        #рисуем желтую часть опыта - полученный
        pygame.draw.rect(window, (255, 255, 0), (0, PLAYER_HEALTHBAR_HEIGHT // 2,
                                                 int((total_exp - EXP_TO_LVL[total_lvl]) / EXP_DIFF[total_lvl] * WIDTH),
                                                 PLAYER_HEALTHBAR_HEIGHT // 2))
        player_healthbar.draw(window)
        # подпись с количеством опыта
        window.blit(font_player_healthbar.render('Level '+str(total_lvl)+ '   Exp ' + str(total_exp) +
                                                  ' / ' + str(EXP_TO_LVL[total_lvl + 1] ),
                                                 1,
                                                 (255, 255, 255)),
                    (WIDTH / 2 - 60, PLAYER_HEALTHBAR_HEIGHT // 2))

    def draw_healthbar(self):
        if self.cur_hp <= 0:
            pygame.mixer.music.load("assets/sad.mp3")  # загружаем музыку на бэкграунд
            pygame.mixer.music.play(0, 0.0)  # бесконечно повторяется, начало с 0.0
            pygame.time.delay(3000)
            self.cur_hp = 0

        # рисуем красную часть хп и зелёную
        pygame.draw.rect(window, (255,0,0), (0,0,WIDTH, PLAYER_HEALTHBAR_HEIGHT // 2))
        player_healthbar.draw(window)
        pygame.draw.rect(window, (0, 220, 0), (0, 0,  int(self.cur_hp / self.max_hp * WIDTH), PLAYER_HEALTHBAR_HEIGHT // 2))
        player_healthbar.draw(window)
        # подпись с количеством здоровья
        window.blit(font_player_healthbar.render('Health ' + str(Player.cur_hp) + ' / ' + str(Player.max_hp),
                                                 1,
                                                 (255, 255, 255)),
                    (WIDTH / 2 - 60, 0))
        if self.cur_hp <= 0:
            EndGame()


    def update(self):
        global total_exp  # может и костыль. Стоит ли пользоваться глобальным опытом, или сделать это частью героя?

        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            self.current_speed = self.max_speed
        elif keys[pygame.K_UP]:
            self.current_speed = - self.max_speed
        else:
            self.current_speed = 0

        self.rect.move_ip((0, self.current_speed))  # относительное смещение игрока

        if self.rect.bottom >= HEIGHT + PLAYER_HEALTHBAR_HEIGHT:  # проверка, чтобы за границы не выходил
            self.rect.bottom = HEIGHT + PLAYER_HEALTHBAR_HEIGHT
        if self.rect.top <= PLAYER_HEALTHBAR_HEIGHT:
            self.rect.top = PLAYER_HEALTHBAR_HEIGHT

        self.shooting()
        self.draw_healthbar()
        self.draw_exp()

    def shooting (self):  # стреляем стрелами с частотой  shooting_cooldown
        #координаты выстрела
        global ALACRITY_ON
        global total_lvl
        if self.current_shooting_cooldown <= 0:
            self.arrows.add(Arrow(( self.rect.right - 50,
                                    self.rect.top +self.rect.height / 3,),
                                  self.damage,
                                  True))
            self.current_shooting_cooldown = int(SHOOTING_RATE / (1 + 1/4 * total_lvl / ALACRITY_ON))

           # print(self.current_shooting_cooldown, total_lvl, ALACRITY_ON)
        else:
            self.current_shooting_cooldown -= 1

        for arrow in list(self.arrows):  # удаляем стрелы при выходе за экран
            if ((arrow.rect.x > WIDTH )
                    or (arrow.rect.y > HEIGHT)
                    or arrow.rect.y < PLAYER_HEALTHBAR_HEIGHT
                    or arrow.rect.x < self.rect.right /2 ):
                self.arrows.remove(arrow)


class Arrow(pygame.sprite.Sprite):
    ax = 0
    ay = 0
    # gravity = 1  # если очень захочется гравитации
    arrow_damage = 5
    def __init__(self, position, damage, is_player):  # конструироваться должен в позиции игрока
        super(Arrow, self).__init__()
        arrow_damage = damage
        (px, py) = position  # позиция стреляющего
        #if is_player:
        (cx, cy) = pygame.mouse.get_pos()  # позиция курсора
      #  else:
       #     for i in player_singlegroup:
      #          (cx, cy) = i.rect.midright
        #  вектор полёта в сторону курсора. +1 от деления на 0
        n = cmath.sqrt((cx - px) ** 2 + (cy - py) ** 2 + 1)
        self.ax = (cx - px) / n
        self.ay = (cy - py) / n

        rot = 1
        if cy > py:  # условие переворота стрелы
            rot = -1

        self.image = pygame.image.load('assets/arrow.png')
        self.rect = self.image.get_rect()
        # поворот стрелы
        self.image = pygame.transform.rotate(self.image, rot * 180 / cmath.pi * cmath.acos(self.ax.real).real)
        self.rect.midleft = position

    def update(self):
        # self.gravity -= 1   # и добавить в правую часть скобки   -self.gravity
        self.rect.move_ip((ARROW_SPEED * self.ax.real, ARROW_SPEED * self.ay.real + random.randint(0,DIFFICULTY))) #self.ay.real


class SpellDamage(pygame.sprite.Sprite):
    (x, y) = (0, 0) #pygame.mouse.get_pos()  # по умолчанию стреляет в курсор
    damage = 0
    lasts = 2 # длительность появления
    img_dest = 'assets/sunstrike.png' # картинка по-умолчанию
    def __init__(self, x, y, img, dmg):  # конструироваться должен в позиции игрока
        super(SpellDamage, self).__init__()
        self.x = x
        self.y = y
        self.image = img
        self.damage = dmg
        #(x, y) = pygame.mouse.get_pos()  # позиция стреляющего
        self.update()

    #нам не надо его рисовать. Нужно просто продамажить всех мобов по текстуре каста
    def update(self):
        #print(self.lasts)
        self.lasts -= 1
        if self.lasts > 0:
            self.image = pygame.image.load(self.img_dest)
            self.rect = self.image.get_rect()
            self.rect.midbottom = (self.x, self.y)
        else: #если счётчик убежал, то уничтожаем объект
            self.image = pygame.image.load('assets/noimage.png')
            spells_damage.remove(self)
            self.kill()


class Sunstrike(pygame.sprite.Sprite):
    (x, y) = pygame.mouse.get_pos()  # по умолчанию стреляет в курсор
    damage = 0
    lasts = 15  # длительность появления
    img_dest = 'assets/sunstrike.png'
    def __init__(self):  # конструироваться должен в позиции игрока
        super(Sunstrike, self).__init__()
        # self.damage = dmg
        (self.x, self.y) = pygame.mouse.get_pos()  # позиция стреляющего
        global total_lvl
        self.image = pygame.image.load(self.img_dest)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.x, self.y + 50)
        #добавляем текстуру урона самому санстрайку
        spells_damage.add(SpellDamage(self.x, self.y, self.img_dest, total_lvl*SUNSTRIKE_DMG))

    def update(self):
        #print(self.lasts)
        self.lasts -= 1
        if self.lasts > 5:
            pass
        elif self.lasts > 0:
            self.image = pygame.image.load('assets/sunstrike2.png')
            self.rect = self.image.get_rect()
            self.rect.midbottom = (self.x, self.y + 50)
        else:  # если счётчик убежал, то уничтожаем объект
            self.image = pygame.image.load('assets/noimage.png')
            spells.remove(self)
            self.kill()


class Mob(pygame.sprite.Sprite):
    max_hp = cur_hp = 1                      # здоровье моба
    #percent_hp = 0.99           # процент оставшегося здоровья
    damage = 1                  # урон герою
    speed = 1  # скорость движения
    current_cooldown = 0        # текущий кулдаун. Нужен для перемещения
    attack_current_cooldown = MOB_DAMAGE_COOLDOWN     # кулдаун атаки в секундах
    image_name = 'assets/mob1.png'
    mob_type = 0             #0 - melee, 1 range
    mob_healthbar = pygame.sprite.Sprite()  # собственная полоска здоровья моба
    casting = False
    spawn_another = 0
    def __init__(self, spawn_x ,spawn_y):
        super(Mob, self).__init__()

        self.image = pygame.image.load(self.image_name)
        self.rect = self.image.get_rect()
        self.rect.left = spawn_x   #спауним по заданным координатам
        self.rect.bottom = spawn_y
        self.new_healtbar()

    def new_healtbar(self):
        self.mob_healthbar = Healthbar(self)
        healthbars.add(self.mob_healthbar)
        self.draw_heathbar()

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        self.draw_heathbar()
        pygame.display.flip()

    def draw_heathbar(self):  # отрисовка панельки здоровья
        self.mob_healthbar.update(self)
        self.mob_healthbar.rect.union_ip(self.rect)

    @staticmethod # чтобы можно было использовать статические переменные
    def process_mobs(clock, mobs, current_mob): # создаём новых мобов по кд
        # спауним мобов из списка спауна по кд
        if (Mob.current_cooldown <= 0):   #and (current_mob < len(TEST_MOB_LIST)):
            #if TEST_MOB_LIST[current_mob] > 0:
               #TEST_MOB_LIST[current_mob % len(TEST_MOB_LIST)]

            #mobs.add(Golem())
            spawn_x = WIDTH
            spawn_y = random.randint(int(HEIGHT * 2 / 3), HEIGHT)

            i = random.randint(-5 + total_lvl*2, 5 + total_lvl*2)

            #mobs.add(Slime(spawn_x, spawn_y))
            if i < 3:
                mobs.add(Slime(spawn_x, spawn_y))
            elif (i < 5):
                mobs.add(Bat(spawn_x, spawn_y))
            elif i < 7:
                mobs.add(Bee(spawn_x, spawn_y))
            elif i < 8:
                mobs.add(Goblin(spawn_x, spawn_y))
            elif i < 10:
                mobs.add(Skeleton(spawn_x, spawn_y))
            elif i < 12:
                mobs.add(BigSlime(spawn_x, spawn_y))
            elif i < 16:
                mobs.add(BabyGolem(spawn_x, spawn_y))
            elif i < 19:
                mobs.add(HugeSlime(spawn_x, spawn_y))
            elif i < 20:
                mobs.add(Crab(spawn_x, spawn_y))
            elif i < 24:
                mobs.add(Spider(spawn_x, spawn_y))
            elif i < 25:
                mobs.add(Golem(spawn_x, spawn_y))

            Mob.current_cooldown = MOB_SPAWN_COOLDOWN    #]
            #print(current_mob, "----", TEST_MOB_LIST[current_mob], "----", MOB_MAP[TEST_MOB_LIST[current_mob]])
            return current_mob + 1  # сдвигаемся на нового моба (спауним)
        else:
            Mob.current_cooldown -= 1


        # если новый моб не создался, остаёмся на текущем
        return current_mob


    def mob_die(self, mobs):
        # анимация и звук смерти
        # прибавление опыта и денег игроку
        self.image = pygame.image.load('assets/noimage.png')
        mobs.remove(self)
        self.kill()
        healthbars.remove(self.mob_healthbar)
        self.mob_healthbar.kill()


        #проверка посмертных спаунов новых мобов
        if self.spawn_another == 1: #большой слизняк спаунит маленьких
           for i in range(1,3):
               mobs.add(Slime(self.rect.x + random.randint(0,120), self.rect.y + random.randint(0,100)))
        elif self.spawn_another == 20:
            for i in range(0, 3): #огромный слизняк спаунит больших
                mobs.add(BigSlime(self.rect.x + random.randint(0,120), self.rect.y + random.randint(0,100)))
        #elif self.spawn_another == 3:
       #     mobs.add(Slime(self.rect.x, self.rect.y + self.rect.height))



        else: #если моб никого не спаунит, значит он сдох и даёт опыт и монетки
            # даёт монеток (15 + максхп)/15 штук
            for i in range(1, int(math.ceil((self.max_hp+15) / 15))):
                coins.add(Coin((self.rect.x, self.rect.y)))

            # даёт опыта = здоровью убитого моба
            global total_exp
            global total_lvl
            total_exp += self.max_hp * EXP_MULT

            print('LvL:',total_lvl, 'Shooting rate', SHOOTING_RATE, 'Санстрайк ', total_lvl*SUNSTRIKE_DMG)

            #проверка получения нового уровня
            i = 0
            while total_exp > EXP_TO_LVL[i] - 1 :
                i+=1
            total_lvl = i-1

            #print(total_lvl, total_exp, EXP_TO_LVL[total_lvl], EXP_DIFF[total_lvl], EXP_TO_LVL[total_lvl+1], EXP_DIFF[total_lvl+1])


    def take_damage(self, damage): # получение урона в каком-то количестве
        self.cur_hp -= damage
        #self.update()

    def damaging(self):
        if self.mob_type == 1: # если моб стреляющий, пусть стреляет
            self.arrows.add(Arrow((self.rect.left ,
                                   self.rect.top + self.rect.height / 2,
                                   ), self.damage),  False)

            for arrow in list(self.arrows):  # удаляем стрелы при выходе за экран
                if ((arrow.rect.x > WIDTH)
                        or (arrow.rect.y > HEIGHT)
                        or arrow.rect.y < 0
                        or arrow.rect.x < 0):
                    self.arrows.remove(arrow)
        else:
            Player.cur_hp -= self.damage
            #print(Player.cur_hp)




class Slime(Mob): #1
    max_hp = cur_hp = 5
    damage = 1
    speed = 1
    image_name = 'assets/mob1.png'

class BigSlime(Mob): #20
    max_hp = cur_hp = 15
    damage = 1
    speed = 1
    image_name = 'assets/mob20.png'
    spawn_another = 1

class HugeSlime(Mob): #21
    max_hp = cur_hp = 45
    damage = 1
    speed = 1
    image_name = 'assets/mob21.png'
    spawn_another = 20

class Bat(Mob): #2
    max_hp = cur_hp = 25
    damage = 2
    speed = 3
    image_name = 'assets/mob2.png'

class Bee(Mob): #3
    max_hp = cur_hp = 15
    damage = 5
    speed = 4
    image_name = 'assets/mob3.png'

class Goblin(Mob): #4
    max_hp = cur_hp = 50
    damage = 7
    speed = 1
    image_name = 'assets/mob4.png'

class Skeleton(Mob): #5
    max_hp = cur_hp = 60
    damage = 6
    speed = 2
    image_name = 'assets/mob5.png'

class BabyGolem(Mob): #6
    max_hp = cur_hp = 60
    damage = 4
    speed = 1
    image_name = 'assets/mob6.png'

class Mage(Mob): #7
    max_hp = cur_hp = 40
    damage = 10
    speed = 1
    image_name = 'assets/mob7.png'
  #  mob_type = 1

class GoblinArcher(Mob): #8
    max_hp = cur_hp = 60
    damage = 10
    speed = 2
    image_name = 'assets/mob8.png'
  #  mob_type = 1

class Crab(Mob): #9
    max_hp = cur_hp = 75
    damage = 15
    speed = 3
    image_name = 'assets/mob9.png'

class Spider(Mob): #10
    max_hp = cur_hp = 100
    damage = 15
    speed = 3
    image_name = 'assets/mob10.png'
 #   mob_type = 1

class Golem(Mob): #14
    max_hp = cur_hp = 300
    damage = 20
    speed = 1
    image_name = 'assets/mob14.png'
 #   spawn_another = True



class Healthbar(pygame.sprite.Sprite):
    percent_hp = 0.99
    healthbar_hight = 10
    #is_mob = True
    def __init__(self, mob):
        super(Healthbar, self).__init__()
        self.update(mob)

    def update(self, mob):
        # высчитываем процент оставшихся хп чтобы нарисовать полоску хп

        if mob.cur_hp < 0:
            mob.cur_hp = 0
        self.percent_hp = float(mob.cur_hp / mob.max_hp)


        # укорачиваем полоску по проценту оставшихся хп
        self.image = pygame.transform.scale(pygame.image.load('assets/health.png'),
                                            (int(self.percent_hp * mob.rect.width), self.healthbar_hight))
        # рисуем зелёную часть хп
        self.rect = self.image.get_rect()
        self.rect = pygame.Rect(mob.rect.left, mob.rect.top - 13, int(self.percent_hp * mob.rect.width),  self.healthbar_hight)



class Background(pygame.sprite.Sprite):  # бэкграунд
    def __init__(self):
        super(Background, self).__init__()

        self.image = pygame.transform.scale(pygame.image.load('assets/background.png'),
                                            (WIDTH, HEIGHT))

        self.rect = self.image.get_rect()   # берём его собственный прямоугольник за размер
        self.rect.width = WIDTH
        self.rect.height = HEIGHT
        self.rect.top = PLAYER_HEALTHBAR_HEIGHT  # низ по высоте экрана


class Button(pygame.sprite.Sprite):
    button_width = 200
    button_higth = 38
    chosen = False # выбрана ли кнопка?
    dir = 'assets/button.png'
    def __init__(self, position, text):
        super(Button, self).__init__()
        self.image = pygame.transform.scale(pygame.image.load(dir),
                                            (self.button_width, self.button_higth))
        self.rect = self.image.get_rect()

    def update(self):
        if self.chosen:
            dir = 'assets/button_chosen.png'
        else:
            dir = 'assets/button.png'

        self.image = pygame.transform.scale(pygame.image.load(dir),
                                            (self.button_width, self.button_higth))
        self.rect = self.image.get_rect()

       # buttons.add(Button((self.rect.right - 50,
       #                     self.rect.top + self.rect.height / 3,),
       #                         True))


class Coin(pygame.sprite.Sprite):
    gravity = 0     #гравитация будет прибавляться тут
    rotation = 0    #размер проекции поворота
    coin_speed = ARROW_SPEED + random.randint(-5, 5) #скорость полёта монетки
    cx = 50         #направление полёта итоговое
    cy = HEIGHT - 50#летят на панельку с баблом
    (px, py) = (WIDTH, HEIGHT)  #место начальной смерти

    def __init__(self, position):  # конструироваться должен в позиции умершего моба
        super(Coin, self).__init__()
        (self.px, self.py) = position  # позиция умершего
        self.px += random.randint(-10, 10) #рандомизируем место появления
        self.px += random.randint(-10, 10)

        #(cx, cy) = (random.randint(30, WIDTH), random.randint(30,HEIGHT)) #летят нарандом

        #  вектор полёта в сторону курсора. +1 от деления на 0
        n = cmath.sqrt((self.cx - self.px) ** 2 + (self.cy - self.py) ** 2 + 1)
        self.ax = (self.cx - self.px) / n
        self.ay = (self.cy - self.py) / n

        coin_size = random.randint(15, 45)  #рандомизируем размеры монетки
        self.image = pygame.transform.scale(pygame.image.load('assets/coin.png'), (coin_size, coin_size))
        self.rect = self.image.get_rect()


        self.rect.midbottom = (self.px, self.py)

    def update(self):
        self.gravity -= 0   # гравитация
        self.rotation = (self.rotation + 1) % 20
        self.image = pygame.transform.scale(pygame.image.load('assets/coin.png'),
                                            (int(self.rect.width  * (80-self.rotation**2 + 20 * self.rotation) / 180),
                                             int(self.rect.height * (80-self.rotation**2 + 20 * self.rotation) / 180)))

        self.rect.move_ip((self.coin_speed * self.ax.real, self.coin_speed * self.ay.real - self.gravity)) #self.ay.real

        #print(self.cx - self.rect.right, self.cy - self.rect.top, self.ax, self.ay)
        for coin in list(coins):
            if ((coin.rect.x > WIDTH)
                 or (coin.rect.y > HEIGHT + PLAYER_HEALTHBAR_HEIGHT)  # проверка выхода за экран
                 or coin.rect.y < 0
                 or coin.rect.x < 0):

                self.image = pygame.image.load('assets/noimage.png')
                coins.remove(self)
                self.kill()


def EndGame():
    sys.exit()  # тут смерть игрока и выход на менюшку
