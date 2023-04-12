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
    print('Loading OAGSE...')
    print('Done!')
    print('******************')
    print('*****OAGSE 1.1****')
    print('****************** \n optimised to find information quickly and easily \n This work is licensed under a CC BY-NC-SA 4.0 License. Read it here: https://creativecommons.org/licenses/by-nc-sa/4.0/ \n Source code: https://github.com/phoenintel/oagse')
    print("")
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
    answer = ""
    for sentence in sentences:
        if "?" in sentence:
            continue
        answer += sentence
    source = re.search("(?P<url>https?://[^\s]+)", str(soup)).group("url")
    return answer, source

def main():
    while True:
        question = ask_question()
        search_results = search_google(question)
        answer_found = False
        answers = []
        sources = []
        for i, result in enumerate(search_results):
            try:
                answer, source = extract_information(result)
                if answer != "":
                    answers.append(answer)
                    sources.append(source)
                    answer_found = True
            except:
                pass
        if not answer_found:
            print("sorry, no answer was found for your question. Please try to formulate it more simply, for example with keywords.")
        else:
            print(f"Done! {answers[0]}")
            print("Sources:")
            for i, source in enumerate(sources):
                print(f"{i+1}. {source}")
            print("\n")
        
if __name__ == "__main__":
    main()
