import matplotlib.pyplot as plt
import numpy
import random

(L, R) = [3600, 72000000]
T = L/R

class Station(object):
    def __init__(self, index):
        self.index = index
        self.buffer = Buffer()
        self.state = 'Thinking'
        self.backoff_time = 0

    def try_to_transmit(self, slot):
        if not self.buffer.isempty():
            slot.add_to_transmission_queue(self.index)

    def successfully_transmitted(self):
            self.buffer.removepacket()
            self.state = 'Thinking'

    def receivedpacket(self, p):
        if self.buffer.isempty() and random.random() <= p:
            self.buffer.storepacket(Packet())
            return True
        return False

    def getstate(self):
        return self.state

    def set_backoff_time(self, backoff_time):
        self.backoff_time = backoff_time

    def get_backoff_time(self):
        return self.backoff_time

class Buffer(object):
    def __init__(self):
        self.capacity = L
        self.stored_packet = 0
        self.empty = True

    def isempty(self):
        return self.empty

    def storepacket(self, packet):
        if self.empty:
            self.stored_packet = packet
            self.empty = False

    def removepacket(self):
        self.empty = True


class Packet(object):
    def __init__(self):
        self.size = L


class Slot(object):
    def __init__(self, start):
        self.duration = T
        self.start = start
        self.end = start + self.duration
        self.transmitting_stations = []
        self.state = 'idle'

    def add_to_transmission_queue(self, station_index):
        self.transmitting_stations.append(station_index)
        self.state = 'busy'

    def transmission_successful(self):
        return len(self.transmitting_stations) == 1

    def get_station_index(self):
        return self.transmitting_stations[0]

class Simulator(object):
    def __init__(self, K, N, special_case):
        self.K = K
        self.N = N
        self.times = len(K)*len(N)
        self.special_case = False
        if special_case:
            self.times = self.times + 1
            self.special_case = True
        self.G = [[] for i in range(self.times)]
        self.S = [[] for i in range(self.times)]
        self.D = [[] for i in range(self.times)]
        self.Expected_N_T = [[] for i in range(self.times)]

    def simulate(self):
        print("Starting simulation...")
        num = 0
        for k in K:
            for n in N:
                print("Simulating K = " + repr(k) + ", N = " + repr(n) +".")
                self.compute(k, n, num)
                num = num + 1
        if self.special_case:
            print("Simulating K = 10, N = 10.")
            self.compute(10, 10, num)
        print("Finished simulation.")

    def compute(self, k, n, num):
        stationlist = [Station(index) for index in range(n)]
        timeslots = [Slot(i * T) for i in range(0, 101, 1)]
        prev_slot = timeslots[0]
        self.G[num] = numpy.linspace(0.01, 3, 1000)
        p_list = numpy.divide(self.G[num], n)

        for p in p_list:
            successfully_transmitted_packets = 0
            for i in range(len(timeslots)):
                current_slot = timeslots[i]
                if i > 0 and prev_slot.transmission_successful():
                    successfully_transmitted_packets = successfully_transmitted_packets + 1
                    index = prev_slot.get_station_index()
                    stationlist[index].successfully_transmitted()
                else:
                    for index in prev_slot.transmitting_stations:
                        stationlist[index].set_backoff_time(random.randint(1, k))

                for station in stationlist:
                    if station.getstate() == 'Thinking':
                        if station.receivedpacket(p):
                            station.try_to_transmit(current_slot)
                    elif station.getstate() == 'Backlogged':
                        if station.get_backoff_time() == 0:
                            if random.random() > p:
                                station.try_to_transmit(current_slot)
                        else:
                            station.set_backoff_time(station.get_backoff_time() - 1)

                prev_slot = current_slot
            self.S[num].append(successfully_transmitted_packets / 100)

        self.Expected_N_T[num] = numpy.divide(self.G[num], self.S[num])
        self.D[num] = 1 - numpy.divide(1, p_list) + numpy.divide(n, self.S[num]) + k / 2

    def plot_performance_curves(self):
        print("Plotting performance curves...")
        label_list = ['K = 4, N = 4', 'K = 4, N = 16', 'K = 10, N = 4', 'K = 10, N = 16']
        if self.special_case:
            label_list.append('K = 10, N = 10')

        for i in range(self.times):
            plt.plot(self.G[i]/0.08, self.S[i], label=label_list[i])
            plt.xlim(0, 3)
        plt.ylabel('Throughput S')
        plt.xlabel('Load G')
        plt.title('S vs. G Performance Curve')
        plt.legend()
        plt.show()

        for i in range(self.times):
            plt.plot(self.G[i]/0.08, self.Expected_N_T[i], label=label_list[i])
            plt.xlim(0, 10)
        plt.ylabel('Average number of transmissions to success E(N_T)')
        plt.xlabel('Load G')
        plt.title('E(N_T) vs. G Performance Curve')
        plt.legend()
        plt.show()

        for i in range(self.times):
            plt.plot(self.G[i]/0.08, self.D[i], label=label_list[i])
            plt.xlim(0, 20)
        plt.ylabel('Average delay time D')
        plt.xlabel('Load G')
        plt.title('D vs. G Performance Curve')
        plt.legend()
        plt.show()

        for i in range(self.times):
            plt.plot(self.S[i], self.D[i], label=label_list[i])
            plt.ylim(0, 1500)
        plt.ylabel('Average delay time D')
        plt.xlabel('Throughput S')
        plt.title('D vs. S Performance Curve')
        plt.legend()
        plt.show()
        print("Finished plotting.")

if if __name__ == "__main__":
    K = [4, 10]
    N = [4, 16]
    sim1 = Simulator(K, N, special_case=False)
    sim1.simulate()
    sim1.plot_performance_curves()

    #Simulate the special case with K = 10, N = 10
    sim2 = Simulator(K, N, special_case=True)
    sim2.simulate()
    sim2.plot_performance_curves()