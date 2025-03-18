import pygame
import sys
import os
from pygame import mixer

pygame.init()
mixer.init()

screen = pygame.display.set_mode((600, 173))
pygame.display.set_caption("MP3 Player ежже")

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

music_folder = "C:/Users/Asus/Documents/Little/PP2/lab7/music/"
playlist = [os.path.join(music_folder, f) for f in os.listdir(music_folder) if f.endswith(".mp3")]

nomer = 0 
is_playing = False
is_paused = False
paused_pos = 0
mixer.music.set_volume(0.5)

def load_and_play():
    global is_playing, is_paused, paused_pos
    try:
        mixer.music.load(playlist[nomer])
        mixer.music.play(start=paused_pos if is_paused else 0)
        is_playing = True
        is_paused = False
    except pygame.error:
        print(f"Ошибка: файл {playlist[nomer]} не найден")

while True:
    screen.fill((255, 255, 255))  
    mouse = pygame.mouse.get_pos()  

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Play/Pause
            if width / 3 <= mouse[0] <= width / 1.5 and 0 <= mouse[1] <= height:
                if not is_playing:
                    load_and_play()
                elif is_paused:
                    mixer.music.unpause()
                    is_paused = False
                else:
                    paused_pos = mixer.music.get_pos() / 1000
                    mixer.music.pause()
                    is_paused = True

            # Stop
            elif width / 3 <= mouse[0] <= width / 1.5 and 0 <= mouse[1] <= height:
                mixer.music.stop()
                is_playing = False
                is_paused = False
                paused_pos = 0

            # Next
            elif width / 1.5 <= mouse[0] <= width and 0 <= mouse[1] <= height:
                nomer = (nomer + 1) % len(playlist)
                load_and_play()

            # Previous
            elif 0 <= mouse[0] <= width / 3 and 0 <= mouse[1] <= height:
                nomer = (nomer - 1) % len(playlist)
                load_and_play()

    # Past
    if 0 <= mouse[0] <= width / 3 and 0 <= mouse[1] <= height:
        screen.blit(past2_img, (0, 0))
    else:
        screen.blit(past_img, (0, 0))

    # Play/Pause
    if width / 3 <= mouse[0] <= width / 1.5 and 0 <= mouse[1] <= height:
        screen.blit(play2_img if not is_playing or is_paused else stop2_img, (width / 3, 0))
    else:
        screen.blit(play_img if not is_playing or is_paused else stop_img, (width / 3, 0))

    # Next
    if width / 1.5 <= mouse[0] <= width and 0 <= mouse[1] <= height:
        screen.blit(next2_img, (width / 1.5, 0))
    else:
        screen.blit(next_img, (width / 1.5, 0))

    pygame.display.update()