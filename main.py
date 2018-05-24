from game_objects import *

#   x,   y,  заголовок,   выбранный,   не выбранный
choosen_color =     (250, 100, 100)
unchoosen_color =   (250, 250, 250)
items = [(WIDTH *9/20, HEIGHT /3 +   0, u'PLAY ', choosen_color, unchoosen_color, 0),
         (WIDTH *9/20, HEIGHT /3 +  50, u'QUIT ', choosen_color, unchoosen_color, 1),
         (WIDTH *9/20, HEIGHT /3 + 100, u'RESULTS', choosen_color, unchoosen_color, 2),
         (WIDTH *9/20, HEIGHT /3 + 150, u'SETTINGS', choosen_color, unchoosen_color, 3)
         ]


game = Menu(items)
game.menu() # вызываем меню игры



# музыка
if SOUND_ON:
    pygame.mixer.music.load("assets/menu"+str(random.randint(0,3))+".mp3") # загружаем музыку на бэкграунд
    pygame.mixer.music.play(-1,0.0)  # бесконечно повторяется, начало с 0.0



# Game objects
player = Player(clock, arrows)  # т.к. игрок стреляет, передаём ему часы и стрелы
background = Background()

# занесение объектов в группы
all_objects.add(background)  # чтобы убрать бэкграунд, комментить тут
player_singlegroup.add(player)

# текущий элемент массива мобов для спауна
current_mob = 1
#prev_mob = 0

sunstrike_cd = 0
alacrity_cd = 0
global SHOOTING_RATE
global ALACRITY_ON


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

    # нажатые клавиши
    keys = pygame.key.get_pressed()
    if keys[pygame.K_KP_ENTER]:
        clock.tick(FPS)
    elif keys[pygame.K_d]:
        if (sunstrike_cd == 0):#and(total_lvl > 3):
            spells.add(Sunstrike())
            sunstrike_cd = SUNSTRIKE_CD
    elif keys[pygame.K_f]:
        if (alacrity_cd <= 0):#and(total_lvl > 5):
            alacrity_cd = ALACRITY_CD
            ALACRITY_ON = 2



    current_mob = Mob.process_mobs(clock, mobs, current_mob)  # пускаем мобов
    #print(current_mob)


    # проверяем, если моб достиг цели
    for mob in list(mobs):
        # дальники с mob_type=1 стреляют через пол карты. type=0 это melee, бьющие вплотную
        if ((mob.rect.x < 200 + mob.mob_type * WIDTH // 2)):
            mob.rect.x = 200 + mob.mob_type * WIDTH // 2
            if (mob.attack_current_cooldown <= 0):
                mob.damaging()
                mob.attack_current_cooldown = MOB_DAMAGE_COOLDOWN
                mob.rect.x +=10
            else:
                mob.attack_current_cooldown -= 1
            # скорость не уменьшаем чтобы он при отталкивании мог подойти

    # проверка для всех мобов условий смерти (от выхода за экран и  здоровья = 0
    #for mob in list(mobs):
        if (((mob.rect.x > WIDTH)
             or (mob.rect.y > HEIGHT + PLAYER_HEALTHBAR_HEIGHT)  # проверка выхода за экран
             or mob.rect.y < 0
             or mob.rect.x < 0) or
                (mob.cur_hp <= 0)):  # смерть если закончилось здоровье
            mob.mob_die(mobs)
    # групповое столкновение. Стрелы ломаются об врагов и наносят им урон
        for arrow in pygame.sprite.spritecollide(mob, arrows, True):
            mob.take_damage(arrow.arrow_damage)
            #print(mob, mob.cur_hp)


    # получение мобами урона от скиллов
        for spell in pygame.sprite.spritecollide(mob, spells_damage, False):
            #print(spell.damage, type(spell.damage))
            mob.take_damage(spell.damage)



    # герой умирает от столкновения с мобами
    player_and_mobs_collided = pygame.sprite.spritecollide(player, mobs, False)
    if player_and_mobs_collided:
        all_objects.remove(player)
        # здесь могло бы быть ваше меню и сообщение о неудаче



    # обновление всех групп
    all_objects.update()
    player_singlegroup.update()#  проводим все изменения над игроком
    arrows.update()
    mobs.update()
    coins.update()
    spells_damage.update()
    spells.update()


    # отрисовка всех групп
    all_objects.draw(window)
    player_singlegroup.draw(window)
    arrows.draw(window)
    mobs.draw(window)
    coins.draw(window)
    spells.draw(window)

    # рисуем красную часть хп всем мобам. Это возможно надо засунуть в process mobs
    for i in mobs:
        pygame.draw.rect(window, (255, 0,0), (i.rect.left + int(i.mob_healthbar.percent_hp * i.mob_healthbar.rect.width),
                                        i.rect.top - 13,  int((1 - i.mob_healthbar.percent_hp) * i.mob_healthbar.rect.width),
                                                              i.mob_healthbar.healthbar_hight))

    healthbars.draw(window)



    # отрисовать экран заново

    pygame.display.flip()


    info_string.fill((45,80,40))
    window.blit(info_string, (0, HEIGHT+PLAYER_HEALTHBAR_HEIGHT))



    if sunstrike_cd > 0:
        sunstrike_cd -= 1 #уменьшаем кулдаун санстрайка на 1

    if alacrity_cd > 0:
        alacrity_cd -=1

    if alacrity_cd < int(1/2*ALACRITY_CD):
        ALACRITY_ON = 1

   # print(ALACRITY_ON)
    clock.tick(FPS)  # оттикать фпс, чтобы всё не закончилось сразу



# разинициализация шрифтов после игрового цикла
#pygame.font.quit()
