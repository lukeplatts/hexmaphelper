import random
import os

water = [9, 1, 1, 6, 3, 1, 0]
swamp = [1, 9, 0, 6, 3, 0, 0]
desert = [1, 0, 9, 3, 0, 6, 1]
plains = [1, 1, 1, 9, 6, 3, 0]
forest = [1, 1, 0, 6, 9, 3, 1]
hills = [1, 0, 1, 3, 1, 9, 6]
mountain = [0, 0, 1, 0, 3, 6, 9]

terrtypes = ['water', 'swamp', 'desert', 'plains', 'forest', 'hills', 'mountain']
terrvalues = [water, swamp, desert, plains, forest, hills, mountain]
climates = ['arctic', 'subarctic', 'temperate', 'subtropical', 'tropical']

terraindict = {}
for terrtype1 in terrtypes:
    terraindict[terrtype1] = {}
    for terrtype2 in terrtypes:
        terraindict[terrtype1][terrtype2] = terrvalues[terrtypes.index(terrtype1)][terrtypes.index(terrtype2)]


def tileroll(optionslist, weights=None):
    """
    Rolls randomly to determine a tile.
    :param: optionslist - list of tile options.
    :param: chance - list of chance for each tile in the list. Must add to <= 1, and be in same order as optionslist.

    :returns: Tile option from optionslist
    """
    return random.choices(optionslist, weights=weights)


