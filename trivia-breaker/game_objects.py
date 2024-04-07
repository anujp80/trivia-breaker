import pygame
import pygame_gui
import json

class Brick:
    def __init__(self, x, y, color, hits=1, is_trivia=False):
        self.rect = pygame.Rect(x, y, 75, 20)  # Standard brick size
        self.color = pygame.Color(color)
        self.hits = hits
        self.is_trivia = is_trivia  # Indicates if this is a trivia brick

    def draw(self, screen):
        # Draw the brick
        pygame.draw.rect(screen, self.color, self.rect)
        # Draw a question mark on trivia bricks
        if self.is_trivia:
            font = pygame.font.Font(None, 24)  # Default font, size 24
            text = font.render("?", True, pygame.Color('black'))
            text_rect = text.get_rect(center=self.rect.center)
            screen.blit(text, text_rect)

    def hit(self):
        self.hits -= 1

class Ball:
    def __init__(self, screen_width, screen_height):
        self.radius = 10
        self.reset(screen_width, screen_height)
        
    def reset(self, screen_width, screen_height):
        self.x = screen_width // 2
        self.y = screen_height // 2
        self.vx = 5
        self.vy = 5  # Make the ball move downwards initially
        self.screen_width = screen_width
        self.screen_height = screen_height

    @property
    def rect(self):
        # Returns a pygame.Rect representing the ball's current position
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def move(self):
        self.x += self.vx
        self.y += self.vy

        # Screen boundary collision logic remains unchanged
        if self.x <= 0 or self.x + self.radius * 2 >= self.screen_width:
            self.vx = -self.vx
        if self.y <= 0:
            self.vy = -self.vy

    def draw(self, screen):
        pygame.draw.circle(screen, pygame.Color('white'), (self.x, self.y), self.radius)


class Trivia_Question:
    def __init__(self, question, answers, correct_answer):
        self.question = question
        self.answers = answers  # List of answers
        self.correct_answer = correct_answer

    def check_answer(self, answer):
        return answer == self.correct_answer

class Paddle:
    def __init__(self, screen_width, screen_height):
        self.width = 100
        self.height = 20
        self.x = (screen_width - self.width) / 2
        self.y = screen_height - self.height * 2
        self.color = pygame.Color('white')
        self.speed = 10
        self.screen_width = screen_width

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, direction):
        if direction == "left":
            self.x -= self.speed
            if self.x < 0:
                self.x = 0
        elif direction == "right":
            self.x += self.speed
            if self.x + self.width > self.screen_width:
                self.x = self.screen_width - self.width

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.width, self.height))

class Trivia_Game:
    def __init__(self, manager, screen_width, screen_height):
        self.manager = manager
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.questions = self.load_questions()
        self.current_question = None
        self.ui_elements = []

    def load_questions(self):
        with open('trivia_questions.json', 'r') as file:
            return json.load(file)

    def show_question(self, level_number):
        self.current_question = self.questions[level_number - 1]
        question_text = self.current_question["question"]
        answers = self.current_question["answers"]
        
        # Clear existing UI elements
        for element in self.ui_elements:
            element.kill()
        self.ui_elements.clear()

        # Create a UI panel to host the question and answers
        panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((100, 100), (600, 400)),
                                            manager=self.manager)
        self.ui_elements.append(panel)
        
        # Display the question
        question_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 0), (600, 50)),
                                                     text=question_text,
                                                     manager=self.manager,
                                                     container=panel)
        self.ui_elements.append(question_label)
        
        # Display answer buttons
        for i, answer in enumerate(answers):
            button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100, 50 + i*60), (400, 50)),
                                                  text=answer,
                                                  manager=self.manager,
                                                  container=panel,
                                                  object_id=str(i))
            self.ui_elements.append(button)

    def check_answer(self, answer):
        return answer == self.current_question["correct_answer"]