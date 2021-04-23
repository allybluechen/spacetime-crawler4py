import re
from urllib.parse import urlparse


def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]


def extract_next_links(url, resp):
    # Implementation required.
    # Checks for valid response
    if resp.status >= 300:
        return list()

    urlList = []

    return list()


def is_valid(url):
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print("TypeError for ", parsed)
        raise


# Oscars implementation, feel free to change
def tokenize(text_file_path: str):
    tokens = []
    with open(text_file_path, 'r') as file:
        for line in file:
            for word in line.split():
                new_word = ""

                for character in word:
                    if character.isalnum():
                        new_word += character
                    else:
                        if new_word != "":
                            new_word = new_word.lower()
                            tokens.append(new_word)
                            new_word = "";
                if new_word != "":
                    new_word = new_word.lower()
                    tokens.append(new_word)
    file.close()
    return tokens
