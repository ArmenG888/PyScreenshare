import socket
import pygame
from zlib import decompress
ip_port = ("127.0.0.1", 52000)
def recvall(conn, length):
    buf = b''
    while len(buf) < length:
        data = conn.recv(length - len(buf))
        if not data:
            return data
        buf += data
    return buf
def main(ip_port):
    sock = socket.socket()
    sock.bind(ip_port)
    print("Listening ....")
    sock.listen(5)
    conn, addr = sock.accept()
    print("Accepted ....", addr)
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    watching = True
    try:
        while watching:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    watching = False
                    break
            size_len = int.from_bytes(conn.recv(1), byteorder='big')
            size = int.from_bytes(conn.recv(size_len), byteorder='big')
            pixels = decompress(recvall(conn, size))
            img = pygame.image.fromstring(pixels, (WIDTH, HEIGHT), 'RGB')
            screen.blit(img, (0, 0))
            pygame.display.flip()
            clock.tick(60)
    finally:
        print("PIXELS: ", pixels)
        sock.close()

if __name__ == "__main__":
    main(ip_port)
