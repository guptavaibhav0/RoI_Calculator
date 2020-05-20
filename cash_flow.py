"""Module for cash flow sheet"""

__version__ = "0.1"
__author__ = "Vaibhav Gupta"

from typing import List, Tuple
from collections.abc import Iterable
import textwrap
import math

import numpy as np
import lxml.etree as etree

import random_type

# ----- Currency Symbols ----- #
USD_SIGN = "\u0024"    # United States dollar
INR_SIGN = "\u20B9"    # Indian rupee
GBP_SIGN = "\u00A3"    # Pound sterling
JPY_SIGN = "\u00A5"    # Japanese yen
KRW_SIGN = "\u20A9"    # South Korean won
EUR_SIGN = "\u20AC"    # Euro
BITCOIN_SIGN = "\u20BF"


# ----- Cash Flow Item ----- #
class CashFlowItem():
    """
    Class for an item in the cash flow sheet.

    Attributes:
        name: Name of the item.
        desc: Description of the item.
    """
    name: str
    desc: str

    # --- Properties --- #
    @property
    def upfront_cost(self) -> random_type.RandomType:
        """Upfront Cost of the item"""
        return self._upfront_cost

    @upfront_cost.setter
    def upfront_cost(self, upfront_cost: random_type.RandomType) -> None:
        self._upfront_cost = self._checkCost(upfront_cost)

    @property
    def recurring_cost(self) -> random_type.RandomType:
        """Recurring Cost of the item"""
        return self._recurring_cost

    @recurring_cost.setter
    def recurring_cost(self, recurring_cost: random_type.RandomType) -> None:
        self._recurring_cost = self._checkCost(recurring_cost)

    # --- Constructors --- #
    def __init__(self,
                 name: str = "",
                 desc: str = "",
                 upfront_cost: random_type.RandomType = random_type.Constant(),
                 recurring_cost: random_type.RandomType = random_type.Constant()) -> None:
        """
        Default initialization method for CashFlowItem class

        Args:
            name: Name of the item
            desc: Description of the item
            upfront_cost: Upfront Cost of the item
            recurring_cost: Recurring Cost of the item
        """
        self.name = name
        self.desc = desc
        self.upfront_cost = upfront_cost
        self.recurring_cost = recurring_cost

    @classmethod
    def create_from_etree_element(cls, etree_element: etree.Element) -> None:
        """Initialize from an etree element"""
        name = etree_element.find('name').text
        desc = etree_element.find('desc').text
        desc = "" if desc is None else desc
        for random_type_element in etree_element.find('upfrontCost'):
            upfront_cost = random_type.create_from_etree_element(random_type_element)
        for random_type_element in etree_element.find('recurringCost'):
            recurring_cost = random_type.create_from_etree_element(random_type_element)
        return cls(name=name, desc=desc, upfront_cost=upfront_cost, recurring_cost=recurring_cost)

    # --- Methods --- #
    def get_upfront_cost(self) -> float:
        """Gives upfront cost of the item."""
        return self.upfront_cost.sample_value(year=0)

    def get_recurring_cost(self, year: int = 1) -> float:
        """
        Sample recurring cost for the year

        Args:
            year: Year of sampling

        Returns:
            sampled recurring cost if year in active interval, 0 otherwise
        """
        return self.recurring_cost.sample_value(year)

    def generate_etree_element(self) -> etree.Element:
        """Generate etree element of the instance"""
        item_element = etree.Element("CashFlowItem")
        etree.SubElement(item_element, "name").text = self.name
        etree.SubElement(item_element, "desc").text = self.desc

        upfront_cost_element = etree.SubElement(item_element, "upfrontCost")
        upfront_cost_element.append(self.upfront_cost.generate_etree_element())

        recurring_cost_element = etree.SubElement(item_element, "recurringCost")
        recurring_cost_element.append(self.recurring_cost.generate_etree_element())

        return item_element

    # --- String Representation --- #
    def __repr__(self) -> str:
        """String representation of the instance"""
        return "".join([f"{self.__class__.__name__}(name='{self.name}', ",
                        f"desc='{self.desc}', ",
                        f"upfront_cost={self.upfront_cost!r}, ",
                        f"recurring_cost={self.recurring_cost!r})"])

    def __str__(self) -> str:
        """Readable string representation of the instance"""
        prop_names = ["Name", "Description", "Upfront Cost", "Recurring Cost"]
        return "".join([f"{prop_names[0]:14} -> {self.name}\n",
                        f"{prop_names[1]:14} -> {self.desc}\n",
                        f"{prop_names[2]:14} -> {self.upfront_cost}\n",
                        f"{prop_names[3]:14} -> {self.recurring_cost}"])

    # --- Internal Functions --- #
    def _checkCost(self, cost) -> random_type.RandomType:
        """Ensures that the data type of 'cost' is a RandomType."""
        if isinstance(cost, random_type.RandomType):
            return cost
        elif isinstance(cost, (float, int)):
            return random_type.Constant(value=cost)
        else:
            raise TypeError("cost must be a RandomType, float or int")


