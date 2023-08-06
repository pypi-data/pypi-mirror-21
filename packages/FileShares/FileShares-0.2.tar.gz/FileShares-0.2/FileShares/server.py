import pickle
import os
from termcolor import cprint, colored
from time import sleep
from socketserver import ThreadingTCPServer, BaseRequestHandler
from struct import unpack, pack
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from collections import Iterable
from functools import partial
from concurrent.futures import ThreadPoolExecutor

from .base import Dir, IO,Encry, FileNotFoundErr
from .config import loger

def send_msg(fp, cmd, data, key=b'what#@!$THeFuck!@$You'):
    if not isinstance(data, bytes):
        data = pickle.dumps(data)
    l = len(data)
    loger.debug(colored("l: %d" % l,'yellow'))
    
    data = bytes(Encry.stream(data, key))
    fp.sendall(cmd + pack('>I', l) + data)


def read_msg(fp, key=b'what#@!$THeFuck!@$You'):
    cmd = fp.recv(1)
    rl, = unpack(">I", fp.recv(4))
    data = fp.recv(rl)
    l = len(data)
    while l < rl:
        loger.debug("read continue: l:%d, rl:%d\r" %(l,rl))
        data += fp.recv(rl-l)
        l = len(data)

    data = bytes(Encry.stream(data, key))
    return cmd, l, data


# handle_maps = {
#     b'r': _read,
#     b'm': _mkdir,
#     # b'l': _list,
# }


class ServerHandler(BaseRequestHandler):
    io = None
    root = os.path.abspath(os.path.curdir)
    key=b'what#@!$THeFuck!@$You'
    tmp_downloads = set()
    tmp_hash = set()

    def handle(self):
        cmd, l, data = read_msg(self.request)
        if cmd == b'f':
            self.save_file(data)
        elif cmd == b'm':
            self.mkdir(data)
        elif cmd == b'l':
            # loger.debug(data[:5])
            if data[:5] == b'check':
                self.list()
                loger.debug(colored("sync check", "yellow"))
                return
            else:
                ha_s = [f for f in pickle.loads(data)]
                files = [self.ready_file(f) for f in ha_s]
                for f in ha_s:
                    print(ServerHandler.io[f])
                # files_ready = []
                # for f in files:
                #     if f not in ServerHandler.tmp_downloads:
                #         files_ready.append(f)
                #         ServerHandler.tmp_downloads.add(f)

                send_msg(self.request, b'z', files)
                loger.debug(colored("sync : ok", "red"))
                # for f in files:
                #     if f in ServerHandler.tmp_downloads:
                #         ServerHandler.tmp_downloads.remove(f)

                # cprint(ServerHandler.tmp_hash, "blue")
                for h in ha_s:
                    if h in ServerHandler.tmp_hash:
                        ServerHandler.tmp_hash.remove(h)
                loger.debug(colored("sync : finished", "red"))

                return

        send_msg(self.request, b'z', b'ok')


#############################################
#### function area ##########################
#############################################

    @staticmethod
    def SRun(ip='', port=20000, key=b'what#@!$THeFuck!@$You', root=None):
        ServerHandler.io = IO()
        ServerHandler.key = key
        if root:
            ServerHandler.root = root

        serv = ThreadingTCPServer(('', 20000), ServerHandler)
        serv.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        serv.serve_forever()

    def mkdir(self, data):
        dirs = pickle.loads(data)
        for d in dirs:
            try:
                os.makedirs(d)
            except FileExistsError:
                pass

    def save_file(self, data):
        head_l, = unpack(">I", data[:4])
        head = pickle.loads(data[4:4 + head_l])
        dirs_path = os.path.dirname(head.path)

        if not os.path.exists(dirs_path):
            os.makedirs(dirs_path)
        loger.debug(head.path)
        with open(os.path.join(".", head.path), 'wb') as fp:
            fp.write(data[4 + head_l:])

    def ready_file(self, file_hash):
        loger.debug(colored("Search: "+ file_hash, 'red'))
        file = ServerHandler.io[file_hash]
        if os.path.exists(file):

            if os.path.isfile(file):
                data = b''
                with open(file, 'rb') as fp:
                    data = fp.read()

                file_path = os.path.abspath(file)
                path = file_path.replace(ServerHandler.root, '.')
                loger.debug("send file's path: %s | root: %s" % (path, ServerHandler.root))
                header = pickle.dumps(Header(os.path.basename(path), path))
                header_l = pack(">I", len(header))
                # return header_l + header + data
                return header_l + header + data
                # return True

        else:
            raise FileExistsError("no such file")

    def list(self):
        try:
            d = Dir(ServerHandler.root, ServerHandler.io) 
        except OSError as e:
            cprint(ServerHandler.io.items, "red")
            raise e
        hash_list = set(d.all())
        c_l = []
        for h in hash_list:
            if h in ServerHandler.tmp_hash:
                c_l.append(h)
            else:
                ServerHandler.tmp_hash.add(h)
        for h in c_l:
            hash_list.remove(h)
        send_msg(self.request, b'z', hash_list)


