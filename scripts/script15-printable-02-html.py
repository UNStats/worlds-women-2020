
from yattag import Doc
from yattag import indent
import sys
import os
import copy
import json
import utils
import re

from selenium import webdriver
from bs4 import BeautifulSoup


import pdfkit 

last_url = None

options = {
  "enable-local-file-access": None,
  'page-size': 'Letter',
    'margin-top': '1.25in',
    'margin-right': '1in',
    'margin-bottom': '0.75in',
    'margin-left': '1.25in',
    'image-dpi' : '850',
    'footer-font-size': '8',
    'header-font-size': '8',
    'header-right': 'World\'s Women 2020',
    'footer-line': None,
    'footer-right': 'Statistics Division',
    'footer-left': 'United Nations Department of Economic and Social Affairs',
}

graph_count = 1

json_dir = 'printable/json/'
data_files = os.listdir('printable/json/')
#print(data_files)

for item in data_files:


    if item != '022ab89e10d04700901ced2a133eda86.json':
        continue

    with open('printable/json/' + item) as json_file:
        d = json.load(json_file)

    theme = d['values']['title']
    print('-----------')
    print(theme)
    print('-----------')

    sections = d['values']['story']['sections']

    doc, tag, text = Doc().tagtext()
    
    doc.asis('<!DOCTYPE html>')
    with tag('html', lang = 'en'):
        with tag('head'):
            doc.stag('meta', charset='utf-8')
            with tag('title'):
                text(theme)
            doc.stag('meta', name='viewport', content='width=device-width, initial-scale=1')
            doc.stag('link', href='https://fonts.googleapis.com/css?family=Raleway:400,300,600', rel='stylesheet', type='text/css')

            doc.stag('link', href='css/normalize.css', rel='stylesheet', type='text/css')
            doc.stag('link', href='css/skeleton.css', rel='stylesheet', type='text/css')
            doc.stag('link', href='css/custom.css', rel='stylesheet', type='text/css')

            
        with tag('body'):
            with tag('div', klass='container'):
                with tag('div', klass='row'):
                    
                    for i, s in enumerate(sections):
                        soup1 = BeautifulSoup(s['title'], features='html.parser')
                        soup2 = BeautifulSoup(s['content'], features='html.parser')

                        footnotes = soup2.findAll('span', {'class' : 'footnote-index'})

                        for fn in footnotes:
                            if fn.a:
                                fn.a.unwrap()

                        if i == 0:
                            title = soup2.find('div', attrs={'class': 'title'}).string
                            title = str(title).replace('&nbsp;', '')
                            title = title.replace(u'\u00A0', '')

                            with tag('h5'):
                                text(theme)
                            with tag('h1'):
                                with tag('a', href='https://worlds-women-2020-data-undesa.hub.arcgis.com/app/' + item.replace('.json','')):
                                    text(title)
                        else:
                            subtitle = soup1.get_text()
                            
                            subtitle = str(subtitle).replace('&nbsp;', '')
                            subtitle = subtitle.replace(u'\u00A0', '')

                            content = str(soup2).replace('⇡','&#8673;')
                            content = content.replace(u'\u00a0', ' ')
                            content = content.replace(u'\u2013', '&ndash;')
                            content = content.replace(u'\u201c', '&#8220;')
                            content = content.replace(u'\u201d', '&#8221;')
                            content = content.replace(u'\u2019', '&#8217;')
                            content = content.replace(u'\u2014', '&#8212;')
                            print(content)
                            

                            content = re.sub(r'\(<a(.*?)back to text</a>\)', "", content)
                            content = content.replace('(&#8673; back to text)', '')

                            with tag('div', klass='page'):
                                doc.stag('br')
                                with tag('h4'):
                                    text(subtitle)
                                with tag('div', klass='content'):
                                    doc.asis(content)
                                
                        media = s['media']
                        
                        if media['type'] == 'webpage':
                            url = media['webpage']['url']
                            
                            if url != last_url:
                                
                                graph_count += 1

                                driver = webdriver.Chrome('C:/Users/LGONZALE20/Downloads/chromedriver.exe')
                                driver.get(url)
                                driver.execute_script('document.body.style.zoom = "85%"')
                                screenshot = driver.save_screenshot('printable/img/image_'+ str(graph_count) +'.png')
                                
                                image_file = '../img/image_'+ str(graph_count) +'.png'
                                print(image_file)
                                driver.quit()

                                doc.stag('img', src=image_file, width='800')
                            
                            last_url = url

                        if media['type'] == 'image':
                            url = media['image']['url']
                            
                            if url != last_url:
                                if i == 0:
                                    doc.stag('img', src=url, height='600')
                                if i > 1:
                                    doc.stag('img', src=url, style='height:400px;max-width:500px;width: expression(this.width > 500 ? 500: true);')

                            last_url = url

    result = doc.getvalue()
    
    filename = 'printable/html/' + item.replace('.json','') + '.html'

    
    original_stdout = sys.stdout # Save a reference to the original standard output

    with open(filename, 'w') as f:
        sys.stdout = f # Change the standard output to the file we created.
        print(result)
        sys.stdout = original_stdout # Reset the standard output to its original value

    


    pdfkit.from_file(filename,  'printable/pdf/' + item.replace('.json','') + '.pdf', options=options) 
