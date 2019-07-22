import csv
import os

class dataProperty():
    allowed_methods=[]

    def __init__(self, uri, var ,fe_var):
        self.uri = uri
        self.var = var
        self.fe_var = fe_var
        dataProperty.allowed_methods.append(fe_var)

    def dp_uri(self):
        return(self.uri)

class objectProperty():
    allowed_methods=[]
    
    def __init__(self, uri, var ,fe_var):
        self.uri = uri
        self.var = var
        self.fe_var = fe_var
        objectProperty.allowed_methods.append(fe_var)

class owlclass():
    allowed_methods=[]
    
    def __init__(self, uri, var ,fe_var):
        self.uri = uri
        self.var = var
        self.fe_var = fe_var
        owlclass.allowed_methods.append(fe_var)