# ----- Cash Flow Group ----- #
class CashFlowGroup():
    """
    Class for a group in the cash flow sheet.

    Attributes:
        name: Name of the item
        desc: Description of the item
    """
    name: str
    desc: str

    # --- Properties --- #
    @property
    def items(self) -> List[CashFlowItem]:
        """List of cash flow items in the CashFlowGroup"""
        return self._items

    @items.setter
    def items(self, items: List[CashFlowItem]) -> None:
        self._items = []
        self.add_items(items)

    # --- Constructors --- #
    def __init__(self,
                 name: str = "",
                 desc: str = "",
                 items: List[CashFlowItem] = []) -> None:
        """
        Default initialization method for CashFlowGroup class

        Args:
            name: Name of the group
            desc: Description of the group
            items: List of cash flow items in the CashFlowGroup
        """
        self.name = name
        self.desc = desc
        self.items = items

    @classmethod
    def create_from_etree_element(cls, etree_element: etree.Element) -> None:
        """Initialize from an etree element"""
        name = etree_element.find('name').text
        desc = etree_element.find('desc').text
        desc = "" if desc is None else desc
        items = [CashFlowItem.create_from_etree_element(item_element)
                 for item_element in etree_element.findall("CashFlowItem")]
        return cls(name=name, desc=desc, items=items)

    # --- Methods --- #
    def add_items(self, items: List[CashFlowItem]) -> None:
        """
        Appends items to the list of CashFlowGroup instance

        Args:
            items: List of items in the CashFlowGroup
        """
        items = self._check_items(items)
        self.items.extend(items)

    def get_items(self, item_names: List[str]) -> CashFlowItem:
        """
        Get specific items from the list of CashFlowGroup instance

        Args:
            item_names: Names of items to remove from the CashFlowGroup
        """
        return [item for item in self.items if item.name in item_names]

    def remove_items(self, item_names: List[str]) -> None:
        """
        Remove specific items from the list of CashFlowGroup instance

        Args:
            item_names: Names of items to remove from the CashFlowGroup
        """
        self.items = [item for item in self.items if item.name not in item_names]

    def get_names(self) -> List[str]:
        """Returns a list of cashflow items' name"""
        return [x.name for x in self.items]

    def get_upfront_cost(self) -> List[float]:
        """
        Gives list of upfront costs for all the items in the group.

        Returns:
            Upfront cost of the item
        """
        return [x.get_upfront_cost() for x in self.items]

    def get_recurring_cost(self, year: int) -> List[float]:
        """
        Gives list of recurring costs for all the items in the group.

        Returns:
            Recurring cost of the item
        """
        return [x.get_recurring_cost(year) for x in self.items]

    def generate_etree_element(self) -> etree.Element:
        """Generate etree element of the instance"""
        element = etree.Element("CashFlowGroup")
        etree.SubElement(element, "name").text = self.name
        etree.SubElement(element, "desc").text = self.desc
        for item in self.items:
            element.append(item.generate_etree_element())
        return element

    # --- String Representation --- #
    def __repr__(self) -> str:
        """String representation of the instance"""
        item_str = ""
        for item in self.items:
            item_str = ", ".join([item_str, repr(item)])
        item_str = item_str.lstrip(', ')
        return "".join([f"{self.__class__.__name__}(name='{self.name}', ",
                        f"desc='{self.desc}', ",
                        f"items=[{item_str}])"])

    def __str__(self) -> str:
        """Readable string representation of the instance"""
        item_str = ""
        for item in self.items:
            item_str = "".join([item_str, "\n  =>", textwrap.indent(str(item), "\t")])
        prop_names = ["Name", "Description", "Items"]
        return "".join([f"{prop_names[0]:14} -> {self.name}\n",
                        f"{prop_names[1]:14} -> {self.desc}\n",
                        f"{prop_names[2]:14}{item_str}"])

    # --- Internal Functions --- #
    def _check_items(self, items) -> List[CashFlowItem]:
        """Ensures that the data type of 'items' is a list of CashFlowItem"""
        if isinstance(items, CashFlowItem):
            return [items]
        elif isinstance(items, Iterable):
            for item in items:
                if not isinstance(item, CashFlowItem):
                    raise TypeError("Items must be a list of CashFlowItem")
            return list(items)
        else:
            raise TypeError("Items must be a list of CashFlowItem")


