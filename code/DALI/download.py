from . import utilities as ut
import os
import yt_dlp

base_url = 'http://www.youtube.com/watch?v='


class MyLogger(object):
    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


def get_my_ydl(directory=os.path.dirname(os.path.abspath(__file__)), cookiefile=None, cookies=None, cookiesfrombrowser=None, http_headers=None):
    ydl = None
    outtmpl = None
    if ut.check_directory(directory):
        outtmpl = os.path.join(directory, '%(title)s.%(ext)s')
        ydl_opts = {'format': 'bestaudio/best',
                    'postprocessors': [{'key': 'FFmpegExtractAudio',
                                        'preferredcodec': 'mp3',
                                        'preferredquality': '320'}],
                    'outtmpl': outtmpl,
                    'logger': MyLogger(),
                    'progress_hooks': [my_hook],
                    'verbose': False,
                    'ignoreerrors': False,
                    'external_downloader': 'ffmpeg',
                    'nocheckcertificate': True}
        if cookiefile:
            ydl_opts['cookiefile'] = cookiefile
        if cookiesfrombrowser:
            ydl_opts['cookiesfrombrowser'] = cookiesfrombrowser
        if http_headers:
            ydl_opts['http_headers'] = http_headers
        elif cookies:
            ydl_opts['http_headers'] = {'Cookie': cookies}
                    # 'external_downloader_args': "-j 8 -s 8 -x 8 -k 5M"}
                    # 'maxBuffer': 'Infinity'}
                    #  it uses multiple connections for speed up the downloading
                    #  'external-downloader': 'ffmpeg'}
        ydl = yt_dlp.YoutubeDL(ydl_opts)
        ydl.cache.remove()
        import time
        time.sleep(.5)
    return ydl


def audio_from_url(url, name, path_output, errors=[], cookiefile=None, cookies=None, cookiesfrombrowser=None, http_headers=None):
    """
    Download audio from a url.
        url : str
            url of the video (after watch?v= in youtube)
        name : str
            used to store the data
        path_output : str
            path for storing the data
    """
    error = None

    # ydl(yt-dlp.YoutubeDL): extractor
    ydl = get_my_ydl(path_output, cookiefile=cookiefile, cookies=cookies, cookiesfrombrowser=cookiesfrombrowser, http_headers=http_headers)

    tmpl = ydl.params.get('outtmpl')
    target_ext = ydl.params['postprocessors'][0].get('preferredcodec', 'mp3')
    if isinstance(tmpl, dict):
        base = tmpl.get('default') or tmpl.get('outtmpl') or '%(title)s.%(ext)s'
        ydl.params['outtmpl']['default'] = base % {'ext': target_ext, 'title': name}
    else:
        ydl.params['outtmpl'] = tmpl % {'ext': target_ext, 'title': name}

    if ydl:
        print ("Downloading " + url)
        try:
            ydl.download([base_url + url])
        except Exception as e:
            print(e)
            error = e
    if error:
        errors.append([name, url, error])
    return
