from draw import *
from classes.fsm import FSM
from classes.entity import Player, Enemy
import phases.movement_phase

print(f'Grid Width: {GRID.GRID_WIDTH}; Grid Height: {GRID.GRID_HEIGHT}')


def main():
    player = Player()
    fsm = FSM()

    pygame.init()

    enemy = Enemy()

    draw_grid()
    draw_characters([enemy])
    old_pos = enemy.get_position().col, enemy.get_position().row
    enemy.currentTile = GRID.game_map[10][10]
    move_player(enemy, old_pos)

    # fsm.add_phase(phases.movement_phase.PlayerMovementPhase(player))
    # fsm.next_phase()
    # fsm.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        # pygame.draw.rect(SCREEN, WHITE, button)

if __name__ == "__main__":
    main()
