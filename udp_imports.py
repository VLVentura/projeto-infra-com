#!/usr/bin/env python3
from socket import socket, AF_INET, SOCK_DGRAM
from checksum import checksum
from client import get_package
from packet import Packet

SERVER_PORT = 12000
SERVER_NAME = "localhost"
CONN = socket(AF_INET, SOCK_DGRAM)
