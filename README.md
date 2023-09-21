# apple-music-load
Converts and uploads your music directly to iTunes (Apple Music).

Recursivily finds all MP3 and FLAC files in the current directory and uploads them to iTunes.  
Flac files will be converted to MP3 (using ffmpeg) because iTunes doesn't support FLAC.

Usage:
```sh
# Go to the directory with your music (or root directory)
cd my-music

# Start uploading
python3 apple-music-load.py
```

## Performance

 * To better utilize all cores, the script launches multiple processes in parallel to convert your FLAC files to MP3 
 * You can configure how much processes the script can run in parallel by changing `MAX_PROCESSES` variable
 * Also uses multiple processes in parallel for copying MP3 files to make transfers of multiple files almost instant
