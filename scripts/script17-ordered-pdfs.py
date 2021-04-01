import utils
from os import listdir
from os import rename
from os.path import isfile, join
from slugify import slugify

ordered_index = utils.tsv2dictlist('printable/index-ordered.txt')
print(ordered_index[0])

pdf_path = 'printable/pdf'
pdf_files = listdir(pdf_path)

for i in pdf_files:
    
    id = i.split('_')[1].split('.')[0]

    d = utils.select_dict(ordered_index, {'id': id})[0]
    
    new_name = slugify(d['Chapter'])+'_'+d['order']+'_'+d['id'] +'_' + d['Narrative']+'.pdf'

    print(new_name)

    rename(pdf_path + '/' +i,pdf_path + '/' +new_name)



