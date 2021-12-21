import AttributeGetter
import DataPiece
import categorized_calc_lts
import re


class AllofLtsCalcs(
    DataPiece.Mixin,
    AttributeGetter.Mixin,
    categorized_calc_lts.LTSCalc
):
    def __init__(self):

        self.data_pieces_dict = dict()
        self.row_data = list()

    def run_lts(self, id_trc, id_cycl, classe, length, spd_q85, lane_p_direction, one_way, adt, centerline,
                estmt, djma_d, cld, clx, cyclway_attr, divided):

        self.row_data = []
        self.row_data.append(
            {
                "id_trc": id_trc,
                "id_cycl": id_cycl,
                "classe": classe,
                "spd_q85": spd_q85,
                "lane_p_direction": lane_p_direction,
                "one_way": one_way,
                "adt": adt,
                "centerline": centerline,
                "estmt": estmt,
                "djma_d": djma_d,
                "cld": cld,
                "clx": clx,
                "cyclway_attr": cyclway_attr,
                "_centerline": None,  # to handle oneway lts with contraflow
                "_one_way": None,  # to handle oneway lts with contraflow
                "divided": divided

            }
        )
        # print(self.row_data)
        lts_negD = -9999

        if self.row_data[0]['classe'] in [1, 2, 3, 4]:  # no access for bikes and not a freeway
            lts, lts_c, lts_w, lts_c_w = 5, 5, 5, 5

        elif self.row_data[0]['classe'] == 8:  # freeway or freeway ramp
            lts, lts_c, lts_w, lts_c_w = 6, 6, 6, 6

        else:  # accessible by bikes
            # if length < 50:  # short links
            #     lts, lts_c, lts_w, lts_c_w, lts_negD = 0, 0, 0, 0, 0

            if ('gestion_r' in self.row_data[0]['cyclway_attr']) and \
                    (self.row_data[0]['cyclway_attr']['gestion_r'] in [11, 12]):
                lts = self.path()
                lts_c = -9999
                lts_c_w = -9999
                if ('protege_4s' in self.row_data[0]['cyclway_attr']) and \
                        (self.row_data[0]['cyclway_attr']['protege_4s'] != 'OUI'):
                    lts_w = 5
                else:
                    lts_w = lts

            elif ('gestion_r' in self.row_data[0]['cyclway_attr']) and \
                    (self.row_data[0]['cyclway_attr']['gestion_r'] == 6):  # in the intersection LTS
                lts = -9999
                lts_w = -9999
                lts_c = -9999
                lts_c_w = -9999

            else:

                # NO BIKE INFRASTRUCTURE -- mixed traffic
                if len(self.row_data[0]['cyclway_attr'].keys()) == 0 or (
                        ('type_voie' in self.row_data[0]['cyclway_attr'])
                        and (self.row_data[0]['cyclway_attr']['type_voie'] in [0, 1, 8, -9999])):
                    # LTS in default direction
                    lts = self.mixed_traffic('one_way', 'centerline', 'divided')
                    lts_w = lts
                    lts_c = -9999
                    lts_c_w = -9999

                # BIKE INFRASTRUCTURE withflow and/or contraflow
                elif len(self.row_data[0]['cyclway_attr'].keys()) > 0:
                    if self.row_data[0]['cyclway_attr']['type_voie'] in [3]:

                        # contraflow bikelane and no with-flow bikelane (happens on oneway streets)
                        if self.row_data[0]['cyclway_attr']['type_voie2'] in [30, 31] or \
                                self.row_data[0]['cyclway_attr']['ed_typvoi2'] in (
                                31, 30):  # TODO change only if edited>0
                            self.row_data[0]['_centerline'] = 0
                            self.row_data[0]['_one_way'] = 0
                            lts = self.mixed_traffic('one_way', 'centerline', 'divided')
                            print("lts is", lts)
                            lts_w = lts
                            lts_c = self.on_street_bikelane('contraReac', 'contraLanW', 'contraParW')
                            if self.row_data[0]['cyclway_attr']['protege_4s'] != 'OUI':
                                lts_c_w = self.mixed_traffic('_one_way', '_centerline', 'divided')
                            else:
                                lts_c_w = lts_c

                        # contraflow + w/flow bikelanes(happens only on oneway streets except for 4 cases;
                        elif self.row_data[0]['cyclway_attr']['type_voie2'] == 33 or \
                                self.row_data[0]['cyclway_attr']['ed_typvoi2'] == 33:
                            self.row_data[0]['_centerline'] = 0
                            self.row_data[0]['_one_way'] = 0
                            lts = self.on_street_bikelane('Reach', 'BLanW', 'ParkW')
                            lts_c = self.on_street_bikelane('contraReac', 'contraLanW', 'contraParW')

                            if self.row_data[0]['cyclway_attr']['protege_4s'] != 'OUI':
                                lts_w = self.mixed_traffic('one_way', 'centerline', 'divided')
                                lts_c_w = self.mixed_traffic('_one_way', '_centerline', 'divided')
                            else:
                                lts_w = lts
                                lts_c_w = lts_c

                        # bike lane IN THE DEFAULT DIRECTION type_voie2 in [0,13,35,39]
                        else:
                            # type 3, two way and one cycle lane -- asymmetric twoway
                            if self.row_data[0]['cyclway_attr']['nbr_voie'] == 1 and \
                                    self.row_data[0]['one_way'] == 0:
                                lts = -8321  # TODO: change with regard to LOCALISATI
                                lts_c = -9999
                                lts_c_w = -9999
                                lts_negD = -8321
                                if self.row_data[0]['cyclway_attr']['protege_4s'] != 'OUI':
                                    lts_w = self.mixed_traffic('one_way', 'centerline', 'divided')
                                else:
                                    lts_w = lts

                            else:
                                lts = self.on_street_bikelane('Reach', 'BLanW', 'ParkW')
                                lts_c = -9999
                                lts_c_w = -9999
                                if self.row_data[0]['cyclway_attr']['protege_4s'] != 'OUI':
                                    lts_w = self.mixed_traffic('one_way', 'centerline', 'divided')
                                else:
                                    lts_w = lts
                            # asymmetric
                            if re.search('yes', str(self.row_data[0]['cyclway_attr']['asymmetric']),
                                         re.IGNORECASE):
                                if self.row_data[0]['cyclway_attr']['BLanW_negD'] > 0:
                                    lts_negD = self.on_street_bikelane('Reach_negD', 'BLanW_negD', 'ParkW_negD')
                                else:
                                    lts_negD = self.mixed_traffic('one_way', 'centerline', 'divided')

                    # Shared Bus - Bike route
                    elif self.row_data[0]['cyclway_attr']['type_voie'] in [9]:
                        lts = self.on_street_bikelane('Reach', 'BLanW', 'ParkW', 4.8)
                        lts_w = lts  # I assumed they always plow the bus-bike lane
                        lts_c = -9999
                        lts_c_w = -9999

                    # protected track
                    elif self.row_data[0]['cyclway_attr']['type_voie'] in [4]:
                        # Oneway track
                        if self.row_data[0]['cyclway_attr']['type_voie2'] in [40] or \
                                self.row_data[0]['cyclway_attr']['ed_typvoi2'] in [40]:

                            # one cycle lane
                            if self.row_data[0]['cyclway_attr']['nbr_voie'] == 1:
                                if self.row_data[0]['one_way'] == 0:  # twoway street - asymmetric
                                    lts = -8440  # TODO: change with regard to LOCALISATI
                                    lts_c = -9999
                                    lts_negD = -8440
                                elif self.row_data[0]['one_way'] in [-1, 1]:  # oneway street
                                    lts = self.path()
                                    lts_c = -9999

                            # two cycle lanes
                            if self.row_data[0]['cyclway_attr']['nbr_voie'] == 2:
                                if self.row_data[0]['one_way'] == 0:  # twoway street - symmetric
                                    lts = self.path()
                                    lts_c = -9999
                                elif self.row_data[0]['one_way'] in [-1,
                                                                     1]:  # oneway street, biketracks on two sides of the road
                                    lts = self.path()
                                    lts_c = self.path()

                        # one protected lane contraflow (happens on oneway streets)
                        elif self.row_data[0]['cyclway_attr']['type_voie2'] in [41] or \
                                self.row_data[0]['cyclway_attr']['ed_typvoi2'] in [41]:
                            lts = self.mixed_traffic('one_way', 'centerline', 'divided')
                            lts_c = self.path()

                        # one protected lane contraflow, bike lane with-flow (happens on oneway streets)
                        elif self.row_data[0]['cyclway_attr']['type_voie2'] in [43] or \
                                self.row_data[0]['cyclway_attr']['ed_typvoi2'] in [43]:
                            lts = self.path()
                            lts_c = self.path()

                        # bidirectional track
                        elif self.row_data[0]['cyclway_attr']['type_voie2'] in [44] or \
                                self.row_data[0]['cyclway_attr']['ed_typvoi2'] in [44]:
                            lts = self.path()
                            lts_c = self.path()

                        # type_voie = 4, type_voi2 = 0
                        elif self.row_data[0]['cyclway_attr']['type_voie2'] in [0]:
                            # one cycle lane
                            if self.row_data[0]['cyclway_attr']['nbr_voie'] == 1:
                                if self.row_data[0]['one_way'] == 0:  # twoway street - asymmetric
                                    lts = -8401  # TODO: change with regard to LOCALISATI
                                    lts_c = -9999
                                    lts_negD = -8401
                                else:  # oneway street
                                    lts = self.path()
                                    lts_c = -9999

                            # two cycle lanes
                            if self.row_data[0]['cyclway_attr']['nbr_voie'] == 2:
                                if self.row_data[0]['one_way'] == 0:  # twoway street - symmetric
                                    lts = self.path()
                                    lts_c = -9999
                                else:  # oneway street, biketracks on two sides of the road
                                    lts = self.path()
                                    lts_c = self.path()

                        # winter
                        if self.row_data[0]['cyclway_attr']['protege_4s'] != 'OUI':
                            lts_w = self.mixed_traffic('one_way', 'centerline', 'divided')
                            lts_c_w = self.mixed_traffic('one_way', 'centerline', 'divided')
                        else:
                            lts_w = lts
                            lts_c_w = lts_c

                    # path
                    elif self.row_data[0]['cyclway_attr']['type_voie'] in [5, 6, 7]:  # path
                        lts = self.path()
                        lts_c = -9999
                        lts_c_w = -9999
                        if self.row_data[0]['cyclway_attr']['protege_4s'] != 'OUI':
                            lts_w = 5
                        else:
                            lts_w = lts

                    # anything else
                    else:
                        lts, lts_c, lts_w, lts_c_w = -5040, -5040, -5040, -5040
                else:
                    lts, lts_c, lts_w, lts_c_w = -6040, -6040, -6040, -6040

        if abs(lts_w) < abs(lts): lts = lts_w
        if abs(lts_c_w) < abs(lts_c): lts_c = lts_c_w
        self.row_data[0]['lts'] = lts
        self.row_data[0]['lts_c'] = lts_c
        self.row_data[0]['lts_w'] = lts_w
        self.row_data[0]['lts_c_w'] = lts_c_w
        self.row_data[0]['lts_negD'] = lts_negD

        return self.row_data[0]
