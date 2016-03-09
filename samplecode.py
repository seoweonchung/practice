import collections
import csv
import urllib.request

def extractor(head, tail, source):
    if head == '' and tail != '':
        return source[:source.find(tail)]
    elif head != '' and tail == '':
        return source[(source.find(head)+len(head)):]
    else:
        return source[(source.find(head)+len(head)):source.find(tail)]

def tidy(source):
    if '<div class="highlight-box">' in source and '<div class="views-row views-row-1 views-row-odd views-row-first views-row-last full-width">' not in source:
        source = source[source.find('<div class="highlight-box">'):]
        test = source[(source.index('<div class="highlight-box">')+len('<div class="highlight-box">')):source.find('</div>')]
        if "Phone" in test:
            source = source[source.find('<div class="highlight-box">'):]
            source = source[:source.find('</div>')]
        else: 
            source = source[(source.index('<div class="highlight-box">')+len('<div class="highlight-box">')):]
            source = source[source.find('<div class="highlight-box">'):]
            source = source[:source.find('</div>')]
    elif '<div class="views-row views-row-1 views-row-odd views-row-first views-row-last full-width">' in source:
        source = source[source.find('<div class="views-row views-row-1 views-row-odd views-row-first views-row-last full-width">'):]
        source = source[:source.find('<div class="views-field views-field-edit">')]
    else:
        print ("Error: information not found!")
    return source

def splitName(name):
    newName = name.split(' ')
    nameR = []
    if len(newName) == 2:
        nameR.append(newName[0])
        nameR.append(newName[1])
    else:
        nameR.append(newName[0])
        testlist = newName[1].split(',')
        nameR.append(testlist[0])
    return nameR


with open('text.txt', 'r') as myfile:
    text = myfile.read().replace('\n', '')

info = text.split('<div class="views-field views-field-title">')

site = ''
source = ''
program = ''
director = ''
email = ''
phone = ''
temp = ''
testStr = ''
nameF = ''
nameL = ''
test = ''
newDir = []

final_list = []
n = 0


#========================================================== LOOP =============================================================================
for i in range(0, len(info)):
    dict_name = collections.OrderedDict()
    
    #finding program name
    
    text = extractor('<span class="field-content">', '', text)
    
    site = extractor('<a href="', '">', text)
    
    text = extractor(site, '', text)
    text = extractor('">', '', text)
    
    program = extractor('', '</a>', text)
    
    dict_name['program'] = program
    print (program)
    
    #special cases. using n as a variable to check if the loop should run, condition being n!= 1.
    if program == 'Automotive Service Technician (GM-ASEP) [Apprenticeship] - MMA3' :
        n = 1
    elif program == 'Bachelor of Commerce (Digital Marketing) - BDM1':
        n = 1
    elif program == 'Child and Youth Care - CYW4':
        n = 1
    elif program == 'Child and Youth Care (Fast Track) - CYW5':
        n = 1
    elif program == 'Personal Support Worker (Weekend) - PSW9':
        n = 1

    else:
        response = urllib.request.urlopen(site).read()
        source = response.decode('utf-8').replace('\n', '')

        source = tidy(source)
        #start extrating info
        
        if '<h4 class="field-content program-coordinator-title">' in source:
            director = extractor('<h4 class="field-content program-coordinator-title">', '</h4>', source)
            source = extractor('<div class="field-item even" property="content:encoded">', '', source)
        else:
            director = extractor('<p>', '<br />', source)
            source = extractor('<br />', '', source)

        test = source[:3]

#        print (source)
        if test != 'E-m' and test != 'Pho':
            source = extractor('<p>', '', source)
            test = source[:3]
        
        if test == 'E-m':
            email = extractor('<a href="mailto:', '">', source)
            source = extractor('</a>', '', source)
            phone = extractor('Phone: ', '<', source)


        elif test == 'Pho':
            phone = extractor('Phone: ', '<', source)
            email = extractor('<a href="mailto:', '">', source)
            source = extractor('</a>', '', source)

        newDir = splitName(director)
        nameF = newDir[0]
        nameL = newDir[1]
        
        if '<h4 class="field-content program-coordinator-title">' in source:
            source = source[(source.index('</a>')+len('</a>')):source.index('</div>')]
        
            

    if 'Phone' in source or n == 1:
            dict_name['program coordinator'] = ''
            dict_name['email'] = ''
            dict_name['phone'] = ''
            dict_name['nameF'] = ''
            dict_name['nameL'] = ''
            print (source)
            print (' ')
            print (' ')
            print (' ')
            print (' ')
            print (' ')
            print (' ')
    else:
        print (director)
        print (nameF)
        print (nameL)        
        print (email)
        print (phone)
        print (' ')
    
    dict_name['program coordinator'] = director
    dict_name['email'] = email
    dict_name['phone'] = phone
    dict_name['nameF'] = nameF
    dict_name['nameL'] = nameL
    n = 0
    final_list.append(dict_name)
    
I EDITED THIS LINE