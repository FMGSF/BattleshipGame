#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 12:23:32 2021

@author: lollo
"""


import socket



class Network(object):
    """
    This Object is defined for handling the communication between the Clients and the Server:

    Attributes:
    ----
    self.client: socket 
        we use the address family name AF_INET (IPv4 addresses), in combination with the TCP protocol for creating our socket
    
    self.server: string
        Static IP addres of the Digital Ocean server we're relying on. It must be the same as on  the server.py script
    
    self.port: int 
        port we are using for the connection. It must be the same as on the server.py script

    self.addr: tuple
        tuple containing the pair (IP_address, port). This tuple is the same as the one which the server socket is bound to.
        
    """
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "188.166.81.86" 
        self.port = 8888
        self.addr = (self.server, self.port)
    def connect(self):
        """
        This method is called for requesting a connection to the server
        """
        return self.client.connect(self.addr)
    def recv(self):
        """"
        This method is called for Reading from the server
        """
        return self.client.recv(331).decode()
    def send(self, data):
        """"
        This method is called for Writing to the server
        """
        return self.client.send(bytes(data, encoding="utf-8"))
    def close(self):
        """
        This method is called for ending the connection
        """     
        return self.client.close()
    

        
 
