#!python3

import os
import subprocess

TARGET_DIR = os.path.expanduser("~/Music/Music/Media.localized/Automatically Add to Music.localized")

# Max number of running processes
# Increase this values if you have large amount of cores
MAX_PROCESSES = 16 

processes = []

# Wait for some processes to complete if MAX_PROCESSES limit is reached
def complete_processes():
  global processes

  # Check if any of the processes has completed
  live_processes = []
  for process in processes:
    if process.poll() is None:
      live_processes.append(process)
  processes = live_processes
  
  # If there is no processes still completed, we will wait for one to complete
  if len(processes) >= MAX_PROCESSES:
    print("=> Waiting for processes to complete")
    process = processes.pop()
    process.wait()

def handle_file(filepath, filename):

  # MP3 files will be moved directly to the target directoy
  if filepath.endswith(".mp3"): 
    complete_processes()

    print("=> Copying:", filepath)
    p = subprocess.Popen(['cp', filepath, os.path.join(TARGET_DIR, filename)])
    processes.append(p)
    
  # Flac files will be converted first and then moved to the target directory
  elif filepath.endswith(".flac"):
    complete_processes()

    print("=> Converting:", filepath)
    mp3_filename = filename.replace(".flac", ".mp3")
    mp3_filepath = os.path.join(TARGET_DIR, mp3_filename)
    p = subprocess.Popen(['ffmpeg', '-loglevel', 'fatal', '-i', filepath, '-ab', '320k', '-map_metadata', '0', '-id3v2_version', '3', mp3_filepath])
    processes.append(p)

# Walk recursively through all directories
def find_music_files(directory = './'):
  for dirpath, dirnames, filenames in os.walk(directory):
    for filename in filenames:
      full_path = os.path.join(dirpath, filename)
      handle_file(full_path, filename)

find_music_files()

for process in processes:
  process.wait()

print("=> All processes completed!")
