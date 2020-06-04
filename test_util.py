import unittest
from util import fitness
from scipy.stats import multivariate_normal

class TestUtils(unittest.TestCase):
    def testFitnessNearMean(self):
        self.assertEqual(fitness([1],[1],[0.1],2)[0], multivariate_normal.pdf(0))

    def testFitnessFarFromMean(self):
        self.assertEqual(fitness([5],[1],[0.1],2)[0], -1)
        self.assertEqual(fitness([5,5],[1,1],[0.1,0.1],3)[0], -2)

    def testFitnessNotNearEnough(self):
        self.assertGreaterEqual(fitness([0.5],[1],[0.1],1)[0], 0)

    def testFitnessTooFar(self):
        self.assertLessEqual(fitness([1.5],[1],[0.1],1)[0], 0)
