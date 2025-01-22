class logger:
    # define logger levels
    levels = ['debug', 'info', 'error']

    # define level colors for output
    DEBUG = '\033[93m'
    ERROR = '\033[91m'
    INFO = '\033[97m'

    def __init__(self, level):
        try:
            f = self.levels[int(level)]
            self.level = level
            print(f'[LOGGER]: Logger initialized to {f.upper()}')
        except Exception as e:
            print(e)
            print(self.ERROR+'Invalid level entered. Allowed levels: 0 (debug), 1 (info), 2 (error)')
            exit(1)

    # printing debug msgs
    def debug(self, msg):
        if self.level == 0:
            print(self.DEBUG+f'[DEBUG ]: {msg}')

    # printing info msgs
    def info(self, msg):
        if self.level <= 1:
            print(self.INFO+f'[INFO  ]: {msg}')

    # printing error msgs
    def error(self, msg):
        print(self.ERROR+f'[ERROR ]: {msg}')