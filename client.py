import pygame as pg
import socket

IP = "127.0.0.1"
PORT = 5555



def try_connection(server_ip, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, port))
    print(f"Le client s'est connecté.")
    return client

def main():
    client_socket = try_connection(IP, PORT)

    pg.init()

    screen = pg.display.set_mode((1280,720))

    clock = pg.time.Clock()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                raise SystemExit

        screen.fill("purple")

        pg.display.flip()  
        clock.tick(60)


main()



