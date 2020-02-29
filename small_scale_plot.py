import psycopg2
from matplotlib import animation
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from _collections import deque

def show_plot(host, port, dbname, user, password, wait_list):
    connect_params = {'host' : host, 'port' : port, 'dbname': dbname, 'user' : user, 'password' : password}
    window_size = 120 # sec
    interval_query = 1000 # ms

    valid_wait_list = ['Client', 'Activity', 'IO', 'LWLock', 'Lock', 'Extension', 'IPC', 'BufferPin', 'Timeout']
    for wait in wait_list:
        if wait not in valid_wait_list:
            raise Exception('You need input valid wait list in configuration file!')
            raise SystemExit
    try:
        connect = psycopg2.connect(**connect_params)
    except Exception as err:
        print(err)
        raise SystemExit
    connect.autocommit = True
    sql_query = '/*NO LOAD BALANCE*/ select event_type, count(*) from pg_wait_sampling_history group by event_type;'
    data = pd.read_sql_query(sql_query, connect)

    # Create base from plot
    matplotlib.use('qt5agg')
    fig, ax = plt.subplots()

    def get_y_lists(wait_list):
        ys_lists = dict()
        ys = []
        for title_line in wait_list:
            ys.append(deque())
            ys_lists[title_line] = ys[-1]
        return ys_lists, ys

    def append_deque(deque, max_length, val):
        if len(deque) == max_length:
            deque.popleft()
        deque.append(val)

    # Start axis X
    plt.xlim(0, window_size)
    xs = deque()
    ys_lists, ys = get_y_lists(wait_list)
    # Create dict with change axis values flags.
    set_y_flags = {title_line: False for title_line in ys_lists.keys()}
    # Create arguments for ax.plot(...)
    xy = []
    for y in ys:
        xy.append(xs)
        xy.append(y)

    def set_property_plot():
        plt.xlabel('Time [sec]')
        plt.ylabel('Count waits')
        plt.title('Monitor waits')
        plt.legend(wait_list)

    def animate(i):
        if xs:
            append_deque(xs, window_size, xs[-1] + 1)
        else:
            append_deque(xs, window_size, 0)
        try:
            data = pd.read_sql_query(sql_query, connect)
        except Exception as err:
            print(err)
            raise SystemExit
        for event_type, count in data.values.tolist():
            if event_type in ys_lists:
                append_deque(ys_lists[event_type], window_size, int(count))
                set_y_flags[event_type] = True
        for event_type in set_y_flags.keys():
            if event_type in ys_lists:
                if set_y_flags[event_type]:
                    set_y_flags[event_type] = False
                else:
                    append_deque(ys_lists[event_type], window_size, 0)
        ax.clear()
        ax.grid()
        #print(xs, '\n', ys, '\n', wait_list, '\n', ys_lists, '\n')
        ax.plot(*xy, linewidth=3)
        set_property_plot()

    anim = animation.FuncAnimation(fig, animate, interval=interval_query)
    ax.clear()
    plt.show()
    connect.close()