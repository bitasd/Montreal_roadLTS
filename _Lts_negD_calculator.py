import re
import pandas


class Mixin:

    def __init__(self):
        print("lts calculator")
        pass

    def calc_lts_negD(self, m_id_cycl, m_gestion, spd_q85, lane_p_direction, one_way, adt,
                 centerline, cyclway_attr):

        mixed_traffic = 0
        on_street_bikelane = 0  # type_voie: 3, 4, 9

        if pandas.isna(m_id_cycl):  # coming from geobase layer(on-street and mixed traffic)
            if 'type_voie' in cyclway_attr.keys():  # 1. road could have a bike lane or a nearby off-street path or both 2. mixed traffic with nearby off-street path --use gestion
                if cyclway_attr['type_voie'] in (3, 9):
                    if cyclway_attr['type_voie2'] in (30, 31) or cyclway_attr['ed_typvoi2'] in (
                            31, 30):  # contraflow bikelane
                        # and no with-flow bikelane
                        mixed_traffic = 1
                    else:
                        on_street_bikelane = 1

                elif cyclway_attr['type_voie'] in [4]:  # protected track
                    _lts = 1

                elif cyclway_attr['type_voie'] in [5, 6, 7]:  # paths
                    mixed_traffic = 1

                else:  # 0, -9999 city has not got around categorizing the bike facility yet-- could be anything
                    if cyclway_attr['cycl_gestion'] in (6, 11, 12):
                        mixed_traffic = 1  # mixed traffic with nearby off-street path
                    else:
                        on_street_bikelane = 1

            else:
                mixed_traffic = 1

        else:  # coming from off-street path layer
            _lts = 1

        # Protected and paths
        if 'Prot_negD' in cyclway_attr.keys() and re.search('yes', str(cyclway_attr['Prot_negD']),
                                                            re.IGNORECASE):
            _lts = 1
        if m_gestion in (11, 12):
            _lts = 1
        if m_gestion == 6:
            _lts = 'intrscton'

        # assigning LTS to on_street bikelanes and mixed traffic
        if on_street_bikelane == 1:
            if float(cyclway_attr['BLanW_negD']) > 0:

                # TABLE 2
                if ('ParkW_negD' in cyclway_attr.keys()) and (float(cyclway_attr['ParkW_negD']) > 0):
                    if lane_p_direction == 1:
                        if float(cyclway_attr['Reach_negD']) >= 4.5:
                            if float(spd_q85) <= 46:
                                _lts = 1
                            elif float(spd_q85) <= 54:
                                _lts = 2
                            elif float(spd_q85) <= 62:
                                _lts = 2
                            elif float(spd_q85) > 62:
                                _lts = 3
                            else:
                                _lts = 'c1'
                        elif 4.4 >= float(cyclway_attr['Reach_negD']) >= 3.5:
                            if spd_q85 <= 54:
                                _lts = 2
                            elif spd_q85 <= 62:
                                _lts = 3
                            elif spd_q85 > 62:
                                _lts = 3
                            else:
                                _lts = 'c2'
                        else:
                            _lts = 'c3'
                    elif lane_p_direction == 2 and one_way == 0:
                        if float(cyclway_attr['Reach_negD']) >= 4.5:
                            if spd_q85 <= 46:
                                _lts = 2
                            elif spd_q85 <= 54:
                                _lts = 3
                            elif spd_q85 <= 62:
                                _lts = 3
                            elif spd_q85 > 62:
                                _lts = 3
                            else:
                                _lts = 'c4'
                        else:
                            _lts = 3  # any other multilane
                    elif (lane_p_direction in [2, 3]) and (one_way in [-1, 1]):
                        if float(cyclway_attr['Reach_negD']) >= 4.5:
                            if spd_q85 <= 46:
                                _lts = 2
                            elif spd_q85 <= 54:
                                _lts = 3
                            elif spd_q85 <= 62:
                                _lts = 3
                            elif spd_q85 > 62:
                                _lts = 3
                            else:
                                _lts = 'c6'

                        elif float(cyclway_attr['Reach_negD']) < 4.5:
                            _lts = 3
                        else:
                            _lts = 3
                    elif lane_p_direction > 1:  # any other multilane
                        _lts = 3
                    else:
                        _lts = 'c7'

                else:
                    # TABLE 3  -- not next to a parking space
                    if lane_p_direction == 1 or centerline == 0:
                        if 'Reach_negD' in cyclway_attr.keys():
                            if float(cyclway_attr['Reach_negD']) >= 1.8:
                                if spd_q85 <= 54:
                                    _lts = 1
                                elif 62 >= spd_q85 > 54:
                                    _lts = 2
                                elif spd_q85 > 62:
                                    _lts = 3
                                else:
                                    _lts = 'c8'
                            elif float(cyclway_attr['Reach_negD']) < 1.8:
                                if spd_q85 <= 62:
                                    _lts = 2
                                elif 78 >= spd_q85 > 62:
                                    _lts = 3
                                else:
                                    _lts = 4
                            else:
                                _lts = 'c9'
                        else:
                            _lts = 'c10'
                    elif lane_p_direction == 2:
                        if 'Reach_negD' in cyclway_attr.keys():
                            if float(cyclway_attr['Reach_negD']) >= 1.8:
                                if spd_q85 <= 62:
                                    _lts = 2
                                else:
                                    _lts = 3
                            elif float(cyclway_attr['Reach_negD']) < 1.8:
                                if spd_q85 <= 62:
                                    _lts = 2
                                elif 70 >= spd_q85 > 62:
                                    _lts = 3
                                else:
                                    _lts = 4
                            else:
                                _lts = 'c11'
                    elif lane_p_direction >= 3:
                        if spd_q85 <= 62:
                            _lts = 3
                        else:
                            _lts = 4
                    else:
                        _lts = 'c12'
            else:
                _lts = -8888  # no info on the width of the bikelane type 3

        # Table 1 -- Mixed Traffic
        # street segments with no bikelane (with-flow or contraflow)
        if mixed_traffic == 1:
            # row 1 -- Unlaned 2-way street (no centerline)
            if one_way == 0 and centerline == 0:
                if adt <= 750:
                    if spd_q85 <= 46:
                        _lts = 1
                    elif spd_q85 <= 62:
                        _lts = 2
                    elif spd_q85 > 62:
                        _lts = 3
                    else:
                        _lts = 'c13'
                elif adt <= 1500:
                    if spd_q85 <= 46:
                        _lts = 1
                    elif spd_q85 <= 54:
                        _lts = 2
                    elif spd_q85 <= 70:
                        _lts = 3
                    elif spd_q85 > 70:
                        _lts = 4
                    else:
                        _lts = 'c14'
                elif adt <= 3000:
                    if spd_q85 <= 54:
                        _lts = 2
                    elif spd_q85 <= 62:
                        _lts = 3
                    elif spd_q85 > 62:
                        _lts = 4
                    else:
                        _lts = 'c15'
                elif adt > 3000:
                    if spd_q85 <= 46:
                        _lts = 2
                    elif spd_q85 <= 62:
                        _lts = 3
                    elif spd_q85 > 62:
                        _lts = 4
                    else:
                        _lts = 'c16'
                else:
                    _lts = 'c17'
            # row 2 -- 2-way street with 1+1 lanes and centerline, or one-way street with 1 lane-- for both NBLane = 1
            elif lane_p_direction == 1:
                if one_way in [-1, 1]:  # oneway
                    if adt <= 1000:
                        if spd_q85 <= 46:
                            _lts = 1
                        elif spd_q85 <= 62:
                            _lts = 2
                        elif spd_q85 > 62:
                            _lts = 3
                        else:
                            _lts = 'c18'
                    elif adt <= 1500:
                        if spd_q85 <= 54:
                            _lts = 2
                        elif spd_q85 <= 70:
                            _lts = 3
                        elif spd_q85 > 70:
                            _lts = 4
                        else:
                            _lts = 'c19'
                    elif adt > 1500:
                        if spd_q85 <= 38:
                            _lts = 2
                        elif spd_q85 <= 62:
                            _lts = 3
                        elif spd_q85 > 62:
                            _lts = 4
                    else:
                        _lts = 'c20'
                elif one_way == 0 and centerline == 1:  # two-way 1+ 1 and centerline
                    if adt <= 1000:
                        if spd_q85 <= 46:
                            _lts = 1
                        elif spd_q85 <= 62:
                            _lts = 2
                        elif spd_q85 > 62:
                            _lts = 3
                        else:
                            _lts = 'c21'
                    elif adt <= 1500:
                        if spd_q85 <= 54:
                            _lts = 2
                        elif spd_q85 <= 70:
                            _lts = 3
                        elif spd_q85 > 70:
                            _lts = 4
                        else:
                            _lts = 'c22'
                    elif adt > 1500:
                        if spd_q85 <= 38:
                            _lts = 2
                        elif spd_q85 <= 62:
                            _lts = 3
                        elif spd_q85 > 62:
                            _lts = 4
                        else:
                            _lts = 'c23'
                    else:
                        _lts = 'c24'
                else:
                    _lts = 'c25'
            # row 3 -- 2 thru lanes per direction
            elif lane_p_direction == 2:
                if adt <= 8000:
                    if spd_q85 <= 62:
                        _lts = 3
                    elif spd_q85 > 62:
                        _lts = 4
                    else:
                        _lts = 'c26'
                elif adt > 8000:
                    if spd_q85 <= 46:
                        _lts = 3

                    elif spd_q85 > 46:
                        _lts = 4
                    else:
                        _lts = 'c27'
                else:
                    _lts = 'c28'
            # row 4 -- 3+ thru lanes per direction
            elif lane_p_direction >= 3:
                if spd_q85 <= 46:
                    _lts = 3
                elif spd_q85 > 46:
                    _lts = 4
                else:
                    _lts = 'c29'
            else:
                _lts = -8888

        return _lts
