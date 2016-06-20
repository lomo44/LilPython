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
def is_file(_path):
    return os.path.isfile(_path)
def is_dir(_path):
    return os.path.isdir(_path)


def copyDirectoryandContent(_fromDir, _toDir):
    '''
    deprecated
    Function that copies directory and its content
    :param _fromDir: Source Directory
    :param _toDir: Target Directory
    :return: None
    '''
    shutil.copytree(_fromDir,_toDir)
def delete_content_in_directory(src):
    for dir in os.listdir(src):
        delete_directory_and_content(dir)

def checkDirectoryExist(_dir):

    return os.path.isdir(_dir)
def checkDirectoryEmpty(_dir):
    return not os.listdir(_dir)
def checkFileExist(_file):
    return os.path.exists(_file)
def check_file_exist_in_directory(_file,dir):
    for root, dirs,files in os.walk(dir):
        for file in files:
            if _file == file:
                return True
    return False
def check_dir_exist_in_directory(dirmame, dir):
    for dir in os.listdir(dir):
        if dir == dirmame:
            return  True
    return False
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


def set_rw(operation, name, exc):
    os.chmod(name, stat.S_IWRITE)
    return True

def clean_directory(src, excludelist):
    excludelistcpy = excludelist.copy()
    for root,dirs,files in os.walk(src):
        for dir in dirs:
            path = getRelativePath(os.path.join(root,dir),src)
            if path !='' and path not in excludelistcpy:
                os.chmod(os.path.join(root,dir), stat.S_IWRITE)
                shutil.rmtree(os.path.join(root,dir), onerror=set_rw)

def delete_directory_and_content(dir):
    shutil.rmtree(os.path.join(dir), onerror=set_rw)

def copy_directory_and_content(_from, _to):
    if not checkDirectoryExist(_to):
        os.makedirs(_to, mode=0o777, exist_ok=True)
    for item in os.listdir(_from):
        torealpath = os.path.join(_to,item)
        fromrealpath = os.path.join(_from,item)
        if is_file(fromrealpath) and not checkFileExist(torealpath):
            shutil.copyfile(fromrealpath,torealpath)
        if is_dir(fromrealpath):
            copy_directory_and_content(fromrealpath, torealpath)

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


def sync_folder_using_mtime(_remoteroot, _localroot):
    updated = False
    for root,dirs,files in os.walk(_remoteroot):
        for file in files:
            remoterealpath = os.path.join(root,file)
            relativepath = getRelativePath(root, _remoteroot)
            localrealpath = os.path.join(_localroot, relativepath, file)
            try:
                localmodifiedtime = getModifiedtime(localrealpath)

            except:
                localmodifiedtime = 0
            remotemodifiedtime = getModifiedtime(remoterealpath)
            if (remotemodifiedtime != localmodifiedtime):
                print("Sync: " + localrealpath)
                filedir = getFileDirectory(localrealpath);
                if not checkDirectoryExist(filedir):
                    os.makedirs(filedir)
                updatefile(localrealpath, remoterealpath)
                if updated is False:
                    updated = True
    print(_localroot + " is up-to-date")
    return updated
def selective_syncing(_remoteDir, _localDir, include_list, forceupdate = None, keeprelativepath = True):
    updated = False
    _include_list = include_list.copy()
    for root, dirs, files in os.walk(_remoteDir):
        for dir in dirs:
            if dir in _include_list:
                _include_list.remove(dir)
                if keeprelativepath == False:
                    localrealpath = os.path.join(_localDir,dir)
                else:
                    relativepath = getRelativePath(root,_remoteDir)
                    localrealpath = os.path.join(_localDir,relativepath,dir)
                remotepath = os.path.join(root,dir)
                if checkDirectoryExist(localrealpath):
                    if forceupdate:
                        forceUpdateLocalTestDepot(remotepath,localrealpath)
                    else:
                        print("Local " + localrealpath + " exist, Syncing...")
                        updated = sync_folder_using_mtime(remotepath, localrealpath)
                else:
                    print("Copying: "+ dir)
                    copyDirectoryandContent(os.path.join(root,dir),localrealpath)
                    updated = True
            if len(_include_list) == 0:
                return updated
    return updated
if __name__ == "__main__":
    #download_file("http://amf-farm2-winx6:8080/job/AMF_1.3_4Main_Nightly/3/artifact/*zip*/archive.zip")
    #clean_directory(r"C:\Depot\AMFDepot", ["Thirdparty"])
    copy_directory_and_content(r'C:\Depot\AMFDepot\AMF\tests-amf\_results',
                               r'\\amf-farm2-winx6\AMF-Results\4main_test_result')