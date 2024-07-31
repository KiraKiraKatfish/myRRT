import matplotlib.pyplot as plt
import json
import numpy as np

def get_data(map_id, yes_hull, hull_size, trial):
    if yes_hull:
        path = "Results/Map" + str(map_id) + "/Hull/" + str(hull_size)
        with open(path + "/map" + str(map_id) + "_hullSize" + str(hull_size) + "_trial" + str(trial) + ".json", 'r') as f:
            return json.load(f)
    else:
        path = "Results/Map" + str(map_id) + "/NoHull"
        with open(path + "/map" + str(map_id) + "_trial" + str(trial) + ".json", 'r') as f:
            return json.load(f)
        
def get_any_percent(data):
    for pair in data:
        # pair = [time, length]
        if pair[1] < 1000:
            return pair
    return []
    # data = [x for x in data if x[1] < 1000]

def get_last(data):
    return data[-1]

def get_avg_any_percent(map_id, yes_hull, hull_size):
    times = []
    lengths = []
    num_trials = 5

    for i in range(1,num_trials+1):
        data = get_data(map_id,yes_hull,hull_size,i)
        any_percent = get_any_percent(data)
        if not any_percent:
            print("PATH NOT FOUND")
            return []
        times.append(any_percent[0])
        lengths.append(any_percent[1])

    avg_time = sum(times)/num_trials
    avg_length = sum(lengths)/num_trials

    return [avg_time,avg_length]

def plot_hull_size_to_avg_any_percent(map_id,ax):
    # fig, ax = plt.subplots()
    ticks = [4,5,6,7,8,9,10]
    ax.set_xticks(ticks)
    # set axis
    ax.set_xlim([3,11])
    ax.set_ylim([0,4])

    x,y = [],[]
    for i in range(4,11):
        avg_any_percent = get_avg_any_percent(map_id,True,i)
        x.append(i)
        y.append(avg_any_percent[0])

    # convert to numpy to calculate line of best fit
    x = np.array(x)
    y = np.array(y)

    #find line of best fit
    a, b = np.polyfit(x, y, 1)

    #add points to plot
    ax.scatter(x, y, label="Bounding Hull vs. Avg Time to Path")

    #add line of best fit to plot
    ax.plot(x, a*x+b, color = 'steelblue', linestyle='--', label="Line of Best Fit")
    ax.text(3.2, b.item() + 0.2, 'y = ' + '{:.2f}'.format(b) + ' + {:.2f}'.format(a) + 'x', size=10, color='steelblue')

    # plot control
    control_any_percent = get_avg_any_percent(map_id,False,0)
    ax.axhline(y = control_any_percent[0], color='r', linestyle='--', label="Control (No Bounding Hull)\nAvg Time to Path")
    ax.text(3.2, control_any_percent[0] + 0.1, 'y = ' + '{:.2f}'.format(control_any_percent[0]), size=10, color='red')


    if map_id == 1:
        ax.legend(loc='upper right')

# get the average difference between control any percent, and each hull's average any percent
def get_avg_diff_time(map_id):
    x,y = [],[]
    for i in range(4,11):
        avg_any_percent = get_avg_any_percent(map_id,True,i)
        x.append(i)
        y.append(avg_any_percent[0])

    control_any_percent = get_avg_any_percent(map_id,False,0)
    
    diff = []
    for time in y:
        diff.append(time-control_any_percent[0])
    avg_diff = sum(diff)/len(diff)
    return avg_diff


def get_refinement(data):
    first_length = []
    last_length = []
    
    for pair in data:
        # pair = [time, length]
        if pair[1] < 1000:
            first_length = pair
            break

    # Edge Case: if unsolved, dont proceed
    if first_length:
        # get the data 0.5 seconds after first length
        t_floor = first_length[0] + 0.5
        for pair in data:
            if pair[0] >= t_floor:
                last_length = pair
                break

    print(first_length)
    if last_length:
        # avg rate of change for 0.5 secs after path discovered
        slope = (last_length[1]-first_length[1])/(last_length[0]-first_length[0])
        return slope
    
    return []
        
