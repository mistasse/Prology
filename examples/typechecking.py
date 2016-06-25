from _prology import *
_ = L
l = plist

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

print(Push(plist("list", _.A), "animal").all())  # In what kind of list can we put an "animal"?


Collection = Predicate("collection")
Collection("list").known()
Collection("set").known()

function = Predicate("function")

Map = Predicate("map")
Map(function(l(_.P), _.Rfun), l(_.C, _.Q), _.Rmap).known_when(
    InstanceOf(_.Q, _.P),
    Collection(_.C),
    Equal(_.Rmap, plist(_.C, _.Rfun))
)

# Would it work to map a function of vehicle on a list of birds?
print(Map(function(l("vehicle"), "bird"), l("list", "bird"), _.R).ever())
# What is the return type of this map?
print(Map(function(l("vehicle"), "bird"), l("set", "car"), _.R).all())
# What can be the return type of a map with unbound collection?
print(Map(function(l("vehicle"), "bird"), l(_.C, "car"), _.R).all())
