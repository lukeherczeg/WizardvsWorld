from draw import *
from classes.fsm import FSM
import phases.player_movement_phase
import phases.player_attack_phase
import phases.enemy_attack_phase
import phases.enemy_movement_phase
from classes.user_interface import MessageBox
import test

from classes.entity import Player, Archer, Knight
import time

print(f'Grid Width: {GRID.GRID_WIDTH}; Grid Height: {GRID.GRID_HEIGHT}')


def main():
    pygame.init()
    pygame.display.set_caption('Wizard vs. World PRE-ALPHA')

    ######################### DEMO ########################
    player = Player()
    knight = Knight()
    archer = Archer()
    archer1 = Archer()
    archer2 = Archer()

    message_box = MessageBox('Big long message to give to you. It\'s a very long message that should take up multiple lines lol it is such a long message')

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

    message_box.draw_message_box()
    MessageBox.confirm()

    player.attacking = True
    animate_attack(player, knight)
    time.sleep(1)
    animate_attack(player, archer)
    player.attacking = False
    print('Done')
    ######################### DEMO ########################

    fsm = FSM()

    # Declare Phases
    player_movement_phase = phases.player_movement_phase.PlayerMovementPhase(player)
    player_attack_phase = phases.player_attack_phase.PlayerAttackPhase(player, player_movement_phase)
    enemy_attack_phase = phases.enemy_attack_phase.EnemyAICombatPhase()
    enemy_movement_phase = phases.enemy_movement_phase.EnemyAIMovement()

    # Add Phases
    fsm.add_phase(player_movement_phase)
    fsm.add_phase(player_attack_phase)
    fsm.add_phase(enemy_movement_phase)
    fsm.add_phase(enemy_attack_phase)

    # Start the FSM
    fsm.restart()

    # Gameplay Loop
    while True:
        for event in pygame.event.get():
            fsm.update()
            if event.type == pygame.QUIT:
                quit_game()


if __name__ == "__main__":
    main()
