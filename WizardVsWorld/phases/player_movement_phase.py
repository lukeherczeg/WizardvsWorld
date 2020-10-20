from WizardVsWorld.classes.draw import *
from WizardVsWorld.classes.phase import Phase
from WizardVsWorld.classes.entity import Player, Boss
from WizardVsWorld.classes.tile import Tile
from WizardVsWorld.classes.user_interface import MessageBox, SelectionMenu


def select(row, col, enemy=None):
    if enemy is None:
        draw_selected_tile(GRID.game_map[row][col])
    else:
        draw_selected_tile(GRID.game_map[row][col], enemy)


class PlayerMovementPhase(Phase):
    player: Player
    currentTile: Tile
    grid: Grid
    immovable_tiles: [Tile]
    movable_tiles: [Tile]
    enemy_tiles: [Tile]
    occupied_index: int

    def __init__(self, player):
        self.player = player
        self.currentTile = player.currentTile
        self.grid = GRID
        self.immovable_tiles = None
        self.movable_tiles = None
        self.enemy_tiles = None
        self.occupied_index = 0
        self.is_tutorial = True
        self.level_win_tile = GRID.game_map[7][24]
        self.all_bosses_defeated = False
        self.level_complete = False

    def cyclic_last(self, tile_list, current_tile):
        self.occupied_index -= 1
        return tile_list[(current_tile - 1) % len(tile_list)]

    def cyclic_next(self, tile_list, current_tile):
        self.occupied_index += 1
        return tile_list[(current_tile + 1) % len(tile_list)]

    def select_tile(self, row, col):
        """Restricts tile selection based on the tile constraints passed to it.
           If there are no movable or enemy tiles, then it must be normal, free selection phase,
           if there are movable tiles, it sets constraints and tints for the movement phase,
           and if there are enemy tiles, it sets constraints for the attack phase."""

        if self.movable_tiles is None and self.enemy_tiles is None:
            if self.grid.is_valid_standable_tile(row, col):
                draw_tile(self.currentTile)
                self.currentTile = self.grid.game_map[row][col]
                select(self.currentTile.row, self.currentTile.col)
                draw_entities()

        elif self.movable_tiles and self.grid.is_valid_tile_in_list(row, col, self.movable_tiles):
            draw_tinted_tiles(self.movable_tiles, self.player, TileTint.BLUE)
            self.currentTile = self.grid.game_map[row][col]
            select(self.currentTile.row, self.currentTile.col)

        elif self.enemy_tiles and self.grid.is_valid_tile_in_list(row, col, self.enemy_tiles):
            draw_tinted_tiles(self.enemy_tiles, self.player, TileTint.ORANGE)
            self.currentTile = self.grid.game_map[row][col]
            select(self.currentTile.row, self.currentTile.col)

            # If we want to use enemy specific selection tiles:

            # for enemy in ENTITIES:
            #     if enemy.currentTile is self.currentTile:
            #         select(self.currentTile.row, self.currentTile.col, enemy)
            #         break

    def select_by_keypress(self, event):
        row = self.currentTile.row
        col = self.currentTile.col
        if self.enemy_tiles is None:
            if event.key == pygame.K_LEFT:
                self.select_tile(row, col - 1)

            elif event.key == pygame.K_RIGHT:
                self.select_tile(row, col + 1)

            elif event.key == pygame.K_UP:
                self.select_tile(row - 1, col)

            elif event.key == pygame.K_DOWN:
                self.select_tile(row + 1, col)
        else:
            occupied_enemy_tiles = []

            for tile in self.enemy_tiles:
                if tile.occupied:
                    occupied_enemy_tiles.append(tile)

            if event.key == pygame.K_LEFT or event.key == pygame.K_DOWN:
                hovered_tile = self.cyclic_next(occupied_enemy_tiles, self.occupied_index)
                self.select_tile(hovered_tile.row, hovered_tile.col)

            elif event.key == pygame.K_RIGHT or event.key == pygame.K_UP:
                hovered_tile = self.cyclic_last(occupied_enemy_tiles, self.occupied_index)
                self.select_tile(hovered_tile.row, hovered_tile.col)

    def selection(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:
                    if self.movable_tiles is None and self.enemy_tiles is None:
                        return True
                    elif self.movable_tiles:
                        if self.currentTile in self.movable_tiles:
                            if self.all_bosses_defeated and self.currentTile == self.level_win_tile:
                                self.level_complete = True
                            return True
                    elif self.enemy_tiles:
                        if self.currentTile in self.enemy_tiles and self.currentTile.occupied:
                            return True

                self.select_by_keypress(event)

    def movement(self):
        movable_tiles = GRID.get_movement(self.currentTile.row, self.currentTile.col, self.player.max_movement)
        self.immovable_tiles = GRID.get_movement_border(movable_tiles, self.player.range)
        self.movable_tiles = list(set(movable_tiles).difference(set(self.immovable_tiles)))
        draw_tinted_tiles(self.movable_tiles, self.player, TileTint.BLUE)
        draw_tinted_tiles(self.immovable_tiles, self.player, TileTint.RED)

        initial_tile = self.currentTile

        select(self.currentTile.row, self.currentTile.col)
        selecting = True
        while selecting:
            if self.selection():
                self.player.selected = False
                selecting = False

        self.player.currentTile = self.currentTile

        animate_entity_movement(self.player, initial_tile)

    def enter(self):
        bosses_remaining = 0
        for enemy in ENTITIES[1:]:
            if isinstance(enemy, Boss):
                bosses_remaining += 1
        if bosses_remaining < 1:
            self.all_bosses_defeated = True

        if self.all_bosses_defeated:
            self.level_win_tile.tint = TileTint.ORANGE

        self.enemy_tiles = None
        self.currentTile = self.player.currentTile
        total_refresh_drawing()

        background = pygame.transform.scale(BACKGROUND_PNG, (562, 225))
        animate_text_abs('Player Phase', 75, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, BLUE, 1, background, 15)
        total_refresh_drawing()

        # TUTORIAL
        if self.is_tutorial:
            MessageBox('In order to win, defeat the boss inside the castle guarding the exit!')
            MessageBox('After defeating the boss, the entrance to the next level will be highlighted.')
            GRID.game_map[7][24].tint = TileTint.ORANGE
            total_refresh_drawing()
            MessageBox('See that orange tile at the back of the castle on the right? That\'s it!')
            GRID.game_map[7][24].tint = TileTint.NONE
            total_refresh_drawing()
            MessageBox('You can use the arrow keys to move the tile selector. ENTER will let you select a character. '
                       + 'You are the lone wizard in blue. Please select yourself!')
            
            total_refresh_drawing()

        select(self.currentTile.row, self.currentTile.col)
        selecting = True
        while selecting:
            if self.selection():
                if self.currentTile == self.player.currentTile:
                    self.player.selected = True

                    # TUTORIAL
                    if self.is_tutorial:
                        MessageBox('Great job! Now pick one of the blue spaces to move to.')
                        total_refresh_drawing()

                    selecting = False

    def update(self):
        self.movement()

    def exit(self):
        self.movable_tiles = None
        self.is_tutorial = False
        if self.level_complete:
            self.player.level_up(self.player.level + 1)
            upgrade_menu = SelectionMenu('You leveled up! Choose an Upgrade', [
                ('Health', 'Increase your Health by 15', self.player.boost_health),
                ('Attack', 'Increase your Attack by 5', self.player.boost_attack),
                ('Movement', 'Increase your Movement by 1', self.player.boost_movement)])
            upgrade_menu.draw_menu()
            upgrade_menu.await_response()
            prev_map = GRID
            prev_enemies = []
            prev_location = [self.player.currentTile.row, self.player.currentTile.col]

            if len(ENTITIES) > 1:
                prev_enemies = ENTITIES[1:]
                wiz = ENTITIES[0]
                ENTITIES.clear()
                ENTITIES.append(wiz)

            GRID.update_layout()
            new_map = [[GRID.generate_tile(x, y) for x in range(GRID.GRID_WIDTH)] for y in range(GRID.GRID_HEIGHT)]
            GRID.set_game_map(new_map)
            GRID.generate_enemies(self.player.level)

            animate_map_transition(prev_map, prev_enemies, self.player)
            self.player.currentTile = GRID.game_map[prev_location[0]][0]
            self.player.health = self.player.max_health
            self.all_bosses_defeated = False
            self.level_complete = False
            self.level_win_tile = GRID.win_tile
            self.enter()
            self.update()
            self.exit()