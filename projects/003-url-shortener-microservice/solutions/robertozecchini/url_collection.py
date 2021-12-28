import re

class UrlCollection:
    def __init__(self):
        self.collection = {}
        self.count = 0

    def __str__(self):
        return str(self.collection)
    
    #add url to collection, return the short_url if it's valid, 0 if not
    def add_url(self, url):
        if self.is_valid(url):
            shorturl = self.first_free_url()
            self.collection[shorturl] = url
            self.count += 1
            return shorturl
        else:
            return 0
    
    #return url if shorturl is registered, an empty string if not
    def get_original(self, shorturl):
        return self.collection.get(shorturl, '')

    #return the first free url to use
    def first_free_url(self):
        if self.count == 0:
            return 1
        keys = list(self.collection.keys())
        keys.sort()
        for i, k in enumerate(keys, start=1):
            if i != k:
                print(i)
                return i
        else:
            return self.count + 1
    
    #return if the url is valid
    def is_valid(self, url):
        pattern = r'(http|https)://(www.)?[a-zA-Z0-9@:%._\\+~#?&//=]{2,256}.[a-z]{2,6}(/[-a-zA-Z0-9@:%._\\+~#?&//=]*)?'
        if re.fullmatch(pattern, url):
            return True
        else:
            return False