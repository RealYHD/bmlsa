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
        """Instantiates a :obj:bmlsa.datatypes.QuerySequence object

        :param id: The id of the query sequence
        :type id: str
        :param sequence: The sequence itself
        :type sequence: str
        :param name: The name of the sequence, defaults to None
        :type name: str, optional
        :param description: The description of the sequence, defaults to None
        :type description: str, optional
        :param start: The start of the sequence, defaults to None
        :type start: int, optional
        :param end: The end of the sequence, defaults to None
        :type end: int, optional
        :param score: The alignment score of the sequence, defaults to None
        :type score: int, optional
        """
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
