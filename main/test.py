import pandas as pd
from AuditData.text import txt
from AuditData.Audit import Audit
import psutil
from file.file_ulti import get_list_file,move_file,create_folder,write_data,zip_file,zipfile
import time
import os
import logging
class testfiletxt:
    def checkall(self,path,path_log):     
        list_header=['TransactionId', 'Type', 'Balance', 'PaidOut', 'Description', 'TransactionDate', 'Currency', 'CompanyId', 'PaidIn']
        files = get_list_file(path)
        for file in files:
            basename = os.path.basename(file)
            name_tuple= os.path.splitext(basename)
            print(file)
            write_data(path_log,'',name_tuple[0])
            flag,result= Audit().checkdelimiter(file)
            if(flag == False):
                Audit().write_data(file,result,'checkdelimiter')
                print("sai")
            else:
                df=txt().open_file(file,'~')
                fg_id,rs_id = Audit().check_ascending_number(df,'TransactionId')
                if(fg_id == False):
                    Audit().write_data(path_log,rs_id,'check_ascending_number')
                fg_bl,rs_bl=Audit().check_balance(df)
                if(fg_bl == False):
                    Audit().write_data(path_log,rs_bl,'check_balance')
                fg_cp,rs_cp = Audit().checkcompanyID(df,file)
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
            
    def refix_txt(self,path,path1):
        files = get_list_file(path)
        for file in files:
            df=txt().open_file(file,'~')
            rs=self.checkall(path,path1)
            if(self.checkall(path,path1) == True):
                dt=Audit().deleteSpace(df,'Description')
                dt.to_csv(file, sep='~', index=False)
                txt().check_list_file(path,rs,file)
                
            else:
                txt().check_list_file(path,rs,file)
if __name__ == '__main__':
    process = psutil.Process()
    start_time = time.time()
    path='D:/alt'
    #path_log='C:/Users/Admin/Downloads/alo.txt'
    #testfiletxt().checkall(path,path_log)
    #testfiletxt().refix_txt(path,path_log)
    
    list_header=['TransactionId', 'Type', 'Balance', 'PaidOut', 'Description', 'TransactionDate', 'Currency', 'CompanyId', 'PaidIn']
    txt().check_list_file(path,path,list_header)
    # zip_filepath = os.path.join(path, 'result.zip')
    # zip_file(zip_filepath,path)
    #zipfile(path+"\\zip",path)
          
            
            
            
            
            
                
                

