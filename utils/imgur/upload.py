from . import imgur_client

def upload(img_path:str)->str:
  '''
	Upload a picture and return uploaded url
	'''
  image = imgur_client.upload_from_path(img_path, anon=False)
  return image['link']