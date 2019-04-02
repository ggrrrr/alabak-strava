import logging

class StravaDto:
    def __init__(self, stravaMap = None, sqlMap = None):
        self.stravaData = None
        self.stravaMap = stravaMap
        if stravaMap is not None:
            self.loadStravaMap()

    def loadSqlMap(self, data):
        if data is None:
            return
        if k in ['id']:
            v = data[k]
            self.__dict__[toKey]= v

    def loadStravaMap(self):
        for k in self.map:
            if k in self.stravaMap:
                toKey = self.map[k]
                v = self.stravaMap[k]
                if type(toKey) is str:
                    self.LOG.debug("%s.loadStravaMap: %s %s %s" %(self.__class__.__name__, k, toKey,v))
                    # print("loadMap: name:%s, value:%s" % (toKey, v))
                    self.__dict__[toKey]= v
                else:
                    f = toKey['method']
                    c = toKey['class']
                    mapName = toKey['name']
                    f(mapName, c, v)
            else:
                self.LOG.debug("%s.loadStravaMap: %s NOT FOUND" %(self.__class__.__name__, k))

    def loadList(self, name, className, jsonData,):
        self.LOG.debug("%s loadList: name: %s class(%s) %s " %(self.__class__.__name__,name, type(className),type(jsonData)))
        for l in jsonData:
            self.__dict__[name].append(className(jsonData=l))

class Segment(StravaDto):
    def __init__(self, jsonData = None):
        self.LOG = logging.getLogger('alabak.strava.Segment')
        self.map = {
                'id': 'strava_segment_id'
                ,'name': 'strava_segment_name'
                ,'activity_type': 'strava_sport'
                ,'distance': 'strava_distance'
                ,'average_grade': 'strava_average_grade'
                ,'effort_count': 'strava_effort_count'
                # ,'start_latlng': 'start_latlng'
                # ,'end_latlng': 'strava_end_latlng'
                # ,'climb_category': 'strava_climb_category'
            }
        StravaDto.__init__(self, jsonData)

    def __repr__(self):
        return "Segment: id: %s, name: %s, activity_type: %s, average_grade: %s\n" % ( 
            self.strava_segment_id
            , self.strava_segment_name
            , self.strava_activity_type
            , self.strava_average_grade
            )

class SegmentLeaderboard(StravaDto):
    def __init__(self, strava_segment_id = None, jsonData = None):
        self.LOG = logging.getLogger('alabak.strava.SegmentLeaderboard')
        self.entries = list()
        self.id = None
        self.segment_name = None
        self.alabak_track_id = None
        self.strava_segment_id = strava_segment_id
        self.map = {
                'entry_count':'strava_entry_count'
                ,'effort_count':'strava_effort_count'
                ,'kom_type':'strava_kom_type'
                ,'name':'strava_segment_name'
                ,'entries':{
                    'method':self.loadList
                    , 'class':SegmentLeaderboardEntry
                    , 'name':'entries'
                    }
            }
        StravaDto.__init__(self, jsonData)

    def setPK(self, id):
        self.id = id

    def getPK(self):
        return self.id

    def setAlabakTrackId(self, id):
        self.alabak_track_id = id

    def __repr__(self):
        return "SegmentLeaderboard: entrys: id: %s/%s, kom: %s, entry: %s, effort: %s, entries: %s\n" % ( 
                self.strava_segment_id
                , self.strava_segment_name
                , self.strava_kom_type
                , self.strava_entry_count
                , self.strava_effort_count
                , self.entriesJson()
                )
    
    def entriesJson(self):
        out = ""
        jsonsList = (e.json() for e in self.entries)
        out = ",".join(jsonsList)
        # return "[%s]" % (  )
        return "[%s]" % out

