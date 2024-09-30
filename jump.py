running = True
setting = True
while running:
    while setting:
        import pygame
        import random
        import math
        
        try:
            with open("bestscore.txt", 'r') as file:
                bestscore = file.read()
        except FileNotFoundError:
            with open("bestscore.txt", 'w') as file:
                file.write("0")
            with open("bestscore.txt", 'r') as file:
                bestscore = file.read()

        pygame.init()
        
        opening = True
        playing = True
        gameover = True

        logo = pygame.image.load("logo.png", "logo")
        sound = pygame.mixer.Sound("jump.wav")

        fps = pygame.time.Clock()
        screen_w, screen_h = 450, 800
        screen = pygame.display.set_mode((screen_w, screen_h))
        pygame.display.set_caption("Jump Game")
        pygame.display.set_icon(logo)

        opening_line = pygame.surface.Surface((screen_w, 4))
        opening_line.fill((255,255,255))

        title_font = pygame.font.SysFont(None, 100, True, False)
        title_text = title_font.render("Jump Game", False, (255,255,255))
        gameover_text = title_font.render("Game Over", False, (255,255,255))

        score_font = pygame.font.SysFont(None, 75, False, False)
        
        click_font = pygame.font.SysFont(None, 50, False, False)
        start_text = click_font.render("click to start",False , (255,255,255))
        restart_text = click_font.render("click to restart",False , (255,255,255))
        
        platform_v = 4
        platform_width, platform_height = 40, 4
        platform_spacing = 100
        
        circle_y = 195.5
        circle_x = screen_w//2
        v = 0
        score = 0
        circle_r = 10
        click_effect = 0
        jumping = True
        setting = False


    while opening:
        fps.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                opening =False
            if event.type == pygame.QUIT:
                running = False
                opening = False
                playing = False
                gameover = False

        if pygame.key.get_pressed()[pygame.K_a] == True or pygame.key.get_pressed()[pygame.K_LEFT] == True:
            circle_x -= 4
        if pygame.key.get_pressed()[pygame.K_d] == True or pygame.key.get_pressed()[pygame.K_RIGHT] == True:
            circle_x += 4
        if circle_x - circle_r >= screen_w:
            circle_x = circle_r
        if circle_x + circle_r <= 0:       
            circle_x = screen_w - circle_r

        if not jumping:
            sound.play()
            jumping = True
            v = -13
        circle_y += v
        v += 0.25

        if v >= 0:
            if  550 + 10 >= circle_y + circle_r >= 550 - 10:
                circle_y = 550 - circle_r
                jumping = False

        screen.fill((0,0,0))
        pygame.draw.circle(screen, (255,255,255), (circle_x, circle_y), circle_r)
        screen.blit(title_text, (20, 100))
        screen.blit(opening_line, (0, 550))
        screen.blit(start_text, (125, 650))
        pygame.display.flip()

    circle_y = 395.5
    circle_x = screen_w//2
    v = 0
    jumping = True
    score = 0
    platforms = []
    distance = [0]

    for i in range(8):
        platform_x = random.randint(0, screen_w - platform_width)
        platform_y = 750 - i * 100
        if random.randint(1, 3) == 1:
            platform_move = True
        else:
            platform_move = False
        ismoving = random.randint(0, 1)
        platforms.append([platform_x, platform_y, platform_move, ismoving])

    while playing:
        fps.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                opening = False
                playing = False
                gameover = False
                running = False

        for platform in platforms:
            if platform[2] == True:
                if platform[3] == 0:
                    if platform[0] + platform_width > screen_w:
                        platform[3] = 1
                    else:
                        platform[0] += platform_v
                if platform[3] == 1:
                    if platform[0] < 0:
                        platform[3] = 0
                    else:
                        platform[0] -= platform_v
                
        if circle_y > screen_h:
                playing = False
                gameover = True
        if not jumping:
            sound.play()
            jumping = True
            v = -13
        circle_y += v
        v += 0.25


        if v >= 0:
            for platform in platforms:
                platform_x, platform_y = platform[0], platform[1]
                if  platform_y + 5 >= circle_y + circle_r >= platform_y - 5 and circle_x + circle_r > platform_x and circle_x - circle_r < platform_x + platform_width:
                    distance.append(platform[1] - 750)
                    jumping = False
                    
                    for platform in platforms:
                        platform[1] += math.fabs(distance[1])
                        if platform[1] > screen_h:
                            platform[1] = platform[1] - screen_h
                            platform[0] = random.randint(0, screen_w - platform_width)
                            if random.randint(1, 2) == 1:
                                platform[2] = True
                            else:
                                platform[2] = False
                    circle_y = platform_y - circle_r + math.fabs(- distance[1])
                    score += (math.fabs(distance[0] - distance[1]))//100
                    if distance[1] < 0:
                        distance[1] = 0
                    distance.remove(distance[0])

        if pygame.key.get_pressed()[pygame.K_a] == True or pygame.key.get_pressed()[pygame.K_LEFT] == True:
            circle_x -= 4
        if pygame.key.get_pressed()[pygame.K_d] == True or pygame.key.get_pressed()[pygame.K_RIGHT] == True:
            circle_x += 4
        if circle_x - circle_r >= screen_w:
            circle_x = circle_r
        if circle_x + circle_r <= 0:       
            circle_x = screen_w - circle_r

        screen.fill((0,0,0))
        for platform in platforms:
            pygame.draw.rect(screen, (255, 255, 255), (platform[0], platform[1], platform_width, platform_height))
        pygame.draw.circle(screen, (255,255,255), (circle_x, circle_y), circle_r)
        score_text = click_font.render(str(int(score)), False, (255,255,255))
        screen.blit(score_text, (0,0))
        pygame.display.update()
    

    while gameover:
        score_gameovertext = score_font.render(str(int(score)), False, (255,255,255))
        bestscore_gameovertext = score_font.render(str(int(float(bestscore))), False, (255,255,255))
        score_scoretext = click_font.render("score", False, (255,255,255))
        bestscore_text = click_font.render("best", False, (255,255,255))
        with open('bestscore.txt', 'r') as file:
            bestscore = file.read()
        if score > float(bestscore):
            bestscore.replace(bestscore, '')
            with open('bestscore.txt', 'w') as file:
                file.write(str(score))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                opening = False
                playing = False
                gameover = False
                running = False 
            if event.type == pygame.MOUSEBUTTONDOWN:
                gameover = False
                opening = False
                playing = True

        screen.fill((0,0,0))
        screen.blit(bestscore_text, (40, 300))
        screen.blit(bestscore_gameovertext, (40, 400))
        screen.blit(score_scoretext, (screen_w//2 + 40, 300))
        screen.blit(score_gameovertext, (screen_w//2 + 40, 400))
        screen.blit(gameover_text,(30, 100))
        screen.blit(restart_text, (120, 600))
        pygame.display.flip()

pygame.quit()
