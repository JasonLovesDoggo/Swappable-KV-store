import time


class DatabaseStats:
    def __init__(self):
        """
        initiates the stats module and sets the start time
     """
        self.__start_time = time.time()

    def uptime_info(self) -> dict:
        """
        returns total uptime of the connection to the database
        :return: a dict that has uptime info in multiple formats
        """

        now = time.time() - self.__start_time  # total time in seconds
        days, hours, minutes, seconds = int(now // 86400), int(now // 3600 % 24), int(now // 60 % 60), int(now % 60)
        uptime_readable = {'days': days, 'hours': hours, 'minutes': minutes, 'seconds': seconds}

        return {'total_seconds': int(now), 'readable': uptime_readable}
