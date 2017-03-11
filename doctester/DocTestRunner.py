import logging as root_logger
logging = root_logger.getLogger(__name__)
from doctester.DocException import DocException

class DocTestRunner:
    """ The main test runner class. Subclass this to add tests """
    #Usefule constants:
    TEST_NAME = 'test_'
    FAIL = 'test_fail_'
    TICK = '✓'
    CROSS = 'X' 
    TAB =  "	"
    
    def __call__(self):
        """ The main call to run tests """
        passed = 0
        failed = 0
        tests = [x for x in dir(self) if DocTestRunner.TEST_NAME in x and DocTestRunner.FAIL not in x]
        fail_tests = [x for x in dir(self) if DocTestRunner.FAIL in x]
        total = len(tests)+len(fail_tests)
        logging.info("Running Tests:")
        for test in tests:
            try:
                result = getattr(self,test)()
                if result is not None and result == False:
                    raise DocException('Test returned False')
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

        logging.info('Running Fail Tests:')
        for test in fail_tests:
            try:
                result = getattr(self,test)()
                if result is not None and result != False:
                    logging.warning('{} : Did not return false'.format(test))
                    failed += 1
            except DocException as e:
                passed += 1
                logging.info("{} {} : {}".format(DocTestRunner.TAB,DocTestRunner.TICK, test))
                    
                
        logging.info("\n\nFinished. {}/{} Passed. {}/{} Failed.".format(passed,total,failed,total)) 