class SegmentLeaderboardEntry(StravaDto):
    def __init__(self, strava_leaderboard_id = None, strava_segment_id = None, jsonData = None):
        self.LOG = logging.getLogger('alabak.strava.SegmentLeaderboardEntry.init')
        self.strava_leaderboard_id = strava_leaderboard_id
        self.strava_segment_id = strava_segment_id
        self.map = {
                # 'athlete_id':'athlete_id'
                # ,'athlete_photo':'athlete_photo'
                'athlete_name':'strava_athlete_name'
                ,'elapsed_time':'strava_elapsed_time'
                # ,'moving_time':'strava_moving_time'
                ,'start_date':'strava_start_date'
                # ,'start_date_local':'strava_start_date_local'
                ,'rank':'strava_rank'
            }
        StravaDto.__init__(self, jsonData)
    
    def setPK(self, id):
        self.id = id

    def setFK(self, id):
        self.strava_leaderboard_id = id

    def __repr__(self):
        return "SegmentLeaderboardEntry: %s, rank: %s, name: %s, time: %s\n" % ( 
            self.strava_segment_id
            , self.strava_rank
            , self.strava_athlete_name
            , self.strava_elapsed_time
            )

    def json(self):
        return """{"rank":"%s","name":"%s","time":"%s"}""" % ( 
            self.strava_rank
            , self.strava_athlete_name
            , self.strava_elapsed_time
            )

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    leaderboardData = {'effort_count': 121, 'entry_count': 121, 'kom_type': 'kom', 'entries': [{'athlete_name': 'Zlatislav I.', 'elapsed_time': 186, 'moving_time': 186, 'start_date': '2018-04-09T10:41:05Z', 'start_date_local': '2018-04-09T13:41:05Z', 'rank': 1}, {'athlete_name': 'Румен Д.', 'elapsed_time': 279, 'moving_time': 225, 'start_date': '2018-08-19T15:09:25Z', 'start_date_local': '2018-08-19T18:09:25Z', 'rank': 2}, {'athlete_name': 'Vihren M.', 'elapsed_time': 300, 'moving_time': 300, 'start_date': '2017-07-18T17:29:30Z', 'start_date_local': '2017-07-18T20:29:30Z', 'rank': 3}, {'athlete_name': 'Alexander M.', 'elapsed_time': 327, 'moving_time': 327, 'start_date': '2017-12-30T11:11:53Z', 'start_date_local': '2017-12-30T13:11:53Z', 'rank': 4}, {'athlete_name': 'Martin D.', 'elapsed_time': 341, 'moving_time': 341, 'start_date': '2018-04-09T12:03:04Z', 'start_date_local': '2018-04-09T15:03:04Z', 'rank': 5}, {'athlete_name': 'Georgi N.', 'elapsed_time': 351, 'moving_time': 351, 'start_date': '2018-05-16T11:02:27Z', 'start_date_local': '2018-05-16T14:02:27Z', 'rank': 6}, {'athlete_name': 'Vladislav G.', 'elapsed_time': 361, 'moving_time': 361, 'start_date': '2016-08-14T11:51:11Z', 'start_date_local': '2016-08-14T14:51:11Z', 'rank': 7}, {'athlete_name': 'Boyko T.', 'elapsed_time': 361, 'moving_time': 361, 'start_date': '2017-08-27T10:24:51Z', 'start_date_local': '2017-08-27T13:24:51Z', 'rank': 7}, {'athlete_name': 'Vladimir M.', 'elapsed_time': 393, 'moving_time': 393, 'start_date': '2018-09-02T14:46:24Z', 'start_date_local': '2018-09-02T17:46:24Z', 'rank': 9}, {'athlete_name': 'Dimitar P.', 'elapsed_time': 395, 'moving_time': 395, 'start_date': '2018-06-03T10:10:09Z', 'start_date_local': '2018-06-03T13:10:09Z', 'rank': 10}, {'athlete_name': 'Angel B.', 'elapsed_time': 687, 'moving_time': 609, 'start_date': '2018-07-01T09:06:42Z', 'start_date_local': '2018-07-01T12:06:42Z', 'rank': 4}, {'athlete_name': 'Aleksandar P.', 'elapsed_time': 699, 'moving_time': 635, 'start_date': '2018-08-21T17:24:47Z', 'start_date_local': '2018-08-21T20:24:47Z', 'rank': 5}, {'athlete_name': 'Varban K.', 'elapsed_time': 703, 'moving_time': 703, 'start_date': '2013-07-28T11:40:31Z', 'start_date_local': '2013-07-28T14:40:31Z', 'rank': 6}, {'athlete_name': 'Stoyan C.', 'elapsed_time': 705, 'moving_time': 705, 'start_date': '2017-07-08T10:46:36Z', 'start_date_local': '2017-07-08T13:46:36Z', 'rank': 7}, {'athlete_name': 'Dinko D.', 'elapsed_time': 713, 'moving_time': 664, 'start_date': '2016-06-04T15:03:07Z', 'start_date_local': '2016-06-04T18:03:07Z', 'rank': 8}]}
    segment = {'id': 4920835, 'resource_state': 3, 'name': 'Segment', 'activity_type': 'Ride', 'distance': 1677.9, 'average_grade': 10.9, 'maximum_grade': 50.0, 'elevation_high': 934.8, 'elevation_low': 751.4, 'start_latlng': [42.546149, 23.160795], 'end_latlng': [42.55877, 23.159511], 'start_latitude': 42.546149, 'start_longitude': 23.160795, 'end_latitude': 42.55877, 'end_longitude': 23.159511, 'climb_category': 2, 'city': 'Kladnitsa', 'state': 'Pernik', 'country': 'Bulgaria', 'private': False, 'hazardous': False, 'starred': False, 'created_at': '2013-07-29T22:17:03Z', 'updated_at': '2019-02-25T09:18:36Z', 'total_elevation_gain': 183.4, 'map': {'id': 's4920835', 'polyline': 'kxtbG}qjlCKFSDKCG@U^MZQT_@~@GF_@hAYn@IFi@Ng@AiAJyCR_AJg@?SCiA_@uA]iACqARgEnAk@L_Ct@w@Lu@C}@e@a@g@_@{@k@uCW[SMo@Yg@Mk@Gu@?Y@kAJcAG_AB}Bl@_Br@s@VaAVEBM@MFOBg@BBFDCECGJFC?EGDHC@IIPJI?EGHLCKEQA', 'resource_state': 3}, 'effort_count': 167, 'athlete_count': 121, 'star_count': 0, 'athlete_segment_stats': {'pr_elapsed_time': 703, 'pr_date': '2013-07-28', 'effort_count': 1}}
    # asd1 = Segment(jsonData = segment)
    leaderboard = SegmentLeaderboard(strava_segment_id = 4920835, stravaMap = leaderboardData)
    # print( ";\n".join( SegmentLeaderboard.dropSql() ) )
    # print( ";\n".join( SegmentLeaderboard.createSql() ) )

    print( ";\n".join( SegmentLeaderboardEntry.dropSql() ) )
    print( ";\n".join( SegmentLeaderboardEntry.createSql() ) )
        
    # print("", asd1.__class__.__name__, asd1.__dict__)
    # print("", asd2.__class__.__name__, asd1.__dict__)
    # print("", asd3.__class__.__name__, asd1.__dict__)

