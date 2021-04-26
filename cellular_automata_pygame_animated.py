import pygame
from pygame import *
import numpy as np


def flip_bit(bit: int):
    return (1, 0)[bit]


def get_bitfield(num):
    return np.binary_repr(num=num, width=8)


class CellularAutomata:
    def __init__(self, size: int, rule: int):
        self.size = size
        self.grid = np.zeros(shape=(self.size, self.size), dtype=int)
        self.grip_size_index = size - 1
        self.rule = get_bitfield(rule)
        self.iter_counter = 0

        # set first inconsistent value
        self.grid[0, size // 2] = 1

    def apply_rule(self, a, b, c):
        """ define next gen cell state based on it and its neighbors current state

        :param a, b, c: state of left, current and right cells accordingly on T-1
        :return: state of current cell on T
        """
        index = int(f'{flip_bit(a)}{flip_bit(b)}{flip_bit(c)}', 2)
        return self.rule[index]

    def get_next_generation(self, index):
        """ applies rule and updates index+1 `grid` with next generation

        :param index: `grid` index contains current generation
        """
        # iterate over one array line an calculate next generation
        for i in range(1, self.grip_size_index):
            left = self.grid[index, i - 1]
            current = self.grid[index, i]
            right = self.grid[index, i + 1]
            self.grid[index + 1, i] = self.apply_rule(left, current, right)

    def iterate(self):
        """ simulates one generation iteration

        grid array dimensions are size X size, so it can store up to `size` iterations
        so up to `size` amount of iterations are just added to the `grid`
        when all following iterations kept by swiping the `grid`
        """
        index = self.iter_counter

        if index < self.grip_size_index:  # array is not yet filled
            self.get_next_generation(index)

        else:  # array full - time to swipe it down (up in visualized mode)
            for line in range(1, self.grip_size_index + 1):
                self.grid[line - 1] = self.grid[line]

            self.get_next_generation(self.grip_size_index - 1)  # next gen added in the end

        self.iter_counter += 1


if __name__ == "__main__":
    # SIZE: size of grid for visualization (recommended range 150-200 to balance visualization range VS performance)
    # RULE: int in range 0 - 255 which represents all possible binary state combinations
    size = 200
    ca = CellularAutomata(size=size, rule=182)  # nice one - 30, 126, 150, 60, 182, 73, 255

    WIN_WIDTH = WIN_HEIGHT = size * 5
    DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
    BACKGROUND_COLOR = "#FFFFFF"

    BLOCK_WIDTH = BLOCK_HEIGHT = 5
    BLOCK = (BLOCK_WIDTH, BLOCK_HEIGHT)
    BLOCK_COLOR = "#000000"

    pygame.init()
    screen = display.set_mode(DISPLAY)
    pygame.display.set_caption("HEADER")

    while 1:

        ca.iterate()

        for e in pygame.event.get():
            if e.type == QUIT:
                raise SystemExit("QIUT")

            bg = Surface(DISPLAY)
            bg.fill(Color(BACKGROUND_COLOR))
            screen.blit(bg, (0, 0))

            x_cor = y_cor = 0
            for i in range(size):
                for j in range(size):
                    if ca.grid[i, j] == 1:
                        block = Surface(BLOCK)
                        block.fill(Color(BLOCK_COLOR))
                        screen.blit(block, (x_cor, y_cor))
                    x_cor += BLOCK_WIDTH
                y_cor += BLOCK_HEIGHT
                x_cor = 0

            pygame.display.update()
