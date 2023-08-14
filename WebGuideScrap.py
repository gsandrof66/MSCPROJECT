import requests, re
import Database.DataSave as Data
from time import sleep
from datetime import datetime
from bs4 import BeautifulSoup
from random import randint

the_headers = {
    # "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}
ROOT_URL = "https://www.euansguide.com"
TYPE_REV = ['Overview', 'Transport & Parking', 'Access', 'Toilets', 'Staff', 'Anything else you wish to tell us?', 'Photos', 'Video']
OPC_V = ['AccessibleToilet', 'ChangingPlaces', 'Hoist', 'Wet Room']


def add_initial(text):
    if text is not None:
        if text[-1]==".":
            return text
        else:
            return text + ". "
    else:
        return ""


def get_idurl(link):
    x = re.findall("[-][0-9]+", link)
    return int(x[-1].replace("-", "")) if len(x)>0 else 0


def get_date(text):
    x = re.search("[A-z]+", text)
    y = re.search("[0-9]+", text)
    return datetime.strptime(x.group(0), '%B').month, int(y.group(0))


def get_venues(url_results):
    inx, pag_ven = 1, 1
    my_venues = list()
    while inx <= pag_ven:
        if inx == 1:
            res1 = requests.get(url_results, the_headers)
        else:
            res1 = requests.get(url_results + "&pagenum=" + str(inx), the_headers)
        soup = BeautifulSoup(res1.text, features="lxml")
        if inx == 1:
            pag = soup.find("div", {"class":"v2-page-controls"}).find_all("li")
            if pag is not None: pag_ven = int(pag[-1].text)
        for unit in soup.find_all("article", {"class":"v2-panel v2-place clearfix"}):
            name = unit.find("h3").text
            link = unit.find("a", {"class":"btn btn-places btn-purple"}, href=True)
            access_opt = [i.text.replace("\n", "") for i in unit.find_all("div", {"class":"acc"})]
            venue = {"idv": 0, "idevenue": None, "name": name, "url": ROOT_URL + link['href'],
                     "acc": OPC_V[0] in access_opt, "ch": OPC_V[1] in access_opt,
                     "ho": OPC_V[2] in access_opt, "we": OPC_V[3] in access_opt}
            venue["idevenue"] = get_idurl(venue["url"])
            venue["idv"] = Data.save_venue(venue)
            if venue["idv"] == 0:
                print("Error venue")
            my_venues.append(venue)
        inx += 1
        sleep(randint(1, 2))
    print(len(my_venues))
    return my_venues


def get_det_venues(my_venues):
    for my_v in my_venues:
        inc, pag_comm = 1, 1
        while inc <= pag_comm:
            if inc == 1:
                res2 = requests.get(my_v["url"], the_headers)
            else:
                res2 = requests.get(my_v["url"] + "?pagenum=" + str(inc), the_headers)
            soup_place = BeautifulSoup(res2.text, features="lxml")
            if inc == 1:
                pag = soup_place.find("div", {"class": "v2-page-controls"})
                if pag is not None: pag = pag.find_all("li")
                if pag is not None: pag_comm = int(pag[-1].text)
            for review_div in soup_place.find_all("div", {"class": "v2-panel v2-venue-review"}):
                user = {"idu": 0, "author": None, "location": None}
                user["author"] = review_div.find("p", {"class": "author-username"}).text
                location = review_div.find("p", {"class": "author-location"})
                if location is not None: user["location"] = location.text
                print(user)
                user["idu"] = Data.save_user(user)
                if user["idu"] == 0:
                    print("Error user")
                rev_more_link = review_div.find("a", {"class": "btn btn-purple"}, href=True)
                rev_more_link = ROOT_URL + rev_more_link['href']
                review = {"idrev": 0, "idu": 0, "idv": 0, "idevrev": get_idurl(rev_more_link), "rank": None, "month": 0, "year": 0}
                review["idu"] = user["idu"]
                review["idv"] = my_v["idv"]
                review["rank"] = review_div.find("span", {"class": "v2-rating-label"}).text
                review["month"], review["year"] = get_date(review_div.find("time").text)
                rev_initial = review_div.find("span", {"itemprop": "itemReviewed"})
                if rev_initial is not None: rev_initial = rev_initial.text.strip()
                res_det = requests.get(rev_more_link, the_headers)
                soup_read_more = BeautifulSoup(res_det.text, features="lxml")
                det_title_rev = [i.text for i in
                                 soup_read_more.find("div", {"class": "review-body"}).find_all("h4") if i.text != "Photos" and i.text != "Video"]
                det_content_rev = [i.text.strip() for i in
                                   soup_read_more.find("div", {"class": "review-body"}).find_all("p", {"class": "pre-line"})]
                det_ven_rev = {'Overview': None, 'Transport & Parking': None, 'Access': None, 'Toilets': None,
                               'Staff': None, 'Anything else you wish to tell us?': None, 'Photos': None, 'Video': None}
                try:
                    for n in range(len(det_title_rev)):
                        det_ven_rev[det_title_rev[n]] = det_content_rev[n]
                except Exception as e:
                    print("url", my_v["url"], str(inc))
                    print("long", str(len(det_title_rev)))
                    print("val", det_title_rev)
                    print("long", str(len(det_content_rev)))
                    return
                det_ven_rev["Overview"] = add_initial(rev_initial) + det_ven_rev["Overview"]
                review.update(det_ven_rev)
                review["idrev"] = Data.save_review(review)
                if review["idrev"] == 0:
                    print("Error review")
                print(review)
                print("+++")
            inc += 1
            sleep(randint(1, 2))


print("Start: " + str(datetime.now()))
get_det_venues(get_venues("https://www.euansguide.com/reviews/results/?city=Glasgow&countrycode=GB&location=Glasgow,%20UK&sortby=NumberOfReviews"))
print("End: " + str(datetime.now()))
