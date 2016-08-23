from _prology import *
_ = L
l = plist

t = Predicate("t")

Print = Predicate("print")
@PyPred(Print(_.A))
def _print(A):
    print(A)
    yield {}

Bound = Predicate("bound")
@PyPred(Bound(_.A))
def _bound(A):
    if not isinstance(A, Variable):
        yield {}
@PyPred(Bound(_.A, _.B))
def _bound(A, B):
    if not isinstance(A, Variable) and not isinstance(B, Variable):
        yield {}

NotMatching = Predicate("not_matching")
@PyPred(NotMatching(_.A, _.B))
def _not_matching(A, B):
    if isinstance(B, Instance):
        if unify(A, B) is None:
            yield {}

extends = Predicate("extends")

hasSuper = Predicate("hasSuper")  # A is a superclass of B
hasSuper(_.A, _.B).known_when(extends(_.A, _.B))
hasSuper(_.A, _.B).known_when(extends(_.A, _.T), hasSuper(_.T, _.B))

instanceof = Predicate("instanceof")
instanceof(_.A, _.A).known()
instanceof(_.A, _.B).known_when(hasSuper(_.A, _.B))

generic = Predicate("generic")
inv = Predicate("inv")
sup = Predicate("sup")
sub = Predicate("sub")

geninstanceof = Predicate("generic_instanceof")
geninstanceof(_.A, _.B).known_when(instanceof(_.A, _.B))
geninstanceof(_.A, inv(_.B)).known_when(Equal(_.A, _.B))
geninstanceof(_.A, sub(_.B)).known_when(instanceof(_.A, _.B))
geninstanceof(_.A, sup(_.B)).known_when(instanceof(_.B, _.A))

aregeninstances = Predicate("array_generic_instanceof")
aregeninstances(nil, nil).known()
aregeninstances(cons(_.A, _.T1), cons(_.B, _.T2)).known_when(geninstanceof(_.A, _.B), aregeninstances(_.T1, _.T2))

instanceof(generic(_.A, _.Params), generic(_.B, _.RParams)).known_when(instanceof(_.A, _.B), aregeninstances(_.Params, _.RParams))

extends("car", "any").known()
extends("animal", "any").known()
extends("cat", "animal").known()
extends("mouse", "animal").known()
extends("cat", generic("killer", _["mouse"])).known()  # Cat is a mouse killer

print(instanceof("cat", _.B).all())
print(instanceof("cat", generic("killer", _[_.B])).all())
print(instanceof(generic("killer", _["mouse"]), generic("killer", _[_.B])).all())

# A cage of killer of animal should contain cats
print(instanceof(generic("killer", _["mouse"]), generic("killer", _["animal"])).all())
print(instanceof("cat", generic("killer", _["animal"])).all())
print(instanceof(generic("cage", _["cat"]), generic("cage", _[generic("killer", _["animal"])])).all())
