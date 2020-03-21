from reference import check_ignition
from collections import defaultdict

def adjacency_range(m, point):
    """gives a list of adjacent points for a point in one dimension"""
    
    if point == m - 1:
        adjacent_range = [point - 1, point]
    elif point == 0:
        adjacent_range = [point, point + 1]
    else:
        adjacent_range = [point - 1, point, point + 1]
    
    return adjacent_range

def run_model_with_burn_count(f_grid, h_grid, i_threshold, w_direction,
                              burn_seeds, burnt_cell_count):
    """ returns a tuple containing (a) the final state of the landscape once the
    fire has stopped burning, and (b) the total number of cells that have been 
    burnt by the fire (including any initially burning cells in burn_seeds)."""
    
    m = len(f_grid)
    
    # creates b_grid: a list of lists representing what is currently burning 
    b_grid = []
    for i_num in range(m):
        i_row = []
        for j_num in range(m):
            if (i_num, j_num) in burn_seeds:
                i_row.append(True)
            else:
                i_row.append(False)
        b_grid.append(i_row)
        
    # creates a list of cells that are adjacent to the burning seeds 
    adjacent_cells = []
    for seed in burn_seeds:
        for i_num in adjacency_range(m, seed[0]):
            for j_num in adjacency_range(m, seed[1]):
                adjacent_cells.append([i_num, j_num])
        
    # reduces fuel load where there are burnt seeds
    for seed in burn_seeds:
        if f_grid[seed[0]][seed[1]] > 0:
            f_grid[seed[0]][seed[1]] -= 1

    # creates a new list of burn_seeds consisting if adjacent cells that have 
    # ignited. Cells are considered ignited if they have if they still have 
    # fuel, are not currently in burn_seeds, and fulfils check_ignition 
    # conditions
    new_burn_seeds = []
    for cell in adjacent_cells:
        if (check_ignition(b_grid, f_grid, h_grid, i_threshold, w_direction, 
                          cell[0], cell[1]) and 
            f_grid[cell[0]][cell[1]] > 0 and 
            (cell[0], cell[1]) not in burn_seeds and 
            (cell[0], cell[1]) not in new_burn_seeds):
            new_burn_seeds.append((cell[0], cell[1]))
    
    for seed in burn_seeds:
        if f_grid[seed[0]][seed[1]] > 0:
            new_burn_seeds.append((seed[0], seed[1]))
        else:
            burnt_cell_count +=1

    if new_burn_seeds:
        return run_model_with_burn_count(f_grid, h_grid, i_threshold, 
                                         w_direction, new_burn_seeds,
                                         burnt_cell_count)
    else:
        return(f_grid, burnt_cell_count)

def run_model(f_grid, h_grid, i_threshold, w_direction, burn_seeds):
    
    burnt_cell_count = 0
    
    return (run_model_with_burn_count(f_grid, h_grid, i_threshold, w_direction,
                                     burn_seeds, burnt_cell_count))
