from .horda import HordasSample, Horda

from pandas import DataFrame


class RNoProbability: # нормируем сигмы через средние. Все параметры нормируются через свое абсолютное среднее (раздельно каждый)
    def __init__(self, hordas_sample, signal):
        self.signal = signal
        self.hordas_sample = hordas_sample
        self.center_coord = len(signal) / 2


    def get_mean_abs_u_readction(self):
        abs_u_redaction = 0
        for horda in self.hordas_sample.get_hordas():
            abs_u_redaction += horda.get_abs_u_redaction(center_coord=self.center_coord)
        mean_abs_u_readction = abs_u_redaction /len(self.hordas_sample.get_hordas())
        return mean_abs_u_readction

    def get_mean_abs_v_readction(self):
        abs_v_redaction = 0
        for horda in self.hordas_sample.get_hordas():
            abs_v_redaction += horda.get_abs_v_redaction()
        mean_abs_v_readction = abs_v_redaction /len(self.hordas_sample.get_hordas())
        return mean_abs_v_readction

    def get_mean_abs_err(self):
        abs_err = 0
        for horda in self.hordas_sample.get_hordas():
            abs_err  += horda.get_abs_err()
        mean_abs_err = abs_err / len(self.hordas_sample.get_hordas())
        return mean_abs_err

    def get_sigma_u(self, real_abs_u, len_program):
        naive_u_one_step = self.get_mean_abs_u_readction()
        expected_naive_u = naive_u_one_step *len_program
        # если реальный больге наивного, то сигма отрицательная
        sigma_u = (expected_naive_u -real_abs_u )/ expected_naive_u
        return sigma_u

    def get_sigma_v(self, real_abs_v , len_program):
        naive_v_one_step = self.get_mean_abs_v_readction()
        expected_naive_v = naive_v_one_step * len_program
        # если реальный больге наивного, то сигма отрицательная
        sigma_v = (expected_naive_v -real_abs_v) / expected_naive_v
        return sigma_v

    def get_sigma_err(self, real_abs_err, len_program):
        naive_err_one_step = self.get_mean_abs_err()
        expected_naive_err = naive_err_one_step * len_program
        # если реальный больге наивного, то сигма отрицательная
        sigma_err = (expected_naive_err - real_abs_err) / expected_naive_err
        return sigma_err

    def get_r(self, program_realisation, program, log): # длина программы это кол-во сегментов, а не точек! real_abs_u - это именно на сегменте!
        real_abs_err = program_realisation.get_e()
        n_segments = program.get_num_segments()
        us, vs = program_realisation.get_uv_dynamic()
        real_abs_v = sum(vs)
        real_abs_u = sum(us)

        sigma_err = self.get_sigma_err(real_abs_err, len_program=n_segments)
        sigma_u = self.get_sigma_u(real_abs_u, len_program=n_segments)
        sigma_v = self.get_sigma_v(real_abs_v, len_program=n_segments)
        r = sigma_err+ sigma_v + sigma_u

        LOG_DICT = {}
        LOG_DICT["r"] = r
        LOG_DICT["sigma_err"] = sigma_err
        LOG_DICT["sigma_u"] = sigma_u
        LOG_DICT["sigma_v"] = sigma_v
        self.to_log(LOG_DICT, log)

        # TODO можно sigma_redaction = сумма сигм по всем параметрам / колво параметров.
        #Тогда редакция это по сути выигрыш на символ, т.е. оно становится соразмерно  величине sigma_err

        return r

    def to_log(self, map, log):
        temp = {}
        for name, val in map.items():
            temp[name] = [val]

        data_frame = DataFrame.from_dict(temp)
        log.add_dataframe(data_frame)