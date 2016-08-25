from _prology import *
_ = L

def PrintEach(lst):
    case = switch(lst)
    for H, T in (_.H, _.T) | case(cons(_.H, _.T)):
        print(H)
        PrintEach(T)
    for x in case(nil):
        print("end of message")
    for x in case.default:
        print("/!\\ lst should be a list but got {}".format(x))

PrintEach(3)
PrintEach(_["hello", "world"])
