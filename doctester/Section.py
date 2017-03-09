import spacy
import logging as root_logger
logging = root_logger.getLogger(__name__)
from doctester.Should import Should

nlp = spacy.load('en')

class Section:
    """ An individual section of a document """
    def __init__(self,title,text):
        self.title = title
        self.text = nlp(text)
        self.tags = {}
        self.sections = {}
        
    def extract_tags(self):
        return None

    def extract_subsections(self):
        return None
        
    def should(self):
        return None

