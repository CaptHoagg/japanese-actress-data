from bs4 import BeautifulSoup
import re
import requests
import csv

def get_soup(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.text,"html.parser")
    return soup 

def get_name(soup):
    actress_name = []
    name = soup.find_all("h1")
    for i in name[0]: 
        actress_name.append(str(i.text))
    return actress_name

def get_image(soup):
    image_links = []
    image_link = []
    link = soup.find_all('img',{"class":"actressThumb"})
    for object in link: 
        image_links.append(object.get('src'))
    image_link.append(image_links[-1])
    return image_link 

def get_favorite(soup): 
    favor = []
    favor_in4 = soup.find_all('span',{'class': 'favorite-count'})
    for i in favor_in4:
        favor.append(i.text)
    return favor

def get_base_in4(soup): 
    actress_info_first = []
    actress_info_final = []
    info = soup.find_all("dl",{'class':'profile'})
    for k in info[0].find_all('dd'):
        actress_info_first.append(str(k.text))
    del actress_info_first[0]
    col_name = ['Date of birth','Blood Type','City of Born','Height','Size','Hobby','Special Skill','Other']
    for i in range (len(col_name)):
        if i != 1: 
            actress_info_final.append(actress_info_first[i][len(col_name[i]):])
        else:
            blood = actress_info_first[1][len(col_name[1]):][0:2]
    return actress_info_final

def get_height(info): 
    h_info = info[3]
    height = re.findall(r'\d+', h_info)
    return height

def get_deep_in4(info): 
    deep_in4 =[]
    base_in4 = info[4].split()
    for info in base_in4 : 
        for char in info.split():  
            number = re.findall(r'\d+', char)
            str = ""
            for object in number : 
                str+=object
                deep_in4.append(str)
    return deep_in4
    
def get_movie(soup):
    movies = []
    total_info_of_movie = []
    collection = soup.find_all("img",{'class':'packageThumb'})
    for info in collection : 
        if 'alt' in info.attrs: 
            movies.append(info.attrs['alt'])
    total_info_of_movie.append(movies)
    return total_info_of_movie

def get_all_data_from_link(link):
    soup = get_soup(link)
    name = get_name(soup)
    image = get_image(soup)
    base_info = get_base_in4(soup)
    height = get_height(base_info)
    hehe_info = get_deep_in4(base_info)
    del base_info[3:5]
    favorite=get_favorite(soup)
    movies=get_movie(soup)
    final = name+base_info+hehe_info+height+favorite+image+movies
    return final

def main(): 
    with open('final_data_of_project.csv','w',encoding='utf') as file: 
        for i in range(1,19394): 
            try:
                link = "https://xxx.xcity.jp/idol/detail/"+str(i)+"/"
                data = get_all_data_from_link(link)
                print('Get '+data[0]+"'s data successfully ("+ str(i)+').')
                writer = csv.writer(file)
                writer.writerow(data)
            except:
                print("non-data from id "+str(i)+'!!!!' )
                continue
main()