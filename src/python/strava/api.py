# tests
import argparse
import logging
import requests
from datetime import datetime

class StravaApi():
    def __init__(self, args=None
                , accessToken=None
                , clientId=None
                , clientSecret=None
                , refreshToken=None):
        if args is not None:
            self.parseArgs(args)
        if accessToken is not None:
            self.accessToken = accessToken
        if clientId is not None:
            self.clientId = clientId
        if clientSecret is not None:
            self.clientSecret = clientSecret
        if refreshToken is not None:
            self.refreshToken = refreshToken

        self.log = logging.getLogger('alabak.strava')
        self.baseUrl = "https://www.strava.com"
        self.apiUrl = "/api/v3"
        self.refreshAuthUrl = "/oauth/token"
        self.segmentsUrl = "/segments/%s"
        self.leaderboardUrl = "/segments/%s/leaderboard"
        self.segmentsEffortsUrl = "/segments/%s/all_efforts"
        self.segmentsStreamsUrl = "/segments/%s/streams"

    def parseArgs(self, args):
        """
        Parse params from args
        """
        self.accessToken = args.accessToken
        self.clientId = args.clientId
        self.clientSecret = args.clientSecret
        self.refreshToken = args.refreshToken

    def callLeaderboard(self, id):
        """
        Make call to strava LeaderBoard for segment id=id
        """
        data = None
        if self.accessToken is None:
            raise NameError("accessToken is none")
        # self.log.info("refreshToken:%s" % inline)
        path = self.leaderboardUrl % id
        url = "%s%s%s" % ( self.baseUrl,self.apiUrl, path)
        self.log.info("callLeaderboard:url:%s" % url)
        headers = {'Authorization': "Bearer %s" % self.accessToken}
        try:
            response = requests.get(url, headers=headers)
            if ( response.status_code == 200):
                data = response.json()
                self.log.debug("callLeaderboard:response:%s" % data)
                return data 
            else:
                self.log.error("callLeaderboard:response:%s:%s" % (response.status_code, response.text ) )
                if response.status_code == 404:
                    raise Exception("strava.return.error.segment not found:%s" % (id ) ) 
                raise Exception("strava.return.error:%s:%s" % (response.status_code, response.text ) ) 
        
        except Exception as e:
            self.log.error("%s, %s" % (type(e).__name__, e.args ) )
            error = "%s" % (type(e).__name__ )
            raise e

    def callSegment(self, id):
        """
        Make call to strava Segment for id
        """
        data = None
        if self.accessToken is None:
            raise NameError("accessToken is none")
        # self.log.info("refreshToken:%s" % inline)
        path = self.segmentsUrl % id
        url = "%s%s%s" % ( self.baseUrl,self.apiUrl, path)
        self.log.info("getSegment123123:url:%s" % url)
        headers = {'Authorization': "Bearer %s" % self.accessToken}
        try:
            response = requests.get(url, headers=headers)
            if ( response.status_code == 200):
                data = response.json()
                self.log.debug("callSegment:response:%s" % data)
                return data
            else:
                self.log.error("callSegment:response:%s:%s" % (response.status_code, response.text ) )
                if response.status_code == 404:
                    raise Exception("strava.return.error.callLeaderboard  not found::%s" % (id ) ) 
                raise Exception("strava.return.error:%s:%s" % (response.status_code, response.text ) ) 

        except Exception as e:
            self.log.error("%s, %s" % (type(e).__name__, e.args ) )
            error = "%s" % (type(e).__name__ )
            raise e

    def callRefreshToken(self):
        """
        Make call to refresh token = /oauth/token
        """
        data = None
        if self.clientId is None:
            raise NameError("clientId is none")
        if self.clientSecret is None:
            raise NameError("clientSecret is none")
        if self.refreshToken is None:
            raise NameError("refreshToken is none")

        inline = "client_id=%s&client_secret=%s&grant_type=%s&refresh_token=%s" % (
            self.clientId
            , self.clientSecret
            , 'refresh_token'
            , self.refreshToken
        )
        # self.log.info("refreshToken:%s" % inline)

        url = "%s%s?%s" % ( self.baseUrl, self.refreshAuthUrl, inline)
        self.log.info("callRefreshToken:%s" % url)

        try:
            response = requests.post(url, headers=None, json=None)
            if ( response.status_code == 200):
                data = response.json()
                token_type = data['token_type']
                self.accessToken = data['access_token']
                self.expiresAt = datetime.utcfromtimestamp(int(data['expires_at']))
                self.expiresIn = round(int(data['expires_in'])/60)
                refresh_token = data['refresh_token']

                self.log.info("callRefreshToken:expiresAt:%s, accessToken:%s" % ( 
                    self.expiresAt
                    , self.accessToken
                    , ) )
                self.log.debug("callRefreshToken:body:%s" % data)
            else:
                self.log.error("callRefreshToken:%s:%s" % (response.status_code, response.text ) )
                if response.status_code == 404:
                    raise Exception("strava.return.error.segment not found::%s" % (id ) ) 
                raise Exception("strava.return.error:%s:%s" % (response.status_code, response.text ) ) 
        except Exception as e:
            self.log.error("%s, %s" % (type(e).__name__, e.args ) )
            error = "%s" % (type(e).__name__ )
            raise e
        return True

    def callSegmentsEfforts(self, id):
        """
        Make call to strava Segment efforts for segment id
        """
        data = None
        if self.accessToken is None:
            raise NameError("accessToken is none")
        # self.log.info("refreshToken:%s" % inline)
        path = self.segmentsEffortsUrl % id
        url = "%s%s%s" % ( self.baseUrl,self.apiUrl, path)
        self.log.info("callSegmentsEfforts:url:%s" % url)
        headers = {'Authorization': "Bearer %s" % self.accessToken}
        try:
            response = requests.get(url, headers=headers)
            if ( response.status_code == 200):
                print("-------")
                print(response.text)
                print("-------")
                data = response.json()
                self.log.debug("callSegmentsEfforts:response:%s" % data)
                return data
            else:
                self.log.error("callSegmentsEfforts:response:%s:%s" % (response.status_code, response.text ) )
                if response.status_code == 404:
                    raise Exception("strava.return.error.callSegmentsEfforts not found::%s" % (id ) ) 
                raise Exception("strava.return.error:%s:%s" % (response.status_code, response.text ) ) 

        except Exception as e:
            self.log.error("%s, %s" % (type(e).__name__, e.args ) )
            error = "%s" % (type(e).__name__ )
            raise e


