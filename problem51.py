#!/usr/bin/python

#http://projecteuler.net/index.php?section=problems&id=51

#SUMMARY:
##it seems like these problems are getting us to think about
##equivalence relations.  in this case, the equivalence class is defined by
##a collection of indices which are variable and a set of integers occupying
##numbers at the non-variable indices.  For example, [1,2,4,6],[2,4]
##defines the class [1,2,*,4,*,6].
##or maybe that is wrong.  who knows.

##OPTIMIZATION EMPLOYED:
##Suppose that I come across the number [1,2,3,4,5,6], where indices [2,4]
##are variable.  Then, i will look at the numbers of the form [1,2,*,4,*,6],
##checking for an 8-prime-family.
##If I later examine the number [1,2,9,4,9,6] where indices [2,4] are varaible,
##I would also be examining the class [1,2,*,4,*,6].  SO, if i were smart,
##I would recognize that the pair ([1,2,4,6],[2,4]) was already used,
##and not bother computing with it.  The way I optimize is to only look at
##the elements of the class which are greater than the number being plugged in


import sys
sys.path.append("..")
import math as m
import prime as p
import itertools as i
import time


#assume answer < 1000000
#and if it's not, well, try again!
#i could wrap the whole thing in some loop that increases the count of the primes...
primes=p.primes_under(1000000)
print "primes calculated.  starting cool stuff"


class NumChangeEquivalenceClass:
    """
    (equivalence)CLASS definition:

    EXAMPLE:
    For the class [1,2,*,4,*,6], we will have:
    var_indices=[2,4]
    and digit_list=[1,2,-1,4,-1,6].
    elements is everything in [1,2,*,4,*,6]
    """


    def __init__(self,seed,var_indices):
        """seed, in conjunction with var_indices, defines the class"""
        self._seed=seed
        self.var_indices=var_indices
        self.digit_list=self.get_digit_list(seed,var_indices)
        self.elements=self.get_elements()


    def get_elements(self):
        """figure out the members of [1,2,*,4,*,6]"""
        rtn_val=[]

        for x in range(10):
            cur_member=[x if d<0 else d for d in self.digit_list]
            rtn_val.append(self.list_to_num(cur_member))
        return rtn_val
    
    
    def list_to_num(self,l):
        """
        turn a list of integers to the corresponding number
        [1,2,3]->123
        """
        #print l
        return reduce(lambda x,y: x*10+y,l)

    
    def get_digit_list(self,seed,var_indices):
        """
        get a list of the static digits from the seed
        and var_indices constructor args
        """
        seed_as_list=self.get_list_from_num(seed)
        return [-1 if i in var_indices else seed_as_list[i] for i in range(len(seed_as_list))]
    
    def get_list_from_num(self,x):
        """
        turn an integer to a list of digits
        123->[1,2,3]
        """
        #this is probably really really awful behind the scenes...
        #the idea of converting an integer to a string is offputting to me...
        return map(lambda i:int(i),list(str(x)))
    
    def is_in_eight_prime_fam(self):
        """
        check if the current equivalence class is the winner.
        iterate through elements,
        counging how many primes exist.
        """
        count=0
        misses=0
        #this is the optimization discussed at top
        greater_than_seed_elts=filter(lambda(x):x>=self._seed,self.elements)
        #begin counting primes
        if len(greater_than_seed_elts)>=8:
            for x in greater_than_seed_elts:
                if x in primes:
                    count +=1
                else:
                    misses+=1
                if misses > 2:
                    #short circuit!
                    break
        #check if count was adequate
        if (count<8):
            return False
        else:
            return True


    
    def signature(self):
        """
        return a tuple containing the static digits and a list of
        variable indices.  this uniquely defines the class
        """
        static_digits=[]
        for x in self.digit_list:
            if x >=0:
                static_digits.append(x)
        num_representing_static_digits=self.list_to_num(static_digits)
        return (num_representing_static_digits,self.var_indices[:])


#begin SCRIPTING

#make a dictionary where key N maps to
#proper subsets of [1,2,...N]
indices_list=[0,1,2,3,4,5,6]
proper_subsets_dict={}




def get_proper_subsets(l):
    """get the proper subsets of a list"""
    length=len(l)
    rtn_val=[]
    for x in range(1,length):
        cur_iterator=i.combinations(l,x)
        for y in cur_iterator:
            rtn_val.append(y)
    return rtn_val


#proper_subsets_dict maps a length "l" to all subsets of the list "range(l)"
for x in range(1,7):
    proper_subsets_dict[x]=get_proper_subsets(range(x))

start_time=time.clock()
#use pre existing stufff to SOLVE PROBLEM
found=False
for cur_prime in primes:
    #for each prime in the prime list,
    #look for all of the potential eight-prime families
    #by swapping out subsets of its digits.
    l=m.floor(m.log(cur_prime,10))+1
    subs=proper_subsets_dict[l]
    for indices_to_change in subs:
        #take cur_prime and indicesToChage, and generate
        #an object to represent the equivalence class
        cur_EQ_class=NumChangeEquivalenceClass(cur_prime,indices_to_change)
        if cur_EQ_class.is_in_eight_prime_fam():
            found=True
            print cur_prime
            print indices_to_change
            for x in cur_EQ_class.elements:
                if x in primes:
                    print x
            break
    if found:
        break

end_time=time.clock()
print "after calculating primes, the program took %(time)f seconds to complete" % {"time": end_time-start_time}
print cur_EQ_class.signature()
