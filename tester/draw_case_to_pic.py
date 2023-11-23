from main_constructions import Program, ProgramRealisation

from utils import draw_ECG

import matplotlib.pyplot as plt


def draw_case_to_pic(signal, program, program_realisation):
    fig, ax = plt.subplots()
    draw_ECG(ax, signal)

    signal_len = len(signal)

    program.draw(signal_len, ax)
    program_realisation.draw(ax)

    ax.legend()
    return fig

