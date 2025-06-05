import pygame as pg
import socket

IP = "zola-info-02"
PORT = 5555

class Button:
    def __init__(self, coord : tuple, effect, surf_active = None, surf_inactive = None, param : list = None):
        assert surf_active or surf_inactive, "initalize at least one of the two surface attributes"
        self.surf_active = surf_active
        self.surf_inactive = surf_inactive
        self.surf : pg.Surface = surf_inactive if surf_inactive else surf_active
        self.rect : pg.Rect = self.surf.get_rect(topleft=coord)
        self.selected = False
        self.param = param if param else []

    def handle_event(self, event):
        """Manage the events"""
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Activates the button's effect when pressed
                return True
        return False

    def draw(self, win : pg.Surface):
        # Changes the sprite if the button is hovered
        if self.selected:
            self.surf = self.surf_active
        else:
            self.surf = self.surf_inactive
            
        # Blit the text.
        win.blit(self.surf, self.rect)

def draw_round_event(action, opponent_action, screen : pg.Surface, images):
    screen.blit(images["background"], (0,0))

    # Show player's action
    if action == "pew":
        screen.blit(images["tir1"], (0,0))
    elif action == "reload":
        screen.blit(images["recharg1"], (0,0))
    elif action == "dodge":
        screen.blit(images["dodge1"], (0,0))
    else:
        screen.blit(images["idle1"], (0,0))

    # Show opponent's action
    if opponent_action == "pew":
        screen.blit(images["tir2"], (0,0))
    elif opponent_action == "reload":
        screen.blit(images["recharg2"], (0,0))
    elif opponent_action == "dodge":
        screen.blit(images["dodge2"], (0,0))
    else:
        screen.blit(images["idle2"], (0,0))

    pg.display.flip()
    pg.time.wait(2000)

def try_connection(server_ip, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, port))
    print(f"Le client s'est connecté.")
    return client

def main():
    server = try_connection(IP, PORT)

    pg.init()

    screen = pg.display.set_mode((0,0), pg.FULLSCREEN)
    font = pg.font.SysFont('Arial', 20)
    clock = pg.time.Clock()

    # Load images into a dictionary
    images = {
        "tir1": pg.image.load("tir 1.png").convert_alpha(),
        "tir2": pg.image.load("tir 2.png").convert_alpha(),
        "recharg1": pg.image.load("recharg 1.png").convert_alpha(),
        "recharg2": pg.image.load("recharg 2.png").convert_alpha(),
        "idle1": pg.image.load("idle 1.png").convert_alpha(),
        "idle2": pg.image.load("idle 2.png").convert_alpha(),
        "dodge1": pg.image.load("dodge 1.png").convert_alpha(),
        "dodge2": pg.image.load("dodge 2.png").convert_alpha(),
        "background": pg.image.load("background.png").convert_alpha(),
        "button_shoot": pg.image.load("bouton1.png").convert_alpha(),
        "button_shoot_hover": pg.image.load("bouton1_hover.png").convert_alpha(),
        "button_block": pg.image.load("bouton2.png").convert_alpha(),
        "button_block_hover": pg.image.load("bouton2_hover.png").convert_alpha(),
        "button_reload": pg.image.load("bouton3.png").convert_alpha(),
        "button_reload_hover": pg.image.load("bouton3_hover.png").convert_alpha(),
    }

    button_shoot = Button((250, 880), int, images["button_shoot_hover"], images["button_shoot"])
    button_block= Button((990, 880), int, images["button_block_hover"], images["button_block"])
    button_reload = Button((615, 880), int, images["button_reload_hover"], images["button_reload"])
    

    bullets = 0  
    action = 'idle'  # Possible actions: pew, reload, dodge, idle
    game_over_status = 0

    max_time_incr = 6
    time_incr = max_time_incr

    choice_made = False

    while game_over_status == 0:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                raise SystemExit
            if not choice_made:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:  # Space to "pew"
                        if bullets > 0:
                            action = "pew"
                            bullets -= 1
                        else:
                            action = "clic"  # No bullets to shoot
                        choice_made = True
                    elif event.key == pg.K_r:  # R to reload
                        action = "reload"
                        bullets += 1
                        choice_made = True
                    elif event.key == pg.K_d:  # D to dodge
                        action = "dodge"
                        choice_made = True
                    else:
                        action = "idle"
                
                if button_block.handle_event(event):
                    action = 'dodge'
                    choice_made = True
                if button_reload.handle_event(event):
                    action = 'reload'
                    bullets += 1
                    
                    choice_made = True
                if button_shoot.handle_event(event):
                    if bullets > 0:
                        action = "pew"
                        bullets -= 1
                        
                    else:
                        action = "clic"
                    choice_made = True

            match action:
                case "pew" | "clic":
                    button_shoot.selected = True
                    button_reload.selected = False
                    button_block.selected = False
                case "reload":
                    button_shoot.selected = False
                    button_reload.selected = True
                    button_block.selected = False
                case "dodge":
                    button_shoot.selected = False
                    button_reload.selected = False
                    button_block.selected = True
                case _:
                    button_shoot.selected = False
                    button_reload.selected = False
                    button_block.selected = False

        screen.blit(images["background"], (0,0))
        screen.blit(images["idle1"], (0,0))
        screen.blit(images["idle2"], (0,0))
        button_shoot.draw(screen)
        button_block.draw(screen)
        button_reload.draw(screen)


        if time_incr <= 0:
            opponent_action = server.recv(60).decode()

            server.send(b' ')
            print(f"Opponent action: {opponent_action}")

            server.send(action.encode())
            server.recv(1) # confirmation

            draw_round_event(action, opponent_action, screen, images) 

            max_time_incr = float(server.recv(60).decode())
            server.send(b' ')
            time_incr = max_time_incr
            game_over_status = int(server.recv(60).decode())
            server.send(b' ')

            action = "idle"
            choice_made = False
        
        screen.blit(font.render(f"max {max_time_incr}, incr {button_shoot.selected}, action {action}, fps {int(clock.get_fps())}", False, "white"), (0,0))

        pg.display.flip()  
        time_incr -= 1/60
        clock.tick(60)

    if game_over_status == 2:
        print("you lost ...")
    
    else:
        print("you win !!")

main()