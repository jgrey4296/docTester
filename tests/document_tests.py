import unittest
import logging
from test_context import doctester as dt
from doctester.Document import Document
from doctester.Section import Section
from doctester.Should import Should

class Document_Tests(unittest.TestCase):

    def setup(self):
        self.doc = Document('./data')

    def test_existence(self):
        self.assertIsInstance(self.doc,Document)
        self.assertFalse(self.doc.is_section())
        self.assertTrue(self.doc.is_document())

    def test_found_files(self):
        self.assertTrue(True)

    def test_chapter(self):
        self.assertTrue(True)

    def test_found_files(self):
        self.assertTrue(True)

    def test_word_count(self):
        self.assertTrue(True)

    def test_sentence_count(self):
        self.assertTrue(True)

    def test_citations(self):
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
