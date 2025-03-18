import pygame
import datetime
import pytz

pygame.init()
screen = pygame.display.set_mode((1000, 800))
ticks = pygame.time.Clock()
done = False

font = pygame.font.Font(None, 50)

clock = pygame.image.load(r"C:/Users/Asus/Documents/Little/PP2/lab7/images/mainclock.png")
secunda = pygame.image.load(r"C:/Users/Asus/Documents/Little/PP2/lab7/images/leftarm.png")
minuta = pygame.image.load(r"C:/Users/Asus/Documents/Little/PP2/lab7/images/rightarm.png")

clock = pygame.transform.smoothscale(clock, (1000, 800))

def blit_rotate_center(surf, image, center, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=center)
    surf.blit(rotated_image, new_rect.topleft)

while not done:
    ticks.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill((255, 255, 255))

    tz = pytz.timezone("Asia/Almaty")
    now = datetime.datetime.now(tz)
    secunda_angle = -now.second * 6
    minuta_angle = -now.minute * 6

    screen.blit(clock, (0, 0))
    
    blit_rotate_center(screen, secunda, (500, 400), secunda_angle)
    blit_rotate_center(screen, minuta, (500, 400), minuta_angle)
    
    text_string = now.strftime("%H:%M:%S")
    text_surface = font.render(text_string, True, (0, 0, 0))
    screen.blit(text_surface, (screen.get_width() // 2 - text_surface.get_width() // 2, 750))
    
    pygame.display.flip()

pygame.quit()