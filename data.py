from bs4           import BeautifulSoup
from constants     import *
from drawables     import Tile


def load_map(filename, layr, resize=None, collidable=True, extra_groups=[]):
    """Loads .tmx files in csv format"""
    f = open(MAP_DIR + filename, "r")
    soup = BeautifulSoup(f, "xml")
    f.close()

    gerps       = [all_sprites_list, tile_sprites_list] + extra_groups
    mwidth      = soup.map.layer['width']
    mheight     = soup.map.layer['height']
    twidth      = int(soup.map.tileset["tilewidth"])
    theight     = int(soup.map.tileset["tileheight"])
    tsetwidth   = int(soup.map.tileset.image['width']) / twidth
    tsetheight  = int(soup.map.tileset.image['height']) / theight
    
    map_csv     = soup.map.find(attrs={'name' : layr}).data.string.split(',')

    x = 0;
    y = 0;

    if not map_csv:
        print "No Layer with name: %s" % layr
        return
        
    for num in map_csv:
        index = int(num)
        px = int(x) % int(mwidth)
        py = int(x) / int(mwidth)
        
        # indexing in .tmx files starts at 1
        # we want it to start at 0 so we 
        # subtract 1 from num
        tx = (index - 1) % tsetwidth
        ty = (index - 1) / tsetheight

        x += 1
        if index == 0:
            continue
        tile = Tile("TestTiles.png",
                        x=px, y=py,
                        w=twidth, h=theight,
                        tx=tx, ty=ty,
                        resize=resize,
                        groups=gerps)
        if not collidable:
            tile.collidable = False
