from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from datetime import datetime
from PyPDF2 import PdfReader, PdfWriter
import pdfplumber
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///deeppdf.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

UPLOAD_FOLDER = 'static/uploads'
SORT_FOLDER = 'static/sorted_pdf'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)


class PdfSave(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pdf_name = db.Column(db.String(200), nullable=False)


with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def upload_pdf():

    if request.method == 'POST':

        pdf = request.files['pdf']

        if pdf:

            filename = secure_filename(pdf.filename)

            pdf_path = os.path.join(
                app.config['UPLOAD_FOLDER'],
                filename
            )

            pdf.save(pdf_path)

            reader = PdfReader(pdf_path)

            couriers = {}

            with pdfplumber.open(pdf_path) as pdf_file:

                for i, page in enumerate(pdf_file.pages):

                    text = page.extract_text()

                    text = text.lower()

                    if 'valmoplus' in text:
                        courier_name = 'ValmoPlus'
                    
                    elif 'valmo' in text:
                        courier_name = 'Valmo'
                    
                    elif 'delhivery' in text:
                        courier_name = 'Delhivery'
                    
                    elif 'xpress bees' in text:
                        courier_name = 'XpressBees'
                    
                    elif 'shadowfax' in text:
                        courier_name = 'Shadowfax'
                    
                    else:
                        courier_name = 'Unknown'

                    if courier_name not in couriers:
                            couriers[courier_name] = PdfWriter()

                    couriers[courier_name].add_page(
                            reader.pages[i]
                        )

            # Save PDFs
            sorted_files = []

            for courier, writer in couriers.items():
                current_time = datetime.now().strftime('%d-%m-%Y_%H-%M-%S')
                output_filename = f'{courier}_{current_time}.pdf'

                output_path = os.path.join(
                    'static/sorted_pdf',
                    output_filename
                )

                with open(output_path, 'wb') as output_pdf:
                    writer.write(output_pdf)

                sorted_files.append(output_filename)

            return render_template(
                'uploadpdf.jinja',
                files=sorted_files
            )

    return render_template('uploadpdf.jinja')

@app.route('/old_pdf')
def old_pdf():

    all_pdfs = os.listdir(SORT_FOLDER)

    return render_template(
        'old_pdf.jinja',
        files=all_pdfs
    ) 
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)