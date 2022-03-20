########################################################################################
#
# Author Information
#   Name: Brian Lucero
#   Email 1: blucero.cu@gmail.com
#   Email 2: 13rianlucero@csu.fullerton.edu
#
# Program Information
#   Program Name: UDP-Pinger
#   Purpose: This project utilizes a UDP pinger, a tool designed 
#            to send a UDP packet to a target on an unallocated 
#            port and waits for a specific error answer.
#
#
#   Copyright (C) 2022 Brian Lucero
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published
#   by the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
########################################################################################
#
# This File
#   Filename: ClientTest.py
#   Language: Python 3.9.1
#   Run Command: python3 ClientTest.py
#   Purpose: UDP sender: Send the host name and system time as a message to a 
#            destination host designated by its IP address and port number. Repeat the 
#            transmission when enabled to do so.Read and display the returned messages, 
#            and indicate the IP address and port number of the sender. Also, will keep 
#            track of the RTT values of each ping and give a stats summary at the end, 
#            also indicating if there’s packet loss.
#
##### CODE BEGINS: #####################################################################


import socket
from time import *
import sys

######## socket variables
host = "127.0.0.1" # set to server ip or hostname
port = 12002
serverAddress = (host, port)

######## ping variables
number_of_pings = 500 
timeout = 1 # 1 second = max amount of time to make client wait, any longer and it times out
sleep_time = 0

######## message size
message_bytes = 256

######## ping stats variables
min_ping = 999999
max_ping = 0
ping_count = 0
ping_received = 0
avg_ping = 0

######## send out msg to server
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
######## set timeout limit (1 sec)
clientSocket.settimeout(timeout)

####### stats summary 
def summary():
    ######## get end time of ping loop when summary function is called (after 10 pings OR num of pings after timeout)
    ######## subtract start time before ping loop from the end time after ping 
    total_time = (time() - time_start) * 1000

    packet_loss = (ping_count - ping_received) / ping_count * 100

    total_milliseconds = total_time
    total_seconds = total_time / 1000
    total_minutes = total_time / 60000

    ######## print out summary stats
    print("\n\n STATISTICS:")                                   # RTT = Round Trip Time
    print("  Min RTT     = " + str('%.2f'%min_ping) + " ms")    # smallest recorded RTT
    print("  Max RTT     = " + str('%.2f'%max_ping) + " ms")    # biggest recorded RTT
    print("  Avg RTT     = %0.3f ms" % (avg_ping / ping_count)) # average recorded RTT
    print("  Packet Lost = " + str(packet_loss) + "%")          # Packets sent - Packets received
    print("  MDEV        = " + str(max_ping - min_ping))        # MDEV = RTT Deviation from Mean (mean = avg rtt)
    

    print("\n\n ALTERNATE ANALYSIS: ")
    print('  --- %s udp ping statistics ---' % (host))
    print('  %d packets transmitted, %d received, %0.0f%% packet loss,total time %0.0fms' % (ping_count, ping_received, (ping_count - ping_received) / ping_count * 100, total_time))
    print('  rtt min/avg/max/mdev = %0.3f/%0.3f/%0.3f/%0.3f ms' % (min_ping, avg_ping / ping_count, max_ping, max_ping - min_ping))
    
    print("\n\n TOTAL TIME:")
    print("  Total Milli-Seconds: " + str(total_milliseconds))
    print("  Total Seconds:       " + str(total_seconds))
    print("  Total Minutes:       " + str(total_minutes))
    print("--------------------------------------------------------------------------------------")
    sys.exit()

####### get time before the seq of pings starts
time_start = time()

####### ping loop 
for seq in range(number_of_pings):

    ######## set the message
    t = strftime("%H:%M:%S:%S", localtime())
    dt = "Wed Oct 14 " + t + " 2021"
    message = "seq " + str(seq) + " " + str(dt)# + str(byteTracker)

    ######## try to send & receive a message in <= 1 second
    try:
        ####### send message to server
        clientSocket.sendto(message.encode('utf-8'), serverAddress)
        ####### get start time
        start = time()
        ####### record response from server and address
        response, address = clientSocket.recvfrom(2048)
        ####### get end time
        end = time()

        ####### calculate stats 
        elapsed = (end - start) * 1000
        if elapsed < min_ping: min_ping = elapsed
        if elapsed > max_ping: max_ping = elapsed
        ping_count += 1
        ping_received += 1
        avg_ping += elapsed

        ####### update ping counter & stats variables
        # ping_count += 1
        # ping_received += 1
        # avg_ping += ping
        time_delay = elapsed - min_ping # keeps track of the jitter 

        ####### remove byte tracker from response
        # bt = len(str(byteTracker))
        # r = response[:-bt]

        a = str(address)[2:]
        sa = a[:-9]
        b = str(response)[2:]
        res = b[:-1]

        ####### print out response
                 
        print("+-------------------------------------------------------------------------------------+")
        print("| - Ping " + str(seq) + ":" + " host " + sa + " replied: " + res + ", RTT = " + str('%.2f'%elapsed) + " ms")
        # time.sleep(sleep_time) # can be adjusted to see the pings come in more slowly
        # from other file:
        print("|            received %s bytes from %s udp_seq=%d time=%0.1f ms jitter=%0.2f ms" % (len(response), host, seq, elapsed, time_delay))
        print("|            ping_count: " + str(ping_count) + ", ping_received: " + str(ping_received) + ", packet_loss: " + str((ping_count - ping_received) / ping_count * 100) + "%") 
    ####### if socket timesout, no stats will be calculated and ping is not lossless 
    except socket.timeout as e:
        ####### time out message to inform client
        print('>  udp_seq=%d REQUEST TIMED OUT' % (seq))
        ping_count += 1
        print("| --------- (TIMEOUT) ping_count: " + str(ping_count) + ", ping_received: " + str(ping_received) + ", packet_loss: " + str((ping_count - ping_received) / ping_count * 100) + "%") 


####### display stats
summary()
