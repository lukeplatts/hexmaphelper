import random

water = [9, 1, 1, 6, 3, 1, 0]
swamp = [1, 9, 0, 6, 3, 0, 0]
desert = [1, 0, 9, 3, 0, 6, 1]
plains = [1, 1, 1, 9, 6, 3, 0]
forest = [1, 1, 0, 6, 9, 3, 1]
hills = [1, 0, 1, 3, 1, 9, 6]
mountain = [0, 0, 1, 0, 3, 6, 9]

terrtypes = ['water', 'swamp', 'desert', 'plains', 'forest', 'hills', 'mountain']
terrvalues = [water, swamp, desert, plains, forest, hills, mountain]

terraindict = {}
for terrtype1 in terrtypes:
    terraindict[terrtype1] = {}
    for terrtype2 in terrtypes:
        terraindict[terrtype1][terrtype2] = terrvalues[terrtypes.index(terrtype1)][terrtypes.index(terrtype2)]


def tileroll(optionslist, chance=None):
    """
    Rolls randomly to determine a tile.
    :param: optionslist - list of tile options.
    :param: chance - list of chance for each tile in the list. Must add to <= 1, and be in same order as optionslist.

    :returns: Tile option from optionslist
    """
    # If no probabilities are given, divide 1 by the number of elements in the list.
    if chance is None:
        chance = [(1 / len(optionslist))] * len(optionslist)
    # Check that probabilities are <= 1.
    listsum = 0
    for element in chance:
        listsum += element
    if listsum > 1:
        raise SyntaxError('List of probabilities must be <= 1.')
    tile = None
    # Generate roll.
    randnum = random.random()
    elementcount = 0
    probcumulative = 0
    # Compare random roll to probability.
    for prob in chance:
        if randnum <= prob:
            tile = optionslist[elementcount]
        else:
            elementcount += 1
            probcumulative += prob
    if tile is None:
        tile = optionslist[-1]
    return tile


