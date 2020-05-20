import PySimpleGUI as sg
import random_type
import math

def _get_value_dict(current_random_type):
    """Generate Value Dictionary"""
    def _empty_or_string(value, compare_to=0):
        if value == compare_to:
            return ""
        else:
            return str(value)

    # Set default Random Types
    gaussian = random_type.Gaussian()
    constant = random_type.Constant()
    pareto = random_type.Pareto()

    # Update current random type
    if isinstance(current_random_type, random_type.Gaussian):
        gaussian = current_random_type
    elif isinstance(current_random_type, random_type.Constant):
        constant = current_random_type
    elif isinstance(current_random_type, random_type.Pareto):
        pareto = current_random_type

    # Load values
    value_dict = {
        "mu_gaussian": str(gaussian.mu),
        "sigma_gaussian": str(gaussian.sigma),
        "start_year_gaussian": _empty_or_string(gaussian.start_year, 0),
        "end_year_gaussian": _empty_or_string(gaussian.end_year, math.inf),
        "value_constant": str(constant.value),
        "start_year_constant": _empty_or_string(constant.start_year, 0),
        "end_year_constant": _empty_or_string(constant.end_year, math.inf),
        "alpha_pareto": str(pareto.alpha),
        "start_year_pareto": _empty_or_string(pareto.start_year, 0),
        "end_year_pareto": _empty_or_string(pareto.end_year, math.inf)
    }

    return value_dict

def _get_gaussian_tab(value_dict):
    """Generate Gaussian tab"""
    gaussian_layout = [
        [sg.Text("mu (\u03BC)", size=(15, 1)),
            sg.InputText(default_text=value_dict["mu_gaussian"], key="mu_gaussian", enable_events=True)],
        [sg.Text("sigma (\u03C3)", size=(15, 1)),
            sg.InputText(default_text=value_dict["sigma_gaussian"], key="sigma_gaussian")],
        [sg.Text("Start Year", size=(15, 1)),
            sg.InputText(default_text=value_dict["start_year_gaussian"], key="start_year_gaussian")],
        [sg.Text("End Year", size=(15, 1)),
            sg.InputText(default_text=value_dict["end_year_gaussian"], key="end_year_gaussian")]
    ]
    gaussian_tab = sg.Tab("Gaussian", layout=gaussian_layout, key="gaussian")
    return gaussian_tab

def _get_constant_tab(value_dict):
    """Generate Constant tab"""
    constant_layout = [
        [sg.Text("value", size=(15, 1)),
            sg.InputText(default_text=value_dict["value_constant"], key="value_constant")],
        [sg.Text("Start Year", size=(15, 1)),
            sg.InputText(default_text=value_dict["start_year_constant"], key="start_year_constant")],
        [sg.Text("End Year", size=(15, 1)),
            sg.InputText(default_text=value_dict["end_year_constant"], key="end_year_constant")]
    ]
    constant_tab = sg.Tab("Constant", layout=constant_layout, key="constant")
    return constant_tab

def _get_pareto_tab(value_dict):
    """Generate Pareto tab"""
    pareto_layout = [
        [sg.Text("alpha (\u03B1)", size=(15, 1)),
            sg.InputText(default_text=value_dict["alpha_pareto"], key="alpha_pareto")],
        [sg.Text("Start Year", size=(15, 1)),
            sg.InputText(default_text=value_dict["start_year_pareto"], key="start_year_pareto")],
        [sg.Text("End Year", size=(15, 1)),
            sg.InputText(default_text=value_dict["end_year_pareto"], key="end_year_pareto")]
    ]
    pareto_tab = sg.Tab("Pareto", layout=pareto_layout, key="pareto", visible=False)
    return pareto_tab

def _set_random_type(window_value):
    """Generate new Random Type"""
    def _default_or_int(string, default_value=0):
        if string in (""):
            return default_value
        else:
            return math.floor(float(string))

    # Set Random Type to Gaussian
    if window_value["random_type"] in ("gaussian"):
        mu = float(window_value["mu_gaussian"])
        sigma = float(window_value["sigma_gaussian"])
        start_year = _default_or_int(window_value["start_year_gaussian"], 0)
        end_year = _default_or_int(window_value["end_year_gaussian"], math.inf)
        return random_type.Gaussian(mu=mu, sigma=sigma, start_year=start_year, end_year=end_year)

    # Set Random Type to Constant value
    elif window_value["random_type"] in ("constant"):
        value = float(window_value["value_constant"])
        start_year = _default_or_int(window_value["start_year_constant"], 0)
        end_year = _default_or_int(window_value["end_year_constant"], math.inf)
        return random_type.Constant(value=value, start_year=start_year, end_year=end_year)

    # Set Random Type to Pareto
    elif window_value["random_type"] in ("pareto"):
        alpha = float(window_value["alpha_pareto"])
        start_year = _default_or_int(window_value["start_year_pareto"], 0)
        end_year = _default_or_int(window_value["end_year_pareto"], math.inf)
        return random_type.Pareto(alpha=alpha, start_year=start_year, end_year=end_year)

def window_random_type(current_random_type=random_type.Gaussian()):
    """Window for random type"""
    # Load default values
    value_dict = _get_value_dict(current_random_type)

    # Generate tab group for Random Type selection
    random_type_layout = [
        [sg.TabGroup(
            layout=[[_get_gaussian_tab(value_dict), _get_constant_tab(value_dict), _get_pareto_tab(value_dict)]],
            key="random_type")]
    ]

    # Generate Button Layout
    button_layout = [
        [sg.OK(bind_return_key=True), sg.Cancel()]
    ]

    # Generate window layout
    window_layout = random_type_layout + button_layout

    # Generate window
    window = sg.Window("Set Random Type", layout=window_layout)

    while True:
        # Read event & data from window
        event, window_value = window.Read()

        # Take action based on window event
        # Do not save any changes and close window
        if event in (None, "Cancel"):
            new_random_type = None
            break
        # Save Changes and close window
        elif event in ("OK"):
            new_random_type = _set_random_type(window_value)
            break
        # Ensure proper input (Not Implemented)
        elif event in ("mu_gaussian", "sigma_gaussian"):
            pass

    window.Close()
    return new_random_type
