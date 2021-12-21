class LTSCalc:

    # Table 1 -- Mixed Traffic
    # street segments with no bikelane (with-flow or contraflow)
    def mixed_traffic(self, oneway, cntreline, divided):
        if divided == 'DIVIDED':  # dual carriageway
            adt_ = self.row_data[0]['adt'] * 2
        else:
            adt_ = self.row_data[0]['adt']

        # row 1 -- Unlaned 2-way street (no centerline)
        if self.row_data[0][oneway] == 0 and self.row_data[0][cntreline] == 0:
            if adt_ <= 750:
                if self.row_data[0]['spd_q85'] <= 46:
                    _lts = 1
                elif self.row_data[0]['spd_q85'] <= 62:
                    _lts = 2
                elif self.row_data[0]['spd_q85'] > 62:
                    _lts = 3
                else:
                    _lts = 'c13'
            elif adt_ <= 1500:
                if self.row_data[0]['spd_q85'] <= 46:
                    _lts = 1
                elif self.row_data[0]['spd_q85'] <= 54:
                    _lts = 2
                elif self.row_data[0]['spd_q85'] <= 70:
                    _lts = 3
                elif self.row_data[0]['spd_q85'] > 70:
                    _lts = 4
                else:
                    _lts = 'c14'
            elif adt_ <= 3000:
                if self.row_data[0]['spd_q85'] <= 54:
                    _lts = 2
                elif self.row_data[0]['spd_q85'] <= 62:
                    _lts = 3
                elif self.row_data[0]['spd_q85'] > 62:
                    _lts = 4
                else:
                    _lts = 'c15'
            elif adt_ > 3000:
                if self.row_data[0]['spd_q85'] <= 46:
                    _lts = 2
                elif self.row_data[0]['spd_q85'] <= 62:
                    _lts = 3
                elif self.row_data[0]['spd_q85'] > 62:
                    _lts = 4
                else:
                    _lts = 'c16'
            else:
                _lts = 'c17'
        # row 2 -- 2-way street with 1+1 lanes and centerline, or one-way street with 1 lane-- for both NBLane = 1
        elif self.row_data[0]['lane_p_direction'] == 1:
            if self.row_data[0][oneway] in [-1, 1]:  # oneway
                if adt_ <= 1000:
                    if self.row_data[0]['spd_q85'] <= 46:
                        _lts = 1
                    elif self.row_data[0]['spd_q85'] <= 62:
                        _lts = 2
                    elif self.row_data[0]['spd_q85'] > 62:
                        _lts = 3
                    else:
                        _lts = 'c18'
                elif adt_ <= 1500:
                    if self.row_data[0]['spd_q85'] <= 54:
                        _lts = 2
                    elif self.row_data[0]['spd_q85'] <= 70:
                        _lts = 3
                    elif self.row_data[0]['spd_q85'] > 70:
                        _lts = 4
                    else:
                        _lts = 'c19'
                elif adt_ > 1500:
                    if self.row_data[0]['spd_q85'] <= 38:
                        _lts = 2
                    elif self.row_data[0]['spd_q85'] <= 62:
                        _lts = 3
                    elif self.row_data[0]['spd_q85'] > 62:
                        _lts = 4
                else:
                    _lts = 'c20'
            elif self.row_data[0][oneway] == 0 and self.row_data[0][cntreline] == 1:  # two-way 1+ 1 and centerline
                # present
                if adt_ <= 1000:
                    if self.row_data[0]['spd_q85'] <= 46:
                        _lts = 1
                    elif self.row_data[0]['spd_q85'] <= 62:
                        _lts = 2
                    elif self.row_data[0]['spd_q85'] > 62:
                        _lts = 3
                    else:
                        _lts = 'c21'
                elif adt_ <= 1500:
                    if self.row_data[0]['spd_q85'] <= 54:
                        _lts = 2
                    elif self.row_data[0]['spd_q85'] <= 70:
                        _lts = 3
                    elif self.row_data[0]['spd_q85'] > 70:
                        _lts = 4
                    else:
                        _lts = 'c22'
                elif adt_ > 1500:
                    if self.row_data[0]['spd_q85'] <= 38:
                        _lts = 2
                    elif self.row_data[0]['spd_q85'] <= 62:
                        _lts = 3
                    elif self.row_data[0]['spd_q85'] > 62:
                        _lts = 4
                    else:
                        _lts = 'c23'
                else:
                    _lts = 'c24'
            else:
                _lts = -8825
        # row 3 -- 2 thru lanes per direction
        elif self.row_data[0]['lane_p_direction'] == 2:
            if adt_ <= 8000:
                if self.row_data[0]['spd_q85'] <= 62:
                    _lts = 3
                elif self.row_data[0]['spd_q85'] > 62:
                    _lts = 4
                else:
                    _lts = 'c26'
            elif adt_ > 8000:
                if self.row_data[0]['spd_q85'] <= 46:
                    _lts = 3

                elif self.row_data[0]['spd_q85'] > 46:
                    _lts = 4
                else:
                    _lts = 'c27'
            else:
                _lts = 'c28'
        # row 4 -- 3+ thru lanes per direction
        elif self.row_data[0]['lane_p_direction'] >= 3:
            if self.row_data[0]['spd_q85'] <= 46:
                _lts = 3
            elif self.row_data[0]['spd_q85'] > 46:
                _lts = 4
            else:
                _lts = 'c29'
        else:
            _lts = 'c30'

        return _lts

    def on_street_bikelane(self, reach, blane, plane, bus_blane=0):

        # assigning LTS to on_street bikelanes
        _lts = 2000  # TODO: fix this

        if float(self.row_data[0]['cyclway_attr'][blane]) > 0 or bus_blane > 0:

            # TABLE 3 -- adjacent to a parking lane
            if (plane in self.row_data[0]['cyclway_attr'].keys()) and (
                    float(self.row_data[0]['cyclway_attr'][plane]) > 0):
                if self.row_data[0]['lane_p_direction'] == 1:

                    if float(self.row_data[0]['cyclway_attr'][reach]) >= 4.45:
                        if float(self.row_data[0]['spd_q85']) <= 46:
                            _lts = 1
                        elif float(self.row_data[0]['spd_q85']) <= 62:
                            _lts = 2
                        elif float(self.row_data[0]['spd_q85']) > 62:
                            _lts = 3
                        else:
                            _lts = 'c1'
                    elif 4.4 >= float(self.row_data[0]['cyclway_attr'][reach]) >= 3.5:
                        if self.row_data[0]['spd_q85'] <= 54:
                            _lts = 2
                        elif self.row_data[0]['spd_q85'] <= 62:
                            _lts = 3
                        elif self.row_data[0]['spd_q85'] > 62:
                            _lts = 3
                        else:
                            _lts = 'c2'
                    else:
                        _lts = 'c3'
                elif self.row_data[0]['lane_p_direction'] == 2 and self.row_data[0]['one_way'] == 0:
                    if float(self.row_data[0]['cyclway_attr'][reach]) >= 4.45:
                        if self.row_data[0]['spd_q85'] <= 46:
                            _lts = 2
                        elif self.row_data[0]['spd_q85'] <= 54:
                            _lts = 3
                        elif self.row_data[0]['spd_q85'] <= 62:
                            _lts = 3
                        elif self.row_data[0]['spd_q85'] > 62:
                            _lts = 3
                        else:
                            _lts = 'c4'
                    else:
                        _lts = 3  # any other multilane
                elif (self.row_data[0]['lane_p_direction'] in [2, 3]) and (self.row_data[0]['one_way'] in [-1, 1]):
                    if float(self.row_data[0]['cyclway_attr'][reach]) >= 4.45:
                        if self.row_data[0]['spd_q85'] <= 46:
                            _lts = 2
                        else:
                            _lts = 3
                    elif float(self.row_data[0]['cyclway_attr'][reach]) < 4.45:
                        _lts = 3
                    else:
                        _lts = 3
                elif self.row_data[0]['lane_p_direction'] > 1:  # any other multilane
                    _lts = 3
                else:
                    _lts = 'c7'

            # TABLE 2  -- not next to a parking space
            elif (plane in self.row_data[0]['cyclway_attr'].keys()) and (
                    float(self.row_data[0]['cyclway_attr'][plane]) == 0):

                if self.row_data[0]['lane_p_direction'] == 1 or self.row_data[0]['centerline'] == 0:
                    if reach in self.row_data[0]['cyclway_attr'].keys():
                        if float(self.row_data[0]['cyclway_attr'][reach]) >= 1.8:
                            if self.row_data[0]['spd_q85'] <= 54:
                                _lts = 1
                            elif 62 >= self.row_data[0]['spd_q85'] > 54:
                                _lts = 2
                            elif self.row_data[0]['spd_q85'] > 62:
                                _lts = 3
                            else:
                                _lts = 'c8'
                        elif float(self.row_data[0]['cyclway_attr'][reach]) < 1.8:
                            if self.row_data[0]['spd_q85'] <= 62:
                                _lts = 2
                            elif 78 >= self.row_data[0]['spd_q85'] > 62:
                                _lts = 3
                            else:
                                _lts = 4
                        else:
                            _lts = 'c9'
                    else:
                        _lts = 'c10'
                elif self.row_data[0]['lane_p_direction'] == 2:
                    if reach in self.row_data[0]['cyclway_attr'].keys():
                        if float(self.row_data[0]['cyclway_attr'][reach]) >= 1.8:
                            if self.row_data[0]['spd_q85'] <= 62:
                                _lts = 2
                            else:
                                _lts = 3
                        elif float(self.row_data[0]['cyclway_attr'][reach]) < 1.8:
                            if self.row_data[0]['spd_q85'] <= 62:
                                _lts = 2
                            elif 70 >= self.row_data[0]['spd_q85'] > 62:
                                _lts = 3
                            else:
                                _lts = 4
                        else:
                            _lts = 'c11'
                elif self.row_data[0]['lane_p_direction'] >= 3:
                    if self.row_data[0]['spd_q85'] <= 62:
                        _lts = 3
                    else:
                        _lts = 4
                else:
                    _lts = 'c12'

            else:
                _lts = 'idk'
        else:
            _lts = -8888  # no info on the width of the bikelane type 3

        return _lts

    def path(self):
        if self.row_data[0]['cyclway_attr']['drvewayVis'] == 0:
            _lts = 1
        else:
            _lts = 2
        return _lts
