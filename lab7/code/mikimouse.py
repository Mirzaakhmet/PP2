import pygame
import datetime

pygame.init()
screen = pygame.display.set_mode((1000, 800))
ticks = pygame.time.Clock()
done = False

font = pygame.font.Font(None, 50)

clock = pygame.image.load(r"C:/Users/Asus/Documents/Little/PP2/lab7/images/mainclock.png")
secunda = pygame.image.load(r"C:/Users/Asus/Documents/Little/PP2/lab7/images/leftarm.png")
minuta = pygame.image.load(r"C:/Users/Asus/Documents/Little/PP2/lab7/images/rightarm.png")

clock = pygame.transform.smoothscale(clock, (1000, 800))

while not done:
    ticks.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill((255, 255, 255)) 

    now = datetime.datetime.now()
    secunda_angle = -now.second * 6
    minuta_angle = -now.minute * 6 - now.second * 0.1

    screen.blit(clock, (0, 0))

    rotated_sec = pygame.transform.rotate(secunda, secunda_angle)
    rotated_min = pygame.transform.rotate(minuta, minuta_angle)

    sec_centr = rotated_sec.get_rect(center=(500, 400))
    min_centr = rotated_min.get_rect(center=(500, 400))

    screen.blit(rotated_min, min_centr.topleft)
    screen.blit(rotated_sec, sec_centr.topleft)

    text_string = now.strftime("%H:%M:%S")
    text_surface = font.render(text_string, True, (0, 0, 0))
    screen.blit(text_surface,(screen.get_width() // 2 - text_surface.get_width() // 2, 750))


    pygame.display.flip()

pygame.quit()