# -*- coding: utf-8 -*-
# Version: 1.1.2
# Auteur: Michoko
# Date de création 18/02/2023
# https://github.com/michoko999

import random
import os
import json
import csv
import time
import webbrowser
import keyboard
import requests
import re


# Variables globales
TRADPATH = "traduction.json"
LANGDICT = None

ASCII_LOGO = [
    r"""

                                                                                     
     _/      _/       _/                    _/                       _/                
    _/_/  _/_/                 _/_/_/      _/_/_/        _/_/       _/  _/       _/_/    
   _/  _/  _/       _/      _/            _/    _/    _/    _/     _/_/       _/    _/   
  _/      _/       _/      _/            _/    _/    _/    _/     _/  _/     _/    _/    
 _/      _/       _/        _/_/_/      _/    _/      _/_/       _/    _/     _/_/""",
    r"""
 ::::    ::::  :::::::::::  ::::::::  :::    :::  ::::::::  :::    :::  ::::::::  
 +:+:+: :+:+:+     :+:     :+:    :+: :+:    :+: :+:    :+: :+:   :+:  :+:    :+: 
 +:+ +:+:+ +:+     +:+     +:+        +:+    +:+ +:+    +:+ +:+  +:+   +:+    +:+ 
 +#+  +:+  +#+     +#+     +#+        +#++:++#++ +#+    +:+ +#++:++    +#+    +:+ 
 +#+       +#+     +#+     +#+        +#+    +#+ +#+    +#+ +#+  +#+   +#+    +#+ 
 #+#       #+#     #+#     #+#    #+# #+#    #+# #+#    #+# #+#   #+#  #+#    #+# 
 ###       ### ###########  ########  ###    ###  ########  ###    ###  ######## """,
    r"""
 .::       .::                            .::               
 .: .::   .::: .:       .::               .::               
 .:: .:: . .::      .:::.::        .::    .::  .::   .::     
 .::  .::  .::.:: .::   .: .:    .::  .:: .:: .::  .::  .:: 
 .::   .:  .::.::.::    .::  .::.::    .::.:.::   .::    .::
 .::       .::.:: .::   .:   .:: .::  .:: .:: .::  .::  .:: 
 .::       .::.::   .:::.::  .::   .::    .::  .::   .::  """,
    r"""
 888b     d888 d8b          888               888               
 8888b   d8888 Y8P          888               888               
 88888b.d88888              888               888                
 888Y88888P888 888  .d8888b 88888b.   .d88b.  888  888  .d88b.  
 888 Y888P 888 888 d88P     888  88b d88  88b 888 .88P d88  88b 
 888  Y8P  888 888 888      888  888 888  888 888888K  888  888 
 888       888 888 Y88b.    888  888 Y88..88P 888  88b Y88..88P 
 888       888 888   Y8888P 888  888   Y88P   888  888   Y88P  """,
r"""
 ███▄ ▄███▓ ██▓ ▄████▄   ██░ ██  ▒█████   ██ ▄█▀ ▒█████   
▓██▒▀█▀ ██▒▓██▒▒██▀ ▀█  ▓██░ ██▒▒██▒  ██▒ ██▄█▒ ▒██▒  ██▒
▓██    ▓██░▒██▒▒▓█    ▄ ▒██▀▀██░▒██░  ██▒▓███▄░ ▒██░  ██▒
▒██    ▒██ ░██░▒▓▓▄ ▄██▒░▓█ ░██ ▒██   ██░▓██ █▄ ▒██   ██░
▒██▒   ░██▒░██░▒ ▓███▀ ░░▓█▒░██▓░ ████▓▒░▒██▒ █▄░ ████▓▒░  
░ ▒░   ░  ░░▓  ░ ░▒ ▒  ░ ▒ ░░▒░▒░ ▒░▒░▒░ ▒ ▒▒ ▓▒░ ▒░▒░▒░ 
░  ░      ░ ▒ ░  ░  ▒    ▒ ░▒░ ░  ░ ▒ ▒░ ░ ░▒ ▒░  ░ ▒ ▒░ 
░      ░    ▒ ░░         ░  ░░ ░░ ░ ░ ▒  ░ ░░ ░ ░ ░ ░ ▒  
       ░    ░  ░ ░       ░  ░  ░    ░ ░  ░  ░       ░ ░  
               ░                                         
"""]


