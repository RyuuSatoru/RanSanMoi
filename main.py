import pygame
import sys
import random
import os

# Khoi tao Pygame
pygame.init()

# Cai dat man hinh
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ran San Moi")

# Load anh dau ran
snake_head_img = None
try:
    snake_head_img = pygame.image.load('head.png')
except FileNotFoundError:
    print("Khong the load file head.png. Su dung hinh mac dinh.")

# Mau sac
BACKGROUND_COLOR = (20, 30, 40)
BUTTON_COLOR = (41, 128, 185)
BUTTON_HOVER_COLOR = (52, 152, 219)
TEXT_COLOR = (236, 240, 241)
TITLE_COLOR = (46, 204, 113)
SNAKE_BODY_COLOR = (0, 200, 0) 

# Phong chu
try:
    title_font = pygame.font.SysFont(None, 80)
    button_font = pygame.font.SysFont(None, 50)
    small_font = pygame.font.SysFont(None, 30)
except:
    # Neu khong the tai font he thong, su dung font mac dinh cua Pygame
    title_font = pygame.font.Font(None, 80)
    button_font = pygame.font.Font(None, 50)
    small_font = pygame.font.Font(None, 30)

# Cac bien cai dat mac dinh
GAME_SETTINGS = {
    'snake_size': 20,
    'snake_speed': 10,  # Thay doi gia tri mac dinh
    'fps': 30,
    'background_color': BACKGROUND_COLOR
}

# Ham ve nut voi hieu ung hover
def draw_button(text, position, is_hover=False, font=None):
    # Su dung font mac dinh neu khong co font duoc truyen vao
    if font is None:
        font = button_font
    
    # Tao text surface
    text_surface = font.render(text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=position)
    
    # Ve nen nut voi hieu ung hover
    button_rect = text_rect.inflate(40, 20)
    button_color = BUTTON_HOVER_COLOR if is_hover else BUTTON_COLOR
    
    # Ve nut voi goc bo tron
    pygame.draw.rect(screen, button_color, button_rect, border_radius=10)
    screen.blit(text_surface, text_rect)
    
    return button_rect

# Ham ve background voi gradient
def draw_background():
    for y in range(height):
        # Tao gradient tu mau dam sang mau nhat
        r = int(20 + (y / height) * 30)
        g = int(30 + (y / height) * 40)
        b = int(40 + (y / height) * 50)
        pygame.draw.line(screen, (r, g, b), (0, y), (width, y))

