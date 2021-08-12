#https://www.youtube.com/watch?v=jO6qQDNa2UY&list=WL&index=1
import pygame
pygame.font.init()
pygame.mixer.init()

WIDTH, HIGHT= 900,650
WIN = pygame.display.set_mode((WIDTH,HIGHT))
pygame.display.set_caption("First game")

WHITE=(255,255,255) # win background
BLACK=(0,0,0) #border color
RED= (255,0,0)
YELLOW= (255,255,0)
HEALTH_FONT = pygame.font.SysFont('comicsans', 40, bold=True)
WINNER_FONT = pygame.font.SysFont('comicsans', 100, bold=True)

BORDER= pygame.Rect(WIDTH//2-5, 0, 10, HIGHT)
YELLOW_HIT= pygame.USEREVENT +1
RED_HIT = pygame.USEREVENT +2

BULLET_HIT_SOUND=pygame.mixer.Sound((r'Assets\Grenade+1.mp3'))
BULLET_FIRE_SOUND=pygame.mixer.Sound((r'Assets\Gun+Silencer.mp3'))

FPS=60
vel=5
BULLET_VEL=8
MAX_BULLETS= 3
SPACESHIP_WIDTH,SPACESHIP_HEIGHT= 60, 55


YELLOW_SPACESHIP_IMAGE = pygame.image.load(r'D:\py_game1\Assets\spaceship_yellow.png')
YELLOW_SPACESHIP= pygame.transform.rotate(
    pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(r'D:\py_game1\Assets\spaceship_red.png')
RED_SPACESHIP= pygame.transform.rotate(
    pygame.transform.scale(RED_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)), 270)

SPACE=pygame.transform.scale(pygame.image.load(r'Assets\space.png'),(WIDTH,HIGHT))


def draw_window(red, yellow, red_bullets, yellow_bullets,red_health,yellow_health):
    WIN.blit(SPACE,(0,0))
    pygame.draw.rect(WIN,BLACK,BORDER)
    red_health_text=HEALTH_FONT.render("Health: "+str(red_health),1,WHITE)
    yellow_health_text=HEALTH_FONT.render("Health: "+str(yellow_health),1,WHITE)
    WIN.blit(red_health_text,(WIDTH-red_health_text.get_width()-10,10))
    WIN.blit(yellow_health_text,(10,10))
    WIN.blit(RED_SPACESHIP,(red.x,red.y))
    WIN.blit(YELLOW_SPACESHIP,(yellow.x,yellow.y))


    for bullet in yellow_bullets:
        pygame.draw.rect(WIN,YELLOW,bullet)
   
    for bullet in red_bullets:
        pygame.draw.rect(WIN,RED,bullet)

    pygame.display.update()

def yellow_heandel_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x- vel > 0 :  #left
        yellow.x-=vel
    if keys_pressed[pygame.K_d] and yellow.x + vel + yellow.width < BORDER.x :  #right
        yellow.x+=vel
    if keys_pressed[pygame.K_w] and yellow.y - vel > 0 :  #up
        yellow.y-=vel
    if keys_pressed[pygame.K_s] and yellow.y + vel + yellow.width < HIGHT:  #down
        yellow.y+=vel
        

def red_heandel_movement(keys_pressed, red):

    if keys_pressed[pygame.K_LEFT] and red.x - vel > BORDER.x + BORDER.width:  #left
        red.x-=vel
    if keys_pressed[pygame.K_RIGHT] and red.x + vel+ red.width < WIDTH :  #right
        red.x+=vel
    if keys_pressed[pygame.K_UP] and red.y - vel > 0 : #up 
        red.y-=vel
    if keys_pressed[pygame.K_DOWN] and red.y + vel + red.width < HIGHT:  #down
        red.y+=vel


def heandel_bullets(yellow_bullets,red_bullets,yellow, red):
    for bullet in yellow_bullets:
        bullet.x+=BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x>WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x-=BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x<0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text=WINNER_FONT.render(text,1,WHITE)
    WIN.blit(draw_text,(WIDTH//2-draw_text.get_width()//2,HIGHT//2-draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    red=pygame.Rect(700,300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow=pygame.Rect(100,400, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    
    red_bullets=[]
    yellow_bullets=[]
    yellow_health,red_health=10,10
    
    clock= pygame.time.Clock()
    run=True
    while(run):
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                run= False
                pygame.quit()

            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LCTRL and len(yellow_bullets)<MAX_BULLETS:
                    bullet= pygame.Rect(yellow.x + yellow.width//2, yellow.y + yellow.height//2 , 10 , 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                
                if event.key==pygame.K_RCTRL and len(red_bullets)<MAX_BULLETS:
                    bullet= pygame.Rect(red.x + red.width//2, red.y + red.height//2 , 10 , 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type==RED_HIT:
                red_health-=1 
                BULLET_HIT_SOUND.play()
            if event.type==YELLOW_HIT:
                yellow_health-=1
                BULLET_HIT_SOUND.play()
        
        winner_text=""       
        if red_health<=0:
            winner_text="Yellow Wins !"
        if yellow_health<=0:
             winner_text="Red Wins !"
        if  winner_text!="":
            draw_winner(winner_text)
            break


        keys_pressed= pygame.key.get_pressed()
        yellow_heandel_movement(keys_pressed,yellow)
        red_heandel_movement(keys_pressed,red)
        heandel_bullets(yellow_bullets, red_bullets,yellow,red)
        draw_window(red, yellow,red_bullets,yellow_bullets,red_health,yellow_health)
    main()


if __name__== "__main__":
    main()

