import os
from deal_with_files.vecDB import vectorize

location_map = {
    'desktop': r'C:\Users\Hp\Desktop',
    'code folder': r'C:\Users\Hp\Desktop\Code',
    'college folder': r'C:\Users\Hp\Desktop\College',
    'downloads': r'C:\Users\Hp\Downloads'
}

def location_translate(location):
    return location_map.get(location.lower(), None)

def deal_with_query(query) : 
    count = 0
    temp_index = 0
    words = query.lower().split()
    
    for i, word in enumerate(words):
        if word == "open" or word == 'read':
            start_ind = i+2
            if i + 1 < len(words):
                file_type = words[i + 1]
        elif word == 'located':
            file_name = '_'.join(words[start_ind: i])
            if i + 2 < len(words):
                folder_name = location_translate(' '.join(words[i + 2:]))
            else : 
                folder_name = location_translate('desktop')
    
    if file_name and folder_name:
        path = folder_name + f"\{file_name}.{file_type}"
    print(path)  
    if path and 'open' in query:
        if os.path.exists(path):
            os.startfile(path)
        else:
            print(f"File not found: {path}")

    vectorize(path)

if __name__ == "__main__":
    deal_with_query('Jarvis open pdf offer letter located in Code folder')
    #Jarvis open pdf offer letter in Code folder
