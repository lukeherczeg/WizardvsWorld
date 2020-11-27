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


def get_all_stats(entity):
    # Initialize the first stat as the name
    stats = [entity.get_name()]
    # Add all the other entity stats
    stats.extend(entity.get_character_stats())
    # Make each stat in the array a formatted string to print
    stats[1] = f"Health: {stats[1]}/{entity.get_max_health()}"
    stats[2] = f"Defense: {stats[2]}"
    stats[3] = f"Attack: {stats[3]}"
    stats[4] = f"Range: {stats[4]}"
    stats[5] = f"Crit Chance: {stats[5]}"
    stats[6] = f"Hit Chance: {stats[6]}"
    stats[7] = f"Movement: {stats[7]}"
    return stats


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
        self.prev_tile = player.currentTile
        self.grid = GRID
        self.immovable_tiles = None
        self.movable_tiles = None
        self.enemy_tiles = None
        self.occupied_index = 0
        self.is_tutorial = True
        self.level_win_snow_tile = GRID.game_map[0][16]
        self.level_win_grass_tile = GRID.game_map[7][24]
        self.level_win_sand_tile = GRID.game_map[14][8]
        self.all_bosses_defeated = False
        self.level_complete = False
        #bools used for knowing which maps to load and which animations
        self.load_grass = False
        self.load_snow = False
        self.load_sand = False

    def cyclic_last(self, tile_list, current_tile):
        self.occupied_index -= 1
        return tile_list[(current_tile - 1) % len(tile_list)]

    def cyclic_next(self, tile_list, current_tile):
        self.occupied_index += 1
        return tile_list[(current_tile + 1) % len(tile_list)]

    def display_tile_type(self, tile_info, draw_color, row, col, offset_x, offset_y):
        if self.currentTile.win_tile and self.all_bosses_defeated:
            draw_text("Win Tile", 24, GRID.game_map[row][col], (offset_x, offset_y), BRIGHT_GREEN)
        elif tile_info == TileTexture.DIRT:
            draw_text("Dirt", 24, GRID.game_map[row][col], (offset_x, offset_y), draw_color)
        elif tile_info == TileTexture.GRASS:
            draw_text("Grass", 24, GRID.game_map[row][col], (offset_x, offset_y), draw_color)
        elif tile_info == TileTexture.FLOOR:
            draw_text("Floor Tile", 24, GRID.game_map[row][col], (offset_x, offset_y), draw_color)
        elif tile_info == TileTexture.BUSH:
            draw_text("Bush", 24, GRID.game_map[row][col], (offset_x, offset_y), draw_color)
        elif tile_info == TileTexture.STONE:
            draw_text("Stone Wall", 24, GRID.game_map[row][col], (offset_x, offset_y), draw_color)

        if self.currentTile.standable:
            draw_color = BLUE
            standable = "(Standable)"
        else:
            draw_color = RED
            standable = "(Non-Standable)"

        offset_y += .75
        draw_text(standable, 18, GRID.game_map[row][col],
                  (offset_x, offset_y), draw_color)

    def display_tile_info(self, entities_in_top_left):
        if entities_in_top_left:
            draw_rectangular_area(GRID.game_map[10][0], GRID.game_map[14][3])
        else:
            draw_rectangular_area(GRID.game_map[1][0], GRID.game_map[5][3])

        stats = []
        tile_info = []
        draw_color = WHITE
        if self.currentTile.occupied:
            for enemy in ENTITIES:
                if enemy.currentTile is self.currentTile:
                    stats = get_all_stats(enemy)
                    draw_color = BRIGHT_RED

        elif self.currentTile is self.player.currentTile:
            stats = get_all_stats(self.player)
            draw_color = BLUE
        else:
            tile_info = self.currentTile.texture_type

        if entities_in_top_left:
            stat_draw_location = [10, 0]
        else:
            stat_draw_location = [1, 0]

        stat_draw_offset_vertical = 0
        stat_draw_offset_horizontal = .03

        # Print the character type slightly larger before the rest of the stats
        if len(stats) > 0:
            draw_text(stats[0], 24, GRID.game_map[stat_draw_location[0]][stat_draw_location[1]],
                      (stat_draw_offset_horizontal, stat_draw_offset_vertical), draw_color)
            stat_draw_offset_vertical += .75
            # Print all other stats to the top left of the screen
            for stat in stats[1:]:
                draw_text(stat, 15, GRID.game_map[stat_draw_location[0]][stat_draw_location[1]],
                          (stat_draw_offset_horizontal, stat_draw_offset_vertical))
                stat_draw_offset_vertical += .5
        # If there aren't any entities on this tile, we display the tile type instead
        else:
            draw_color = WHITE

            self.display_tile_type(tile_info, draw_color, stat_draw_location[0], stat_draw_location[1],
                                   stat_draw_offset_horizontal, stat_draw_offset_vertical)

    def select_tile(self, row, col):
        """Restricts tile selection based on the tile constraints passed to it.
           If there are no movable or enemy tiles, then it must be normal, free selection phase,
           if there are movable tiles, it sets constraints and tints for the movement phase,
           and if there are enemy tiles, it sets constraints for the attack phase."""

        # Free selection phase
        if self.movable_tiles is None and self.enemy_tiles is None:
            if self.grid.is_valid_tile(row, col):
                # Draw the previous tile
                draw_tile(self.currentTile)

                self.currentTile = self.grid.game_map[row][col]

                tile = self.currentTile

                rect_size = 2
                #   for example, rect_size = 2 means:
                #
                #   2 1 0 1 2
                #   X X X X X
                #   X X X X X
                #   X X O X X
                #   X X X X X
                #   X X X X X
                #
                #   where O is the current tile.

                # We check if it is possible to make a n-size rect area, and if not, make an n-1,
                # n-2, and so on until n=0
                for i in range(rect_size + 1):
                    if GRID.is_valid_tile(tile.row - rect_size, tile.col - rect_size) and \
                            GRID.is_valid_tile(tile.row + rect_size, tile.col + rect_size):
                        top_left = GRID.game_map[tile.row - rect_size][tile.col - rect_size]
                        bottom_right = GRID.game_map[tile.row + rect_size][tile.col + rect_size]
                        entities_in_top_left = check_for_entities_in_area(GRID.game_map[1][0], GRID.game_map[5][3])
                        self.display_tile_info(entities_in_top_left)
                        select(self.currentTile.row, self.currentTile.col)
                        draw_entities_in_rectangular_area(top_left, bottom_right)
                        break
                    else:
                        rect_size = rect_size - 1

                if rect_size == 0:
                    draw_entity_from_tile(self.prev_tile)

        # Movement selection phase
        elif self.movable_tiles and self.grid.is_valid_tile_in_list(row, col, self.movable_tiles):
            draw_tinted_tiles(self.movable_tiles, self.player, TileTint.BLUE)
            self.currentTile = self.grid.game_map[row][col]
            select(self.currentTile.row, self.currentTile.col)
            draw_entity_from_tile(self.currentTile)

        # Attack selection phase
        elif self.enemy_tiles and self.grid.is_valid_tile_in_list(row, col, self.enemy_tiles):
            draw_tinted_tiles(self.enemy_tiles, self.player, TileTint.ORANGE)
            self.currentTile = self.grid.game_map[row][col]
            select(self.currentTile.row, self.currentTile.col)
            draw_entity_from_tile(self.currentTile)

            # If we want to use enemy specific selection tiles:

            # for enemy in ENTITIES:
            #     if enemy.currentTile is self.currentTile:
            #         select(self.currentTile.row, self.currentTile.col, enemy)
            #         break

    def select_by_keypress(self, event):
        row = self.currentTile.row
        col = self.currentTile.col
        if self.enemy_tiles is None:
            self.prev_tile = GRID.game_map[row][col]
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
                self.prev_tile = hovered_tile
                self.select_tile(hovered_tile.row, hovered_tile.col)

            elif event.key == pygame.K_RIGHT or event.key == pygame.K_UP:
                hovered_tile = self.cyclic_last(occupied_enemy_tiles, self.occupied_index)
                self.prev_tile = hovered_tile
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
                            #Several win tiles, level is complete if on any one of them and all bosses defeated
                            if self.all_bosses_defeated:
                                self.level_win_grass_tile.tint = TileTint.ORANGE
                                self.level_win_snow_tile.tint = TileTint.ORANGE
                                self.level_win_sand_tile.tint = TileTint.ORANGE
                                #if player is on a win tile acknowledge this and level is complete
                                if self.player.currentTile == self.level_win_grass_tile:
                                    self.load_grass = True
                                    self.level_complete = True
                                elif self.player.currentTile == self.level_win_snow_tile:
                                    self.load_snow = True
                                    self.level_complete = True
                                elif self.player.currentTile == self.level_win_sand_tile:
                                    self.load_sand = True
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

        select(self.currentTile.row, self.currentTile.col)
        draw_entity_from_tile(self.currentTile)
        initial_tile = self.currentTile

        selecting = True
        while selecting:
            if self.selection():
                selecting = False

        clear_tinted_tiles(self.movable_tiles, self.player)
        clear_tinted_tiles(self.immovable_tiles, self.player)

        self.player.currentTile = self.currentTile

        animate_entity_movement(self.player, initial_tile)

    def enter(self):
        bosses_remaining = 0
        for enemy in ENTITIES[1:]:
            if isinstance(enemy, Boss):
                bosses_remaining += 1
        if bosses_remaining < 1:
            self.all_bosses_defeated = True

        self.enemy_tiles = None
        self.currentTile = self.player.currentTile
        # Stop heal from level advance
        self.player.healing = False
        total_refresh_drawing()

        background = pygame.transform.scale(BACKGROUND_PNG, (562, 225))
        animate_text_abs('Player Phase', 75, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, BLUE, 1, background, 15)
        total_refresh_drawing()

        if self.all_bosses_defeated:
            self.level_win_grass_tile.tint = TileTint.ORANGE
            self.level_win_snow_tile.tint = TileTint.ORANGE
            self.level_win_sand_tile.tint = TileTint.ORANGE
            if self.player.currentTile == self.level_win_grass_tile:
                self.load_grass = True
                self.level_complete = True
            if self.player.currentTile == self.level_win_snow_tile:
                self.load_snow = True
                self.level_complete = True
            if self.player.currentTile == self.level_win_sand_tile:
                self.load_sand = True
                self.level_complete = True


        if not self.level_complete:
            # TUTORIAL
            if self.is_tutorial:
                MessageBox('In order to win, defeat the boss inside the castle guarding the exit!')
                MessageBox('After defeating the boss, the entrance to the next level will be highlighted.')
                GRID.game_map[7][24].tint = TileTint.ORANGE
                total_refresh_drawing()
                MessageBox('See that orange tile at the back of the castle on the right? That\'s it!')
                GRID.game_map[7][24].tint = TileTint.NONE
                MessageBox('You can use the arrow keys to move the tile selector. ENTER will let you select a character. '
                           + 'You are the lone wizard in blue. Select the wizard!')

                total_refresh_drawing()

            entities_in_top_left = check_for_entities_in_area(GRID.game_map[1][0], GRID.game_map[5][3])
            self.display_tile_info(entities_in_top_left)
            select(self.currentTile.row, self.currentTile.col)
            draw_entity_from_tile(self.currentTile)
            selecting = True
            while selecting:
                if self.selection():
                    if self.currentTile == self.player.currentTile:

                        # TUTORIAL
                        if self.is_tutorial:
                            MessageBox('Great job! Now pick one of the blue spaces to move to.')

                        total_refresh_drawing()

                        selecting = False

    def update(self):
        if not self.level_complete:
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
            prev_enemies = []
            prev_location = [self.player.currentTile.row, self.player.currentTile.col]

            if len(ENTITIES) > 1:
                prev_enemies = ENTITIES[1:]
                wiz = ENTITIES[0]
                ENTITIES.clear()
                ENTITIES.append(wiz)

            if self.load_grass:
                #for grid.update_layout 1,2,3 depending on level type 1 is grass, 2 is sand 3 is snow
                GRID.update_layout(1)
                new_map = [[GRID.generate_tile(x, y) for x in range(GRID.GRID_WIDTH)] for y in range(GRID.GRID_HEIGHT)]
                GRID.set_game_map(new_map)
                GRID.generate_enemies(self.player.level)
                prev_map = GRID
                animate_map_transition(prev_map, prev_enemies, self.player)
                self.player.currentTile = GRID.game_map[prev_location[0]][0]
                self.load_grass = False
            elif self.load_sand:
                GRID.update_layout(2)
                new_map = [[GRID.generate_tile(x, y) for x in range(GRID.GRID_WIDTH)] for y in range(GRID.GRID_HEIGHT)]
                GRID.set_game_map(new_map)
                GRID.generate_enemies(self.player.level)
                prev_map = GRID
                animate_map_transition_up(prev_map, prev_enemies, self.player)
                self.player.currentTile = GRID.game_map[0][8]
                self.load_sand = False
            elif self.load_snow:
                GRID.update_layout(3)
                new_map = [[GRID.generate_tile(x, y) for x in range(GRID.GRID_WIDTH)] for y in range(GRID.GRID_HEIGHT)]
                GRID.set_game_map(new_map)
                GRID.generate_enemies(self.player.level)
                prev_map = GRID
                animate_map_transition_down(prev_map, prev_enemies, self.player)
                self.player.currentTile = GRID.game_map[14][16]
                self.load_snow = False
            self.player.health = self.player.max_health
            self.all_bosses_defeated = False
            self.level_complete = False
            self.level_win_grass_tile = GRID.win_tile
            self.level_win_snow_tile = GRID.win_tile
            self.level_win_sand_tile = GRID.win_tile
            self.enter()
            self.update()
            self.exit()
