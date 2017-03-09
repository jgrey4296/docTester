import logging as root_logger
logging = root_logger.getLogger(__name__)
from doctester.DocException import DocException

class DocTestRunner:
    """ The main test runner class. Subclass this to add tests """
    
    TEST_NAME = 'test_'
    TICK = '✓'
    CROSS = 'X' 
    TAB =  "	"
    def __call__(self):
        """ The main call to run tests """
        passed = 0
        failed = 0
        tests = [x for x in dir(self) if DocTestRunner.TEST_NAME in x]
        total = len(tests)
        for test in tests:
            try:
                getattr(self,test)()
            except DocException as e:
                logging.warning("{} {} : {} {} {} {} {}".format(DocTestRunner.TAB,
                                                        DocTestRunner.CROSS,
                                                        test,
                                                        '\n',
                                                        DocTestRunner.TAB, DocTestRunner.TAB,
                                                        repr(e)))
                failed += 1
            else:
                logging.info("{} {} : {}".format(DocTestRunner.TAB,
                                                 DocTestRunner.TICK,
                                                 test))
                passed += 1

        logging.info("\n\nFinished. {}/{} Passed. {}/{} Failed.".format(passed,total,failed,total)) 
