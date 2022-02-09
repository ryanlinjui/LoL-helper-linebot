from os import getenv
from imgurpython import ImgurClient

imgur_cfg = {
    "id":getenv("IMGUR_ID"),
    "secret":getenv("IMGUR_SECRET"),
    "access_token":getenv("IMGUR_ACCESS_TOKEN"),
    "refresh_token":getenv("IMGUR_REFRESH_TOKEN")
}

imgur_client = ImgurClient(imgur_cfg["id"], imgur_cfg["secret"])
imgur_client.set_user_auth(imgur_cfg["access_token"], imgur_cfg["refresh_token"])

__all__ = [
    "upload"
]