# Lib
import pygame
import pygame_gui
import sys
import pandas as pd
import numpy as np


def draw_table(screen, df, x, y, cell_width, cell_height, font):
    for j, col_name in enumerate(df.columns):
        rect = pygame.Rect(x + j * cell_width, y, cell_width, cell_height)
        pygame.draw.rect(screen, BLACK, rect, 1)

        text_surface = font.render(str(col_name), True, BLACK)
        screen.blit(text_surface, (x + j * cell_width + 5, y + 5))

    for i, row in df.iterrows():
        for j, value in enumerate(row):
            rect = pygame.Rect(x + j * cell_width, y + (i + 1) * cell_height, cell_width, cell_height)
            pygame.draw.rect(screen, BLACK, rect, 1)

            text_surface = font.render(str(value), True, BLACK)
            screen.blit(text_surface, (x + j * cell_width + 5, y + (i + 1) * cell_height + 5))


# width, height for table
cell_width = 150
cell_height = 60


# Data for App
df = pd.read_csv('')  # Name file here
df_show = df.head(5)
df.fillna(0, inplace=True)

# Compute Data
overall_mean = df.mean().mean()

block_means = df.mean(axis=1)
block_effects = block_means - overall_mean

treatment_means = df.mean(axis=0)
treatment_effects = treatment_means - overall_mean

expected_values = overall_mean + (block_effects.values[:, np.newaxis] + treatment_effects.values)

residuals = df.values - expected_values

results_df = pd.DataFrame({
    'Overall Mean (μ)': [overall_mean] * len(df),
    'Block Effects (b_j)': block_effects.values,
})


for i, treatment_effect in enumerate(treatment_effects):
    results_df[f'Treatment Effect (CT{i+1})'] = treatment_effect


residuals_df = pd.DataFrame(residuals, index=df.index, columns=df.columns)

# Init Pygame
pygame.init()

WIDTH, HEIGHT = 1200, 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('AGT4003_1')

running = True

# Color
BACKGROUND = (214, 214, 214)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# font
font = pygame.font.SysFont('sans', 40)

# GUI
manager = pygame_gui.UIManager((1600, 900))

text_name = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((100, 50), (500, 50)), manager=manager,
                                                object_id='#main_text_name')
text_MSV = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((100, 100), (500, 50)), manager=manager,
                                               object_id='#main_text_MSV')

clock = pygame.time.Clock()

# text
text_summited = font.render('Enter', True, WHITE)
text_enter = font.render('Enter', True, WHITE)

while running:
    screen.fill(BACKGROUND)
    draw_table(screen, df_show, 50, 200, cell_width, cell_height, font)

    # pos mouse
    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 850 < mouse_x < 950 and 100 < mouse_y < 150 and text_MSV.text != '' and text_name.text != '':
                print(text_name.text)
                print(text_MSV.text)

            if 100 < mouse_x < 200 and 600 < mouse_y < 650:
                results_df.to_csv(f'{text_name.text}_{text_MSV.text}.csv', index=False)
                print('Completed')
        manager.process_events(event)

    pygame.draw.rect(screen, BLACK, (850, 100, 100, 40))
    pygame.draw.rect(screen, BLACK, (100, 600, 100, 40))
    screen.blit(text_summited, (850, 100))
    screen.blit(text_enter, (100, 600))

    UI_REFRESH_RATE = clock.tick(60) / 1000

    manager.update(UI_REFRESH_RATE)
    manager.draw_ui(screen)

    pygame.display.update()

pygame.quit()
sys.exit()
