"""
	The Main Section class to hold text, references and tags
"""
import logging as root_logger
import spacy
from doctester.DocException import DocException
from doctester.Should import Should

logging = root_logger.getLogger(__name__)
NLP = spacy.load('en')


class Section:
    """ An individual section of a document """
    def __init__(self, title, level):
        #the name of the section / chapter
        self.title = title
        #Any extracted tags and sections from the text
        self.level = level
        self.parent_section = None
        #paragraphs hold tags and citations fields
        self.paragraphs = []
        self.tags = set()
        self.ordered_subsections = []
        self.named_subsections = {}

    def __getattr__(self, value):
        """ Overrides the default getattr to allow something.should,
        while not breaking the typical usage of getattr """
        if value == 'should':
            return Should(self)
        else:
            raise AttributeError('{} not suitable for Section'.format(value))

    def is_section(self):
        return True

    def is_document(self):
        return False

    def add_subsection(self, title, level):
        """ Add a new subsection to the current section, or a set indentation level """
        ftitle = title.lower().strip()
        new_section = Section(ftitle, level)
        new_section.set_parent(self)
        self.ordered_subsections.append(new_section)
        self.named_subsections[ftitle] = new_section
        return new_section

    def get_parent(self):
        return self.parent_section

    def set_parent(self,ref):
        if self.parent_section is not None:
            raise Exception('Attempting to redefine parent section')
        else:
            self.parent_section = ref
    
    def add_tag(self, text):
        ftext = text.lower().strip()
        self.tags.add(ftext)

    def has_tag(self, text):
        ftext = text.lower().strip()
        return ftext in self.tags

    def add_paragraph(self, text):
        new_paragraph = {'text':NLP(text), 'tags': set(), 'citations': set()}
        self.paragraphs.append(new_paragraph)
        return new_paragraph

    def get_paragraphs(self):
        return self.paragraphs

    def get_all_paragraphs(self):
        initial = self.paragraphs.copy()
        initial.extend([x for ss in self.ordered_subsections for x in ss.get_all_paragraphs()])
        return initial

    def section(self, value):
        """ Get a subsection of a section """
        fvalue = value.lower().strip()
        if fvalue in self.named_subsections:
            return self.named_subsections[fvalue]
        else:
            raise DocException("Subsection not found", missing=value)

    def get_sentence_count(self):
        """ Get the total sentence count of this sections paragraphs,
        and sub-sections sentence counts """
        base_count = 0
        base_count += sum([len(list(x['text'].sents)) for x in self.paragraphs])
        base_count += sum([x.get_sentence_count() for x in self.ordered_subsections])
        return base_count

    def get_word_count(self):
        """ Get the total word count of paragraphs + subsections """
        base_count = 0
        base_count += sum([len(x['text']) for x in self.paragraphs])
        base_count += sum([x.get_word_count() for x in self.ordered_subsections])
        return base_count

    def get_paragraph_count(self):
        """ Get the total paragraph count of this section + subsections """
        base_count = len(self.paragraphs)
        base_count += sum([x.get_paragraph_count() for x in self.ordered_subsections])
        return base_count

    def get_citations(self):
        """ Get the union set of all citations in paragraphs + subsections """
        base_set = set()
        paragraph_sets = [x['citations'] for x in self.paragraphs]
        subsection_sets = [x.get_citations() for x in self.ordered_subsections]
        base_set = base_set.union(*paragraph_sets, *subsection_sets)
        return base_set

    def mentions(self, reference):
        """ Check for a string literal in the text of the section + subsections """
        for paragraph in self.paragraphs:
            if reference in paragraph['text'].text:
                return True
        for section in self.ordered_subsections:
            if section.mentions(reference):
                return True

        return False
