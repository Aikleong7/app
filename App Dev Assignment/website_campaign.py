from uuid import uuid4


class website_camp:

    def __init__(self, campaign_name, start_date, end_date, camp_img):
        self.__campaign_id = str(uuid4())[:8]
        self.__campaign_name = campaign_name
        self.__start_date = start_date
        self.__end_date = end_date
        self.__camp_img = camp_img

    def get_campaign_id(self):
        return self.__campaign_id

    def set_campaign_name(self, campaign_name):
        self.__campaign_name = campaign_name

    def get_campaign_name(self):
        return self.__campaign_name

    def set_start_date(self, start_date):
        self.__start_date = start_date

    def get_start_date(self):
        return self.__start_date

    def set_end_date(self, end_date):
        self.__end_date = end_date

    def get_end_date(self):
        return self.__end_date

    def set_camp_img(self, camp_img):
        self.__camp_img = camp_img

    def get_camp_img(self):
        return self.__camp_img


