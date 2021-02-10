class LeanHtml:
    def __init__(self, start, theorem_proof):
        """

        :param start: List containing the open/import before the proof
        :param theorem_proof: proof
        """
        self.start = start
        self.theorem_proof = theorem_proof

    def to_html(self):
        raise NotImplementedError
