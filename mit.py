# -*- coding: utf-8 -*-

import os, time
import fire, xxhash, json

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

    # 生成文件摘要
    def file_digest(self, path):
        if not os.path.exists(path):
            path = './mit.py'
        xx = xxhash.xxh128()
        with open(path,'rb' ) as f:
            data = f.read(10240)
            while data:
                xx.update(data)
                data = f.read(10240)
        return xx.hexdigest()

    # 返回文件路径摘要及其内容摘要
    def file_info(self, path):
        objname = xxhash.xxh128_hexdigest(path)
        if os.path.isfile(path):
            # 文件为其内容摘要
            filehash = self.file_digest(path)
        else:
            # 文件夹为其路径摘要
            filehash = objname
        print(path)
        # print(objname, filehash)
        return objname, filehash
    
    # 创建文件对象，记录其内容摘要
    def file_obj(self, file):
        if os.path.isfile(file):
            objname, filehash = self.file_info(file)
        elif not len(os.listdir(file)):
            objname, filehash = self.file_info(file)
        else:
            return
        # 添加路径长度目录，降低哈希碰撞
        # TODO
        objname = os.path.join(self.cwd, '.mit', 'objects', objname)
        msecs = os.path.getmtime(file)
        mtime = time.ctime(os.path.getmtime(file))
        file_info = {}
        file_info['path'] = os.path.relpath(file, self.cwd)
        file_info['secs'] = msecs
        file_info['time'] = mtime
        file_info['hash'] = filehash
        file_json = json.dumps(file_info, indent = 4, ensure_ascii = False)
        with open(objname, 'w') as f:
            f.write(file_json)
            # f.write(filehash)

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
            print(os.path.getctime(item), time.ctime(os.path.getctime(item)))
            print(os.path.getmtime(item), time.ctime(os.path.getmtime(item)))
            print(os.path.getatime(item), time.ctime(os.path.getatime(item)))
    
    @mcheck
    def fresh(self):
        filelist = self.file_list(self.cwd)
        for item in filelist:
            self.file_obj(item)

    # 处理忽略文件
    def ignore(self):
        if not os.path.exists('.mitignore'):
            print('.mitignore is not exist.')
            return
        else:
            print('Ignore to be perfected!')

if __name__ == '__main__':
    '''test command

    1. .\mit.py status

    2. python .\mit.py status
    '''
    fire.Fire(Mit)
