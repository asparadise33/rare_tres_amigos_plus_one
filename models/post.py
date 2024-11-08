from datetime import date

class Post():
  def __init__(self, id, user_id, category_id, title, image_url, content):
    self.id = id
    self.user_id = user_id
    self.category_id = category_id
    self.title = title
    self.publication_date = date
    self.image_url = image_url
    self.content = content
    self.approved = True
  
