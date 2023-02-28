import pandas as pd
from file.file_ulti import get_list_file,move_file,create_folder,write_data
import chardet
import os
from AuditData.Audit import Audit
class txt():
    def __init__(self):
        super().__init__()
        
    def open_file(self,path,delimiter):
        with open(path, 'rb') as f:
            result = chardet.detect(f.read())
        df = pd.read_csv(path, sep=delimiter, header=0, encoding=result['encoding'])
        return df
    
    def check_file(self,path_log, path_file,list_header):
        basename = os.path.basename(path_file)
        name_tuple= os.path.splitext(basename)
        write_data(path_log,'',name_tuple[0])
        flag,result= Audit().checkdelimiter(path_file)
        if(flag == False):
            Audit().write_data(path_log,result,'checkdelimiter')
        else:
            df=txt().open_file(path_file,'~')
            fg_id,rs_id = Audit().check_ascending_number(df,'TransactionId')
            if(fg_id == False):
                Audit().write_data(path_log,rs_id,'check_ascending_number')
            fg_bl,rs_bl=Audit().check_balance(df)
            if(fg_bl == False):
                Audit().write_data(path_log,rs_bl,'check_balance')
            fg_cp,rs_cp = Audit().checkcompanyID(df,path_file)
            if(fg_cp == False):
                Audit().write_data(path_log,rs_cp,'checkcompanyID')
            fg_io,rs_io=Audit().checkInOut(df)
            if(fg_io == False):                    
                Audit().write_data(path_log,rs_io,'checkInOut')
            fg_etrow,rs_etrow= Audit().check_empty_row(df)
            if(fg_etrow == False):
                Audit().write_data(path_log,rs_etrow,'check_empty_row')
            fg_tt,rs_tt = Audit().check_tittle(df,list_header)
            if(fg_tt == False):
                Audit().write_data(path_log,rs_tt,'check_tittle')
            fg_date,rs_date=Audit().checkvalidatedate(df,'TransactionDate')
            if(fg_date == False):
                Audit().write_data(path_log,rs_date,'checkvalidatedate')
            if(False in (fg_bl,fg_cp,fg_date,fg_etrow,fg_io,fg_tt,fg_id ) ):
                return False
            return True
        
    def check_list_file(self,path,pathLog,list_header):
        fileSuccess=path+'\\fileSuccess'
        create_folder(fileSuccess)
        fileError=path+'\\fileError'
        create_folder(fileError)
        files = get_list_file(path)
        for filePath in files:
            #rs=self.check_file(path,pathLog)
            #basename = os.path.basename(file)
            #name_tuple= os.path.splitext(basename)
            if (self.check_file(pathLog,filePath,list_header) == True):
                move_file(filePath,fileSuccess)       
                # path_ex = f"""{fileError}\\{basename}"""
                # print(path_ex)
                # if os.path.exists(path_ex):
                #     os.remove(path_ex)
            else:
                # path_ex = f"""{fileSuccess}\\{basename}"""
                # if os.path.exists(path_ex):
                #     os.remove(path_ex)
                move_file(filePath,fileError)
            
if __name__ == '__main__':
    txt().check_file()
    #print(txt().open_file('C:\\Users\\Asus\\Downloads\\convert_pdf\\0000011264_20230118_S1_20230120130001.txt','~'))
    print(txt().open_file('C:/Users/Admin/Downloads/0000011264_20230118_S1_20230120130001.txt','~'))
