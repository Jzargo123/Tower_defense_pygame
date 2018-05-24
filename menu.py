
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
        done = False  #показывать ли меню?
        #шрифты меню
        font_menu = pygame.font.Font("assets\IntervalSansProCondensedLight.otf" ,FONTSIZE)
        item = 0

        pygame.key.set_repeat()# залипание клавиш
        pygame.mouse.set_visible(True)

        menu_back = pygame.sprite.Sprite()
        main_menu_background.add(menu_back)
        # подгоняем под размер экрана
        menu_back.image = pygame.transform.scale(pygame.image.load('assets/menu_background.png'),
                                                 (WIDTH, HEIGHT))
        menu_back.rect = menu_back.image.get_rect()  # берём его собственный прямоугольник за размер


        #bu = Healthbar(self)
     #   button_quit = Button((WIDTH, HEIGHT /3))
    #    buttons.add(button_quit)



        while done:
            #info_string.fill((0, 100, 200))
            #screen.fill((0, 100, 200))
            main_menu_background.update()
            main_menu_background.draw(screen)
            all_objects.draw(screen)


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
                                                     (WIDTH, HEIGHT))
            menu_back.rect = menu_back.image.get_rect()  # берём его собственный прямоугольник за размер
            main_menu_background.update()
            main_menu_background.draw(screen)
            all_objects.draw(screen)
            pygame.mixer.music.load("assets/game_ready.mp3")  # загружаем музыку на бэкграунд
            pygame.mixer.music.play(0, 0.1)

            window.blit(screen, (0, 0))
            pygame.display.update()
            pygame.time.delay(3000)
