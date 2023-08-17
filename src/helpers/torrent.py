import mimetypes, tempfile
import libtorrent as lt

"""
Credit to XayOn's Torrentstream 
application which gave me the idea
of how to get media types with 
mimetype
https://github.com/XayOn/torrentstream/
"""


class Torrent:
    def __init__(self, magnet: str):
        self.directory = tempfile.TemporaryDirectory()
        self.params = {
            "save_path": self.directory,
            "storage_mode": lt.storage_mode_t.storage_mode_sparse
        }
        
    def get_files(self) -> list[File]:
        return [File(self, i) for i in range(len(self.torrent_info.files()))]

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