def tile_terrain_creation(terrtype):
    """
    Creates a dictionary containing the number of tiles that a terrain hex should have from a given terrain type.
    """
    if terrtype not in terrtypes:
        raise TypeError(f'Terrain type {terrtype} not accepted.')
    # Reset Rolls.
    roll = None
    # Create initial dictionary for tile.
    tiledict = {'water': 0, 'swamp': 0, 'desert': 0, 'plains': 0, 'forest': 0, 'hills': 0, 'mountain': 0}

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
            tiledict[wildcard] += 1

    # Assign tiles to tiledict.
    tiledict[primary] = terraindict[terrtype][primary]
    tiledict[secondary] = terraindict[terrtype][secondary]
    tiledict[tertiary] = terraindict[terrtype][tertiary] - wldcrdx

    # Water Terrain Tile Special Cases
    if terrtype == 'water':
        # Roll for light vs heavy forest.
        lightforest, heavyforest = 0, 0
        for i in range(tiledict['forest']):
            roll = tileroll([1, 2], [0.66])
            if roll == 1:
                lightforest += 1
            elif roll == 2:
                heavyforest += 1
        tiledict['forest'] -= (lightforest + heavyforest)
        tiledict['lightforest'] = lightforest
        tiledict['heavyforest'] = heavyforest

    # Desert Terrain Tile Special Cases
    if terrtype == 'desert':
        # Roll for Hills Modifier
        modhills, rockdesert, highdunes = 0, 0, 0
        for i in range(terraindict["desert"]["hills"]):
            roll = tileroll([1, 2], [0.33])
            if roll == 1:
                modhills += 1
                if tileroll([1, 2], [0.5]) == 1:
                    rockdesert += 1
                else:
                    highdunes += 1
        if modhills > 0:
            tiledict['hills'] -= (rockdesert + highdunes)
            tiledict['rockdesert'] = rockdesert
            tiledict['highdunes'] = highdunes

    # Plains Terrain Tile Special Cases
    if terrtype == 'plains':
        pass
        # Determine if tile is 'settled' and then set plains as farmland.

    # Forest Terrain Tile Special Cases
    if terrtype == 'forest':
        # Roll for light vs heavy forest.
        lightforest, heavyforest = 0, 0
        for i in range(tiledict['forest']):
            roll = tileroll([1, 2], [0.66])
            if roll == 1:
                lightforest += 1
            elif roll == 2:
                heavyforest += 1
        tiledict['forest'] -= (lightforest + heavyforest)
        tiledict['lightforest'] = lightforest
        tiledict['heavyforest'] = heavyforest

        # Roll for forested hills vs grassy hills.
        forestedhills = 0
        for i in range(tiledict['hills']):
            roll = tileroll([1, 2], [0.66])
            if roll == 1:
                forestedhills += 1
        if forestedhills > 0:
            tiledict['forestedhills'] = forestedhills
            tiledict['hills'] -= forestedhills

        # Roll for forested mountains vs mountains.
        # Determine if mountain wildcard has been generated.
        if tiledict['mountain'] > 0:
            forestedmountain = 0
            for i in range(int(tiledict['mountain'])):
                roll = tileroll([1, 2], [0.66])
                if roll == 1:
                    forestedmountain += 1
            if forestedmountain > 0:
                tiledict['forestedmountain'] = forestedmountain
                tiledict['mountain'] -= forestedmountain

    # Hills Terrain Tile Special Cases
    if terrtype == 'hills':
        # Roll for Forested Hills
        if tiledict['forest'] > 0:
            forestedhill = 0
            for i in range(int(tiledict['forest'])):
                roll = tileroll([1, 2], [0.33])
                if roll == 1:
                    forestedhill += 1
            if forestedhill > 0:
                tiledict['forestedhill'] = forestedhill
                tiledict['forest'] -= forestedhill
        # Roll for Canyon or Fissure
        canyon = 0
        for i in range(int(tiledict['hills'])):
            roll = tileroll([1, 2], [0.2])
            if roll == 1:
                canyon += 1
        if canyon > 0:
            tiledict['canyon'] = canyon
            tiledict['hills'] -= canyon
        # Roll for Mountain Pass
        mpass = 0
        for i in range(int(tiledict['mountain'])):
            roll = tileroll([1, 2], [0.4])
            if roll == 1:
                mpass += 1
        if mpass > 0:
            tiledict['mpass'] = mpass
            tiledict['mountain'] -= mpass

    # Mountains Terrain Tile Special Cases
    if terrtype == 'mountain':
        # Roll for Forested Mountain
        forestedmnt = 0
        for i in range(int(tiledict['forest'])):
            roll = tileroll([1, 2], [0.33])
            if roll == 1:
                forestedmnt += 1
        if forestedmnt > 0:
            tiledict['forestedmnt'] = forestedmnt
            tiledict['forest'] -= forestedmnt
        # Roll for Peak, Pass, or Volcano
        mpeak, mpass, mvol = 0, 0, 0
        for i in range(int(tiledict['mountain'])):
            roll = tileroll([1, 2, 3, 4], [0.2, 0.1, 0.05])
            if roll == 1:
                mpeak += 1
            elif roll == 2:
                mpass += 1
            elif roll == 3:
                mvol += 1
        tiledict['mountain'] -= (mpeak + mpass + mvol)
        tiledict['mpeak'] = mpeak
        tiledict['mpass'] = mpass
        tiledict['mvol'] = mvol

    return tiledict


def format_tiledict(tiledict):
    """
    Recieves a dictonary of tile numbers, trims the empty values, and prints the number
    of each tile in an easily readable format.

    :param: tiledict
    Dictionary of tiles from tile_terrain_creation() function.
    """

    pass


if __name__ == '__main__':
    # terrtype = input('What is the terrain type?: ')
    # tile_terrain_creation(terrtype)
    for ttype in terrtypes:
        print(tile_terrain_creation(ttype))
