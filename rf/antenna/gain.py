from math import radians


def get_scale(
    beam_width: float,
) -> float:
    """
    Computa o fator de escala para ajustar a largura do feixe.

    :param beam_width: largura do feixe em graus [deg]
    :return: valor do fator de escala adimensional
    """

    # d/dx [sin(x)/x] = 0 => x = tan(x) => x != 0, x ~= 4.49340945790906
    # x = k * theta => k = 4.49340945790906 / theta
    return 4.49340945790906 / radians(beam_width / 2.0)
