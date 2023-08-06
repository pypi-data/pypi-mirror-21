from argparse import ArgumentError, ArgumentTypeError


class VolumeValidator():
    '''
    Created on Apr 16, 2015
    
    This is an independant class to facilitate the validation of volume fields so that it 
    can be used both in the volume model object, and int conjunction with argparse to
    handle ranges with an exorbinant number of choices.  For example... a range from 86400 to 1209600
    would print a list of thousands of choices if a bad value was entered.  This solves that.
    
    @author: nate
    '''
    
    @staticmethod
    def priority( priority ):
        
        priority = int(priority)
        
        if (priority > 10 or priority < 1):
            raise ArgumentTypeError("Priority must be a value between 1 and 10.")
        
        return priority
    
    @staticmethod
    def iops_guarantee( iops ):
        
        iops = int(iops)
        
        if ( iops < 0 or iops > 30000 ):
            raise ArgumentTypeError( "IOPs guarantee must be between 0 and 30,0000.")
        
        return iops
        
    @staticmethod
    def iops_limit( iops ):
        
        iops = int(iops)
        
        if ( iops < 0 or iops > 10000):
            raise ArgumentTypeError( "IOPs limit must be between 0 and 10,000.")
        
        return iops
        
    @staticmethod
    def continuous_protection( seconds ):
        
        seconds = int(seconds)
        
        if ( seconds < 0 or seconds > 1209600 ):
            raise ArgumentTypeError( "Continuous protection must be between 0 and 1209600 (1 year).")
        
        return seconds
        
    @staticmethod
    def size( size ):
        
        size = int(size)
        
        if ( size < 0 ):
            raise ArgumentTypeError( "Must be greater than zero.")
        
        return size
    
    @staticmethod
    def chap( arg ):
        
        password = arg.split( ":" )[1];
        chars = len( password )
        
        if ( chars < 12 or chars > 16 ):
            raise ArgumentTypeError( "iSCSI CHAP passwords Must be between 12 and 16 characters.")
        
        return arg
