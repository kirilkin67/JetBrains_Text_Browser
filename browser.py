import sys
import os
import requests
from collections import deque
from bs4 import BeautifulSoup
from colorama import init, Fore, Style

init(autoreset=False)


def create_directory(args):
    if len(args) > 2:
        print("Usage: one argument, name directory")
        exit()
    directory = args[1]
    try:
        # Create target Directory
        os.mkdir(f"{os.getcwd()}/{directory}")
        print(f"Directory <directory> Created")
    except FileExistsError:
        print(f"Directory <{directory}> already exists")
    finally:
        return f"{os.getcwd()}/{directory}"


def parser_text(soup):
    text = str()
    tags = ['p', 'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', "title"]
    # tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'ul', 'ol', 'li', "title"]
    page = soup.find_all(tags)
    # for tag in tags:
    #     page = soup.select(tag)
    for p in page:
        # text += Fore.RED + f'{p.name}\n' + Style.RESET_ALL
        if p.name in ('a',):
            text += Fore.BLUE + f'{p.text}\n' + Style.RESET_ALL
        else:
            text += f'{p.text}\n'
    return text


def write_file(direct, url):
    file = f"{direct}/{url.lstrip('https://').rstrip('.comrg')}.txt"
    with open(file, "w", encoding='utf-8') as fd:
        url = check_url(url)
        response = requests.get(url)
        if response:
            soup = BeautifulSoup(response.content, 'html.parser')
            text = parser_text(soup)
            print(text)
            fd.write(text)


def read_file(direct, url):
    try:
        with open(f"{direct}/{url}.txt", encoding='utf-8') as fd:
            print(fd.read())
    except FileNotFoundError:
        print("Error: Incorrect URL")


def check_url(url):
    if url.lower().startswith("https://"):
        return url.lower()
    return "https://" + url


def main(direct):
    url_stack = deque()
    while True:
        url = input("> ")
        if url == "exit":
            break
        elif url == "back":
            if len(url_stack) > 1:
                try:
                    url_stack.pop()
                    write_file(direct, url_stack.pop())
                    url_stack.append(url)
                except IndexError:
                    pass
        elif url.endswith((".com", ".org")):
            url_stack.append(url)
            write_file(direct, url)
        else:
            read_file(direct, url)


dir_name = str()
if len(sys.argv) > 1:
    dir_name = create_directory(sys.argv)
else:
    dir_name = os.getcwd()
print(dir_name)
main(dir_name)
