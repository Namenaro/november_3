from .segment_info import SegmentInfo
from utils import IdGenedator
from interpolation1d import Interpolator


class Program:
    def __init__(self):
        self.seg_names_generator = IdGenedator(prefix="seg_")

        self.segments_order = []  # [segment_name1, segment_name2,...]
        self.names_to_segments_ifo = {}  # segment_name: SegmentInfo

    def add_segment(self, name1, name2, parent_name_for1, abs_coord1, abs_coord2, v1, v2, du_from_parent):
        seg_name = self.seg_names_generator.get_id()
        segment_ifo = SegmentInfo(name1, name2, parent_name_for1, abs_coord1, abs_coord2, v1, v2, du_from_parent)
        self.names_to_segments_ifo[seg_name] = segment_ifo
        self.segments_order.append(seg_name)

    def draw(self, signal_len, ax):
        interp = Interpolator(signal_len=signal_len)

        for segment_name in self.segments_order:
            seg_info = self.names_to_segments_ifo[segment_name]
            interp.add_new_segment(index1=seg_info.abs_coord1, v1=seg_info.v1, index2=seg_info.abs_coord2, v2=seg_info.v2, name1=seg_info.name1, name2=seg_info.name2)


        interp.draw(ax, color='blue', label="программа")

    def get_num_segments(self):
        return len(self.names_to_segments_ifo)
