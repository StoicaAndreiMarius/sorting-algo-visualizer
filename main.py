import math

import pygame
import random

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

    FONT = pygame.font.SysFont('timesnewroman', 30)
    LARGE_FONT = pygame.font.SysFont('timesnewroman', 30)

    SIDE_PAD = 100
    TOP_PAD = 150

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


def generate_starting_list(n, min_val, max_val):
    lst = [random.randint(min_val, max_val) for _ in range(n + 1)]
    return lst


def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]
            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
                yield True


def insertion_sort(draw_info, ascending=True):
    arr = draw_info.lst
    n = len(arr)  # Get the length of the array

    if n <= 1:
        return  # If the array has 0 or 1 element, it is already sorted, so return

    if ascending:
        for i in range(1, n):  # Iterate over the array starting from the second element
            key = arr[i]  # Store the current element as the key to be inserted in the right position
            j = i - 1

            while j >= 0 and key < arr[j]:  # Move elements greater than key one position ahead
                arr[j + 1] = arr[j]  # Shift elements to the right
                j -= 1
            draw_list(draw_info, {arr[j]: draw_info.GREEN, arr[j + 1]: draw_info.RED, key:draw_info.BLUE}, clear_bg=True)
            arr[j + 1] = key  # Insert the key in the correct position
            yield True
    else:
        for i in range(n, 1, -1):  # Iterate over the array starting from the second element
            key = arr[i]  # Store the current element as the key to be inserted in the right position
            j = i - 1

            while j >= 0 and key < arr[j]:  # Move elements greater than key one position ahead
                arr[j + 1] = arr[j]  # Shift elements to the right
                j -= 1
            draw_list(draw_info, {arr[j]: draw_info.GREEN, arr[j + 1]: draw_info.RED, key:draw_info.BLUE}, clear_bg=True)
            arr[j + 1] = key  # Insert the key in the correct position
            yield True


def draw(draw_info, sorting_alg_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)
    draw_list(draw_info)

    current_sort = draw_info.FONT.render(f"{sorting_alg_name} - {'Ascending' if ascending == True else "Descending"}",
                                         1, draw_info.BLUE)
    draw_info.window.blit(current_sort, (draw_info.width / 2 - current_sort.get_width() / 2, 5))

    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1,
                                     draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width / 2 - controls.get_width() / 2, current_sort.get_height() + 5))

    sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width / 2 - sorting.get_width() / 2,
                                    controls.get_height() + current_sort.get_height() + 5))

    pygame.display.update()


def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD // 2, draw_info.TOP_PAD, draw_info.width - draw_info.SIDE_PAD,
                      draw_info.height)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val, in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        color = draw_info.GRADIENTS[i % 3]
        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color, ((x, y), (draw_info.block_width, draw_info.height)))

    if clear_bg:
        pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()

    height = 720
    width = 1280

    n = 300
    min_val = 0
    max_val = 100

    sorting = False
    ascending = True

    sorting_alg = bubble_sort
    sorting_alg_name = "Bubble Sort"
    sorting_alg_generator = None

    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(width, height, lst)

    while run:
        clock.tick(60)

        if sorting:
            try:
                next(sorting_alg_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_alg_name, ascending)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                lst = generate_starting_list(n, min_val, max_val)
                draw_info = DrawInformation(width, height, lst)
                sorting = False
            elif event.key == pygame.K_SPACE:
                if not sorting:
                    sorting = True
                    sorting_alg_generator = sorting_alg(draw_info, ascending)
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_b:
                sorting_alg_name = "Bubble Sort"
                sorting_alg = bubble_sort
            elif event.key == pygame.K_i:
                sorting_alg_name = "Insertion Sort"
                sorting_alg = insertion_sort

    pygame.quit()


if __name__ == "__main__":
    main()
