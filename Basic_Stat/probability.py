# coding: utf-8
from collections import Counter
import math, random
import matplotlib.pyplot as plt

"""
[DS from scaratch] chap.6 probability/確率
"""

# [6.1]従属と独立
# P(E, F) = P(E)P(F)

# [6.2]条件付き確率
# P(E|F) = P(E, F) / P(F)

# (e.f.)家族構成
def random_kid():
    return random.choice(["boy", "girl"])


def uniform_pdf(x):
    return 1 if ( x >= 0 and x < 1 ) else 0


# 累積分布関数(cumulative distributuion function:cdf)
def uniform_cdf(x):
    "returns the probabolity that a uniform random variable is less than x"
    if x < 0:   return 0     # uniform random is never less than 0
    elif x < 1: return x     # e.g. P(x < 0.4) = 0.4
    else:       return 1     # uniform random is always less than 1


""" [6.6]正規分布 """
def normal_pdf(x, mu = 0, sigma = 1):
    sqrt_two_pi = math.sqrt(2 * math.pi)
    return ( math.exp(-(x-mu) ** 2 / 2 / sigma ** 2 ) / (sqrt_two_pi * sigma) )


def plot_normal_pdfs(plt):
    xs = [x / 10.0 for x in range(-50, 50)]
    plt.plot(xs, [normal_pdf(x, sigma = 1) for x in xs], '-', label = 'mu=0, simga=1')
    plt.plot(xs, [normal_pdf(x, sigma = 2) for x in xs], '-', label = 'mu=0, simga=2')
    plt.plot(xs, [normal_pdf(x, sigma = 0.5) for x in xs], '-', label = 'mu=0, simga=0.5')
    plt.plot(xs, [normal_pdf(x, mu = -1) for x in xs], '-', label = 'mu=-1, simga=1')
    plt.legend()
    plt.title("Various Normal pdfs")
    plt.show()
            

def normal_cdf(x, mu = 0, sigma = 1):
    # [math.erf] https://docs.python.jp/3/library/math.html
    # gaussian の類軌跡分布関数がerror function
    return ( 1 + math.erf((x - mu) / math.sqrt(2) / sigma ) ) / 2 


def plot_normal_cdfs(plt):
    xs = [x / 10.0 for x in range(-50, 50)]
    plt.plot(xs, [normal_cdf(x, sigma = 1) for x in xs], '-', label = 'mu=0, simga=1')
    plt.plot(xs, [normal_cdf(x, sigma = 2) for x in xs], '-', label = 'mu=0, simga=2')
    plt.plot(xs, [normal_cdf(x, sigma = 0.5) for x in xs], '-', label = 'mu=0, simga=0.5')
    plt.plot(xs, [normal_cdf(x, mu = -1) for x in xs], '-', label = 'mu=-1, simga=1')
    plt.legend(loc=4)
    plt.title("Various Normal cdfs")
    plt.show()
   

def inverse_normal_cdf(p, mu = 0, sigma = 1, tolerance = 0.00001):
    """ 
    find approximate inverse using binary search 
    二部探索を用いて，逆関数の近似値をを計算
    """
    
    # 標準正規分布でない場合，標準正規分布からの差分を求める
    if mu != 0 or sigma != 1:
        return mu + sigma * inverse_normal_cdf(p, tolerance = tolerance)

    low_z, low_p = -10.0, 0          # normal_cdf(-10) is (very close to) 0
    hi_z, hi_p   =  10.0, 1          # normal_cdf(-10) is (very close to) 1
    while hi_z - low_z > tolerance:
        mid_z = (low_z + hi_z) / 2   # midpoint
        mid_p = normal_cdf(mid_z)    # and the cdf's value there
        if mid_p < p:
            # midpoint is still too low, search above it
            low_z, low_p = mid_z, mid_p
        elif mid_p > p:
            # midpoint is still too high, search below it
            hi_z, hi_p = mid_z, mid_p
        else:
            break

    return mid_z


# [6.7]中心極限定理
# 非常に多数の独立で同一の分布に従う確率変数の平均として定義される確率変数は，おおよそ正規分布に従う
def bernoulli_trial(p):
    """
    2種類の可能な結果(S, F)を観測し，それらの確率をp, 1-pとする．
    n回(S:x回, F:n-x回)繰り返す. 
    f(x) = nCx * p**x * (1-p)**(n-x)
    """
    return 1 if random.random() < p else 0


def binomial(p, n):
    """
    E(x) = np
    V(x) = np(1-p)
    """
#    使わない返り値に変数を割り当てるのはナンセンス->アンダースコアで無視
#    代入後に参照されない変数は変数名 _ or dummy を使う
    return sum(bernoulli_trial(p) for _ in range(n))


def make_hist(p, n, num_points):

    # 二項分布をプロット
    data = [binomial(p, n) for _ in range(num_points)]

    # https://qiita.com/hatchinee/items/a904c1f8d732a4686c9d
    histogram = Counter(data)
    plt.bar([ x - 0.4 for x in histogram.keys() ], # get key
            [ v / num_points for v in histogram.values() ], # get value
            0.8,
            color = '0.75')

    mu = p * n
    sigma = math.sqrt(n * p * (1-p))

    # 正規分布の近似曲線をプロット
    xs = range(min(data), max(data) + 1)
    ys = [normal_cdf(i + 0.5, mu, sigma) - normal_cdf(i - 0.5, mu, sigma)
          for i in xs]
    plt.plot(xs, ys)
    plt.title("Binomial Distribution vs. Normal Approximation")
    plt.show()
  

if __name__ == '__main__':

    #
    # Conditional probability
    #

    both_girls = 0
    older_girl = 0
    either_girl = 0

    random.seed(0)
    for _ in range(10000):
        younger = random_kid()
        older = random_kid()
        if older == "girl":
            older_girl += 1
        if older == "girl" and younger == "girl":
            both_girls += 1
        if older == "girl" or younger == "girl":
            either_girl += 1

    print("P(both | older(1人目がfemale)):", both_girls / older_girl)  # 0.514 ~ 1/2
    print("P(both | either(どちらかがfemale)):", both_girls / either_girl) # 0.342 ~ 1/3


    plot_normal_pdfs(plt)
    plot_normal_cdfs(plt)

    make_hist(0.75, 100, 100000)
    #    make_hist(0.2, 5, 10000)
    
#    print(normal_pdf(50, 5, 1))