def load_translations(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def check_url(url, lang):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    lang_params = {
        'fr': 'fr',
        'en': 'en',
        'es': 'es',
        'de': 'de',
        'pt': 'pt',
        'it': 'it',
        'pl': 'pl'
    }
    lang_param = lang_params.get(lang, 'en')
    if 'instant-gaming.com' in url:
        url = re.sub(r'/[a-z]{2}/', f'/{lang_param}/', url)

    messages = {
        'fr': {
            'giveaway_ended': 'Ce Giveaway est terminé',
            'win_game': 'Gagne le jeu de ton choix'
        },
        'en': {
            'giveaway_ended': 'This giveaway is over',
            'win_game': 'Win the game of your choice'
        },
        'es': {
            'giveaway_ended': 'Este sorteo ya ha terminado',
            'win_game': 'Gana el juego que quieras'
        },
        'de': {
            'giveaway_ended': 'Dieses Giveaway ist vorüber',
            'win_game': 'Gewinne ein Spiel deiner Wahl'
        },
        'pt': {
            'giveaway_ended': 'O giveaway terminou',
            'win_game': 'Ganha um jogo à tua escolha'
        },
        'it': {
            'giveaway_ended': 'Questo giveaway è finito',
            'win_game': 'Vinci un gioco a tua scelta'
        },
        'pl': {
            'giveaway_ended': 'To giveaway zakończone',
            'win_game': 'Wygraj wybraną przez siebie grę'
        }
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 404:
            return 'invalid'
        if messages[lang]['giveaway_ended'] in response.text:
            return 'invalid'
        if messages[lang]['win_game'] in response.text:
            return 'valid'
        return 'unknown'
    except requests.RequestException:
        return 'invalid'


def update_giveaways(csv_path, lang, translations):
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        urls = [row[0] for row in reader if row]  # Vérifie que la ligne n'est pas vide

    valid_urls = []
    invalid_urls = []
    unknown_urls = []

    for url in urls:
        status = check_url(url, lang)
        if status == 'valid':
            valid_urls.append(url)
            print(f"Valid: {url}")
        elif status == 'invalid':
            invalid_urls.append(url)
            print(f"Invalid: {url}")
        else:
            unknown_urls.append(url)
            print(f"Unknown: {url}")

        delay = random.uniform(0.25, 1.25)
        time.sleep(delay)

    with open('valid_urls.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for url in valid_urls:
            writer.writerow([url])

    with open('invalid_urls.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for url in invalid_urls:
            writer.writerow([url])

    with open('unknown_urls.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for url in unknown_urls:
            writer.writerow([url])

    print(translations[lang]["valid_urls_message"])


def get_urls(lang: str, csv_path: str, translations) -> list:
    """
    Renvoie une liste contenant les urls contenues dans le fichier csv
    :param csv_path: Chemin vers le fichier csv
    :return: Liste contenant les urls
    """
    try:
        abs_path = os.path.abspath(__file__)
        full_path = os.path.join(os.path.dirname(abs_path), csv_path)
        urls = []
        with open(full_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                urls.append(row[0])
        return urls
    except FileNotFoundError:
        print(translations[lang]["errorfile"])
        return None


def get_lang(translations) -> str:
    """
    Renvoie la langue choisie par l'utilisateur
    :return: Langue choisie par l'utilisateur
    """
    langchoice = input("\n" + "Language (fr/en/es/de/pt/it/pl) : ")
    if langchoice not in list(translations.keys()):
        langchoice = "en"
        print(translations[langchoice]["errorlang"])
    return langchoice


def get_seconds_per_url(lang: str, translations) -> float:
    """
    Renvoie le nombre de secondes entre chaque ouverture d'URL
    :return: Nombre de secondes entre chaque ouverture d'URL
    """
    while True:
        try:
            seconds_per_url = float(input("\n" + translations[lang]["seconds_per_url"]))
            return seconds_per_url
        except ValueError:
            print(translations[lang]["errortype"] + "\n")


def get_ready(lang: str) -> bool:
    """
    Renvoie True si l'utilisateur est prêt à lancer le programme
    :return: True si l'utilisateur est prêt à lancer le programme
    """
    ready = input("\n" + translations[lang]["reponse"]).lower()
    if ready in (translations[lang]["yes"].lower(), translations[lang]["yes"][0].lower()):
        return True
    return False


def open_urls(lang, urls, seconds_per_url):
    lang_params = {
        'fr': 'fr',
        'en': 'en',
        'es': 'es',
        'de': 'de',
        'pt': 'pt',
        'it': 'it',
        'pl': 'pl'
    }
    lang_param = lang_params.get(lang, 'en')

    for url in urls:
        if 'instant-gaming.com' in url:
            url_with_lang = re.sub(r'/[a-z]{2}/', f'/{lang_param}/', url)
        else:
            url_with_lang = url
        print(f"Opening URL: {url_with_lang}")
        webbrowser.open(url_with_lang)
        time.sleep(seconds_per_url)
        keyboard.press_and_release('ctrl+w')
    print(translations[lang]["endmessage"].format(len(urls), len(urls) * seconds_per_url))


def main():
    """
    Fonction principale
    """
    os.system('cls' if os.name == 'nt' else 'clear')

    global translations
    translations = load_translations('traduction.json')

    ascii_art = random.choice(ASCII_LOGO)
    print(ascii_art + "\n")

    lang = get_lang(translations)
    update_choice = input("\n" + translations[lang]["update_choice"])
    if update_choice.lower() in ['yes', 'oui', 'y', 'o','sí','si','ja']:
        update_giveaways('List-Uncheck.csv', lang, translations)
    file_name = input("\n" + translations[lang]["csv_file_name"])
    liste_urls = get_urls(lang, file_name, translations)
    if liste_urls is None:
        return
    seconds_between_urls = get_seconds_per_url(lang, translations)
    print("\n" + translations[lang]["explications"])

    ready = get_ready(lang)
    if not ready:
        return

    open_urls(lang, liste_urls, seconds_between_urls)


if __name__ == "__main__":
    main()