def call(args):
    if args.call is None:
        logging.error("call not set")
        return
    strava = StravaApi(args)
    if args.call == "refresh":
        strava.callRefreshToken()
        print(strava.accessToken)
        return 
    if args.call == "segment":
        print( strava.callSegment('4920835'))
        return 
    if args.call == "leaderboard":
        id = 4920835
        if args.id is not None:

            id = args.id
        data = strava.callLeaderboard(id)
        from objects import SegmentLeaderboard
        leaderboard = SegmentLeaderboard(strava_segment_id = id, jsonData = data)
        print(leaderboard)
        return 
    if args.call == "efforts":
        id = 4920835
        if args.id is not None:
            id = args.id
        data = strava.callSegmentsEfforts(id)
        # from objects import SegmentLeaderboard
        # leaderboard = SegmentLeaderboard(strava_segment_id = id, jsonData = data)

        # print(data)
        print(data[0])
        return 

    logging.error("call:%s not known" % args.call)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='alabak.strava API CLI.')
    parser.add_argument('--clientId', default=None, dest='clientId', help='pg Db')
    parser.add_argument('--clientSecret', default=None, dest='clientSecret', help='pg user')
    parser.add_argument('--grantType', default='refresh_token', dest='grantType', help='pg password')
    parser.add_argument('--refreshToken', default=None, dest='refreshToken', help='pg host')
    parser.add_argument('--accessToken', default=None, dest='accessToken', help='accessToken')
    parser.add_argument('--call', default=None, dest='call', help='call refresh')
    parser.add_argument('--level', default='debug', dest='level', help='level')
    parser.add_argument('--id', default=None, dest='id', help='id of shit', required = False)

    args = parser.parse_args()

    if args.level == "debug":
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    
    logging.info("args: %s" % args )
    call(args)

