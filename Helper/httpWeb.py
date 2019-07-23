import urllib
import http

from urllib import request

class HttpWeb:

    OnSuccess = None
    OnFailed = None
    Url = ""
    def __init__(self, url, onSuccess, onFailed):
        self.OnSuccess = onSuccess
        self.OnFailed = onFailed
        self.Url = url

    def execute(self):

        r = urllib.request.urlopen(self.Url)
       
        data = r.read()
        if r.status == http.HTTPStatus.OK:
           self.OnSuccess(data)
        else:
            self.OnFailed(data)







