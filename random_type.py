"""Module for various Random Types"""

__version__ = "0.1"
__author__ = "Vaibhav Gupta"

import math
import random

import lxml.etree as etree


# ----- Internal Functions ----- #
def _value_or_default(value: str, default: float) -> float:
    if value is None:
        return default
    else:
        return float(value)

def _value_or_empty(value: float, compare_to: float) -> str:
    if value == compare_to:
        return ""
    else:
        return str(value)

# ----- Base Class for Random Type ----- #
class RandomType():
    pass

# ----- Gaussian Random Type ----- #
class Gaussian(RandomType):
    """
    Random Type with Gaussian distribution

    Attributes:
        mu: Mean for Gaussian distribution
        sigma: Std. deviation for Gaussian distribution
        start_year: Starting year of active interval
        end_year: Ending year of active interval
    """
    mu: float
    sigma: float
    start_year: float
    end_year: float

    def __init__(self,
                 mu: float = 0,
                 sigma: float = 1,
                 start_year: float = 0,
                 end_year: float = math.inf) -> None:
        """
        Default initialization method for Gaussian Random Type

        Args:
            mu: Mean for Gaussian distribution
            sigma: Std. deviation for Gaussian distribution
            start_year: Starting year of active interval
            end_year: Ending year of active interval
        """
        self.mu = mu
        self.sigma = sigma
        self.start_year = start_year
        self.end_year = end_year

    @classmethod
    def create_from_etree_element(cls, etree_element: etree.Element) -> None:
        """Initialize from an etree element"""
        return cls(mu=float(etree_element.find("mu").text),
                   sigma=float(etree_element.find("sigma").text),
                   start_year=_value_or_default(etree_element.find("startYear").text, 0),
                   end_year=_value_or_default(etree_element.find("endYear").text, math.inf))

    def sample_value(self, year: int = 0) -> float:
        """
        Sample a random value for the year

        Args:
            year: Year of sampling

        Returns:
            sampled value if year in active interval, 0 otherwise
        """
        if (year >= self.start_year and year <= self.end_year):
            return random.gauss(self.mu, self.sigma)
        else:
            return 0.0

    def generate_etree_element(self) -> etree.Element:
        """Generate etree element of the instance"""
        element = etree.Element("Gaussian")
        etree.SubElement(element, "mu").text = str(self.mu)
        etree.SubElement(element, "sigma").text = str(self.sigma)
        etree.SubElement(element, "startYear").text = _value_or_empty(self.start_year, 0)
        etree.SubElement(element, "endYear").text = _value_or_empty(self.end_year, math.inf)
        return element

    def __repr__(self) -> str:
        """String representation of the instance"""
        string_list = [f"{self.__class__.__name__}(mu={self.mu:.2f}, sigma={self.sigma:.2f}"]
        if self.start_year != 0:
            string_list.append(f", start_year={self.start_year:.0f}")
        if not math.isinf(self.end_year):
            string_list.append(f", end_year={self.end_year:.0f}")
        string_list.append(")")
        return "".join(string_list)

    def __str__(self) -> str:
        """Readable string representation of the instance"""
        string = f"Gaussian distribution with mu={self.mu:.2f} and sigma={self.sigma:.2f}"
        if self.start_year != 0:
            string = "".join([string, f", starting in year {self.start_year:.0f}"])
        if not math.isinf(self.end_year):
            string = "".join([string, f", ending in year {self.end_year:.0f}"])
        return string

