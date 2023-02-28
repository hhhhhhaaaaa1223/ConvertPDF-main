from flask import Flask, request, render_template, session
import os
from AuditData.text import txt
from AuditData.Audit import Audit
app = Flask(__name__)
app.secret_key = os.urandom(24)

# @app.route('/', methods=['GET', 'POST'])
# def upload_file():
#     if 'logged_in' not in session:
#         session['logged_in'] = False

#     if request.method == 'POST':
#         file = request.files['file']
#         if file.filename == '':
#             return render_template('test.html', message='No file selected')
#         if file and file.filename.endswith('.txt'):
#             file_contents = file.read().decode('utf-8')
#             session['logged_in'] = True
#             session['contents'] = file_contents
#             return render_template('test.html', contents=file_contents)
#         else:
#             return render_template('test.html', message='Invalid file type')

#     if session['logged_in']:
#         return render_template('test.html', contents=session['contents'])
#     else:
#         return render_template('test.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Lấy file từ request
        file = request.files['file']
        
        # Đọc nội dung file
        df=txt().open_file(file,'~')
        flag,result=Audit().check_empty_row(df)
        #file_content = file.read().decode('utf-8')
        
        # Lưu nội dung vào session
        session['file_content'] = result
        
    # Trả về giao diện
    return render_template('test.html')


if __name__ == '__main__':
    app.run(debug=True)
