#!/usr/bin/env python3
from threading import Thread, Event, Lock
import threading
import time
import random
import iperf3
import asyncio
from socket import *
from click import command, option, Choice
from socksx.socks6 import Client
from socksx.socket import SocketAddress
from socket import fromfd, AF_INET, SOCK_STREAM

@command()
@option('-d', '--debug', default=False, help="Prints debug information")
@option('-d', '--destination', default="145.100.135.52:30020", help="Address of the destination")
@option('-p', '--proxy', default='145.100.135.52:30007', help="Address of the proxy")
@option('-s', '--socks', default=6, type=Choice([6]), help="SOCKS version")


def cli(**kwargs):
    print("here")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop, **kwargs))

# We'll limit ourself to a 1000KB/sec maximum send rate
maxSendRateBytesPerSecond = (1000*1024)

def ConvertSecondsToBytes(numSeconds):
    return numSeconds*maxSendRateBytesPerSecond

def ConvertBytesToSeconds(numBytes):
    return float(numBytes)/maxSendRateBytesPerSecond


async def main(loop, debug, destination, proxy, socks):
    """
    """
    # --debug  and --socks are currently ignored.
    destination = SocketAddress(destination)

    client = Client(proxy)
    try:
        socket = await client.connect(destination)
     # Convert to Python socket.
        raw_fd = await socket.get_raw_fd()
        print(f"RAW SOCKET FD: {raw_fd}")
#    time.sleep(seconds)
#    with open('./socksx/socksx-py/examples/test-files/1M.txt', 'rb') as file:
#        sendfile = file.read()
        py_socket = fromfd(raw_fd, AF_PACKET, SOCK_RAW)

# We'll add to this tally as we send() bytes, and subtract from
# at the schedule specified by (maxSendRateBytesPerSecond)
        bytesAheadOfSchedule = 0

# Dummy data buffer, just for testing
        dataBuf = bytearray(1024)

        prevTime = None
    
        idx = random.randint(100, 200)
        idx = 30
        while idx:
            now = time.time()
            if (prevTime != None):
                bytesAheadOfSchedule -= ConvertSecondsToBytes(now-prevTime)
            prevTime = now

            numBytesSent = py_socket.send(dataBuf)
            if (numBytesSent > 0):
                bytesAheadOfSchedule += numBytesSent
            # print("sent {} bytes".format(bytesAheadOfSchedule))
                if (bytesAheadOfSchedule > 0):
                    time.sleep(ConvertBytesToSeconds(bytesAheadOfSchedule))
            else:
                print("Error sending data, exiting!")
                break
            idx -= 1
        
 #print py_socket.recvfrom(65565)
        print(py_socket)
    except Exception as e:
        print('catched error')
###    py_socket.recv(40)
#    iclient = iperf3.Client()
#    iclient.run()

if __name__ == "__main__":
     cli()

#    threads = []
#    input = input("Enter the number of clients you want to spawn:")
#    num_of_threads = int(input)
#    for t in range(num_of_threads):
#      th = threading.Thread(target=main)
#      threads.append(th)
#      th.setDaemon(True)
#      th.start()

#    for thread in threads:
#      thread.join()
