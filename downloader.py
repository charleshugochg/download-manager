from threading import Thread, RLock

import requests

lock = RLock()


class DownloadManager:
    def __init__(self, url):
        self.url = url
        self._downloads = []

    @property
    def size(self):
        with requests.get(self.url, stream=True) as r:
            size = r.headers['content-length']
        return int(size)

    def create_downloads(self, num_downloads):
        total_size = self.size
        download_size = total_size // num_downloads
        for i in range(num_downloads - 1):
            d = Download(self.url, i * download_size, (i + 1) * download_size)
            self._downloads.append(d)
        i = num_downloads - 1
        self._downloads.append(Download(self.url, i * download_size, total_size))

    def iter_downloads(self):
        for download in self._downloads:
            yield download


class Download(Thread):
    def __init__(self, url, start, end):
        Thread.__init__(self)
        self.params = set()
        self.url = url
        self._start = start
        self._end = end
        self._pointer = start
        self.on_chunk = lambda *a: None

        self.setDaemon(True)

    @property
    def length(self):
        return self._end - self._start

    def bind(self, on_chunk, *params):
        self.on_chunk = on_chunk
        self.params = params

    def start_index(self):
        return self._start

    def run(self) -> None:
        headers = {'Range': 'bytes=%d-%d' % (self._start, self._end)}

        # request the specified part and get into variable
        with requests.get(self.url, headers=headers, stream=True) as r:
            r.raise_for_status()
            for chunk in r.iter_content(chunk_size=131072):
                if chunk:
                    lock.acquire()
                    self.on_chunk(self._pointer, chunk, self.params)
                    self._pointer += len(chunk)
                    lock.release()

def parse_filename(url):
    return url.split('/')[-1].split('?')[0]
