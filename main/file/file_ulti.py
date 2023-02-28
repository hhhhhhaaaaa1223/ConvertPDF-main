import os
import glob
import pathlib
import shutil
import psutil
import time
from datetime import datetime
from zipfile import ZipFile
import os
from os.path import basename
from  AuditData.contants import log_text
from shutil import make_archive

def zip_file(nameFile,path):
    make_archive(nameFile, 'zip', path)

def move_file(src_file,dst_file):
    shutil.copy(src_file, dst_file)

def file_get_contents(filename):
    try:
        with open(filename, encoding="utf-8-sig") as f:
            return f.read()
    except Exception as e:
        print('ex>>>', filename)
        with open(filename) as f:
            return f.read()

def get_list_file(directory, tp="*"):
    direct = os.path.join(directory, tp)
    list_of_files = glob.glob(direct, recursive=True)  # * means all if need specific format then *.csv
    # files = [f for f in list_of_files if os.path.isfile(f)]
    files = []
    for f in list_of_files:
        if os.path.isfile(f):
            files.append(f)
    return files
      
def write_data(path, data,name):
    now = datetime.now()
    path_config = path
    print('write_data path>>>', path_config)
    #error=map(log_text,name)
    #error = log_text[name]
    try:
        with open(os.path.join(path_config, 'log.txt'), 'a', encoding='utf-8') as f:
            # f = open(path_config, 'a', encoding='utf-8')
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

            f.write('\n'+str(dt_string)+'\t'+str(name) + '\n\t\t\t' + str(data))
            f.close()
    except Exception as e:
        print('ex write_data>>>', e)
        
def create_folder(path):
     if not os.path.isdir(path):
        os.makedirs(path)

def get_list_name_file(directory, tp="*", only_name=False):
    files = get_list_file(directory, tp)
    rs = []
    for f in files:
        name = pathlib.Path(f).name
        if only_name:
            name = name.split('.')[0]
        rs.append(name)
    return rs


def measure_perfomance():
    process = psutil.Process()
    start_time = time.time()
    # code need  measure perfomance in here:
    
    #
    end_time = time.time()
    print("CPU sử dụng: ", process.cpu_percent(), "%")
    print("Dung lượng RAM sử dụng: ", process.memory_info().rss / 1024 / 1024, "MB")
    print("Thời gian thực hiện: ", end_time - start_time, "giây")

def zipfile(path_folder,path_zip):
    with ZipFile(path_zip, 'w') as zipObj:
        for folderName, subfolders, filenames in os.walk(path_folder):
            for filename in filenames:
                #create complete filepath of file in directory
                filePath = os.path.join(folderName, filename)
                # Add file to zip
                zipObj.write(filePath, basename(filePath))

if __name__ == '__main__':
    path='C:\\Users\\Asus\\Downloads\\convert_pdf\\txt'
    fileSuccess=path+'\\fileSuccess'
    print()
    create_folder(fileSuccess)
    files = get_list_file(path)
    for file in files:
        print(file)
        print(fileSuccess)
        #move_file(file,fileSuccess)