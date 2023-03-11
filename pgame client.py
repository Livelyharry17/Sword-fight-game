import pygame, socket, threading, random

pygame.init()
clicked = True

hit_damage = 0
deaths = 0

font1 = pygame.font.SysFont("Ariel", 34)
font2 = pygame.font.SysFont("Ariel", 50)

list_pos = [50, 50]
_my_x, _my_y = 50, 50

other_pos = (50, 50)

health = 100
# add file location here

player = pygame.image.load("personal sprite.png")
player_rect = player.get_rect()

enemy = pygame.image.load("enemy sprite.png")
enemy_rect = enemy.get_rect()

player_rect.x = 200


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostbyname(socket.gethostname())
port = 10000
sock.connect((host, port))


def send_or_recv_pos():
    while True:
        global other_pos, list_pos, enemy_x, enemy_y, hit_damage, health
#        print(_my_pos)
        our_damage = 0
        my_pos = str(_my_x) + " " + str(_my_y) + " " + str(hit_damage)
        sock.send(my_pos.encode())
        other_player_pos = sock.recv(100)
        other_pos = other_player_pos.decode()
        list_pos = other_pos.split(" ", 2)
        enemy_x = int(list_pos[0])
        enemy_y = int(list_pos[1])
        our_damage = int(list_pos[2])
#        print(str(our_damage))
        health -= our_damage
#        hit_damage = 0

#        print(list_pos)


thread_1 = threading.Thread(target=send_or_recv_pos)
thread_1.start()


velocity_x = 4
velocity_y = 4

is_jump = False
jump_count = 10

background = pygame.display.set_mode((1024, 569))
pygame.display.set_caption("First Game")
background_image = pygame.image.load('game background1024_1.png')


running = True


def check_key_presses():
    if not player_rect.colliderect(enemy_rect):
        keys = pygame.key.get_pressed()
        if player_rect.x < 944:
            if keys[pygame.K_d]:
                player_rect.x += 3
                if not player_rect.colliderect(enemy_rect):
                    player_rect.x += velocity_x
                player_rect.x -= 3
        if player_rect.x > 0:
            if keys[pygame.K_a]:
                player_rect.x -= 3
                if not player_rect.colliderect(enemy_rect):
                    player_rect.x -= velocity_x
                player_rect.x += 3
        if player_rect.y < 489:
            if keys[pygame.K_s]:
                player_rect.y += 3
                if not player_rect.colliderect(enemy_rect):
                    player_rect.y += velocity_y
                player_rect.y -= 3
        if player_rect.y > 0:
            if keys[pygame.K_w]:
                player_rect.y -= 3
                if not player_rect.colliderect(enemy_rect):
                    player_rect.y -= velocity_y
                player_rect.y += 3

    # player collisions


def hit():
    global hit_damage, velocity_x, velocity_y
    while True:
        velocity_x =4
        velocity_y = 4
        hit_damage = 0
        mouse_pos = pygame.mouse.get_pos()
        collide = enemy_rect.collidepoint(mouse_pos)
        mouse_button_clicked = pygame.mouse.get_pressed()
        if collide and mouse_button_clicked[0]:
            velocity_x /= 2
            velocity_y /= 2
            hit_damage = 10
            pygame.time.wait(10)
            hit_damage = 0
            pygame.time.wait(490)
            hit_damage = 0


def respawn():
    global health, deaths
    if health <= 0:
        player_rect.x = random.randint(0, 944)
        player_rect.y = random.randint(0, 516)
        while player_rect.colliderect(enemy_rect):
            player_rect.x = random.randint(0, 944)
            player_rect.y = random.randint(0, 516)
        health = 100
        deaths += 1

thread_2 = threading.Thread(target=hit)
thread_2.start()

while running:
    pygame.time.delay(10)
    background.blit(background_image,(0,0))

    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            running = False
# key events

    _my_x, _my_y = player_rect.x, player_rect.y
    enemy_x = int(list_pos[0])
    enemy_y = int(list_pos[1])
    enemy_rect.x = enemy_x
    enemy_rect.y = enemy_y
    check_key_presses()
    respawn()
    health_bar1 = font1.render('Health: ', True, (0, 0, 225))
    health_bar2 = font2.render(str(health), True, (0, 0, 225))
    death_bar1 = font1.render('Deaths: ', True, (225, 0, 0))
    death_bar2 = font2.render(str(deaths), True, (225, 0, 0))
    background.blit(enemy, enemy_rect)
    background.blit(player, player_rect)
    background.blit(health_bar1, (910, 20))
    background.blit(health_bar2, (920, 48))
    background.blit(death_bar1, (910, 88))
    background.blit(death_bar2, (920, 116))
    pygame.display.flip()
    pygame.display.update()
#    print("refreshed")
