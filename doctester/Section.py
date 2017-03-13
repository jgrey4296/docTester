import spacy
import logging as root_logger
from doctester.DocException import DocException
logging = root_logger.getLogger(__name__)
from doctester.Should import Should
nlp = spacy.load('en')


class Section:
    """ An individual section of a document """
    def __init__(self,title,level):
        #the name of the section / chapter
        self.title = title
        #Any extracted tags and sections from the text
        self.level = level
        self.parentSection = None
        #paragraphs hold tags and citations fields
        self.paragraphs = []
        self.tags = set()
        self.ordered_subsections = []
        self.named_subsections = {}

    def __getattr__(self,value):
        """ Overrides the default getattr to allow something.should,
        while not breaking the typical usage of getattr """
        if value == 'should':
            return Should(self)
        else:
            raise AttributeError('{} not suitable for Section'.format(value))
        
    def extract_tags(self):
        """ Goes through the text, sentence by sentence, 
        and extracts any tags of the form %alphas% to be associated in metadata with that sentence """
        return None

    def extract_subsections(self):
        """ Goes through the text, extracting a subsection tree (as this is written for org file parsing """
        return None
        
    def add_paragraph(self,text):
        newParagraph = {'text':nlp(text), 'tags': set(), 'citations': set()}
        self.paragraphs.append(newParagraph)
        return newParagraph

    def section(self,value):
        """ Get a subsection of a section """
        if value in self.sections:
            return self.sections[value]
        else:
            raise DocException("Subsection not found",missing=value)

    
