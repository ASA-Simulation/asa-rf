from dataclasses import dataclass


@dataclass
class Radar:
    """
    Parâmetros para a modelagem de um radar.

    :param peak_power: potência de pico em Watts [W]
    :param antenna_gain: ganho da antena em [dB]
    :param frequency: frequência de transmissão em Hertz [Hz]
    :param noise_figure: figura de ruído em [dB]
    :param band_width: largura de banda em [Hz]
    :param pulse_width: largura do pulso em [s]
    :param pulse_repetition: frequência de repetição do pulso em [Hz]
    :param beam_width: largura do feixe em [rad]
    :param angular_velocity: velocidade angular da varredura (significado depende do seu tipo)
    """

    peak_power: float
    antenna_gain: float
    frequency: float
    noise_figure: float
    band_width: float
    pulse_width: float
    pulse_repetition: float
    beam_width: float
    angular_velocity: float  # circular => ômega; cônica => número de revoluções por segundo


@dataclass
class Target:
    """
    Parâmetros para a modelagem do alvo de um radar.

    :param rcs: seção reta radar em [m^2]
    """

    rcs: float
