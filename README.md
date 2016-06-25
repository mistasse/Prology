# Prology

Prology is a minimal library aiming at bringing to Python the power of Logic Programming. For now, it is more of an experiment (this is the result of only two days of work), and thus no efforts have been put into performances, and there might even be bugs, though I do not have find any. (my tests are rather poor for now, I cannot wait to be done with my exams!)

However, this should only be a matter of time, and anyone who is wanting to contribute is really welcome. I will try to put it on PyPI later, and wish to improve it as far as I can.

## Are there dependencies?

There's absolutely no dependency except Python3.

## How does it compare to logpy or PyLog?

In fact, I do not have any idea. I just wanted to work in Python with a very Prolog-like library written from scratch, which has been achieved in around 300 lines of code. It seems much more close to Prolog in expressiveness than logpy.

Prology seems a bit more similar to PyLog, but in contrast to it, it does not require to have a Prolog installation, and seems more interoperable with Python's functionalities.

## How to get started?
First, create your own predicates and the rules in which case the predicate is true. It will work by unification, just like in Prolog. I personally create unbound variables by binding `_` to `prology.L`, so a variable `X` is declared typing `_.X` but you could also use `L.X`, or just `Variable(X)`.

Here is an example:


```python
from prology import *
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
```

Also notice how predicate instances are complete data structures.

To go further, I propose you to watch the *examples* folder, or look around for how Prolog works, keeping in mind Prology will never try to unify objects that are not suggested by the backtracking process.

I will also write more documentation when I have more time. But note it is also possible to write python predicates to make it even more powerful! Please have a look at the *examples* folder.

## License?

MIT
