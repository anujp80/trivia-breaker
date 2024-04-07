import pygame
import pygame_gui
import sys
from levels import Level
from game_objects import Ball, Paddle, Trivia_Game  

# Initialize Pygame
pygame.init()

# Setup screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Trivia Breaker")

# Initialize UIManager
manager = pygame_gui.UIManager((screen_width, screen_height))

# Game entities
ball = Ball(screen_width, screen_height)
paddle = Paddle(screen_width, screen_height)
trivia_game = Trivia_Game(manager, screen_width, screen_height)
current_level = None  # Will be set when a level is selected

home_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((screen_width - 60, 10), (50, 50)),
    text='H',
    manager=manager
)


# Game state
game_state = 'menu'
trivia_active = False  # Indicator if trivia question is currently displayed
selected_answer = None  # To store player's answer
level_buttons = [pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50 + i * 70, screen_height - 100), (60, 60)),
                                              text=str(i + 1), manager=manager)
                 for i in range(10)]

# Initialize game loop setup
clock = pygame.time.Clock()
running = True

while running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        manager.process_events(event)  # Moved up for easier event processing
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == home_button:
                # Reset to menu state
                game_state = 'menu'
                trivia_active = False
                for btn in level_buttons: btn.show()  
                current_level = None  # Reset current level
                manager.clear_and_reset()  # Clear any trivia UI components
                continue  # Skip the rest of the loop after handling home button


        if game_state == 'menu':
            manager.process_events(event)
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                for i, button in enumerate(level_buttons):
                    if event.ui_element == button:
                        game_state = 'playing'
                        current_level_number = i + 1
                        current_level = Level(current_level_number, screen_width)
                        ball.reset(screen_width, screen_height)
                        paddle = Paddle(screen_width, screen_height)
                        for btn in level_buttons:
                            btn.hide()

        elif game_state == 'playing' and trivia_active:
            manager.process_events(event)
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element in trivia_game.ui_elements:
                selected_answer = event.ui_element.text
                if trivia_game.check_answer(selected_answer):
                    current_level.bricks = current_level.bricks[:int(len(current_level.bricks)*0.8)]
                    trivia_active = False  # Trivia question answered
                    manager.clear_and_reset()  # Clear trivia UI
                else:
                    current_level = Level(current_level_number, screen_width)
                    ball.reset(screen_width, screen_height)
                    trivia_active = False  # Reset trivia state
                    manager.clear_and_reset()  # Clear trivia UI

    # Update section for 'playing' state
    if game_state == 'playing' and not trivia_active:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.move("left")
        if keys[pygame.K_RIGHT]:
            paddle.move("right")

        ball.move()

        # Ball collision with paddle
        if ball.rect.colliderect(paddle.rect):
            ball.vy = -ball.vy
            ball.y = paddle.y - ball.radius * 2  # Prevents ball from sticking

        # Ball collision with bricks
        if current_level:
            for brick in current_level.bricks[:]:  # Safe iteration for removal
                if ball.rect.colliderect(brick.rect):
                    if brick.is_trivia:  # If it's a trivia brick, show question
                        trivia_game.show_question(current_level_number)
                        trivia_active = True
                    current_level.bricks.remove(brick)
                    ball.vy = -ball.vy
                    break  # Handle one collision per frame
            if len(current_level.bricks) == 0:
                game_state = 'menu'
                trivia_active = False
                for btn in level_buttons:
                    btn.show()  # Show level selection buttons again
                current_level = None  # Reset current level for a fresh start


        # Ball out of bounds, just respawn it
        if ball.y + ball.radius * 2 > screen_height:
            ball.reset(screen_width, screen_height)

    # Drawing section
    screen.fill((0, 0, 0))  # Clear screen
    if game_state == 'menu':
        manager.update(time_delta)
        manager.draw_ui(screen)
    else:
        if current_level:
            current_level.draw(screen)
        paddle.draw(screen)
        ball.draw(screen)
        if trivia_active:
            manager.update(time_delta)
            manager.draw_ui(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()