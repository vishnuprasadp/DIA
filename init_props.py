##################################################################
#@author: Vishnu Prasad P
#
#
#
#
##################################################################
from SPARQLWrapper import SPARQLWrapper, JSON
import json
import csv

sparql = SPARQLWrapper("http://localhost:8890/sparql")
####################################
#Mapping All Data Property
####################################
sparql.setQuery("""
select distinct *
where
{
?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#DatatypeProperty>.
}
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
with open('dataProperty.csv', mode='w') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(['uri', 'backEnd_Variable', 'frontEnd_Variable'])
    for result in results["results"]["bindings"]:
        try:
            uri,var=((result["s"]["value"]).split('#'))
            csv_writer.writerow([result["s"]["value"], var, ''])
        except:
            uri=((result["s"]["value"]))
            var=''
            csv_writer.writerow([uri, var, ''])



####################################
#Mapping All Object Property
####################################
sparql.setQuery("""
select distinct *
where
{
?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#ObjectProperty>.
}
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
with open('objectProperty.csv', mode='w') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(['uri', 'backEnd_Variable', 'frontEnd_Variable'])
    for result in results["results"]["bindings"]:
        try:
            uri,var=((result["s"]["value"]).split('#'))
            csv_writer.writerow([result["s"]["value"], var, ''])
        except:
            uri=((result["s"]["value"]))
            var=''
            csv_writer.writerow([uri, var, ''])


####################################
#Mapping All Classes
####################################
sparql.setQuery("""
select distinct *
where
{
?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#Class>.
}
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
with open('owlclasses.csv', mode='w') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(['uri', 'backEnd_Variable', 'frontEnd_Variable'])
    for result in results["results"]["bindings"]:
        try:
            uri,var=((result["s"]["value"]).split('#'))
            csv_writer.writerow([result["s"]["value"], var, ''])
        except:
            uri=((result["s"]["value"]))
            var=''
            csv_writer.writerow([uri, var, ''])