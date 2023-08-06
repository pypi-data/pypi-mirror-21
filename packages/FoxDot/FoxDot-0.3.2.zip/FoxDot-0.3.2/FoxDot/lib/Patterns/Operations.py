from __future__ import division
import Base
import PlayString

"""
    Module for key operations on Python lists or FoxDot Patterns
"""

class POperand:

    def __init__(self, func):
        
        self.operate = func

    def __call__(self, A, B):
        """ A is always a pattern.
        """

        # If the first pattern is empty, return the other as a pattern

        if len(A) == 0:

            return Base.Pattern(B)

        # Get the dominant pattern type and convert B

        cls = Base.Dominant(A, B)
        
        A = cls(A)
        B = cls(B)

        # Calculate total length before operations

        i, length = 0, LCM(len(A), len(B))

        P1 = []

        while i < length:

            try:

                val = self.operate(A[i], B[i])

            except ZeroDivisionError:

                val = 0

            P1.append(val)
            i += 1

        return cls(P1)

# General operations
def Nil(a, b):  return a
def Add(a, b):  return a + b
def Sub(a, b):  return a - b
def Mul(a, b):  return a * b
def Div(a, b):  return a / b
def Mod(a, b):  return a % b
def Pow(a, b):  return a ** b
def Get(a, b):  return a[b]

def rAdd(a, b): return b + a
def rGet(a, b): return b[a]
def rSub(a, b): return b - a
def rDiv(a, b): return b / a
def rMod(a, b): return b % a
def rPow(a, b): return b ** a

# Pattern operations
PAdd = POperand(Add)

PSub = POperand(Sub)
PSub2 = POperand(rSub)

PMul = POperand(Mul)

PDiv = POperand(Div)
PDiv2 = POperand(rDiv)

PMod = POperand(Mod)
PMod2 = POperand(rMod)

PPow = POperand(Pow)
PPow2 = POperand(rPow)

PGet = POperand(Get)

# Pattern comparisons -> need to maybe have a equals func?
PEq = lambda a, b: (all([a[i]==b[i] for i in range(len(a))]) if len(a) == len(b) else False) if a.__class__ == b.__class__ else False
PNe = lambda a, b: (any([a[i]!=b[i] for i in range(len(a))]) if len(a) == len(b) else True) if a.__class__ == b.__class__ else True


#: Misc. Operations

def sliceToRange(s):
    start = s.start if s.start is not None else 0
    stop  = s.stop 
    step  = s.step if s.step is not None else 1
    try:
        return list(range(start, stop, step))
    except OverflowError:
        raise TypeError("range() integer end argument expected, got NoneType")

def LCM(*args):
    """ Lowest Common Multiple """

    args = [n for n in args if n != 0]
    
    # Base case
    if len(args) == 0:
        return 1
    
    elif len(args) == 1:
        return args[0]

    X = list(args)
    
    while any([X[0]!=K for K in X]):

        i = X.index(min(X))
        X[i] += args[i]        

    return X[0]

def EuclidsAlgorithm(n, k):
    
    if n == 0: return [n for i in range(k)]
    
    data = [[1 if i < n else 0] for i in range(k)]
    
    while True:
        
        k = k - n

        if k <= 1:
            break

        elif k < n:
            n, k = k, n

        for i in range(n):
            data[i] += data[-1]
            del data[-1]
    
    return [x for y in data for x in y]


def patternclass(a, b):
    return Base.PGroup if isinstance(a, Base.PGroup) and isinstance(b, Base.PGroup) else Base.Pattern


def modi(array, i, debug=0):
    """ Returns the modulo index i.e. modi([0,1,2],4) will return 1 """
    try:
        return array[i % len(array)]
    except(TypeError, AttributeError, ZeroDivisionError): 
        return array

def group_modi(pgroup, index):
    """ Returns value from pgroup that modular indexes nested groups """
    if isinstance(pgroup, (int, float, str, bool, PlayString.PlayGroup)):
        return pgroup
    else:
        try:
            return group_modi(pgroup[index % len(pgroup)], index // len(pgroup))
        except(TypeError, AttributeError, ZeroDivisionError):
            return pgroup

def get_expanded_len(data):
    """ (0,(0,2)) returns 4. int returns 1 """
    l = []
    try:
        for item in data:
            try:
                l.append(len(item))
            except(TypeError, AttributeError):
                l.append(1)
        return LCM(*l) * len(data)
    except TypeError:
        return 1

def max_length(*patterns):
    """ Returns the largest length pattern """
    return max([len(p) for p in patterns])  
