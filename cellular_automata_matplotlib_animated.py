import matplotlib.animation as animation
import matplotlib.pyplot as plt
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
    ca = CellularAutomata(size=150, rule=182)  # nice one - 30, 126, 150, 60, 182, 73, 90

    fig, ax = plt.subplots(1, 1)

    def animate(frame, inst: CellularAutomata):
        inst.iterate()
        data = np.flipud(inst.grid)  # flip for more natural top-down visualization
        ax.clear()
        ax.set_axis_off()

        # all these show quite same performance: pcolormesh, pcolorfast, imshow (imshow requires non-flipped array)
        ax.pcolorfast(data, cmap='binary')

    manager = plt.get_current_fig_manager()
    manager.set_window_title(f'Rule {int(ca.rule, 2)}')

    ani = animation.FuncAnimation(fig, animate, fargs=(ca,), cache_frame_data=False, interval=1, save_count=0)

    fig.tight_layout()
    plt.show()
