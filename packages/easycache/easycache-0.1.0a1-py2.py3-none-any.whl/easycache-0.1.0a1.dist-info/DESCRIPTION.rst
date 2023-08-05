Copyright 2017 Jeff Ward

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
either express or implied. See the License for the specific
language governing permissions and limitations under the License.


This is an extremely *basic* implementation of a value and function cache. There are better tools out there I am sure.
It is in initial development so there are likely major bugs. I may update this as I use it more, but you are safest
expecting no further updates.

The intent behind this package is to provide something that in one line decorates a function call to, as transparently
as possible, cache its results. The use case I built this around was searching hyperparameters. By wrapping your
model call in this cache you can quickly implement either random search, or even MCTS, where previously generated
results are automatically re-loaded without putting custom caching logic into your code. Additionally, if you
are performing grid searches with parameter values from a-c and later realizae you wanted to search from a-m then
using this function cache allows you to re-test and automatically re-load existing results while only calculating
new results.

A simple example::

    import easycache as ec
    import time


    def myExpensiveFunction(cost):
        time.sleep(cost)
        print("This was expensive!")
        return cost

    def gridSearchExample(paramA, paramB):
        """ Simulates a grid search over parameter values

        :param paramA: list of values
        :param paramB: list of values
        :return:
        """
        cachedEF = ec.cacheFunction(myExpensiveFunction, 'example.pkl', name="myExpensiveFunction")

        bestValue = None
        bestA = None
        bestB = None
        for a in paramA:
            for b in paramB:
                newValue = cachedEF(a+b)
                if bestValue is None or newValue > bestValue:
                    bestValue = newValue
                    bestA = a
                    bestB = b
        return bestValue, bestA, bestB

    print("Best Value={} using A={} and B={}".format(*gridSearchExample([.1, .2], [.01, .02])))

    #Oh, we REALLY should have searched more! This should only run the 2 new tests
    print("Best Value={} using A={} and B={}".format(*gridSearchExample([.1, .2], [.01, .02, .003])))

Of course you can do other things::

    def runClass(cache):
        print("Cached Value={}", cache.someValue)
        #Assignment will flush the cache.
        #If this is a complex object you will need to manually flush if internal state changes
        cache.someValue = 12
        print("Cached Value={}", cache.someValue)
        print("peek={}".format(cache.myExpensiveFunction(.5, mode="cache_peek")))
        cache.myExpensiveFunction(.5)

    def classExample():
        cache = ec.EasyCache("exampleClass.pkl")
        cache.clearCache()
        cache.cacheFunction(myExpensiveFunction, name="myExpensiveFunction")
        cache.cacheProperty("someValue", initialValue=42)
        runClass(cache)
        runClass(cache)
        cache.myExpensiveFunction(.5,mode="force_run")
        cache.myExpensiveFunction(.5,mode="cache_clear")
        cache.myExpensiveFunction(.5)
        del cache.someValue
        del cache.myExpensiveFunction

    classExample()



