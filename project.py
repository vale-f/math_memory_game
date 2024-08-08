import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
CARD_WIDTH = 100
CARD_HEIGHT = 100
CARD_FRAME_WIDTH = 5
SPACE_BETWEEN_BLOCKS = 150
SPACE_AT_TOP = 60
FPS = 60
WAIT_TIME = 1500  # 1.5 seconds
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 36
LARGE_FONT_SIZE = 88
EQUALS_FONT_SIZE = 75

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Math Matching Game")

# Timer
timer = pygame.time.Clock()

# Card class
class Card(pygame.sprite.Sprite):
    def __init__(self, text, x, y):
        super().__init__()
        self.text = text
        self.image = pygame.Surface((CARD_WIDTH, CARD_HEIGHT))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.visible = False
        self.matched = False
        self.render_background()

    def render_background(self):
        self.image.fill(WHITE)
        pygame.draw.rect(self.image, BLACK, self.image.get_rect(), CARD_FRAME_WIDTH)

    def render_text(self):
        font = pygame.font.Font(None, FONT_SIZE)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.image.get_rect().center)
        self.image.blit(text_surface, text_rect)

    def flip(self):
        if not self.matched:
            self.visible = not self.visible
            if self.visible:
                self.render_text()
            else:
                self.render_background()

def create_board_operations():
    operations = ['+', '-', '*', '/']
    board = []
    for row in range(3):
        for col in range(4):
            operation = random.choice(operations)
            number1 = random.randint(1, 10)
            number2 = random.randint(1, 10)
            text = f"{number1} {operation} {number2}"
            x = col * (CARD_WIDTH + 10)
            y = row * (CARD_HEIGHT + 10) + SPACE_AT_TOP
            board.append(Card(text, x, y))
    random.shuffle(board)
    return board

def create_board_results(board_operations):
    results = []
    for card in board_operations:
        try:
            result = eval(card.text)
            if isinstance(result, float):
                result = round(result, 2)
        except ZeroDivisionError:
            result = 'Inf'
        results.append(str(result))
    random.shuffle(results)

    board_results = []
    for index, result in enumerate(results):
        x = (index % 4) * (CARD_WIDTH + 10)
        y = (index // 4) * (CARD_HEIGHT + 10) + SPACE_AT_TOP
        board_results.append(Card(result, x, y))
    return board_results

def center_cards_horizontally(cards, start_x):
    for card in cards:
        card.rect.x += start_x

def render_text(screen, text, size, color, position):
    font = pygame.font.Font(None, size)
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=position)
    screen.blit(surface, rect)

def main():
    board_operations = create_board_operations()
    board_results = create_board_results(board_operations)

    total_width_operations = (4 * CARD_WIDTH) + (3 * 10)
    total_width_results = (4 * CARD_WIDTH) + (3 * 10)
    total_width_blocks = total_width_operations + SPACE_BETWEEN_BLOCKS + total_width_results

    start_x_operations = (SCREEN_WIDTH - total_width_blocks) // 2
    start_x_results = start_x_operations + total_width_operations + SPACE_BETWEEN_BLOCKS

    center_cards_horizontally(board_operations, start_x_operations)
    center_cards_horizontally(board_results, start_x_results)

    all_sprites = pygame.sprite.Group(board_operations + board_results)

    flipped_cards = []
    matched_cards = []
    last_flip_time = None
    start_time = pygame.time.get_ticks()
    elapsed_time = 0  # Initialize elapsed time
    game_over = False
    moves = 0
    misses = 0

    running = True
    while running:
        timer.tick(FPS)
        screen.fill(WHITE)
        all_sprites.draw(screen)
        all_sprites.update()

        current_time = pygame.time.get_ticks()

        if not game_over:
            elapsed_time = (current_time - start_time) // 1000

        if not game_over and all(card.matched for card in all_sprites):
            game_over = True

        render_text(screen, f"Time: {elapsed_time} s", FONT_SIZE, BLACK, (SCREEN_WIDTH - 155, SCREEN_HEIGHT - 53))
        render_text(screen, f"Moves: {moves}", FONT_SIZE, BLACK, (SCREEN_WIDTH - 305, SCREEN_HEIGHT - 53))
        render_text(screen, f"Misses: {misses}", FONT_SIZE, BLACK, (SCREEN_WIDTH - 455, SCREEN_HEIGHT - 53))

        if game_over:
            render_text(screen, "Great!", LARGE_FONT_SIZE, BLACK, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 158))

        render_text(screen, "=", EQUALS_FONT_SIZE, BLACK, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 70))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                pos = pygame.mouse.get_pos()
                if len(flipped_cards) < 2:
                    for card in all_sprites:
                        if card.rect.collidepoint(pos) and not card.visible:
                            card.flip()
                            flipped_cards.append(card)
                            if len(flipped_cards) == 2:
                                moves += 1
                                card1_result = eval(flipped_cards[0].text)
                                card2_result = eval(flipped_cards[1].text)
                                if isinstance(card1_result, float):
                                    card1_result = round(card1_result, 2)
                                if isinstance(card2_result, float):
                                    card2_result = round(card2_result, 2)
                                if card1_result == card2_result:
                                    flipped_cards[0].matched = True
                                    flipped_cards[1].matched = True
                                    matched_cards.extend(flipped_cards)
                                    flipped_cards = []
                                else:
                                    misses += 1
                                    last_flip_time = current_time

        if len(flipped_cards) == 2 and last_flip_time and current_time - last_flip_time >= WAIT_TIME:
            for card in flipped_cards:
                card.flip()
            flipped_cards = []
            last_flip_time = None

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
