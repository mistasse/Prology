from _prology import *
_ = L

SmallInteger = Predicate("sminteger")
@PyPred(SmallInteger(_.A))
def sminteger(A):
    if isinstance(A, Variable):
        for i in range(0, 10):
            yield {A: i}
    if isinstance(A, int):
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
print(Five(_.A).dfs())  # Not an exhaustive search, hopefully, the dfs is lazy and won't compute all the 2**32 alternatives!
