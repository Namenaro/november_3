import matplotlib.pyplot as plt

from .segment import InterpolationSegment

class Point:
    def __init__(self, u, v, name):
        self.u = u
        self.v = v
        self.name = name

class Interpolator:
    def __init__(self, signal_len):
        self.signal_len = signal_len
        self.segments = []  # [InterpolationSegment, InterpolationSegment,...]
        self.points = []

        self.coords_to_predictions = {}  # над любой точкой сцены самое новое предсказание (хронологичски добавленное)

        for coord in range(signal_len):
            self.coords_to_predictions[coord] = 0

        self._fill_prediction()

    def get_interpolation(self):
        pointwise_prediction = []
        for coord in range(self.signal_len):
            pointwise_prediction.append(self.coords_to_predictions[coord])
        return pointwise_prediction

    def add_new_segment(self, index1, v1, index2, v2, name1, name2):
        seg = InterpolationSegment(index1, v1, index2, v2)
        self.segments.append(seg)
        self.points.append(Point(u=index1, v=v1, name=name1))
        self.points.append(Point(u=index2, v=v2, name=name2))


        vals = seg.get_vals_from_left()
        indexes = seg.get_indexes_from_left()

        for i in range(len(vals)):
            coord = indexes[i]
            val = vals[i]

            self.coords_to_predictions[coord] = val

    def _fill_prediction(self):
        for seg in self.segments:

            vals = seg.get_vals_from_left()
            indexes = seg.get_indexes_from_left()

            for i in range(len(vals)):
                coord = indexes[i]
                val = vals[i]

                self.coords_to_predictions[coord] = val

    def draw(self, ax, color, label=None):
        pointwise_prediction = self.get_interpolation()

        ax.plot(pointwise_prediction, 'o-',  c=color, markersize=2, alpha=0.8, label=label)

        for point in self.points:
            ax.scatter(point.u, point.v, c=color)
            ax.annotate(str(point.name), (point.u, point.v), xytext=(5, 2), c=color, textcoords='offset points',  weight='bold',  alpha=0.8)
        plt.legend()

    def get_abs_error(self, signal):
        abs_err = 0
        prediction = self.get_interpolation()
        for i in range(len(signal)):
            signal_val = signal[i]
            predicion_val = prediction[i]
            err = abs(signal_val - predicion_val)
            abs_err += err
        return abs_err


