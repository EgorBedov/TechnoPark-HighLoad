from MyServer import MyServer
from MyConfig import MyConfig

if __name__ == '__main__':
    settings = MyConfig
    settings.port = 80
    settings.host = '127.0.0.1'

    s = MyServer(settings)
    s.run()
