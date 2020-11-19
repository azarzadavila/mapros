import abc
from enum import Enum, auto
import xml.etree.ElementTree as ET


class Sentence(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def add_to_tree(self, parent):
        """
        Adds this element to build a XML representation of the sentence
        :param parent: instance of ET.Element
        :return: instance of ET.Element
        """
        pass

    @classmethod
    @abc.abstractmethod
    def build_from_tree(cls, element):
        """
        Builds an instance from the xml representation
        :param element: instance of ET.Element
        :return: instance of the current class
        """
        pass

    @abc.abstractmethod
    def substitute(self, var, new_var):
        """
        :param var:
        :param new_var:
        :return: new Sentence with the substitution
        """
        pass

    @abc.abstractmethod
    def is_free(self, var):
        """
        Checks if the variable is free in this sentence
        If the variable is not in the sentence it returns False
        :param var: Variable instance
        :return: True if var is free in the sentence, False otherwise
        """
        pass


class ConstantPredicate(Sentence):
    def __init__(self, symbol):
        self.symbol = symbol

    def add_to_tree(self, parent):
        tree = ET.SubElement(
            parent, "constantPredicate", attrib={"symbol": self.symbol}
        )
        return tree

    @classmethod
    def build_from_tree(cls, element):
        return cls(element.get("symbol"))

    def substitute(self, var, new_var):
        return self

    def is_free(self, var):
        return False

    def __eq__(self, other):
        return self.symbol == other.symbol

    def __str__(self):
        return self.symbol


class Predicate(Sentence):
    def __init__(self, symbol, *terms):
        self.symbol = symbol
        self.terms = list(terms)
        for term in self.terms:
            if not isinstance(term, Term):
                raise ValueError("incorrect term")

    def add_to_tree(self, parent):
        tree = ET.SubElement(parent, "predicate", attrib={"symbol": self.symbol})
        for term in self.terms:
            term.add_to_tree(tree)
        return tree

    @classmethod
    def build_from_tree(cls, element):
        return cls(
            element.get("symbol"), *[build_from_tree_term(child) for child in element]
        )

    def substitute(self, var, new_var):
        new_terms = [term.substitute(var, new_var) for term in self.terms]
        return Predicate(self.symbol, new_terms)

    def is_free(self, var):
        for term in self.terms:
            if term.is_free(var):
                return True
        return False

    def __eq__(self, other):
        if self.symbol != other.symbol:
            return False
        if len(self.terms) != other.terms:
            return False
        for term1, term2 in zip(self.terms, other.terms):
            if term1 != term2:
                return False
        return True

    def __str__(self):
        res = self.symbol + "("
        for term in self.terms:
            res += str(term) + ", "
        res += ")"
        return res


class UnaryConnectorSentence(Sentence):
    def __init__(self, connector, sentence):
        self.connector = connector
        self.sentence = sentence
        if not isinstance(connector, UnaryConnector):
            raise ValueError("incorrect connector")
        if not is_sentence(sentence):
            raise ValueError("incorrect sentence")

    def add_to_tree(self, parent):
        tree = ET.SubElement(
            parent, "unaryConnectorSentence", {"connector": self.connector.to_str()}
        )
        self.sentence.add_to_tree(tree)
        return tree

    @classmethod
    def build_from_tree(cls, element):
        return cls(
            UnaryConnector.from_str(element.get("connector")),
            build_from_tree_sentence(element[0]),
        )

    def substitute(self, var, new_var):
        return UnaryConnectorSentence(
            self.connector, self.sentence.substitute(var, new_var)
        )

    def is_free(self, var):
        return self.sentence.is_free(var)

    def __eq__(self, other):
        return self.connector == other.connector and self.sentence == other.sentence

    def __str__(self):
        return str(self.connector) + " (" + str(self.sentence)


class BinaryConnectorSentence(Sentence):
    def __init__(self, connector, sentence1, sentence2):
        self.connector = connector
        self.sentence1 = sentence1
        self.sentence2 = sentence2
        if not isinstance(connector, BinaryConnector):
            raise ValueError("incorrect connector")
        if not is_sentence(sentence1) or not is_sentence(sentence2):
            raise ValueError("incorrect sentence")

    def add_to_tree(self, parent):
        tree = ET.SubElement(
            parent,
            "binaryConnectorSentence",
            attrib={"connector": self.connector.to_str()},
        )
        self.sentence1.add_to_tree(tree)
        self.sentence2.add_to_tree(tree)
        return tree

    @classmethod
    def build_from_tree(cls, element):
        return cls(
            BinaryConnector.from_str(element.get("connector")),
            build_from_tree_sentence(element[0]),
            build_from_tree_sentence(element[1]),
        )

    def substitute(self, var, new_var):
        return BinaryConnectorSentence(
            self.connector,
            self.sentence1.substitute(var, new_var),
            self.sentence2.substitute(var, new_var),
        )

    def is_free(self, var):
        return self.sentence1.is_free(var) or self.sentence2.is_free(var)

    def __eq__(self, other):
        return (
            self.connector == other.connector
            and self.sentence1 == other.sentence1
            and self.sentence2 == other.sentence2
        )


class QuantifierSentence(Sentence):
    def __init__(self, quantifier, var, sentence):
        self.quantifier = quantifier
        self.var = var
        self.sentence = sentence
        if not isinstance(quantifier, Quantifier):
            raise ValueError("incorrect quantifier")
        if not isinstance(var, Variable):
            raise ValueError("incorrect variable")
        if not is_sentence(sentence):
            raise ValueError("incorrect sentence")

    def add_to_tree(self, parent):
        tree = ET.SubElement(
            parent,
            "quantifierSentence",
            attrib={"quantifier": self.quantifier.to_str()},
        )
        self.var.add_to_tree(tree)
        self.sentence.add_to_tree(tree)
        return tree

    @classmethod
    def build_from_tree(cls, element):
        return cls(
            Quantifier.from_str(element.get("quantifier")),
            Variable.build_from_tree(element[0]),
            build_from_tree_sentence(element[1]),
        )

    def substitute(self, var, new_var):
        if var == self.var:
            return self
        if new_var == self.var:
            raise ValueError("variable capture")
        return QuantifierSentence(
            self.quantifier, self.var, self.sentence.substitute(var, new_var)
        )

    def is_free(self, var):
        if self.var == var:
            return False
        return self.sentence.is_free(var)

    def __eq__(self, other):
        return (
            self.quantifier == other.quantifier
            and self.var == other.var
            and self.sentence == other.sentence
        )


class Term(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def add_to_tree(self, parent):
        """
        Adds this element to build a XML representation of the term
        :param parent: instance of ET.Element
        :return: instance of ET.Element
        """
        pass

    @classmethod
    @abc.abstractmethod
    def build_from_tree(cls, element):
        """
        Builds an instance from the xml representation
        :param element: instance of ET.Element
        :return: instance of the current class
        """
        pass

    @abc.abstractmethod
    def substitute(self, var, new_var):
        pass

    @abc.abstractmethod
    def is_free(self, var):
        """
        Checks if the variable is free in this term
        If the variable is not in the term it returns False
        :param var: Variable instance
        :return: True if var is free in the term, False otherwise
        """
        pass


class Constant(Term):
    def __init__(self, symbol):
        self.symbol = symbol

    def add_to_tree(self, parent):
        tree = ET.SubElement(parent, "constant", attrib={"symbol": self.symbol})
        return tree

    @classmethod
    def build_from_tree(cls, element):
        return cls(element.get("symbol"))

    def substitute(self, var, new_var):
        return self

    def is_free(self, var):
        return False

    def __eq__(self, other):
        return self.symbol == other.symbol


class Variable(Term):
    def __init__(self, symbol):
        self.symbol = symbol

    def add_to_tree(self, parent):
        tree = ET.SubElement(parent, "variable", attrib={"symbol": self.symbol})
        return tree

    @classmethod
    def build_from_tree(cls, element):
        return cls(element.get("symbol"))

    def substitute(self, var, new_var):
        if var == self:
            return new_var
        if var == new_var:
            raise ValueError("variable capture")
        return self

    def is_free(self, var):
        return var == self

    def __eq__(self, other):
        return self.symbol == other.symbol


class Function(Term):
    def __init__(self, symbol, *terms):
        self.symbol = symbol
        self.terms = list(terms)
        for term in self.terms:
            if not isinstance(term, Term):
                raise ValueError("incorrect term")

    def add_to_tree(self, parent):
        tree = ET.SubElement(parent, "function", attrib={"symbol": self.symbol})
        for term in self.terms:
            term.add_to_tree(tree)
        return tree

    @classmethod
    def build_from_tree(cls, element):
        return cls(
            element.get("symbol"), *[build_from_tree_term(child) for child in element]
        )

    def substitute(self, var, new_var):
        new_terms = [term.substitute(var, new_var) for term in self.terms]
        return Function(self.symbol, new_terms)

    def is_free(self, var):
        for term in self.terms:
            if term.is_free(var):
                return True
        return False

    def __eq__(self, other):
        if self.symbol != other.symbol:
            return False
        if len(self.terms) != len(other.terms):
            return False
        for term1, term2 in zip(self.terms, other.terms):
            if term1 != term2:
                return False
        return True


class UnaryConnector(Enum):
    NEGATION = auto()

    def __str__(self):
        smap = {self.NEGATION: "NOT"}
        return smap[self]

    def to_str(self):
        """
        :return: String representation used to store data (e.g. in XML format)
        """
        smap = {self.NEGATION: "negation"}
        return smap[self]

    @classmethod
    def from_str(cls, s):
        smap = {"negation": cls.NEGATION}
        return smap[s]


class BinaryConnector(Enum):
    CONJUNCTION = auto()
    DISJUNCTION = auto()
    IMPLICATION = auto()
    BICONDITIONAL = auto()

    def __str__(self):
        smap = {
            self.CONJUNCTION: "AND",
            self.DISJUNCTION: "OR",
            self.IMPLICATION: "=>",
            self.BICONDITIONAL: "<=>",
        }
        return smap[self]

    def to_str(self):
        """
        :return: String representation used to store data (e.g. in XML format)
        """
        smap = {
            self.CONJUNCTION: "conjunction",
            self.DISJUNCTION: "disjunction",
            self.IMPLICATION: "implication",
            self.BICONDITIONAL: "biconditional",
        }
        return smap[self]

    @classmethod
    def from_str(cls, s):
        smap = {
            "conjunction": cls.CONJUNCTION,
            "disjunction": cls.DISJUNCTION,
            "implication": cls.IMPLICATION,
            "biconditional": cls.BICONDITIONAL,
        }
        return smap[s]


class Quantifier(Enum):
    UNIVERSAL = auto()
    EXISTENTIAL = auto()

    def __str__(self):
        smap = {self.UNIVERSAL: "FORALL", self.EXISTENTIAL: "EXISTS"}
        return smap[self]

    def to_str(self):
        """
        :return: String representation used to store data (e.g. in XML format)
        """
        smap = {self.UNIVERSAL: "universal", self.EXISTENTIAL: "existential"}
        return smap[self]

    @classmethod
    def from_str(cls, s):
        smap = {"universal": cls.UNIVERSAL, "existential": cls.EXISTENTIAL}
        return smap[s]


def is_sentence(sentence):
    return isinstance(sentence, Sentence) or isinstance(sentence, bool)


TAG_SENTENCE_MAP = {
    "true": True,
    "false": False,
    "constantPredicate": ConstantPredicate,
    "predicate": Predicate,
    "unaryConnectorSentence": UnaryConnectorSentence,
    "binaryConnectorSentence": BinaryConnectorSentence,
    "quantifierSentence": QuantifierSentence,
}

TAG_TERM_MAP = {
    "constant": Constant,
    "variable": Variable,
    "function": Function,
}


def build_from_tree_term(element):
    """
    Builds an instance of a term from the xml representation
    :param element: ET.Element
    :return: Term instance
    """
    cls = TAG_TERM_MAP.get(element.tag, None)
    if cls is None:
        raise ValueError("incorrect term")
    return cls.build_from_tree(element)


def build_from_tree_sentence(element):
    """
    Builds an instance of a sentence from the xml representation
    :param element: ET.Element
    :return: Sentence instance
    """
    cls = TAG_SENTENCE_MAP.get(element.tag, None)
    if cls is None:
        raise ValueError("incorrect sentence")
    if isinstance(cls, bool):
        return cls
    return cls.build_from_tree(element)


def build_from_tree(root):
    """
    Builds an instance of a sentence from the xml representation
    :param root: instance of ET.Element, root element that must contain the tag <sentence>
    :return: Sentence instance
    """
    if root.tag != "sentence":
        raise ValueError("incorrect root, please use <sentence> as root tag")
    if len(root) != 1:
        raise ValueError("incorrect number of child for root")
    return build_from_tree_sentence(root[0])


def sentence_to_xml(sentence):
    root = ET.Element("sentence")
    sentence.add_to_tree(root)
    return ET.tostring(root)
