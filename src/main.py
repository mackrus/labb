from error import main as error_main
from plot_data_A import main as plot_a_main
from plot_data_B import main as plot_b_main
from plot_planck import main as plot_planck_main


def main() -> None:
    plot_a_main()
    plot_b_main()
    plot_planck_main()
    error_main()


if __name__ == "__main__":
    main()
