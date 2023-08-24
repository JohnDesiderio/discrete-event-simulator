"""
Station class that manages all the 
messages received from the executive
simulator.
"""
from matplotlib import pyplot as plt
import numpy as np
import simpy
import csv
import argparse
from Station import Station
from Train import Cargo, Train

"""
TODO: IMPLEMENT THE CARGO CLASS:
- This should follow the same path path finding algorithm
- Every stop check to see if there is cargo that can be dumped off
- Readjust the rate at which new cargo spawns so it does not become overwhelming
- Cargo should be dropped off at the closest point to its destination
"""

def send_message(env, stations):
    """
    This function communicates with the train station
    to tell it to depart a new train.
    """
    for station in stations:
        if station.queue.empty():
            destination = stations[np.random.randint(0, len(stations))]
            while True:
                if destination == station.name:
                    destination = stations[np.random.randint(0, len(stations))]
                else:
                    break
            msg = {'type': 'CARGO', 'contents': destination}
            station.messages.append(msg)
        else:
            #print(f"{station.name}, {station.queue.qsize()} ")
            destination = stations[np.random.randint(0, len(stations))]
            while True:
                if destination.name == station.name:
                    destination = stations[np.random.randint(0, len(stations))]
                else:
                    break
            msg = {'type': 'DEPART', 'contents': destination}
            station.messages.append(msg)
    yield env.timeout(0)


def setup(s_c, seed, t_c, st_c, n, times):
    """
    Generate all the train stations, trains, and
    environment for the trains to run.
    """
    with open(n) as csv_file:
        data = [row for row in csv.reader(csv_file)]
    env = simpy.Environment()
    stations = [Station(x, data[x][0], env, st_c, seed) for x in range(1, len(data))]
    for x in stations:
        x.network = stations
    words = None
    with open(times, newline='') as csvfile:
        words = csv.reader(csvfile, delimiter=' ', quotechar='|')
        graph = []
        for row in words:
            first_city = row[0][:3]
            f_city = None
            for x in stations:
                if first_city == x.name:
                    f_city = x
                    break
            neighbor_cities = row[1].split('-')
            for neigh in neighbor_cities:
                n_city = None
                for x in stations:
                    if neigh == x.name:
                        n_city = x
                        break
                graph.append((f_city.name, n_city.name, int(data[f_city.num][n_city.num])))
    """
    TODO: Implement the arg tag for the number of trains we are using.    
    """
    trains = [Train(x, f"Train #{x}", t_c, graph, data, stations, seed) for x in range(5)]
    # Stuff the trains into the train stations
    for train in trains:
        rand_stat = np.random.randint(1, len(stations))
        stations[rand_stat].queue.put(train)
        train.current = stations[rand_stat]
    for st in stations:
        for c in range(s_c):
            n_place = np.random.randint(0, len(stations))
            while True:
                if n_place != st.num:
                    break
                n_place = np.random.randint(0, len(stations))
            temp = Cargo(st.name, stations[n_place].name, graph)
            temp.calculate_path()
            if len(temp.schedule) == 0:
                continue
            st.cargo.append(temp)
    return stations, graph, env, trains


def run_kernel(env, stations):
    """
    This function mananges the kernels and sends out
    all the new messages.
    """
    while True:
        yield env.process(send_message(env, stations))
        for x_x in stations:
            yield env.process(x_x.receive_message())
        yield env.timeout(1)


if __name__ == '__main__':
    START_CARGO = 8 # starting number of cars in each station
    SEED = 47 # Starting seed
    TRAIN_CARGO = 7 # Size of the train car
    STATION_CARGO_SIZE = 10
    NEIGHBORS_CSV = "Book1.csv"
    TRAVEL_TIMES = "Georgia.csv"
    parser = argparse.ArgumentParser()
    parser.add_argument('-sc', action='store', dest="START_CARGO", default=START_CARGO, type=int)
    parser.add_argument('-seed', action='store', dest="SEED", default=SEED, type=int)
    parser.add_argument('-tc', action='store', dest="TRAIN_CARGO", default=TRAIN_CARGO, type=int)
    parser.add_argument('-stc', action='store', dest="STATION_CARGO_SIZE", default=STATION_CARGO_SIZE, type=int)
    parser.add_argument('-neigh', action='store', dest="NEIGHBORS_CSV", default=NEIGHBORS_CSV, type=str)
    parser.add_argument('-times', action='store', dest="TRAVEL_TIMES", default=TRAVEL_TIMES, type=str)
    args = parser.parse_args()
    START_CARGO = args.START_CARGO
    SEED = args.SEED
    TRAIN_CARGO = args.TRAIN_CARGO
    STATION_CARGO_SIZE = args.STATION_CARGO_SIZE
    NEIGHBORS_CSV = args.NEIGHBORS_CSV
    TRAVEL_TIMES = args.TRAVEL_TIMES
    stations, paths, env, trains = setup(START_CARGO, SEED, TRAIN_CARGO, STATION_CARGO_SIZE, NEIGHBORS_CSV, TRAVEL_TIMES)

    np.random.seed(seed=args.SEED)
    env.process(run_kernel(env, stations))
    env.run(until=500)
    print("-----------------------------------------------------------------")
    print("Post Sim Statistics:")
    for s in stations:
        print(f"{s.name} Station delivered cars: {s.delivered_cars}")
    print("------------------")
    for s in trains:
        print(f"{s.name} current size of luggage: {len(s.luggage)}")