# ----- Cash Flow Sheet ----- #
class CashFlowSheet():
    """Data class for the CashFlow sheet"""

    # --- Properties --- #
    @property
    def groups(self) -> List[CashFlowGroup]:
        """List of cash flow groups in the CashFlowSheet"""
        return self._groups

    @groups.setter
    def groups(self, groups: List[CashFlowGroup]) -> None:
        self._groups = []
        self.add_groups(groups)

    # --- Constructors --- #
    def __init__(self,
                 groups: List[CashFlowGroup] = []) -> None:
        """
        Default initialization method for CashFlowSheet class

        Args:
            groups: List of groups in the CashFlowSheet
        """
        self.groups = groups

    @classmethod
    def create_from_etree_element(cls, etree_element: etree.Element) -> None:
        """Initialize from an etree element"""
        return cls(groups=[CashFlowGroup.create_from_etree_element(group_element)
                           for group_element in etree_element.findall("CashFlowGroup")])

    # --- Methods --- #
    def add_groups(self, groups: List[CashFlowGroup]) -> None:
        """
        Appends groups to the list of CashFlowSheet instance

        Args:
            groups: List of groups in the CashFlowSheet
        """
        groups = self._check_groups(groups)
        self.groups.extend(groups)

    def get_groups(self, group_names: List[str]) -> None:
        """
        Get specific groups from the list of CashFlowGroup instance

        Args:
            group_names: Names of groups to remove from the CashFlowGroup
        """
        return [group for group in self.groups if group.name in group_names]

    def remove_groups(self, group_names: List[str]) -> None:
        """
        Remove specific groups from the list of CashFlowGroup instance

        Args:
            group_names: Names of groups to remove from the CashFlowGroup
        """
        self.groups = [group for group in self.groups if group.name not in group_names]

    def get_names(self) -> List[Tuple[str, List[str]]]:
        """Gives cashflow groups' name and  cashflow items' name"""
        return [(grps.name, grps.get_names()) for grps in self.groups]

    def get_cash_flow(self, years: int = 10) -> Tuple[List[List[float]], List[float]]:
        """
        Generate cashflow sheet for given number of years

        Args:
            years: Number of years for which sheet is to be generated
        """
        total_cash_flow = [self.get_upfront_cost()] + ([self.get_recurring_cost(year) for year in range(1, years+1)])
        net_cash_flow = [sum([sum(grps) for grps in year]) for year in total_cash_flow]
        return (total_cash_flow, net_cash_flow)

    def get_upfront_cost(self) -> List[float]:
        """Gives list of upfront costs for all the items in the sheet"""
        return [group.get_upfront_cost() for group in self.groups]

    def get_recurring_cost(self, year: int) -> List[float]:
        """Gives list of recurring costs for all the items in the sheet"""
        return [x.get_recurring_cost(year) for x in self.groups]

    def generate_etree_element(self) -> etree.Element:
        """Generate etree element of the instance"""
        element = etree.Element("CashFlowSheet")
        for group in self.groups:
            element.append(group.generate_etree_element())
        return element

    # --- String Representation --- #
    def __repr__(self) -> str:
        """String representation of the instance"""
        group_str = ""
        for group in self.groups:
            group_str = ", ".join([group_str, repr(group)])
        group_str = group_str.lstrip(', ')
        return "".join([f"{self.__class__.__name__}(",
                        f"groups=[{group_str}])"])

    def __str__(self) -> str:
        """Readable string representation of the instance"""
        group_str = ""
        for group in self.groups:
            group_str = "".join([group_str, "\n  =>", textwrap.indent(str(group), "\t")])
        return (f"Groups{group_str}")

    # --- Internal Functions --- #
    def _check_groups(self, groups) -> List[CashFlowGroup]:
        """Ensures that the data type of 'groups' is a list of CashFlowGroup"""
        if isinstance(groups, CashFlowGroup):
            return [groups]
        elif isinstance(groups, Iterable):
            for item in groups:
                if not isinstance(item, CashFlowGroup):
                    raise TypeError("Groups must be a list of CashFlowGroup")
            return list(groups)
        else:
            raise TypeError("Groups must be a list of CashFlowGroup")


