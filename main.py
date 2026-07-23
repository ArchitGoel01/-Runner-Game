import pygame
from sys import exit 
from random import randint
pygame.init()
width=800
height=400
screen=pygame.display.set_mode((width,height)) 
game_active=False
    
pygame.display.set_caption("runner")

#sounds
jump_sound=pygame.mixer.Sound("audio/jump.mp3")
jump_sound.set_volume(0.4)
bg_music=pygame.mixer.Sound("audio/music.wav")
bg_music.play()
bg_music.set_volume(0.4)

clock=pygame.time.Clock()

w=800
h=400

test_surface=pygame.Surface((w,h))
test_surface.fill("blue")
ground = pygame.image.load("graphics\ground.png").convert()
sky = pygame.image.load("graphics\sky.png").convert()

player_walk1=pygame.image.load("graphics\player_walk_1.png").convert_alpha()
player_walk2=pygame.image.load("graphics\player_walk_2.png").convert_alpha()
player_walk=[player_walk1,player_walk2]
player_index=0
player_jump=pygame.image.load("graphics\jump.png").convert_alpha()

player_stand=pygame.image.load("graphics\player_stand.png").convert_alpha()
player_stand=pygame.transform.rotozoom(player_stand,0,2)# increase scale

player_surface=player_walk[player_index]

#creating rectangles
player_rect=player_surface.get_rect(midbottom=(50,300))
stand_rect=player_stand.get_rect(center=(400,200))

#obstacles
snail_frame1=pygame.image.load("graphics\snail1.png").convert_alpha()
snail_frame2=pygame.image.load("graphics\snail2.png").convert_alpha()
snail_frames=[snail_frame1,snail_frame2]
snail_frame_index=0
snail_surface=snail_frames[snail_frame_index]

fly_frame1=pygame.image.load("graphics\Fly1.png").convert_alpha()
fly_frame2=pygame.image.load("graphics\Fly2.png").convert_alpha()
fly_frames=[fly_frame1,fly_frame2]
fly_frame_index=0
fly_surface=fly_frames[fly_frame_index]


snail_rect=snail_surface.get_rect(midbottom=(800,300))

obstacle_rect_list=[]

#font
test=pygame.font.Font("graphics\Pixeltype.ttf",50)

intro_surf=test.render(f"Runner Game",True,"black")
intro_rect=intro_surf.get_rect(center=(400,75))

start_surf=test.render(f"Press space to start",True,"black")
start_rect=start_surf.get_rect(center=(400,350))

player_gravity = 0
start_time=0
score=0

#timer
obstacle_timer=pygame.USEREVENT +1
pygame.time.set_timer(obstacle_timer,1400) 

snail_animation_timer=pygame.USEREVENT +2
pygame.time.set_timer(snail_animation_timer,500)

fly_animation_timer=pygame.USEREVENT +3
pygame.time.set_timer(fly_animation_timer,100)

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x-=5
            
            if obstacle_rect.bottom ==300:
                screen.blit(snail_surface,obstacle_rect)
            else:
                screen.blit(fly_surface,obstacle_rect)
        obstacle_list=[obstacle for obstacle in obstacle_list if obstacle.x>-100]
        return obstacle_list
    else: return []  

def display_score():
    current_time=int(pygame.time.get_ticks()/1000)-start_time
    score_surf=test.render(f"SCORE:{current_time}",True,(64,64,64))
    score_rect=score_surf.get_rect(center=(400,50))
    screen.blit(score_surf,score_rect)
    return current_time

def collision(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True            

def player_animation():
    global player_surface,player_index
    if player_rect.bottom<300:
        player_surface=player_jump
    else:
        player_index+=0.1
        if player_index >= len(player_walk):player_index=0
        player_surface=player_walk[int(player_index)]

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit() 

        if game_active:
            if event.type==pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos): 
                    if player_rect.bottom==300:
                        player_gravity = -20
                        jump_sound.play()
            if event.type==pygame.KEYDOWN :
                if event.key==pygame.K_SPACE or event.key==pygame.K_UP: 
                    if player_rect.bottom==300:
                        player_gravity = -20
                        jump_sound.play()
        else:
            if event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE:
                game_active=True
                snail_rect.left=800
                start_time=int(pygame.time.get_ticks()/1000)
        if game_active:
            if event.type==obstacle_timer:
                if randint(0,2):
                    obstacle_rect_list.append(snail_surface.get_rect(midbottom=(randint(900,1100),300)))
                else:
                    obstacle_rect_list.append(fly_surface.get_rect(midbottom=(randint(900,1100),210)))
            
            if event.type==snail_animation_timer:
                if snail_frame_index==0: snail_frame_index=1
                else: snail_frame_index=0
                snail_surface=snail_frames[snail_frame_index]
            
            if event.type==fly_animation_timer:
                if fly_frame_index==0: fly_frame_index=1
                else: fly_frame_index=0
                fly_surface=fly_frames[fly_frame_index]

    if game_active:
        screen.blit(ground,(0,300))
        screen.blit(sky,(0,0))
        
        score=display_score()
        with open("high_score.txt", "r") as file:
            if int(file.read())<score:
                with open("high_score.txt", "w") as file:
                    file.write(str(score))
        #player
        player_gravity+=1
        player_rect.y+=player_gravity
        if player_rect.bottom>=300: player_rect.bottom=300
        player_animation()
        screen.blit(player_surface,player_rect)

        #obstacle movement
        obstacle_rect_list=obstacle_movement(obstacle_rect_list)
        
        #collision
        game_active=collision(player_rect,obstacle_rect_list)
    else:
        #intro screen
        screen.fill((94,129,162))
        screen.blit(player_stand,stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom=(80,300)
        player_gravity=0
        with open("high_score.txt", "r") as file:
            highest_score=int(file.read())
        score_message=test.render(f"Highest Score:{highest_score}   Your Score :{score}",True,"black")
        score_message_rect=score_message.get_rect(center=(400,350))
        screen.blit(intro_surf,intro_rect)
        if score==0:
            screen.blit(start_surf,start_rect)
        else:
            screen.blit(score_message,score_message_rect)
    pygame.display.update()
    clock.tick(60)