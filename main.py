from multiprocessing import Process, Pipe
from os import getpid

def calc_recv_timestamp(recv_time_stamp, counter, pid):
    pid_counter = max(recv_time_stamp[pid], counter[pid]) + 1

    recv_time_stamp[pid] = pid_counter
    return recv_time_stamp

def event(pid, counter):
    counter[pid] += 1
    return counter

def send_message(pipe, pid, counter):
    counter[pid] += 1
    pipe.send(('Empty shell', counter))
    return counter

def recv_message(pipe, pid, counter):
    message, timestamp = pipe.recv()
    counter = calc_recv_timestamp(timestamp, counter, pid)
    return counter

def process_a(pipe_ab):
    pid = 0
    counter = [0, 0, 0]

    counter = send_message(pipe_ab, pid, counter)
    counter = send_message(pipe_ab, pid, counter)
    counter = event(pid, counter)
    counter = recv_message(pipe_ab, pid, counter)
    counter = event(pid, counter)
    counter = event(pid, counter)
    counter = recv_message(pipe_ab, pid, counter)

    print("Process a ", counter)

def process_b(pipe_ba, pipe_bc):
    pid = 1
    counter = [0, 0, 0]

    counter = recv_message(pipe_ba, pid, counter)
    counter = recv_message(pipe_ba, pid, counter)
    counter = send_message(pipe_ba, pid, counter)
    counter = recv_message(pipe_bc, pid, counter)
    counter = event(pid, counter)
    counter = send_message(pipe_ba, pid, counter)
    counter = send_message(pipe_bc, pid, counter)
    counter = send_message(pipe_bc, pid, counter)

    print("Process b ", counter)

def process_c(pipe_cb):
    pid = 2
    counter = [0, 0, 0]

    counter = send_message(pipe_cb, pid, counter)
    counter = recv_message(pipe_cb, pid, counter)
    counter = event(pid, counter)
    counter = recv_message(pipe_cb, pid, counter)

    print("Process c ", counter)

if __name__ == '__main__':
    ab, ba = Pipe()
    bc, cb = Pipe()

    oneandtwo, twoandone = Pipe()
    twoandthree, threeandtwo = Pipe()

    process1 = Process(target=process_a, 
                       args=(oneandtwo,))
    process2 = Process(target=process_b, 
                       args=(twoandone, twoandthree))
    process3 = Process(target=process_c, 
                       args=(threeandtwo,))

    process1.start()
    process2.start()
    process3.start()

    process1.join()
    process2.join()
    process3.join()
