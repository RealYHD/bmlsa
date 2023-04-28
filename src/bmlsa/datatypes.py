class QuerySequence:
    """Represents a sequence that may be aligned."""

    def __init__(
        self,
        id: str,
        sequence: str,
        name: str = None,
        description: str = None,
        start: int = None,
        end: int = None,
        score: int = None,
    ) -> None:
        self._description = description
        self._start = start
        self._end = end
        self._id = id
        self._name = name
        self._sequence = sequence.replace("\n", "").replace("\r", "")
        self._score = score

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def sequence(self):
        return self._sequence

    @property
    def score(self):
        return self._score
