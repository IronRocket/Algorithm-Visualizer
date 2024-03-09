import pygame,random,math,time,pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button
from pygame_widgets.dropdown import Dropdown

pygame.init()
pygame.mixer.init()

width,height = 800,600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Sorting Algortihm")

font = pygame.font.SysFont('Comic Sans MS', 14)


BLACK = 0,0,0
WHITE = 255,255,255
GREEN = 0,255,0
RED = 255,0,0
GREY = 128,128,128
BLUE = 0,0,255
INTERSTELLAR = pygame.mixer.Sound("assets/Interstellar Main Theme - Hans Zimmer.mp3")
GRADIENTS = [
    GREY,
    (160,160,160),
    (192,192,192)
]
SIDE_PAD = 100
TOP_PAD = 150


class Game:
    def __init__(self):
        self.n = 50
        self.min_val = 0
        self.max_val = 100
        self.l = []
        self.sorting_algorithm = self.bubble_sort
        self.sorting_algorithm_generator = None
        self.sorting = False

    def generate_list(self):
        self.l = []
        for _ in range(self.n):
            val = random.randint(self.min_val,self.max_val)
            self.l.append(val)
            
        self.min_val = min(self.l)
        self.max_val = max(self.l)
        self.block_width = round(width - SIDE_PAD) / len(self.l)
        self.block_height = math.floor((height- TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = SIDE_PAD // 2
    
    def resetList(self,newValue:int):
        self.l = []
        self.n = newValue
        self.generate_list()

    def toggleSorting(self):
        if not self.sorting:
            self.sorting = True
            self.sorting_algorithm_generator = self.sorting_algorithm()
        else:
            self.sorting = False
            self.sorting_algorithm_generator = None

    def draw_list(self, color_positions={}, clear_bg=False):
        if clear_bg:
            clear_rect = (SIDE_PAD//2, TOP_PAD, width - SIDE_PAD, height - TOP_PAD)
            pygame.draw.rect(window, WHITE, clear_rect)
        for i, val in enumerate(self.l):
            x = self.start_x + i * self.block_width
            y = height - (val - self.min_val) * self.block_height

            color = GRADIENTS[i % 3]
            if i in color_positions:
                color = color_positions[i]
            pygame.draw.rect(window, color, (x,y, self.block_width, height))
        if clear_bg:
            pygame.display.update()
    
    def countingSort(self):
        i_lower_bound , upper_bound = min(self.l), max(self.l)
        lower_bound = i_lower_bound
        if i_lower_bound < 0:
            lb = abs(i_lower_bound)
            temp = []
            for i,item in self.l:
                temp.append(item+lb)
                self.draw_list({i:BLACK}, True)
                yield True
            self.l = temp
            lower_bound , upper_bound = min(self.l), max(self.l)
        
        counter_nums = [0]*(upper_bound-lower_bound+1)
        for item in self.l:
            counter_nums[item-lower_bound] += 1
            self.draw_list({item-lower_bound:BLACK}, True)
            yield True
        pos = 0
        for idx, item in enumerate(counter_nums):
            num = idx + lower_bound
            for i in range(item):
                self.l[pos] = num
                self.draw_list({pos:BLACK}, True)
                yield True
                pos += 1
        if i_lower_bound < 0:
            lb = abs(i_lower_bound)
            self.l = [item - lb for item in self.l]
    
    def shellSort(self):
        n = len(self.l)
        k = int(math.log2(n))
        interval = 2**k -1
        while interval > 0:
            for i in range(interval, n):
                temp = self.l[i]
                j = i
                while j >= interval and self.l[j - interval] > temp:
                    self.l[j] = self.l[j - interval]
                    self.draw_list({j:BLUE, j-interval: BLACK}, True)
                    yield True
                    j -= interval
                self.l[j] = temp
            k -= 1
            interval = 2**k -1


    def selectionSort(self):
        size = len(self.l)
        for ind in range(size):
            min_index = ind

            for j in range(ind + 1, size):
                # select the minimum element in every iteration
                if self.l[j] <self.l[min_index]:
                    min_index = j
                # swapping the elements to sort the array
            (self.l[ind], self.l[min_index]) = (self.l[min_index], self.l[ind])
            self.draw_list({ind:BLUE, min_index: BLACK}, True)
            yield True


    def bubble_sort(self,ascending=True):
        for i in range(len(self.l)-1):
            for j in range(len(self.l)-1-i):
                num1= self.l[j]
                num2 = self.l[j+1]
                if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                    self.l[j], self.l[j+1] = self.l[j+1], self.l[j]
                    self.draw_list({j:BLUE, j + 1: BLACK}, True)
                    yield True
        return self.l
    
    def insertion_sort(self,ascending=True):

        for i in range(1,len(self.l)):
            current = self.l[i]
            while True:
                ascending_sort = i > 0 and self.l[i - 1] > current and ascending
                descending_sort = i > 0 and self.l[i - 1] < current and not ascending
                if not ascending_sort and not descending_sort:
                    break
                self.l[i] = self.l[i - 1]
                i = i - 1
                self.l[i] = current
                self.draw_list( {i: BLUE, i - 1: BLACK}, True)
                yield True
        return self.l

    def draw(self):
        window.fill(WHITE)
        self.draw_list()

if __name__ == "__main__":
    clock = pygame.time.Clock()
    FPS = 30
    run = True
    sorting = False
    game = Game()
    game.generate_list()

    sizeOfList = Slider(window, 10, 10, 200, 20, min=0, max=150, step=1)
    game.resetList(sizeOfList.getValue())
    sizeOfListOutput = TextBox(window, 225, 5, 150, 30, fontSize=20)
    sizeOfListOutput.disable()

    framesPerSecond = Slider(window, 10, 50, 200, 20, min=5, max=200, step=1)
    framesPerSecond.setValue(60)
    framesPerSecondOutput = TextBox(window, 225, 45, 150, 30, fontSize=20)
    framesPerSecondOutput.disable()
    reset = Button(window,
        10,80,
        50,50,

        text='Reset',
        fontSize=20,
        margin=20,
        inactiveColour=(200, 50, 0),
        hoverColour=(150, 0, 0),
        pressedColour=(0, 200, 20),
        radius=20,
        onClick=lambda: game.resetList(sizeOfList.getValue())
    )
    start = Button(window,
        width-195,10,
        50,50,

        text='Start',
        fontSize=20,
        margin=20,
        inactiveColour=(200, 50, 0),
        hoverColour=(150, 0, 0),
        pressedColour=(0, 200, 20),
        radius=20,
        onClick=lambda: game.toggleSorting()
    )

    sortingAlgorithms = Dropdown(
        window, width-125, 10, 115, 50, name='Select Algorithm',
        choices=[
            'Bubble Sort',
            'Insertion Sort',
            'Selection Sort',
            'Shell Sort',
            'Counting Sort'
        ],
        borderRadius=3, colour=pygame.Color('green'), 
        values=[
            game.bubble_sort, game.insertion_sort, game.selectionSort,
            game.shellSort, game.countingSort
            ], 
        direction='down', textHAlign='left'
    )
    
    ascending = True
    sorting_algorithm = game.bubble_sort
    game.sorting_algorithm_generator = None
    compare = 0
    counter = 0
    INTERSTELLAR.play()
    while run:
        clock.tick(FPS)
        if game.sorting:
            counter += 1
            if counter == 1:
                start = time.time()
            try:
                next(game.sorting_algorithm_generator)
                compare += 1
            except StopIteration:
                print("Comparisons:"+str(compare))
                print("Time:"+str(time.time()-start))
                game.sorting = False
                counter = 0
        else:
            game.draw()

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
        
        sizeOfListOutput.setText(f'Size of list:{sizeOfList.getValue()}')
        framesPerSecondOutput.setText(f'Fps:{framesPerSecond.getValue()}')
        FPS = framesPerSecond.getValue()

        game.sorting_algorithm = sortingAlgorithms.getSelected()

        pygame_widgets.update(events)
        pygame.display.update()
    pygame.quit()