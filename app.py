import os
from flask import send_file
import re
import urllib.request
from flask import Flask, flash, request, redirect, render_template,url_for,send_from_directory
from werkzeug.utils import secure_filename
from pdfminer.pdfinterp import PDFResourceManager#, PDFPage.get_pages()
from pdfminer.converter import TextConverter
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter#process_pdf
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams
import pathlib,os

# done = False
# #here is the animation
# def animate():
#     for c in itertools.cycle(['|', '/', '-', '\\']):
#         if done:
#             break
#         sys.stdout.write('\rloading ' + c)
#         sys.stdout.flush()
#         time.sleep(0.1)
#     sys.stdout.write('\rDone!     ')

# t = threading.Thread(target=animate)
# t.start()

# #long process here
# time.sleep(10)
# done = True
app = Flask(__name__)

UPLOAD_FOLDER = '/tmp'
DOWNLOAD_FOLDER = '/tmp'
app.secret_key = "1234"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['pdf'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
        # check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(url_for('index'))
		file = request.files['file']
		if file.filename == '':
			flash('No file selected for uploading')
			return redirect(url_for('index'))
		elif file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

			#convert function pdf to text
			rsrcmgr = PDFResourceManager()
			retstr = StringIO()
			laparams = LAParams()
			device = TextConverter(rsrcmgr, retstr, laparams=laparams)
			pdf_file = "/tmp/" + filename
			fp = open(pdf_file, 'rb')
			interpreter = PDFPageInterpreter(rsrcmgr, device)
			password = ""
			maxpages = 0
			caching = True
			pagenos=set()
			for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
				interpreter.process_page(page)
			fp.close()
			device.close()
			string = retstr.getvalue()
			retstr.close()

			text_file_path = filename+".txt"
			with open("/tmp/"+text_file_path,'w+') as f:
				f.write(str(string))
			#file.save(os.path.join(app.config['DOWNLOAD_FOLDER'], text_file_path))
			# Cleanup
			#display file
			#flash(filename)
			#animate()
			#flash('File successfully Converted')
			#flash(text)
			return redirect(url_for('uploaded_file', filename=text_file_path))
		else:
			flash('Allowed file types is pdf')
			return redirect(url_for('index'))
	return render_template('index.html')
@app.route('/tmp/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)			

if __name__ == "__main__":
    app.run()