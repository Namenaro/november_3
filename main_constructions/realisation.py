from .segment_info import SegmentInfo
from utils import IdGenedator
from interpolation1d import Interpolator
from .program import Program


class ProgramRealisation:
    def __init__(self, program, signal):
        self.program = program  # только она знает линкерную информацию, которая нужна для преобразования в ii + посчитать ошибку стат. и динамич. предсказаний
        self.points_names_to_points = {}  # имя точки - abs_координата_реальная
        self.signal = signal

    def add(self, point_name, point_coord_real):
        self.points_names_to_points[point_name] = point_coord_real

    def _to_interpolator(self):
        interp = Interpolator(signal_len=len(self.signal))
        for segment_name in self.program.segments_order:
            seg_info = self.program.names_to_segments_ifo[segment_name]
            name1 = seg_info.name1
            u1_real = self.points_names_to_points[name1]
            v1_real = self.signal[u1_real]

            name2 = seg_info.name2
            u2_real = self.points_names_to_points[name2]
            v2_real = self.signal[u2_real]

            interp.add_new_segment(index1=u1_real, v1=v1_real, index2=u2_real, v2=v2_real, name1=name1, name2=name2)

        return interp

    def get_e(self):
        interpolator = self._to_interpolator()
        prediction = interpolator.get_interpolation()
        es = list([abs(self.signal[i] - prediction[i]) for i in range(len(prediction))])
        e = sum(es)
        return e

    def get_uv_static(self):
        us = []
        vs = []
        for segment_name in self.program.segments_oder:
            sement_info = self.program.names_to_segments_ifo[segment_name]
            v1, abs_u1, v2, abs_u2 = sement_info.get_static_prediction()
            # реальные u1,u2,v1,v2 берем из self
            real_u1 = self.points_names_to_points[sement_info.name1]
            real_u2 = self.points_names_to_points[sement_info.name2]
            real_v1 = self.signal[real_u1]
            real_v2 = self.signal[real_u2]

            u_err1 = abs(real_u1 - abs_u1)
            u_err2 = abs(real_u2 - abs_u2)

            v_err1 = abs(real_v1 - v1)
            v_err2 = abs(real_v2 - v2)

            us.append(u_err1 + u_err2)
            vs.append(v_err1 + v_err2)


        return us, vs

    def get_uv_dynamic(self):
        us = []
        vs = []
        for segment_name in self.program.segments_order:
            sement_info = self.program.names_to_segments_ifo[segment_name]
            parent_name = sement_info.parent_name_for1
            if parent_name is None:
                parent_abs_coord = None
            else:
                parent_abs_coord = self.points_names_to_points[parent_name]
            v1, abs_u1, v2, abs_u2 = sement_info.get_dynamic_prediction(parent_abs_coord)
            # реальные u1,u2,v1,v2 берем из self
            real_u1 = self.points_names_to_points[sement_info.name1]
            real_u2 = self.points_names_to_points[sement_info.name2]
            real_v1 = self.signal[real_u1]
            real_v2 = self.signal[real_u2]

            u_err1 = abs(real_u1 - abs_u1)
            u_err2 = abs(real_u2 - abs_u2)

            v_err1 = abs(real_v1 - v1)
            v_err2 = abs(real_v2 - v2)

            us.append(u_err1 + u_err2)
            vs.append(v_err1 + v_err2)


        return us, vs

    def draw(self, ax):
        interp = self._to_interpolator()
        interp.draw(ax, color='green', label="реализация")

    def get_num_events(self):
        return len(self.points_names_to_points)

