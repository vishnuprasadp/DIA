from SPARQLWrapper import SPARQLWrapper, JSON ,XML , POST, DIGEST
import json

sparql = SPARQLWrapper("http://localhost:8890/sparql")
sparql.addDefaultGraph("http://www.Gokdepartments.org")

def selDeptList():
    sparql.setQuery("""
        SELECT *
        {?Org <http://www.w3.org/ns/org#Name> ?name.
        ?Org <http://www.w3.org/ns/org#DepartmentID> ?ID.}
        """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    dept=[]
    for result in results["results"]["bindings"]:
       dept.append({
            'name': result["name"]["value"],
            'id': result["ID"]["value"]
        })  
    return (json.dumps(dept))

def selDeptDetail(deptId):
    sparql.setQuery("""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>	
        PREFIX org: <http://www.w3.org/ns/org#>
        SELECT ?name ?ID ?altname ?location ?url ?phone ?mail ?pincode ?addresse 
        where
        {
        ?d rdf:type <http://www.w3.org/ns/org#FormalOrganization>.
        ?d org:Name ?name.
        ?d org:DepartmentID ?ID.
        ?d org:Telephone ?phone.
        ?d org:Address ?addresse.
        ?d org:hasSite ?location.
        ?d org:PostalCode ?pincode.
        ?d org:AdditionalDepartmentName	?altname.
        ?d org:URL ?url.
        ?d org:Email ?mail.
        ?d org:DepartmentID """+deptId+"""
        }
        """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    # print(results)
    dept=[]
    for result in results["results"]["bindings"]:
        dept=({
                'name': result["name"]["value"],
                'id': result["ID"]["value"],
                'altname': result["altname"]["value"],
                'location': result["location"]["value"],
                'url': result["url"]["value"],
                'phone': result["phone"]["value"],
                'mail': result["mail"]["value"],
                'pincode': result["pincode"]["value"],
                'addresse': result["addresse"]["value"],
                'schemes':[],
                'posts':[],
                'units':[],
            })
        
    #posts
    sparql.setQuery("""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>	
        PREFIX org: <http://www.w3.org/ns/org#>
        SELECT ?name ?email ?des 
        where
        {
        ?d rdf:type <http://www.w3.org/ns/org#FormalOrganization>.
        ?d <http://www.w3.org/ns/org#hasPost> ?post.
        ?post <http://www.w3.org/ns/org#Name> ?name.
        ?post <http://www.w3.org/ns/org#Email> ?email.
        ?post <http://www.w3.org/ns/org#Description> ?des.
        ?d org:DepartmentID """+deptId+""" 
        }
        """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    # print(results)
    for result in results["results"]["bindings"]:
        dept.get("posts").append({"postName": result["name"]["value"],"email": result["email"]["value"],"description": result["des"]["value"]})

    #Schemes        
    sparql.setQuery("""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>	
        PREFIX org: <http://www.w3.org/ns/org#>
        SELECT ?name ?startdate ?enddate
        where
        {
        ?d rdf:type <http://www.w3.org/ns/org#FormalOrganization>.
        ?d <http://www.w3.org/ns/org#hasSchemes> ?schemes.
        ?schemes <http://www.w3.org/ns/org#Name> ?name.
        ?schemes <http://www.w3.org/ns/org#StartDate> ?startdate.
        ?schemes <http://www.w3.org/ns/org#EndDate> ?enddate.
        ?d org:DepartmentID """+deptId+""" 
        }
        """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    for result in results["results"]["bindings"]:
        dept.get("schemes").append({"schemeName": result["name"]["value"],"startDate": result["startdate"]["value"],"endDate": result["enddate"]["value"]})

    #units        
    sparql.setQuery("""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>	
        PREFIX org: <http://www.w3.org/ns/org#>
        SELECT ?name ?id ?altname ?location ?email 
        where
        {
        ?d rdf:type <http://www.w3.org/ns/org#FormalOrganization>.
        ?d <http://www.w3.org/ns/org#hasSubOrganization> ?units.
        ?units <http://www.w3.org/ns/org#Name> ?name.
        ?units <http://www.w3.org/ns/org#DepartmentID> ?id.
        ?units <http://www.w3.org/ns/org#AdditionalDepartmentName> ?altname.
        ?units <http://www.w3.org/ns/org#hasSite> ?location.
        ?units <http://www.w3.org/ns/org#Email> ?email.
        ?d org:DepartmentID """+deptId+""" 
        }
        """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    for result in results["results"]["bindings"]:
        dept.get("units").append({"unitName": result["name"]["value"],"unitId": result["id"]["value"],"altUnitName": result["altname"]["value"],"location": result["location"]["value"],"email": result["email"]["value"]})        
    print(dept)
    return(dept)

def enterDept(deptDeatail):
    data=deptDeatail
    print(data)
    sparql.setHTTPAuth(DIGEST)
    sparql.setCredentials("dba", "dba")
    sparql.setMethod(POST)

    sparql.setQuery("""
        SELECT COUNT(*)
    WHERE{
    ?d <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/ns/org#FormalOrganization>.
    }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    for result in results["results"]["bindings"]:
        idd=result["callret-0"]["value"]
    
    sparql.setQuery("""
    PREFIX org:  <http://www.w3.org/ns/org>
    INSERT DATA
      { 
        GRAPH <http://www.Gokdepartments.org> 
          { 
            <http://www.w3.org/ns/org#d"""+idd+"""> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#NamedIndividual>.
            <http://www.w3.org/ns/org#d"""+idd+"""> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/ns/org#FormalOrganization>.
            <http://www.w3.org/ns/org#d"""+idd+"""> <http://www.w3.org/ns/org#hasSite>\""""+ data["location"]+"""\".
            <http://www.w3.org/ns/org#d"""+idd+"""> <http://www.w3.org/ns/org#AdditionalDepartmentName>\""""+data["altname"]+"""\".
            <http://www.w3.org/ns/org#d"""+idd+"""> <http://www.w3.org/ns/org#Address>\""""+data["address"]+"""\".
            <http://www.w3.org/ns/org#d"""+idd+"""> <http://www.w3.org/ns/org#DepartmentID>"""+'"'+""""""+idd+""""""+'"'+"""^^<http://www.w3.org/2001/XMLSchema#int>.
            <http://www.w3.org/ns/org#d"""+idd+"""> <http://www.w3.org/ns/org#Email>\""""+data["mail"]+"""\".
            <http://www.w3.org/ns/org#d"""+idd+"""> <http://www.w3.org/ns/org#Name>\""""+data["name"]+"""\".
            <http://www.w3.org/ns/org#d"""+idd+"""> <http://www.w3.org/ns/org#PostalCode>\""""+str(data["pincode"])+"""\".
            <http://www.w3.org/ns/org#d"""+idd+"""> <http://www.w3.org/ns/org#Telephone>\""""+data["phone"]+"""\".
            <http://www.w3.org/ns/org#d"""+idd+"""> <http://www.w3.org/ns/org#URL>\""""+data["url"]+"""\".     
          } 
      }
    """)
    results = sparql.query()
    sparql.setQuery("""
    SELECT COUNT(*)
    WHERE{
    ?d <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/ns/org#Post>.
    }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    #print(results)
    for result in results["results"]["bindings"]:
        iddp=result["callret-0"]["value"]
    
    # print(results)
    for post in data["posts"]:
        print (post["postName"],post["description"],post["email"])
        sparql.setQuery("""
        PREFIX org:  <http://www.w3.org/ns/org>
        INSERT DATA
          { 
            GRAPH <http://www.Gokdepartments.org> 
              { 
                <http://www.w3.org/ns/org#p"""+iddp+"""> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#NamedIndividual>.
                <http://www.w3.org/ns/org#p"""+iddp+"""> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/ns/org#Post>.
                <http://www.w3.org/ns/org#d"""+idd+"""> <http://www.w3.org/ns/org#hasPost> <http://www.w3.org/ns/org#p"""+iddp+""">.
                <http://www.w3.org/ns/org#p"""+iddp+"""> <http://www.w3.org/ns/org#Email>\""""+post["email"]+"""\".
                <http://www.w3.org/ns/org#p"""+iddp+"""> <http://www.w3.org/ns/org#Name>\""""+post["postName"]+"""\".
                <http://www.w3.org/ns/org#p"""+iddp+"""> <http://www.w3.org/ns/org#Description>\""""+post["description"]+"""\".     
              } 
          }
        """)
        results = sparql.query()
        iddp=str(int(iddp)+1)
    
    sparql.setQuery("""
    SELECT COUNT(*)
    WHERE{
    ?d <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/ns/org#Schemes>.
    }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    #print(results)
    for result in results["results"]["bindings"]:
        idds=result["callret-0"]["value"]
           
    for scheme in data["schemes"]:
        print (scheme["schemeName"],scheme["startDate"],scheme["endDate"])
        sparql.setQuery("""
        PREFIX org:  <http://www.w3.org/ns/org>
        INSERT DATA
          { 
            GRAPH <http://www.Gokdepartments.org> 
              { 
                <http://www.w3.org/ns/org#s"""+idds+"""> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#NamedIndividual>.
                <http://www.w3.org/ns/org#s"""+idds+"""> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/ns/org#Schemes>.
                <http://www.w3.org/ns/org#d"""+idd+"""> <http://www.w3.org/ns/org#hasSchemes> <http://www.w3.org/ns/org#s"""+idds+""">.
                <http://www.w3.org/ns/org#s"""+idds+"""> <http://www.w3.org/ns/org#Name>\""""+scheme["schemeName"]+"""\".
                <http://www.w3.org/ns/org#s"""+idds+"""> <http://www.w3.org/ns/org#EndDate>\""""+scheme["endDate"]+"""\".
                <http://www.w3.org/ns/org#s"""+idds+"""> <http://www.w3.org/ns/org#StartDate>\""""+scheme["startDate"]+"""\".     
              } 
          }
        """)
        results = sparql.query()
        idds=str(int(idds)+1)
        
    
    sparql.setQuery("""
    SELECT COUNT(*)
    WHERE{
    ?d <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/ns/org#FormalOrganization>.
    }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    for result in results["results"]["bindings"]:
        iddu=result["callret-0"]["value"]
     
    for unit in data["units"]:
        print (unit["unitName"],unit["unitId"],unit["altUnitName"],unit["location"],unit["email"],unit["linkedTo"])
        sparql.setQuery("""
        PREFIX org:  <http://www.w3.org/ns/org>
        INSERT DATA
          { 
            GRAPH <http://www.Gokdepartments.org> 
              { 
                <http://www.w3.org/ns/org#d"""+iddu+"""> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#NamedIndividual>.
                <http://www.w3.org/ns/org#d"""+iddu+"""> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/ns/org#FormalOrganization>.
                <http://www.w3.org/ns/org#d"""+idd+"""> <http://www.w3.org/ns/org#hasSubOrganization> <http://www.w3.org/ns/org#d"""+iddu+""">.
                <http://www.w3.org/ns/org#d"""+iddu+"""> <http://www.w3.org/ns/org#hasSite>\""""+unit["location"]+"""\".
                <http://www.w3.org/ns/org#d"""+iddu+"""> <http://www.w3.org/ns/org#AdditionalDepartmentName>\""""+unit["altUnitName"]+"""\".
                <http://www.w3.org/ns/org#d"""+iddu+"""> <http://www.w3.org/ns/org#DepartmentID>"""+'"'+""""""+iddu+""""""+'"'+"""^^<http://www.w3.org/2001/XMLSchema#int>.
                <http://www.w3.org/ns/org#d"""+iddu+"""> <http://www.w3.org/ns/org#Email>\""""+unit["email"]+"""\".
                <http://www.w3.org/ns/org#d"""+iddu+"""> <http://www.w3.org/ns/org#Name>\""""+unit["unitName"]+"""\".     
              } 
          }
        """)
        results = sparql.query()
        iddu=str(int(iddu)+1)



