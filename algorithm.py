#Encryption False
import pygame
import random,math,time,os
pygame.init()
pygame.mixer.init()

class DrawData:
    BLACK = 0,0,0
    WHITE = 255,255,255
    GREEN = 0,255,0
    RED = 255,0,0
    GREY = 128,128,128
    BLUE = 0,0,255
    BACKGROUND_COLOR = WHITE
    INTERSTELLAR = pygame.mixer.Sound("assets/Interstellar Main Theme - Hans Zimmer.mp3")
    GRADIENTS = [
        GREY,
        (160,160,160),
        (192,192,192)
    ]
    SIDE_PAD = 100
    TOP_PAD = 150

    def __init__(self,width,height,lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algortihm")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)
        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor((self.height- self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2

def generate_list(n,min_val,max_val):
    lst = []
    for _ in range(n):
        val = random.randint(min_val,max_val)
        lst.append(val)
    return lst

def draw(draw_info, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)
    draw_list(draw_info)
    pygame.display.update()

def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst
    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)
    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        color = draw_info.GRADIENTS[i % 3]
        if i in color_positions:
            color = color_positions[i]
        pygame.draw.rect(draw_info.window, color, (x,y, draw_info.block_width, draw_info.height))
    if clear_bg:
        pygame.display.update()

def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst
    for i in range(len(lst)-1):
        for j in range(len(lst)-1-i):
            num1= lst[j]
            num2 = lst[j+1]
            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j+1] = lst[j+1], lst[j]
                draw_list(draw_info, {j:draw_info.BLUE, j + 1: draw_info.BLACK}, True)
                yield True
    return lst
def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst
    for i in range(1,len(lst)):
        current = lst[i]
        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending
            if not ascending_sort and not descending_sort:
                break
            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current
            draw_list(draw_info, {i: draw_info.BLUE, i - 1: draw_info.BLACK}, True)
            yield True
    return lst
def main():
    clock = pygame.time.Clock()
    FPS = 30
    run = True
    sorting = False
    n = 50
    min_val = 0
    max_val = 100
    lst = generate_list(n,min_val,max_val)
    draw_info = DrawData(800,600,lst)
    ascending = True
    sorting_algorithm = bubble_sort
    sorting_algorithm_generator = None
    compare = 0
    counter = 0
    while run:
        clock.tick(FPS)
        if sorting:
            counter += 1
            if counter == 1:
                DrawData.INTERSTELLAR.play()
                start = time.time()
            try:
                next(sorting_algorithm_generator)
                compare += 1
            except StopIteration:
                print("Comparisons:"+str(compare))
                print("Time:"+str(time.time()-start))
                sorting = False
        else:
            draw(draw_info, ascending)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.QUIT:
                    run = False
                if event.key == pygame.K_r:
                    lst = generate_list(n,min_val,max_val)
                    draw_info.set_list(lst)
                    sorting = False
                if event.key == pygame.K_q:
                    FPS += 2
                if event.key == pygame.K_e:
                    FPS -= 2
                if event.key == pygame.K_SPACE and sorting == False:
                    sorting = True
                    sorting_algorithm_generator = sorting_algorithm(draw_info, ascending) 
                if event.key == pygame.K_a and sorting == False:
                    ascending = True
                if event.key == pygame.K_d and sorting == False:
                    ascending = False
                elif event.key == pygame.K_i and sorting == False:
                    sorting_algorithm = insertion_sort
                    sorting_algo_name = "Insertion Sort"
                elif event.key == pygame.K_b and sorting == False:
                    sorting_algorithm = bubble_sort
                    sorting_algo_name = "Bubble Sort"
    pygame.quit()
if __name__ == "__main__":
    main()