"""
	Defines the Document class, top level collection of texts
"""
import logging as root_logger
from os.path import join, isdir, splitext
from os import listdir
from doctester.DocException import DocException
from doctester.Should import Should
from doctester.TextParser import parseText
logging = root_logger.getLogger(__name__)

class Document:
    """ Top level document, loads files, sorts them into chapters,
    and allows access to 'should' testing """
    FILETYPE = '.org'


    def __init__(self, directory):
        """ Given a directory, load in all files of FILETYPE, and create indiv chapters for them """
        if not isdir(directory):
            raise Exception("Bad Directory Specification: {}".format(directory))
        read_files = listdir(directory)
        org_files = [x for x in read_files if splitext(x)[1] == Document.FILETYPE]
        self.directory = directory
        self.files = org_files
        self.chapters = {}
        #Actually read in all found files
        self.read_files()

    def __getattr__(self, value):
        #allows doc.should, instead of doc.should()
        #while retaining doc.read_files()
        if value == 'should':
            return Should(self)
        else:
            raise AttributeError('{} Not Suitable for Document'.format(value))

    def read_files(self):
        for file in self.files:
            fullpath = join(self.directory, file)
            title = splitext(file)[0]
            with open(fullpath, 'r') as f:
                text = f.read()
            #chapters are the same ds as sections
            self.chapters[title.lower().strip()] = parseText(text)

    def chapter(self, name):
        #Get a chapter from the document, use the same error as 'should'ing if it fails
        fname = name.lower().strip()
        if fname in self.chapters:
            return self.chapters[fname]
        else:
            raise DocException("No Chapter Found", missing=name)

    def get_word_count(self):
        return sum([x.get_word_count() for x in self.chapters.values()])

    def get_sentence_count(self):
        return sum([x.get_sentence_count() for x in self.chapters.values()])

    def get_paragraph_count(self):
        return sum([x.get_paragraph_count() for x in self.chapters.values()])

    def get_citations(self):
        """ Get the Union of all citation sets of all sub chapters/sections """
        base_set = set()
        citation_sets = [x.get_citations() for x in self.chapters.values()]
        for chapter in citation_sets:
            base_set = base_set.union(chapter)
        return base_set

    def mentions(self, reference):
        """ Test for a literal string in the documents chapters/sections """
        for chapter in self.chapters.values():
            if chapter.mentions(reference):
                return True
        return False
