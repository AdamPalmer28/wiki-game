"""Used for evaluating different async methods and functions for the link_handler.py module"""
from matplotlib import pyplot as plt
import numpy as np
import time
import asyncio

import async_functions as af

class async_eval:

    def __init__(self, list_of_funcs, increment=25, max_links=1000, rerun=3):

        self.funcs = list_of_funcs
        self.load_links() 

        # testing parameters
        self.increment = increment
        self.max_links = max_links

        # testing sets
        self.test_set = [i for i in range(0, self.max_links, self.increment)]
        self.test_set[0] = 1 # ensure at least one link is tested

        # run tests
        self.run()


    def run(self):
        "Main loop - testing all functions"
        fn_results = {}
        for fn in self.funcs:
            results = self.run_fn(fn)

            fn_results[fn.__name__] = results # store results

        self.plot(fn_results)

    def run_fn(self, fn):
        "Run a single function returning the time taken"
        results = np.zeros(shape = (len(self.test_set), self.rerun) )

        for i in self.test_set:
            i_results = []
            print(f"Running {fn.__name__} with {i} links")

            start = time.time()

            asyncio.run( fn(self.links[:i]) )

            end = time.time()

            results.append(end - start)

        return results

    def plot(self, fn_results):
        "Plot the results"
        fig, ax = plt.subplots(figsize= (8,6))

        for fn, results in fn_results.items():
            ax.plot(self.test_set, results, label=fn)

        ax.set_xlabel('Number of links')
        ax.set_ylabel('Time taken (s) per link')

        plt.show()


    def load_links(self):
        "Load links from file into a list"
        with open('links.txt', 'r') as f:
            self.links = f.read().splitlines()


if __name__ == '__main__':

    async_eval([af.gather_links])
