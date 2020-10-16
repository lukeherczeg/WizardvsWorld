from draw import *
from classes.fsm import FSM
import phases.player_movement_phase
import phases.player_attack_phase
import test

from classes.entity import Player, Archer, Knight
import time

print(f'Grid Width: {GRID.GRID_WIDTH}; Grid Height: {GRID.GRID_HEIGHT}')


def main():
    pygame.init()

    ######################### DEMO ########################
    wiz = Player()
    knight = Knight()
    archer = Archer()
    archer1 = Archer()
    archer2 = Archer()

    wiz.currentTile = GRID.game_map[1][10]
    knight.currentTile = GRID.game_map[13][5]
    knight.currentTile.occupied = True
    archer.currentTile = GRID.game_map[1][1]
    archer.currentTile.occupied = True
    archer1.currentTile = GRID.game_map[2][1]
    archer1.currentTile.occupied = True
    archer2.currentTile = GRID.game_map[1][2]
    archer2.currentTile.occupied = True

    ENTITIES.append(wiz)
    ENTITIES.append(knight)
    ENTITIES.append(archer)
    ENTITIES.append(archer1)
    ENTITIES.append(archer2)


    total_refresh_drawing()
    time.sleep(1)

    wiz.attacking = True
    animate_attack(wiz, knight)
    wiz.attacking = False
    time.sleep(1)

    archer1.attacking = True
    animate_attack(archer1, wiz)
    archer.attacking = False
    time.sleep(1)

    knight.attacking = True
    animate_attack(knight, wiz)
    knight.attacking = False

    print('Done')
    ######################### DEMO ########################

    fsm = FSM()
    player_movement_phase = phases.player_movement_phase.PlayerMovementPhase(wiz)
    player_attack_phase = phases.player_attack_phase.PlayerAttackPhase(wiz, player_movement_phase)
    fsm.add_phase(player_movement_phase)
    fsm.add_phase(player_attack_phase)

    while True:
        for event in pygame.event.get():
            fsm.next_phase()
            fsm.update()
            if event.type == pygame.QUIT:
                quit_game()

        # pygame.draw.rect(SCREEN, WHITE, button)


if __name__ == "__main__":
    main()
