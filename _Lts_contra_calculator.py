import re
import pandas


class Mixin:

    def __init__(self):
        print("lts calculator")
        pass

    def calc_c_lts(self, m_id_cycl, spd_q85, lane_p_direction, one_way,
                   centerline, cyclway_attr):

        # only where contraflow is allowed, which is 4,44 and 3,30, 3,31  3,33
        on_street_contra_bikelane = 0

        if pandas.isna(m_id_cycl):  # coming from geobase layer (on-street and mixed traffic)
            if 'type_voie' in cyclway_attr.keys():  # 1. road could have a bike lane or a nearby off-street path or both 2. mixed traffic with nearby off-street path --use gestion
                if cyclway_attr['type_voie'] == 3:
                    if cyclway_attr['type_voie2'] in (30, 31, 33) or cyclway_attr['ed_typvoi2'] in (
                            31, 30, 33):  # contraflow bikelane
                        # and no with-flow bikelane
                        on_street_contra_bikelane = 1
                    else:
                        _c_lts = -9999

                elif cyclway_attr['type_voie'] == 4:
                    if cyclway_attr['type_voie2'] == 44 or cyclway_attr[
                            'ed_typvoi2'] == 44:  # paths and protected track
                        _c_lts = 1
                    else:
                        _c_lts = -9999

                else:  # 0, -9999 city has not got around categorizing the bike facility yet-- could be anything
                    _c_lts = -9999

            else:
                _c_lts = -9999

        else:  # coming from off-street path layer
            _c_lts = -9999

        # Protected and paths
        if 'contraProt' in cyclway_attr.keys() and re.search('yes', str(cyclway_attr['contraProt']),
                                                             re.IGNORECASE):
            _c_lts = 1

        # assigning LTS to on_street contraflow bikelanes
        if on_street_contra_bikelane == 1:
            if 'contraLanW' in cyclway_attr.keys() and float(cyclway_attr['contraLanW']) > 0:

                # TABLE 2
                if ('contraParW' in cyclway_attr.keys()) and (float(cyclway_attr['contraParW']) > 0):
                    if lane_p_direction == 1:
                        if float(cyclway_attr['contraReac']) >= 4.5:
                            if float(spd_q85) <= 46:
                                _c_lts = 1
                            elif float(spd_q85) <= 54:
                                _c_lts = 2
                            elif float(spd_q85) <= 62:
                                _c_lts = 2
                            elif float(spd_q85) > 62:
                                _c_lts = 3
                            else:
                                _c_lts = 'c1'
                        elif 4.4 >= float(cyclway_attr['contraReac']) >= 3.5:
                            if spd_q85 <= 54:
                                _c_lts = 2
                            elif spd_q85 <= 62:
                                _c_lts = 3
                            elif spd_q85 > 62:
                                _c_lts = 3
                            else:
                                _c_lts = 'c2'
                        else:
                            _c_lts = 'c3'
                    elif lane_p_direction == 2 and one_way == 0:
                        if float(cyclway_attr['contraReac']) >= 4.5:
                            if spd_q85 <= 46:
                                _c_lts = 2
                            elif spd_q85 <= 54:
                                _c_lts = 3
                            elif spd_q85 <= 62:
                                _c_lts = 3
                            elif spd_q85 > 62:
                                _c_lts = 3
                            else:
                                _c_lts = 'c4'
                        else:
                            _c_lts = 3  # any other multilane
                    elif (lane_p_direction in [2, 3]) and (one_way in [-1, 1]):
                        if float(cyclway_attr['contraReac']) >= 4.5:
                            if spd_q85 <= 46:
                                _c_lts = 2
                            elif spd_q85 <= 54:
                                _c_lts = 3
                            elif spd_q85 <= 62:
                                _c_lts = 3
                            elif spd_q85 > 62:
                                _c_lts = 3
                            else:
                                _c_lts = 'c6'

                        elif float(cyclway_attr['contraReac']) < 4.5:
                            _c_lts = 3
                        else:
                            _c_lts = 3
                    elif lane_p_direction > 1:  # any other multilane
                        _c_lts = 3
                    else:
                        _c_lts = 'c7'

                else:
                    # TABLE 3  -- not next to a parking space
                    if lane_p_direction == 1 or centerline == 0:
                        if 'contraReac' in cyclway_attr.keys():
                            if float(cyclway_attr['contraReac']) >= 1.8:
                                if spd_q85 <= 54:
                                    _c_lts = 1
                                elif 62 >= spd_q85 > 54:
                                    _c_lts = 2
                                elif spd_q85 > 62:
                                    _c_lts = 3
                                else:
                                    _c_lts = 'c8'
                            elif float(cyclway_attr['contraReac']) < 1.8:
                                if spd_q85 <= 62:
                                    _c_lts = 2
                                elif 78 >= spd_q85 > 62:
                                    _c_lts = 3
                                else:
                                    _c_lts = 4
                            else:
                                _c_lts = 'c9'
                        else:
                            _c_lts = 'c10'
                    elif lane_p_direction == 2:
                        if 'contraReac' in cyclway_attr.keys():
                            if float(cyclway_attr['contraReac']) >= 1.8:
                                if spd_q85 <= 62:
                                    _c_lts = 2
                                else:
                                    _c_lts = 3
                            elif float(cyclway_attr['contraReac']) < 1.8:
                                if spd_q85 <= 62:
                                    _c_lts = 2
                                elif 70 >= spd_q85 > 62:
                                    _c_lts = 3
                                else:
                                    _c_lts = 4
                            else:
                                _c_lts = 'c11'
                    elif lane_p_direction >= 3:
                        if spd_q85 <= 62:
                            _c_lts = 3
                        else:
                            _c_lts = 4
                    else:
                        _c_lts = 'c12'
            else:
                _c_lts = -8888  # no info on the width of the bikelane type 3
        else:
            _c_lts = -9999

        return _c_lts
