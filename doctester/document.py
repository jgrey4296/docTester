import logging as root_logger
from os.path import join,isfile,exists,isdir, splitext
from os import listdir
from doctester.DocException import DocException
from doctester.Section import Section
from doctester.Should import Should
logging = root_logger.getLogger(__name__)

class Document:
    """ Top level document, loads files, sorts them into chapters,
    and allows access to 'should' testing """
    FILETYPE = '.org'

    
    def __init__(self,directory):
        """ Given a directory, load in all files of FILETYPE, and create indiv chapters for them """
        read_files = listdir(directory)
        org_files = [x for x in read_files if splitext(x)[1] == Document.FILETYPE]
        self.directory = directory
        self.files = org_files
        self.chapters = {}
        #Actually read in all found files
        self.read_files()

    def __getattr__(self,value):
        #allows doc.should, instead of doc.should()
        #while retaining doc.read_files()
        if value == 'should':
            return Should(self)
        else:
            raise AttributeError('{} Not Suitable for Document'.format(value))
        
    def read_files(self):
        for x in self.files:
            fullpath = join(self.directory,x)
            title = splitext(x)[0]
            with open(fullpath,'r') as f:
                text = f.read()
            #chapters are the same ds as sections
            self.chapters[title] = Section(title,text)

    def chapter(self,name):
        #Get a chapter from the document, use the same error as 'should'ing if it fails
        if name in self.chapters:
            return self.chapters[name]
        else:
            raise DocException("No Chapter Found",missing=name)