# Ham cai dat
def settings_menu():
    clock = pygame.time.Clock()
    
    # Tao cac gia tri slider
    snake_size_value = GAME_SETTINGS['snake_size']
    snake_speed_value = GAME_SETTINGS['snake_speed']
    fps_value = GAME_SETTINGS['fps']
    
    while True:
        # Ve background
        draw_background()
        
        # Ve tieu de
        title_surface = title_font.render("CAI DAT", True, TITLE_COLOR)
        title_rect = title_surface.get_rect(center=(width//2, height//6))
        screen.blit(title_surface, title_rect)
        
        # Cap nhat vi tri chuot
        mouse_pos = pygame.mouse.get_pos()
        
        # Ve cac tuy chon cai dat
        # Kich thuoc ran
        size_text = small_font.render(f"Kich Thuoc: {snake_size_value}", True, TEXT_COLOR)
        size_rect = size_text.get_rect(center=(width//2, height//2 - 100))
        screen.blit(size_text, size_rect)
        
        minus_size_rect = draw_button("-", (width//2 - 100, height//2 - 100), 
                                       pygame.Rect(width//2 - 140, height//2 - 120, 80, 40).collidepoint(mouse_pos),
                                       small_font)
        plus_size_rect = draw_button("+", (width//2 + 100, height//2 - 100), 
                                     pygame.Rect(width//2 + 60, height//2 - 120, 80, 40).collidepoint(mouse_pos),
                                     small_font)
        
        # Toc do ran
        speed_text = small_font.render(f"Toc Do Ran: {snake_speed_value}", True, TEXT_COLOR)
        speed_rect = speed_text.get_rect(center=(width//2, height//2))
        screen.blit(speed_text, speed_rect)
        
        minus_speed_rect = draw_button("-", (width//2 - 100, height//2), 
                                        pygame.Rect(width//2 - 140, height//2 - 20, 80, 40).collidepoint(mouse_pos),
                                        small_font)
        plus_speed_rect = draw_button("+", (width//2 + 100, height//2), 
                                       pygame.Rect(width//2 + 60, height//2 - 20, 80, 40).collidepoint(mouse_pos),
                                       small_font)
        
        # FPS
        fps_text = small_font.render(f"FPS: {fps_value}", True, TEXT_COLOR)
        fps_rect = fps_text.get_rect(center=(width//2, height//2 + 100))
        screen.blit(fps_text, fps_rect)
        
        minus_fps_rect = draw_button("-", (width//2 - 100, height//2 + 100), 
                                      pygame.Rect(width//2 - 140, height//2 + 80, 80, 40).collidepoint(mouse_pos),
                                      small_font)
        plus_fps_rect = draw_button("+", (width//2 + 100, height//2 + 100), 
                                     pygame.Rect(width//2 + 60, height//2 + 80, 80, 40).collidepoint(mouse_pos),
                                     small_font)
        
        # Nut quay lai
        back_rect = draw_button("Quay Lai", (width//2, height//2 + 200))
        
        # Xu ly su kien
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Su kien click chuot
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Kich thuoc ran
                if minus_size_rect.collidepoint(event.pos):
                    snake_size_value = max(10, snake_size_value - 5)
                elif plus_size_rect.collidepoint(event.pos):
                    snake_size_value = min(40, snake_size_value + 5)
                
                # Toc do ran
                elif minus_speed_rect.collidepoint(event.pos):
                    snake_speed_value = max(1, snake_speed_value - 1)
                elif plus_speed_rect.collidepoint(event.pos):
                    snake_speed_value = min(20, snake_speed_value + 1)
                
                # FPS
                elif minus_fps_rect.collidepoint(event.pos):
                    fps_value = max(30, fps_value - 15)
                elif plus_fps_rect.collidepoint(event.pos):
                    fps_value = min(120, fps_value + 15)
                
                # Quay lai
                elif back_rect.collidepoint(event.pos):
                    # Cap nhat cai dat
                    GAME_SETTINGS['snake_size'] = snake_size_value
                    GAME_SETTINGS['snake_speed'] = snake_speed_value
                    GAME_SETTINGS['fps'] = fps_value
                    main_menu()
        
        pygame.display.flip()
        clock.tick(30)

# Man hinh menu chinh
def main_menu():
    clock = pygame.time.Clock()
    
    # Nut va vi tri
    buttons = [
        {"text": "Bat Dau", "position": (width // 2, height // 2)},
        {"text": "Cai Dat", "position": (width // 2, height // 2 + 100)},
        {"text": "Thoat", "position": (width // 2, height // 2 + 200)}
    ]
    
    while True:
        # Ve background
        draw_background()
        
        # Ve tieu de
        title_surface = title_font.render("RAN SAN MOI", True, TITLE_COLOR)
        title_rect = title_surface.get_rect(center=(width//2, height//4))
        screen.blit(title_surface, title_rect)
        
        # Cap nhat vi tri chuot
        mouse_pos = pygame.mouse.get_pos()
        
        # Ve cac nut va kiem tra hover
        button_rects = []
        for button in buttons:
            # Kiem tra hover
            is_hover = pygame.Rect(button["position"][0]-100, button["position"][1]-25, 200, 50).collidepoint(mouse_pos)
            button_rect = draw_button(button["text"], button["position"], is_hover)
            button_rects.append((button_rect, button["text"]))
        
        # Xu ly su kien
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Su kien click chuot
            if event.type == pygame.MOUSEBUTTONDOWN:
                for rect, text in button_rects:
                    if rect.collidepoint(event.pos):
                        if text == "Bat Dau":
                            game_loop(
                                snake_size=GAME_SETTINGS['snake_size'], 
                                background_color=GAME_SETTINGS['background_color'], 
                                snake_speed=GAME_SETTINGS['snake_speed'],
                                game_fps=GAME_SETTINGS['fps']
                            )
                        elif text == "Cai Dat":
                            settings_menu()
                        elif text == "Thoat":
                            pygame.quit()
                            sys.exit()
        
        pygame.display.flip()
        clock.tick(30)

# Chuc nang game loop
def game_loop(snake_size=20, background_color=(0,0,0), snake_speed=10, game_fps=30):
    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]
    
    def spawn_food():
        while True:
            # Thay doi kich thuoc thuc an theo kich thuoc ran
            food_pos = [random.randrange(1, (width // snake_size)) * snake_size, 
                        random.randrange(1, (height // snake_size)) * snake_size]
            if food_pos not in snake_body:
                return food_pos
    
    food_pos = spawn_food()
    direction = 'RIGHT'
    next_direction = direction
    score = 0

    # Them bien dem de dieu khien toc do ran
    move_delay = 0
    move_threshold = 21 - snake_speed  # Cang tang toc do, cang giam move_threshold

    def show_score(choice, color, font, size):
        score_font = pygame.font.SysFont(None, size)
        score_surface = score_font.render('Diem: ' + str(score), True, color)
        score_rect = score_surface.get_rect()
        if choice == 1:
            score_rect.midtop = (width / 10, 15)
        else:
            score_rect.midtop = (width / 2, height / 1.25)
        screen.blit(score_surface, score_rect)

    def game_over():
        my_font = pygame.font.SysFont(None, 50)
        game_over_surface = my_font.render('Game Over', True, (255,0,0))
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (width / 2, height / 4)
        screen.blit(game_over_surface, game_over_rect)
        show_score(0, (255,0,0), None, 20)
        pygame.display.flip()
        pygame.time.wait(2000)
        main_menu()

    clock = pygame.time.Clock()
    
    # Xu ly phim lien tuc
    pygame.key.set_repeat(10, 10)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Xu ly phim di chuyen
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'DOWN':
                    next_direction = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    next_direction = 'DOWN'
                elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                    next_direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    next_direction = 'RIGHT'
                elif event.key == pygame.K_ESCAPE:
                    main_menu()

        direction = next_direction

        # Dieu khien toc do ran bang cach dem so lan lap
        move_delay += 1
        if move_delay >= move_threshold:
            # Di chuyen ran
            if direction == 'UP':
                snake_pos[1] -= snake_size
            elif direction == 'DOWN':
                snake_pos[1] += snake_size
            elif direction == 'LEFT':
                snake_pos[0] -= snake_size
            elif direction == 'RIGHT':
                snake_pos[0] += snake_size

            # Reset bo dem
            move_delay = 0

            if abs(snake_pos[0] - food_pos[0]) < snake_size and abs(snake_pos[1] - food_pos[1]) < snake_size:
                score += 10
                food_pos = spawn_food()
                snake_body.append(list(snake_pos))

            snake_body.insert(0, list(snake_pos))
            
            if len(snake_body) > len(snake_body[:-1]):
                snake_body.pop()

        screen.fill(background_color)
        
        # Ve than ran
        for pos in snake_body[1:]:
            pygame.draw.rect(screen, SNAKE_BODY_COLOR, pygame.Rect(pos[0], pos[1], snake_size, snake_size))
        
        # Ve dau ran
        if snake_head_img:
            # Neu co anh head.png, su dung anh
            resized_head = pygame.transform.scale(snake_head_img, (snake_size, snake_size))
            
            # Xoay dau ran theo huong di chuyen
            if direction == 'RIGHT':
                rotated_head = resized_head
            elif direction == 'LEFT':
                rotated_head = pygame.transform.rotate(resized_head, 180)
            elif direction == 'UP':
                rotated_head = pygame.transform.rotate(resized_head, 90)
            elif direction == 'DOWN':
                rotated_head = pygame.transform.rotate(resized_head, 270)
            
            screen.blit(rotated_head, (snake_pos[0], snake_pos[1]))
        else:
            # Neu khong co anh, ve hinh chu nhat mau xanh
            pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(snake_pos[0], snake_pos[1], snake_size, snake_size))
        
        # Ve thuc an
        pygame.draw.rect(screen, (255,255,255), pygame.Rect(food_pos[0], food_pos[1], snake_size, snake_size))
        
        show_score(1, (255,255,255), None, 20)

        if snake_pos[0] < 0 or snake_pos[0] > width - snake_size:
            game_over()
        if snake_pos[1] < 0 or snake_pos[1] > height - snake_size:
            game_over()

        for block in snake_body[1:]:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                game_over()

        pygame.display.flip()
        clock.tick(game_fps)

# Bat dau tro choi
def main():
    main_menu()

if __name__ == "__main__":
    main()