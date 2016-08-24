from prology import *
_ = L
from unittest import main, TestCase


class Test(TestCase):

    def testRebind(self):
        pass

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

    def testAppend(self):
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




if __name__ == "__main__":
    main()
