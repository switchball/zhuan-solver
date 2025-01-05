

class MaybeResult(object):
    def __init__(self, result, prob):
        self.result = result
        self.prob = prob

    def __str__(self):
        return f"Result:{self.result} Prob:{self.prob}"