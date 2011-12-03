#!/usr/bin/python
import copy
import math

def eliminate_factor(x,d):
    """
    return x/K where K is the largest exponentiation  of d dividing x
    """
    assert (x==int(x)), "argument must be an integer"
    if(x % d != 0):
        return x
    else:
        return eliminate_factor(x/d, d)

def unique_factors(x, potential_factors=None):
    """
    what are teh unique factors of x?
    """
    assert (x==int(x)), "argument must be an integer"
    if potential_factors==None:
        potential_factors=get_potential_prime_factors(x)
    unique_factors=set()
    for p in potential_factors:
        if(p<x) and x%p == 0:
            unique_factors.add(p)
    return unique_factors

#self-explanatory
def smallest_divisor(x):
    assert (x==int(x)), "argument must be an integer"
    i=2
    while ((x%i) != 0):
        i = i+1
    return i

#largest power of d which divides x
#this scales about linearly with the sum of x's factors...
def find_largest_factor(x):
    assert (x==int(x)), "argument must be an integer"
    last_divisor=x
    while(x!=1):
        last_divisor = smallest_divisor(x)
        x = eliminate_factor(x, last_divisor)
    return last_divisor

#self-explanatory.  could stand to use a binary search!
#but it's probably not going to be your bottleneck...
def max_dividing_power(x,d):
    assert (x==int(x)), "argument must be an integer"
    d_exp=0
    while x%d == 0:
        d*=d
        d_exp = d_exp + 1
    return d_exp
    
def get_factor_dict(x,potential_factors=None):
    """
    asssuming potential_factors contains all of the
    divisors of x, return a dictionary mapping divisors
    to powers in factorization
    """
    assert (x==int(x)), "argument must be an integer"
    if potential_factors==None:
        potential_factors=get_potential_prime_factors(x)
    sqrt = math.sqrt(x)
    factor_dict = {}
    #use a generator, in case the user supplied the
    #first billion primes.  hopefully theyre sorted
    for d in (f for f in potential_factors if f<=sqrt):
        if x % d == 0:
            max_pow = max_dividing_power(x, d)
            factor_dict[d] = max_pow
            x= x/(d**max_pow)
        if x==1:
            break
    if x>1:
        #think of 77 here.  7 goes away and youre left with 11.
        #note that there can only be one divisor greater than the square root..
        factor_dict[x]=1
    return factor_dict


def primes_under(x):
    """
    Find all the primes under x, by eliminating
    composite numbers less than x
    this should be optimized...
    """
    assert (x==int(x)), "argument must be an integer"
    rtn_val=set(range(2,x))
    sqrt=int(math.sqrt(x))
    #any composite less than x will have
    #some divisor less than its own square root,
    #consequently, less than square root of x
    #as square root is monotonic in its argument
    for i in range(2,sqrt+1):
        if i in rtn_val:
            rtn_val=elim_strict_multiples(rtn_val,i,x)
    return rtn_val


def primes_between(a,b,primes_under_a):
    """
    find all the primes between a and b, given all primes <=a
    Note: primes_under_a must be a SET or at least implement UNION
    """
    assert (a==int(a) and b==int(b)), "argument must be an integer"
    range_between_endpts=range(a+1,b)
    set_between_endpts=set(range_between_endpts)
    #any composite less than b will have some divisor less than
    #square root of b
    sqrt=int(math.sqrt(b))
    potential_divisors=[d for d in primes_under_a.union(range_between_endpts) if d<=sqrt]
    for d in potential_divisors:
        set_between_endpts=elim_strict_multiples(set_between_endpts,d,b)
    return set_between_endpts

def get_potential_prime_factors(x):
    assert int(x)==x, "argument must be an integer"
    return primes_under(int(math.sqrt(x))+1)

def primes_generator(grow_upper_bound=lambda x: x*2):
    """
    yields all of the primes, yo!
    this is pretty sick.
    """
    cur_primes=[2,3,5,7]
    #we maintain a separate set which matches cur_primes,
    #this is because i want to avoid constantly casting to a set
    #wheen calling primes_between
    cur_primes_set=set(cur_primes)
    cur_idx=0
    cur_max_idx=3
    while True:
        cur_prime=cur_primes[cur_idx]
        yield cur_prime
        while cur_idx==cur_max_idx:
            new_upper_bound=grow_upper_bound(cur_prime)
            new_primes_set=primes_between(cur_prime,new_upper_bound,cur_primes_set)
            new_primes=list(new_primes_set)
            new_primes.sort()
            cur_primes=cur_primes+new_primes
            cur_primes_set=cur_primes_set.union(new_primes_set)
            cur_max_idx+=len(new_primes)
        cur_idx+=1

def elim_strict_multiples(potential_multiples,base,upper_bound):
    """
    take an iterable of numbers (potential_multiples),
    return a set containing all of the contents of potential_multiples
    with all elements removed which are greater than base, multiples of base,
    and less than upper_bound
    """
    rtn_val=set(potential_multiples)
    cur_multiple=2*base
    while cur_multiple<=upper_bound:
        rtn_val.discard(cur_multiple)
        cur_multiple+=base
    return rtn_val


if __name__ == "__main__":
    """
    poor-man's unit tests.
    useful tip: use a macro to copy all of the function signatures into another buffer,
    then check for tests you haven't written yet...
    """
    #test unary functions
    test_number=100
    large_test_number=test_number+100
    print "test number is ",str(test_number)
    print "large test number is ",str(large_test_number),"\n\n\n"

    factor_to_eliminate=3
    print "eliminate_factor {0} from {1}".format(factor_to_eliminate, test_number)
    print eliminate_factor(test_number,3),"\n"
    
    print "unique_factors of {0}".format(test_number)
    print unique_factors(test_number),"\n"
    
    print "smallest_divisor of {0}".format(test_number)
    print smallest_divisor(test_number)
    
    print "find_largest_factor of {0}".format(test_number)
    print find_largest_factor(test_number),"\n"
    
    div_power_arg=3
    print "max_dividing_power of {0} into {1}".format(div_power_arg,test_number)
    print max_dividing_power(test_number,3),"\n"
    
    print "get_factor_dict of {0}".format(test_number)
    print get_factor_dict(test_number),"\n"
    
    print "primes_under of {0}".format(test_number)
    print primes_under(test_number)
    primes_under_list=sorted(list(primes_under(test_number)))
    print "sorted",primes_under_list,"\n"
    
    print "primes_between {0} and {1}".format(test_number,large_test_number)
    print primes_between(test_number,large_test_number,primes_under(large_test_number))
    primes_between_list=sorted(list(primes_between(test_number,large_test_number,primes_under(large_test_number))))
    print "sorted",primes_between_list,"\n"
    
    print "get_potential_prime_factors of {0}".format(test_number)
    print get_potential_prime_factors(test_number),"\n"
    
    elim_mults_arg=3
    elim_mults_max=10
    print "elim_strict_multiples of {0} from 0-{1}".format(elim_mults_arg,elim_mults_max)
    print elim_strict_multiples(range(elim_mults_max),elim_mults_arg,elim_mults_max)
    
    print "fooling around with prime generation.  first prime after 1000000 is:"
    y=primes_generator(lambda x:x*10)
    c=0
    for x in y:
        if x>1000000:
            print x
            break
