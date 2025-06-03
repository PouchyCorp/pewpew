import pygame
import socket

HOST = "127.0.0.1"
PORT = 5555

def wait_connection(host_ip, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host_ip, port))
    server.listen()
    print(f"Le serveur écoute en {host_ip} avec sur le port : {port}")
    client_socket, addr = server.accept()
    print(f"Le client s'est connecté.")
    return client_socket

def main():

    client = wait_connection(HOST, PORT)

    pg.init()

    screen = pg.display.set_mode((1280,720))

    clock = pg.time.Clock()


    max_time_incr = 6

    time_incr = max_time_incr

    bullets = 0

    action = 'idle' #pew, reload, dodge, idle, clic

    game_over_status = 0

    while game_over_status == 0:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                raise SystemExit

        screen.fill("purple")


        if time_incr <= 0:
            if action == "reload":
                bullets += 1
            
            elif action == "pew" and bullet <= 0:
                action = "clic"
            
            elif action == "pew" and bullet > 0:
                bullet -= 1

            client.send(action.encode())

            opponent_action = client.recv(60).decode()

            if opponent_action == "pew" and action in ("idle", "reload"):
                game_over_status = 1
            
            elif action == "pew" and opponent_action in ("idle", "reload"):
                game_over_status = 2

            elif opponent_action == "pew" and action == "pew":
                pass
                # TODO special interaction


            # TODO make while loop to draw results for two sec
            
            

            max_time_incr -= max_time_incr/1.1
            client.send(str(max_time_incr).encode())
            client.send(str(game_over_status).encode())

        pg.display.flip()  
        clock.tick(60)
        time_incr -= 1/60

    if game_over_status == 1:
        print("you lost ...")
    
    else:
        print("you win !!")
        

main()