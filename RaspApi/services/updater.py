from urllib.request import urlopen
import zipfile36
import glob, os, shutil
import io

class updateService(object):
    
    def checkForUpdate(workingDir):
        with open('build_number') as f:
            thisBuild = f.readline()

        gitBuildUri = "https://raw.githubusercontent.com/louisvarley/RaspApi/master/build_number"
        with urlopen(gitBuildUri) as url:
            remoteBuild = url.read().decode()

        print("This Build " + str(thisBuild))
        print("Available Build " + str(remoteBuild))
           
        if(thisBuild < remoteBuild):
            return True
        else:
            return False
                

    def update(workingDir):

        gitArchiveUri = "https://github.com/louisvarley/RaspApi/archive/master.zip"

        print("Downloading Updates...")

        #Download ZIP
        with urlopen(gitArchiveUri) as r:
            with zipfile36.ZipFile(io.BytesIO(r.read()), "r") as z:
                print("Installing Updates...")

                for file in z.namelist():
                    if file.startswith('RaspApi-master/'):
                        z.extract(file, workingDir)


        root_src_dir = workingDir + "/RaspApi-master"
        root_target_dir = workingDir

        operation= 'move' # 'copy' or 'move'

        for src_dir, dirs, files in os.walk(root_src_dir):
            dst_dir = src_dir.replace(root_src_dir, root_target_dir)
            if not os.path.exists(dst_dir):
                os.mkdir(dst_dir)
            for file_ in files:
                src_file = os.path.join(src_dir, file_)
                dst_file = os.path.join(dst_dir, file_)
                if os.path.exists(dst_file):
                    os.remove(dst_file)
                if operation is 'copy':
                    shutil.copy(src_file, dst_dir)
                elif operation is 'move':
                    shutil.move(src_file, dst_dir)


