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
    archer1 = Archer()
    archer2 = Archer()

    player.currentTile = GRID.game_map[8][15]
    knight.currentTile = GRID.game_map[8][16]
    knight.currentTile.occupied = True
    archer1.currentTile = GRID.game_map[5][15]
    archer1.currentTile.occupied = True
    archer2.currentTile = GRID.game_map[13][15]
    archer2.currentTile.occupied = True

    ENTITIES.append(player)
    ENTITIES.append(knight)
    ENTITIES.append(archer1)
    ENTITIES.append(archer2)


    total_refresh_drawing()
    time.sleep(1)

    archer1.attacking = True
    animate_attack(archer1, player)
    archer1.attacking = False
    old_player_health = player.health
    player.health = player.health - 20
    player.damaged = True
    animate_damage(player, old_player_health)
    player.damaged = False

    archer2.attacking = True
    animate_attack(archer2, player)
    archer2.attacking = False
    old_player_health = player.health
    player.health = player.health - 20
    player.damaged = True
    animate_damage(player, old_player_health)
    player.damaged = False

    knight.attacking = True
    animate_attack(knight, player)
    knight.attacking = False
    old_player_health = player.health
    player.health = player.health - 50
    player.damaged = True
    animate_damage(player, old_player_health)
    player.damaged = False

    player.attacking = True
    animate_attack(player, knight)
    player.attacking = False
    old_knight_health = knight.health
    knight.health = knight.health - 50
    knight.damaged = True
    animate_damage(knight, old_knight_health)
    ENTITIES.remove(knight)
    animate_death(knight)

    player.attacking = True
    animate_attack(player, archer1)
    player.attacking = False
    old_archer1_health = archer1.health
    archer1.health = archer1.health - 30
    archer1.damaged = True
    animate_damage(archer1, old_archer1_health)
    ENTITIES.remove(archer1)
    animate_death(archer1)

    player.attacking = True
    animate_attack(player, archer2)
    player.attacking = False
    old_archer2_health = archer2.health
    archer2.health = archer2.health - 30
    archer2.damaged = True
    animate_damage(archer2, old_archer2_health)
    ENTITIES.remove(archer2)
    animate_death(archer2)

    draw_text("BIG DICK WIZ", 24, offset=(200,200))
    time.sleep(2)
    draw_text("COMING TO YO CASTLE", 24, offset=(220,300), color=RED)
    time.sleep(2)
    draw_text("STEALING YO GRILL", 24, offset=(240,400), color=WHITE)
    time.sleep(2)

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
