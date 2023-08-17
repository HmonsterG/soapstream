import mimetypes, tempfile
import libtorrent as lt
from functools import cached_property

"""
Credit to XayOn's Torrentstream 
application which gave me the idea
of how to get media types with 
mimetype
https://github.com/XayOn/torrentstream/
"""

mimetypes.init()

#Thanks XayOn for these 
PORTS = (1024, 1096) #Should be randomised
DHT = (("router.utorrent.com", 6881), ("router.bittorrent.com", 6881), ("dht.transmissionbt.com", 6881), ("router.bitcomet.com", 6881), ("dht.aelitis.com", 6881))
EXTENSIONS = ('ut_pex', 'ut_metadata', 'smart_ban', 'metadata_transfoer')

class Torrent:
    """
    TorrentSession and Torrent compressed
    into one class for simplicity and 
    functions I won't need removed, 
    again thanks to XayOn
    """
    def __init__(self, magnet: str):
        self.session = lt.session()
        self.session.set_severity_level(lt.alert.severity_levels.critical)
        self.session.listen_on(*PORTS)
        for extension in EXTENSIONS:
            self.session.add_extension(extension)
        
        self.session.start_dht()
        self.session.start_lsd()
        self.session.start_upnp()
        self.session.start_natpmp()
        
        for router in DHT:
            self.session.add_dht_router(*router)
        
        self.directory = tempfile.TemporaryDirectory()
        self.params = {
            "save_path": self.directory,
            "storage_mode": lt.storage_mode_t.storage_mode_sparse
        }
        self.handle = None
        
    def __enter__(self):
        self.handle = lt.add_magnet_uri()
        self.handle.set_sequential_download(True)
        
        return self
        
    def __exit__(self):
        self.directory.cleanup()
        
    def __iter__(self):
        return iter(self.files)
        
    @property
    def torrent_info(self):
        return self.handle.get_torrent_info()
        
    @cached_property
    def files(self) -> list[File]:
        return [File(self, i) for i in range(len(self.torrent_info.files()))]
    
    def download_only(self, file: str) -> str:
        if file not in self.files:
            return None
        for f in self.files:
            file.priority = 7 if file == f else 0
        return file

class File:
    """
    Highly debloated version of XayOn's
    TorrentFile class with only media 
    checking methods
    """
    def __init__(self, parent, index: int):
        self.torrent = parent
        self.handle = parent.handle
        self.index = index
        
    @cached_property
    def mime_type(self):
        return mimetypes.guess_type(self.path)[0] or None
    
    @cached_property
    def is_video(self) -> bool:
        return any(self.mime_type.startswith('video'))
        
    @cached_property
    def path(self):
        return self.handle.get_torrent_info().files.path