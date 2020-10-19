class YoutubeDownloader:
    def __init__(self, yt):
        self.yt = yt

    #meter numa janelinha de opções
    def get_title(self):
        return self.yt.title

    def download_video(self):
        return self.yt.streams.order_by("resolution").desc().first().download()
    
    def get_video(self):
        return self.yt.streams.filter(type="video").order_by('resolution').desc().first().download(filename="video")

    def get_audio(self):
        return self.yt.streams.filter(only_audio=True).order_by("abr").desc().first().download(filename="audio")

