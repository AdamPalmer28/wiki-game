"""Used for evaluating different async methods and functions for the link_handler.py module"""

from matplotlib import pyplot as plt

class async_eval:
    full_url = 'https://en.wikipedia.org/wiki/'
    def __init__(self, list_of_funcs):

        self.funcs = list_of_funcs

    def load_links(self):
        "Load links from file"
        pass

    def run(self):
        "Main loop - testing all functions"
        pass

    def run_fn(self, fn):
        "Run a single function returning the time taken"
        pass

    def plot(self):
        "Plot the results"
        pass

