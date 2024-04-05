from math import radians


def get_scale(
    beam_width: float,
) -> float:
    """
    Computa o fator de escala para ajustar a largura do feixe.

    :param beam_width: largura do feixe em graus [deg]
    :return: valor do fator de escala adimensional
    """

    # sin(x) / x = 0.5 (~= -3dB) => x ~= 1.89549
    # x = k * theta => k = 1.89275 / theta
    return 1.89549 / radians(beam_width / 2.0)
