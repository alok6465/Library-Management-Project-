from flask import Flask, render_template, request, send_file, jsonify
import pandas as pd
import os
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file selected'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'})
    
    if file and (file.filename.endswith('.xlsx') or file.filename.endswith('.csv')):
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Read file data
        try:
            if filename.endswith('.xlsx'):
                df = pd.read_excel(filepath)
            else:
                df = pd.read_csv(filepath)
            
            # Convert to HTML table
            table_html = df.to_html(classes='table table-striped table-hover', table_id='dataTable', escape=False)
            
            return jsonify({
                'success': True,
                'table': table_html,
                'filename': filename,
                'rows': len(df),
                'columns': len(df.columns)
            })
        except Exception as e:
            return jsonify({'error': f'Error reading file: {str(e)}'})
    
    return jsonify({'error': 'Invalid file format. Only .xlsx and .csv files are allowed.'})

@app.route('/download_pdf', methods=['POST'])
def download_pdf():
    filename = request.json.get('filename')
    search_term = request.json.get('search', '')
    
    if not filename:
        return jsonify({'error': 'No filename provided'})
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    try:
        # Read file
        if filename.endswith('.xlsx'):
            df = pd.read_excel(filepath)
        else:
            df = pd.read_csv(filepath)
        
        # Apply search filter if provided
        if search_term:
            mask = df.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
            df = df[mask]
        
        # Create PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        
        # Add title
        styles = getSampleStyleSheet()
        title = Paragraph(f"Data from {filename}", styles['Title'])
        elements.append(title)
        
        # Convert DataFrame to table data
        data = [df.columns.tolist()] + df.values.tolist()
        
        # Create table
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        doc.build(elements)
        
        buffer.seek(0)
        pdf_filename = f"{filename.split('.')[0]}_data.pdf"
        
        return send_file(
            buffer,
            as_attachment=True,
            download_name=pdf_filename,
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({'error': f'Error generating PDF: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True, port=5001)