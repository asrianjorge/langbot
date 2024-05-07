from bs4 import BeautifulSoup
import requests
from requests.utils import default_headers
from aiogram import Router
from random import choice
import re


def cambridge_dict_find_word():
    url = 'https://dictionary.cambridge.org/dictionary/english/'
    headers = default_headers()
    headers.update({'User-Agent': 'Combine Agent'})
    page = requests.get(url, headers=headers)
    print(page.status_code)

    if page.status_code == 200:
        soup = BeautifulSoup(page.text, "html.parser")
        letters = ['0-9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                   't', 'u', 'v', 'w', 'x', 'y', 'z']
        letter = choice(letters)
        letters_url = f"https://dictionary.cambridge.org/browse/english-russian/{letter}/"
        class_ = 'hdf ff-50 lmt-15 i-browse'  # all packs

        page = requests.get(letters_url, headers=headers)
        soup = BeautifulSoup(page.text, "html.parser")

        packs_cols = soup.find_all(
            'a', class_='hlh32 hdb dil tcbd')  # each pack
        packs = []
        print('packs')
        for i in packs_cols:
            # print(i, str(i.get('href')))
            packs.append(str(i.get('href')))

        try:
            pack_url = choice(packs)
        except IndexError:  # if empty
            return cambridge_dict_find_word()

        page = requests.get(pack_url, headers=headers)
        soup = BeautifulSoup(page.text, "html.parser")
        words_cols = soup.find_all('a', class_='tc-bd')  # each word
        words = []

        print('words')
        for i in words_cols:
            # print(i, str(i.get('href')))
            words.append(str(i.get('href')))

        w = choice(words)
        word_url = "https://dictionary.cambridge.org" + w
        # word_url = "https://dictionary.cambridge.org/dictionary/english-russian/draft"
        # word_url = "https://dictionary.cambridge.org/dictionary/english-russian/root-about-around-sth"
        # word_url = "https://dictionary.cambridge.org/dictionary/english-russian/take-on-sth"
        # word_url = "https://dictionary.cambridge.org/dictionary/english-russian/not-care-for-sth-sb"
        print(word_url)
        page = requests.get(word_url, headers=headers)
        soup = BeautifulSoup(page.text, "html.parser")
        # soup.find

        # there are 3 ways: word, word with multiple meanings, idioms

        # words with single/multiple meanings
        parts = soup.find_all('div', class_='pr entry-body__el')
        # parts = soup.find_all('div', class_='def-block ddef_block')
        print(len(parts))
        data = []

        # try:
        #     if len(parts) == 0:
        #         # parsing
        #         print('оно!')
        #         idiom = soup.find_all(
        #             'h2', class_='headword tw-bw dhw dpos-h_hw')
        #         meaning = soup.find_all('div', class_='def ddef_d db')
        #         mass = [idiom[0].text]
        #         translation = soup.find_all(
        #             'span', class_='trans dtrans dtrans-se')
        #         examples = soup.find_all('span', class_='eg deg')
        #         if len(examples) == 0:
        #             mass = [idiom[0].text, 'idiom',
        #                     translation[0].text, meaning[0].text, []]
        #         else:
        #             mass = [idiom[0].text, 'idiom', translation[0].text, meaning[0].text,
        #                     [ex.text for ex in examples]]
        #         print(mass)

        #         # forming message
        #         msg = f"<b>{mass[0]}</b> <i>({mass[1]})</i> – {mass[2]}\n" \
        #             f"– {mass[3]}\n\n"
        #         if len(mass[4]) != 0:
        #             msg += '<i>🗣️ examples:</i>\n'
        #             for ex in mass[4]:
        #                 msg += f'– {ex}\n'
        #         print(msg)
        #         return [msg, mass]
        #     else:
        #         # parsing
        #         for part in parts:
        #             word = part.find_next('span', class_='hw dhw')
        #             part_of_speech = part.find_next('span', class_='pos dpos')
        #             transcription = part.find_next('span', class_='pron dpron')
        #             # mass = [word.text, part_of_speech.text, transcription.text]
        #             mass = []
        #             for block in part.find_all('div', class_='def-block ddef_block'):
        #                 meaning = block.find_next(
        #                     'div', class_='def ddef_d db')
        #                 translation = block.find_next(
        #                     'span', class_='trans dtrans dtrans-se')
        #                 # examples = part.find_all_next('div', class_='def-body ddef_b')
        #                 examples = part.find_all('span', class_='eg deg')
        #                 qmass = [word, part_of_speech, transcription, translation.text, meaning.text,
        #                          [ex.text for ex in examples]]
        #                 mass.append(qmass)
        #             data.append(mass)
        #         print(mass)

        #         # forming message
        #         msg = f"<b>{
        #             data[0][0]}</b> <i>({data[0][1]})</i> – {data[0][2]}\n"
        #         for i in range(len(data)):
        #             msg += f"{i}. {data[i][0]}\n"
        #             msg += f"– {data[i][1]}\n\n"
        #             if len(data[i][5]) != 0:
        #                 msg += '<i>🗣️ examples:</i>\n'
        #                 for ex in data[i][5]:
        #                     msg += f'– {ex}\n'
        #             msg += '\n–––\n'
        #         print(msg)
        #         return [msg, mass]
        # except IndexError:
        #     cambridge_dict_find_word()

        if len(parts) == 0:
            # parsing
            print('оно!')
            idiom = soup.find_all(
                'h2', class_='headword tw-bw dhw dpos-h_hw')
            if len(idiom) == 0:
                idiom = soup.find_all(
                    'h2', class_='headword tw-bw dhw dpos-h_hw dhw-m')
            meaning = soup.find_all('div', class_='def ddef_d db')
            part_of_speech = soup.find('span', class_='pos dpos').text
            mass = [idiom[0].text]
            translation = soup.find_all(
                'span', class_='trans dtrans dtrans-se')
            examples = soup.find_all('span', class_='eg deg')
            if len(examples) == 0:
                mass = [idiom[0].text, 'idiom',
                        translation[0].text, meaning[0].text, []]
            else:
                mass = [idiom[0].text, part_of_speech, translation[0].text, meaning[0].text,
                        [ex.text for ex in examples]]
            data.append(mass)
            print(data)

            # forming message
            msg = f"<b>{mass[0]}</b> <i>({mass[1]})</i>\n\n" \
                f"1. {mass[2]}\n" \
                f"– {mass[3]}\n\n"
            if len(mass[4]) != 0:
                msg += '<i>🗣️ examples:</i>\n'
                for ex in mass[4]:
                    msg += f'– {ex}\n'
            msg += f'\n\n<i>taken from the <a href="{word_url}">Cambridge Dictionary</a></i>'
            print(msg)
            return [msg, data]
        else:
            # parsing
            for part in parts:
                word = part.find('span', class_='hw dhw').text
                try:
                    part_of_speech = part.find(
                        'span', class_='pos dpos').text
                except AttributeError:
                    part_of_speech = ''
                try:
                    transcription = part.find(
                        'span', class_='pron dpron').text
                except AttributeError:
                    transcription = ''
                print(word, part_of_speech, transcription)
                # qmass = []
                # mass = [word.text, part_of_speech, transcription]
                # mass = []
                for block in part.find_all('div', class_='def-block ddef_block'):
                    print('block')
                    meaning = block.find(
                        'div', class_='def ddef_d db')
                    translation = block.find(
                        'span', class_='trans dtrans dtrans-se')
                    # examples = part.find_all_next('div', class_='def-body ddef_b')
                    examples = block.find_all('span', class_='eg deg')
                    mass = [word, part_of_speech, transcription, translation.text, meaning.text,
                             [ex.text for ex in examples]]
                    # mass.append(qmass)
                    data.append(mass)
                    print(mass)
            print(data)

            # forming message
            if len(data[0][2]) != 0:
                d2 = f'– {data[0][2]}'
            else:
                d2 = ''
            msg = f'<b>{data[0][0]}</b> {d2}\n'
            for i in range(len(data)):
                if i > 0:
                    msg += '\n–––\n'

                if len(data[i][1]) != 0:
                    d1 = f'<i>({data[i][1]})</i>'
                else:
                    d1 = ''

                msg += f"\n{i+1}. {d1} {data[i][3]}\n"
                msg += f"– {data[i][4]}\n"
                if len(data[i][5]) != 0:
                    msg += '\n<i>🗣️ examples:</i>\n'
                    for ex in data[i][5]:
                        msg += f'– {ex}\n'
            msg += f'\n\n<i>taken from the <a href="{word_url}">Cambridge Dictionary</a></i>'

            print(msg)
            return [msg, data]

    else:
        print("BadConnectionError")
        return "BadConnectionError"
