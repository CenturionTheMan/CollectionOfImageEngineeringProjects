import matplotlib.pyplot as plt
import numpy as np


def plot(data, title, rows, columns, index):
    plt.subplot(rows, columns, index)
    plt.imshow(data)
    plt.gray()
    plt.axis('off')
    plt.title(title)
    plt.tight_layout(pad=1, w_pad=0.8, h_pad=0.5)


def mse(base_image, mod_image, round_dig=2):
    return round(np.square(np.subtract(base_image, mod_image)).mean(), 2)


def create_single_dot_line_plt(X: list, Y: list, x_axis_name: str = "", y_axis_name: str = "", title: str = "",
                               x_ax_numbers=None, line_style='--o', line_width=1, show_points_value=True, output_path: str = None):
    f = plt.figure()
    #f.set_figwidth(plot_width)
    #f.set_figheight(plot_height)
    plt.plot(X, Y, line_style, linewidth=line_width)
    plt.xlabel(x_axis_name)
    plt.ylabel(y_axis_name)
    plt.title(title)

    y_max = max(Y)

    if show_points_value:
        for x_pos, y_pos in zip(X,Y):
            plt.text(x_pos, y_pos + y_max * 0.02, y_pos, ha="center")
        plt.ylim(-y_max*0.01, y_max * 1.1)

    if x_ax_numbers is not None:
        plt.xticks(x_ax_numbers)

    if output_path is not None:
        plt.savefig(output_path)
    plt.show()
