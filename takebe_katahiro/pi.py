# -*- coding: utf-8 -*-

import sys
import operator as op
import math

"""
π^2 = 9 * (1 + 1^2/(3*4) + (1*2)^2/(3*4*5*6) + (1*2*3)^2/(3*4*5*6*7*8) + ...)
    = 9 * ( lim k→∞ S(k) )
where
S(k) = if k=0:
           1
       else
           (1*...*k)^2 / (3*...*(2+2k))
"""
def s(k):
    if k <= 0:
        return 1
    try:
        numer = pow(sum(range(1, k+1)), 2)
        denom = reduce(op.mul, range(3, 3+2*k))
        res = float(numer) / float(denom)
        sys.stderr.write("#### s(k): %s = %s / %s\n"
                         %(res, float(numer), float(denom)))
    except OverflowError:
        return 0
    return res

"""
π^2 = 9 * (1 + 1^2/(3*4) + (1*2)^2/(3*4*5*6) + (1*2*3)^2/(3*4*5*6*7*8) + ...)
    = 9 * (1 + 1^2/(3*4) + (1^2/(3*4) * 2^2/(5*6)) + (1^2/(3*4) * 2^2/(5*6) * 3^2/(7*8))
    = 9 * ( lim k→∞ T(k) )
where
T(k) = if k=0:
           1
       else:
           1^2/(3*4) *...* k^2/((2+2k)*(1+2k))
           = U(1)*U(2)*...*U(k)
"""
def t(k):
    if k <= 0:
        return 1
    try:
        us = [u(i) for i in range(1, k+1)]
        res = reduce(op.mul, us)
        sys.stderr.write("#### t(k): %s\n" %(res))
        return res
    except OverflowError:
        return 0
def u(k):
    numer = pow(k,2)
    denom = (2+2*k)*(1+2*k)
    res = float(numer) / float(denom)
    #sys.stderr.write("#### u(k): %s = %s / %s\n"
    #                 %(res, float(numer), float(denom)))
    return res

def pi_square(n, func=t):
    res = 0
    for i in range(n):
        res += func(i)
        sys.stderr.write("## 9*res: %s\n" %(9*res))
    return 9*res

def main():
    N = 100
    func = t
    print math.sqrt( pi_square(N, func) )

if __name__ == '__main__':
    main()
