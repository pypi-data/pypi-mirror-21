from collections import defaultdict

class realign:

    def __init__(self):
        self.sequence = ""
        self.precursors = defaultdict(isomir)
        self.score = []
        self.best_hits = [] # maybe sam object?

    def set_precursor(self, precursor, isomir):
        self.precursors[precursor] = isomir

    def remove_precursor(self, precursor):
        del self.precursors[precursor]

class isomir:

    def __init__(self):
        self.t5 = []
        self.t3 = []
        self.add = []
        self.subs = []
        self.align = None
        self.start = 0
        self.mirna = None

    def format(self, sep="\t"):
        subs = "".join(["".join(map(str, mism)) for mism in self.subs])
        if not subs:
            subs = "0"
        add = "0" if not self.add else self.add
        return "%s%s%s%s%s%s%s" % (subs, sep, add, sep,
                                   self.t5, sep, self.t3)

    def format_id(self, sep="\t"):
        subs = ["".join(["".join([c[2], str(c[0]), c[1]]) for c in self.subs])]
        if not subs:
            subs = []
        add = [] if not self.add else ["e%s" % self.add]
        t5 = ["s%s" % self.t5] if self.t5 and self.t5 != "NA" else []
        t3 = ["%s" % self.t3] if self.t3 and self.t3 != "NA" else []
        full = t5 + subs + t3 + add
        return sep.join([f for f in full if f])

    def get_score(self, sc):
        for a in self.add:
            if a in ['A', 'T']:
                sc -= 0.25
            else:
                sc -= 0.75
        for e in self.subs:
            sc -= 1
        return sc
