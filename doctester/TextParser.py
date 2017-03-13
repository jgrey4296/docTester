import logging as root_logger
logging = root_logger.getLogger(__name__)
import pyparsing as pp
from pyparsing import pyparsing_common as ppc
from collections import namedtuple
import re
from doctester.Section import Section
import IPython
# Group, Suppress, ParseResults, Forward
# OnlyOnce, , FollowedBy, NotAny, OneOrMore, ZeroOrMore, Optional, SkipTo, Combine, Dict
# And, Each, MatchFirst, Or, CharsNotIn, Empty, Keyword, CaselessKeyword, Literal, CaselessLiteral,
# NoMatch, QuotedString, Regex, White, Word

# PARSER.setParseAction(lambda toks: toks))
# PARSER.setResultsName('')
# PARSER.parseString('')

#Tuples:
HEADER = namedtuple('Header','level title')
PARAGRAPH = namedtuple('Paragraph','text tags citations')
TAG = namedtuple('Tag','text')
CITATION = namedtuple('Citation','text')

#utils
lineSep = re.compile(r'\n\s*\n+')
s = pp.Suppress
op = pp.Optional
opLn = s(op(pp.LineEnd()))

#parsers
tag = s(pp.Literal('%')) + pp.OneOrMore(pp.Word(pp.alphas + pp.nums)) + s(pp.Literal('%'))
citation = s(pp.Literal('[')) + pp.OneOrMore(pp.Word(pp.alphas)) + s(pp.Literal(',')) + pp.Word(pp.nums) + s(pp.Literal(']'))

heading_stars = pp.lineStart + pp.OneOrMore(pp.Literal('*'))
heading = heading_stars + pp.restOfLine

paragraph = pp.OneOrMore(s(pp.Word(pp.alphas+'.!"\'()+-_=@#$<>,?/;:')) | citation | tag)

ROOT = pp.OneOrMore(heading | paragraph)


def parseText(text):
    """ Parse text, creating headings, paragraphs, tags, citations """
    separated = lineSep.split(text)
    rootSection = None
    currentSection = None
    while len(separated) > 0:
        current = separated.pop(0)
        results = ROOT.parseString(current)
        #parsed a header, create a section
        if len(results) == 0:
            results = "Nothing, just add the paragraph"
            
        if isinstance(results[0],HEADER) and rootSection is None:
            #a new, root section
            currentSection = Section(results[0].title,results[0].level)
            rootSection = currentSection
            for res in results[1:]:
                if isinstance(res,TAG):
                    currentSection.add_tag(res.text)

        elif isinstance(results[0],HEADER):
            #a subsection
            if results[0].level > currentSection.level:
                currentSection = currentSection.add_subsection(results[0].title,
                                                               results[0].level)
            elif results[0].level <= currentSection.level:
                #a subsection of an ancestor 
                while results[0].level <= currentSection.level:
                    currentSection = currentSection.get_parent()
                    
                currentSection = currentSection.add_subsection(results[0].title,
                                                               results[0].level)
            for res in results[1:]:
                if isinstance(res,TAG):
                    currentSection.add_tag(res.text)

        else:
            #Paragraphs of a section
            currentParagraph = currentSection.add_paragraph(current)
            for res in results:
                if isinstance(res,TAG):
                    currentParagraph['tags'].add(res.text)
                elif isinstance(res,CITATION):
                    currentParagraph['citations'].add(res.text)
                        
    return rootSection
        
#actions:
heading_stars.setParseAction(lambda toks: len(toks))
heading.setParseAction(lambda toks: HEADER(toks[0],toks[1].strip()))

tag.setParseAction(lambda toks: TAG(" ".join(toks[:])))
citation.setParseAction(lambda toks: CITATION(" ".join(toks[:])))
