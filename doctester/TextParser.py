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
    data = []
    separated = lineSep.split(text)
    currentSection = None
    while len(separated) > 0:
        current = separated.pop(0)
        results = ROOT.parseSring(current)
        if isinstance(results[0],HEADER):
            currentSection = {'title':result, paragraphs: [], tags: []}
            data.append(currentSection)
            for res in results[1:]:
                if isinstance(res,TAG):
                    currentSection['tags'].append(res)
        else:
            currentParagraph = {'text': current, tags: [], citations: [] }
            currentSection['paragraphs'].append(currentParagraph)
            for res in results:
                if isinstance(res,TAG):
                    currentParagraph['tags'].append(res)
                elif isinstance(res,CITATION):
                    currentParagraph['citations'].append(res)
                        
    return data
        
#actions:
heading_stars.setParseAction(lambda toks: len(toks))
heading.setParseAction(lambda toks: HEADER(toks[0],toks[1]))

tag.setParseAction(lambda toks: TAG(toks))
citation.setParseAction(lambda toks: CITATION(toks))
