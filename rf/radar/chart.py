from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from matplotlib.figure import Figure

from rf.radar.component import Radar, Target
from rf.radar.equation import get_ranges, get_snrs
from rf.utils.charts import new_chart
from rf.utils.constants import METERS_TO_NAUTIC_MILES, NAUTIC_MILES_TO_METERS
from rf.radar.scan import get_circular


def plot_snrs(
    start: float,
    end: float,
    step: float,
    radar: Radar,
    target: Target,
    losses: float,
) -> Tuple[Figure, Tuple[npt.NDArray[np.float64]], npt.NDArray[np.float64]]:
    """
    Plota uma figura:
        - Relação Sinal-Ruído em função da Distância

    :param start: distância mínima para análise em milhas náuticas [nm]
    :param end: distância máxima para análise em milhas náuticas [nm]
    :param step: resolução da distância para análise em milhas náuticas [nm]
    :param radar: parâmetros do radar
    :param target: parâmetros do alvo
    :param losses: perdas durante o processo [dB]
    :return: tupla com a figura plotada e os dados brutos (Dist, SNR)
    """

    dists = np.arange(start, end, step, dtype=np.float64)

    num_pulses = get_circular(radar)

    snrs = get_snrs(
        radar,
        target,
        losses,
        num_pulses,
        dists * NAUTIC_MILES_TO_METERS,
    )

    figure = new_chart()
    axes = figure.subplots()
    axes.grid()
    axes.plot(dists, snrs, linewidth=2)
    plt.xlim(start, end)
    plt.ylim(np.min(snrs), np.max(snrs))
    plt.title("Radar gain profile")
    plt.xlabel("Distance ($nm$)")
    plt.ylabel("Signal-Noise ratio ($dB$)")
    plt.tight_layout()

    return (figure, (dists, snrs))


def plot_ranges(
    start: float,
    end: float,
    step: float,
    radar: Radar,
    target: Target,
    losses: float,
) -> Tuple[Figure, Tuple[npt.NDArray[np.float64]], npt.NDArray[np.float64]]:
    """
    Plota uma figura:
        - Distância em função da Relação Sinal-Ruído

    :param start: distância mínima para análise em milhas náuticas [nm]
    :param end: distância máxima para análise em milhas náuticas [nm]
    :param step: resolução da distância para análise em milhas náuticas [nm]
    :param radar: parâmetros do radar
    :param target: parâmetros do alvo
    :param losses: perdas durante o processo [dB]
    :return: tupla com a figura plotada e os dados brutos (SNR, Dist)
    """

    snrs = np.arange(start, end, step, dtype=np.float64)

    num_pulses = get_circular(radar)

    ranges = get_ranges(radar, target, losses, num_pulses, snrs)

    ranges *= METERS_TO_NAUTIC_MILES

    figure = new_chart()
    axes = figure.subplots()
    axes.grid()
    axes.plot(snrs, ranges, linewidth=2)
    plt.xlim(start, end)
    plt.ylim(np.min(ranges), np.max(ranges))
    plt.title("Radar range profile")
    plt.xlabel("Signal-Noise ratio ($dB$)")
    plt.ylabel("Distance ($nm$)")
    plt.tight_layout()

    return (figure, (snrs, ranges))
