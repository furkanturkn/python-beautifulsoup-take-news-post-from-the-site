import requests
from bs4 import BeautifulSoup
import urllib.request
import collections
import os
import errno
import datetime
from unidecode import unidecode



print("BBC News"+"\n")
for yazisayi in range(60): # limit the number of posts to pull. default: 60
    try:
        Path = "C:/Users/Administrator/Desktop/Haberler/BBC_News/"

        BBC_world_URL = "http://feeds.bbci.co.uk/news/world/rss.xml" #BBC World category RSS url given
        r_world = requests.get(BBC_world_URL) #Url çek
        soup = BeautifulSoup(r_world.content,"xml") #Urlnin içeriğini al

        items = soup.findAll('item') #İçerikte tüm "item" id olanlari bul
        ################

        BBC_tech_URL = "http://feeds.bbci.co.uk/news/technology/rss.xml" #BBC technology category RSS url given
        r_world_t = requests.get(BBC_tech_URL)
        soup_t = BeautifulSoup(r_world_t.content,"xml")

        items_t = soup_t.findAll('item') # Find all "item" id in content
        ################

        BBC_politics_URL = "http://feeds.bbci.co.uk/news/politics/rss.xml" #BBC politics category RSS url given
        r_world_t = requests.get(BBC_tech_URL)

        r_world_p = requests.get(BBC_politics_URL)
        soup_p = BeautifulSoup(r_world_p.content,"xml")

        items_p = soup_p.findAll('item')    # Find all "item" id in content

        world_list = [] # News URL list
        for i in range(20):
            world_list.append(items[i].contents[5].text)# URL is in items[i].contents[5] (May Change)
            world_list.append(items_p[i].contents[5].text)
            world_list.append(items_t[i].contents[5].text)




        haber_url = world_list[yazisayi] # get link (don't forget we're in the for loop. line: 13)

        r_world_content = requests.get(haber_url)
        haber_url_control = haber_url[-8:]
        print('Haber ID: '+haber_url_control)


        soup = BeautifulSoup(r_world_content.content,"html.parser")#Urlnin içeriğini al
        list = []
        list_px = []
        list_alt = []


        wp_category = "World"

        imageall = soup.findAll("span", {"class":"image-and-copyright-container"})
        if len(imageall)%2 == 0:
            intrage = len(imageall)
        else:
            intrage = len(imageall) +1

        # Some BBC custom pictures to pass size control
        for i in range(0,intrage):
            if i % 2 == 0:
                imgpx = str(imageall[i-1])

                imgpx = imgpx.split('height="')
                imgpx = imgpx[1]
                imgpx = imgpx.split('"')
                imgpx = int(imgpx[0])

                if  imgpx > 200:

                    imgone = str(imageall[i-1])
                    imgone = imgone.split('src="')
                    imgone = imgone[1]
                    imgone = imgone.split('"')
                    imgone = imgone[0]

                    altone = str(imageall[i-1])
                    altone = altone.split('alt="')
                    if len(altone)< 2:
                        baci='a'

                    else:
                        altone = altone[1]
                        altone = altone.split('"')
                        altone = altone[0]
                    if altone!="BBC Stories logo":
                        list.append(imgone)
                        list_alt.append(altone)

                else:
                    pass

            else:
                pass


        # avoid repeating different sizes of the same image
        for i in range(len(list)):
            try:
                aga = a[i]
                be = a[i+1]
                if aga[-16:] == be[-16:]:
                    del list[i]
                    baci='a'
                else:
                    baci='a'
                    #print("resim esit degil")
            except:
                baci='a'
                #print('list index out of range')




        #print(imageall)
        thumbnail_img = soup.findAll('img',{"class":"js-image-replace"})
        if not thumbnail_img:

            pass
        else:
            list.append(thumbnail_img[0]['src'])
            list_alt.append(thumbnail_img[0]['alt'])





        description = soup.find("meta",{"name":"description"}).get("content")
        wp_description = description
        gelen_veri = soup.find("div", {"class":"story-body__inner"})
        try:
            gelen_veri = gelen_veri.findAll(['p','h2']) # get paragraphs and headings
        except:
            continue

        title = soup.find("h1",{"class":"story-body__h1"}) # get title

        baslik_kontrol = []

        ii = len(gelen_veri)

        metin = ""
        metin_html = ""

        for i in range (0, ii):
            if  gelen_veri[i].name == "h2":
                metin += (gelen_veri[i].text)+"\n\n"
                metin_html += "<h2>"+(gelen_veri[i].text)+"</h2>"+"<br><br>" # I am writing in html format, will work when sharing wordpress
                baslik_kontrol.append(gelen_veri[i].text)

            else:
                metin += (gelen_veri[i].text)+"\n\n"
                metin_html += (gelen_veri[i].text)+"<br><br>"

        if title is None:
            titleH =baslik_kontrol[0].replace("'", "")
            wp_title = titleH
        else:
        	wp_title = title.text


        if not list:
            list.append(r"C:\Users\Administrator\Desktop\Haberler\News.png")
        if not list_alt:
           list_alt.append(wp_title)

        for i in range(len(list)):
            list[i] = list[i].replace("320","660") # 660 > normal size picture 320 > small size picture

        # keyword and tag selector.
        # most repeated word. excluding black list words

        blacklist = open(r"C:\Users\Administrator\Desktop\Haberler\BlackList.txt", "r")
        blacklist=blacklist.read()
        liste = blacklist.split(",")

        stopwords = set(line.strip() for line in metin)
        stopwords = stopwords.union(set(liste))

        wordcount = {}

        for word in metin.lower().split():
            word = word.replace(".","")
            word = word.replace(",","")
            word = word.replace(":","")
            word = word.replace("\"","")
            word = word.replace("!","")
            word = word.replace("â€œ","")
            word = word.replace("â€˜","")
            word = word.replace("*","")
            if word not in stopwords:
                if word not in wordcount:
                    wordcount[word] = 1
                else:
                    wordcount[word] += 1


        word_counter = collections.Counter(wordcount)
        etiketler = ""

        keyword = ""

        for word, count in word_counter.most_common(1): # most repeated word

            keyword+=  word


        for word, count in word_counter.most_common(7):  # 7 most repeated words

            etiketler+=  word+','


        ######WP TITLE cannot contain special characters because the folder is pressed
        wp_title=wp_title.replace(":","")
        wp_title=wp_title.replace("<","")
        wp_title=wp_title.replace(">","")
        wp_title=wp_title.replace("*","")
        wp_title=wp_title.replace("?","")
        wp_title=wp_title.replace("/","")
        wp_title=wp_title.replace("|","")
        wp_title=wp_title.replace('"','')


        PathControl = Path+haber_url_control+"/"

        if not os.path.exists(os.path.dirname(PathControl)):
            try:
                os.makedirs(os.path.dirname(PathControl))
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise

        for i in range(len(list)):  # pictures download
            urllib.request.urlretrieve(str(list[i]),Path+haber_url_control+"/"+keyword+str(i)+ ".jpg")

        now = datetime.datetime.now()
        if now.month<10:
            now=str(0)+str(now.month)



            # convert to html
        html_list = metin_html.split("<br><br>")
        html_list_count = len(html_list)
        resim_linki_pin = "2what.com/wp-content/uploads/2019/"+now+"/"+keyword+str(0)+".jpg"

