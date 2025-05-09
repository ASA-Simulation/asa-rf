from typing import Tuple
from math import radians

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from rf.utils.charts import new_chart
from rf.utils.constants import PI, NAUTIC_MILES_TO_METERS, NAUTIC_MILES_TO_FEET
from rf.antenna.gain import get_scale


def plot_azimuth_gains(
    max_range: float,
    beam_width: float,
) -> Tuple[Figure, Figure]:
    """
    Plota duas figuras:
        - Distribuição espacial do lóbulo de emissão da antena
        - Ganho da antena em função do ângulo de azimute

    :param max_range: alcance máximo em milhas náuticas [nm]
    :param beam_width: largura do feixe em graus [deg]
    :return: tupla com as duas figuras plotadas
    """

    angles = np.arange(-PI / 24.0, PI / 24.0, 0.001 * PI / 180.0, dtype=np.float64)

    scale = get_scale(beam_width)
    gains = np.abs(np.sin(scale * angles) / (scale * angles))

    np.nan_to_num(gains, copy=False, nan=0.0, posinf=np.inf, neginf=-np.inf)

    y = max_range * np.sqrt(gains) * np.cos(angles)
    x = (
        max_range * np.sqrt(gains) * np.sin(angles) * NAUTIC_MILES_TO_METERS / 1_000.0
    )  # nm to km

    figure1 = new_chart()
    axes = figure1.subplots()
    axes.grid()
    axes.plot(x, y, linewidth=2)
    plt.xlim(np.min(x), np.max(x))
    plt.ylim(np.min(y), np.max(y))
    plt.title("Antenna Range Profile in Azimuth")
    plt.xlabel("$x$ ($km$)")
    plt.ylabel("$y$ ($km$)")
    plt.tight_layout()

    y = gains
    x = angles * 180.0 / PI

    figure2 = new_chart()
    axes = figure2.subplots()
    axes.grid()
    axes.plot(x, y, linewidth=2)
    plt.xlim(np.min(x), np.max(x))
    plt.ylim(np.min(y), np.max(y))
    plt.title("Antenna Gain Profile in Azimuth")
    plt.xlabel("$\\theta$ ($deg$)")
    plt.ylabel("Gain")
    plt.tight_layout()

    return (figure1, figure2)


def plot_elevation_gains(
    max_range: float, max_elev: float, min_elev: float, tgt_ang: float, factor: float
) -> Tuple[Figure, Figure]:
    """
    Plota duas figuras:
        - Distribuição espacial do lóbulo de emissão da antena
        - Ganho da antena em função do ângulo de elevação

    :param max_range: alcance máximo em milhas náuticas [nm]
    :param max_elev: ângulo de elevação máximo de projeto [deg]
    :param min_elev: ângulo de elevação máximo de projeto [deg]
    :param tgt_ang: ângulo de elevação do alvo esperado [deg]
    :param factor: fator adimensional de escala
    :param beam_width: largura do feixe em graus [deg]
    :return: tupla com as duas figuras plotadas
    """

    # Primeiro caso: da elevação mínima até o ângulo do alvo esperado

    angles_1st = np.arange(
        radians(min_elev), radians(tgt_ang), radians(0.001), dtype=np.float64
    ) - radians(tgt_ang)
    gains_1st = np.sin(factor * angles_1st) / (factor * angles_1st)

    np.nan_to_num(gains_1st, copy=False, nan=1.0, posinf=np.inf, neginf=-np.inf)

    x_2nd = max_range * np.sqrt(gains_1st) * np.cos(angles_1st)
    y_2nd = max_range * np.sqrt(gains_1st) * np.sin(angles_1st) * NAUTIC_MILES_TO_FEET

    # Segundo caso: do ângulo do alvo esperado até a elevação máxima

    angles_2nd = np.arange(
        radians(tgt_ang), radians(max_elev), radians(0.001), dtype=np.float64
    )
    gains_2nd = np.power(np.sin(angles_2nd), -2.0) / np.power(
        np.sin(radians(tgt_ang)), -2.0
    )

    np.nan_to_num(gains_2nd, copy=False, nan=0.0, posinf=np.inf, neginf=-np.inf)

    x_1st = max_range * np.sqrt(gains_2nd) * np.cos(angles_2nd)
    y_1st = max_range * np.sqrt(gains_2nd) * np.sin(angles_2nd) * NAUTIC_MILES_TO_FEET

    # Juntando as curvas:

    xs = np.concatenate([[0], x_2nd, x_1st, [0]])
    ys = np.concatenate([[0], y_2nd, y_1st, [0]])

    figure1 = new_chart()
    axes = figure1.subplots()
    axes.grid()
    axes.plot(xs, ys, linewidth=2)
    plt.title("Antenna Range Profile in Elevation")
    plt.xlabel("$x$ ($km$)")
    plt.ylabel("$y$ ($feet$)")
    plt.tight_layout()

    xs = np.concatenate([angles_1st, angles_2nd]) * 180.0 / PI
    ys = np.concatenate([gains_1st, gains_2nd])

    figure2 = new_chart()
    axes = figure2.subplots()
    axes.grid()
    axes.plot(xs, ys, linewidth=2)
    plt.title("Antenna Gain Profile in Elevation")
    plt.xlabel("$\phi$ ($deg$)")
    plt.ylabel("Gain")
    plt.tight_layout()

    return (figure1, figure2)
