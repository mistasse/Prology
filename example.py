from prology import *
_ = L

Integer = Predicate("integer")
@PyPred(Integer(_.A))
def integer(A):
    if isinstance(A, Variable):
        for i in range(0, 10):
            yield {A: i}
    if isinstance(A, int):
        yield {}


append = Predicate("append")
append(nil, _.L, _.L).known()
append(lst(_.H, _.T), _.L2, lst(_.H, _.L3)).known_when(
    append(_.T, _.L2, _.L3)
)

NotFive = Predicate("notFive")(_.A).known_when(Integer(_.A), Not(Equal(_.A, 5)))
# List all Integers (in the predicate extension) not equal to 5
print(NotFive(_.X).all())

# Append [1, 2, 3] and [4, 5, 6], prints the result in Z
print(append(plist(1, 2, 3), plist(4, 5, 6), _.Z).dfs(_.Z))
# Return first matching instance
print(append(_.A, _.B, plist(1, 2, 3, 4, 5, 6, 7)).dfs())
# Returns if it was possible to find an answer
print(append(_.A, _.B, plist(1, 2, 3, 4, 5, 6, 7)).ever())
# Get all working substitutions
print(append(_.A, _.B, plist(1, 2, 3, 4, 5, 6, 7)).all())
