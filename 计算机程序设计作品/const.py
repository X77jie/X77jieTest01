class BlockType: 
    RED=0
    ORANGE=1
    YELLOW=2
    GREEN=3
    PURPLE=4
    BLUE=5
    BLOCKMAX=6

class BlockGroupType:
    FIXED=0
    DROP=1


BLOCK_RES={
    BlockType.RED:"red.png",
    BlockType.ORANGE:"orange.png",
    BlockType.YELLOW:"yellow.png",
    BlockType.GREEN:"green.png",
    BlockType.PURPLE:"purple.png",
    BlockType.BLUE:"blue.png",
}


GAME_ROW=17
GAME_COL=10

BLOCK_SIZE_W=32
BLOCK_SIZE_H=32

GAME_WIDTH_SIZE=800
GAME_HEIGHT_SIZE=600


BLOCK_SHAPE =[[((0,0),(0,1),(1,0),(1,1)),],
              [((0,0),(0,1),(0,2),(0,3)),((0,0),(1,0),(2,0),(3,0))],
              [((0,0),(0,1),(1,1),(1,2)),((0,1),(1,0),(1,1),(2,0))],
              [((0,1),(1,0),(1,1),(1,2)),((0,1),(1,1),(1,2),(2,1)),((1,0),(1,1),(1,2),(2,1)),((0,1),(1,0),(1,1),(2,1))],
              ]