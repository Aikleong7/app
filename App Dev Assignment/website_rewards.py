from uuid import uuid4


class website_rwds:

    def __init__(self, rank, web_reward_type, web_reward_name, amt_rewarded, points, start_date, end_date, reward_description):
        self.__count = str(uuid4())[:8]
        self.__rank = rank
        self.__web_reward_type = web_reward_type
        self.__web_reward_name = web_reward_name
        self.__amt_rewarded = amt_rewarded
        self.__points = points
        self.__start_date = start_date
        self.__end_date = end_date
        self.__reward_description = reward_description

    def get_count(self):
        return self.__count

    def set_rank(self, rank):
        self.__rank = rank

    def get_rank(self):
        return self.__rank

    def set_web_reward_type(self, web_reward_type):
        self.__web_reward_type = web_reward_type

    def get_web_reward_type(self):
        return self.__web_reward_type

    def set_reward_name(self, web_reward_name):
        self.__web_reward_name = web_reward_name

    def get_web_reward_name(self):
        return self.__web_reward_name

    def set_amt_rewarded(self, amt_rewarded):
        self.__amt_rewarded = amt_rewarded

    def get_amt_rewarded(self):
        return self.__amt_rewarded

    def set_points(self, points):
        self.__points = points

    def get_points(self):
        return self.__points

    def set_start_date(self, start_date):
        self.__start_date = start_date

    def get_start_date(self):
        return self.__start_date

    def set_end_date(self, end_date):
        self.__end_date = end_date

    def get_end_date(self):
        return self.__end_date

    def set_reward_description(self, reward_description):
        self.__reward_description = reward_description

    def get_reward_description(self):
        return self.__reward_description
