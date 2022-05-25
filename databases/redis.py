from databases.Base import DatabaseStats


class Redis(DatabaseStats):
    def __init__(self, config):
        super().__init__()
        self.config = config


