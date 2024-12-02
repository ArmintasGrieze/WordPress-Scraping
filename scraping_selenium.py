import pandas as pd
from selenium import webdriver
import time
from selenium.webdriver.common.by import By



def calculating_words(words_in_titles, word_dict):
    for word in words_in_titles:
        if word not in word_dict.keys():
            word_dict[word] = words_in_titles.count(word)


def calculating_authors(author_names, author_dict):
    for author in author_names:
        if author not in author_dict.keys():
            author_dict[author] = author_names.count(author)


def adding_links(author_dict, thread_links, combined_data):
    for author, count in author_dict.items():
        combined_data.append({
            "Authors": author,
            "Posts": count,
            "URLs": ", ".join(thread_links.get(author, []))
        })


def main():
    driver = webdriver.Chrome()

    combined_data = []
    words_in_titles = []
    author_names = []
    thread_links = {}
    word_dict = {}
    author_dict = {}
    page = 1


    while True:
        driver.get(f"https://wordpress.org/support/plugin/mailpoet/page/{page}")  # Visiting website
        time.sleep(3)
        titles = driver.find_elements(By.CLASS_NAME, "bbp-topic-permalink") # Getting needed info
        authors = driver.find_elements(By.CLASS_NAME, "bbp-topic-started-by") 

        if not titles:
            break

        for title, author in zip(titles, authors): # Adding this information to the list
            author_name = author.text.split()[-1]
            link = title.get_attribute("href")
        
            words_in_titles.extend(title.text.split())
            author_names.append(author_name)
            if author_name in thread_links:
                if isinstance(thread_links[author_name], list):
                    thread_links[author_name].append(link)
                else:
                    thread_links[author_name] = [thread_links[author_name], link]
            else:
                thread_links[author_name] = [link]
                        

        time.sleep(3)

        page += 1

    calculating_words(words_in_titles, word_dict)
    calculating_authors(author_names, author_dict)
    adding_links(author_dict, thread_links, combined_data)

    df_words = pd.DataFrame(list(word_dict.items()), columns=["Words", "Frequency"])
    df_authors = pd.DataFrame(combined_data, columns=["Authors", "Posts", "URLs"])

    pd.concat([df_words, df_authors], axis=1).sort_values(by="Posts", ascending=False).to_csv("out_v2.csv")


if __name__ == "__main__":
    main()