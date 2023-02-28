from flask import Flask, request, render_template, session,send_file
import os
from  AuditData.text import txt
from  AuditData.Audit import Audit
import pandas as pd
import tempfile
app = Flask(__name__)
app.secret_key = os.urandom(24)
import zipfile
from zipfile import ZipFile
import shutil
from file.file_ulti import create_folder

@app.teardown_request
def delete_temp_folders(exception=None):
    # Lấy đường dẫn thư mục tạm thời
    temp_folder = session.get('temp_folder')
    print(temp_folder)
    # Nếu tồn tại thư mục tạm thời
    if temp_folder is not None:
        # Xóa thư mục tạm thời
        shutil.rmtree(temp_folder)
        
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Tạo thư mục tạm trên mỗi phiên session
        tp = tempfile.mkdtemp()
        os.chmod(tp, 0o777)
        #tp = tempfile.TemporaryDirectory()
       
        # with tempfile.TemporaryDirectory() as tp:
        print(tp)

        # Lưu các file txt vào thư mục tạm
        uploaded_files=request.files.getlist('file')    
        for file in uploaded_files:
            filename = file.filename
            file.save(os.path.join(tp, filename))
        list_header=['TransactionId', 'Type', 'Balance', 'PaidOut', 'Description', 'TransactionDate', 'Currency', 'CompanyId', 'PaidIn']
        #create_folder(tp+'\\log')
        txt().check_list_file(tp,tp,list_header)
        # Xử lý các file txt
        # for file in os.listdir(temp_dir):
        #     if file.endswith('.txt'):
        #         filepath = os.path.join(temp_dir, file)
        #         with open(filepath, 'r') as f:
        #             content = f.read()
        #         content = content.replace(' ', '')
        #         with open(filepath, 'w') as f:
        #             f.write(content)
        
        # Tạo file zip chứa các file txt đã được xử lý
        zip_filepath = os.path.join(tp, 'result.zip')
        with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for file in os.listdir(tp):
                if file.endswith('.txt'):
                    zip_file.write(os.path.join(tp, file), file)
        #shutil.rmtree(tp)
        session['file_content'] = 'ab'
        # # Trả về file zip cho người dùng để tải xuống
        return send_file(zip_filepath, as_attachment=True)
    
    return render_template('test.html')

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         # Lấy file từ request
#         file = request.files['file']
#         # file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
#         # file.save(file_path)
#         temp_dir = tempfile.mkdtemp()
#         print(temp_dir)
#         filename = file.filename
#         file.save(os.path.join(temp_dir, filename))
#         # Tạo một thư mục để lưu trữ các tệp tin đã tải lên
#         # folder_path = os.path.join(os.getcwd(), 'uploads')
#         # os.makedirs(folder_path, exist_ok=True)
#         zip_filepath = os.path.join(temp_dir, 'processed_files.zip')
#         return send_file(zip_filepath, as_attachment=True)
#         # df = pd.read_csv(file, sep='~', header=0)
#         # print(df)
#         # Đọc nội dung file
#         #df=txt().open_file(file,'~')
#         # flag,result=Audit().check_empty_row(df)
#         # print(result)
#         file_content = file.read().decode('utf-8')
        
#         # Lưu nội dung vào session
#         session['file_content'] = 'ab'
        
#     # Trả về giao diện
#     return render_template('test.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
