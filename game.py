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
    enemy = Knight()

    wiz.currentTile = GRID.game_map[1][10]
    enemy.currentTile = GRID.game_map[13][5]

    ENTITIES.append(wiz)
    ENTITIES.append(enemy)

    total_refresh_drawing()
    time.sleep(1)

    old_pos = wiz.get_position().col, wiz.get_position().row
    wiz.currentTile = GRID.game_map[3][9]
    animate_move(wiz, old_pos)
    time.sleep(2)

    animate_attack(wiz, enemy)
    print('Done')
    ######################### DEMO ########################

    fsm.add_phase(phases.movement_phase.PlayerMovementPhase(wiz))
    fsm.next_phase()
    fsm.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        # pygame.draw.rect(SCREEN, WHITE, button)


if __name__ == "__main__":
    main()
