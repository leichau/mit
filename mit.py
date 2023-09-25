import os
import fire, xxhash

from functools import wraps

# 进度条 rich/tpdm

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
        topfile = os.listdir(self.cwd)
        topfile.remove('.mit')
        topfile.remove('.git')
        print(topfile)
        filelist = []
        # for file in topfile:
        #     if os.path.isfile(file):
        #         filelist.append(file)
        #     else:

        for file in topfile:
            path = os.path.join(self.cwd, file)
            os.path.walk(path, self.file_obj, 0)
    
    def ignore(self):
        if not os.path.exists('.mitignore'):
            print('.mitignore is not exist.')
            return

    def fdigest(self, path):
        if not os.path.exists(path):
            path = './mit.py'
        print(path)
        xx = xxhash.xxh128()
        with open(path,'rb' ) as f:
            data = f.read(10240)
            while data:
                xx.update(data)
                data = f.read(10240)
        print(xx.hexdigest())
        return xx.hexdigest()
    
    def file_info(self, path):
        filename = xxhash.xxh128_hexdigest(path)
        if os.path.isfile(path):
            filehash = self.fdigest(path)
        else:
            filehash = filename
        return filename, filehash
    
    def file_obj(self, args, dir, file):
        if os.path.isfile(file):
            filename, filehash = self.file_info(file)
        elif not len(os.listdir(file)):
            filename, filehash = self.file_info(file)
        else:
            return
        filename = os.path.join(self.cwd, '.mit', 'objects', filename)
        with open(filename,'w' ) as f:
            f.write(filehash)

if __name__ == '__main__':
    fire.Fire(Mit)
