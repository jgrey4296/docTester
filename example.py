from doctester import Document, DocTestRunner

# Setup root_logger:
import logging as root_logger
LOGLEVEL = root_logger.DEBUG
LOG_FILE_NAME = "DocTestExample.log"
root_logger.basicConfig(filename=LOG_FILE_NAME, level=LOGLEVEL, filemode='w')

console = root_logger.StreamHandler()
console.setLevel(root_logger.INFO)
root_logger.getLogger('').addHandler(console)
logging = root_logger.getLogger(__name__)
##############################

class ExampleTester(DocTestRunner):

    def __init__(self):
        self.d = Document('./data')
    
    def test_init(self):
        self.d.should.have.section('introduction')
        self.d.should.have.section('conclusion')
        self.d.chapter('introduction').should.have.sentences(2)
        self.d.chapter('conclusion').should.have.sentences.atLeast(2)

    def test_sections(self):
        return True

    def test_blah(self):
        return True

##############################
if __name__ == '__main__':
    runner = ExampleTester()
    runner()
