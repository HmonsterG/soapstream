import requests, json, urllib.parse

class Yts:
    """ YTS API Class to retrieve magnet urls for a given query """
    def __init__(self, query, page=1, quality="1080p", sort_by="rating"):
        self.trackers = [
            "udp://open.demonii.com:1337/announce",
            "udp://tracker.openbittorrent.com:80",
            "udp://tracker.coppersurfer.tk:6969",
            "udp://glotorrents.pw:6969/announce",
            "udp://tracker.opentrackr.org:1337/announce",
            "udp://torrent.gresille.org:80/announce",
            "udp://p4p.arenabg.com:1337",
            "udp://tracker.leechers-paradise.org:6969"
        ]
        self.movie_data = []
        
        url = "https://yts.mx/api/v2/list_movies.json"
        params = {
                "query_term": query,
                "page": str(page), 
                "quality": quality, 
                "sort_by": sort_by
            }
        movies = requests.get(url, params).json()["data"]["movies"]
        self.movie_data = (self.construct_magnets(movies[0]["torrents"], movies[0]["title"]))
        
    def construct_magnets(self, torrents: list[dict], name: str, tracker_amt=3) -> list[tuple]:
        magnets = []
        magnet_parts = ["magnet:?xt=urn:btih:", "&dn=", "&tr="]
        """ Create magnet URL from hash and add trackers """
        for torrent in torrents:
            magnet_base = magnet_parts[0] + str(torrent["hash"]) + magnet_parts[1] + urllib.parse.quote_plus(str(name))
            
            magnet_tracked = magnet_base
            for i in range(tracker_amt):
                magnet_tracked += magnet_parts[2] + str(self.trackers[i])
                
            """ Provide simple metadata from webrequest """
            data = {
                "name": str(name), 
                "quality": str(torrent["quality"]),
                "codec": str(torrent["video_codec"]),
                "bytes": str(torrent["size_bytes"])
            }
            
            magnets.append((data, magnet_tracked))
        
        return magnets
    
    @property
    def data(self): return self.movie_data