#!/usr/bin/env python
# =======================================================================
# title             :SerialDo0n
# description       :This program displays Information About Tv Series
# author            :LinArcX
# date              :03/21/2017
# version           :0.1
# mail              :linarcx@gmail.com
# web               :stack.blog.ir
# notes             :
# python_version    :3.6.0
# main api:         :http://www.tvmaze.com/api
# second api:       :https://www.episodate.com/api
# =======================================================================

# Import the modules needed to run the script.
import sys, os, pwd, json, requests
from collections import namedtuple
from prettytable import PrettyTable
from pyfiglet import figlet_format
import tvdb_api

# import pprint
# from util.pillow import showPixArt
# import pyfiglet # termcolor, colorama

# Main definition - constants
menu_actions = {}

# Url definition
searchUrl = "http://api.tvmaze.com/search/shows?q="
peopleUrl = 'http://api.tvmaze.com/search/people?q='
upComingUrl = 'http://api.tvmaze.com/schedule?date='
showUrl = 'http://api.tvmaze.com/shows'
showUrlByPage = ' http://api.tvmaze.com/shows?page='
url="https://www.episodate.com/api/show-details?q=arrow"

# init tvdb_api
t = tvdb_api.Tvdb(banners=True)

# =======================
#     MENUS FUNCTIONS
# =======================

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   ITALIC = '\e[3m'
   END = '\033[0m'

class Payload(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)

def main_menu():

    os.system('clear')
    userName = pwd.getpwuid(os.getuid()).pw_name
    print(color.BOLD + figlet_format('TvDo0n',font='starwars') + color.END)
    print("Welcome " + userName + ", Please Choose The Items:")
    print("s. Search Tv Series")
    print("w. whoAmI")
    print("x. truct")
    print("h. help")
    print("c. Clear Screen")
    print("\nq. Quit")
    choice = input(" >>  ")
    exec_menu(choice)
    return

def exec_menu(choice, dict=None):
    ch = choice.lower()
    if ch == '':
        menu_actions['main_menu']()
    else:
        try:
            if dict is None:
                menu_actions[ch]()
            else:
                menu_actions[ch](dict)
        except KeyError:
            print("Invalid selection, please try again.\n")
            menu_actions['main_menu']()
    return

def searchTvSeries(serailName=None):
    items = ""
    if serailName is None:
        os.system('clear')
        tVar = input("Enter Tv Show Name:")
        items = t.search(tVar)
        count = len(items)
    else:
        items = serailName
    x = PrettyTable()
    for i, item in enumerate(items):
        x.field_names = [i, "seriesname"]
        x.add_row([i, item['seriesname']])
    print(x)
    print(color.CYAN + "for see more details, enter 'row Number' and hit ENTER.otherwise use below Capabilities." + color.END)
    print("b. Back")
    print("q. Quit")
    selectTvShow(items)
    return

def selectTvShow(items, pDict=None):
    dict = ""
    choice = ""
    try:
        if pDict is None:
            choice = input(" >>  ")
            dict = items[int(choice)]
        else:
            dict = pDict
        x = PrettyTable()
        # x.add_column(item['seriesname'], [1295, 5905, 112, 1357, 2058, 1566, 5386])
        x.add_column("No.", [choice])
        x.add_column("seriesname",[(t[dict['seriesname']]['seriesname'])])
        x.add_column("rating",[(t[dict['seriesname']]['rating'])])
        x.add_column("ratingcount",[(t[dict['seriesname']]['ratingcount'])])
        x.add_column("genre",[(t[dict['seriesname']]['genre'])])
        x.add_column("airs_dayofweek",[(t[dict['seriesname']]['airs_dayofweek'])])
        x.add_column("firstaired",[(t[dict['seriesname']]['firstaired'])])
        x.add_column("finale_aired",[(t[dict['seriesname']]['finale_aired'])])
        x.add_column("network",[(t[dict['seriesname']]['network'])])
        x.add_column("runtime",[(t[dict['seriesname']]['runtime'])])
        x.add_column("status",[(t[dict['seriesname']]['status'])])
        print(x)
    except ValueError:
        main_menu()
    except IndexError:
        print("Oops! You Enter Incorrect Number.Please Select Another Series Again: ")
        selectTvShow(items)
    print("s. Search Another Tv Show")
    print("o. OverView")
    print("a. actors")
    print("b. Back")
    print("q. Quit")
    choice = input(" >>  ")
    if choice == 'o' or choice == 'a':
        exec_menu(choice, dict)
    elif choice == 'b':
        searchTvSeries(items)
    else:
        exec_menu(choice)
    return

def OverView(dict):
    print("overview: \n")
    print(color.RED + str([(t[dict['seriesname']]['overview'])]) + color.END)
    print("b. Back")
    print("q. Quit")
    choice = input(" >>  ")
    if choice == 'b':
        selectTvShow("", dict)
    else:
        exec_menu(choice)
    return

def actors(dict):
    x = PrettyTable()
    splitActors = str([(t[dict['seriesname']]['actors'])]).split("|")
    for i, item in enumerate(splitActors):
        x.field_names = [i, "actors"]
        x.add_row([i, color.GREEN + item + color.END])
    print(x)
    print("b. Back")
    print("q. Quit")
    choice = input(" >>  ")
    if choice == 'b':
        selectTvShow("", dict)
    else:
        exec_menu(choice)
    return

def whoAmI():
    print("i am nobody, please visit us on : http://www.bbs.archusers.ir!\n")
    print("b. Back")
    print("q. Quit")
    choice = input(" >>  ")
    exec_menu(choice)
    return

def help():
    print("this program use english letters for get into other menu(sub-menu).\nfor example, if you see: 'b. Back', you must enter b letter, "+
          "and hit enter from keyboard.")
    print("b. Back")
    print("q. Quit")
    choice = input(" >>  ")
    exec_menu(choice)
    return

def clear():
    os.system('clear')
    print("b. Back")
    print("q. Quit")
    choice = input(" >>  ")
    exec_menu(choice)
    return

def getTvObj():
    resp = requests.get(url)
    return json.loads(resp.content.decode('utf-8'), object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

def truct():
    #client-id = 87f242aaa6dd444422926ef424ebd1f86567fee2810914ca98154601b0cfc899
    #client-secret-id=dbdb42b6a0a7039f652dd24330fc7a8a3e6083062978fb8e755520ed21ad4f70
    # payload = {'Content-type': 'application/json',
    #            'trakt-api-key': '87f242aaa6dd444422926ef424ebd1f86567fee2810914ca98154601b0cfc899',
    #            'trakt-api-version': '2'}
    # resp = requests.get('https://api.trakt.tv', params=payload)
    # print(resp.headers)

    # p = lambda: None

    p = getTvObj()
    print(p)

def back():
    menu_actions['main_menu']()

def quit():
    sys.exit()

# =======================
#    MENUS DEFINITIONS
# =======================
# Menu definition

menu_actions = {
    'main_menu': main_menu,
    's': searchTvSeries,
    'w': whoAmI,
    'h': help,
    'a': actors,
    't': selectTvShow,
    'o': OverView,
    'x': truct,
    'c': clear,
    'b': back,
    'q': quit,
}

# =======================
#      MAIN PROGRAM
# =======================
# Tv Show Samples: Game of Thrones - stranger things - dexter - lost

# Main Program
if __name__ == "__main__":
    # Launch main menu
    main_menu()
