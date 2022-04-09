
import validators

class Urls:

    def __init__(self):

        self.url_list = []
    
    def validate_url(self, url):

        """Check if the url has a correct format"""

        res = validators.url(url)
        if res == True: return True
        else: return False
    

    def add_post(self, post):

        """
        If the url is valid return a JSON response with original_url and short_url properties
        else return an error message
        """

        if self.validate_url(post):
            
            if post not in self.url_list:
               url_data = {"original_url": post, "short_url": len(self.url_list) + 1}
               self.url_list.append(url_data)
               
               return url_data
            else:
               return {"error": "that url already exists"}

        else:
            
            return {"error": "invalid url"}



       


