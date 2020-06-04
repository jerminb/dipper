import numpy
from scipy.stats import multivariate_normal

def maxSumLessthanStep(vals, means, covs, maxVal):
    sumMaxs = sum(max(v, m+(5*c)) for v,m,c in zip(vals,means,covs))
    return -1*len(means) if (float(sum(v for v in vals))/float(sumMaxs)) - (float(maxVal)/float(sumMaxs)) > 0 else 0

def constraint(dist, maxAllowed):
    dt = dist.transpose()
    return maxSumLessthanStep(dt[0], dt[1], dt[2], maxAllowed)

def fitness(individual, mean, stdev, maxAllowed):
    dist = numpy.array([(i, m, s) for i,m,s in zip(individual, mean, stdev)])
    normDist = numpy.array([(v[0] - v[1])/v[2] for v in dist])
    return sum(multivariate_normal.pdf(v) for v in normDist) + constraint(dist, maxAllowed),


def househouldPersonCalculator(val):
  return (0.2*val)+0.6 if val < 2 else (0.6*val)-0.2
