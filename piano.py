import pygame
import csv
import os

pygame.init()

SCREEN_HEIGHT = 500     
SCREEN_WIDTH = 900

BG_COLOR = (100, 200, 200, 1)
BLACK = (1,1,1,1)
WHITE = (255,255,255,1)
GREY = (155,155,155,1)
BLUE = (120,120,200,1)
NORM_BLUE = (130,130,250,1)
DEEP_BLUE = (50,50,200,1)
WHITE_CLICKED = (220,220,220,1)
BLACK_CLICKED = (50,50,50,1)
BLACK_TILE = (20,20,20,1)
TILE_COLOR = (250,250,220,1)
TILE_CLICKED = (230,230,200,1)

key_caption_list = ['Doh', 'Reh', 'Mi', 'Fa', 'Soh', 'La', 'Ti', 'Doh']
white_key_alp = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k']
black_key_alp = ['w', 'e', 't', 'y', 'u']

TILE_WIDTH = (SCREEN_WIDTH-200) / 8
BLACK_TILE_WIDTH = TILE_WIDTH-20

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.RESIZABLE)
pygame.display.set_caption('KEYBOARD')

clock = pygame.time.Clock()
FPS = 60
sounds = [[],[]]
#sounds
for i in range(8):
    new_sound = pygame.mixer.Sound(f'sounds\w3{i}.wav')
    sounds[0].append(new_sound)
for i in range(5):
    new_sound = pygame.mixer.Sound(f'sounds\\b3{i}.wav')
    sounds[1].append(new_sound)
pygame.mixer.set_num_channels(24)

tile_clicked = [[0 for i in range(8)],[0 for i in range(5)]]
last_clicked_tile = [[0 for i in range(8)],[0 for i in range(5)]]
tiles = [[None for i in range(8)],[None for i in range(5)]]

black_button_pressed = False

#button variables
stopper = 5
#record variables
recording = False
playing = False
recorded_lists = []
played_lists = []
playing_counter = 0
playlist = os.listdir(f'my_record')
playlist_counter = 0
playlist_rect = []
chosen_record = 0
scroll = 0

record_name = ''

save_menu = False
play_menu = False
typing = False

def draw_bg():
    screen.fill(BG_COLOR)
      
def text_objects(text, font,color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def button(msg,x,y,w,h,ic,ac,bc,action=None):
    global stopper
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))
        if click[0] == 1 and action != None :
            if stopper > 4:
                action()
            stopper -= 1
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))
    pygame.draw.rect(screen, bc,(x,y,w,h),3)
    smallText = pygame.font.SysFont("cursive",20)
    textSurf, textRect = text_objects(msg, smallText, BLACK)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(textSurf, textRect)

def writeText(msg, center_x, center_y, msg_color=BLACK):
    smallText = pygame.font.SysFont("cursive",20)
    textSurf, textRect = text_objects(msg, smallText, msg_color)
    textRect.center = ( center_x, center_y )

    screen.blit(textSurf, textRect)
def record():
    global recording
    global save_menu
    stop_playing()

    if recording == False:
        recording = True
    else:
        recording = False
        save_menu = True
        
