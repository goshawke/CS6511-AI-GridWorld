import requests


class Requests:

    def __init__(self):
        # Costants
        self.BASE_GW_URL = "https://www.notexponential.com/aip2pgaming/api/rl/gw.php"
        self.BASE_SCORE_URL = "https://www.notexponential.com/aip2pgaming/api/rl/score.php"
        self.TEAMID = "1387"
        self.USERID = "1201"
        self.API_KEY = '05049c9e31fc51cdb173'
        
        # change depending of what computer is running this code
        self.USER_AGENT = '\'User-Agent\': \'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36\''

    # end of __init__()

    # POST METHODS
    
    '''
    enter_world()
        @params: 
            String worldId
    '''
    def enter_world(self, worldId):
        payload = {'type': 'enter',
                   'worldId': worldId,
                   'teamId': self.TEAMID}
        files = []
        headers = {
            'userId': self.USERID,
            'x-api-key': self.API_KEY,
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': self.USER_AGENT
        }

        response = requests.request(
            "POST", self.BASE_GW_URL, headers=headers, data=payload, files=files)

        print(response.text)
        # {"code":"FAIL","message":"Cannot enter the world.  You are currently in world: 0"}
    # end of enter_world()

    ''' 
    make_move()
        @params: 
            String worldId
            String move = {'N','S','E','W'} 
    '''
    def make_move(self, worldId, move):
        payload = {'type': 'move',
                   'teamId': self.TEAMID,
                   'move': move,
                   'worldId': worldId}
        files = []
        headers = {
            'userId': self.USERID,
            'x-api-key': self.API_KEY,
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': self.USER_AGENT
        }
        response = requests.request(
            "POST", self.BASE_GW_URL, headers=headers, data=payload, files=files)

        print(response.text)
        # {"code":"OK","worldId":0,"runId":"44748","reward":-0.10,"scoreIncrement":-0,"newState":{"x":"0","y":10}}
    # end of make_move()
    

    # GET METHODS

    '''
    get_location()
        @params: N/A
        @return: String in format "#:#"
    '''
    def get_location(self):
        
        url = self.BASE_GW_URL + '?type=location&teamId=' + self.TEAMID
        headers = {
            'userId': self.USERID,
            'x-api-key': self.API_KEY,
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': self.USER_AGENT
            }

        response = requests.request("GET", url, headers=headers)

        print(response.text)
        # Ex. {"code":"OK","world":"0","state":"0:11"}     
    # end of get_location()
    
    '''
    get_learning_score()
        @params: N/A
        @return: String score
    '''
    def get_learning_score(self):
        url = "https://www.notexponential.com/aip2pgaming/api/rl/score.php?type=score&teamId=" + self.TEAMID
        headers = {
            'userId': self.USERID,
            'x-api-key': self.API_KEY,
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': self.USER_AGENT
            }
        response = requests.request("GET", url, headers=headers)

        print(response.text)
        # Ex. {"score":0,"code":"OK"}
    # end of get_learning_score()
    
    '''
    get_last_x_runs()
        @params: 
            String count = number of previous runs to retrieve
        @returns:
            List of Runs in format: 
    '''
    def get_last_x_runs(self, count):
        url = "https://www.notexponential.com/aip2pgaming/api/rl/score.php?type=runs&teamId="+ self.TEAMID+ "&count=" + count
        headers = {
            'userId': self.USERID,
            'x-api-key': self.API_KEY,
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': self.USER_AGENT
            }
        response = requests.request("GET", url, headers=headers)

        print(response.text)
        # Ex. {"runs":[{"runId":"44748","teamId":"1387","gworldId":"0","createTs":"2023-04-22 17:26:52","score":"-0.9998955043236689","moves":"87"}],"code":"OK"}
    # end of get_last_x_runs()
        
    def reset_agent(self):
        url = "https://www.notexponential.com/aip2pgaming/api/rl/reset.php?teamId=" + self.TEAMID + "&otp=5712768807"

        headers = {
            'userId': self.USERID,
            'x-api-key': self.API_KEY,
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': self.USER_AGENT
            }
        response = requests.request("GET", url, headers=headers)

        print(response.text)
        # Ex. {"code":"OK","teamId":1387}
        
    # end of reset_agent()


# main() used for testing
def main():
    req = Requests()

    # START - POST METHOD TESTING
    
    # Entering a World
    #req.enter_world("0")
    
    # Making a Move
    #req.make_move("0", "N")
    
    # END - POST METHOD TESTING
    
    # GET METHOD TESTING
    
    # Locating the agent
    #req.get_location()
    
    # Getting the learning score
    # req.get_learning_score()
    
    # Getting the last x runs
    # req.get_last_x_runs('1')
    
    # resetting the agent
    # req.reset_agent()
    

# end of main()


if __name__ == "__main__":
    main()
