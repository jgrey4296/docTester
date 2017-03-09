from doctester import Document, DocTestRunner, DocException

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
    
    def test_success(self):
        return True

    def test_fail(self):
        return False

    def test_chapters(self):
        self.d.should.have.chapter('test')
        self.d.should.have.chapter('second')

    def test_chapters_fail(self):
        self.d.should.have.chapter('third')

    def test_section(self):
        self.d.chapter('test').should.have.section('introduction')
        self.d.chapter('second').should.have.section('background')

    def test_section_fail(self):
        self.d.chapter('test').should.have.section('blahh')

    def test_mention(self):
        self.d.chapter('test').should.mention('blah')

    def test_mention_fail(self):
        self.d.chapter('test').should.mention('bloo')

    def test_length(self):
        self.d.should.have.length(5).pages()
        self.d.chapter('test').should.have.length(3).paragraphs()
        self.d.chapter('test').section('introduction').should.have.at.least.length(1).paragraphs()
        
    def test_length_fail(self):
        self.d.chapter('second').should.have.length(2).paragraphs()
        self.d.chapter('second').section('introduction').should.have.at.least.length(1).paragraphs()

    def test_precedence(self):
        self.d.chapter('test').section('introduction').should.precede('conclusion')

    def test_precedence_fail(self):
        self.d.chapter('test').section('conclusion').should.precede('introduction')
        
##############################
if __name__ == '__main__':
    runner = ExampleTester()
    runner()
