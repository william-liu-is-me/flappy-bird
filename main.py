import pygame, sys,random


def create_pipe(centery):
    bottom_pipe = pipe_picture.get_rect(midtop = (600,centery))#bottom pipe
    top_pipe = pipe_picture.get_rect(midbottom = (600,centery-200))#top pipe
    return bottom_pipe, top_pipe

def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 3
    return pipes

def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >900:
            screen.blit(pipe_picture,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_picture,False,True)
            screen.blit(flip_pipe,pipe)

def delete_pipe(pipes):
    for pipe in pipes:
        if pipe.right< -50:
            pipes.remove(pipe)
            point_sound.play()
            return 1
    return 0



def check_collision(pipes):
    for pipe in pipes:
        if pipe.right >= bird_rect.left:
            if bird_rect.colliderect(pipe):
                play_hit_sound()
                return True

    if bird_rect.top <= -50 or bird_rect.bottom >= 950:
        hit_sound.play()
        return True
    else:
        return False

def rotate_bird(bird):
    new_bird_picture = pygame.transform.rotozoom(bird,-bird_movement*3,1)
    return new_bird_picture

def flap_animation():
    global bird_rect
    global bird_index
    global bird_picture
    if bird_index <= 2:
        bird_picture = bird_list[bird_index]
        bird_rect = bird_picture.get_rect(center = (100,bird_rect.centery))
        bird_index +=1
    else:
        bird_index = 0
    return bird_picture,bird_rect
def score_display():
    #score_surface = game_font.render(f'Score: {str(int(count/2))}',True,(255,255,255))
    #score_rect = score_surface.get_rect(center = (288, 100))
    #screen.blit(score_surface,score_rect)
    score = int(count/2)
    if score < 10:
        number_rect = picture_list[score].get_rect(center = (300, 100))
        screen.blit(picture_list[score],number_rect)
    elif 9 < score<100:
        first_number = score//10
        sec_number = score % 10
        first_number_rect = picture_list[first_number].get_rect(center=(576/2 - 25,100))
        sec_number_rect = picture_list[sec_number].get_rect(center = (576/2 + 25,100))
        screen.blit(picture_list[first_number],first_number_rect)
        screen.blit(picture_list[sec_number],sec_number_rect)

def play_hit_sound():
    global first_hit
    if first_hit == True:
        hit_sound.play()
        first_hit = False

pygame.mixer.pre_init(frequency = 22050, size = -16, channels = 1, buffer = 256)
pygame.init()#still work without it.
screen = pygame.display.set_mode((576,900))#this is to create a canvas to draw
#game_font = pygame.font.SysFont('ornanong',40)#cannot find the font
bg_picture = pygame.image.load('pictures/background-day.png').convert()#load the picture
bg_picture = pygame.transform.scale2x(bg_picture)

floor_picture = pygame.image.load('pictures/base.png')
floor_picture = pygame.transform.scale2x(floor_picture)
floor_pos_x = 0

#import 3 different pics for flap --- animation later
mid_bird_picture = pygame.image.load('pictures/bluebird-midflap.png')
up_bird_picture = pygame.image.load('pictures/bluebird-upflap.png')
down_bird_picture = pygame.image.load('pictures/bluebird-downflap.png')
mid_bird_picture = pygame.transform.scale2x(mid_bird_picture).convert()
up_bird_picture = pygame.transform.scale2x(up_bird_picture).convert()
down_bird_picture = pygame.transform.scale2x(down_bird_picture).convert()
bird_list = [mid_bird_picture,up_bird_picture,down_bird_picture]

bird_index = 0
bird_picture = bird_list[bird_index]
bird_rect = bird_picture.get_rect(center=(100,450))
#bird_picture = pygame.image.load('pictures/bluebird-midflap.png')
#bird_picture = pygame.transform.scale2x(bird_picture)#same as above
#bird_rect = bird_picture.get_rect(center = (100,450))#add an invisible rect around the picture ofr collision check later, and location

pipe_picture = pygame.image.load('pictures/pipe-green.png').convert()
pipe_picture = pygame.transform.scale2x(pipe_picture)

