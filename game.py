from draw import *
from classes.fsm import FSM
import phases.player_movement_phase
import phases.player_attack_phase
import phases.enemy_attack_phase
import phases.enemy_movement_phase

from classes.entity import Player

print(f'Grid Width: {GRID.GRID_WIDTH}; Grid Height: {GRID.GRID_HEIGHT}')


def main():
    pygame.init()

    pygame.display.set_caption('Wizard vs. World ALPHA Build v 0.1')
    pygame.display.set_icon(WIZ_LARGE_PNG)

    player = Player()
    player.currentTile = GRID.game_map[7][20]
    ENTITIES.append(player)
    GRID.generate_enemies(0)

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
        fsm.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()


if __name__ == "__main__":
    main()
