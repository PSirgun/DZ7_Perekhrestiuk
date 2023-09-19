from pathlib import Path
import shutil
import sys


TRANSLIT_DICT = {
    ord("а"): "a", ord("б"): "b", ord("в"): "v", ord("г"): "g", ord("д"): "d", ord("е"): "e", ord("є"): "ie", ord("ж"): "zh", ord("з"): "z",
    ord("и"): "i", ord("і"): "i", ord("ї"): "ji", ord("й"): "j", ord("к"): "k", ord("л"): "l", ord("м"): "m", ord("н"): "n", ord("о"): "o",
    ord("п"): "p", ord("р"): "r", ord("с"): "s", ord("т"): "t", ord("у"): "u", ord("ф"): "f", ord("х"): "h", ord("ц"): "c", ord("ч"): "ch",
    ord("ш"): "sh", ord("щ"): "shch", ord("ь"): " ", ord("ю"): "ju", ord("я"): "ja",
    ord("А"): "A", ord("Б"): "B", ord("В"): "V", ord("Г"): "G", ord("Д"): "D", ord("Е"): "E", ord("Є"): "Ye", ord("Ж"): "Zh", ord("З"): "Z",
    ord("И"): "I", ord("І"): "I", ord("Ї"): "Ji", ord("Й"): "J", ord("К"): "K", ord("Л"): "L", ord("М"): "M", ord("Н"): "N", ord("О"): "O",
    ord("П"): "P", ord("Р"): "R", ord("С"): "S", ord("Т"): "T", ord("У"): "U", ord("Ф"): "F", ord("Х"): "H", ord("Ц"): "C", ord("Ч"): "Ch",
    ord("Ш"): "Sh", ord("Щ"): "Shch", ord("Ь"): " ", ord("Ю"): "Ju", ord("Я"): "Ja"
}  

all_known_ext  = { 'documents' : ['.DOC', '.DOCX', '.TXT', '.PDF', '.XLSX', '.PPTX'], 
'images' : ['.JPEG', '.PNG', '.JPG', '.SVG', '.BMP'], 
'audio' : ['.MP3', '.OGG', '.WAV', '.AMR'],
'video' : ['.AVI', '.MP4', '.MOV', '.MKV'],
'archives' : ['.ZIP', '.GZ', '.TAR'] 
}
unknown_ext_set = set()
known_ext_set = set()
known_ext_dict = {}

cpf = {} # count peremishchenna fajliv - потрібен для перейменування файлів з однаковими іменами, для кожної окремої папки буде починатися свій відлік,
# якщо у різних папках зовсім різні файли з однаковим іменем для прикладу (Документ Microsoft Word.docx). в одному може бути реферат а в іншому перелік покупок ))
def dz6():
    try:
        folder_path = Path(sys.argv[1])  
    except IndexError:
        print("Не введено шляху")
        return  
    if not folder_path.exists():
        print ("Шляху до папки не існує")
        return 
    else:

        def normalize(obj:Path):    #в завданні сказано що функція повинна приймати рядок, але мені здається так зручніше, хоча якщо потрібно то можна і рядок.
            lat_obj = obj.stem.translate(TRANSLIT_DICT)  
            lat_obj = ''.join(char if char.isalnum() else '_' for char in lat_obj) + obj.suffix
            return lat_obj
    

        def sort(obj:Path):  
            for folder_name, extensions in all_known_ext.items():
                if obj.suffix.upper() in extensions:
                    if folder_name not in known_ext_dict:
                        known_ext_dict[folder_name] = []
                    known_ext_set.add(obj.suffix)
                    return folder_name
            
            unknown_ext_set.add(obj.suffix.upper())
            return "others"


        def moving_files(obj:Path, folder_path:Path, new_folder:str):
            global cpf
            dest_folder = Path(folder_path).joinpath(new_folder) 

            if not dest_folder.exists():
                dest_folder.mkdir()  
                cpf[new_folder] = 1
            
            normalize_z = normalize(obj)  
            way1 = dest_folder.joinpath(normalize_z)
            way2 = dest_folder.joinpath(str(cpf.get(new_folder)) + normalize_z) # поробив змінні щоб кожного разу не виконувало одну і ту ж функцію 
            
            if not way1.exists():
                shutil.move(obj, way1)                                            # ця і наступні 3 стрічки можна занести в функцію але залишу так :)
                print ("| {:<10}| {:<14}| {:<10}".format(obj.suffix, new_folder, way1.stem))
                if dest_folder.name == "archives":
                    shutil.unpack_archive(way1,way1.with_suffix(''))
                    
            else:
                
                shutil.move(obj, way2)
                print ("| {:<10}| {:<14}| {:<10}".format(obj.suffix, new_folder, way2.stem))
                if dest_folder.name == "archives":
                    shutil.unpack_archive(way2,way2.with_suffix(''))
                cpf[new_folder] += 1     

            return
        
        
        print ("\n| {:<10}| {:<14}| {:<10}".format('Розширення', 'цільова папка','назва файлу'))
        print ("---------------------------------------")
        usi_objekty = Path(folder_path).rglob("**/*")

        for obj in usi_objekty:
            
            if obj.is_file() and 'archives' not in str(obj):    
                if obj.parent.name not in all_known_ext and obj.parent.name != "others": # це потрібно щоб при повторному виклику на вже відсортовану папку
# не було повторного сортування, а також не лізло в папку з розпакованими архівами
                                           
                    new_folder = sort(obj)  
                    moving_files(obj, folder_path, new_folder)              
        
        
               
        for key in all_known_ext:           # От прям, знаю що це можна зробити якось простіше в сортуванні але не придумав як так що ось!
            for ext in all_known_ext[key]:
                if ext.lower() in known_ext_set:
                    known_ext_dict[key].append(ext)

        print(f"Невідомі розширення файлів - {unknown_ext_set}") 
        print(f"Знайдені відомі розширення файлів - {known_ext_dict}") 

      
        for obj in Path(folder_path).glob('*'):
            if obj.name not in all_known_ext and obj.name != "others":
                shutil.rmtree(obj)

        print ("Готово")
        return 
    


if __name__ == "__main__":
 
    
    dz6()

# PS  назви змінних українською легше сприймати на фоні того що різні вбудовані частини коду підсвічуються так само як змінні, голубеньким кольором.  
# і коли я бачу слово, наприклад, "papka" я відразу розумію що це не якийсь метод чи ідентифікатор. 