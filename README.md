# Prology

Prology is a minimal library aiming at bringing to Python the power of Logic Programming. For now, it is more of an experiment (this is the result of only two days of work), and thus no efforts have been put into performances, and there might even be bugs, though I do not have find any. (my tests are rather poor for now, cannot wait to be done with my exams)

However, this should only be a matter of time, and anyone who is wanting to contribute is really welcome. I will try to put it on PyPI later, and wish to improve it as far as I can.

## How does it compare to logpy?

In fact, I do not have any idea. I just wanted to work in Python with a very Prolog-like library written from scratch, which has been achieved in around 300 lines of code. It seems much more close to Prolog in expressiveness than logpy.

## How to get started?
First, create your own predicates and the rules in which case the predicate is true. It will work by unification, just like in Prolog. I personally create unbound variables by binding `_` to `prology.L`, so a variable `X` is declared typing `_.X` but you could also use `L.X`, or just `Variable(X)`.

Here is an example:


```python
from prology import *
_ = L

append = Predicate("append")
append(nil, _.L, _.L).known()
append(lst(_.H, _.T), _.L2, lst(_.H, _.L3)).known_when(
    append(_.T, _.L2, _.L3)
)

# Get the first matching instance
print(append(_.A, _.B, plist(1, 2, 3, 4, 5, 6, 7)).dfs())
# Returns if it was possible to find an answer
print(append(_.A, _.B, plist(1, 2, 3, 4, 5, 6, 7)).ever())
# Get all working substitutions
print(append(_.A, _.B, plist(1, 2, 3, 4, 5, 6, 7)).all())
```

To go further, I propose you to watch the example.py file, or look around for how Prolog works, keeping in mind Prology will never try to unify objects that are not suggested by the backtracking process.

I will also write more documentation when I have more time. But note it is also possible to write python predicates to make it even more powerful! Please have a look at the example.py file.

## License?

MIT