def play():
    global playing
    global play_menu
    global scroll
    global played_lists
    if playing == False:
        playing = True
        with open(f'my_record/{playlist[playlist_counter]}', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                play_list = []
                for j in row:
                    play_list.append(int(j))
                played_lists.append(play_list)
        play_menu = False
        scroll = 0
    else:
        played_lists = []
        playing = False

def stop_playing():
    global playing
    global playing_counter
    global last_clicked_tile
    global tile_clicked
    global played_lists

    playing = False
    playing_counter = 0
    played_lists = []
    last_clicked_tile = [[0 for i in range(8)],[0 for i in range(5)]]
    tile_clicked = [[0 for i in range(8)],[0 for i in range(5)]]

def recorder():
    record_list = []
    for i in tile_clicked:
        for j in i:
            record_list.append(j)
    recorded_lists.append(record_list)

def show_save_menu():
    global save_menu
    save_menu = True

def show_play_menu():
    global play_menu
    play_menu = True

def exit_save_menu():
    global save_menu
    save_menu = False

def exit_play_menu():
    global play_menu
    global scroll
    play_menu = False
    scroll = 0

def save_record():
    global save_menu
    global record_name
    global recorded_lists
    with open(f'my_record/{record_name}.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            for row in recorded_lists:
                writer.writerow(row)
    record_name = ''
    save_menu = False
    recorded_lists = []


def draw_save_menu():
    if typing == False:
        color = WHITE_CLICKED
    else:
        color = WHITE
    if len(record_name) < 14:
        show_name = record_name
    else:
        show_name = record_name[(len(record_name)-13):len(record_name)]
    pygame.draw.rect(screen, WHITE,((SCREEN_WIDTH//2)-150,(SCREEN_HEIGHT//2)-100,300,200))
    button(show_name,(SCREEN_WIDTH//2)-100,210,200,30,color,color,BLACK,start_typing)
    button('save',(SCREEN_WIDTH//2)-100,250,200,30,WHITE_CLICKED,WHITE,BLACK,save_record)
    button('x',(SCREEN_WIDTH//2)+120,(SCREEN_HEIGHT//2)-90,20,20,WHITE_CLICKED,WHITE,BLACK,exit_save_menu)

def draw_play_menu():
    global chosen_record
    global scroll
    global stopper
    global playlist_counter
    
    li_x = (SCREEN_WIDTH//2)-90
    li_y = (SCREEN_HEIGHT//2)-60
    pygame.draw.rect(screen, GREY,((SCREEN_WIDTH//2)-150,(SCREEN_HEIGHT//2)-100,300,200))
    pygame.draw.rect(screen, WHITE,((SCREEN_WIDTH//2)-100,(SCREEN_HEIGHT//2)-70,200,100))
    button('play',(SCREEN_WIDTH//2)-100,300,200,30,WHITE_CLICKED,WHITE,BLACK,play)
    button('x',(SCREEN_WIDTH//2)+120,(SCREEN_HEIGHT//2)-90,20,20,WHITE_CLICKED,WHITE,BLACK,exit_play_menu)

    pygame.draw.rect(screen, BLUE,(li_x-5,(li_y + (chosen_record*15)),180,15))

    
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if len(playlist) < 6:
        for i in range(len(playlist)):
            x = li_x
            y = li_y + (i*15)
            playlist_name = str(i+1)+ '. ' + playlist[i][:playlist[i].find('.')]
            playText = pygame.font.SysFont("cursive",20)
            textSurf, textRect = text_objects(playlist_name, playText, BLACK)
            playlist_rect.append(textRect)
            textRect.x = x
            textRect.y = y
            screen.blit(textSurf, textRect)
            if x+180 > mouse[0] > x and y+15 > mouse[1] > y:
                if click[0] == 1:
                    chosen_record = i
                    playlist_counter = i
    else:
        for i in range(5):
            x = li_x
            y = li_y + (i*15)
            new_playlist = playlist[scroll:5+scroll]
            current_playlist = new_playlist[i]
            ind = playlist.index(current_playlist)
            playlist_name = str(ind+1)+ '. ' + current_playlist[:current_playlist.find('.')]
            playText = pygame.font.SysFont("cursive",20)
            textSurf, textRect = text_objects(playlist_name, playText, BLACK)
            playlist_rect.append(textRect)
            textRect.x = x
            textRect.y = y
            screen.blit(textSurf, textRect)
            if x+180 > mouse[0] > x and y+15 > mouse[1] > y:
                if click[0] == 1:
                    chosen_record = i
                    playlist_counter = i + scroll
        move_up = pygame.draw.rect(screen, GREY,((SCREEN_WIDTH//2)+100-15,(SCREEN_HEIGHT//2)-65,11,40))
        move_down = pygame.draw.rect(screen, GREY,((SCREEN_WIDTH//2)+100-15,(SCREEN_HEIGHT//2)-15,11,40))
        if move_up.x+11 > mouse[0] > move_up.x and move_up.y+40 > mouse[1] > move_up.y:
                if click[0] == 1 and scroll > 0 and stopper > 4:
                    scroll -= 1
                    stopper -= 1
                    playlist_counter -= 1
        if move_down.x+11 > mouse[0] > move_down.x and move_down.y+40 > mouse[1] > move_down.y:
                if click[0] == 1 and scroll < len(playlist)-5 and stopper > 4:
                    scroll += 1
                    stopper -= 1
                    playlist_counter += 1

def start_typing():
    global typing
    if typing == True:
        typing = False
    else:
        typing = True

def draw_keyboard():
    playlist_name = playlist[playlist_counter][:playlist[playlist_counter].find('.')]
    if recording == False:
        record_btn = 'record'
    else:
        record_btn = 'stop'
        recorder()

    if playing == False:
        play_btn = 'play'
    else:
        play_btn = 'pause'
    button(record_btn,(SCREEN_WIDTH)-100,10,70,30,WHITE_CLICKED,WHITE,BLACK,record)
    button(play_btn,210,10,70,30,WHITE_CLICKED,WHITE,BLACK,play)
    button(playlist_name,10,10,203,30,WHITE_CLICKED,WHITE,BLACK,show_play_menu)
    if playing == True:
        button('stop',(SCREEN_WIDTH//2)+200,10,70,30,WHITE_CLICKED,WHITE,BLACK,stop_playing)


    for i,tile_index in enumerate(tile_clicked[0]):
        if tile_index == 0:
            tile = pygame.draw.rect(screen, TILE_COLOR, (100+(TILE_WIDTH*i),100,TILE_WIDTH,SCREEN_HEIGHT-200))
            writeText(white_key_alp[i],100+(TILE_WIDTH*i)+TILE_WIDTH//2, SCREEN_HEIGHT-130)
        elif tile_index == 1 or tile_index == 2:
            tile = pygame.draw.rect(screen, TILE_CLICKED, (100+(TILE_WIDTH*i),100,TILE_WIDTH,SCREEN_HEIGHT-200))
            writeText(white_key_alp[i],100+(TILE_WIDTH*i)+TILE_WIDTH//2, SCREEN_HEIGHT-130,DEEP_BLUE)
        tiles[0][i] = tile
        pygame.draw.rect(screen, BLACK, (100+(TILE_WIDTH*i),100,TILE_WIDTH,SCREEN_HEIGHT-200),1)
    for i,tile_index in enumerate(tile_clicked[1]):
        if i < 2:
            j = i
        else:
            j = i+1
        if tile_index == 0:
            black_tile = pygame.draw.rect(screen, BLACK_TILE, (100+(TILE_WIDTH*j)+TILE_WIDTH/2+10,100,BLACK_TILE_WIDTH,SCREEN_HEIGHT-300))
            writeText(black_key_alp[i],100+TILE_WIDTH/2+(TILE_WIDTH*j)+TILE_WIDTH//2, SCREEN_HEIGHT-220,WHITE)
        if tile_index == 1 or tile_index == 2:
            black_tile = pygame.draw.rect(screen, BLACK_CLICKED, (100+(TILE_WIDTH*j)+TILE_WIDTH/2+10,100,BLACK_TILE_WIDTH,SCREEN_HEIGHT-300))
            writeText(black_key_alp[i],100+TILE_WIDTH/2+(TILE_WIDTH*j)+TILE_WIDTH//2, SCREEN_HEIGHT-220,NORM_BLUE)
        tiles[1][i] = black_tile
    pygame.draw.rect(screen, BLACK, (100,100,SCREEN_WIDTH-200,SCREEN_HEIGHT-200),2)
    for keys_index in range(8):
        writeText(key_caption_list[keys_index], 100+(TILE_WIDTH*keys_index)+TILE_WIDTH//2,SCREEN_HEIGHT-80)

run = True
while run:
    clock.tick(FPS)
    playlist = os.listdir(f'my_record')
    draw_bg()

    draw_keyboard()

    if save_menu == True:
        draw_save_menu()

    if play_menu == True:
        draw_play_menu()

    if playing == True:
        for i in range(8):
            last_clicked_tile[0][i] = tile_clicked[0][i]
            tile_clicked[0][i] = played_lists[playing_counter][i]
            if last_clicked_tile[0][i] != 1 and tile_clicked[0][i] == 1:
                sounds[0][i].play()
        for i in range(5):
            last_clicked_tile[1][i] = tile_clicked[1][i]
            tile_clicked[1][i] = played_lists[playing_counter][i+8]
            if last_clicked_tile[1][i] != 1 and tile_clicked[1][i] == 1:
                sounds[1][i].play()
        if playing_counter < len(played_lists)-1:
            playing_counter += 1
        else:
            stop_playing()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if save_menu == False and play_menu == False:
                for i,tile in enumerate(tiles[1]):
                    if tile.collidepoint(event.pos):
                        black_button_pressed = True
                        if tile_clicked[1][i] == 0:
                            tile_clicked[1][i] = 1
                            sounds[1][i].play()
                        else:
                            tile_clicked[1][i] = 2
                for i,tile in enumerate(tiles[0]):
                    if tile.collidepoint(event.pos) and black_button_pressed == False:
                        if tile_clicked[0][i] == 0:
                            tile_clicked[0][i] = 1
                            sounds[0][i].play()
                        else:
                            tile_clicked[0][i] = 2
        
        if event.type == pygame.KEYDOWN:
            if save_menu == False and play_menu == False:
                if event.key == pygame.K_a:
                    tile_clicked[0][0] = 1
                    sounds[0][0].play()
                if event.key == pygame.K_s:
                    tile_clicked[0][1] = 1
                    sounds[0][1].play()
                if event.key == pygame.K_d:
                    tile_clicked[0][2] = 1
                    sounds[0][2].play()
                if event.key == pygame.K_f:
                    tile_clicked[0][3] = 1
                    sounds[0][3].play()
                if event.key == pygame.K_g:
                    tile_clicked[0][4] = 1
                    sounds[0][4].play()
                if event.key == pygame.K_h:
                    tile_clicked[0][5] = 1
                    sounds[0][5].play()
                if event.key == pygame.K_j:
                    tile_clicked[0][6] = 1
                    sounds[0][6].play()
                if event.key == pygame.K_k:
                    tile_clicked[0][7] = 1
                    sounds[0][7].play()

                if event.key == pygame.K_w:
                    tile_clicked[1][0] = 1
                    sounds[1][0].play()
                if event.key == pygame.K_e:
                    tile_clicked[1][1] = 1
                    sounds[1][1].play()
                if event.key == pygame.K_t:
                    tile_clicked[1][2] = 1
                    sounds[1][2].play()
                if event.key == pygame.K_y:
                    tile_clicked[1][3] = 1
                    sounds[1][3].play()
                if event.key == pygame.K_u:
                    tile_clicked[1][4] = 1
                    sounds[1][4].play()

            if event.key == pygame.K_BACKSPACE and len(record_name) >0 and typing == True:
                record_name = record_name[:len(record_name)-1]

        if event.type == pygame.MOUSEBUTTONUP:
            stopper = 5
            if save_menu == False and play_menu == False:
                for i,tile in enumerate(tiles[1]):
                    if tile.collidepoint(event.pos):
                        black_button_pressed = False
                        tile_clicked[1][i] = 0
                for i,tile in enumerate(tiles[0]):
                    if tile.collidepoint(event.pos):
                        tile_clicked[0][i] = 0

        if event.type == pygame.KEYUP:
            if save_menu == False and play_menu == False:
                if event.key == pygame.K_a:
                    tile_clicked[0][0] = 0
                if event.key == pygame.K_s:
                    tile_clicked[0][1] = 0
                if event.key == pygame.K_d:
                    tile_clicked[0][2] = 0
                if event.key == pygame.K_f:
                    tile_clicked[0][3] = 0
                if event.key == pygame.K_g:
                    tile_clicked[0][4] = 0
                if event.key == pygame.K_h:
                    tile_clicked[0][5] = 0
                if event.key == pygame.K_j:
                    tile_clicked[0][6] = 0
                if event.key == pygame.K_k:
                    tile_clicked[0][7] = 0
                
                if event.key == pygame.K_w:
                    tile_clicked[1][0] = 0
                if event.key == pygame.K_e:
                    tile_clicked[1][1] = 0
                if event.key == pygame.K_t:
                    tile_clicked[1][2] = 0
                if event.key == pygame.K_y:
                    tile_clicked[1][3] = 0
                if event.key == pygame.K_u:
                    tile_clicked[1][4] = 0

        if event.type == pygame.TEXTINPUT and save_menu == True and typing == True:
            record_name += event.text

    pygame.display.update()
pygame.quit()