# ----- Constant Random Type ----- #
class Constant(RandomType):
    """
    Random Type with Constant value

    Attributes:
        value: Constant value
        start_year: Starting year of active interval
        end_year: Ending year of active interval
    """
    value: float
    start_year: float
    end_year: float

    def __init__(self,
                 value: float = 0.0,
                 start_year: float = 0,
                 end_year: float = math.inf) -> None:
        """
        Default initilization method for Constant Random Type

        Attributes:
            value: Constant value
            start_year: Starting year of active interval
            end_year: Ending year of active interval
        """
        self.value = value
        self.start_year = start_year
        self.end_year = end_year

    @classmethod
    def create_from_etree_element(cls, etreeElement: etree.Element) -> None:
        """Initialize from an etree element"""
        return cls(value=float(etreeElement.find("value").text),
                   start_year=_value_or_default(etreeElement.find("startYear").text, 0),
                   end_year=_value_or_default(etreeElement.find("endYear").text, math.inf))

    def sample_value(self, year: int = 0) -> float:
        """
        Sample a random value for the year

        Args:
            year: Year of sampling

        Returns:
            sampled value if year in active interval, 0 otherwise
        """
        if (year >= self.start_year and year <= self.end_year):
            return self.value
        else:
            return 0.0

    def generate_etree_element(self) -> etree.Element:
        """Generate etree element of the instance"""
        element = etree.Element("Constant")
        etree.SubElement(element, "value").text = str(self.value)
        etree.SubElement(element, "startYear").text = _value_or_empty(self.start_year, 0)
        etree.SubElement(element, "endYear").text = _value_or_empty(self.end_year, math.inf)
        return element

    def __repr__(self) -> str:
        """String representation of the instance"""
        string_list = [f"{self.__class__.__name__}(value={self.value:.2f}"]
        if self.start_year != 0:
            string_list.append(f", start_year={self.start_year:.0f}")
        if not math.isinf(self.end_year):
            string_list.append(f", end_year={self.end_year:.0f}")
        string_list.append(")")
        return "".join(string_list)

    def __str__(self) -> str:
        """Readable string representation of the instance"""
        string = f"Constant with a value of {self.value:.2f}"
        if self.start_year != 0:
            string = "".join([string, f", starting in year {self.start_year:.0f}"])
        if not math.isinf(self.end_year):
            string = "".join([string, f", ending in year {self.end_year:.0f}"])
        return string

# ----- Pareto Random Type ----- #
class Pareto(RandomType):
    """
    Random Type with Pareto distribution

    Attributes:
        alpha: Shape factor for pareto distribution
        start_year: Starting year of active interval
        end_year: Ending year of active interval
    """
    alpha: float
    start_year: float
    end_year: float

    def __init__(self,
                 alpha: float = 1,
                 start_year: float = 0,
                 end_year: float = math.inf) -> None:
        """
        Default initialization method for Pareto Random Type

        Args:
            alpha: Shape factor for pareto distribution
            start_year: Starting year of active interval
            end_year: Ending year of active interval
        """
        self.alpha = alpha
        self.start_year = start_year
        self.end_year = end_year

    @classmethod
    def create_from_etree_element(cls, etreeElement: etree.Element) -> None:
        """Initialize from an etree element"""
        return cls(alpha=float(etreeElement.find("alpha").text),
                   start_year=_value_or_default(etreeElement.find("startYear").text, 0),
                   end_year=_value_or_default(etreeElement.find("endYear").text, math.inf))

    def sample_value(self, year: int = 0) -> float:
        """
        Sample a random value for the year

        Args:
            year: Year of sampling

        Returns:
            sampled value if year in active interval, 0 otherwise
        """
        if (year >= self.start_year and year <= self.end_year):
            return random.paretovariate(self.alpha)
        else:
            return 0.0

    def generate_etree_element(self) -> etree.Element:
        """Generate etree element of the instance"""
        element = etree.Element("Pareto")
        etree.SubElement(element, "alpha").text = str(self.alpha)
        etree.SubElement(element, "startYear").text = _value_or_empty(self.start_year, 0)
        etree.SubElement(element, "endYear").text = _value_or_empty(self.end_year, math.inf)
        return element

    def __repr__(self) -> str:
        """String representation of the instance"""
        string_list = [f"{self.__class__.__name__}(alpha={self.alpha:.2f}"]
        if self.start_year != 0:
            string_list.append(f", start_year={self.start_year:.0f}")
        if not math.isinf(self.end_year):
            string_list.append(f", end_year={self.end_year:.0f}")
        string_list.append(")")
        return "".join(string_list)

    def __str__(self) -> str:
        """Readable string representation of the instance"""
        string = f"Pareto distribution with alpha of {self.alpha:.2f}"
        if self.start_year != 0:
            string = "".join([string, f", starting in year {self.start_year:.0f}"])
        if not math.isinf(self.end_year):
            string = "".join([string, f", ending in year {self.end_year:.0f}"])
        return string

# ----- Base Methods for Random Type ----- #
def create_from_etree_element(etree_element: etree.Element) -> RandomType:
    if (etree_element.tag == "Gaussian"):
        return Gaussian.create_from_etree_element(etree_element)
    elif (etree_element.tag == "Constant"):
        return Constant.create_from_etree_element(etree_element)
    elif (etree_element.tag == "Pareto"):
        return Pareto.create_from_etree_element(etree_element)
