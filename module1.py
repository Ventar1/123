import pygame
import random

# Inicjalizacja Pygame
pygame.init()

# Ustawienia ekranu
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Kolory
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (255, 0, 0)

# Ustawienia gry
clock = pygame.time.Clock()
FONT = pygame.font.SysFont('Arial', 30)

# Obrazki
BIRD_WIDTH = 34
BIRD_HEIGHT = 24
PIPE_WIDTH = 50
PIPE_HEIGHT = 300
PIPE_GAP = 200

bird_image = pygame.Surface((BIRD_WIDTH, BIRD_HEIGHT))
bird_image.fill(GREEN)

# Funkcja rysująca ptaka
def draw_bird(bird):
    screen.blit(bird_image, bird)

# Funkcja rysująca rury
def draw_pipes(pipes):
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, pipe)

# Funkcja sprawdzająca kolizje
def check_collision(bird, pipes):
    for pipe in pipes:
        if bird.colliderect(pipe):
            return True
    if bird.top <= 0 or bird.bottom >= SCREEN_HEIGHT:
        return True
    return False

# Funkcja wyświetlająca ekran końcowy
def game_over_screen(score):
    screen.fill(WHITE)
    game_over_text = FONT.render('Game Over', True, BLACK)
    score_text = FONT.render(f'Score: {int(score)}', True, BLACK)
    restart_button = pygame.Rect(100, 300, 200, 50)
    quit_button = pygame.Rect(100, 400, 200, 50)
    pygame.draw.rect(screen, GREEN, restart_button)
    pygame.draw.rect(screen, RED, quit_button)
    restart_text = FONT.render('Restart', True, BLACK)
    quit_text = FONT.render('Quit', True, BLACK)

    screen.blit(game_over_text, (100, 100))
    screen.blit(score_text, (100, 200))
    screen.blit(restart_text, (150, 310))
    screen.blit(quit_text, (170, 410))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    return True
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    return False

# Funkcja główna gry
def game():
    bird = pygame.Rect(100, SCREEN_HEIGHT // 2, BIRD_WIDTH, BIRD_HEIGHT)
    pipes = []
    pipe_timer = 0
    pipe_frequency = 1500
    score = 0

    running = True
    while running:
        clock.tick(30)
        screen.fill(GREY)

        # Rysowanie ptaka
        draw_bird(bird)

        # Rysowanie rur
        for pipe in pipes:
            pipe.x -= 5
        pipes = [pipe for pipe in pipes if pipe.right > 0]
        draw_pipes(pipes)

        # Tworzenie nowych rur
        pipe_timer += clock.get_time()
        if pipe_timer >= pipe_frequency:
            pipe_timer = 0
            pipe_height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
            top_pipe = pygame.Rect(SCREEN_WIDTH, 0, PIPE_WIDTH, pipe_height)
            bottom_pipe = pygame.Rect(SCREEN_WIDTH, pipe_height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - pipe_height - PIPE_GAP)
            pipes.append(top_pipe)
            pipes.append(bottom_pipe)

        # Ruch ptaka
        bird.y += 6

        # Sprawdzenie kolizji
        if check_collision(bird, pipes):
            running = False

        # Aktualizacja wyniku
        for pipe in pipes:
            if pipe.right == bird.left:
                score += 0.5  # Dodawanie 0.5 punktu za każdą rurę

        # Wyświetlanie wyniku
        score_text = FONT.render(f'Score: {int(score)}', True, BLACK)
        screen.blit(score_text, (10, 10))

        # Aktualizacja ekranu
        pygame.display.flip()

        # Obsługa zdarzeń
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.y -= 50

    return score

# Uruchomienie gry
if __name__ == "__main__":
    while True:
        score = game()
        if not game_over_screen(score):
            break
