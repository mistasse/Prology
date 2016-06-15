from collections import *
from inspect import signature
from operator import indexOf
from contextlib import contextmanager


def instantiate(f):
    return f()


def unify(this, that, env=None):
    if env is None:
        env = {}
    if isinstance(this, Instance):
        env = {**this.vars, **env}
    if isinstance(that, Instance):
        env = {**that.vars, **env}
    links = defaultdict(set)

    def bind(var, val):
        toBind = set()
        toBind.add(var)
        while toBind:
            rem = toBind.pop()
            toBind |= links.get(rem, set())
            if links.get(rem, _notfound) is not _notfound:
                del links[rem]

            if env[rem] is not rem:
                push(env[rem], val)
            else:
                env[rem] = val

    def push(this, that):
        states.append((this, that))

    def link(this, that):
        links[this].add(that)
        links[that].add(this)

    states = []
    states.append((this, that))
    while states:
        (this, that) = states.pop()
        if this == that:
            continue

        # Are those two instances?
        if isinstance(this, Instance) and isinstance(that, Instance):
            if this.predicate != that.predicate or len(this.args) != len(that.args):
                return None
            for a, b in zip(this.args, that.args):
                push(a, b)
            continue

        # if this is not a variable
        if not isinstance(this, Variable):
            if not isinstance(that, Variable):
                # both not variables => must be equal
                if this != that:
                    return None
                continue
            else:  # that is a variable, not this
                bind(that, this)
            continue
        # so this is a variable. if that is not a variable
        if not isinstance(that, Variable):
            bind(this, that)
            continue

        # Now, both are Variables
        if env[this] is this:
            if env[that] is that:
                link(this, that)
            else:
                bind(this, env[that])
        elif env[that] is that:
            bind(that, env[this])
        else:
            # both have values
            push(env[this], env[that])

    # Now, we close the linking by clustering equal variables
    while links:
        rem = next(iter(links))
        toLink = links[rem]
        del links[rem]
        while toLink:
            linked = toLink.pop()
            if linked != rem:
                env[linked] = rem

            toLink |= links[linked]
            if links.get(linked, _notfound) is not _notfound:
                del links[linked]
    return env


@instantiate
class L:
    def __getattr__(self, name):
        return Variable(name)

_ = L


_notfound = object()

@instantiate
class unbound:
    def __repr__(self):
        return "_"

class Variable:

    def __init__(self, name):
        self.name = name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if not isinstance(other, Variable):
            return False
        return self.name == other.name

    def eval(self, subst):
        val = subst.get(self, self)
        if val is not self and isinstance(val, Variable):
            return val.eval(subst)
        if isinstance(val, Instance):
            return val.eval(subst)
        return val

    def __repr__(self):
        return self.name


class Instance:

    def __init__(self, predicate, args):
        self.predicate = predicate
        self.args = args

        self.vars = {}
        def unbounds(item):
            if isinstance(item, Variable):
                if item in self.vars:
                    return
                yield (item, item)
            if isinstance(item, Instance):
                for arg in item.args:
                    yield from unbounds(arg)
        for arg in args:
            self.vars = {**self.vars, **dict(unbounds(arg))}

    def rebind(self, env, newEnv=False):
        subst = {}
        for v in self.vars:
            new = v
            i = 0
            while new in env:
                new = Variable("{}_{}".format(v, i))
                i += 1
            subst[v] = new
        if newEnv:
            return self.eval(subst), subst
        return self.eval(subst)

    def __repr__(self):
        if not self.args:
            return str(self.predicate)
        return "{}({})".format(self.predicate, ", ".join(str(arg) for arg in self.args))

    def __eq__(self, other):
        if not isinstance(other, Instance):
            return False
        return self.predicate == other.predicate and self.args == other.args

    def eval(self, subst):
        newargs = [0]*len(self.args)
        for i, arg in enumerate(self.args):
            if isinstance(arg, (Variable, Instance)):
                newargs[i] = arg.eval(subst)
            else:
                newargs[i] = arg

        return Instance(self.predicate, tuple(newargs))

    def known(self):
        return self.known_when()

    def known_when(self, *args):
        self.predicate.facts.append(self)
        self.predicate.bodies.append(args)
        return self.predicate

    def ever(self):
        return next(self.ask(), None) is not None

    def dfs(self, var=None):
        subst = next(self.ask(), None)
        if subst is None:
            return None
        if var:
            return subst[var]
        return self.eval(subst)

    def all(self, var=None):
        ret = list(self.ask())
        if var:
            return [r[var] for r in ret]
        return ret

    def ask(self, toRename=None):
        """Yields a possible substitution, toRename contains the variable names
        already taken (since fsubst and subst coexist)"""
        if toRename is None:
            toRename = set()
        toRename |= set(self.vars)
        for i, fact in enumerate(self.predicate.facts):
            fact, reboundFactVariables = fact.rebind(toRename, True)  # gets the fact and rebind it
            fsubst = unify(self, fact)  # try unifying with the fact
            if fsubst is None:
                continue

            if not self.predicate.bodies[i]:  # if no body, just yield the substitution
                yield {k: v.eval(fsubst) for k, v in self.vars.items()}
                continue

            stack = [(0, fsubst, None)]  # Otherwise, perform a DFS on the possible unifications with body
            bodies = [body.eval(reboundFactVariables) for body in self.predicate.bodies[i]]
            while stack:
                j, fsubst, gen = stack.pop()
                if gen is None:
                    gen = bodies[j].eval(fsubst).ask(toRename | set(reboundFactVariables.values()))
                subst = next(gen, None)
                if subst is None:
                    continue
                stack.append((j, fsubst, gen))

                fsubst = {**fsubst, **subst}  # unbounded overrided
                if j == len(bodies)-1:  # yield if at the end of the body
                    yield {k: v.eval(fsubst) for k, v in self.vars.items()}
                else:
                    stack.append((j+1, fsubst, None))  # if not at the end, go one step further


class PythonPredicate:

    def __init__(self, fct, params=None):
        self.fct = fct
        if params is None:
            params = signature(fct).parameters
            self.vars = [Variable(name) for name in params]
            self.mapping = {var: var for var in self.vars}
        else:
            self.vars, self.mapping = params

    def eval(self, subst):
        mapping = {}
        for k, v in self.mapping.items():
            if isinstance(v, (Variable, Instance)):
                mapping[k] = v.eval(subst)
            else:
                mapping[k] = v
        return PythonPredicate(self.fct, (self.vars, mapping))

    def ask(self, toRename=None):
        for answer in self.fct(*(v.eval(self.mapping) for v in self.vars)):
            yield {self.mapping.get(k, k): v for k, v in answer.items()}


def PyPred(fct):
    if isinstance(fct, Instance):
        instance = fct
        def _(fct):
            instance.known_when(PythonPredicate(fct))
            return fct
        return _
    else:
        return PythonPredicate(fct)


class Predicate:

    def __init__(self, name):
        self.name = name
        self.facts = []
        self.bodies = []

    def __call__(self, *args):
        return Instance(self, args)

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self is other

def plist(*iterable):
    current = nil
    for item in iterable[::-1]:
        current = lst(item, current)
    return current


Equal = Predicate("equal")
Equal(_.A, _.A).known()


Not = Predicate("not")
@PyPred(Not(_.A))
def _not(A):
    if isinstance(A, Instance):
        return [] if A.ever() else [{}]
    raise Exception("Not only works with predicate instances. Got {}".format(A))


lst = Predicate("list")
nil = Predicate("nil")()
true = Predicate("true")()
true.known()
false = Predicate("false")()
