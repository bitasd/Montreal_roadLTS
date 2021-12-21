class Mixin:
    def get_attr_by_trc_id(self, trc_id='', _attr=''):
        attr_ret = []
        if _attr == 'num_lanes':
            by_trc_id_subdf = self.data_pieces_dict['geobase_mtl'].loc[
                self.data_pieces_dict['geobase_mtl']['ID_TRC'] == trc_id, ]
            if len(by_trc_id_subdf) > 0:

                num_lanes = by_trc_id_subdf['NBLane'].values[0]
                if num_lanes == 0:
                    num_lanes = 1
            else:
                num_lanes = 1

            attr_ret.append(num_lanes)

            # by_trc_id_subdf = self.data_pieces_dict['aimsun_geobase'].loc[
            #     self.data_pieces_dict['geobase_mtl']['ID_TRC'] == trc_id, ]
            # sort_by_trc_id_subdf = by_trc_id_subdf.sort_values(by='NBLane', ascending=False)
            # if len(sort_by_trc_id_subdf) > 0:
            #     most_lanes_subdf = sort_by_trc_id_subdf.head(n=1)
            #     num_lanes = most_lanes_subdf['NBLane'].values[0]
            #     if num_lanes == 0:
            #         num_lanes = 1
            # else:
            #     num_lanes = 1
            #
            # attr_ret.append(num_lanes)
        elif _attr == 'divided':
            by_trc_id_subdf = self.data_pieces_dict['geobase_mtl'].loc[
                self.data_pieces_dict['geobase_mtl']['ID_TRC'] == trc_id, ]
            if len(by_trc_id_subdf['DIVIDED']) > 0:
                divided = by_trc_id_subdf['DIVIDED'].values[0]
            else:
                divided = 'NOT'
            attr_ret.append(divided)

        elif _attr == 'spd_q85':
            by_trc_id_subdf = self.data_pieces_dict['geobase_mtl'].loc[
                self.data_pieces_dict['geobase_mtl']['ID_TRC'] == trc_id, ]
            if len(by_trc_id_subdf['Q85'].values) > 0:
                spd_q85 = by_trc_id_subdf['Q85'].values[0]
            else:
                spd_q85 = 37
            attr_ret.append(spd_q85)

        elif _attr == 'one_way':
            by_trc_id_subdf = self.data_pieces_dict['geobase_mtl'].loc[
                self.data_pieces_dict['geobase_mtl']['ID_TRC'] == trc_id,]
            if len(by_trc_id_subdf['SENS_CIR'].values) > 0:
                _one_way = by_trc_id_subdf['SENS_CIR'].values[0]
            else:
                _one_way = 0
            attr_ret.append(_one_way)

        elif _attr == 'centerline':
            by_trc_id_subdf = self.data_pieces_dict['geobase_mtl'].loc[
                self.data_pieces_dict['geobase_mtl']['ID_TRC'] == trc_id, ]
            if len(by_trc_id_subdf) > 0:
                _centerline = by_trc_id_subdf['CL_d_2'].values[0]
            else:
                _centerline = -9999
            attr_ret.append(_centerline)

        elif _attr == 'adt':
            by_trc_id_subdf = self.data_pieces_dict['geobase_mtl'].loc[
                self.data_pieces_dict['geobase_mtl']['ID_TRC'] == trc_id,]
            if len(by_trc_id_subdf) > 0:
                _adt = by_trc_id_subdf['DJMA_2src'].values[0]
            else:
                _adt = -9999
            attr_ret.append(_adt)

        elif _attr == 'estmt':
            by_trc_id_subdf = self.data_pieces_dict['geobase_mtl'].loc[
                self.data_pieces_dict['geobase_mtl']['ID_TRC'] == trc_id,]
            if len(by_trc_id_subdf) > 0:
                _estmt = by_trc_id_subdf['Estmt'].values[0]
            else:
                _estmt = -9999
            attr_ret.append(_estmt)

        elif _attr == 'djma_d':
            by_trc_id_subdf = self.data_pieces_dict['geobase_mtl'].loc[
                self.data_pieces_dict['geobase_mtl']['ID_TRC'] == trc_id,]
            if len(by_trc_id_subdf) > 0:
                _djma_d = by_trc_id_subdf['DJMA_d'].values[0]
            else:
                _djma_d = -9999
            attr_ret.append(_djma_d)

        elif _attr == 'cld':
            by_trc_id_subdf = self.data_pieces_dict['geobase_mtl'].loc[
                self.data_pieces_dict['geobase_mtl']['ID_TRC'] == trc_id,]
            if len(by_trc_id_subdf) > 0:
                _cld = by_trc_id_subdf['CL_d'].values[0]
            else:
                _cld = -9999
            attr_ret.append(_cld)

        elif _attr == 'clx':
            by_trc_id_subdf = self.data_pieces_dict['geobase_mtl'].loc[
                self.data_pieces_dict['geobase_mtl']['ID_TRC'] == trc_id,]
            if len(by_trc_id_subdf) > 0:
                _clx = by_trc_id_subdf['CL_x'].values[0]
            else:
                _clx = -9999
            attr_ret.append(_clx)

        elif _attr == 'cyclway_attr':  # TODO: change the format for cycle network, remove lists
            _cyclway_attr_dict = dict()
            _reachs = list()
            _bike_lane_widths = list()
            _type_voies = list()
            _type_voie2s = list()
            _park_ws = list()
            _c_reachs = list()
            _c_bike_lane_widths = list()
            _c_park_ws = list()
            _ed_typvois = list()
            _ed_typvoi2s = list()
            #  the opposite direction -- added to account for the asymmetric roads
            _reach_negDs = list()
            _bike_lane_widths_negDs = list()
            _park_w_negDs = list()
            _asymmetrics = list()
            _gestions = list()
            _id_cycls = list()
            _driveways = list()
            _narrow1ways = list()
            _proteges = list()
            _nbr_voies = list()
            _localisatis = list()
            _localisati2s = list()
            _cnBuff_Rs = list()
            _cnBuff_Ls = list()
            _buff_rs = list()
            _buff_ls = list()

            # ID_TRC_GEO is in the cycle_network (except for type_voie 1, 8)
            by_trc_id_subdf2 = self.data_pieces_dict['cycle_net_2'].loc[
                self.data_pieces_dict['cycle_net_2']['ID_CYCL'] == float(trc_id),]

            # TODO: CHANGE THE COLUMNS' NAME FOR THE POSITIVE DIRECTION.
            if len(by_trc_id_subdf2) > 0:
                _reach2 = by_trc_id_subdf2['Reach'].values[0]
                _reachs.append(_reach2)
                _bike_lane_width2 = by_trc_id_subdf2['BLanW'].values[0]
                _bike_lane_widths.append(_bike_lane_width2)
                _type_voie_2 = by_trc_id_subdf2['TYPE_VOIE'].values[0]
                _type_voies.append(_type_voie_2)
                _type_voie2_2 = by_trc_id_subdf2['TYPE_VOIE2'].values[0]
                _type_voie2s.append(_type_voie2_2)
                _park_w2 = by_trc_id_subdf2['ParkW'].values[0]
                _park_ws.append(_park_w2)
                _c_reach2 = by_trc_id_subdf2['contraReac'].values[0]
                _c_reachs.append(_c_reach2)
                _c_bike_lane_width2 = by_trc_id_subdf2['contraLanW'].values[0]
                _c_bike_lane_widths.append(_c_bike_lane_width2)
                _c_park_w2 = by_trc_id_subdf2['contraParW'].values[0]
                _c_park_ws.append(_c_park_w2)
                _ed_typvoi_2 = by_trc_id_subdf2['ed_typVoi'].values[0]
                _ed_typvois.append(_ed_typvoi_2)
                _ed_typvoi2_2 = by_trc_id_subdf2['ed_typVoi2'].values[0]
                _ed_typvoi2s.append(_ed_typvoi2_2)
                # the negative direction
                _reach_negD_2 = by_trc_id_subdf2['Reach_negD'].values[0]
                _reach_negDs.append(_reach_negD_2)
                _bike_lane_widths_negD_2 = by_trc_id_subdf2['BLanW_negD'].values[0]
                _bike_lane_widths_negDs.append(_bike_lane_widths_negD_2)
                _park_w_negD_2 = by_trc_id_subdf2['ParkW_negD'].values[0]
                _park_w_negDs.append(_park_w_negD_2)
                _asymmetric_2 = by_trc_id_subdf2['asymmetric'].values[0]
                _asymmetrics.append(_asymmetric_2)
                _gestion_2 = by_trc_id_subdf2['GESTION_R'].values[0]
                _gestions.append(_gestion_2)
                _id_cycl_2 = by_trc_id_subdf2['ID_CYCL'].values[0]
                _id_cycls.append(_id_cycl_2)

                _driveway_2 = by_trc_id_subdf2['drvewayVis'].values[0]
                _driveways.append(_driveway_2)
                _narrow1way_2 = by_trc_id_subdf2['Narrow1Way'].values[0]
                _narrow1ways.append(_narrow1way_2)
                _protege_4s_2 = by_trc_id_subdf2['PROTEGE_4S'].values[0]
                _proteges.append(_protege_4s_2)
                _nbr_voie_2 = by_trc_id_subdf2['NBR_VOIE'].values[0]
                _nbr_voies.append(_nbr_voie_2)
                _localisati_2 = by_trc_id_subdf2['LOCALISATI'].values[0]
                _localisatis.append(_localisati_2)
                _localisati2_2 = by_trc_id_subdf2['LOCALIS_2'].values[0]
                _localisati2s.append(_localisati2_2)
                _cnBuff_R_2 = by_trc_id_subdf2['cnBuff_R'].values[0]
                _cnBuff_Rs.append(_cnBuff_R_2)
                _cnBuff_L_2 = by_trc_id_subdf2['cnBuff_L'].values[0]
                _cnBuff_Ls.append(_cnBuff_L_2)
                _buff_r = by_trc_id_subdf2['buffer_R'].values[0]
                _buff_rs.append(_buff_r)
                _buff_l = by_trc_id_subdf2['buffer_L'].values[0]
                _buff_ls.append(_buff_l)

            else:
                pass

            if len(_reachs) > 0:
                _cyclway_attr_dict.update({
                    'Reach': max(_reachs)
                })

                _cyclway_attr_dict.update({
                    'BLanW': max(_bike_lane_widths)
                })
                _cyclway_attr_dict.update({
                    'type_voie': max(_type_voies)
                })
                _cyclway_attr_dict.update({
                    'type_voie2': max(_type_voie2s)
                })
                _cyclway_attr_dict.update({
                    'ParkW': max(_park_ws)
                })
                _cyclway_attr_dict.update({
                    'contraReac': max(_c_reachs)
                })

                _cyclway_attr_dict.update({
                    'contraLanW': max(_c_bike_lane_widths)
                })
                _cyclway_attr_dict.update({
                    'contraParW': max(_c_park_ws)
                })

                _cyclway_attr_dict.update({
                    'Reach_negD': max(_reach_negDs)
                })

                _cyclway_attr_dict.update({
                    'BLanW_negD': max(_bike_lane_widths_negDs)
                })

                _cyclway_attr_dict.update({
                    'ParkW_negD': max(_park_w_negDs)
                })

                _cyclway_attr_dict.update({
                    'asymmetric': max(_asymmetrics)
                })

                _cyclway_attr_dict.update({
                    'gestion_r': max(_gestions)
                })

                _cyclway_attr_dict.update({
                    'ed_typvoi': max(_ed_typvois)
                })

                _cyclway_attr_dict.update({
                    'ed_typvoi2': max(_ed_typvoi2s)
                })

                _cyclway_attr_dict.update({
                    'id_cycl': max(_id_cycls)
                })

                _cyclway_attr_dict.update({
                    'drvewayVis': max(_driveways)
                })

                _cyclway_attr_dict.update({
                    'Narrow1Way': max(_narrow1ways)
                })

                _cyclway_attr_dict.update({
                    'protege_4s': max(_proteges)
                })

                _cyclway_attr_dict.update({
                    'nbr_voie': max(_nbr_voies)
                })

                _cyclway_attr_dict.update({
                    'localisati': max(_localisatis)
                })

                _cyclway_attr_dict.update({
                    'localis2': max(_localisati2s)
                })

                _cyclway_attr_dict.update({
                    'cnBuff_R': max(_cnBuff_Rs)
                })

                _cyclway_attr_dict.update({
                    'cnBuff_L': max(_cnBuff_Ls)
                })

                _cyclway_attr_dict.update({
                    'Buff_R': max(_buff_rs)
                })

                _cyclway_attr_dict.update({
                    'Buff_L': max(_buff_ls)
                })

            attr_ret.append(_cyclway_attr_dict)

        else:
            attr_ret.append('elsed out')
        return attr_ret[0]
