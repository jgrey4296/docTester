from doctester.DocException import DocException
import logging as root_logger
logging = root_logger.getLogger(__name__)


class Should:
    """ Should is a stateful chain of tests that when it passes is silent,
    and when it fails raises a DocException """
    def __init__(self,ref):
        self.ref = ref
        self.state = {}
        #raise Exception("Can't call {} on a should chain".format(name))

    def __getattr__(self,value):
        non_terminals = "have a near come after use".split(r' ')
        if value in non_terminals:
            #non-terminals just return the should again for chaining
            return self
        else:
            raise AttributeError('{} not suitable in a should'.format(value))

    #Terminals:
    def mention(self,reference):
        """ Check for a citation in the specified section """
        raise DocException("No mention found",missing=reference)

    def precede(self,name):
        """ Set state for a final test """
        raise DocException("No Precedence found for",missing=name)

    def section(self,name):
        """ Test for a section, and set state to allow further chaining """
        raise DocException("No section found",missing=name)

    def chapter(self,name):
        """ Test for a chapter, and set the state for further chaining """
        return self.ref.chapter(name)
    
    def sections(self,*args):
        """ Utility to test for multiple sections """
        raise DocException("Sections not found",missing=args)
    
    def tag(self,tag):
        """ Test a selected Document/Section/Subsection/Paragraph/Sentence for a tag """
        raise DocException("Tag not found",missing=tag)

    def regex(self,reg):
        """ Test a selected Doc/Sec/SubSec/Para/Sentence for a regex """
        raise DocException("Regex not found",missing=reg)

    def length(self,value):
        raise DocException("Length not found")
    

class SizedShould(Should):
    """ An alternative should for ranges of values, mainly length """
    def __init__(self,ref):
        self.ref = ref
        self.state = {}

    def larger(self):
        return self

    def smaller(self):
        return self

    def equal(self,value):
        return self
    
    def than(self):
        return self

    
