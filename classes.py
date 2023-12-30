import math
import pygame

pygame.init()

class DrawInformation:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    GREY = 128, 128, 128
    BLUE = 22, 105, 240
    BACKGROUND_COLOR = WHITE

    GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    SMALL_FONT = pygame.font.SysFont('timesnewroman', 20)
    FONT = pygame.font.SysFont('timesnewroman', 30)
    LARGE_FONT = pygame.font.SysFont('timesnewroman', 40)

    SIDE_PAD = 100
    TOP_PAD = 150
    INFO_TEXT_SIZE = [0, 0]

    input_rect_color = pygame.Color('black')

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height
        self.set_list(lst)

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algo Visualizer")

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        self.block_width = (self.width - self.SIDE_PAD) / len(lst)
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2