from draw import *
from classes.fsm import FSM
from classes.entity import Player, Enemy
import phases.movement_phase

print(f'Grid Width: {GRID.GRID_WIDTH}; Grid Height: {GRID.GRID_HEIGHT}')


def main():
    player = Player()
    fsm = FSM()

    pygame.init()

    SCREEN.fill(BLACK)
    draw_grid()
    draw_characters([Enemy(), Enemy()])

    fsm.add_phase(phases.movement_phase.PlayerMovementPhase(player))
    fsm.next_phase()
    fsm.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        pygame.display.update()


if __name__ == "__main__":
    main()
