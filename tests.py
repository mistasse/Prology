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
            cross(plist(_.a, _.a), plist(_.b, 1)).dfs(),
            cross(plist(1, 1), plist(1, 1))
            )
        self.assertEqual(
            cross(plist(_.b, 1), plist(_.a, _.a)).dfs(),
            cross(plist(1, 1), plist(1, 1))
            )

    def testAppend(self):
        append = Predicate("append")
        append(nil, _.L, _.L).known()
        append(cons(_.H, _.T), _.L2, cons(_.H, _.L3)).known_when(
            append(_.T, _.L2, _.L3)
        )
        self.assertEqual(append(plist(1, 2, 3), plist(4, 5), _.Z).dfs(), append(plist(1, 2, 3), plist(4, 5), plist(1, 2, 3, 4, 5)))

        self.assertEqual(append(_.X, plist(4, 5), plist(1, 2, 3, 4, 5)).all(), [{_.X: plist(1, 2, 3)}])
        answers = append(_.X, _.Y, plist(1, 2, 3, 4, 5)).all()
        self.assertEqual(len(answers), 6)
        self.assertIn({_.X: plist(1, 2, 3, 4, 5), _.Y: plist()}, answers)
        self.assertIn({_.X: plist(1, 2, 3, 4), _.Y: plist(5)}, answers)
        self.assertIn({_.X: plist(1, 2, 3), _.Y: plist(4, 5)}, answers)
        self.assertIn({_.X: plist(1, 2), _.Y: plist(3, 4, 5)}, answers)
        self.assertIn({_.X: plist(1), _.Y: plist(2, 3, 4, 5)}, answers)
        self.assertIn({_.X: plist(), _.Y: plist(1, 2, 3, 4, 5)}, answers)


if __name__ == "__main__":
    main()
