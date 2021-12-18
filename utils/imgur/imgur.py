from imgurpython import ImgurClient
from . import imgur_cfg

imgur_client = ImgurClient(imgur_cfg["id"], imgur_cfg["secret"])
imgur_client.set_user_auth(imgur_cfg["access_token"], imgur_cfg["refresh_token"])

def upload(img_path:str):
  '''
	Upload a picture and return uploaded url
	'''
  image = imgur_client.upload_from_path(img_path, anon=False)
  return image['link']