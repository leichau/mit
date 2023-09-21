import os
import fire

from functools import wraps

class Mit:
    def __init__(self):
        self.cwd = os.getcwd()

    def mcheck(func):
        @wraps(func)
        def decorator(self, *args, **kwargs):
            if not os.path.exists('.mit'):
                print('fatal: not a mit repository: .mit')
                return
            func(self, *args, **kwargs)
        return decorator

    @mcheck
    def status(self):
        walkList = [file for file in os.walk(self.cwd)]
        for walk in walkList:
            fileList = os.listdir(walk[0])
        print('mit status')
    
    def ignore(self):
        if not os.path.exists('.mitignore'):
            print('.mitignore is not exist.')
            return

if __name__ == '__main__':
    fire.Fire(Mit)
