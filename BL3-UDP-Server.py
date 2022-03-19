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
#   Filename: BL3-UDP-Server.py
#   Language: Python 3.9.1
#   Run Command: python3 BL3-UDP-Server.py (MAC)
#   Run Command: python BL3-UDP-Server.py (WINDOWS)
#   Purpose: UDP sender: Send the host name and system time as a message to a 
#            destination host designated by its IP address and port number. Repeat the 
#            transmission when enabled to do so.Read and display the returned messages, 
#            and indicate the IP address and port number of the sender. Also, will keep 
#            track of the RTT values of each ping and give a stats summary at the end, 
#            also indicating if there’s packet loss.
#
##### CODE BEGINS: #####################################################################

from socket import *
import random
import time
# Create a UDP socket
serverSocket = socket(AF_INET, SOCK_DGRAM)
# Assign IP address and port number to socket 
serverSocket.bind(('', 12002))
while True:
    # Receive the client packet along with the address it is coming from 
    message, address = serverSocket.recvfrom(1024)

    if message != "":
        ####### simulate random rtt delay
        delay = random.randint(10, 40)
        ####### 20% of (40-10) = 6
        if delay >= 34:
            ms = 1
        else:
            ms = delay / 1000
        time.sleep(ms)

    # The server responds
    serverSocket.sendto(message, address)


