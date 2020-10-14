from draw import *
from classes.fsm import FSM
from classes.entity import Player, Enemy
from phases.start_screen import StartScreen
import phases.movement_phase

import time

print(f'Grid Width: {GRID.GRID_WIDTH}; Grid Height: {GRID.GRID_HEIGHT}')


def main():
    player = Player()
    fsm = FSM()

    pygame.init()

    ######################### DEMO ########################
    # wiz = Player()
    #
    # wiz.currentTile = GRID.game_map[1][10]
    #
    # ENTITIES.append(wiz)
    #
    # total_refresh_drawing()
    # time.sleep(1)
    #
    # old_pos = wiz.get_position().col, wiz.get_position().row
    # show_movable_tiles(GRID.get_movement(wiz.currentTile.col,wiz.currentTile.row, 3), wiz)
    #
    # time.sleep(3)
    #
    # wiz.currentTile = GRID.game_map[3][9]
    # move_player(wiz, old_pos)
    ######################### DEMO ########################

    # fsm.add_phase(phases.movement_phase.PlayerMovementPhase(player))
    # fsm.next_phase()
    # fsm.update()

    fsm.add_phase(StartScreen()) # TODO: MAKE THIS A SPECIAL PHASE BEFORE THE GAMEPLAY LOOP
    fsm.next_phase()

    while True:
        fsm.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        # pygame.draw.rect(SCREEN, WHITE, button)

if __name__ == "__main__":
    main()
