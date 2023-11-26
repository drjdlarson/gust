import os
import pathlib
from PIL import Image


for path in pathlib.Path("offline_folders").rglob("*.jpeg"):
    im1 = Image.open(path)
    im1.save(str(path).replace(".jpeg", ".png"))
