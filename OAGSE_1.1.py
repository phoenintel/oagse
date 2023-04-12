print('Loading modules...')
import questionary
from googlesearch import search
import requests
from bs4 import BeautifulSoup
import re
import nltk
nltk.download('punkt')
print('Done!')

def ask_question():
    print('Loading SOGS...')
    print('Done!')
    print('******************')
    print('*****SOGS 1.1*****')
    print('****************** \n optimised to find information quickly and easily \n This work is licensed under a CC BY-NC-SA 4.0 License. Read it here: https://creativecommons.org/licenses/by-nc-sa/4.0/ \n Source code: https://github.com/phoenintel/oagse')
    print(' \n --------------------\n ')

    question = questionary.text("Entrez votre requête:").ask()
    return question

def search_google(query):
    search_results = list(search(query, num_results=10))
    return search_results

def extract_information(search_result):
    page = requests.get(search_result)
    page.encoding = "utf-8"
    soup = BeautifulSoup(page.content, "html.parser")
    paragraphs = soup.find_all("p")
    text = ""
    for paragraph in paragraphs:
        text += paragraph.get_text().encode('utf-8').decode('utf-8')
    sentences = nltk.sent_tokenize(text)
    for sentence in sentences:
        if "?" in sentence:
            continue
        answer = sentence
        source = re.search("(?P<url>https?://[^\s]+)", str(soup)).group("url")
        return answer, source
    return "", ""


def main():
    while True:
        question = ask_question()
        search_results = search_google(question)
        answer_found = False
        for i, result in enumerate(search_results):
            try:
                answer, source = extract_information(result)
                if answer != "":
                    print(f"Résultat {i+1}: {answer}")
                    print(f"Source: {source}\n")
                    answer_found = True
            except:
                pass
        if not answer_found:
            print("Désolé, je n'ai pas trouvé de réponse à votre question.")

if __name__ == "__main__":
    main()
