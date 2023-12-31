import os
import sys
import shutil


def translate(name):
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = (
        "a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
        "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
    TRANS = {}
    for symbol in range(len(CYRILLIC_SYMBOLS)):
        TRANS.update({ord(CYRILLIC_SYMBOLS[symbol]): TRANSLATION[symbol]})
        TRANS.update({ord(CYRILLIC_SYMBOLS[symbol].upper()): TRANSLATION[symbol].upper()})
    name = name.translate(TRANS)
    return name

#changes cyrillic symbols to latin
def normalize(path_to_folder) -> None:
    for filename in os.listdir(path_to_folder):
        original_name = os.path.join(path_to_folder,filename)
        new_name = os.path.join(path_to_folder,translate(filename))
        os.rename(original_name, new_name)

#deletes empty folders
def delete_empty_folders(directory):
    ignore_folders = ['archives', 'images','video','documents','audio']
    for root, dirs, files in os.walk(directory, topdown=False):
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            if not os.listdir(folder_path) and not str(folder) in ignore_folders:  # Check if the folder is empty
                os.rmdir(folder_path)

#name of destination folder for the file
def dst_folder(filename):
    extensions = {"images": ['JPEG', 'PNG', 'JPG', 'SVG'], 'video': ['AVI', 'MP4', 'MOV', 'MKV'],
                  'documents': ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'], 'audio': ['MP3', 'OGG', 'WAV', 'AMR'],
                  'archives': ['ZIP', 'GZ', 'TAR']}
    for key in extensions:
        for value in extensions[key]:
            if filename.upper().endswith('.' + value):
                return key

#Moving files to appropriate directories
def move_folders(directory):
    for item in os.listdir(directory):
        if not os.path.isdir(os.path.join(directory,item)):
            src = os.path.join(directory,item)
            if dst_folder(item) is not None:
                dst = os.path.join(directory,dst_folder(item))
                #unzipping archives
                if item.endswith(('.zip', '.gz', '.tar')):
                    shutil.unpack_archive(src, os.path.join(directory,'archives'))
                    os.remove(src)
                else:
                    shutil.move(src,dst)
        if os.path.isdir(os.path.join(directory,item)) and item!='video':
            move_folders(os.path.join(directory,item))

#main sorting function
def sorting(directory):
    normalize(directory)
    # creating necessary directories
    ignore_folders = ['archives', 'images', 'video', 'documents', 'audio']
    for folder in ignore_folders:
        if not os.path.exists((os.path.join(directory, folder))):
            os.mkdir(os.path.join(directory, folder))

    #Moving files to appropriate directories
    move_folders(directory)
    #deleting of empty folders
    delete_empty_folders(directory)
def run():
    try:
        path = input('Provide a path to directory:')
        sorting(path)
    except IndexError:
        print("Directory was not provided")

if __name__ == '__main__':
    run()
