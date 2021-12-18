from os import getenv
from .imgur import *
imgur_cfg = {
    "id":getenv("IMGUR_ID"),
    "secret":getenv("IMGUR_SECRET"),
    "access_token":getenv("IMGUR_ACCESS_TOKEN"),
    "refresh_token":getenv("IMGUR_REFRESH_TOKEN")
}
__all__ = [
    "upload"
]