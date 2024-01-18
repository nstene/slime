import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# setting up the values for the grid
ON = 255
OFF = 0
vals = [ON, OFF]


def mySlimeGrid(N):
    grid_array = np.array([0]*(N*N))
    grid = grid_array.reshape(N, N)
    used_grid = grid.copy()
    grid[round(N / 2), round(N / 2)] = 255
    grid[round(N / 2) + 1, round(N / 2) + 1] = 255
    grid[round(N / 2) + 1, round(N / 2)] = 255
    grid[round(N / 2), round(N / 2) + 1] = 255
    return grid, used_grid


def update(frameNum, img, grid, usedGrid, N, energy, gen_prob, n_neighbours):
    newGrid = grid.copy()
    newUsedGrid = usedGrid.copy()
    for i in range(N):
        for j in range(N):
            if grid[i, j] == ON:

                # compute neighbor sum
                # using toroidal boundary conditions - x and y wrap around
                # so that the simulaton takes place on a toroidal surface.
                if n_neighbours == 8:
                    total = int((grid[i, (j - 1) % N] +
                                 grid[i, (j + 1) % N] +
                                 grid[(i - 1) % N, j] +
                                 grid[(i + 1) % N, j] +
                                 grid[(i - 1) % N, (j - 1) % N] +
                                 grid[(i - 1) % N, (j + 1) % N] +
                                 grid[(i + 1) % N, (j - 1) % N] +
                                 grid[(i + 1) % N, (j + 1) % N]) / 255)
                elif n_neighbours == 4:
                    total = int((grid[i, (j - 1) % N] +
                                 grid[i, (j + 1) % N] +
                                 grid[(i - 1) % N, j] +
                                 grid[(i + 1) % N, j]) / 255)

                # apply Slime's rules
                generation = False
                if (total >= 1) and (usedGrid[i, j] == 0):
                    if n_neighbours == 8:
                        directionPossibilities = [grid[i, (j - 1) % N], grid[i, (j + 1) % N], grid[(i - 1) % N, j],
                                                  grid[(i + 1) % N, j], grid[(i - 1) % N, (j - 1) % N], grid[(i - 1) % N, (j + 1) % N],
                                                  grid[(i + 1) % N, (j - 1) % N], grid[(i + 1) % N, (j + 1) % N]]
                    elif n_neighbours == 4:
                        directionPossibilities = [grid[i, (j - 1) % N], grid[i, (j + 1) % N], grid[(i - 1) % N, j],
                                                  grid[(i + 1) % N, j]]
                    empty_cells = [i for i, e in enumerate(directionPossibilities) if e == OFF]

                    if not empty_cells:
                        continue

                    direction = np.random.choice(empty_cells, energy)

                    if 0 in direction:
                        rand = np.random.random()
                        if rand <= gen_prob:
                            newGrid[i, (j - 1) % N] = ON
                            generation = True
                    if 1 in direction:
                        rand = np.random.random()
                        if rand <= gen_prob:
                            newGrid[i, (j + 1) % N] = ON
                            generation = True
                    if 2 in direction:
                        rand = np.random.random()
                        if rand <= gen_prob:
                            newGrid[(i - 1) % N, j] = ON
                            generation = True
                    if 3 in direction:
                        rand = np.random.random()
                        if rand <= gen_prob:
                            newGrid[(i + 1) % N, j] = ON
                            generation = True
                    if 4 in direction:
                        rand = np.random.random()
                        if rand <= gen_prob:
                            newGrid[(i - 1) % N, (j - 1) % N] = ON
                            generation = True
                    if 5 in direction:
                        rand = np.random.random()
                        if rand <= gen_prob:
                            newGrid[(i - 1) % N, (j + 1) % N] = ON
                            generation = True
                    if 6 in direction:
                        rand = np.random.random()
                        if rand <= gen_prob:
                            newGrid[(i + 1) % N, (j - 1) % N] = ON
                            generation = True
                    if 7 in direction:
                        rand = np.random.random()
                        if rand <= gen_prob:
                            newGrid[(i + 1) % N, (j + 1) % N] = ON
                            generation = True
                    #else:
                    #    if grid[i, (j - 1) % N] == OFF:
                    #        rand = np.random.random()
                    #        if rand <= gen_prob:
                    #            newGrid[i, (j - 1) % N] = ON
                    #            generation = True
                    #    if grid[i, (j + 1) % N] == OFF:
                    #        rand = np.random.random()
                    #        if rand <= gen_prob:
                    #            newGrid[i, (j + 1) % N] = ON
                    #            generation = True
                    #    if grid[(i - 1) % N, j] == OFF:
                    #        rand = np.random.random()
                    #        if rand <= gen_prob:
                    #            newGrid[(i - 1) % N, j] = ON
                    #            generation = True
                    #    if grid[(i + 1) % N, j] == OFF:
                    #        rand = np.random.random()
                    #        if rand <= gen_prob:
                    #            newGrid[(i + 1) % N, j] = ON
                    #            generation = True