class Header:

    def __init__(self, name, path):
        self.name = name
        self.path = path


class Client:
    server_info = ('127.0.0.1', 20000)
    root = os.path.abspath(os.path.curdir)
    io = IO()
    key=b'what#@!$THeFuck!@$You'

    def __init__(self, root=None, ip=None, port=None, key=None):
        if ip and port:
            Client.server_info = (ip, port)

        if root:
            if os.path.exists(root):
                Client.root = os.path.abspath(root)

        if key:
            if isinstance(key, bytes):
                Client.key = key
            elif isinstance(key, str):
                Client.key = key.encode('utf8','ignore')

    def send_file(self, file):
        if os.path.exists(file):

            if os.path.isfile(file):
                data = b''
                with open(file, 'rb') as fp:
                    data = fp.read()

                file_path = os.path.abspath(file)
                path = file_path.replace(Client.root, '.')
                header = pickle.dumps(Header(os.path.basename(path), path))
                header_l = pack(">I", len(header))
                # return header_l + header + data
                self.cmd(b'f', header_l + header + data)
                return file

        else:
            raise FileExistsError("no such file")

    def save_file(self, data):
        head_l, = unpack(">I", data[:4])
        head = pickle.loads(data[4:4 + head_l])
        dirs_path = os.path.dirname(head.path)

        if not os.path.exists(dirs_path):
            os.makedirs(dirs_path)
        e = os.path.join(Client.root, head.path)
        cprint("abs : %s" % os.path.abspath(e),"blue")
        with open(e, 'wb') as fp:
            fp.write(data[4 + head_l:])
        cprint("Save done: %s" %  e ,'red')

    def check(self):
        c, rl, res = self.cmd(b'l', b'check')
        
        hash_set = pickle.loads(res)
        d = Dir(Client.root, Client.io)
        hash_set_local = set(d.all())

        need_download_hash = hash_set - hash_set_local
        cprint(need_download_hash, "green")
        c, rl, res = self.cmd(b'l', need_download_hash)
        loger.debug("need got: %d , got: %d" %(rl, len(res)))
        files = pickle.loads(res)
        c = 0
        loger.debug("ready to save %d " % len(files))
        for f in files:
            self.save_file(f)
            c += 1
            

    def cmd(self, cmd, data):
        key = Client.key
        D = cmd
        
        if isinstance(data, bytes):
            l = len(data)
            D += pack('>I', l)
            data = bytes(Encry.stream(data, key))
            D += data
        else:
            data = pickle.dumps(data)
            data = bytes(Encry.stream(data, key))
            l = len(data)
            D += pack('>I', l)
            D += data
        
        try:
            s = socket(AF_INET, SOCK_STREAM)
            s.connect(Client.server_info)
            s.send(D)
            cmd = s.recv(1)
            rl, = unpack('>I', s.recv(4))
            res = s.recv(rl)
            l = len(res)
            while l < rl:
                loger.debug(colored("read continue: l: %d , rl: %d" %(l, rl) ,'magenta'))
                res += s.recv(rl-l)
                l = len(res)

            res = bytes(Encry.stream(res, key))
            return cmd, rl, res
        except OSError as e:
            loger.error(e)
        finally:
            s.close()



class Monitor:

    def __init__(self, root, inter = 3, workers=6, key=None,ip=None, port=None):
        if not os.path.isdir(root):
            raise FileNotFoundErr("no such dir found :" + root)

        self.root = root
        self.io = IO()
        self.exe = ThreadPoolExecutor(workers)
        self.client = Client(root=root)
        self.tmp_upload = set()
        self.inter = inter

    def done(self, future):
        url = future.result()
        if url in self.tmp_upload:
            self.tmp_upload.remove(url)
        self.old_d = set(Dir(self.root, self.io).all())

    def check_uploads(self, old_d):
        
        d = set(Dir(self.root, self.io).all())
        new_s =  d - old_d
        loger.debug(colored("upload : %d" % len(new_s), "green"))
        for f in new_s:
            file = self.io[f]
            if os.path.exists(file) and file not in self.tmp_upload:
                fm  = self.exe.submit(self.client.send_file, file)
                fm.add_done_callback(self.done)
                self.tmp_upload.add(file)
            
    def run(self):
        self.old_d = set(Dir(self.root, self.io).all())
        while 1:
            try:
                
                self.check_uploads(self.old_d)
                self.client.check()
                    
            except Exception as e:
                loger.error(e)
            sleep(self.inter)

