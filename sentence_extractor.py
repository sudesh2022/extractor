# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 16:24:50 2024

@author: PrachiRani1
"""

import fitz
import re
import csv


def preprocessing_doc_content(doc_content):
    statement_list = []
    try:
        doc_content = re.sub('[\n]+', '.', doc_content)
        doc_content = re.sub('[\t]+', '', doc_content)
        doc_content=re.sub("\(.*?\)","",doc_content)
        doc_content_list = re.split('[.;]',doc_content)    
        for statement in doc_content_list:
            statement=re.sub(".*?\)","",statement)
            if len(statement) > 30:
                # print("Statement:",statement)
                statement_list.append(statement)
    except:
        print("error in pre-processing text")
    return statement_list

#output_path = 'op.csv'
output_path = 'outputfiles/sentence_split.csv'
text = ""
keywords_list = [[  "Development", "Secure","Software","Custom Secure Development","Client Secure Development","SLA", "SLO", "KPI", "Metrics", "Measurements","Emergency changes", "release management", "code management", "code promotion", "application testing and promotion", "client support"],
[  "Sec Config", "Hardening", "Harden", "Benchmark", "Config", "Configured", "Maintenance or Administrative of responsibilities for an Asset","Administrative of responsibilities for an Asset","Maintenance of responsibilities for an Asset","Image and configuration hardening and validation", "password and access configuration", "protection from malicious code, hacks, and attacks", "firewall rules and revalidations", "remote connectivity controls and configurations", "application code integrity and protection", "secure engineering", "licensing","Land Scape", "SDLC","Password policy"],
[  "user ids", "API keys", "Shared User ID", "Individual User ID Management", "Least Privilege and Privilege Management", "Separation of Duties", "SOD", "Business Need", "Timely Removal", "ID Auth", "Identification", "Authentication", "Authenticate", "Access", "Authorize", "Authorized", "Username", "Password", "Factor", "Token", "Secret", "Duties", "Role","Termination", "OffBoarding","OffBoarding","privileged assess"],
[  "Integrity", "Privacy", "Protection", "Retention", "Reuse", "Direct Data Updates","Data Movement", "secure data restore", "DDUs", "Encryption", "Encrypted", "Encrypt", "Erase", "Erasure", "Dispose","Disposal","Residual","Retain","Access Log", "Monitoring", "Logging", "Compliance", "Guidelines", "Requirements","leak"],
[  "Inventory", "Asset", "Track", "Classification", "Label", "Reconciliation", "Reconcile", "Sensitive", "Reside", "Access", "PI/SPI/BSI", "Inventory Owner","Acceptable Use Policy"],
[  "Security Testing", "Code Scan", "Penetration Test", "Vulnerability Management", "Technical Testing", "TCP/IP","Application scans", "remediation of vulnerabilities"],
[  "Endpoint", "Endpoint", "End point", "Mobile", "iOS", "iPhone", "Android", "Windows", "Laptop", "Workstation", "Training","workplace security"],
[ "Network Security",  "Segregation", "Segregated", "Ingress", "Egress", "Firewall", "Rule", "Ruleset","Route", "Router", "IP", "VLAN", "Boundary", "Proxy", "Transit", "Diagram"],
[ "Container Security", "Container","Docker","Kubernettes","Node","Cluster","Pod"]]
#auditAreaList =  ["Integrated Service Management","System and Application Configuration","Identification and Access Management","Data Integrity and Protection","Inventory Management","Security Assessment","Media Protection","Network Security","Container Security"]
auditAreaList = ["Is System and Application configuration in scope ?",
"Is Identification and Access management in scope ?",
"Is Data Integrity and Protection in scope ?",
"Is Inventory Management in scope ?",
"Is Integrated Service Management in scope ?",
"Is Security Assessment in scope ?",
"Is Media Protection in scope ?",
"Is Network security in scope ?",
"Is Container security in scope ?",
"Is Patch Management in scope ?",
"Is Endpoint Security in scope ?"]
#keywords_list = [["hardware","data center"],['software','testing']]
#path = r"C:\Users\0036LE744\Downloads\MLS-C01-demo.pdf"
path = "auditfiles/document_2.pdf"

with fitz.open(path) as doc: 
    # print("testing",doc)   
    for page in doc:
        text += page.get_text()
statements = preprocessing_doc_content(text)
# print("statements",statements)

result = {'auditarea':[],'keywords':[], 'sentences':[]}
for auditarea in auditAreaList:
    for keyword_sublist in keywords_list:
        keywords_append = ""
        sentence_append = ""
        sentence_seq = 0
        # for sentence in statements:
        for j in range(len(keyword_sublist)):
            for i in range(len(statements)):
                if keyword_sublist[j].lower() in statements[i].lower():
                    sentence_seq += 1
                    sentence_append = str(sentence_seq)+ ". " + statements[i] + '\n' + sentence_append
                if i+1 == len(statements):
                    keywords_append = keyword_sublist[j] + "," + keywords_append
            if j + 1 == len(keyword_sublist):
                result['sentences'].append(sentence_append)
                result['keywords'].append(keywords_append)         
    result['auditarea'].append(auditarea)           
    cols = zip(result['auditarea'],result['keywords'], result['sentences'])
    with open(output_path, "w") as f:
        writer = csv.writer(f)    
        writer.writerow(("Audit Areas","Keywords", "Sentences"))
        writer.writerows(cols)
    f.close()
