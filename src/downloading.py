import os
import time

'''
make It run on both linux /  and windows \
    '''

def download_files(ch=720):
    commandline4k = 'youtube-dl --add-metadata --write-info-json  --write-thumbnail --force-ipv4 \
         --sleep-interval 3 --max-sleep-interval 6 --ignore-errors --no-continue --no-overwrites \
        --download-archive archive.log -f "bestvideo+(bestaudio[acodec^=opus]/bestaudio)/bestvideo[height<=360]" \
        --merge-output-format "mkv" -o "D:/Youtube/%(uploader)s/%(upload_date)s_%(title)s %(id)s.%(ext)s" -a download.txt'
    commandline1080 = 'youtube-dl --add-metadata --write-info-json  --write-thumbnail --force-ipv4 \
         --sleep-interval 3 --max-sleep-interval 6 --ignore-errors --no-continue --no-overwrites \
        --download-archive archive.log -f "bestvideo[height<=1080]+(bestaudio[acodec^=opus]/bestaudio)/bestvideo[height<=360]" \
        --merge-output-format "mkv" -o "D:/Youtube/%(uploader)s/%(upload_date)s_%(title)s %(id)s.%(ext)s" -a download.txt'
    commandline720 = 'youtube-dl --add-metadata --write-info-json  --write-thumbnail --force-ipv4 \
         --sleep-interval 3 --max-sleep-interval 6 --ignore-errors --no-continue --no-overwrites \
        --download-archive archive.log -f "bestvideo[height<=720]+(bestaudio[acodec^=opus]/bestaudio)/bestvideo[height<=360]" \
        --merge-output-format "mkv" -o "D:/Youtube/%(uploader)s/%(upload_date)s_%(title)s %(id)s.%(ext)s" -a download.txt'
    commandline360 = 'youtube-dl --add-metadata --write-info-json  --write-thumbnail --force-ipv4 \
         --sleep-interval 3 --max-sleep-interval 6 --ignore-errors --no-continue --no-overwrites \
        --download-archive archive.log -f "bestvideo[height<=360]+(bestaudio[acodec^=opus]/bestaudio)/bestvideo[height<=360]" \
        --merge-output-format "mkv" -o "D:/Youtube/%(uploader)s/%(upload_date)s_%(title)s %(id)s.%(ext)s" -a download.txt'
    if ch == 720:
        commandline = commandline720
    elif ch == '4k':
        commandline = commandline4k
    elif ch == 1080:
        commandline = commandline1080
    elif ch == 360:
        commandline = commandline360
    os.system(commandline)

def replace2(parent):
    for path, folders, files in os.walk(parent):
        for f in files:
            os.rename(os.path.join(path, f), os.path.join(path, f.replace(' ', '__')))
        for i in range(len(folders)):
            new_name = folders[i].replace(' ', '_').replace('.', '_').replace("'", '')
            try:
                os.rename(os.path.join(path, folders[i]), os.path.join(path, new_name))
            except FileExistsError:
                pass
            folders[i] = new_name
# Traverse the specified directory, display all file names under the directory
def convertWebp2jpgInDirectory(dir):
    if os.path.isdir(dir):
        allfiles = os.listdir(dir)
        for fi in allfiles:
            fi_d = os.path.join(dir, fi)
            if os.path.isdir(fi_d):
                convertWebp2jpgInDirectory(fi_d)
            else:
                if fi_d.endswith(".webp"):
                    webp = os.path.join(dir, fi_d)
                    webp = '"'+webp+'"'
                    filename = webp.split("\\")[-1]
    
                    filedir = "\\".join(webp.split("\\")[:-1])
                    
                    newfilename = filename.replace(".webp",'.jpg')
                    jpg = "%s\%s"%(filedir, newfilename)
                    # jpg = '"'+jpg+'"'
                    commandline = "dwebp %s -o %s" % (webp, jpg)
                   
                    os.system(commandline)
                    print(webp + " ------> conversion succeeded")

                    deleteline = "rm "+webp
                    os.system(deleteline)

if __name__ == '__main__':
    pass
# download_files()
# convertWebp2jpgInDirectory("D:\Youtube")
# replace('D:\Youtube')