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
        self.max_links = max_links + 1
        self.rerun = rerun

        # testing sets
        self.test_set = [i for i in range(0, self.max_links, self.increment)]
        self.test_set[0] = 1 # ensure at least one link is tested

        # run tests
        self.start = time.time()
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
        results = np.zeros(shape = (self.rerun, len(self.test_set)) )

        for ind, i in enumerate(self.test_set):
            i_results = []
            print(f"Running {fn.__name__} with {i} links")
            for j in range(self.rerun):

                start = time.time()

                asyncio.run( fn(self.links[:i]) )

                end = time.time()

                i_results.append(end - start)

            results[:,ind] = i_results

        return results


    def plot(self, fn_results):
        "Plot the results"

        fig, ax = plt.subplots(figsize= (16,12), nrows=2, ncols=2)

        test_set = np.array([self.test_set])
        test_set = np.repeat(test_set, repeats = self.rerun, axis=0)


        for fn, results in fn_results.items():

            mean_results_nonorm = np.mean(results, axis=0)
            results_norm = np.divide(results, test_set) # divide by number of links
            links_per_sec = 1 / results_norm # links per second

            # mean, median, max per link
            mean_results = np.mean(results_norm, axis=0)
            median_results = np.median(results_norm, axis=0)
            max_results = np.max(results_norm, axis=0)

            # stats on computation time
            var_results = np.var(results, axis=0) * ((self.rerun) / (self.rerun-1)) # sample sd
            sd_results = np.sqrt(var_results)

            lower_ci = np.divide((mean_results_nonorm - 1.96 * (sd_results) / np.sqrt(self.rerun)), test_set[0])
            upper_ci = np.divide((mean_results_nonorm + 1.96 * (sd_results) / np.sqrt(self.rerun)), test_set[0])

            # Plot results
            # =================

            # mean
            ax[0,0].plot(self.test_set, mean_results, label=f'{fn}')
            # confidence interval
            ax[0,0].fill_between(self.test_set, lower_ci, upper_ci, alpha=0.2)
            ax[0,0].set_title('Average time taken per link')
            ax[0,0].set_yscale('log')
            ax[0,0].legend(loc=0)

            # median & max
            ax[0,1].plot(self.test_set, median_results, label=f'{fn}-median')
            ax[0,1].plot(self.test_set, max_results, label=f'{fn}-max')
            ax[0,1].set_title('Time taken per link')
            ax[0,1].set_yscale('log')
            ax[0,1].legend(loc=0)

            # std - will be url in future
            ax[1,0].plot(self.test_set, sd_results, label=f'{fn}')
            ax[1,0].set_title('Standard deviation of computation')

            # links per second
            ax[1,1].plot(self.test_set, np.mean(links_per_sec, axis=0), label=f'{fn}')
            ax[1,1].set_title('Average links per second')
            

        end_time = time.time()
        print(f"Total time taken: {end_time - self.start}")

        plt.show()


    def load_links(self):
        "Load links from file into a list"
        with open('links.txt', 'r') as f:
            self.links = f.read().splitlines()


if __name__ == '__main__':

    fig = async_eval([af.gather_links], increment=50, 
               max_links=800, rerun=5)