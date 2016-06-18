from _prology import *
_ = L

append = Predicate("append")  # Create a predicate
append(nil, _.L, _.L).known()  # a simple fact
append(cons(_.H, _.T), _.L2, cons(_.H, _.L3)).known_when(
    append(_.T, _.L2, _.L3),
    true  # will always unify, just to show multi-expressions statements
)  # more complex facts

# Append [1, 2, 3] and [4, 5, 6], prints the result in Z
print(append(plist(1, 2, 3), plist(4, 5, 6), _.Z).first[_.Z])
# Return first matching instance
print(append(_.A, _.B, plist(1, 2, 3, 4, 5, 6, 7)).fill())
# Returns if it was possible to find an answer
print(append(_.A, _.B, plist(1, 2, 3, 4, 5, 6, 7)).ever())
# Get all working substitutions
print(append(_.A, _.B, plist(1, 2, 3, 4, 5, 6, 7)).all())
