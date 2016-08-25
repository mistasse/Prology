from prology import *
_ = L
from unittest import main, TestCase


class Test(TestCase):

    def testForCover(self):
        self.assertEqual(str(cons(_.A, _.B)), "cons(A, B)")
        self.assertEqual(str(nil), "nil")
        self.assertEqual(str(_.A), "A")
        self.assertEqual(str(Variable("A", 0)), "A")
        self.assertEqual(str(Variable("A", 1)), "A#1")
        self.assertNotEqual(_.A, "A")
        self.assertNotEqual(cons(_.A), "cons(A)")

    def testUnify(self):
        assert unify(1, 1) == {}
        pred = Predicate("pred")
        assert unify(pred(_.A, _.B, _.A), pred(1, 2, _.B)) is None
        self.assertEqual(unify(pred(_.A, _.B, _.A), pred(1, 1, _.B)), {_.A: 1, _.B: 1})
        assert unify(pred(1, 2), pred(_.A, _.A)) is None
        assert unify(pred(_.A, _.A), pred(1, 2)) is None
        assert unify(pred(_.A, 2), pred(1, _.A)) is None
        assert unify(pred(1, _.A), pred(_.A, 2)) is None

    def testTruth(self):
        self.assertEqual(true.first, {})
        self.assertEqual(false.first, None)
        self.assertEqual(true.fill(), true)
        self.assertEqual(true.fill(), true)
        self.assertEqual(false.fill(), None)
        self.assertEqual(true.all(), [{}])
        self.assertEqual(true.ever(), True)
        self.assertEqual(false.ever(), False)

    def assertNotNone(self, x):
        print(x)
        super().assertIsNotNone(x)

    def testDFS(self):
        cross = Predicate("cross")
        cross(_.A, _.A).known()
        cross(_.x, nil).known()
        cross(nil, _.x).known()
        self.assertEqual(
            cross(plist(_.a, _.a), plist(_.b, 1)).fill(),
            cross(plist(1, 1), plist(1, 1))
            )
        self.assertEqual(
            cross(plist(_.b, 1), plist(_.a, _.a)).fill(),
            cross(plist(1, 1), plist(1, 1))
            )

    def testAppend(self, append=None):
        if append is None:
            append = Predicate("append")
            append(nil, _.L, _.L).known()
            append(cons(_.H, _.T), _.L2, cons(_.H, _.L3)).known_when(
                append(_.T, _.L2, _.L3)
            )
        self.assertEqual(append(plist(1, 2, 3), plist(4, 5), _.Z).fill(), append(plist(1, 2, 3), plist(4, 5), plist(1, 2, 3, 4, 5)))

        self.assertEqual(append(_.X, plist(4, 5), plist(1, 2, 3, 4, 5)).all(), [{_.X: plist(1, 2, 3)}])
        answers = append(_.X, _.Y, plist(1, 2, 3, 4, 5)).all()
        self.assertEqual(len(answers), 6)
        self.assertIn({_.X: plist(1, 2, 3, 4, 5), _.Y: plist()}, answers)
        self.assertIn({_.X: plist(1, 2, 3, 4), _.Y: plist(5)}, answers)
        self.assertIn({_.X: plist(1, 2, 3), _.Y: plist(4, 5)}, answers)
        self.assertIn({_.X: plist(1, 2), _.Y: plist(3, 4, 5)}, answers)
        self.assertIn({_.X: plist(1), _.Y: plist(2, 3, 4, 5)}, answers)
        self.assertIn({_.X: plist(), _.Y: plist(1, 2, 3, 4, 5)}, answers)

    def testDict(self):
        a = cons(_.A, _.B)
        self.assertEqual(a.a, _.A)
        self.assertEqual(a.b, _.B)
        self.assertEqual(a["a"], _.A)
        self.assertEqual(a["b"], _.B)
        self.assertEqual(a[0], _.A)
        self.assertEqual(a[1], _.B)

        try:
            a["x"]
            assert False
        except KeyError as e:
            assert True
        try:
            a[2]
            assert False
        except KeyError as e:
            assert True
        try:
            print(a["x"])
            assert False
        except KeyError as e:
            assert True


        try:
            print(a.x)
            assert False
        except AttributeError as e:
            assert True

    def testMatch(self):
        case = switch(_["they", "see", "me", "rolling"])
        ok = False
        for a in _.A | case(_[_.A]):
            assert False, "case should not have matched"
        for x in case.default:
            ok = True
        assert ok, "flow should have passed through default"

        case = switch(_["they", "see", "me", "rolling"])
        for a in _.A |\
            case(_[_.A, _.B, _.C, _.D]):
            self.assertEqual(a, "they")
            break
        else:
            assert False, "case should have matched"
        for x in case.default:
            assert False, "default should not have been called"

        for a in _.A |\
            case(_[_.A, _.B, _.C, _.D]):
            assert False, "switch should have sought because of second use"

        case.reset()
        for a in _.A |\
            case(_[_.A, _.B, _.C, _.D]):
            break
        else:
            assert False, "should have been in"

        case.reset()
        for x in case.default:
            break
        else:
            assert False, "should have been in default"

        case = switch(_[1, "2", _._3])
        for l in case(_[_.A, _.B, _.C]):
            self.assertEqual(l, _[1, "2", _._3])
            break
        else:
            assert False, "should have matched"

        case = switch(_[1, "2", _._3])
        for [a, b] in [_.A, _.B] | case(_[_.A, _.B, _.C]):
            self.assertEqual([a, b], [1, "2"])
            break
        else:
            assert False, "should have matched"

        case = switch(_[1, "2", _._3])
        for (a, b) in (_.A, _.B) | case(_[_.A, _.B, _.C]):
            self.assertEqual((a, b), (1, "2"))
            break
        else:
            assert False, "should have matched"

    def testPyPreds(self):
        pred = Predicate("pred")
        pred(1).known_when(true, false)
        pred(2).known()
        pred(3).known()
        assert IsFrom(cons("a", nil), cons).ever()
        assert Not(IsFrom(cons("a", nil), cons)).never()
        assert Not(Not(IsFrom(cons("a", nil), cons))).ever()
        assert Equal(cons(_.A, 4), cons(3, _.A)).never()
        assert Equal(cons(_.A, 3), cons(3, _.A)).ever()
        assert Equal(pred(_.A, 2, _.B), pred(1, _.B, _.A)).never()
        assert pred(1).never()
        self.assertEqual(pred(2).all(), [{}])
        self.assertEqual(pred(_.A).all(_.A), [2, 3])
        self.assertEqual(pred(1).fill(), None)

    def testPeach(self):
        def square(x):
            return x*x
        self.assertEqual(peach(_[1, 2, 3], square), [1, 4, 9])
        self.assertEqual(peach(nil, square), [])

    def testSyntacticSugar(self):
        pred = Predicate("pred")
        pred["a"]
        pred[_.A] = Equal(_.A, 3)
        pred["a", "b"]
        pred[_.A, _.B] = Equal(_.A, _.B)
        pred[_.A, _.B] = Equal(_.A, 1), Equal(_.B, 2)
        assert pred(_.A)
        assert pred(3)
        assert pred(_.A, _.B)
        assert not pred(_.A, _.B, _.C)
        assert pred(1, 2)
        assert pred(true, true)
        assert pred(false, false)

        append = Predicate("append")  # Create a predicate
        append[nil, _.L, _.L]
        append[cons(_.H, _.T), _.L2, cons(_.H, _.L3)] = \
            append(_.T, _.L2, _.L3)

        self.testAppend(append)


if __name__ == "__main__":
    main()
