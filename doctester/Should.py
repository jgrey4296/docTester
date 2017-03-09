from doctester.DocException import DocException

class Should:
    """ Should is a stateful chain of tests that when it passes is silent,
    and when it fails raises a DocException """
    def __init__(self,ref):
        self.ref = ref
        self.state = {}
        
    def __getattr__(self,name):
        non_terminals = "have a near come after use".split(r' ')
        if name in non_terminals:
            #non-terminals just return the should again for chaining
            return self
        elif hasattr(self,name):
            #terminals return the appropriate method to call
            return getattr(super(self),val)
        else:
            raise Exception("Can't call {} on a should chain".format(name))

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

    def sections(self,*args):
        """ Utility to test for multiple sections """
        raise DocException("Sections not found",missing=args)
    
    def tag(self,tag):
        """ Test a selected Document/Section/Subsection/Paragraph/Sentence for a tag """
        raise DocException("Tag not found",missing=tag)

    def regex(self,reg):
        """ Test a selected Doc/Sec/SubSec/Para/Sentence for a regex """
        raise DocException("Regex not found",missing=reg)
    
    

class SizedShould(Should):
    """ An alternative should for ranges of values, mainly length """
    def __init__(self,ref):
        self.ref = ref
        self.state = {}

    def larger(self):
        return self

    def smaller(self):
        return self

    def equal(self,value)
    
    def than(self):
        return self

    
