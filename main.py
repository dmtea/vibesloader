"""Script for decoupling audio from video (Sync)"""

import os
import subprocess
from pathlib import Path

import json

from moviepy.editor import AudioFileClip

import yt_dlp


ydl_opts = {
    # 'proxy':"",
    'verbose': False,
    'quiet': True,
    'noprogress': True,
    'no_warnings': True,
    'noplaylist': True,
    'restrictfilenames': True,
    'outtmpl': 'tmp/%(title)s.%(ext)s',
    'format': 'mp3/bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
    }],
    # 'writethumbnail': True,
}


TMPDIR = "tmp"
LOGDIR = "logs"


# TODO: need function for cheching if the link is youtube-service like (check all variants)
def is_youtube_link(url):
    pass


# Takes video filename - separate audio from it - return audio filename
def local_decoupling(video_filename: str):
    # just use video filename name without extension
    audio_filename = f"tmp/{Path(video_filename).stem}.mp3"

    print(audio_filename)

    # decouple audio or send error back
    try:
        audioclip = AudioFileClip(video_filename)
        audioclip.write_audiofile(audio_filename, verbose=False)
    except Exception as ex:
        return False, ex
    return True, audio_filename


# Takes youtube url - download mp3 only - return audio filename (SHELL SUBPROCESS)
def youtube_decoupling_cmd(url):
    # at first take video filename
    # audio_filename = subprocess.call(f"yt-dlp --print filename -o 'tmp/%(title)s.%(ext)s' --restrict-filenames --verbose '{url}'", shell=True)
    _, video_filename = subprocess.getstatusoutput(f"yt-dlp --print filename -o 'tmp/%(title)s.%(ext)s' --restrict-filenames '{url}'")
    audio_filename = f"tmp/{Path(video_filename).stem}.mp3"

    # then (future: try to with try/except?) download the audio
    subprocess.call(
        f'yt-dlp -o "tmp/%(title)s.%(ext)s" --restrict-filenames -q --no-playlist --extract-audio --audio-format mp3 --xattrs --embed-thumbnail --audio-quality 0 --no-warnings "{url}"', shell=True)

    return audio_filename


# Takes youtube url - download mp3 only - return audio filename
def youtube_decoupling(url):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        info = ydl.extract_info(url, download=False)
        # print(f"INFO: {json.dumps(ydl.sanitize_info(info), indent=4)}")
        # with open("tmp/1.json", "w", encoding="utf-8") as fl:
        #     fl.write(json.dumps(ydl.sanitize_info(info), indent=4, ensure_ascii=False))

        video_filename = ydl.prepare_filename(info_dict=info)
        audio_filename = f"tmp/{Path(video_filename).stem}.mp3"

        error_code = ydl.download([url])

        if error_code == 0:
            return True, audio_filename
        else:
            return False, error_code


def prepare_dir():
    """Prepare directories"""

    tmpdir = os.path.abspath(TMPDIR)

    if not os.path.exists(tmpdir):
        print(f"There is no TMP DIRECTORY: {tmpdir}. Making it ...")
        try:
            os.makedirs(tmpdir)
        # except FileExistsError:
        #     # directory already exists
        #     pass
        except:
            print(f"{tmpdir} was created.")

    logdir = os.path.abspath(LOGDIR)

    if not os.path.exists(logdir):
        print(f"There is no LOG DIRECTORY: {logdir}. Making it ...")
        try:
            os.makedirs(logdir)
        # except FileExistsError:
        #     # directory already exists
        #     pass
        except:
            print(f"{logdir} was created.")


def main():
    # filename = local_decoupling(video_filename="tmp/kurpatov.mp4")
    filename = youtube_decoupling(url="https://www.youtube.com/watch?v=Jsyehb6iNlg")

    print(f"FILENAME: {filename}")


if __name__ == "__main__":
    main()
