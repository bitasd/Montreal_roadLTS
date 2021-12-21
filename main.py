import pandas
import allofltscalcs


class DataAgent(

    allofltscalcs.AllofLtsCalcs
):
    def run(self):
        # INPUT FILE FOR UMBRELLA
        # TODO: CHANGE THIS DIRECTORY TO PASS THE UMBRELLA LAYER
        base_df = pandas.read_csv('C:\\Users\\bitas\\folders\\Research\\Montreal\\Analysis\\LTS\\umbrella_Dec17.csv',
                                  usecols=['umbrell_id', 'ID_TRC', 'ID_CYCL', 'CLASSE', 'slope', 'slope_edit',
                                           'length'],
                                  # nrows=1000,
                                  ).fillna(0)
        coltype = {'umbrell_id': int, 'ID_TRC': int, 'ID_CYCL': int, 'CLASSE': int, 'slope': float,
                   'slope_edit': float,
                   'length': float}
        base_df = base_df.astype(coltype)

        base_df['result_object'] = base_df.apply(lambda row:
                                                 self.run_lts(
                                                     id_trc=row['ID_TRC'],

                                                     id_cycl=row['ID_CYCL'],

                                                     classe=row['CLASSE'],

                                                     length=row['length'],

                                                     spd_q85=self.get_attr_by_trc_id(trc_id=row['ID_TRC'],
                                                                                     _attr='spd_q85'),
                                                     lane_p_direction=self.get_attr_by_trc_id(trc_id=row['ID_TRC'],
                                                                                              _attr='num_lanes'),
                                                     one_way=self.get_attr_by_trc_id(trc_id=row['ID_TRC'],
                                                                                     _attr='one_way'),
                                                     adt=self.get_attr_by_trc_id(trc_id=row['ID_TRC'], _attr='adt'),

                                                     centerline=self.get_attr_by_trc_id(trc_id=row['ID_TRC'],
                                                                                        _attr='centerline'),

                                                     estmt=self.get_attr_by_trc_id(trc_id=row['ID_TRC'],
                                                                                   _attr='estmt'),

                                                     djma_d=self.get_attr_by_trc_id(trc_id=row['ID_TRC'],
                                                                                    _attr='djma_d'),

                                                     cld=self.get_attr_by_trc_id(trc_id=row['ID_TRC'],
                                                                                 _attr='cld'),

                                                     clx=self.get_attr_by_trc_id(trc_id=row['ID_TRC'],
                                                                                 _attr='clx'),

                                                     cyclway_attr=self.get_attr_by_trc_id(trc_id=row['ID_CYCL'],
                                                                                          _attr='cyclway_attr'),

                                                     divided=self.get_attr_by_trc_id(trc_id=row['ID_CYCL'],
                                                                                     _attr='divided')
                                                 ),
                                                 axis=1
                                                 )
        base_df[['ID_TRC', 'ID_CYCL', 'CLASSE', 'Q85', 'NBLane', 'SENS_CIR', 'ADT', 'centerline', 'Estmt', 'DJMA_d',
                 'CL_d', 'CL_x', 'cyclway_attr', '_centerline', '_one_way', 'DIVIDED', 'lts', 'lts_c', 'lts_w',
                 'lts_c_w',
                 'lts_negD']] = base_df[
            'result_object'].apply(pandas.Series)

        base_df[['Reach', 'BLanW', 'TYPE_VOIE', 'TYPE_VOIE2', 'ParkW', 'contraReac', 'contraLanW',
                 'contraParW', 'Reach_negD', 'BLanW_negD', 'ParkW_negD', 'asymmetric', 'GESTION_R',
                 'ed_typvoi', 'ed_typvoi2', 'id_cycl', 'drvewayVis', 'Narrow1Way', 'PROTEGE_4S', 'NBR_VOIE',
                 'LOCALISATI', 'LOCALIS_2', 'cn_Buff_R', 'cn_Buff_L', 'Buffer_R', 'Buffer_L']] = \
            base_df['cyclway_attr'].apply(pandas.Series)
        return base_df


da = DataAgent()
da.get_data_piece()
lts_df = da.run()
# RESULT FILE
# TODO: CHANGE THIS DIRECTORY SAVE THE RESULT LAYER
lts_df.to_csv('C:\\Users\\bitas\\folders\\Research\\Montreal\\Analysis\\LTS\\8_newdata.csv')
# umbrella_gdf = geopandas.read_file(
#     'C:\\Users\\bitas\\folders\\Research\\Montreal\\QGIS_projects\\nov9\\RuesEtSentiers.gpkg',
#     usecols=['umbrell_id', 'slope_edit', 'length'],
#     dtype={'umbrell_id': int, 'slope_edit': float, 'length': float}
# )
#
# res_gdf = umbrella_gdf.merge(lts_df, on='umbrell_id')
# res_gdf = res_gdf.set_crs(2950, allow_override=True)  # or 32188?
# res_gdf.to_file('C:\\Users\\bitas\\folders\\Research\\Montreal\\QGIS_projects\\nov9\\seg_lts.gpkg', layer="lts_1",
#                 driver='GPKG')
# # TODO: TEST LOADING THE GEOPANADAS WITH GEOMETRY IN THE FIRST PLACE
