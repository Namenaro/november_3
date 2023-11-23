

class SegmentInfo:
    def __init__(self, name1, name2, parent_name_for1, abs_coord1, abs_coord2, v1, v2, du_from_parent):
        self.name1 = name1
        self.name2 = name2
        self.parent_name_for1 = parent_name_for1
        self.abs_coord1 = abs_coord1
        self.abs_coord2 = abs_coord2
        self.v1 = v1
        self.v2 = v2
        self.du_from_parent = du_from_parent

    def get_static_prediction(self):
        v1 = self.v1
        abs_u1 = self.abs_coord1
        v2 = self.v2
        abs_u2 = self.abs_coord2

        return v1, abs_u1, v2, abs_u2

    def get_dynamic_prediction(self, parent_abs_coord):
        v1 = self.v1
        v2 = self.v2
        if parent_abs_coord is not None:
            abs_u1 = parent_abs_coord + self.du_from_parent
        else:
            abs_u1 = self.abs_coord1
        abs_u2 = abs_u1 + (self.abs_coord2 - self.abs_coord1)

        return v1, abs_u1, v2, abs_u2

