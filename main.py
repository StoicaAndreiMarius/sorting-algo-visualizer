import pygame
import classes as c
import functions as f

pygame.init()


def main():
    run = True
    clock = pygame.time.Clock()

    height = 720
    width = 1280

    array_size = 100
    sorting_speed = 60
    min_val = 0
    max_val = 100

    sorting = False
    ascending = True

    sorting_alg = f.bubble_sort
    sorting_alg_name = "Bubble Sort"
    sorting_alg_generator = None

    lst = f.generate_starting_list(array_size, min_val, max_val)
    draw_info = c.DrawInformation(width, height, lst)

    while run:
        clock.tick(sorting_speed)

        size_input_rect = pygame.Rect(draw_info.INFO_TEXT_SIZE[1], draw_info.INFO_TEXT_SIZE[0] + 20, 140,
                                      f.size_input_surface.get_height())
        speed_input_rect = pygame.Rect(draw_info.INFO_TEXT_SIZE[1],
                                       draw_info.INFO_TEXT_SIZE[0] + 20 + size_input_rect.height + 5, 140,
                                       f.speed_input_surface.get_height())

        if sorting:
            try:
                next(sorting_alg_generator)
            except StopIteration:
                sorting = False
        else:
            f.draw(draw_info, sorting_alg_name, ascending, size_input_rect, speed_input_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if size_input_rect.collidepoint(event.pos):
                    f.size_selected = True
                    pygame.display.update(size_input_rect)
                else:
                    f.size_selected = False
                    pygame.display.update(size_input_rect)
                if speed_input_rect.collidepoint(event.pos):
                    f.speed_selected = True
                    pygame.display.update(speed_input_rect)
                else:
                    f.speed_selected = False
                    pygame.display.update(speed_input_rect)

            if event.type == pygame.KEYDOWN:
                if f.size_selected:
                    if event.key is pygame.K_BACKSPACE:
                        f.size_input = f.size_input[:-1]
                        f.draw(draw_info, sorting_alg_name, ascending, size_input_rect, speed_input_rect)
                    elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0]:
                        f.size_input += event.unicode
                        f.draw(draw_info, sorting_alg_name, ascending, size_input_rect, speed_input_rect)
                    if event.key is pygame.K_RETURN:
                        array_size = int(f.size_input)
                        lst = f.generate_starting_list(array_size, min_val, max_val)
                        draw_info = c.DrawInformation(width, height, lst)
                        f.draw(draw_info, sorting_alg_name, ascending, size_input_rect, speed_input_rect)
                if f.speed_selected:
                    if event.key is pygame.K_BACKSPACE:
                        f.speed_input = f.speed_input[:-1]
                        f.draw(draw_info, sorting_alg_name, ascending, size_input_rect, speed_input_rect)
                    elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0]:
                        f.speed_input += event.unicode
                        f.draw(draw_info, sorting_alg_name, ascending, size_input_rect, speed_input_rect)
                    if event.key is pygame.K_RETURN:
                        sorting_speed = int(f.speed_input)

            if f.size_selected is not True and f.speed_selected is not True:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        lst = f.generate_starting_list(array_size, min_val, max_val)
                        draw_info = c.DrawInformation(width, height, lst)
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
                        sorting_alg = f.bubble_sort
                    elif event.key == pygame.K_i:
                        sorting_alg_name = "Insertion Sort"
                        sorting_alg = f.insertion_sort

    pygame.quit()


if __name__ == "__main__":
    main()
