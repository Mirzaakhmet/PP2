import pygame
import sys
from pygame import mixer

pygame.init()
mixer.init()
screen = pygame.display.set_mode((600, 173))
done = False

past_img = pygame.image.load(r"C:/Users/Asus/Documents/Little/PP2/lab7/images/past.jpg")
past2_img = pygame.image.load(r"C:/Users/Asus/Documents/Little/PP2/lab7/images/past2.png")
play_img = pygame.image.load(r"C:/Users/Asus/Documents/Little/PP2/lab7/images/play.jpg")
play2_img = pygame.image.load(r"C:/Users/Asus/Documents/Little/PP2/lab7/images/play2.png")
next_img = pygame.image.load(r"C:/Users/Asus/Documents/Little/PP2/lab7/images/next.jpg")
next2_img = pygame.image.load(r"C:/Users/Asus/Documents/Little/PP2/lab7/images/next2.png")
stop_img = pygame.image.load(r"C:/Users/Asus/Documents/Little/PP2/lab7/images/stop.jpg")
stop2_img = pygame.image.load(r"C:/Users/Asus/Documents/Little/PP2/lab7/images/stop2.png")

width = screen.get_width()
height = screen.get_height()

while not done:
    screen.fill((255, 255, 255)) 

    mouse = pygame.mouse.get_pos() 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if width / 3 <= mouse[0] <= width / 1.5 and 0 <= mouse[1] <= height:
                screen.blit(stop_img, (200, 0))
                

    screen.blit(past_img, (0, 0))

    if width / 3 <= mouse[0] <= width / 1.5 and 0 <= mouse[1] <= height:
        screen.blit(play2_img, (200, 0)) 
    else:
        screen.blit(play_img, (200, 0))
    
    screen.blit(next_img, (400, 0))

    pygame.display.update() 

pygame.quit()
