import socket
import pygame
from threading import Thread
from zlib import compress
from mss import mss
WIDTH = 1900
HEIGHT = 1000
def capture_and_send(conn):
    with mss() as sct:
        rect = {'top': 0, 'left': 0, 'width': WIDTH, 'height': HEIGHT}
        while True:
            img = sct.grab(rect)
            pixels = compress(img.rgb, 6)
            size = len(pixels)
            size_len = (size.bit_length() + 7) // 8
            conn.send(bytes([size_len]))
            size_bytes = size.to_bytes(size_len, 'big')
            conn.send(size_bytes)
            conn.sendall(pixels)

def main(host='127.0.0.1', port=52000):
    sock = socket.socket()
    while True:
        try:
            sock.connect((host, port))
            break
        except Exception:
            pass
    try:
        while True:
            thread = Thread(target=capture_and_send, args=(sock,))
            thread.start()
            thread.join()
    except Exception as e:
        print("ERR: ", e)
        sock.close()
if __name__ == '__main__':
    main()
