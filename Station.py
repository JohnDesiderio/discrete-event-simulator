"""
Working station class
"""
import numpy as np
import queue
import simpy
from Train import shortest_Path, Cargo

class Station:
    """
    This class represents the train station. In this class,
    the train station receives instructions from the simulator
    executive to send a train to a new destination. From there,
    the train will make the judgement on whether to release cargo
    that would be moved further along from its destination.
    """
    def __init__(self, num, name, env: simpy.Environment, cargo_space, seed):
        np.random.seed(seed=seed)
        self.num = num
        self.name = name
        self.env = env
        self.messages = []
        self.queue = queue.Queue(maxsize=10)
        self.network = None
        self.cargo = []
        self.cargo_space = cargo_space
        self.delivered_cars = 0
        
    def receive_message(self):
        """
        Method checks the message list to see if there are
        any messages. This would mean it would generate a new
        cargo car to send to a new place.
        This should only process 1 message an hour in order
        to prevent a clog up of trains leaving
        """
        if len(self.messages) == 0:
            # Do not do anything if there are no messages
            yield self.env.timeout(1)
        # Read all the current messages in the queue
        for x in range(len(self.messages)):
            msg = self.messages.pop(0)
            if msg['type'] == 'CARGO':
                print(f"{self.env.now}: {self.name} has received new cargo")
                temp = Cargo(self.name, msg['contents'].name, msg['paths'])
                temp.calculate_path()
                self.cargo.append(temp)
            else:
                if not self.queue.empty():
                    # this brings forward a train
                    departed = self.queue.get(0)
                    print(f"{self.env.now}: {self.name} has received a order to prep a train for {msg['contents'].name}")
                    yield self.env.process(self.travel(departed, msg['contents']))
                    print(f"{self.env.now}: {self.name} sent away {departed.name}")

    def travel(self, train, dest: "Station"):
        """
        The train travels to the destination(s).
        """
        train.path = shortest_Path(train.graph, train.current.name, dest.name)
        new_place = None
        
        for place in train.path[1][1:]:
            yield self.env.timeout(1)
            train.check_cargo(self.env)
            train.update_cargo(self.env)
            train.drop_cargo_off(self.env)
            for x in train.network:
                if place == x.name:
                    new_place = x
            time_delay = int(train.time[train.current.num][new_place.num])
            print(f"{self.env.now}: {train.name} departed from {train.current.name} to {new_place.name} for a {time_delay} hour trip.")
            #print(f"{self.env.now}: {train.name} is carrying {len(train.luggage)} cars!")
            yield self.env.timeout(time_delay)
            train.current = new_place
        new_place.queue.put(train)


        
if __name__ == '__main__':
    print("Everything is going according to plan")
    print("Hehehehehehehehehehehehehehehehehehe")
