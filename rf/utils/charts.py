from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.figure import Figure


def new_chart() -> Figure:
    plt.rcParams.update({"font.family": "serif"})
    plt.rcParams.update({"font.size": 16})
    return plt.figure()


def save_chart(figure: Figure, filename: str) -> None:
    base = Path(
        "./data"
    )  # todas as figuras são salvas em data (seu conteúdo não é versionado)
    figure.savefig(base / f"{filename}.eps", format="eps")
    figure.savefig(base / f"{filename}.png", format="png", dpi=400)
