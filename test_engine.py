from engine import Engine
import unittest

class TestEngine(unittest.TestCase):
    def assertSomeNearValue(self, actual, vals, tolerance, far_count):
        proximity_count = 0
        for i in range(len(actual)):
            if actual[i] < vals[i] - (tolerance*vals[i]):
                proximity_count+=1
        if proximity_count > far_count:
            raise AssertionError("actual " + str(actual[i]) + "is not near value " + str(vals[i]) + " with tolerance " + str(tolerance))

    def testNearMeanLessThanAllowed(self):
        e=Engine([1,1], [0.01,0.01], 5, 0.75)
        e.initialize()
        e.run()
        print("fittest :")
        print(e.fittest())
        self.assertSomeNearValue(e.fittest(), [1,1], 0.05, 0)

    def testNearMeanLessThanAllowedLargeVariance(self):
        e=Engine([1,1], [1,1], 5, 0.75)
        e.initialize()
        e.run()
        print("fittest :")
        print(e.fittest())
        self.assertSomeNearValue(e.fittest(), [1,1], 0.05, 0)

    def testSomeNearMeanLessThanAllowed(self):
        e=Engine([100,100], [25,10], 120, 0.40)
        e.initialize()
        e.run()
        print("fittest :")
        print(e.fittest())
        self.assertSomeNearValue(e.fittest(), [100,100], 0.05, 1)

    def testSomeNearMeanLessThanAllowedDiffMean(self):
        e=Engine([50,100], [25,10], 110, 0.40)
        e.initialize()
        e.run()
        print("fittest :")
        print(e.fittest())
        self.assertSomeNearValue(e.fittest(), [50,100], 0.05, 1)
