import pygame
from models.wall import Wall
from models.block import Block
from models.player import Player
from models.ghost import Ghost
from constants import colors, dimensions

# This creates all the walls in room 1

# The class is responsible for creating maps, enemies, Vax-Man


class LevelConfiguration():

    def __init__(self, all_sprites_list, block_list, vaxman_collide, monsta_list, wall_list):
        self.all_sprites_list = all_sprites_list
        self.block_list = block_list
        self.vaxman_collide = vaxman_collide
        self.monsta_list = monsta_list
        self.wall_list = wall_list

    def setupRoomOne(self):
        # Make the walls. (x_pos, y_pos, width, height)

        # This is a list of walls. Each is in the form [x, y, width, height]

        # Loop through the list. Create the wall, add it to the list
        for item in dimensions.walls:
            wall = Wall(item[0], item[1], item[2], item[3], colors.BLUE)
            self.wall_list.add(wall)
            self.all_sprites_list.add(wall)

    # return our new list
        return self.wall_list

    def setupGate(self):
        gate = pygame.sprite.RenderPlain()
        gate.add(Wall(282, 242, 42, 2, colors.WHITE))
        self.all_sprites_list.add(gate)
        return gate

    def drawLevel(self):
        # Draw the grid
        for row in range(19):
            for column in range(19):
                if (row == 7 or row == 8) and (column == 8 or column == 9 or column == 10):
                    continue
                else:
                    block = Block(colors.YELLOW, 4, 4)

                    # Set a random location for the block
                    block.rect.x = (30*column+6)+26
                    block.rect.y = (30*row+6)+26

                    b_collide = pygame.sprite.spritecollide(
                        block, self.wall_list, False)
                    p_collide = pygame.sprite.spritecollide(
                        block, self.vaxman_collide, False)
                    if b_collide:
                        continue
                    elif p_collide:
                        continue
                    else:
                        # Add the block to the list of objects
                        self.block_list.add(block)
                        self.all_sprites_list.add(block)

    def createEnemies(self):
        # Create the player paddle object
        Blinky = Ghost(dimensions.width, dimensions.blinky_height,
                       "images/Blinky.png")
        self.monsta_list.add(Blinky)
        self.all_sprites_list.add(Blinky)

        Pinky = Ghost(dimensions.width, dimensions.monster_height,
                      "images/Pinky.png")
        self.monsta_list.add(Pinky)
        self.all_sprites_list.add(Pinky)

        Inky = Ghost(dimensions.inky_width,
                     dimensions.monster_height, "images/Inky.png")
        self.monsta_list.add(Inky)
        self.all_sprites_list.add(Inky)

        Clyde = Ghost(dimensions.clyde_width,
                      dimensions.monster_height, "images/Clyde.png")
        self.monsta_list.add(Clyde)
        self.all_sprites_list.add(Clyde)

    def createVaxman(self):
        Vaxman = Player(dimensions.width, dimensions.vaxman_height,
                        "images/Vaxman.png")
        self.all_sprites_list.add(Vaxman)
        self.vaxman_collide.add(Vaxman)
        return Vaxman
