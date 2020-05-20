import PySimpleGUI as sg
import numpy as np
from cash_flow import Summary

def window_result(summary: Summary):
    iterations = summary.iterations
    list_IRR = np.zeros((iterations, ))
    list_NPV = np.zeros((iterations, ))
    list_payback_period = np.zeros((iterations, ))
    for i in range(iterations):
        summary.sample_cash_flow()
        list_IRR[i] = summary.get_IRR()
        list_NPV[i] = summary.get_NPV()
        list_payback_period[i] = summary.get_payback_period()
        stop_check = sg.OneLineProgressMeter('Iterations', i+1, iterations, 'key', "Monte Carlo Sampling...")
        if not stop_check and i+1 != iterations:
            return False

    window_layout = [
        [sg.Text("Internal Return of Investment")],
        [sg.Text("".join(["Mean is ", str(np.mean(list_IRR)), " with std. deviation of ", str(np.std(list_IRR))]))],
        [sg.Text("Net Present Value")],
        [sg.Text("".join(["Mean is ", str(np.mean(list_NPV)), " with std. deviation of ", str(np.std(list_NPV))]))],
        [sg.Text("Payback Period [years]")],
        [sg.Text("".join([
            "Mean is ", str(np.mean(list_payback_period)),
            " with std. deviation of ", str(np.std(list_payback_period))
        ]))]
    ]

    window = sg.Window("Result", layout=window_layout)
    event, window_value = window.Read()
