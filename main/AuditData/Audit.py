import pandas as pd

#from  AuditData.text import txt
from datetime import datetime
import os
import logging
import time
from datetime import datetime
import csv
import sys
from  AuditData.contants import log_text
class Audit():
    def __init__(self):
        super().__init__()
    #Dư khoảng trắng
    def deleteSpace(self,data,col):
        data[col] = data[col].str.replace('\s+', ' ', regex=True).str.strip()
        return data

    def write_data(self,path, data,name):
        now = datetime.now()
        path_config = path
        print('write_data path>>>', path_config)
        #error=map(log_text,name)
        error = log_text[name]
        try:
            with open(os.path.join(path_config, 'log.txt'), 'a', encoding='utf-8') as f:
                # f = open(path_config, 'a', encoding='utf-8')
                f.write('\n'+'\t\t'+'+ '+str(error) + '\n\t\t\t' + str(data))
                f.close()
        except Exception as e:
            print('ex write_data>>>', e)
    #Có cùng lúc in, out
    def checkInOut(self,data):
        dk = data.loc[(data['PaidIn'] != 0) & (data['PaidOut'] != 0)]
        if(len(dk) > 0):
            # path = 'C:/Users/Admin/Downloads/alo.txt'
            # Audit.write_data(path, dk.values.tolist())
            return False,dk.values.tolist()
        return True,[]
    
    # check format date
    def checkvalidatedate(self,df,col):
        # Kiểm tra định dạng ngày tháng trong cột 'date'
        date_format = '%Y-%m-%d'
        is_valid_date = pd.to_datetime(df[col], format=date_format, errors='coerce').notnull().all()
        # Kiểm tra kết quả
        if is_valid_date:
            print('Các giá trị trong cột "date" hợp lệ với định dạng ngày tháng')
            return True,[]
        else:
            invalid_dates = df.loc[pd.to_datetime(df[col], format=date_format, errors='coerce').isna(), col]
            print(f'Các giá trị sau không hợp lệ với định dạng ngày tháng: {invalid_dates.tolist()}')
            return False,invalid_dates
    #Sai mã khách hàng
    def checkcompanyID(self,data,path):
        #='C:/Users/Admin/Downloads/0000011264_20230118_S1_20230120130001.txt'
        basename = os.path.basename(path)
        name_tuple= os.path.splitext(basename)
        filename=name_tuple[0]
        ls = filename.split("_")
        name = f"{ls[0]}"
        k = name.lstrip('0')
        dk = data.loc[(data['CompanyId'] != int(k))]
        if(len(dk) > 0):
            return False,dk
        return True,[]
    # check error balance
    def find_row_error_balance(self,data):
        list= []
        for index, row in data.iterrows():
            if index == 0:
                t = row['Balance']
            else:
                t = data.loc[index - 1, 'Balance']
                # print("Balance -1 ",t)
            t = t + row['PaidIn'] - row['PaidOut']- row['Balance']
            x = round(t, 0)
            if x != 0 :
                # path1='C:/Users/Admin/Downloads/alo.txt'
                # Audit().write_data(path1,row['TransactionId'],sys._getframe().f_code.co_name)
                list.append(row['TransactionId'])
            print(f"Dòng {index +1}: {t}")
        return list
    # check dau phan cach        
    def checkdelimiter(self,path):
        with open(path, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            #print(header)
            t=[]
            if header[0].find('~~') != -1:
                return False , header
            else :
                num_tildes = header[0].count('~')
                rows = []
                for row in reader:
                    #print(row[0].count('~'))
                    rows.append(row)
                    if(rows[0].count('~') > num_tildes ):
                        #print("loi")
                        t.append(rows)
                    #print("qua")
                if(len(t) > 0):
                    return False,t
                return True,[]

    # check transactionID
    def check_ascending_number(self,df,column):
        if(df[column][0] == 1):
            
            diff = df[column].diff()
            if (diff[1:] == 1).all():
                return True,[]
            else:
                not_increasing_rows = diff[diff != 1].index
                #.iloc[1:] avoid first row 
                result = df.loc[not_increasing_rows].iloc[1:]
                return False, result
        else:
            return False , df[column][0]
        
    def check_tittle(self,df,header_list):
        df_header_set = set(df.columns)
        if df_header_set == set(header_list):
            return True,[]
        else:
            missing_values = df_header_set-set(header_list)
            return False, missing_values
        
        
    def check_balance(self,df):
        balanceFinal=df['Balance'][0]-df["PaidOut"][1:].sum()+df["PaidIn"][1:].sum()
        last_row = df.iloc[-1]
        column_value = last_row["Balance"]
        if column_value==balanceFinal: 
            return True,[]
        else:
            rowError=self.find_row_error_balance(df)
            return False,rowError
    
    def check_empty_row(self,df):
        df['Balance'] = df['Balance'].astype(str)
        mask= df[['TransactionDate', 'Balance']].isnull().any(axis=1) | df['Balance'].str.isspace() | df['TransactionDate'].str.isspace() 
        if len(df.loc[mask])>0:
            return False,df.loc[mask]
        else:
            return True,[]
    
if __name__ == '__main__':
    pass
    #print(txt().open_file('C:/Users/Admin/Downloads/0000011264_20230118_S1_20230120130001.txt','~'))