import docx
# from docxapp import app
from flask import Flask, request, jsonify

from flask import Flask

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['docx'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def returnData():
	resp = jsonify({'status' : 'ok'})
	resp = jsonify({'message' : 'Use /docx-read path and upload docx file to get file contents'})
	resp.status_code = 200
	return resp

@app.route('/docx-read',methods=["POST"])
def upload_file():
	if 'file' not in request.files:
		resp = jsonify({'message' : 'No file part in the request'})
		resp.status_code = 400
		return resp
	file = request.files['file']
	if file.filename == '':
		resp = jsonify({'message' : 'No file selected for uploading'})
		resp.status_code = 400
		return resp
	if file and allowed_file(file.filename):
		data = " "
		try:
			doc = docx.Document(file)
			fullText = []
			for para in doc.paragraphs:
				fullText.append(para.text)
				data = ' '.join(fullText)
		except IOError:	 
			print('error')
		resp = jsonify({
			'message' : 'File successfully uploaded',
			'filetext' : data	
		})
		resp.status_code = 201
		return resp
	else:
		resp = jsonify({'message' : 'only docx file allowed'})
		resp.status_code = 400
		return resp
