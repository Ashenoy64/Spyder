import os

class Config:
    def __init__(self, **settings):
        # Use the project root or current working directory as base for tempDir
        base_dir = os.path.abspath(os.getcwd())
        self.tempDir = os.path.join(base_dir, settings.get('tempDir', '.temp'))
        self.dumpFile = os.path.join(self.tempDir, settings.get('dumpFile','dump.txt'))
        os.makedirs(self.tempDir, exist_ok=True)
        self.setScraperConfig(settings.get('scraper', {}))
        self.setExtractorConfig(settings.get('extractor', {}))
        self.setAIConfig(settings.get('ai', {}))

    def setScraperConfig(self, scraper):
        self.scraper = {
            'maxConcurrentBrowsers': scraper.get('maxConcurrentBrowsers', 5),
            'timeoutMs': scraper.get('timeoutMs', 60000),
            'scrapedDir': scraper.get('scrapedDir', 'scraped_pages'),
            'pageLimit': scraper.get('pageLimit', 10),
        }

    def setExtractorConfig(self, extractor):
        self.extractor = {
            'contextLength': extractor.get('contextLength', 2048),
            'concurrentExtractions': extractor.get('concurrentExtractions', 2),
            'csvDir' : extractor.get('csvDir', None),
            'csvWriter' : extractor.get('csvWriter', None)
        }

    def setAIConfig(self, ai):
        self.ai = {
            'model': ai.get('model', 'default-model'),
            'apiKey': ai.get('apiKey', ''),
            'host': ai.get('host', ''),
            'function': ai.get('function', ''),
        }