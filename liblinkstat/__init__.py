
__all__ = [
    ]

__version__ = "1.0.1-dev"

def inall(obj) :
    __all__.append(obj.__name__)
    return obj

@inall
class Actions :
    OR = 1,
    AND = 2,
    UNIQUE = 3

@inall
class ReportException(Exception) :
    def __init__(self, returnValue, *args) :
        super().__init__(*args)
        self.returnValue = returnValue
    
from .linkstat import LinkStat
