import PySimpleGUI as sg
from cash_flow import CashFlowItem
from window_random_type import window_random_type
import textwrap

def _get_value_dict(current_cash_flow_item):
    """Generate Value Dictionary"""
    # Load values from current CashFlowItem
    value_dict = {
        "name": current_cash_flow_item.name,
        "desc": current_cash_flow_item.desc,
        "upfront_cost": current_cash_flow_item.upfront_cost,
        "recurring_cost": current_cash_flow_item.recurring_cost
    }
    return value_dict

def _name_desc_layout(value_dict):
    """Generate Name and Description layout"""
    name_desc_layout = [
        [sg.Text("Name*", size=(15, 1), key="name_text"),
            sg.InputText(default_text=value_dict["name"], key="name", size=(50, 1))],
        [sg.Text("Description", size=(15, 1)),
            sg.Multiline(default_text=value_dict["desc"], key="desc", size=(50, 4))]
    ]
    return name_desc_layout

def _upfront_cost_frame(value_dict):
    # Upfront cost frame
    upfront_cost_layout = [
        [sg.Text(textwrap.fill(str(value_dict["upfront_cost"]), width=65), size=(65, 2), key="upfront_cost"),
            sg.Button("Edit", size=(15, 1), key="edit_upfront_cost")]
    ]
    upfront_cost_frame = [[sg.Frame("Upfront Cost", layout=upfront_cost_layout)]]
    return upfront_cost_frame

def _recurring_cost_frame(value_dict):
    # Recurring cost frame
    recurring_cost_layout = [
        [sg.Text(textwrap.fill(str(value_dict["recurring_cost"]), width=65), size=(65, 2), key="recurring_cost"),
            sg.Button("Edit", size=(15, 1), key="edit_recurring_cost")]
    ]
    recurring_cost_frame = [[sg.Frame("Recurring Cost", layout=recurring_cost_layout)]]
    return recurring_cost_frame

def window_cash_flow_item(current_cash_flow_item=CashFlowItem()):
    value_dict = _get_value_dict(current_cash_flow_item)

    # Buttons
    buttons_layout = [
        [sg.OK(bind_return_key=True), sg.Cancel()],
    ]

    window_layout = _name_desc_layout(value_dict) \
        + _upfront_cost_frame(value_dict) \
        + _recurring_cost_frame(value_dict) \
        + buttons_layout

    # Generate window
    window = sg.Window("Set Cash Flow Item", layout=window_layout)

    while True:
        # Read data from window
        event, window_value = window.Read()

        if event in (None, "Cancel"):
            new_cash_flow_item = None
            break
        elif event in ("OK"):
            if window_value["name"] == "":
                window.FindElement("name_text").Update(text_color="red")
            else:
                new_cash_flow_item = CashFlowItem(
                    name=window_value["name"],
                    desc=window_value["desc"].strip(" \t\n\r\x0b\x0c"),
                    upfront_cost=value_dict["upfront_cost"],
                    recurring_cost=value_dict["recurring_cost"])
                break
        elif event in ("edit_upfront_cost"):
            window.Hide()
            new_upfront_cost = window_random_type(value_dict["upfront_cost"])
            if new_upfront_cost is not None:
                value_dict["upfront_cost"] = new_upfront_cost
            window.FindElement(key="upfront_cost").Update(
                textwrap.fill(str(value_dict["upfront_cost"]), width=65))
            window.UnHide()
        elif event in ("edit_recurring_cost"):
            window.Hide()
            new_recurring_cost = window_random_type(value_dict["recurring_cost"])
            if new_recurring_cost is not None:
                value_dict["recurring_cost"] = new_recurring_cost
            window.FindElement(key="recurring_cost").Update(
                textwrap.fill(str(value_dict["recurring_cost"]), width=65))
            window.UnHide()

    window.Close()
    return new_cash_flow_item
