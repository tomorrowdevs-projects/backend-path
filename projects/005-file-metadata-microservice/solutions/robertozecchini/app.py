from flask import Flask, request, jsonify

UPLOAD_PAGE = '''
<!doctype html>
<title>Upload new File</title>
<h1>Upload new File</h1>
<form method=post enctype=multipart/form-data>
<input type=file name=upload>
<input type=submit value=Upload>
</form>
'''

app = Flask(__name__)
# max file size. Set parameter depending on the ram available for service
app.config['MAX_CONTENT_LENGTH'] = 1024*1024*1024

def file_size(file):
    blob = file.read()
    size = len(blob)
    return size

@app.route('/', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'upload' not in request.files:
        return jsonify({'error': "No file in POST request"})
    file = request.files['upload']
    # If the user does not select a file, the browser submits an empty file without a filename.
    if file.filename == '':
        return jsonify({'error': "No file selected"})
    f_dict = {
        'filename': file.filename,
        'type': file.mimetype,
        'size': file_size(file)
        }
    return jsonify(f_dict)

#provide a html form to simplify the use of api
@app.route('/', methods=['GET'])
def upload_page():
    return UPLOAD_PAGE

if __name__ == '__main__':
    app.run(debug=True)