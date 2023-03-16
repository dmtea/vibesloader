# Vibesloader (version 2023.03.16)

Simple telegram bot for separating audio from video. You can use native telegram video, video-notes, video files or youtube link.

It is using https://github.com/yt-dlp/yt-dlp for youtube links downloading function and moviepy pypi-pkg for native telegram video messages.

## installation / prepare (partly description for now)

1. ??? ffmepg install ??? DO WE NEED THIS ??? (#TODO: chek it on server)
2. Use a virtual enviroment for this script (optional)
3. Install python packeges `pip3 install -r requirements.txt`
4. Add TOKEN enviroment variable for Telegram bot
5. FUTURE (TODO for yt-dlp) Add PROXY enviroment variable for youtube "home-ip-safe" downloading (optional)

## start the bot (manual usage)

`python3 bot.py`

## TODO (first):

- [x] make "local" (from telegram msgs) video-msgs decoupling
- [x] make "local" (from telegram msgs) video-circles decoupling
- [x] make "local" (from telegram msgs) video-files decoupling
- [x] **delete all files after sending audio back (or set this in settings what/how to do/be?)**
- [ ] check all modern youtube-links are working (with regexp)
- [ ] Add PROXY support for youtube downloading
- [ ] **make all work with ASYNC functions or in TASK-Manager like celery (+redis for msg transport)**
  - [ ] test with some free proxy?
- ... what next?

### Need new features or want to develop other bot or whatelse?

Write me on telegram [@tatradev](https://t.me/tatradev)

Have a good time ^-.-^
