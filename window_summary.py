import PySimpleGUI as sg
from window_cash_flow_group import window_cash_flow_group
import math
from cash_flow import Summary, CashFlowSheet, generate_XML_file, read_XML_file
from window_result import window_result

def _default_or_float(string, default_value=0.0):
    if string in (""):
        return default_value
    else:
        return float(string)

def _default_or_int(string, default_value=0.0):
    if string in (""):
        return default_value
    else:
        return math.floor(float(string))

def _get_value_dict(summary: Summary):
    """Generate Value Dictionary"""
    # Load values from current CashFlowItem
    value_dict = {
        "interest_rate": summary.interest_rate,
        "years": summary.years,
        "iterations": summary.iterations
    }
    return value_dict

def _name_desc_layout(value_dict):
    """Generate name and description layout"""
    name_desc_layout = [
        [sg.Text("Interest Rate*", size=(15, 1), key="interest_rate_text"),
            sg.InputText(default_text=value_dict["interest_rate"], key="interest_rate", size=(50, 1))],
        [sg.Text("Years*", size=(15, 1)),
            sg.InputText(default_text=value_dict["years"], key="years", size=(50, 4))],
        [sg.Text("Number of Iterarions*", size=(15, 1)),
            sg.InputText(default_text=value_dict["iterations"], key="iterations", size=(50, 4))]
    ]
    return name_desc_layout

def _group_list_frame(group_list_tree):
    """Generate group list frame layout"""
    group_list_layout = [
        [sg.Tree(data=group_list_tree, headings=[], key="group_list", col0_width=30),
            sg.Column(layout=[
                [sg.Button("Add", key="add_group", size=(8, 1))],
                [sg.Button("Edit", key="edit_group", size=(8, 1))],
                [sg.Button("Remove", key="remove_group", size=(8, 1))]
            ])]
    ]
    group_list_frame = [[sg.Frame("Groups", layout=group_list_layout)]]
    return group_list_frame

def _get_tree(group_list):
    group_list_tree = sg.TreeData()
    for group in group_list:
        group_list_tree.Insert("", key=group.name, text=group.name, values=[])
    return group_list_tree

def _get_window_layout(summary: Summary):
    value_dict = _get_value_dict(summary)

    # Group list tree
    group_list_tree = _get_tree(summary.cash_flow_sheet.groups)

    # Buttons
    buttons_layout = [
        [sg.OK(bind_return_key=True), sg.Open(), sg.Save(), sg.Cancel()],
    ]

    window_layout = _name_desc_layout(value_dict) \
        + _group_list_frame(group_list_tree) \
        + buttons_layout

    return window_layout

def window_summary(summary: Summary = None):
    if summary is None:
        summary = Summary(CashFlowSheet())

    # Generate window
    window = sg.Window("Set Cash Flow Sheet", layout=_get_window_layout(summary))

    while True:
        # Read data from window
        event, window_value = window.Read()

        if event in (None, "Cancel"):
            break
        elif event in ("OK"):
            summary.interest_rate = _default_or_float(window_value["interest_rate"], 0)
            summary.years = _default_or_int(window_value["years"], 0)
            summary.iterations = _default_or_int(window_value["iterations"], 0)
            window_result(summary)
            break
        elif event in ("add_group"):
            window.Hide()
            new_group = window_cash_flow_group()
            if new_group is not None:
                summary.cash_flow_sheet.add_groups(new_group)
            window.FindElement(key="group_list").Update(values=_get_tree(summary.cash_flow_sheet.groups))
            window.UnHide()
        elif event in ("edit_group"):
            window.Hide()
            old_group = summary.cash_flow_sheet.get_groups(window_value["group_list"])
            new_group = window_cash_flow_group(old_group[0])
            if new_group is not None:
                summary.cash_flow_sheet.remove_groups(window_value["group_list"])
                summary.cash_flow_sheet.add_groups(new_group)
            window.FindElement(key="group_list").Update(values=_get_tree(summary.cash_flow_sheet.groups))
            window.UnHide()
        elif event in ("remove_group"):
            summary.cash_flow_sheet.remove_groups(window_value["group_list"])
            window.FindElement(key="group_list").Update(values=_get_tree(summary.cash_flow_sheet.groups))
        elif event in ("Save"):
            window.Hide()
            file_name = sg.PopupGetFile("Select xml file to save to...",
                                        file_types=(("XML Files", "*.xml"), ),
                                        save_as=True)
            if file_name is not None:
                generate_XML_file(summary, file_name)
            window.UnHide()
        elif event in ("Open"):
            window.Hide()
            file_name = sg.PopupGetFile("Select xml file to open...",
                                        file_types=(("XML Files", "*.xml"), ))
            if file_name is not None:
                summary = read_XML_file(file_name)
                window.FindElement("interest_rate").Update(summary.interest_rate)
                window.FindElement("years").Update(summary.years)
                window.FindElement("iterations").Update(summary.iterations)
                window.FindElement(key="group_list").Update(values=_get_tree(summary.cash_flow_sheet.groups))
            window.UnHide()

    window.Close()


window_summary()
