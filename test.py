import os
import pygame
import sys

def test(SCREEN):
        BLOCK = 40
        x = 0
        y = 0
        main_directory = os.path.dirname('WizardvsWorld')
        asset_path = os.path.join(main_directory, 'assets')
        image = os.path.join(asset_path, 'dirt.png')
        dirt = pygame.image.load(image)

        main_directory = os.path.dirname('WizardvsWorld')
        asset_path = os.path.join(main_directory, 'assets')
        image = os.path.join(asset_path, 'grass.png')
        grass = pygame.image.load(image)

        main_directory = os.path.dirname('WizardvsWorld')
        asset_path = os.path.join(main_directory, 'assets')
        image = os.path.join(asset_path, 'stone.png')
        stone = pygame.image.load(image)

        main_directory = os.path.dirname('WizardvsWorld')
        asset_path = os.path.join(main_directory, 'assets')
        image = os.path.join(asset_path, 'floor.png')
        floor = pygame.image.load(image)

        main_directory = os.path.dirname('WizardvsWorld')
        asset_path = os.path.join(main_directory, 'assets')
        image = os.path.join(asset_path, 'dirtBLUE.png')
        dirtBLUE = pygame.image.load(image)

        main_directory = os.path.dirname('WizardvsWorld')
        asset_path = os.path.join(main_directory, 'assets')
        image = os.path.join(asset_path, 'grassBLUE.png')
        grassBLUE = pygame.image.load(image)

        main_directory = os.path.dirname('WizardvsWorld')
        asset_path = os.path.join(main_directory, 'assets')
        image = os.path.join(asset_path, 'stoneBLUE.png')
        stoneBLUE = pygame.image.load(image)

        main_directory = os.path.dirname('WizardvsWorld')
        asset_path = os.path.join(main_directory, 'assets')
        image = os.path.join(asset_path, 'dirtORANGE.png')
        dirtORANGE = pygame.image.load(image)

        main_directory = os.path.dirname('WizardvsWorld')
        asset_path = os.path.join(main_directory, 'assets')
        image = os.path.join(asset_path, 'grassORANGE.png')
        grassORANGE = pygame.image.load(image)

        main_directory = os.path.dirname('WizardvsWorld')
        asset_path = os.path.join(main_directory, 'assets')
        image = os.path.join(asset_path, 'stoneORANGE.png')
        stoneORANGE = pygame.image.load(image)

        main_directory = os.path.dirname('WizardvsWorld')
        asset_path = os.path.join(main_directory, 'assets')
        image = os.path.join(asset_path, 'dirtRED.png')
        dirtRED = pygame.image.load(image)

        main_directory = os.path.dirname('WizardvsWorld')
        asset_path = os.path.join(main_directory, 'assets')
        image = os.path.join(asset_path, 'grassRED.png')
        grassRED = pygame.image.load(image)

        main_directory = os.path.dirname('WizardvsWorld')
        asset_path = os.path.join(main_directory, 'assets')
        image = os.path.join(asset_path, 'stoneRED.png')
        stoneRED = pygame.image.load(image)

        main_directory = os.path.dirname('WizardvsWorld')
        asset_path = os.path.join(main_directory, 'maps')
        map = os.path.join(asset_path, 'test_map.txt')

        main_directory = os.path.dirname('WizardvsWorld')
        asset_path = os.path.join(main_directory, 'assets')
        image = os.path.join(asset_path, 'wiz.png')
        wiz = pygame.image.load(image)

        main_directory = os.path.dirname('WizardvsWorld')
        asset_path = os.path.join(main_directory, 'assets')
        image = os.path.join(asset_path, 'wizattack.png')
        wizattack = pygame.image.load(image)

        main_directory = os.path.dirname('WizardvsWorld')
        asset_path = os.path.join(main_directory, 'assets')
        image = os.path.join(asset_path, 'wizhurt.png')
        wizhurt = pygame.image.load(image)

        main_directory = os.path.dirname('WizardvsWorld')
        asset_path = os.path.join(main_directory, 'assets')
        image = os.path.join(asset_path, 'wizselected.png')
        wizselected = pygame.image.load(image)

        main_directory = os.path.dirname('WizardvsWorld')
        asset_path = os.path.join(main_directory, 'assets')
        image = os.path.join(asset_path, 'knight.png')
        knight = pygame.image.load(image)

        main_directory = os.path.dirname('WizardvsWorld')
        asset_path = os.path.join(main_directory, 'assets')
        image = os.path.join(asset_path, 'knighthurt.png')
        knighthurt = pygame.image.load(image)

        main_directory = os.path.dirname('WizardvsWorld')
        asset_path = os.path.join(main_directory, 'assets')
        image = os.path.join(asset_path, 'knightattack.png')
        knightattack = pygame.image.load(image)

        main_directory = os.path.dirname('WizardvsWorld')
        asset_path = os.path.join(main_directory, 'assets')
        image = os.path.join(asset_path, 'archer.png')
        archer = pygame.image.load(image)

        main_directory = os.path.dirname('WizardvsWorld')
        asset_path = os.path.join(main_directory, 'assets')
        image = os.path.join(asset_path, 'archerattack.png')
        archerattack = pygame.image.load(image)

        main_directory = os.path.dirname('WizardvsWorld')
        asset_path = os.path.join(main_directory, 'assets')
        image = os.path.join(asset_path, 'archerhurt.png')
        archerhurt = pygame.image.load(image)

        file = open(map, 'r')
        while True:
            for line in file:
                tiles = line.split()

                i = 0
                x = 0
                while i < 25:
                    if tiles[i] == '0':
                        SCREEN.blit(grass, (x, y))
                    elif tiles[i] == '1':
                        SCREEN.blit(dirt, (x, y))
                    elif tiles[i] == '2':
                        SCREEN.blit(stone, (x, y))
                    elif tiles[i] == '3':
                        SCREEN.blit(floor, (x,  y))
                    i += 1
                    x += BLOCK
                y += BLOCK

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            SCREEN.blit(wiz, (0, 0))
            SCREEN.blit(wizattack, (120, 120))
            SCREEN.blit(wizhurt, (240, 240))

            SCREEN.blit(knight, (40, 0))
            SCREEN.blit(knightattack, (160, 120))
            SCREEN.blit(knighthurt, (280, 240))
            SCREEN.blit(archer, (80, 0))
            SCREEN.blit(archerattack, (200, 120))
            SCREEN.blit(archerhurt, (320, 240))
            SCREEN.blit(stoneBLUE, (6 * BLOCK, 10 * BLOCK))
            SCREEN.blit(dirtBLUE, (6 * BLOCK, 11 * BLOCK))
            SCREEN.blit(grassBLUE, (6 * BLOCK, 12 * BLOCK))
            SCREEN.blit(stoneORANGE, (7 * BLOCK, 10 * BLOCK))
            SCREEN.blit(dirtORANGE, (7 * BLOCK, 11 * BLOCK))
            SCREEN.blit(grassORANGE, (7 * BLOCK, 12 * BLOCK))
            SCREEN.blit(stoneRED, (8 * BLOCK, 10 * BLOCK))
            SCREEN.blit(dirtRED, (8 * BLOCK, 11 * BLOCK))
            SCREEN.blit(grassRED, (8 * BLOCK, 12 * BLOCK))
            SCREEN.blit(wizselected, (6 * BLOCK, 11 * BLOCK))
            pygame.display.update()