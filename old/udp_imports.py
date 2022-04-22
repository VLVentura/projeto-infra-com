#!/usr/bin/env python3
from socket import socket, AF_INET, SOCK_DGRAM
from checksum import checksum
from client import get_package
from server import parse_package
from packet import Packet
from rdt21_client import *
from rdt21_sever import *

SERVER_PORT = 12000
CLIENT_PORT = 5600
SERVER_HOST = "localhost"
CONN = socket(AF_INET, SOCK_DGRAM)
