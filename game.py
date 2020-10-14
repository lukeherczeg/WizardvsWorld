from draw import *
from classes.fsm import FSM
import phases.movement_phase
import test

from classes.entity import Player, Archer, Knight
import time

print(f'Grid Width: {GRID.GRID_WIDTH}; Grid Height: {GRID.GRID_HEIGHT}')


def main():
    fsm = FSM()
    pygame.init()

    ######################### DEMO ########################
    wiz = Player()
    knight = Knight()
    archer = Archer()

    wiz.currentTile = GRID.game_map[1][10]
    knight.currentTile = GRID.game_map[13][5]
    knight.currentTile.occupied = True
    archer.currentTile = GRID.game_map[1][1]
    archer.currentTile.occupied = True

    ENTITIES.append(wiz)
    ENTITIES.append(knight)
    ENTITIES.append(archer)

    total_refresh_drawing()
    time.sleep(1)

    wiz.attacking = True
    animate_attack(wiz, knight)
    time.sleep(1)
    animate_attack(wiz, archer)
    wiz.attacking = False
    print('Done')
    ######################### DEMO ########################

    fsm.add_phase(phases.movement_phase.PlayerMovementPhase(wiz))

    while True:
        for event in pygame.event.get():
            fsm.next_phase()
            fsm.update()
            if event.type == pygame.QUIT:
                quit_game()

        # pygame.draw.rect(SCREEN, WHITE, button)


if __name__ == "__main__":
    main()
