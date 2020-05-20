import PySimpleGUI as sg
from window_cash_flow_item import window_cash_flow_item
from copy import deepcopy
from cash_flow import CashFlowGroup

def _get_value_dict(current_cash_flow_group: CashFlowGroup):
    """Generate Value Dictionary"""
    # Load values from current CashFlowItem
    value_dict = {
        "name": current_cash_flow_group.name,
        "desc": current_cash_flow_group.desc
    }
    return value_dict

def _name_desc_layout(value_dict):
    """Generate name and description layout"""
    name_desc_layout = [
        [sg.Text("Name*", size=(15, 1), key="name_text"),
            sg.InputText(default_text=value_dict["name"], key="name", size=(50, 1))],
        [sg.Text("Description", size=(15, 1)),
            sg.Multiline(default_text=value_dict["desc"], key="desc", size=(50, 4))]
    ]
    return name_desc_layout

def _item_list_frame(item_list_tree):
    """Generate item list frame layout"""
    item_list_layout = [
        [sg.Tree(data=item_list_tree, headings=[], key="item_list", col0_width=30),
            sg.Column(layout=[
                [sg.Button("Add", key="add_item", size=(8, 1))],
                [sg.Button("Edit", key="edit_item", size=(8, 1))],
                [sg.Button("Remove", key="remove_item", size=(8, 1))]
            ])]
    ]
    item_list_frame = [[sg.Frame("Items", layout=item_list_layout)]]
    return item_list_frame

def _get_tree(item_list):
    item_list_tree = sg.TreeData()
    for item in item_list:
        item_list_tree.Insert("", key=item.name, text=item.name, values=[])
    return item_list_tree

def window_cash_flow_group(current_cash_flow_group=CashFlowGroup()):
    value_dict = _get_value_dict(current_cash_flow_group)

    # Item list tree
    item_list_tree = _get_tree(current_cash_flow_group.items)

    # Buttons
    buttons_layout = [
        [sg.OK(bind_return_key=True), sg.Cancel()],
    ]

    window_layout = _name_desc_layout(value_dict) \
        + _item_list_frame(item_list_tree) \
        + buttons_layout

    # Generate window
    window = sg.Window("Set Cash Flow Group", layout=window_layout)

    new_cash_flow_group = deepcopy(current_cash_flow_group)
    while True:
        # Read data from window
        event, window_value = window.Read()

        if event in (None, "Cancel"):
            new_cash_flow_group = None
            break
        elif event in ("OK"):
            new_cash_flow_group.name = window_value["name"]
            new_cash_flow_group.desc = window_value["desc"]
            break
        elif event in ("add_item"):
            window.Hide()
            new_item = window_cash_flow_item()
            if new_item is not None:
                new_cash_flow_group.add_items(new_item)
                window.FindElement(key="item_list").Update(values=_get_tree(new_cash_flow_group.items))
            window.UnHide()
        elif event in ("edit_item"):
            window.Hide()
            old_item = new_cash_flow_group.get_items(window_value["item_list"])
            new_item = window_cash_flow_item(old_item[0])
            if new_item is not None:
                new_cash_flow_group.remove_items(window_value["item_list"])
                new_cash_flow_group.add_items(new_item)
                window.FindElement(key="item_list").Update(values=_get_tree(new_cash_flow_group.items))
            window.UnHide()
        elif event in ("remove_item"):
            new_cash_flow_group.remove_items(window_value["item_list"])
            window.FindElement(key="item_list").Update(values=_get_tree(new_cash_flow_group.items))

    window.Close()
    return(new_cash_flow_group)
