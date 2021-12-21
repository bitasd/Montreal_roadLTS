import pandas


class Mixin:
    def get_data_piece(self):
        cycle_net_0 = pandas.read_csv('C:\\Users\\bitas\\folders\\Research\\Montreal\\Analysis\\LTS\\cycleNetwork_Nov9.csv',
                                      usecols=['Reach', 'BLanW', 'TYPE_VOIE', 'TYPE_VOIE2', 'ParkW', 'contraReac',
                                               'contraLanW', 'contraParW', 'ed_typVoi', 'ed_typVoi2', 'Reach_negD',
                                               'BLanW_negD', 'ParkW_negD', 'asymmetric', 'GESTION_R', 'ID_CYCL',
                                               'drvewayVis', 'Narrow1Way', 'PROTEGE_4S', 'NBR_VOIE', 'cnBuff_R',
                                               'cnBuff_L', 'LOCALISATI', 'LOCALIS_2', 'buffer_L', 'buffer_R'],

                                      dtype={'ID_TRC': int, 'ID_CYCL': int, 'TYPE_VOIE': int, 'TYPE_VOIE2': int})
                                      # nrows=10000)

        # to exclude mixed traffic cases.
        cycle_net_0 = cycle_net_0.reset_index()
        cycle_net_0['mixedtrfc_id'] = cycle_net_0.index
        cycle_mix_trfc = cycle_net_0.loc[
            cycle_net_0['TYPE_VOIE'].isin([1, 8])]
        cycle_net_bline = cycle_net_0[~ cycle_net_0['mixedtrfc_id'].isin(cycle_mix_trfc['mixedtrfc_id'])]

        # self.data_pieces_dict.update(
        #     {
        #         'aimsun_geobase': pandas.read_csv(
        #             'C:\\Users\\bitas\\folders\\Research\\Montreal\\Analysis\\aimsun_geobase.csv')  ## 71612 rows
        #     })

        self.data_pieces_dict.update(
            {
                'geobase_mtl': pandas.read_csv('C:\\Users\\bitas\\folders\\Research\\Montreal\\Analysis\\LTS'
                                               '\\Geobase_Dec17.csv',
                                               usecols=['ID_TRC', 'CLASSE', 'SENS_CIR', 'CL_d_2', 'DJMA_2src', 'Q85',
                                                        'Estmt', 'DJMA_d', 'CL_d', 'CL_x', 'DIVIDED', 'NBLane'],
                                               dtype={'ID_TRC': int, 'CLASSE': int, 'SENS_CIR': int,
                                                      'CL_d_2': int, 'DJMA_2src': float, 'Q85': float,
                                                      'DJMA_d': float, 'CL_d': int, 'CL_x': int,
                                                      'Estmt': float, 'NBLane': int, 'DIVIDED': str}
                                               )
            })

        self.data_pieces_dict.update(
            {
                'cycle_net_2': cycle_net_bline
            })
