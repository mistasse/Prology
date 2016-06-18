from _prology import *
_ = L

SmallInteger = Predicate("sminteger")
@PyPred(SmallInteger(_.A))
def sminteger(A):
    if isinstance(A, Variable):
        for i in range(0, 10):
            yield {A: i}
    if isinstance(A, int):
        if 0 <= A < 10:
            yield {}

NotFive = Predicate("notFive")
NotFive(_.A).known_when(
    SmallInteger(_.A), Not(Equal(_.A, 5))
)
# List all Integers (in the predicate extension) not equal to 5
print(NotFive(_.X).all())


# Now, we won't stop to the 10 first natural, but we'd better not make an exhaustive search!
BigInteger = Predicate("biginteger")
@PyPred(BigInteger(_.A))
def biginteger(A):
    if isinstance(A, Variable):
        for i in range(0, 2**32):
            yield {A: i}
    if isinstance(A, int):
        yield {}

Five = Predicate("Five")
Five(_.A).known_when(BigInteger(_.A), Equal(_.A, 5))
print(Five(_.A).first)  # Not an exhaustive search, hopefully, the dfs is lazy and won't compute all the 2**32 alternatives!

Addition = Predicate("Addition")
@PyPred(Addition(_.A, _.B, _.C))
def _add(A, B, C):
    bound = tuple(0 if isinstance(v, Variable) else 1 for v in (A, B, C))
    if bound == (0, 1, 1):
        yield {A: C-B}
    elif bound == (1, 0, 1):
        yield {B: C-A}
    elif bound == (1, 1, 0):
        yield {C: B+A}
    elif bound == (1, 1, 1):
        if A+B == C:
            yield {}

# Here, B will be forced to be a smallInteger
SmallIntegerAddition = Predicate("smintegeraddition")
SmallIntegerAddition(_.A, _.B, _.C).known_when(SmallInteger(_.A), SmallInteger(_.B), SmallInteger(_.C), Addition(_.A, _.B, _.C))
print(SmallIntegerAddition(_.B, _.A, 5).all())

# Here, no constraint on B, the addition predicate will be used to compute it => may not be a smallInteger
SmallIntegerAddition = Predicate("smintegeraddition")
SmallIntegerAddition(_.A, _.B, _.C).known_when(SmallInteger(_.A), SmallInteger(_.C), Addition(_.A, _.B, _.C))
print(SmallIntegerAddition(_.B, _.A, 5).all())
