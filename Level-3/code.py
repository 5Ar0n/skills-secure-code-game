import os
from flask import Flask, request  

def safe_path(path):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.normpath(os.path.join(base_dir, path))
    if base_dir != os.path.commonpath([base_dir, filepath]):
        return None
    return filepath
    
class TaxPayer:
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.prof_picture = None
        self.tax_form_attachment = None

    def get_prof_picture(self, path=None):
    
        if not path:
            pass
        
        safe_path = safe_path(path)  

        if not safe_path:
            return None
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        prof_picture_path = os.path.normpath(os.path.join(base_dir, path))
    
        with open(prof_picture_path, 'rb') as pic:
            picture = bytearray(pic.read())

        return prof_picture_path

    def get_tax_form_attachment(self, path=None):
        tax_data = None
        
        if not path:
            raise Exception("Error: Tax form is required for all users")
       
        with open(safe_path, 'rb') as form:
            tax_data = bytearray(form.read())

        return path