def tile_terrain_creation(terrtype):
    """
    Creates a dictionary containing the number of tiles that a terrain hex should have from a given terrain type.
    """
    if terrtype not in terrtypes:
        raise TypeError(f'Terrain type {terrtype} not accepted. Terrain types are: water, swamp, desert, plains, '
                        f'forest, hills, mountain.')
    # Reset Rolls.
    roll = None
    # Create initial dictionary for tile.
    tiledict = {'type': terrtype, 'water': 0, 'swamp': 0, 'desert': 0, 'plains': 0, 'forest': 0, 'hills': 0,
                'mountain': 0}

    # Find primary, secondary, and tertiary tiles.
    primary = [k for k, v in terraindict[terrtype].items() if v == 9][0]
    secondary = [k for k, v in terraindict[terrtype].items() if v == 6][0]
    tertiary = [k for k, v in terraindict[terrtype].items() if v == 3][0]

    # Wildcard Generation
    wldcrdx = 0
    for i in range(3):
        if random.random() <= 0.1:
            wldcrdx += 1
            wildcards = [k for k, v in terraindict[terrtype].items() if v == 1]
            wildcard = tileroll(wildcards)
            tiledict[wildcard[0]] += 1

    # Assign tiles to tiledict.
    tiledict[primary] = terraindict[terrtype][primary]
    tiledict[secondary] = terraindict[terrtype][secondary]
    tiledict[tertiary] = terraindict[terrtype][tertiary] - wldcrdx

    # Water Terrain Tile Special Cases
    if terrtype == 'water':
        # Roll for light vs heavy forest.
        lightforest, heavyforest = 0, 0
        for i in range(tiledict['forest']):
            roll = tileroll(['light forest', 'heavy forest'], [0.66, 0.33])
            if roll == ['light forest']:
                lightforest += 1
            elif roll == ['heavy forest']:
                heavyforest += 1
        tiledict['forest'] -= (lightforest + heavyforest)
        tiledict['light forest'] = lightforest
        tiledict['heavy forest'] = heavyforest

    # Desert Terrain Tile Special Cases
    if terrtype == 'desert':
        # Roll for Hills Modifier
        modhills, rockdesert, highdunes = 0, 0, 0
        for i in range(terraindict["desert"]["hills"]):
            roll = tileroll(['hillmod', 'nomod'], [0.33, 0.66])
            if roll == ['hillmod']:
                modhills += 1
                if tileroll(['rockdesert', 'highdunes'], [0.5, 0.5]) == ['rockdesert']:
                    rockdesert += 1
                else:
                    highdunes += 1
        if modhills > 0:
            tiledict['hills'] -= (rockdesert + highdunes)
            tiledict['rock desert'] = rockdesert
            tiledict['high dunes'] = highdunes

    # Plains Terrain Tile Special Cases
    if terrtype == 'plains':
        pass
        # Determine if tile is 'settled' and then set plains as farmland.

    # Forest Terrain Tile Special Cases
    if terrtype == 'forest':
        # Roll for light vs heavy forest.
        lightforest, heavyforest = 0, 0
        for i in range(tiledict['forest']):
            roll = tileroll(['light forest', 'heavy forest'], [0.66, 0.33])
            if roll == ['light forest']:
                lightforest += 1
            elif roll == ['heavy forest']:
                heavyforest += 1
        tiledict['forest'] -= (lightforest + heavyforest)
        tiledict['light forest'] = lightforest
        tiledict['heavy forest'] = heavyforest

        # Roll for forested hills vs grassy hills.
        forestedhills = 0
        for i in range(tiledict['hills']):
            roll = tileroll(['forested hill', 'hills'], [0.666, 0.333])
            if roll == ['forested hill']:
                forestedhills += 1
        if forestedhills > 0:
            tiledict['forested hill'] = forestedhills
            tiledict['hills'] -= forestedhills

        # Roll for forested mountains vs mountains.
        # Determine if mountain wildcard has been generated.
        if tiledict['mountain'] > 0:
            forestedmountain = 0
            for i in range(int(tiledict['mountain'])):
                roll = tileroll(['forested mountain', 'mountain'], [0.666, 0.333])
                if roll == ['mountain']:
                    forestedmountain += 1
            if forestedmountain > 0:
                tiledict['forested mountain'] = forestedmountain
                tiledict['mountain'] -= forestedmountain

    # Hills Terrain Tile Special Cases
    if terrtype == 'hills':
        # Roll for Forested Hills
        if tiledict['forest'] > 0:
            forestedhill = 0
            for i in range(int(tiledict['forest'])):
                roll = tileroll(['forested hill', 'forest'], [0.333, 0.666])
                if roll == ['forested hill']:
                    forestedhill += 1
            if forestedhill > 0:
                tiledict['forested hill'] = forestedhill
                tiledict['forest'] -= forestedhill
        # Roll for Canyon or Fissure
        canyon = 0
        for i in range(int(tiledict['hills'])):
            roll = tileroll(['canyon', 'hills'], [0.2, 0.8])
            if roll == ['canyon']:
                canyon += 1
        if canyon > 0:
            tiledict['canyon'] = canyon
            tiledict['hills'] -= canyon
        # Roll for Mountain Pass
        mpass = 0
        for i in range(int(tiledict['mountain'])):
            roll = tileroll(['mpass', 'mountain'], [0.4, 0.6])
            if roll == ['mpass']:
                mpass += 1
        if mpass > 0:
            tiledict['mountain pass'] = mpass
            tiledict['mountain'] -= mpass

    # Mountains Terrain Tile Special Cases
    if terrtype == ['mountain']:
        # Roll for Forested Mountain
        forestedmnt = 0
        for i in range(int(tiledict['forest'])):
            roll = tileroll(['forested mountain', 'forest'], [0.333, 0.666])
            if roll == ['forested mountain']:
                forestedmnt += 1
        if forestedmnt > 0:
            tiledict['forested mountain'] = forestedmnt
            tiledict['forest'] -= forestedmnt
        # Roll for Peak, Pass, or Volcano
        mpeak, mpass, mvol = 0, 0, 0
        for i in range(int(tiledict['mountain'])):
            roll = tileroll(['mountain',
                             'mountain peak',
                             'mountain pass',
                             'volcano'], [0.2, 0.1, 0.05, 0.65])
            if roll == ['mountain peak']:
                mpeak += 1
            elif roll == ['mountain pass']:
                mpass += 1
            elif roll == ['volcano']:
                mvol += 1
        tiledict['mountain'] -= (mpeak + mpass + mvol)
        tiledict['mountain peak'] = mpeak
        tiledict['mountain pass'] = mpass
        tiledict['volcano'] = mvol

    return tiledict


def format_tiledict(tiledict, returnres=False):
    """
    Recieves a dictonary of tile numbers, trims the empty values, and prints the number
    of each tile in an easily readable format.

    :param: tiledict
    Dictionary of tiles from tile_terrain_creation() function.
    """

    print(f"TERRAIN TYPE: {tiledict['type']}")
    newdict = {}
    # Strip the type from the dictionary.
    for k, v in tiledict.items():
        if type(v) is not int:
            continue
        else:
            newdict[k] = v
    for k, v in sorted(newdict.items(), key=lambda item: item[1], reverse=True):
        if v > 1:
            print(f'{v} {k} tiles.')
        if v == 1:
            print(f'{v} {k} tile.')

    if returnres:
        printlist = []
        for k, v in sorted(newdict.items(), key=lambda item: item[1], reverse=True):
            if v > 1:
                printlist.append(f'{v} {k} tiles.')
            if v == 1:
                printlist.append(f'{v} {k} tile.')
        return printlist


