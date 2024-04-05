from rf.radar.component import Radar


def get_circular(radar: Radar) -> float:
    """
    Computa o número de pulsos sobre o alvo usando uma varredura circular.
    Nesse caso, a velocidade ângular do radar deve ser [rad/s].

    :param radar: parâmetros do radar
    :return: número de pulsos sobre o alvo como float
    """

    time = radar.beam_width / radar.angular_velocity  # [s]
    return radar.pulse_repetition * time


def get_conic(radar: Radar) -> float:
    """
    Computa o número de pulsos sobre o alvo usando uma varredura cônica.
    Nesse caso, a velocidade ângular do radar deve ser revoluções por segundo.

    :param radar: parâmetros do radar
    :return: número de pulsos sobre o alvo como float
    """

    time = 1.0 / radar.angular_velocity  # assumindo: feixe sempre sobre o alvo
    return radar.pulse_repetition * time
