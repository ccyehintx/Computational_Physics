# IPython log file

import matplotlib.pyplot as plt
import numpy as np

def neig_ls(idx, n):
    cx = idx%n
    cy = idx//n
    nx = list([cx - 1, cx + 1])
    ny = list([cy - 1, cy + 1])
    nxn = [ele for ele in nx if ele >= 0 and ele < n]
    nyn = [ele for ele in ny if ele >= 0 and ele < n]
    out = []
    for i in nxn:
        ij = i + cy*n
        out.append(ij)
    for j in nyn:
        ij = cx + j*n
        out.append(ij)
    return out

def project(arr, n):
    zz = np.zeros((n, n))
    for idx in range(len(arr[0])):
        x = idx%n
        y = idx//n
        zz[y][x] = arr[0][idx]
    return zz
def check_difference(grid1, grid2):
    return np.sum(grid1 != grid2)
    
def run(n, itersmax):
    current_grid = np.random.choice([0, 1, 2, 3], size=(1, n**2))
    iters = 0
    collector = []
    collector.append(current_grid)
    topple_ls = []
    big_grid = []
    while iters < 10000:
        iters = iters + 1
        first_sand_idx = np.random.randint(n**2)
        current_grid = collector[-1]
        current_grid[0][first_sand_idx] = current_grid[0][first_sand_idx] + 1
        over4 = [i for i, e in enumerate(list(current_grid)[0]) if e>=4]
        if len(over4) == 0:
            collector.append(current_grid)
            big_grid.append(project(current_grid, n))
            topple_ls.append(0)
            continue
        else:
            update_grid = np.random.choice([0], size=(1, n**2))
            topple_ls.append(len(over4))
            for i in over4:
                nls = neig_ls(i, n)
                update_grid[0][i] = update_grid[0][i] - 4
                for j in nls:
                    update_grid[0][j] = update_grid[0][j] + 1
            current_grid = current_grid + update_grid
            collector.append(current_grid)
            big_grid.append(project(current_grid, n))
    return collector, big_grid
        
n = 100
collector = run(n, 10000)[0]
big_grid = run(n, 10000)[1]
arrf = project(collector[1], n)
arrl = project(collector[-1], n)

plt.figure()
plt.imshow(arrf, cmap='gray')
plt.title("Initial State")

plt.show()

plt.figure()
plt.imshow(arrl, cmap='gray')
plt.title("Final State")

plt.show()


all_events =  [check_difference(*states) for states in zip(big_grid[:-1], big_grid[1:])]
all_events = all_events[1000:]
# index each timestep by timepoint
all_events = list(enumerate(all_events))
# remove cases where an avalanche did not occur
all_avalanches = [x for x in all_events if x[1] > 1]
all_avalanche_times = [item[0] for item in all_avalanches]
all_avalanche_sizes = [item[1] for item in all_avalanches]
all_avalanche_durations = [event1 - event0 for event0, event1 in zip(all_avalanche_times[:-1], all_avalanche_times[1:])]
log_bins = np.logspace(np.log10(2), np.log10(np.max(all_avalanche_durations)), 50) # logarithmic bins for histogram
vals, bins = np.histogram(all_avalanche_durations, bins=log_bins)
plt.figure()
plt.loglog(bins[:-1], vals, '.', markersize=10)
plt.title('Avalanche duration distribution')
plt.xlabel('Avalanche duration')
plt.ylabel('Count')
plt.show()
all_diffs = np.abs(np.diff(np.array(big_grid), axis=0))
all_diffs[all_diffs > 0] = 1
all_diffs = all_diffs[np.sum(all_diffs, axis=(1, 2)) > 1] # Filter to only keep big events
most_recent_events = np.sum(all_diffs[-100:], axis=0)
plt.figure(figsize=(5, 5))
plt.imshow(most_recent_events)
plt.title("Avalanche activity in most recent timesteps")
plt.show()
