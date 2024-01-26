from rich import print
from rich.console import Console
import shutil
import os
from PIL import Image
from datetime import datetime
import send2trash
from loguru import logger

console = Console(width=100, color_system="truecolor")
imagesPath = "C:/Users/Edy/Pictures/Mis Imagenes"
logPath = f"logs/Log {datetime.now().date()}.log"
# Configure the logger to write to a file
logger.add(logPath, level="INFO", rotation="10 MB", compression="zip", format="{time} - {level} - {message}")

prohibidos = ["ini", "log"]

def file_age_in_days(file_path):
    # Get the file's last modification time
    modification_time = os.path.getmtime(file_path)

    # Calculate the difference between the current time and the modification time
    current_time = datetime.now().timestamp()
    age_in_seconds = current_time - modification_time

    # Convert the age to days
    age_in_days = age_in_seconds / (24 * 3600)

    return age_in_days

def redirectFile(path, filePath, rootPath):
  newPath = path.strip("[]").replace("~", "/") if path.startswith("[") else path.strip("()").replace("~", "/")
  newPath = rootPath + "/" + newPath
  if os.path.exists(newPath):
    shutil.move(filePath, newPath)
  else:
    os.makedirs(newPath)
    shutil.move(filePath, newPath)
  renamed = filePath.split("\\")[-1].split("-")[-1]
  os.rename(f"{newPath}/{filePath.split("\\")[-1]}", f"{newPath}/{renamed}")
  logger.info(f"{renamed} was moved to {newPath}")

def wrapped(text):
  return (text.startswith("[") and text.endswith("]")) or (text.startswith("(") and text.endswith(")"))

def is_image(path):
  try:
    Image.open(path)
    existeTag = path.split("\\")[-1]
    try:
      newPath = existeTag.split("-")[0]
      if wrapped(newPath):
        redirectFile(newPath, path, imagesPath)
    except:
      console.print("[bold red]Something went wrong")
    shutil.move(path,imagesPath)
    logger.info(f"{path.split("\\")[-1]} was moved to {imagesPath}")
  except:
    newPath = path.split("\\")[-1].split("-")[0]
    if path.split("\\")[-1].startswith("["):
      redirectFile(newPath, path, "C:/Users/Edy/Documents/ITEE")
    elif path.split("\\")[-1].startswith("("):
      redirectFile(newPath, path, "C:/Users/Edy/Documents/Projects")
    else:
      if file_age_in_days(path) > 5 and path.split("\\")[-1].split(".")[-1] not in prohibidos:
        path = path.replace("/", "\\")
        send2trash.send2trash(path)
        logger.info(f"{path} was sent to the trashcan")
      else:
        pass

filePath = "C:/Users/Edy/Downloads"
if os.path.exists(filePath):
  files_in_folder = [f for f in os.listdir(filePath) if os.path.isfile(os.path.join(filePath, f))]
  for file in files_in_folder:
    if file.split("-")[0] == "[!]":
      console.print("[bold yellow]File ignored")
    else:
      is_image(os.path.join(filePath, file))
  print("[green]All done")


else:
  os.makedirs(filePath)
  print("[bold]File created with success.")