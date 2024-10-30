import time

from streamseeker.api.core.classes.base_class import BaseClass

from streamseeker.api.providers.providers import Providers
from streamseeker.api.streams.streams import Streams
from streamseeker.api.streams.stream_base import StreamBase


class StreamseekerHandler(BaseClass):
    def __init__(self, config: dict={}):
        super().__init__()
        self._providers = Providers()
        self._streams = Streams()
        self.config = config

        self.config.update({"preferred_provider": config.get("preferred_provider", "voe")})
        self.config.update({"output_folder": config.get("output_folder", "downloads")})
        self.config.update({"output_folder_year": config.get("output_folder_year", False)})
        self.config.update({"ddos_counter": config.get("ddos_counter", 0)})
        self.config.update({"ddos_limit": config.get("ddos_limit", 5)})
        self.config.update({"ddos_timer": config.get("ddos_timer", 60)})
        self.config.update({"overwrite": config.get("overwrite", False)})

        # example
        # stream = self._streams.get("aniworldto")
        # stream.set_config(self.config)
        # response = stream.search("naruto")
        # logger.info(f"Stream response: {response}")

        # self.download("single", "aniworldto", "voe", "naruto", "german", "staffel", 1, 2)
    
    def streams(self):
        return self._streams.get_all()
    
    def providers(self):
        return self._providers.get_all()
    
    def search(self, stream_name: str, name: str):
        stream = self._streams.get(stream_name)
        stream.set_config(self.config)
        return stream.search(name)
    
    def search_query(self, stream_name: str, search_term: str):
        stream = self._streams.get(stream_name)
        stream.set_config(self.config)
        return stream.search_query(search_term)
    
    def search_episodes(self, stream_name: str, name: str, type: str, season: int):
        stream = self._streams.get(stream_name)
        stream.set_config(self.config)
        return stream.search_episodes(name, type, season)

    # download_type: [all, only_season, single]
    # stream_name: [aniworldto, sto, ...]
    # preferred_provider: [voe, streamtape, ...]
    # name: [naruto]
    # language: [german, japanese-english, ...]
    # type: [series, movie, ...] stream specific
    # season: [1, 2, 3, ...] (default: 0) Start from
    # episode [1, 2, 3, ...] (default: 0) Start from
    def download(self, download_type: str, stream_name: str, preferred_provider: str, name: str, language: str, type: str, season: int=0, episode: int=0):
        stream = self._streams.get(stream_name)
        stream.set_config(self.config)

        if stream is None:
            return None
        
        threads = []
        match download_type:
            case "all":
                threads = self._all_download(stream, preferred_provider, name, language, type, season, episode)
            # case "only_season":
            #     self._season_download(stream, preferred_provider, name, language, type, season, episode)
            case "single":
                downloader = stream.download(name, preferred_provider, language, type, season, episode)
                downloader.join()
                return
                # while downloader.is_alive():
                #     time.sleep(1)
            case _:
                return None
            
        for thread in threads:
            thread.join()
    
    def _all_download(self, stream: StreamBase, preferred_provider: str, name: str, language: str, type: str, season: int, episode: int):
        seasons = stream.search_seasons(name, type)
        if season > 0:
            # remove all seasons before the given season
            seasons = [e for e in seasons if e >= season]
        
        threads = []
        for season in seasons:
            sub_threads = self._season_download(stream, preferred_provider, name, language, type, season, episode)
            episode = 0
            threads.extend(sub_threads)

    def _season_download(self, stream: StreamBase, preferred_provider: str, name: str, language: str, type:str, season:int, episode: int=0):
        match type:
            case "staffel":
                episodes = stream.search_episodes(name, season)
                if episodes is None:
                    return None
            case _:
                episodes = [0]
        
        if episode > 0:
            # remove all episodes before the given episode
            episodes = [e for e in episodes if e >= episode]
        
        threads = []
        for episode in episodes:
            if self.ddos_counter >= self.config.get("ddos_limit"):
                self.line(f"<warning>DDOS limit reached. Waiting for {self.config.get('ddos_timer')} seconds.</warning>")
                time.sleep(self.config.get("ddos_timer"))
                self.ddos_counter = 0

            response = stream.download(name, preferred_provider, language, type, season, episode)
            if response is None:
                continue

            threads.append(response)

            self.ddos_counter += 1
        
        return threads
    