from _prology import *
_ = L

Extends = Predicate("class")
Extends("animal", "any").known()
Extends("bird", "animal").known()

Extends("vehicle", "any").known()
Extends("car", "vehicle").known()

Super = Predicate("super")
Super(_.A, _.B).known_when(Extends(_.A, _.B))
Super(_.A, _.B).known_when(Extends(_.A, _.T), Super(_.T, _.B))

InstanceOf = Predicate("instanceof")
InstanceOf(_.A, _.A).known()
InstanceOf(_.A, _.B).known_when(Super(_.A, _.B))

Push = Predicate("push")
# We can only put B in A if B is an instance of B
Push(plist("list", _.A), _.B).known_when(InstanceOf(_.B, _.A))

print(Push(plist("list", "any"), _.A).all())  # What can we put into a list of "any"?
print(Push(plist("list", "animal"), _.A).all())  # What can we put into a list of "animal"?
