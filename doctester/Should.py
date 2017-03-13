"""
	Defines Should Variants that enable chaining assertion syntax
"""
import logging as root_logger
from doctester.DocException import DocException
logging = root_logger.getLogger(__name__)


class Should:
    """ Should is a stateful chain of tests that when it passes is silent,
    and when it fails raises a DocException """
    def __init__(self, ref):
        self.ref = ref
        self.state = {}
        #raise Exception("Can't call {} on a should chain".format(name))

    def __getattr__(self, value):
        non_terminals = "have a near come after use".split(r' ')
        if value in non_terminals:
            #non-terminals just return the should again for chaining
            return self
        elif value == 'length':
            return self._length()
        elif value == 'subsections':
            return self._subsections
        else:
            raise AttributeError('{} not suitable in a should'.format(value))

    #Terminals:
    def mention(self, reference):
        """ Check for a specific string in the specified section """
        if self.ref.mentions(reference):
            return self
        else:
            raise DocException("No mention found", missing=reference)

    def cite(self, citation):
        """ Check for a citation in the section's citation set """
        citation_set = self.ref.get_citations()
        if citation in citation_set:
            return self
        else:
            raise DocException('No Citation Found: {}'.format(citation))

    def precede(self, name):
        """ Set state for a final test """
        #go up to parent section,  ensure the ref section is before the input name
        raise DocException("No Precedence found for", missing=name)

    def section(self, name):
        """ Test for a section,  and set state to allow further chaining """
        return self.ref.section(name)


    def _subsections(self, vals):
        """ Boolean check for correct names, or corrent number, of subsections """
        if isinstance(vals, list):
            return [self.ref.section(x) for x in vals]
        elif isinstance(vals, int):
            return len(self.ref.ordered_subsections) == vals
        else:
            raise DocException("Not enough subsections found")

    def chapter(self, name):
        """ Test for a chapter,  and set the state for further chaining """
        return self.ref.chapter(name)

    def sections(self, *args):
        """ Utility to test for multiple sections """
        raise DocException("Sections not found", missing=args)

    def tag(self, tag):
        """ Test a selected Document/Section/Subsection/Paragraph/Sentence for a tag """
        raise DocException("Tag not found", missing=tag)

    def regex(self, reg):
        """ Test a selected Doc/Sec/SubSec/Para/Sentence for a regex """
        raise DocException("Regex not found", missing=reg)

    def _length(self):
        # _length instead of length to not interfere with getattr above
        return SizedShould(self.ref)


class SizedShould(Should):
    """
    A Should Variant that enables comparisons of numeric values
    """
    #Mod this as necessary
    WordsInAPage = 500

    def __getattr__(self, value):
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
        elif value == 'subsections':
            return self._subsections_len()
        else:
            raise AttributeError('{} not suitable in a should'.format(value))


    def _larger(self):
        self.state['comp'] = lambda a, b: a > b
        return self

    def _smaller(self):
        self.state['comp'] = lambda a, b: a < b
        return self

    def equal(self):
        self.state['comp'] = lambda a, b: a == b
        return self

    def least(self, value):
        self.state['comp'] = lambda a, b: a >= b
        self.state['compVal'] = value
        return self

    def most(self, value):
        self.state['comp'] = lambda a, b: a <= b
        self.state['compVal'] = value
        return self


    def than(self, value):
        #although it comes first in the chain x.should.have.length.larger.than.pages
        #actually sets up the b value in the comparison
        self.state['compVal'] = value
        return self

    #The things that can be checked for size:
    def pages(self):
        base_wordcount = self.ref.get_word_count()
        compare_to = SizedShould.WordsInAPage * self.state['compVal']
        if self.state['comp'](base_wordcount, compare_to):
            return self
        else:
            err_msg = 'Not Enough words to fulfill page count: {}/({} * {})'
            raise DocException(err_msg.format((base_wordcount,
                                               self.state['compVal'],
                                               SizedShould.WordsInAPage)))

    def paragraphs(self):
        paragraph_count = self.ref.get_paragraph_count()
        if self.state['comp'](paragraph_count, self.state['compVal']):
            return self
        else:
            err_msg = "Not Enough Paragraphs: {} / {}"
            raise DocException(err_msg.format(paragraph_count,
                                              self.state['compVal']))

    def sentences(self):
        sentence_count = self.ref.get_sentence_count()
        if self.state['comp'](sentence_count, self.state['compVal']):
            return self
        else:
            err_msg = 'Not Enough Sentences: {} / {}'
            raise DocException(err_msg.format(sentence_count,
                                              self.state['compVal']))

    def words(self):
        word_count = self.ref.get_word_count()
        if self.state['comp'](word_count, self.state['compVal']):
            return self
        else:
            raise DocException('Not Enough Words: {} / {}'.format(word_count,
                                                                  self.state['compVal']))

    def citations(self):
        cite_count = len(self.ref.get_citations())
        if self.state['comp'](cite_count, self.state['compVal']):
            return self
        else:
            err_msg = 'Not Enough Citations: {} / {}'
            raise DocException(err_msg.format(cite_count,
                                              self.state['compVal']))

    def _subsections_len(self):
        num_sections = len(self.ref.subsections)
        if self.state['comp'](num_sections, self.state['compVal']):
            return self
        else:
            err_msg = 'Not Enough Subsections: {} / {}'
            raise DocException(err_msg.format(num_sections,
                                              self.state['compVal']))
