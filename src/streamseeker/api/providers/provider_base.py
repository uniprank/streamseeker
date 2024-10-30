from streamseeker.api.core.classes.base_class import BaseClass

class ProviderBase(BaseClass):
    name = None
    title = None
    priority = 9999
    cache_attemps = 0

    def get_name(self):
        return self.name
    
    def get_title(self):
        return self.title
    
    def get_priority(self):
        return self.priority

    def get_download_url(self, url):
        raise NotImplementedError("getDownloadUrl() must be implemented")

    def download(self, url):
        raise NotImplementedError("download() must be implemented") 