# ----- Summary ----- #
class Summary():
    """Frontend class for the CashFlow sheet"""
    cash_flow_sheet: CashFlowSheet
    interest_rate: float
    years: int
    iterations: int
    sampled: bool
    currency: str = INR_SIGN

    # --- Properties --- #
    @property
    def total_cash_flow(self) -> List[List[float]]:
        """Total cash flow"""
        if not self.sampled:
            self.sample_cash_flow()
        return self._total_cash_flow

    @total_cash_flow.setter
    def total_cash_flow(self, input) -> None:
        raise RuntimeError("Total cash flow cannot be set externally")

    @property
    def net_cash_flow(self) -> List[float]:
        """Net cash flow"""
        if not self.sampled:
            self.sample_cash_flow()
        return self._net_cash_flow

    @net_cash_flow.setter
    def net_cash_flow(self, input) -> None:
        raise RuntimeError("Net cash flow cannot be set externally")

    # --- Constructors --- #
    def __init__(self,
                 cash_flow_sheet: CashFlowSheet,
                 interest_rate: float = 0.10,
                 years: int = 10,
                 iterations: int = 10000) -> None:
        """
        Default initialization method for Summary class

        Args:
            cash_flow_sheet: Instance of CashFlowSheet class
            interest_rate: Annual rate of interest
            years: Number of years for which cash flow has to be calculated
        """
        self.cash_flow_sheet = cash_flow_sheet
        self.interest_rate = interest_rate
        self.years = years
        self.iterations = iterations
        self.sampled = False

    @classmethod
    def create_from_etree_element(cls, etree_element: etree.Element) -> None:
        """Initialize from an etree element"""
        return cls(cash_flow_sheet=CashFlowSheet.create_from_etree_element(etree_element.find("CashFlowSheet")),
                   interest_rate=float(etree_element.find("InterestRate").text),
                   years=math.floor(float(etree_element.find("Years").text)))

    # --- Methods --- #
    def generate_etree_element(self) -> etree.Element:
        """Generate etree element of the instance"""
        element = etree.Element("Summary")
        etree.SubElement(element, "InterestRate").text = str(self.interest_rate)
        etree.SubElement(element, "Years").text = str(self.years)
        etree.SubElement(element, "Iterations").text = str(self.iterations)
        element.append(self.cash_flow_sheet.generate_etree_element())
        return element

    def sample_cash_flow(self) -> None:
        """Sample cash flow"""
        (total_cash_flow, net_cash_flow) = self.cash_flow_sheet.get_cash_flow(self.years)
        self._total_cash_flow = total_cash_flow
        self._net_cash_flow = net_cash_flow
        self.sampled = True

    def get_IRR(self) -> float:
        """Calculate internal rate of interest"""
        if not self.sampled:
            self.sample_cash_flow()
        return np.irr(self.net_cash_flow)

    def get_NPV(self) -> float:
        """Calculate net present value"""
        if not self.sampled:
            self.sample_cash_flow()
        return np.npv(self.interest_rate, self.net_cash_flow)

    def get_payback_period(self) -> float:
        """Calculate payback period"""
        if not self.sampled:
            self.sample_cash_flow()
        cumsum_cash_flow = list(np.cumsum(self.net_cash_flow))
        first_positive_year = self.years
        for year in range(self.years):
            if cumsum_cash_flow[year] > 0:
                first_positive_year = year
                break
        complete_years = first_positive_year - 1
        fractional_year = abs(cumsum_cash_flow[complete_years] / self.net_cash_flow[first_positive_year])
        return (complete_years + fractional_year)

    def get_textual_cash_flow_sheet(self) -> str:
        """Gives a textual cash flow sheet"""
        if not self.sampled:
            self.sample_cash_flow()

        # Header
        format_str = "".join(["||{:^15.15}||{:^15.15}||",
                              "{:^15.15}||"*(self.years + 1)])
        years_text = ["Year {:d}".format(i) for i in range(self.years+1)]
        string = format_str.format("Groups", "Items", *years_text)

        # Total Cash Flow
        names = self.cash_flow_sheet.get_names()
        format_str = "".join(["||{:^15.15}||{:^15.15}||",
                              "".join([self.currency, "{:14.2f}||"])*(self.years + 1)])
        for group_no in range(len(names)):
            group_name = names[group_no][0]
            item_names = names[group_no][1]
            for item_no in range(len(item_names)):
                yr_val = [self.total_cash_flow[year][group_no][item_no]
                          for year in range(self.years+1)]
                string = "\n".join([string, format_str.format(group_name, item_names[item_no], *yr_val)])
                group_name = ""    # Print Group name only in the first line

        # Net Cash Flow
        format_str = "".join(["||{:^32.32}||",
                              "".join([self.currency, "{:14.2f}||"])*(self.years + 1)])
        string = "\n".join([string, format_str.format("Net Cash Flow", *self.net_cash_flow)])

        return string

    # --- String Representation --- #
    def __repr__(self) -> str:
        """String representation of the instance"""
        return "".join([f"{self.__class__.__name__}(interest_rate={self.interest_rate:.2f}, ",
                        f"years={self.years:.0f}, ",
                        f"cash_flow_sheet={self.cash_flow_sheet!r})"])

    def __str__(self) -> str:
        """Readable string representation of the instance"""
        sheet_str = textwrap.indent(str(self.cash_flow_sheet), "\t")
        prop_names = ["Interest Rate", "Years", "Cash Flow Sheet"]
        return "".join([f"{prop_names[0]:15} -> {self.interest_rate}\n",
                        f"{prop_names[1]:15} -> {self.years}\n",
                        f"{prop_names[2]:15}\n  =>{sheet_str}"])


# ----- Module Methods for XML ----- #
def generate_XML_file(summary, file):
    element = summary.generate_etree_element()
    tree = etree.ElementTree(element)
    tree.write(file, pretty_print=True, xml_declaration=True, method="xml")

def read_XML_file(file):
    xmlschema_doc = etree.parse("xml_spec.xsd")
    xmlschema = etree.XMLSchema(xmlschema_doc)
    tree = etree.parse(file)
    xmlschema.assertValid(tree)
    root_element = tree.getroot()
    return Summary.create_from_etree_element(root_element)
