"""
Script will use a Google ID to find google resources and print out links/ open browser windows for each resource it finds
"""
import requests
import webbrowser
from bs4 import BeautifulSoup
import xmltodict

class Target():
    """
    Gooogle Target
    """

    def __init__(self, google_id=""):
        if google_id:
            self.google_id = google_id
        else:
            self.google_id = self.get_google_id()

    def get_google_id(self):
        self.google_id = input("Google ID: ")
        return self.google_id


class GoogleNetwork():
    """
    Abstract class to be used for each individual Google site
    """

    url_template = ""
    
    def __init__(self, google_id):
        self.url = self.build_url(google_id)

    def build_url(self, google_id):
        return self.url_template + google_id

    def request(self):
        self.response = requests.get(self.url)
        return self.response

    def parse(self):
        while True:
            try:
                output = self.response.text
                break
            except AttributeError:
                self.request()
        return output
    
    def verify_existence(self):
        """
        Checks to see if anything was found on the web page
        """
        raise NotImplementedError()



class PhotoAlbum(GoogleNetwork):

    url_template = "https://get.google.com/albumarchive/"

    def verify_existence(self, contents):
        soup = BeautifulSoup(contents, features="html.parser")
        # check_location = '//*[@id="yDmH0d"]/c-wiz/div[2]/div/span/c-wiz/div/div[2]/div[2]/div[2]/div'
        check = soup.find_all('div')
        for tag in check:
            if "Looks like you've reached the end" in tag.text:
                return False
            else:
                print(tag.text)
                return True


class LocalGuide(GoogleNetwork):

    url_template = "https://www.google.com/maps/contrib/"


class YouTube(GoogleNetwork):

    url_template = "https://www.youtube.com/feeds/videos.xml?user="

    def __init__(self, user):
        super().__init__(google_id=user)

    def parse(self):
        object = xmltodict.parse(requests.get(self.url).text)
        self.youtube_url = object['feed']['author']['uri']
        return self.youtube_url


if __name__ == "__main__":
    target = Target(google_id='111847369296165457396')
    local_guide = LocalGuide(google_id=target.google_id)
    photo_album = PhotoAlbum(google_id=target.google_id)
    youtube = YouTube(user="test")

    youtube.parse()
    print("Local Guide: " + local_guide.url)
    print("Photo Album: " + photo_album.url)
    print("YouTube " + youtube.youtube_url)
    
    webbrowser.open(local_guide.url, new=2)
    webbrowser.open(photo_album.url, new=2)
    webbrowser.open(youtube.youtube_url, new=2)