# If the word "x" appears in the sentence, delete the sentence.
        def index_containing_substring(the_list, substring):  # 1. parameter html_list 2. parameter "x" word
            for i, s in enumerate(the_list):
                if substring in s:
                    del split_metin[i]
                    return i
            return -1

        a = 0

        # insert images as html code
        if len(list) > 2:

            for i in range(html_list_count):

                try:
                    if html_list_count > 50:

                        if i % 8 == 0 and i >2:

                            html_list.insert(i,'<img src="/wp-content/uploads/2019/'+now+'/'+keyword+str(a)+'.jpg" alt="'+list_alt[a]+'" />')
                            a += 1

                    else:
                        if i % 4 == 0 and i > 2:

                            html_list.insert(i,'<img src="/wp-content/uploads/2019/'+now+'/'+keyword+str(a)+'.jpg" alt="'+list_alt[a]+'" />')
                            a += 1
                except IndexError:

                    pass
        else:
            passss ='a'# do nothing


        # merge list elements with "<br>"
        html_metin =  '<br><br>'.join(str(e) for e in html_list)

        dosya = open(Path+haber_url_control+"/Content.txt", "w", encoding = 'utf-8')
        #0 title
        #1 Content
        #2 Yoast META
        #3 Keyword
        #4 Tags
        #5 Category
        listaltmetin =""
        for listaltmtn in list_alt:
            listaltmetin+=listaltmtn+"<-->"

        def deEmojify(inputString):
            returnString = ""

            for character in inputString:
                try:
                    character.encode("ascii")
                    returnString += character
                except UnicodeEncodeError:
                    replaced = unidecode(str(character))
                    if replaced != '':
                        returnString += replaced
            return returnString

        html_metin = deEmojify(html_metin)

        dosya.write("""%s<--->%s<--->%s<--->%s<--->%s<--->%s<--->%s<--->%s""" % (wp_title,html_metin,wp_description,keyword,etiketler,wp_category,listaltmetin,resim_linki_pin))

        if not os.listdir(Path+haber_url_control):
            os.rmdir(Path+haber_url_control)
    except:
        print("UPS...bir hata olustu Hata kodu: BBC-Devit-3")
        if not os.listdir(Path+haber_url_control):
            os.rmdir(Path+haber_url_control)
        continue
