from _prology import *
_ = L

# This once caused a bug because of the free variables not being substituted

A = Predicate("A")
A(_.A).known_when(Equal(_.T, 3))

C = Predicate("C")
C(_.Z).known_when(A(_.Z))

B = Predicate("B")
B(_.B).known_when(A(_.T), Equal(_.T, 1))

print(B(_.B).all())
