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

    def add_subsection(self,title,level):
        ftitle = title.lower().strip()
        newSection = Section(ftitle,level)
        newSection.parentSection = self
        self.ordered_subsections.append(newSection)
        self.named_subsections[ftitle] = newSection
        return newSection        

    def get_parent(self):
        return self.parentSection

    def add_tag(self,text):
        ftext = text.lower().strip()
        self.tags.add(ftext)

    def has_tag(self,text):
        ftext = text.lower().strip()
        return ftext in self.tags

    def add_paragraph(self,text):
        newParagraph = {'text':nlp(text), 'tags': set(), 'citations': set()}
        self.paragraphs.append(newParagraph)
        return newParagraph

    def get_paragraphs(self):
        return self.paragraphs

    def get_all_paragraphs(self):
        initial = self.paragraphs.copy()
        initial.extend([x for ss in self.ordered_subsections for x in ss.get_all_paragraphs()])
        return initial
    
    def section(self,value):
        """ Get a subsection of a section """
        fvalue = value.lower().strip()
        if fvalue in self.named_subsections:
            return self.named_subsections[fvalue]
        else:
            raise DocException("Subsection not found",missing=value)

    def get_sentence_count(self):
        base_count = 0
        base_count += sum([len(list(x['text'].sents)) for x in self.paragraphs])
        base_count += sum([x.get_sentence_count() for x in self.ordered_subsections])
        return base_count
        
    def get_word_count(self):
        base_count = 0
        base_count += sum([len(x['text']) for x in self.paragraphs])
        base_count += sum([x.get_word_count() for x in self.ordered_subsections])
        return base_count        

    def get_paragraph_count(self):
        base_count = len(self.paragraphs)
        base_count += sum([x.get_paragraph_count() for x in self.ordered_subsections])
        return base_count
        
    def get_citations(self):
        base_set = set()
        paragraph_sets = [x['citations'] for x in self.paragraphs]
        subsection_sets = [x.get_citations() for x in self.ordered_subsections]
        base_set = base_set.union(*paragraph_sets, *subsection_sets)
        return base_set
    
    def mentions(self,reference):
        for paragraph in self.paragraphs:
            if reference in paragraph['text'].text:
                return True
        for section in self.ordered_subsections:
            if section.mentions(reference):
                return True

        return False
            
    

        
