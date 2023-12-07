import os
import fire, xxhash

from functools import wraps

# 进度条 rich/tpdm

class Mit:
    def __init__(self):
        # 获取当前目录
        self.cwd = os.getcwd()

    # 执行命令前先做必要的检查
    def mcheck(func):
        @wraps(func)
        def decorator(self, *args, **kwargs):
            if not os.path.exists('.mit'):
                print('fatal: not a mit repository: .mit')
                return
            func(self, *args, **kwargs)
        return decorator

    def init(self):
        files = os.listdir(self.cwd)
        if '.mit' in files:
            path = os.path.join(self.cwd, '.mit')
            print('Reinitialized existing Mit repository in', path)
            return
        else:
            os.mkdir('.mit')
            os.mkdir('.mit\objects')
        
        filelist = self.file_list(self.cwd)
        for item in filelist:
            self.file_obj(item)

    @mcheck
    def status(self):
        filelist = self.file_list(self.cwd)
        for item in filelist:
            print(item)
    
    # 处理忽略文件
    def ignore(self):
        if not os.path.exists('.mitignore'):
            print('.mitignore is not exist.')
            return
        else:
            print('Ignore to be perfected!')

    # 生成文件摘要
    def fdigest(self, path):
        if not os.path.exists(path):
            path = './mit.py'
        xx = xxhash.xxh128()
        with open(path,'rb' ) as f:
            data = f.read(10240)
            while data:
                xx.update(data)
                data = f.read(10240)
        return xx.hexdigest()
    
    def file_list(self, path):
        topfile = os.listdir(path)
        # 移除不需要的目录
        topfile.remove('.mit')
        topfile.remove('.git')

        filelist = []
        for file in topfile:
            path = os.path.join(self.cwd, file)
            filelist.append(path)
            if os.path.isdir(path):
                for root, dirs, files in os.walk(path, topdown=True):
                    for name in files:
                        filelist.append(os.path.join(root, name))
                    for name in dirs:
                        filelist.append(os.path.join(root, name))
        return filelist

    # 返回文件路径摘要及其内容摘要
    def file_info(self, path):
        filename = xxhash.xxh128_hexdigest(path)
        if os.path.isfile(path):
            # 文件为其内容摘要
            filehash = self.fdigest(path)
        else:
            # 文件夹为其路径摘要
            filehash = filename
        print(path)
        print(filename, filehash)
        return filename, filehash
    
    # 创建文件对象，记录其内容摘要
    def file_obj(self, file):
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
    '''test command

    1. .\mit.py status

    2. python .\mit.py status
    '''
    fire.Fire(Mit)