def generate_encounters(ttype, climate='temperate'):
    majencprob = {'water': 0.1,
                  'swamp': 0.2,
                  'desert': 0.2,
                  'plains': 0.6,
                  'forest': 0.4,
                  'hills': 0.4,
                  'mountain': 0.2}
    climatemod = {'arctic': -0.1,
                  'subarctic': -0.05,
                  'temperate': 0,
                  'subtropical': 0.05,
                  'tropical': 0.1}
    # Roll Major Encounters
    majencroll = tileroll(['majencounter', 'noencounter'], [majencprob[ttype] + climatemod[climate],
                                                            1 - majencprob[ttype] - climatemod[climate]])
    if majencroll == ['majencounter']:
        majenc = tileroll(['Settlement',
                           'Fortress',
                           'Religious Order',
                           'Ruin',
                           'Monster Lair',
                           'Natural Phenomenon'])
        print(f'MAJOR ENCOUNTER: There is a {majenc[0]} in this terrain.')

        # Major Encounter Specifics
        if majenc == ['Religious Order']:
            alignment = tileroll(['Lawful', 'Neutral', 'Chaotic'])
            print(f'The religious order is of a {alignment[0]} alignment.')

        if majenc == ['Ruin']:
            abandoned = tileroll(['disease', 'being attacked', 'migration'], weights=[1 / 6, 2 / 6, 2 / 6])
            print(f'The ruin was abandoned due to {abandoned[0]}.')

        if majenc == ['Natural Phenomenon']:
            feature = tileroll(['intense weather',
                                'geothermal activity',
                                'a peculiar growth or blight',
                                'an oasis/grove'], weights=[1 / 6, 2 / 6, 2 / 6, 1 / 6])
            print(f'The natural phenomenon in this terrain is {feature[0]}.')

    # Roll Minor Encounters
    for i in range(int(majencprob[ttype] * 10)):
        minorencroll = tileroll(['minencounter', 'noencounter'], weights=[1 / 6, 5 / 6])
        if minorencroll == ['minencounter']:
            minorenc = tileroll(['Village',
                                 'Fort',
                                 'Ruin',
                                 'Monster Lair',
                                 'Wandering Monster',
                                 'Industrial Camp',
                                 'Semi-Permenant Camp',
                                 'Beacon',
                                 'Construction Site',
                                 'Battlefield',
                                 "Outsider's Dwelling",
                                 'Sacred Site',
                                 'Crossing',
                                 'Ancient Structure',
                                 'Special Hazard',
                                 'Treasure',
                                 'Contested Area',
                                 'Natural Resource',
                                 'Supernatural Feature',
                                 'Gathering Place'])
            print(f'MINOR ENCOUNTER: There is a {minorenc[0]} in this terrain.')

            # Minor Encounter Specifics

    print('\n')


def ProcessWrapper(ttype):

    if ttype not in terrtypes:
        print(f'Terrain type {ttype} not accepted. Terrain types are: water, swamp, desert, plains, '
              f'forest, hills, mountain.')
        raise TypeError
    td = tile_terrain_creation(ttype)
    printlist = (format_tiledict(td, returnres=True))
    return printlist


if __name__ == '__main__':
    while True:
        ttype = input('What is the terrain type?: ').lower()
        if ttype not in terrtypes:
            print(f'Terrain type {ttype} not accepted. Terrain types are: water, swamp, desert, plains, '
                  f'forest, hills, mountain.')
            continue
        td = tile_terrain_creation(ttype)
        format_tiledict(td)
        generate_encounters(ttype)
        inp = input('Press any key to continue. Enter R to reload with the same terrain type.')
        clear = lambda: os.system('cls')
        clear()
        while inp == 'r':
            td = tile_terrain_creation(ttype)
            format_tiledict(td)
            generate_encounters(ttype)
            inp = input('Press any key to continue. Enter R to reload with the same terrain type.')
            clear = lambda: os.system('cls')
            clear()
        else:
            continue
