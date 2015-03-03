#!/usr/bin/python

## SINGLE FILE TO KEEP CONNECTION DURING RELOAD ##
import socket
import sys

s = socket.socket( )
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

