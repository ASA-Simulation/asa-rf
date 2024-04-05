from math import pow

import numpy as np
import numpy.typing as npt

from rf.radar.component import Radar, Target
from rf.utils.constants import BOLTZMANN_CONST, LIGHT_SPEED, PI, SYSTEM_TEMPERATURE


def get_snrs(
    radar: Radar,
    target: Target,
    losses: float,
    num_pulses: float,
    ranges: npt.NDArray[np.float64],
) -> npt.NDArray[np.float64]:
    """
    Computa a relação sinal-ruído em função da distância fornecida.
    Usa a Equação Geral do Radar em uma forma vetorial.

    :param radar: parâmetros do radar
    :param target: parâmetros do alvo
    :param losses: perdas durante o processo [dB]
    :param num_pulses: número de pulsos
    :param ranges: distâncias para as quais calcular a relação sinal-ruído
    :return: numpy array com os valores da relação sinal-ruído
    """

    # converte valores em dB para escala normal
    antenna_gain = pow(10.0, radar.antenna_gain / 10.0)
    noise_figure = pow(10.0, radar.noise_figure / 10.0)
    losses = pow(10.0, losses / 10.0)

    # calcula o comprimento de onda em [m]
    wavelength: float = LIGHT_SPEED / radar.frequency

    # calcula o ganho de compressão
    pulse_width_c: float = 1.0 / radar.band_width  # [s]
    N = radar.pulse_width / pulse_width_c
    if N < 1:
        # há alguma incoerência com os parâmetros passados
        N = 1

    # fmt: off
    snr = np.power(ranges, -4.0) * ( radar.peak_power * pow(antenna_gain, 2.0) * pow(wavelength, 2.0) * target.rcs * N * num_pulses) \
        / (pow(4 * PI, 3.0) * (BOLTZMANN_CONST * SYSTEM_TEMPERATURE * noise_figure * radar.band_width) * losses)
    # fmt: on

    # converte para dB
    return np.log10(snr) * 10.0


def get_ranges(
    radar: Radar,
    target: Target,
    losses: float,
    num_pulses: float,
    snrs: npt.NDArray[np.float64],
) -> npt.NDArray[np.float64]:
    """
    Computa a distância em função da relação sinal-ruído fornecida.
    Usa a Equação Geral do Radar em uma forma vetorial.

    :param radar: parâmetros do radar
    :param target: parâmetros do alvo
    :param losses: perdas durante o processo [dB]
    :param num_pulses: número de pulsos
    :param snrs: relação sinal-ruído para as quais calcular a distância
    :return: numpy array com os valores da distância
    """

    # converte valores em dB para escala normal
    antenna_gain = pow(10.0, radar.antenna_gain / 10.0)
    noise_figure = pow(10.0, radar.noise_figure / 10.0)
    losses = pow(10.0, losses / 10.0)

    snrs = np.power(10.0, snrs / 10.0)

    # calcula o comprimento de onda em [m]
    wavelength: float = LIGHT_SPEED / radar.frequency

    # calcula o ganho de compressão
    pulse_width_c: float = 1.0 / radar.band_width  # [s]
    N = radar.pulse_width / pulse_width_c
    if N < 1:
        # há alguma incoerência com os parâmetros passados
        N = 1

    # fmt: off
    ranges = np.power(snrs, -1.0) * ( radar.peak_power * pow(antenna_gain, 2.0) * pow(wavelength, 2.0) * target.rcs * N * num_pulses) \
        / (pow(4.0 * PI, 3.0) * (BOLTZMANN_CONST * SYSTEM_TEMPERATURE * noise_figure * radar.band_width) * losses)
    # fmt: on

    return np.power(ranges, 1.0 / 4.0)


def get_snr(
    radar: Radar,
    target: Target,
    losses: float,
    num_pulses: float,
    range: float,
) -> npt.NDArray[np.float32]:
    """
    Computa a relação sinal-ruído em função da distância fornecida.
    Usa a Equação Geral do Radar em uma forma escalar (não otimizada).

    :param radar: parâmetros do radar
    :param target: parâmetros do alvo
    :param losses: perdas durante o processo [dB]
    :param num_pulses: número de pulsos
    :param range: distância para a qual calcular a relação sinal-ruído
    :return: valor da relação sinal-ruído
    """

    ranges = np.array([range], dtype=np.float64)
    values = get_snrs(
        radar,
        target,
        losses,
        num_pulses,
        ranges,
    )
    return values[0]


def get_range(
    radar: Radar,
    target: Target,
    losses: float,
    num_pulses: float,
    snr: float,
) -> npt.NDArray[np.float32]:
    """
    Computa a distância em função da relação sinal-ruído fornecida.
    Usa a Equação Geral do Radar em uma forma escalar (não otimizada).

    :param radar: parâmetros do radar
    :param target: parâmetros do alvo
    :param losses: perdas durante o processo [dB]
    :param num_pulses: número de pulsos
    :param snr: relação sinal-ruído para a qual calcular a distância
    :return: valor da distância
    """

    snrs = np.array([snr], dtype=np.float64)
    ranges = get_ranges(
        radar,
        target,
        losses,
        num_pulses,
        snrs,
    )
    return ranges[0]
