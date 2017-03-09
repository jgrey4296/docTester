import logging as root_logger
from os.path import join,isfile,exists,isdir, splitext
from os import listdir
from doctester.DocException import DocException
from doctester.Section import Section
from doctester.Should import Should
logging = root_logger.getLogger(__name__)

class Document:
    """ Top level document, loads files, sorts them into sections,
    and allows access to should testing """
    
    def __init__(self,directory):
        read_files = listdir(directory)
        org_files = [x for x in read_files if splitext(x)[1] == '.org']
        self.directory = directory
        self.files = org_files
        self.data = {}

        self.read_files()

    def __getattr__(self,value):
        if value == 'should':
            return Should(self)
        else:
            return getattr(super(self),value)
        
    def read_files(self):
        for x in self.files:
            fullpath = join(self.directory,x)
            title = splitext(x)[0]
            with open(fullpath,'r') as f:
                text = f.read()
            self.data[title] = Section(title,text)

    def chapter(self,name):
        if name in self.data:
            return self.data[name]
        else:
            raise DocException("No Chapter Found",missing=name)
