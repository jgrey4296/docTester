import unittest
import logging
from test_context import doctester as dt
from doctester.Section import Section
from doctester.Should import Should

class Should_Tests(unittest.TestCase):

    def test_existence(self):
        self.assertTrue(True)
        
    def test_mention(self):
        self.assertTrue(True)
            
    def test_cite(self):
        self.assertTrue(True)
        
    def test_precede(self):
        self.assertTrue(True)

    def test_section(self):
        self.assertTrue(True)
        
    def test_subsections(self):
        self.assertTrue(True)
        
    def test_chapter(self):
        self.assertTrue(True)
        
    def test_sections(self):
        self.assertTrue(True)
        
    def test_tag(self):
        self.assertTrue(True)
        
    def test_regex(self):
        self.assertTrue(True)
        
    def test_length(self):
        self.assertTrue(True)
        
class SizedShould_Tests(unittest.TestCase):

    def test_larger(self):
        self.assertTrue(True)
        
    def test_smaller(self):
        self.assertTrue(True)
        
    def test_equal(self):
        self.assertTrue(True)
        
    def test_least(self):
        self.assertTrue(True)
        
    def test_most(self):
        self.assertTrue(True)
        
    def test_than(self):
        self.assertTrue(True)
        
    def test_pages(self):
        self.assertTrue(True)
        
    def test_sentences(self):
        self.assertTrue(True)

    def test_words(self):
        self.assertTrue(True)
        
    def test_citations(self):
        self.assertTrue(True)
    
    def test_subsections_len(self):
        self.assertTrue(True)
        
    
    

        
    
    
    





if __name__ == "__main__":
      LOGLEVEL = logging.DEBUG
      logFileName = "doctester_tests.log"
      logging.basicConfig(filename=logFileName, level=LOGLEVEL, filemode='w')
      console = logging.StreamHandler()
      console.setLevel(logging.INFO)
      logging.getLogger('').addHandler(console)
      unittest.main()
