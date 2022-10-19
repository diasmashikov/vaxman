# Pacman in Python with PyGame
# https://github.com/hbokmann/Pacman

import pygame
from pygame.constants import USEREVENT
from level_configuration import LevelConfiguration
from models.ghost import Ghost
from constants import colors, dimensions, directions
import random


class VaxmanGame():

    screen = None
    font = None

    pl = len(directions.pinky)-1
    bl = len(directions.blinky)-1
    il = len(directions.inky)-1
    cl = len(directions.clyde)-1

    directions_length = [pl, bl, il, cl]
    ghosts_directions = [directions.blinky,
                         directions.pinky, directions.inky, directions.clyde]
    ghosts_turn_steps_list = [[0, 0], [0, 0], [0, 0], [0, 0]]

    clock = pygame.time.Clock()

    def __init__(self):
        pass

    def screenSetup(self):
        Trollicon = pygame.image.load('images/Trollman.png')
        pygame.display.set_icon(Trollicon)

        # Call this function so the Pygame library can initialize itself
        pygame.init()
        pygame.font.init()

        # Create an 606x606 sized screen
        self.screen = pygame.display.set_mode([606, 606])

        # This is a list of 'sprites.' Each block in the program is
        # added to this list. The list is managed by a class called 'RenderPlain.'

        # Set the title of the window
        pygame.display.set_caption('Vax-man')

        # Create a surface we can draw on
        background = pygame.Surface(self.screen.get_size())

        # Used for converting color maps and such
        background = background.convert()

        # Fill the screen with a black background
        background.fill(colors.BLACK)
        self.font = pygame.font.Font("freesansbold.ttf", 24)

    def startGame(self):

        all_sprites_list = pygame.sprite.RenderPlain()

        block_list = pygame.sprite.RenderPlain()

        monsta_list = pygame.sprite.RenderPlain()

        vaxman_collide = pygame.sprite.RenderPlain()

        wall_list = pygame.sprite.RenderPlain()

        levelConfiguration = LevelConfiguration(
            all_sprites_list, block_list, vaxman_collide, monsta_list, wall_list)

        wall_list = levelConfiguration.setupRoomOne()

        gate = levelConfiguration.setupGate()

        Vaxman = levelConfiguration.createVaxman()

        levelConfiguration.createEnemies()

        levelConfiguration.drawLevel()

        bll = len(block_list)

        score = 0

        done = False

        pygame.time.set_timer(USEREVENT+1, 30000)

        while done == False:
            # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

                if event.type == USEREVENT+1:

                    # Doubling ghosts
                    if len(monsta_list) == 0:
                        levelConfiguration.createEnemies()

                    for monsta in monsta_list:
                        Blinky = Ghost(
                            dimensions.width, dimensions.blinky_height, monsta.filename)
                        monsta_list.add(Blinky)
                        self.ghosts_turn_steps_list.append(
                            [random.randint(-200, 200), random.randint(-200, 200)])
                        all_sprites_list.add(Blinky)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        Vaxman.changespeed(-10, 0)
                    if event.key == pygame.K_RIGHT:
                        Vaxman.changespeed(10, 0)
                    if event.key == pygame.K_UP:
                        Vaxman.changespeed(0, -10)
                    if event.key == pygame.K_DOWN:
                        Vaxman.changespeed(0, 10)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        Vaxman.changespeed(10, 0)
                    if event.key == pygame.K_RIGHT:
                        Vaxman.changespeed(-10, 0)
                    if event.key == pygame.K_UP:
                        Vaxman.changespeed(0, 10)
                    if event.key == pygame.K_DOWN:
                        Vaxman.changespeed(0, -10)

            # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT

            # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT
            Vaxman.update(wall_list, gate)

            # Adding stats to new ghosts
            for index, monsta in enumerate(monsta_list):
                direction = self.ghosts_directions[index % 4]
                returned = monsta.changespeed(
                    direction, False, self.ghosts_turn_steps_list[index][0], self.ghosts_turn_steps_list[index][1], random.randint(0, 100))
                self.ghosts_turn_steps_list[index][0] = returned[0]
                self.ghosts_turn_steps_list[index][1] = returned[1]
                monsta.changespeed(
                    direction, False, self.ghosts_turn_steps_list[index][0], self.ghosts_turn_steps_list[index][1], random.randint(0, 100))
                monsta.update(wall_list, False)

            # See if the Pacman block has collided with anything.
            blocks_hit_list = pygame.sprite.spritecollide(
                Vaxman, block_list, True)

            # Check the list of collisions.
            if len(blocks_hit_list) > 0:
                score += len(blocks_hit_list)

            # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT

            # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
            self.screen.fill(colors.BLACK)

            wall_list.draw(self.screen)
            gate.draw(self.screen)
            all_sprites_list.draw(self.screen)
            monsta_list.draw(self.screen)

            text = self.font.render(
                "Score: "+str(score)+"/"+str(bll), True, colors.RED)
            self.screen.blit(text, [10, 10])

            # Indicate how many infected there are
            text = self.font.render(
                "Infected: "+str(len(monsta_list))+"/"+str(128), True, colors.RED)
            self.screen.blit(text, [10, 50])

            if score == bll:
                self.doNext("Congratulations, you won!", 145, all_sprites_list,
                            block_list, monsta_list, vaxman_collide, wall_list, gate)

            if len(monsta_list) >= 128:
                self.doNext("Game Over", 235, all_sprites_list, block_list,
                            monsta_list, vaxman_collide, wall_list, gate)

            pygame.sprite.spritecollide(
                Vaxman, monsta_list, True)

            # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

            pygame.display.flip()

            self.clock.tick(10)

    def doNext(self, message, left, all_sprites_list, block_list, monsta_list, pacman_collide, wall_list, gate):

        while True:
            # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                    if event.key == pygame.K_RETURN:
                        del all_sprites_list
                        del block_list
                        del monsta_list
                        del pacman_collide
                        del wall_list
                        del gate
                        self.startGame()

            # Grey background
            w = pygame.Surface((400, 200))  # the size of your rect
            w.set_alpha(10)                # alpha level
            w.fill((128, 128, 128))           # this fills the entire surface
            # (0,0) are the top-left coordinates
            self.screen.blit(w, (100, 200))

            #Won or lost
            text1 = self.font.render(message, True, colors.WHITE)
            self.screen.blit(text1, [left, 233])
            text2 = self.font.render(
                "To play again, press ENTER.", True, colors.WHITE)
            self.screen.blit(text2, [135, 303])
            text3 = self.font.render(
                "To quit, press ESCAPE.", True, colors.WHITE)
            self.screen.blit(text3, [165, 333])

            pygame.display.flip()

            self.clock.tick(60)


# G ame start
game = VaxmanGame()
game.screenSetup()
game.startGame()

pygame.quit()
