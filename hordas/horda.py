class Horda: # физическая инфа о хорда
    def __init__(self, u1, u2, v1,v2, abs_err):
        self.u1 = u1
        self.u2 = u2
        self.v1 = v1
        self.v2 = v2
        self.abs_err = abs_err

    def get_abs_u_redaction(self, center_coord):
        return abs(self.u1-center_coord) + abs(self.u2-center_coord)

    def get_abs_v_redaction(self):
        return abs(self.v1) + abs(self.v2)

    def get_abs_err(self):
        return self.abs_err



class HordasSample: # заполнять физическую инфу о хордах
    def __init__(self, signal):
        self.signal = signal
        self.hordas = self._fill()

    def _fill(self, SAMPLE_LEN=100):
        hordas = []
        for i in range(SAMPLE_LEN):
            horda = self._create_horda()
            hordas.append(horda)
        return hordas

    def _create_horda(self):
        u1 =
        u2 =
        v1 =self.signal[u1]
        horda = Horda(u1, u2, v1,v2, abs_err)
        return horda









