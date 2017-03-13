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
        elif value == 'length':
            return self._length()
        else:
            raise AttributeError('{} not suitable in a should'.format(value))

    #Terminals:
    def mention(self,reference):
        """ Check for a citation in the specified section """
        if self.ref.mentions(reference):
            return self
        else:        
            raise DocException("No mention found",missing=reference)

    def cite(self,citation):
        citation_set = self.ref.get_citations()
        if citation in citation_set:
            return self
        else:
            raise DocException('No Citation Found: {}'.format(citation))
    
    def precede(self,name):
        """ Set state for a final test """
        #go up to parent section, ensure the ref section is before the input name
        raise DocException("No Precedence found for",missing=name)

    def section(self,name):
        """ Test for a section, and set state to allow further chaining """
        return self.ref.section(name)


    def subsections(self,vals):
        if isinstance(vals,list):
            return [self.ref.section(x) for x in vals]
        elif isinstance(vals,int):
            return len(self.ref.ordered_subsections) == vals
        else:
            raise DocException("Not enough subsections found")
    
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

    def than(self,value):
        """ Test a should state agaisnt a value """
        raise DocException('Than value fail')

    def _length(self):
        # _length instead of length to not interfere with getattr above
        return SizedShould(self.ref)
    

class SizedShould(Should):
    #Mod this as necessary
    WordsInAPage = 500
    
    """ An alternative should for ranges of values, mainly length """
    def __init__(self,ref):
        self.ref = ref
        self.state = {}

    def __getattr__(self,value):
        non_terminals = "than at".split(r' ')
        if value in non_terminals:
            #non-terminals just return the should again for chaining
            return self
        elif value == 'larger':
            return self._larger()
        elif value == 'smaller':
            return self._smaller()
        elif value == 'equal':
            return self._equal()
        else:
            raise AttributeError('{} not suitable in a should'.format(value))

        
    def _larger(self):
        self.state['comp'] = lambda a,b: a > b
        return self

    def _smaller(self):
        self.state['comp'] = lambda a,b: a < b
        return self

    def equal(self):
        self.state['comp'] = lambda a,b: a == b
        return self

    def least(self,value):
        self.state['comp'] = lambda a,b : a >= b
        self.state['compVal'] = value
        return self

    def most(self,value):
        self.state['comp'] = lambda a,b : a <= b
        self.state['compVal'] = value
        return self

    
    def than(self,value):
        #although it comes first in the chain x.should.have.length.larger.than.pages
        #actually sets up the b value in the comparison
        self.state['compVal'] = value
        return self

    