def plot_all_hull_to_any_percent():
    fig, axarr = plt.subplots(1, 3)
    fig.suptitle('The Effect of # Vertices in Bounding Hull on Avg Time for RRT* to find any path')
    plot_hull_size_to_avg_any_percent(1,axarr[0])
    plot_hull_size_to_avg_any_percent(2,axarr[1])
    plot_hull_size_to_avg_any_percent(3,axarr[2])

    axarr[0].set_title('Zig-Zag Map')
    axarr[1].set_title('Maze Map')    
    axarr[2].set_title('Forest Map')

    # Set common labels
    fig.text(0.5, 0.04, 'Vertices in Bounding Hull', ha='center', va='center')
    fig.text(0.06, 0.5, 'Avg Time Until Any Path Found (s)', ha='center', va='center', rotation='vertical')

    plt.show()

def plot_hull_size_to_avg_first_length(map_id,ax):
    # fig, ax = plt.subplots()
    ticks = [4,5,6,7,8,9,10]
    ax.set_xticks(ticks)
    # set axis
    ax.set_xlim([3,11])
    ax.set_ylim([0,150])

    x,y = [],[]
    for i in range(4,11):
        avg_first_length = get_avg_any_percent(map_id,True,i)
        x.append(i)
        y.append(avg_first_length[1])

    # convert to numpy to calculate line of best fit
    x = np.array(x)
    y = np.array(y)

    #find line of best fit
    a, b = np.polyfit(x, y, 1)

    #add points to plot
    ax.scatter(x, y, label="Bounding Hull vs. Avg Initial Path Length")

    #add line of best fit to plot
    ax.plot(x, a*x+b, color = 'steelblue', linestyle='--', label="Line of Best Fit")
    ax.text(3.2, b.item() - 10, 'y = ' + '{:.2f}'.format(b) + ' + {:.2f}'.format(a) + 'x', size=10, color='steelblue')

    # plot control
    control_any_percent = get_avg_any_percent(map_id,False,0)
    ax.axhline(y = control_any_percent[1], color='r', linestyle='--', label="Control (No Bounding Hull)\nAvg Initial Path Length")
    ax.text(3.2, control_any_percent[1] + 5, 'y = ' + '{:.2f}'.format(control_any_percent[1]), size=10, color='red')


    if map_id == 1:
        ax.legend(loc='upper right')

def plot_all_hull_to_avg_first_length():
    fig, axarr = plt.subplots(1, 3)
    fig.suptitle('The Effect of # Vertices in Bounding Hull on RRT*\'s Avg Initial Path Length')
    plot_hull_size_to_avg_first_length(1,axarr[0])
    plot_hull_size_to_avg_first_length(2,axarr[1])
    plot_hull_size_to_avg_first_length(3,axarr[2])

    axarr[0].set_title('Zig-Zag Map')
    axarr[1].set_title('Maze Map')    
    axarr[2].set_title('Forest Map')

    # Set common labels
    fig.text(0.5, 0.04, 'Vertices in Bounding Hull', ha='center', va='center')
    fig.text(0.06, 0.5, 'Avg Initial Path Length', ha='center', va='center', rotation='vertical')

    plt.show()

# get the average difference between control any percent, and each hull's average any percent
def get_avg_diff_length(map_id):
    x,y = [],[]
    for i in range(4,11):
        avg_any_percent = get_avg_any_percent(map_id,True,i)
        x.append(i)
        y.append(avg_any_percent[1])

    control_any_percent = get_avg_any_percent(map_id,False,0)
    
    diff = []
    for length in y:
        diff.append(length-control_any_percent[1])
    avg_diff = sum(diff)/len(diff)
    return avg_diff

if __name__ == "__main__":
    no_hull = get_data(1,False,5,1)
    hull = get_data(1,True,5,1)

    # x,y = zip(*no_hull)
    # plt.plot(x,y)
    # plt.show()

    # x,y = zip(*hull)
    # plt.plot(x,y)
    # plt.show()

    # print(get_any_percent(get_data(2,True,10,1)))
    # print(get_any_percent(get_data(2,True,10,2)))
    # print(get_any_percent(get_data(2,True,10,3)))
    # print(get_any_percent(get_data(2,True,10,4)))
    # print(get_any_percent(get_data(2,True,10,5)))    
    # plot_hull_size_to_avg_any_percent(3)
    # print(get_avg_diff_time(3))

    # plot_all_hull_to_any_percent()
    # plot_all_hull_to_avg_first_length()
    print(get_avg_diff_time(3))
    print(get_avg_diff_length(3))