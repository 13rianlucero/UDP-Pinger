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
#   Filename: BL1-UDP-Client.py
#   Language: Python 3.9.1
#   Run Command: python3 BL1-UDP-Client.py
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
port = 12000
serverAddress = (host, port)

######## ping variables
number_of_pings = 10
timeout = 1 # 1 second = max amount of time to make client wait, any longer and it times out
sleep_time = 0

######## message size
message_bytes = 256
#byteTracker = bytearray([1] * message_bytes)

######## ping stats variables
min_ping = 999999
max_ping = 0
ping_count = 0
ping_received = 0
avg_ping = 0

######## RTT variables
minRTT = 0
maxRTT = 0
avgRTT = 0

######## send out msg to server
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
######## set timeout limit (1 sec)
clientSocket.settimeout(timeout)

####### stats summary 
def summary():
    ######## get end time of ping loop when summary function is called (after 10 pings OR num of pings after timeout)
    ######## subtract start time before ping loop from the end time after ping 
    # total_time = (time.time() - time_start) * 1000
    
    ######## calculate stats
    packet_loss = (ping_count - ping_received) / ping_count * 100
    avgRTT = avg_ping / ping_count
    minRTT = min_ping
    maxRTT = max_ping

    ######## print out summary stats
    print("Min RTT = " + str('%.2f'%minRTT))
    print("Max RTT = " + str('%.2f'%maxRTT))
    print("Avg RTT = " + str('%.2f'%avgRTT))
    print("Packet Lost = " + str('%0.2f%%'%packet_loss))
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
        ping = (end - start) * 1000
        if ping < min_ping: min_ping = ping
        if ping > max_ping: max_ping = ping

        ####### update ping counter & stats variables
        ping_count += 1
        ping_received += 1
        avg_ping += ping
        time_delay = ping - min_ping # keeps track of the jitter 

        ####### remove byte tracker from response
        # bt = len(str(byteTracker))
        # r = response[:-bt]

        a = str(address)[2:]
        sa = a[:-9]
        b = str(response)[2:]
        res = b[:-1]

        ####### print out response
        print("Ping " + str(seq) + ":" + " host " + sa + " replied: " + res + ", RTT = " + str('%.2f'%ping) + " ms")
        # time.sleep(sleep_time) # can be adjusted to see the pings come in more slowly

    ####### if socket timesout, no stats will be calculated and ping is not lossless 
    except socket.timeout as e:
        ####### time out message to inform client
        print('udp_seq=%d REQUEST TIMED OUT' % (seq))

####### display stats
summary()