#number picture
picture_0 = pygame.transform.scale2x(pygame.image.load(f'pictures/0.png').convert_alpha())
picture_1 = pygame.transform.scale2x(pygame.image.load(f'pictures/1.png').convert_alpha())
picture_2 = pygame.transform.scale2x(pygame.image.load(f'pictures/2.png').convert_alpha())
picture_3 = pygame.transform.scale2x(pygame.image.load(f'pictures/3.png').convert_alpha())
picture_4 = pygame.transform.scale2x(pygame.image.load(f'pictures/4.png').convert_alpha())
picture_5 = pygame.transform.scale2x(pygame.image.load(f'pictures/5.png').convert_alpha())
picture_6 = pygame.transform.scale2x(pygame.image.load(f'pictures/6.png').convert_alpha())
picture_7 = pygame.transform.scale2x(pygame.image.load(f'pictures/7.png').convert_alpha())
picture_8 = pygame.transform.scale2x(pygame.image.load(f'pictures/8.png').convert_alpha())
picture_9 = pygame.transform.scale2x(pygame.image.load(f'pictures/9.png').convert_alpha())

picture_list = [picture_0,picture_1,picture_2,picture_3,picture_4,picture_5,
                picture_6,picture_7,picture_8,picture_9 ]
#number picture end


pipe_list = []
clock = pygame.time.Clock()#(this is to control the fps, not too high)
FLAPBIRD = pygame.USEREVENT+1 #flap animation
pygame.time.set_timer(FLAPBIRD,100)
SPAWNPIPE = pygame.USEREVENT#timer for every xx seconds
pygame.time.set_timer(SPAWNPIPE,1500)

#now we need some variables.
gravity = 0.15
bird_movement = 0
count= 0
flap_sound = pygame.mixer.Sound('audio/wing.wav')
hit_sound = pygame.mixer.Sound('audio/hit.wav')
first_hit = True
point_sound = pygame.mixer.Sound('audio/point.wav')
#background_sound = pygame.mixer.Sound('audio/background_sound.mp3')
pygame.mixer.music.load('audio/background_sound.mp3')
pygame.mixer.music.play(-1)
#background_sound.play()
while True:
    screen.blit(bg_picture,(0,0))
    #draw the picture onto the canvas(surface)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and check_collision(pipe_list) == False:
                bird_movement = 0
                bird_movement -= 4.5
                flap_sound.play()

            if event.key == pygame.K_SPACE and check_collision(pipe_list) ==True:
                pipe_list.clear()
                check_collision(pipe_list)
                bird_rect = bird_picture.get_rect(center = (100,450))
                bird_movement = 0
                count = 0
                first_hit = True

        if event.type == SPAWNPIPE:

            centery = random.randrange(400,550)
            new_pipe = create_pipe(centery)
            pipe_list.extend(new_pipe)#extend list with two new items, instead of append

        if event.type == FLAPBIRD:
            bird_picture, bird_rect = flap_animation()

    if not check_collision(pipe_list):#check if this game should continue(false is continue)
        #pipe
        move_pipe(pipe_list)
        draw_pipe(pipe_list)

        count = count + delete_pipe(pipe_list)



        #pipe end

        #bird
        rotated_bird = rotate_bird(bird_picture)
        screen.blit(rotated_bird,bird_rect)#draw the picture, place it as the rect
        bird_movement += gravity#gravity makes birds down
        bird_rect.centery += bird_movement#bird actaully down
        #bird end
    else:
        #this is game pause

        game_pause_picture = pygame.image.load('pictures/message.png').convert_alpha()
        game_pause_picture = pygame.transform.scale2x(game_pause_picture)
        game_pause_rect = game_pause_picture.get_rect(center = (288,450))
        screen.blit(game_pause_picture,game_pause_rect)
        #game pause end


    #floor
    floor_pos_x -= 1#the floor move towards left
    screen.blit(floor_picture,(floor_pos_x,750))
    if floor_pos_x <= -576/6:
        floor_pos_x = 1#reset the floor position if it moves too left.
    #floor end

    #score
    score_display()
    #score end

    pygame.display.update()#this is drawing
    clock.tick(120)#control the fps
