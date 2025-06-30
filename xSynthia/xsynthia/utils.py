import os, io, docx, PyPDF2, chardet

def extract_text_from_file(file_stream, filename):
    try:
        extension = os.path.splitext(filename)[1].lower()
        
        # Handle Word documents
        if extension in ('.doc', '.docx'):
            doc = docx.Document(io.BytesIO(file_stream.read()))
            return '\n'.join([para.text for para in doc.paragraphs])
        
        # Handle PDFs
        elif extension == '.pdf':
            reader = PyPDF2.PdfReader(io.BytesIO(file_stream.read()))
            text = '\n'.join([page.extract_text() for page in reader.pages])
            return text
         
        # Handle text files (try UTF-8 first, then fall back to encoding detection)
        elif extension == '.txt':
            try:
                # First try UTF-8
                file_stream.seek(0)
                return file_stream.read().decode('utf-8')
            except UnicodeDecodeError:
                # If UTF-8 fails, detect encoding
                file_stream.seek(0)
                raw_data = file_stream.read()
                result = chardet.detect(raw_data)
                encoding = result['encoding'] or 'utf-8'
                return raw_data.decode(encoding)
        
        # Handle other text-based files with encoding detection
        else:
            raw_data = file_stream.read(1024)
            file_stream.seek(0)
            result = chardet.detect(raw_data)
            encoding = result['encoding'] or 'utf-8'
            text_content = io.TextIOWrapper(file_stream, encoding=encoding).read()
            return text_content
    
    except UnicodeDecodeError:
        return "This file appears to be binary. Only text-based files are supported."
    except Exception as e:
        return f"Error extracting text: {str(e)}"
