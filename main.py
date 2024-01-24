import pygame, time
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.gravity = 0
        player_walk1 = pygame.image.load('graphics/player/vireo_walk_1.png').convert_alpha()
        player_walk2 = pygame.image.load('graphics/player/vireo_walk_2.png').convert_alpha()
        self.jump = 2
        self.player_walk = [player_walk1, player_walk2]
        self.player_index = 0
        self.jump_sound = pygame.mixer.Sound("audio/vireo_jump.wav")
        self.jump_sound.set_volume(0.3)
        self.player_jump = pygame.image.load('graphics/player/vireo_jump.png').convert_alpha()
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (70,300))

    def player_input(self):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if self.jump == 2:
                    self.gravity = -17
                    self.jump -= 1
                    self.jump_sound.play()
                elif self.jump == 1:
                    self.gravity = -15
                    self.jump -= 1


    def gravity_appl(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.jump = 2
            self.rect.bottom = 300

    def animation(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.gravity_appl()
        self.animation()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == "frog":
            frog_frame1 = pygame.image.load('graphics/animals/frog1.png').convert_alpha()
            frog_frame2 = pygame.image.load('graphics/animals/frog2.png').convert_alpha()
            self.frames = [frog_frame1, frog_frame2]
            ypos = 300
        
        elif type == "wasp":
            wasp_frame1 = pygame.image.load('graphics/wasp/wasp1.png').convert_alpha()
            wasp_frame1 = pygame.transform.scale_by(wasp_frame1, 0.7)
            wasp_frame2 = pygame.image.load('graphics/wasp/wasp2.png').convert_alpha()
            wasp_frame2 = pygame.transform.scale_by(wasp_frame2, 0.7)
            self.frames = [wasp_frame1, wasp_frame2]
            ypos = randint(150, 220)
        
        self.obstacle_index = 0
        self.image = self.frames[self.obstacle_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100), ypos))

    def animation(self):
        if type == "frog":
            self.obstacle_index += 0.1
        else:
            self.obstacle_index += 0.05
        if self.obstacle_index >= len(self.frames): self.obstacle_index = 0
        self.image = self.frames[int(self.obstacle_index)]
        
    def update(self):
        self.animation()
        self.rect.x -= 7
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def display_score():
    current_time = int(pygame.time.get_ticks()/1000) - start_time
    score_surface = font.render(f'Vireo walked {current_time} metres', False, (64, 64, 64))
    score_rect = score_surface.get_rect(center = (400, 40))
    screen.blit(score_surface, score_rect)
    return current_time

def collision():
    game_over_sound = pygame.mixer.Sound("audio/game_over.wav")
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, 0):
            pygame.mixer.Sound.play(game_over_sound)
            pygame.mixer.music.stop()
            obstacle_group.empty()
            player.empty()
            player.add(Player())
            return False  
    return True  
    
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Vireo walking simulator')
clock = pygame.time.Clock()
font = pygame.font.Font('font/DisposableDroidBB.ttf', 40)
game_active = 0
start_time = 0
score = 0

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()

# Background
sky_surface = pygame.image.load('graphics/sky.png').convert_alpha()
ground_surface = pygame.image.load('graphics/ground.png').convert_alpha()

# Intro/Menu screen
player_stand = pygame.transform.scale2x(pygame.image.load('graphics/player/vireo_stand.png').convert_alpha())
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = font.render('Vireo Walking Simulator', 0, 'black')
game_name_rect = game_name.get_rect(center = (400, 70))

menu_message = font.render('Press Enter to start WaLkInG', False, 'black')
menu_message_rect = menu_message.get_rect(center = (400, 330))

unfortunate_message = font.render(f"Unfortunate! Vireo's journey has ended.", False, 'black')
unfortunate_message_rect = unfortunate_message.get_rect(center = (400, 70))

# End-game
success_message1 = font.render(f'Congratulations!', False, 'Green')
success_message_rect1 = success_message1.get_rect(center = (400, 70))
success_message2 = font.render(f'You have successfully guided Vireo', False, 'Green')
success_message_rect2 = success_message2.get_rect(center = (400, 120))
success_message3 = font.render(f'to the safety.', False, 'Green')
success_message_rect3 = success_message3.get_rect(center = (400, 170))

# Timer for "enemies"
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1000)
while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:        
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['frog', 'wasp', 'frog', 'wasp', 'frog'])))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_active = True
                start_time = int(pygame.time.get_ticks()/1000)      



    if game_active:
        # Screen
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,300))
        score = display_score()
        
        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()
        
        # collision detection
        game_active = collision()
        if score >= 50:
            game_active = False

    else:
        obstacle_group.empty()
        player.empty()
        player.add(Player())
        if score == 0:
            screen.fill('#20B2AA')
            pygame.draw.rect(screen, '#FFA07A', menu_message_rect.inflate(10,10))
            screen.blit(menu_message, menu_message_rect)
            screen.blit(player_stand, player_stand_rect)
            pygame.draw.rect(screen, '#FFA07A', game_name_rect.inflate(10,10))
            screen.blit(game_name, game_name_rect)
        elif score >= 50:
            screen.blit(sky_surface, (0,0))
            screen.blit(ground_surface, (0,300))
            pygame.draw.rect(screen, 'Black', success_message_rect1.inflate(15,15))
            screen.blit(success_message1, success_message_rect1)
            pygame.draw.rect(screen, 'Black', success_message_rect2.inflate(15,15))
            screen.blit(success_message2, success_message_rect2)
            pygame.draw.rect(screen, 'Black', success_message_rect3.inflate(15,15))
            screen.blit(success_message3, success_message_rect3)                        

        else:
            screen.fill('#CD5C5C')
            score_message = font.render(f'Vireo walked {score} metres', False, 'black')
            score_message_rect = score_message.get_rect(center = (400,330))
            pygame.draw.rect(screen, '#0ABAB5', score_message_rect.inflate(10,10))
            screen.blit(score_message, score_message_rect)
            screen.blit(pygame.transform.flip(player_stand, 0, 1), player_stand_rect)
            pygame.draw.rect(screen, '#0ABAB5', unfortunate_message_rect.inflate(10,10))
            screen.blit(unfortunate_message, unfortunate_message_rect)
    pygame.display.update()
    clock.tick(60)