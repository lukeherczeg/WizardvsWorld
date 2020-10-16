from draw import *
from classes.fsm import FSM
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

    player.currentTile = GRID.game_map[10][4]
    knight.currentTile = GRID.game_map[10][5]
    knight.currentTile.occupied = True
    archer.currentTile = GRID.game_map[0][0]
    archer.currentTile.occupied = True
    archer1.currentTile = GRID.game_map[8][1]
    archer1.currentTile.occupied = True
    archer2.currentTile = GRID.game_map[9][2]
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
    player.attacking = False
    old_knight_health = knight.health
    knight.health = knight.health - 5
    animate_damage(knight, old_knight_health)
    time.sleep(1)

    archer1.attacking = True
    animate_attack(archer1, player)
    archer.attacking = False
    old_player_health = player.health
    player.health = player.health - 20
    animate_damage(player, old_player_health)
    time.sleep(1)

    knight.attacking = True
    animate_attack(knight, player)
    knight.attacking = False
    old_player_health = player.health
    player.health = player.health - 20
    animate_damage(player, old_player_health)

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
