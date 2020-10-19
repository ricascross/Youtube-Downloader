from main import app
import os

if __name__ == "__main__":
	app.run()
	os.remove("final.mp4")
	os.remove("final.mp3")
