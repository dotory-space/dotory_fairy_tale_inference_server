from src.app import App
import sys

if __name__=="__main__":
    if len(sys.argv) == 4:
        debug = sys.argv[1]
        host = sys.argv[2]
        port = sys.argv[3]

        print('---------------------------------')
        print('START - Dotory Inference Server')
        print('host: ', host)
        print('port: ', port)
        print('debug: ', debug)
        print('---------------------------------')

        app = App()
        app.run(host, port=port, debug=(debug == 'True'))