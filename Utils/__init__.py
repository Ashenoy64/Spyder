import os


class Config:
    def __init__(self, **kwargs):
        self.tempDir = kwargs.get('tempDir', os.path.join(os.path.dirname(__file__), '.temp'))
        os.makedirs(self.tempDir, exist_ok=True)
        
        # Scraper settings
        self.maxConcurrentBrowsers = kwargs.get('maxConcurrentBrowsers', 5)
        self.timeoutMs = kwargs.get('timeoutMs', 60000)
        self.scrapedDir = os.path.join(self.tempDir,kwargs.get('scrapedDir', 'scraped_pages'))
        self.pageLimit = kwargs.get('pageLimit', 50)
        pass
