from classes.tile import Tile
from classes.entity import Enemy, Entity
from draw import *
from classes.phase import Phase
import random
import math


class EnemyAIMovement(Phase):
    player_position: Tile
    Enemies: [Entity]
    grid: Grid

    def __init__(self):
        self.Enemies = ENTITIES[1:]
        self.Player = ENTITIES[0]
        self.player_position = self.Player.get_position()
        self.grid = GRID

    def gets_closer(self, enemy, new_position):
        if new_position.standable and not new_position.occupied and new_position is not self.player_position:
            p1 = [self.player_position.row, self.player_position.col]
            p2 = [enemy.currentTile.row, enemy.currentTile.col]
            p3 = [new_position.row, new_position.col]
            distance1 = int(math.sqrt(((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2)))
            distance2 = int(math.sqrt(((p1[0] - p3[0]) ** 2) + ((p1[1] - p3[1]) ** 2)))
            if distance1 > distance2:
                return False
        else:
            return True

    def move_enemy(self, enemy):
        if enemy.health > 0:
            movable_tiles = GRID.get_movement(enemy.currentTile.row, enemy.currentTile.col, enemy.max_Movement)
            for tile in movable_tiles:
                if tile.occupied or tile is self.player_position:
                    movable_tiles.remove(tile)

            init_post = enemy.currentTile.col, enemy.currentTile.row
            new_tile = random.randint(0, len(movable_tiles) - 1)
            cannot_move = True

            if len(movable_tiles) == 1:
                return
            while cannot_move:
                cannot_move = self.gets_closer(enemy, movable_tiles[new_tile])
                if cannot_move:
                    new_tile = random.randint(0, len(movable_tiles) - 1)

            enemy.currentTile.occupied = False
            enemy.currentTile = movable_tiles[new_tile]
            enemy.currentTile.occupied = True
            time.sleep(0.5)
            animate_move(enemy, init_post)

    def enter(self):
        print('Entering Enemy Movement Selection...')
        self.player_position = ENTITIES[0].currentTile

    def update(self):
        print('Entering Enemy Movement Computation / Animation...')
        for enemy in self.Enemies:
            if isinstance(enemy, Enemy):
                self.move_enemy(enemy)

    def exit(self):
        print('Exiting Player Phase...')



