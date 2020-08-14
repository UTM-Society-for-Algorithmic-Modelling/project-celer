import io
import sys
import astar
from datetime import datetime


# Testing astar and timing some runs

def no_plot_main():
    G, trips = astar.load_data(reset=False, graph=False, trips=False, abbr=False)
    t = astar.random_trip(G)
    astar.process_trips(G, trips=[t], heuristic=astar.distm)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: test.py [# of test runs] [output file name]")
        exit()

    original_stdout = sys.stdout
    sys.stdout = open(sys.argv[2], 'w')

    for i in range(int(sys.argv[1])):
        print("STARTING TRIP %d" % i)
        start = datetime.now()
        no_plot_main()
        end = datetime.now()
        print("Time:", end - start)
        print("DONE TRIP %d" % i)

    sys.stdout.close()
    sys.stdout = original_stdout
    print("Completed")
    exit()
