#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 14:44:59 2021

@author: lollo
"""


import socket 
from _thread import * 


server = "188.166.81.86"
port = 8888 




s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:   
    print(e)
   

s.listen(2)
print("waiting for a connection, server started")




idCount = 0
grids = []
moves = []



def threaded_client(conn,gameID):
    """
    
    This function is structured for implementing multiple-threads in order to handle the client connections.
    On the basis of the message received from the client, it sends back given informations

    Arguments

    -----

    conn: socket
        the client-side socket which the informations are transmitted to

    gameID: int
        unique identifier of the game

    """
    global idCount
    global moves
    while True:
        print("moves", moves[gameID])
        try: 
            data = conn.recv(331)
            reply = data.decode("utf-8")
            answer = b"............."  
            if "[[" in reply[:4]:
                if reply[0] == "0":
                    matrix = reply[1:]
                    grids[gameID][0] = matrix
                    answer = bytes(grids[gameID][1], encoding = "utf-8") 
                elif reply[0] == "1":                 
                    matrix = reply[1:]
                    grids[gameID][1] = matrix
                    answer = bytes(grids[gameID][0], encoding = "utf-8")                  
            elif reply[0] == "$":
                if reply[-3] == "#":            
                    turn = int(reply[-2])
                elif reply[-4]  == "#":                                      
                    turn=int(reply[-3 : -1])
                elif reply[-5] == "#":
                    turn=int(reply[-4 : -1])               
                if reply[2] == "0":                   
                    if turn == 1:      
                        moves[gameID][turn-1][0] = reply
                        print(moves)
                    elif len(moves[gameID]) < turn:
                        moves[gameID].append([b"still nothing yet", b"still nothing yet"])
                    if len(moves[gameID]) == turn  and  reply not in moves[gameID][turn -1]:
                        moves[gameID][turn-1][0] = reply                   
                    answer = moves[gameID][turn-1][1]              
                if reply[2] == "1":
                    if turn == 1:     
                        moves[gameID][0][1] = reply
                        print(moves)
                    elif len(moves[gameID]) < turn:
                        moves[gameID].append(["still nothing yet", "still nothing yet"])                
                    if len(moves[gameID]) == turn and reply not in moves[gameID][turn -1]:
                        moves[gameID][turn-1][1] = reply
                    answer=moves[gameID][turn-1][0]
            print(f"received from player {p}:   ", reply)
            print(f"sent to player {p}:   ", answer)
            if type(answer) != bytes:
                answer = bytes( answer, encoding = "utf-8" )
            conn.send(answer)
        except Exception as e:            
            print(e)
            break




while True:
    conn, addr = s.accept()
    idCount += 1
    gameId = (idCount-1)//2
    stgameId = f"#{gameId}#"
    p = 0
    if idCount % 2 == 1:
        grids.append(["still nothing yet", "still nothing yet"])
        moves.append([["still nothing yet", "still nothing yet"]])
        print("Creating a new game...")
        p = bytes(str(p) + stgameId, encoding = "utf-8")    
    elif idCount % 2 == 0:
        p = 1       
        p = bytes(str(p) + stgameId , encoding = "utf-8")   
    print("connected to: ", addr)
    print("gameID", gameId)
    print("IDcount", idCount)
    conn.send(p)
    start_new_thread(threaded_client, (conn, gameId))
    


    

