from draw import *
from classes.fsm import FSM
from phases.start_screen import StartScreen
import phases.player_movement_phase
import phases.player_attack_phase
import phases.enemy_attack_phase
import phases.enemy_movement_phase
import test

from classes.entity import Player, Archer, Knight
import time

print(f'Grid Width: {GRID.GRID_WIDTH}; Grid Height: {GRID.GRID_HEIGHT}')


def main():
    pygame.init()

    ######################### DEMO ########################
    player = Player()
    knight = Knight()
    archer = Archer()
    archer1 = Archer()
    archer2 = Archer()

    player.currentTile = GRID.game_map[1][0]
    knight.currentTile = GRID.game_map[13][5]
    knight.currentTile.occupied = True
    archer.currentTile = GRID.game_map[0][0]
    archer.currentTile.occupied = True
    archer1.currentTile = GRID.game_map[0][1]
    archer1.currentTile.occupied = True
    archer2.currentTile = GRID.game_map[1][2]
    archer2.currentTile.occupied = True

    ENTITIES.append(player)
    ENTITIES.append(knight)
    ENTITIES.append(archer)
    ENTITIES.append(archer1)
    ENTITIES.append(archer2)


    total_refresh_drawing()
    time.sleep(1)

    player.attacking = True
    animate_attack(player, knight)
    time.sleep(1)
    animate_attack(player, archer)
    player.attacking = False
    print('Done')
    ######################### DEMO ########################

    fsm = FSM()
    player_movement_phase = phases.player_movement_phase.PlayerMovementPhase(player)
    player_attack_phase = phases.player_attack_phase.PlayerAttackPhase(player, player_movement_phase)
    enemy_attack_phase = phases.enemy_attack_phase.EnemyAICombatPhase()
    enemy_movement_phase = phases.enemy_movement_phase.EnemyAIMovement()
    fsm.add_phase(player_movement_phase)
    fsm.add_phase(player_attack_phase)
    fsm.add_phase(enemy_movement_phase)
    fsm.add_phase(enemy_attack_phase)

    fsm.add_phase(StartScreen()) # TODO: MAKE THIS A SPECIAL PHASE BEFORE THE GAMEPLAY LOOP
    fsm.next_phase()

    while True:
        fsm.update()
        for event in pygame.event.get():
            fsm.next_phase()
            fsm.update()
            if event.type == pygame.QUIT:
                quit_game()

        # pygame.draw.rect(SCREEN, WHITE, button)


if __name__ == "__main__":
    main()
