class DocException(Exception):
    """ The exception class thrown by any doc/should test """
    def __init__(self,desc,**kwargs):
        self.desc = desc
        self.vals = {}
        for key in kwargs:
            self.vals[key] = kwargs[key]

    def __repr__(self):
        if 'expected' and 'actual' in self.vals:
            return "{} : Expected {}, Got {}".format(self.desc,
                                                     self.vals['expected'],
                                                     self.vals['actual'])
        elif 'missing' in self.vals:
            return "{} : missing {}".format(self.desc, self.vals['missing'])
        
        return "{} : {}".format(self.desc, )
