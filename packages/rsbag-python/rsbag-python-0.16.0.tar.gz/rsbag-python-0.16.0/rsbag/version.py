__version__ = '0.16.0'
__commit__ = 'gad2e792'

def getVersion():
    """
    Returns a descriptive string for the version of the RSBag client API.
    """
    return "%s-%s" % (__version__, __commit__)
