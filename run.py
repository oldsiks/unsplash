
from threading import Thread
from LinkCrawl import DownLink
from ImageCrawl import DownImage
import time

def main():

    Thread(target=DownLink().run).start()
    time.sleep(2)
    for i in range(3):
        x = Thread(target=DownImage().run)
        x.start()


if __name__ == '__main__':
    main()