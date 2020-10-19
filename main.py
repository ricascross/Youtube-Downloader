from flask import Flask, render_template, redirect, flash, request, Response, send_file
import ffmpeg
import subprocess
import os
import validators
from pytube import YouTube
from download import YoutubeDownloader
import time

# Configure Application
app = Flask(__name__)

# secret key generated
app.secret_key = b'#\xbb$\x87W\x8f\x0c\x83\x0b\x13I\xd00\xa9\xde\xff'

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

#resolve status code == 429;;
if Response.status_code == 429:
    time.sleep(429)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/mp4Downloader", methods=["GET", "POST"])
def mp4Downloader():
    if request.method == "POST":
        url = request.form.get("url")

        # if url is not valid then return an error
        # and redirects to same page
        if not validators.url(url):
            flash("URL Not Valid")
            return render_template("mp4Downloader.html")
        
        # we have a YouTube object called yt
        yt = YouTube(url)

        # we have a youtubeDownloader object called download
        download = YoutubeDownloader(yt)

        # get title from a method designed in class YoutubeDownloader
        title = download.get_title()

        # and reassign with ".mp4" extension
        title2 = title + ".mp4"

        #aux video and audio
        audio = download.get_audio()
        video = download.get_video()


        #getting file extension
        extension_without_dot = video.partition(".")[2]
        extension = "." + extension_without_dot
        
        #ffmpeg.output(audio_stream, video_stream, title2).run()

        subprocess.run(["ffmpeg", "-i", "video.webm", "-i", "audio.webm", "-preset", "ultrafast",  "final.mp4"])
	
        #get dir
        path = os.getcwd()

        #remove the aux files
        os.remove(path + "/" + "video" + extension)
        os.remove(audio)


        # message that everything went fine
        flash("Your download is complete!")
        return render_template("downloadMP4.html")
    else:
        return render_template("mp4Downloader.html")


@app.route("/mp3Downloader", methods=["GET", "POST"])
def mp3Downloader():
    if request.method == "POST":
        url = request.form.get("url")

        # if url is not valid then return an error
        # and redirects to same page
        if not validators.url(url):
            flash("URL Not Valid")
            return render_template("mp3Downloader.html")

        # we have a YouTube object called yt
        yt = YouTube(url)

        # we have a youtubeDownloader object called download
        download = YoutubeDownloader(yt)

        # get title from a method designed in class YoutubeDownloader
        title = download.get_title()
        title_audio = title + ".mp3"


        # get audio
        audio = download.get_audio()

        # generate a "mp3" audio
        subprocess.run(["ffmpeg", "-i", audio, "-preset", "ultrafast", "final.mp3"])

        os.remove(audio)

        # message that everything went fine
        flash("Your download is complete!")
        return render_template("downloadMP3.html")
    else:
        return render_template("mp3Downloader.html")

@app.route("/downloadMP4", methods=["GET"])
def downloadMP4():
    return send_file("final.mp4", as_attachment=True)

@app.route("/downloadMP3", methods=["GET"])
def downloadMP3():
    return send_file("final.mp3", as_attachment=True)

if __name__ == "__main__":
	app.run()
