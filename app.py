import os
#import magic
import re
import urllib.request
from dir_addr import app
from flask import Flask, flash, request, redirect, render_template,url_for
from werkzeug.utils import secure_filename
from pdfminer.pdfinterp import PDFResourceManager#, PDFPage.get_pages()
from pdfminer.converter import TextConverter
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter#process_pdf
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams
import os
#import converter
import csv
import io


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

download_Dir=[]
filename1=[]
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/uploader', methods=['POST'])
def upload_file():
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
			flash(filename)
			filename1.append(filename)
			flash('File successfully uploaded')
			value = os.path.join('/tmp', filename)
			#return('done')
			download_Dir.append(value)
			#print(value1)
			return redirect(url_for('index'))
		else:
			flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
			return redirect(url_for('index'))

#path=os.path.join(app.config['UPLOAD_FOLDER'], 'ANKIT_SINGH_TECH_INTERN.pdf')
@app.route('/convert/')
def convert():#pdfname para
		# PDFMiner boilerplate
		rsrcmgr = PDFResourceManager()
		sio = StringIO()
		laparams = LAParams()
		device = TextConverter(rsrcmgr, sio,  laparams=laparams)
		interpreter = PDFPageInterpreter(rsrcmgr, device)

		# Extract text
		#fp = open('/home/greeneye/Documents/upload/ANKIT_SINGH_TECH_INTERN.pdf', 'rb')
		pdf_file = "/tmp/" + filename1[0]
		fp = open(pdf_file,'rb')
		for page in PDFPage.get_pages(fp):
			interpreter.process_page(page)
		fp.close()

		# Get text from StringIO
		text = sio.getvalue().encode("ascii", "ignore")
		text_file_name = "/tmp/downoad.txt"
		with open(text_file_name,'w') as f:
			f.write(str(text))
			
		# Cleanup
		device.close()
		sio.close()
		flash(text)
		os.unlink('/tmp')
		return redirect(url_for('index'))
			
if __name__ == "__main__":
    app.run(debug=True)