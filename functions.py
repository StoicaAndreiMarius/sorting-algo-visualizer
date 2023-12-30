import pygame
import random
import main as m

pygame.init()


def generate_starting_list(size_text, min_val, max_val):
    try:
        n = int(size_text)
        lst = [random.randint(min_val, max_val) for _ in range(n)]
        return lst
    except TypeError:
        n = 100
        lst = [random.randint(min_val, max_val) for _ in range(n)]
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
            draw_list(draw_info, {arr[j]: draw_info.GREEN, arr[j + 1]: draw_info.RED, key: draw_info.BLUE},
                      clear_bg=True)
            arr[j + 1] = key  # Insert the key in the correct position
            yield True
    else:
        for i in range(1, n):  # Iterate over the array starting from the second element
            key = arr[i]  # Store the current element as the key to be inserted in the right position
            j = i - 1

            while j >= 0 and key > arr[j]:  # Move elements greater than key one position ahead
                arr[j + 1] = arr[j]  # Shift elements to the right
                j -= 1
            draw_list(draw_info, {arr[j]: draw_info.GREEN, arr[j + 1]: draw_info.RED, key: draw_info.BLUE},
                      clear_bg=True)
            arr[j + 1] = key  # Insert the key in the correct position
            yield True


SMALL_FONT = pygame.font.SysFont('timesnewroman', 20)
size_input_surface = SMALL_FONT.render('Input array size: ', True, (0, 0, 0))
speed_input_surface = SMALL_FONT.render('Input sorting speed: ', True, (0, 0, 0))

size_input = ''
speed_input = ''

size_input_rect_surface = SMALL_FONT.render(size_input, True, (0, 0, 0))
speed_input_rect_surface = SMALL_FONT.render(speed_input, True, (0, 0, 0))

color_selected = pygame.Color('blue')
size_selected = False
speed_selected = False


def draw(draw_info, sorting_alg_name, ascending, size_input_rect, speed_input_rect):

    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    if size_selected:
        pygame.draw.rect(draw_info.window, color_selected, size_input_rect, 2)
    else:
        pygame.draw.rect(draw_info.window, draw_info.BLACK, size_input_rect, 2)

    if speed_selected:
        pygame.draw.rect(draw_info.window, color_selected, speed_input_rect, 2)
    else:
        pygame.draw.rect(draw_info.window, draw_info.BLACK, speed_input_rect, 2)

    draw_info.window.blit(draw_info.SMALL_FONT.render(size_input, True, (0, 0, 0)), size_input_rect)
    draw_info.window.blit(draw_info.SMALL_FONT.render(speed_input, True, (0, 0, 0)), speed_input_rect)

    current_sort = draw_info.FONT.render(f"{sorting_alg_name} - {'Ascending' if ascending is True else "Descending"}",
                                         1, draw_info.BLUE)
    draw_info.window.blit(current_sort, (draw_info.width / 2 - current_sort.get_width() / 2, 5))

    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1,
                                     draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width / 2 - controls.get_width() / 2, current_sort.get_height() + 5))

    sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width / 2 - sorting.get_width() / 2,
                                    controls.get_height() + current_sort.get_height() + 5))

    draw_info.INFO_TEXT_SIZE[0] = controls.get_height() + current_sort.get_height() + sorting.get_height()
    draw_info.INFO_TEXT_SIZE[1] = draw_info.width / 2 - controls.get_width() / 2

    draw_info.window.blit(size_input_surface, (draw_info.width / 2 - controls.get_width() / 2,
                                               draw_info.INFO_TEXT_SIZE[0]+20))

    draw_info.window.blit(speed_input_surface, (draw_info.width / 2 - controls.get_width() / 2,
                                                draw_info.INFO_TEXT_SIZE[0] + size_input_surface.get_height() +25))

    draw_info.INFO_TEXT_SIZE[1] = draw_info.width / 2 - controls.get_width() / 2 + speed_input_surface.get_width()

    draw_info.TOP_PAD = max(controls.get_height() + current_sort.get_height() + sorting.get_height() +
                            size_input_surface.get_height() + speed_input_surface.get_height() + 40, draw_info.TOP_PAD)

    draw_list(draw_info)

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
