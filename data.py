from PIL import ImageDraw, Image, ImageFont
import PIL.ImageFont
from pathlib import Path


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

mass = []

for i in range(33):
    mass.append(i)

# список шрифтов для создания базы для обучения
fontsListTest = [ImageFont.truetype("DroidSansArmenian.ttf", font_size)]
def createImage(symbolStr:str, font:ImageFont.FreeTypeFont):
    img = Image.new('RGB', (50, 50), back_ground_color)
    d = ImageDraw.Draw(img)
    # unicode_font = ImageFont.truetype("DejaVuSans.ttf", font_size)
    leftBox, topBox, rightBox, bottomBox = d.textbbox((0,0), symbolStr, font)
    # d.text((25, 25), unicode_text, font=unicode_font, fill=font_color )
    d.text((-leftBox+rightBox, -topBox+bottomBox), symbolStr, font=font, fill=font_color)
    return img

for i in range(len(fontsListTest)):
    nameImg = str(mass[i]) + "_" +"0" + '.png'
    for k in range(len(listSymbol)):
        pathImg = pathStrDataset + pathStrTest + "/" + str(k) + "/" + nameImg
        img = createImage(listSymbol[k], fontsListTest[i])
        img.save(pathImg)



# список шрифтов для создания базы для обучения
fontsListTest = [ImageFont.truetype("Arian_Grqi_U.ttf", font_size)]
def createImage(symbolStr:str, font:ImageFont.FreeTypeFont):
    img = Image.new('RGB', (50, 50), back_ground_color)
    d = ImageDraw.Draw(img)
    # unicode_font = ImageFont.truetype("DejaVuSans.ttf", font_size)
    leftBox, topBox, rightBox, bottomBox = d.textbbox((0,0), symbolStr, font)
    # d.text((25, 25), unicode_text, font=unicode_font, fill=font_color )
    d.text((-leftBox+rightBox, -topBox+bottomBox), symbolStr, font=font, fill=font_color)
    return img

for i in range(len(fontsListTest)):
    nameImg = str(mass[i]) + "_" + "1" + '.png'
    for k in range(len(listSymbol)):
        pathImg = pathStrDataset + pathStrTest + "/" + str(k) + "/" + nameImg
        img = createImage(listSymbol[k], fontsListTest[i])
        img.save(pathImg)

        # параметры цвета фона, шрифта для датасета
back_ground_color=(255,255,255)
font_size=30
font_color=(0,0,0)
unicode_text = u"\u0531"
# unicode_text = "Ա"

mass = []

for i in range(33):
    mass.append(i)

# список шрифтов для создания базы для обучения
fontsListTest = [ImageFont.truetype("DroidSansArmenian.ttf", font_size)]
def createImage(symbolStr:str, font:ImageFont.FreeTypeFont):
    img = Image.new('RGB', (50, 50), back_ground_color)
    d = ImageDraw.Draw(img)
  
    leftBox, topBox, rightBox, bottomBox = d.textbbox((0,0), symbolStr, font)
  
    d.text((-leftBox+rightBox, -topBox+bottomBox), symbolStr, font=font, fill=font_color)
    return img

for i in range(len(fontsListTest)):
    nameImg = str(mass[i]) + "_" +"2" + '.png'
    for k in range(len(listSymbol)):
        pathImg = pathStrDataset + pathStrTest + "/" + str(k) + "/" + nameImg
        img = createImage(listSymbol[k], fontsListTest[i])
        img.save(pathImg)



# список шрифтов для создания базы для обучения
fontsListTest = [ImageFont.truetype("Arian_Grqi_U.ttf", font_size)]
def createImage(symbolStr:str, font:ImageFont.FreeTypeFont):
    img = Image.new('RGB', (50, 50), back_ground_color)
    d = ImageDraw.Draw(img)
    # unicode_font = ImageFont.truetype("DejaVuSans.ttf", font_size)
    leftBox, topBox, rightBox, bottomBox = d.textbbox((0,0), symbolStr, font)
    # d.text((25, 25), unicode_text, font=unicode_font, fill=font_color )
    d.text((-leftBox+rightBox, -topBox+bottomBox), symbolStr, font=font, fill=font_color)
    return img

for i in range(len(fontsListTest)):
    nameImg = str(mass[i]) + "_" + "3" + '.png'
    for k in range(len(listSymbol)):
        pathImg = pathStrDataset + pathStrTest + "/" + str(k) + "/" + nameImg
        img = createImage(listSymbol[k], fontsListTest[i])
        img.save(pathImg)