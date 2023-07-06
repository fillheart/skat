from PIL import ImageDraw, Image, ImageFont, ImageFilter
from pathlib import Path
from random import *

# unicode_text = u"\u0531"
# все заглавные буквы армянского языка
listSymbol = ['\u0531', '\u0532', '\u0533', '\u0534', '\u0535',
'\u0536', '\u0537', '\u0538', '\u0539', '\u053A',
'\u053B', '\u053C', '\u053D', '\u053E', '\u053F',
'\u0540', '\u0541', '\u0542', '\u0543', '\u0544',
'\u0545', '\u0546', '\u0547', '\u0548', '\u0549',
'\u054A', '\u054B', '\u054C', '\u054D', '\u054E',
'\u054F',
'\u0550', '\u0551', '\u0552', '\u0553', '\u0554',
'\u0555', '\u0556']
print(len(listSymbol))
print(listSymbol)

# удаление элементов из общего списка не рассматриваемых букв
listSymbolDel = ['\u0531', '\u0548', '\u054C', '\u054D']
for d in listSymbolDel:
    listSymbol.remove(d)
print(listSymbolDel)

# вывод итогового списка букв
print(len(listSymbol))
print(listSymbol)

pathStrDataset = "../dataset/simpledataset"
Path(pathStrDataset).mkdir(parents=True, exist_ok=True)
pathStrTrain = "/train"
pathStrTest = "/test"

Path(pathStrDataset + pathStrTrain).mkdir(parents=True, exist_ok=True)
Path(pathStrDataset + pathStrTest).mkdir(parents=True, exist_ok=True)
for i in range(len(listSymbol)):
    pathStrDatasetTrainFolder = pathStrDataset + pathStrTrain + "/" + str(i)
    pathStrDatasetTestFolder = pathStrDataset + pathStrTest + "/" + str(i)
    Path(pathStrDatasetTrainFolder).mkdir(parents=False, exist_ok=True)
    Path(pathStrDatasetTestFolder).mkdir(parents=False, exist_ok=True)


# параметры цвета фона, шрифта для датасета
back_ground_color=(255,255,255)
font_size=25
font_color=(0,0,0)
unicode_text = u"\u0531"
# unicode_text = "Ա"


tmp = 0

def createImage(symbolStr:str, font:ImageFont.FreeTypeFont):
        img = Image.new('RGB', (50, 50), back_ground_color)
        d = ImageDraw.Draw(img)
        # unicode_font = ImageFont.truetype("DejaVuSans.ttf", font_size)
        leftBox, topBox, rightBox, bottomBox = d.textbbox((0,0), symbolStr, font)
        # d.text((25, 25), unicode_text, font=unicode_font, fill=font_color )
        d.text((-leftBox+rightBox, -topBox+bottomBox), symbolStr, font=font, fill=font_color)
        return img

def create(str_1, degree = 0, bool = False):

    global tmp
    mass = []

    for i in range(33):
        mass.append(i)

    # список шрифтов для создания базы для обучения
    fontsListTest = [ImageFont.truetype(str_1, font_size)]

    for i in range(len(fontsListTest)):
        nameImg = str(mass[i]) + "_" + str(tmp) + '.png'
        for k in range(len(listSymbol)):
            pathImg = pathStrDataset + pathStrTrain + "/" + str(k) + "/" + nameImg
            img = createImage(listSymbol[k], fontsListTest[i])
            if bool == True:
                img = img.filter(ImageFilter.GaussianBlur(radius=1.2))
            img = img.rotate(degree)
            img.save(pathImg)
    
    tmp = tmp + 1
    return img



def creat(str_1, degree = 0, bool = False):

    global tmp
    mass = []

    for i in range(33):
        mass.append(i)

    # список шрифтов для создания базы для обучения
    fontsListTest = [ImageFont.truetype(str_1, font_size)]

    for i in range(len(fontsListTest)):
        nameImg = str(mass[i]) + "_" + str(tmp) + '.png'
        for k in range(len(listSymbol)):
            pathImg = pathStrDataset + pathStrTest + "/" + str(k) + "/" + nameImg
            img = createImage(listSymbol[k], fontsListTest[i])
            if bool == True:
                img = img.filter(ImageFilter.GaussianBlur(radius=1.2))
            img = img.rotate(degree)
            img.save(pathImg)
    
    tmp = tmp + 1
    return img






if __name__ == '__main__':
    font1 = ["Arian_Grqi_U.ttf","DejaVuSans.ttf","arnamu_serif.ttf","DroidSansArmenian.ttf","NorKirk.ttf","Shatrvan.ttf","SosGro.ttf","SosStm.ttf","Sylfaen.ttf","GaliverSans-lavD.ttf","BiainaBeta.ttf","TITUS Cyberbit Basic.ttf"]
    font2 = ["TruetypewriterPolyglott-mELa.ttf","weblysleekuil.ttf"]
    degr = [0,15,30,45,90,270,285,300,315,330,345]
    for i in range(len(font1)):
        for j in range(len(degr)):
            create(font1[i],degr[j])
    for i in range(len(font1)):
        for j in range(len(degr)):
            create(font1[i],degr[j],True)
    for i in range(len(font2)):
        for j in range(len(degr)):
            creat(font2[i],degr[j])
    for i in range(len(font2)):
        for j in range(len(degr)):
            creat(font2[i],degr[j],True)
   
   