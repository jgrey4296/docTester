import unittest
import logging
from test_context import doctester as dt
from doctester.Section import Section
from doctester.Should import Should

class Section_Tests(unittest.TestCase):

    #use testcase snippets
    def test_initialise(self):
        aSection = Section('aTitle',1)
        self.assertIsInstance(aSection,Section)
        self.assertEqual(aSection.title,'aTitle')
        self.assertEqual(aSection.level,1)
        self.assertTrue(aSection.is_section())
        self.assertFalse(aSection.is_document())
        
    def test_should_retrieval(self):
        aSection = Section('aTitle',1)
        self.assertIsInstance(aSection.should, Should)
        self.assertEqual(aSection.should.ref,aSection)

    def test_set_parent(self):
        aSection = Section('aTitle',1)
        anotherSection = Section('AnotherTitle',2)
        self.assertIsNone(anotherSection.get_parent())
        anotherSection.set_parent(aSection)
        self.assertIsNotNone(anotherSection.get_parent())
                            
    def test_bad_set_parent(self):
        aSection = Section('aTitle',1)
        anotherSection = Section('AnotherTitle',2)
        self.assertIsNone(aSection.get_parent())
        with self.assertRaises(Exception):
            aSection.set_parent(anotherSection)

    def test_tags(self):
        self.assertTrue(True)


    def test_paragraphs(self):
        
        self.assertTrue(True)
        
    def test_subsection(self):
        
        self.assertTrue(True)
        
    def test_get_paragraphs(self):
        
        self.assertTrue(True)
        
    def test_counts(self):
        
        self.assertTrue(True)
        
    def test_mentions(self):
        
        self.assertTrue(True)
        
    
    

        
    
    
    





if __name__ == "__main__":
      LOGLEVEL = logging.DEBUG
      logFileName = "doctester_tests.log"
      logging.basicConfig(filename=logFileName, level=LOGLEVEL, filemode='w')
      console = logging.StreamHandler()
      console.setLevel(logging.INFO)
      logging.getLogger('').addHandler(console)
      unittest.main()
