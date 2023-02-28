#from flask_uploads import UploadSet, configure_uploads, ALL
from flask import Flask, render_template, request, send_file
import os
import zipfile
print(os.listdir())
from werkzeug.utils import secure_filename
app = Flask(__name__)
# files = UploadSet('files', ALL)
# configure_uploads(app, files)

app.config['UPLOAD_FOLDER'] = 'uploads'

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Hiển thị trang tải lên
@app.route('/')
def upload_form():
    return render_template('index.html')


# Xử lý tệp tin được tải lên
@app.route('/', methods=['POST'])
def upload_file():
    uploaded_files = request.files.getlist('file')
    foldername = secure_filename(request.form['foldername'])
    folderpath = os.path.join(app.config['UPLOAD_FOLDER'], foldername)
    os.makedirs(folderpath, exist_ok=True)
    filenames = []
    for file in uploaded_files:
        filename = secure_filename(file.filename)
        print(filename)
        #file.save(os.path.join(folderpath, filename))
        filenames.append(filename)
    return 'Uploaded files: ' + ', '.join(filenames)

@app.route("/download")
def download():
    # jungle_zip = zipfile.ZipFile('uploads', 'w')
    # jungle_zip.write('uploads/files.zip', compress_type=zipfile.ZIP_DEFLATED)
    # jungle_zip.close()
    return send_file("uploads/txt_0000011264_20230118_S1_20230120130001.txt",
                     attachment_filename="txt_0000011264_20230118_S1_20230120130001.txt",
                     as_attachment=True)
    
# @app.route('/download/<path:filename>')
# def download(filename):
#     return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)