from helpers.torrent import Torrent
from sources.yts import Yts

#Debugging to test downloading of a torrent from YTS with helper functions
if __debug__:
    y = Yts("requiem for a dream")
    print(y.data)