# Utility function
import os
import shutil
import stat
import zipfile
import sys

if sys.version_info >= (3,):
    import urllib.request as urllib2
    import urllib.parse as urlparse
else:
    import urllib2
    import urlparse

def copyDirectoryandContent(_fromDir, _toDir):
    '''
    Function that copies directory and its content
    :param _fromDir: Source Directory
    :param _toDir: Target Directory
    :return: None
    '''
    shutil.copytree(_fromDir,_toDir)


def checkDirectoryExist(_dir):

    return os.path.isdir(_dir)
def checkDirectoryEmpty(_dir):
    return not os.listdir(_dir)
def checkFileExist(_file):
    return os.path.exists(_file)
def searchFileInDirectory(_filename, _directory):
    for root,dirs,files in os.walk(_directory):
        for file in files:
                if file == _filename:
                    return os.path.join(root,file)
def searchDirInDirectory(_dirname, _directory):
    for root,dirs,files in os.walk(_directory):
        for dir in dirs:
            if dir == _dirname:
                return os.path.join(root,dir)
    return None
def getFileExtension(_filepath):
    return os.path.splitext(_filepath)[1]
def getFileName(_filepath):
    return os.path.splitext(os.path.basename(_filepath))[0]
def getFileDirectory(_filepath):
    return os.path.split(_filepath)[0]
def is_number(var):
    try:
        complex(var)
    except Exception:
        return False
    return True
def getModifiedtime(path):
    return os.path.getmtime(path)
def updatedirectory(_dir1, _dir2):
    shutil.rmtree(_dir1)
    shutil.copytree(_dir2,_dir1)
def updatefile(_file1, _file2):
    try:
        os.remove(_file1)
    except:
        pass
    shutil.copy2(_file2,_file1)
def removefile(path):
    try:
        os.remove(path)
    except:
        os.chmod(path,stat.S_IWRITE)
        os.remove(path)
def getRelativePath(_real, _root):
    relativepath = _real.split(_root)[1]
    newrelativetpath = relativepath
    if relativepath != '':
        newrelativetpath = relativepath[1:]
    return  newrelativetpath
def selectivecopy(src,dst,list):
    '''
    Selectively copy directories in the directory
    :param src:
    :param dst:
    :param list:
    :return:
    '''
    if not checkDirectoryExist(dst):
        os.makedirs(dst)
    listcpy = list.copy()
    for dir in os.listdir(src):
        if dir in listcpy:
            listcpy.remove(dir)
            realpathsrc = os.path.join(src,dir)
            dstpathsrc = os.path.join(dst,dir)
            shutil.copytree(realpathsrc,dstpathsrc)

''' Zip Related'''

def unzipfile(filename, directory):
    '''
    Extract the content of a zip file
    :param filename: name of the file
    :param directory: extraction directory
    :return:
    '''
    extention = getFileExtension(filename)
    if extention == '.zip' or extention =='.ZIP':
        newzipfile = zipfile.ZipFile(filename)
        newzipfile.extractall(directory)
    else:
        print("Target is not a zip file")

def download_file(url, desc=None):
    u = urllib2.urlopen(url)

    scheme, netloc, path, query, fragment = urlparse.urlsplit(url)
    filename = os.path.basename(path)
    if not filename:
        filename = 'downloaded.file'
    if desc:
        filename = os.path.join(desc, filename)

    with open(filename, 'wb') as f:
        meta = u.info()
        meta_func = meta.getheaders if hasattr(meta, 'getheaders') else meta.get_all
        meta_length = meta_func("Content-Length")
        file_size = None
        if meta_length:
            file_size = int(meta_length[0])
        print("Downloading: {0} Bytes: {1}".format(url, file_size))

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)

            status = "{0:16}".format(file_size_dl)
            if file_size:
                status += "   [{0:6.2f}%]".format(file_size_dl * 100 / file_size)
            status += chr(13)
            print(status, end="")
        print()

    return filename



if __name__ == "__main__":
    download_file("http://amf-farm2-winx6:8080/job/AMF_1.3_4Main_Nightly/3/artifact/*zip*/archive.zip")
