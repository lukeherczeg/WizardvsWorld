import sys
import os.path

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from WizardVsWorld.classes.draw import *
from WizardVsWorld.classes.fsm import FSM
import WizardVsWorld.phases.player_movement_phase
import WizardVsWorld.phases.player_attack_phase
import WizardVsWorld.phases.enemy_attack_phase
import WizardVsWorld.phases.enemy_movement_phase

from WizardVsWorld.classes.entity import Player


def main():
    pygame.init()

    pygame.display.set_caption('Wizard vs. World v1.0.3')
    pygame.display.set_icon(WIZ_LARGE_PNG)

    player = Player()
    player.currentTile = GRID.game_map[7][0]
    ENTITIES.append(player)
    GRID.generate_enemies(0)

    fsm = FSM()

    # Declare Phases
    player_movement_phase = WizardVsWorld.phases.player_movement_phase.PlayerMovementPhase(player)
    player_attack_phase = WizardVsWorld.phases.player_attack_phase.PlayerAttackPhase(player, player_movement_phase)
    enemy_attack_phase = WizardVsWorld.phases.enemy_attack_phase.EnemyAICombatPhase()
    enemy_movement_phase = WizardVsWorld.phases.enemy_movement_phase.EnemyAIMovement()

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