#
                    #    if n_neighbours == 8:
                    #        if grid[(i - 1) % N, (j - 1) % N] == OFF:
                    #            rand = np.random.random()
                    #            if rand <= gen_prob:
                    #                newGrid[(i - 1) % N, (j - 1) % N] = ON
                    #                generation = True
                    #        if grid[(i - 1) % N, (j + 1) % N] == OFF:
                    #            rand = np.random.random()
                    #            if rand <= gen_prob:
                    #                newGrid[(i - 1) % N, (j + 1) % N] = ON
                    #                generation = True
                    #        if grid[(i + 1) % N, (j - 1) % N] == OFF:
                    #            rand = np.random.random()
                    #            if rand <= gen_prob:
                    #                newGrid[(i + 1) % N, (j - 1) % N] = ON
                    #                generation = True
                    #        if grid[(i + 1) % N, (j + 1) % N] == OFF:
                    #            rand = np.random.random()
                    #            if rand <= gen_prob:
                    #                newGrid[(i + 1) % N, (j + 1) % N] = ON
                    #                generation = True



                    # If at least one cell has been created from this one, we call this cell 'used'
                    if generation:
                        newUsedGrid[i, j] = 1

    # update data
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    usedGrid[:] = newUsedGrid[:]
    return img,


# main() function
def main(grid_size, energy, gen_prob, n_neighbours):
    if energy > n_neighbours:
        raise ValueError('energy should be between 1 and n_neighbours')
    if gen_prob > 1:
        raise ValueError('gen_prob should be between 0 and 1')
    if n_neighbours not in {4, 8}:
        raise ValueError('n_neighbours should be either 4 or 8')
    N = grid_size
    # Command line args are in sys.argv[1], sys.argv[2] ..
    # sys.argv[0] is the script name itself and can be ignored
    # parse arguments
    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life simulation.")

    # add arguments
    parser.add_argument('--grid-size', dest='N', required=False)
    parser.add_argument('--mov-file', dest='movfile', required=False)
    parser.add_argument('--interval', dest='interval', required=False)
    parser.add_argument('--glider', action='store_true', required=False)
    parser.add_argument('--gosper', action='store_true', required=False)
    args = parser.parse_args()

    # set grid size
    if args.N and int(args.N) > 8:
        N = int(args.N)

    # set animation update interval
    updateInterval = 50
    if args.interval:
        updateInterval = int(args.interval)

    grid, usedGrid = mySlimeGrid(N)

    # set up animation
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, usedGrid, N, energy, gen_prob, n_neighbours),
                                  frames=10,
                                  interval=updateInterval,
                                  save_count=50)

    # # of frames?
    # set output file
    if args.movfile:
        ani.save(args.movfile, fps=30, extra_args=['-vcodec', 'libx264'])

    plt.show()


# call main
if __name__ == '__main__':
    # grid_size is the side of the grid. Then total area will be grid_size^2
    # energy is the number of cells that could grow from a single source (number of directions, from 1 to n_neighbours)
    # gen_prob is the probability of cell generation in each possible direction from a source
    # n_neighbours is the number of neighbours each cell has (which cell it can see or interact with). On such grid it would be either 4 or 8
    main(grid_size=100, energy=2, gen_prob=0.3, n_neighbours=4)