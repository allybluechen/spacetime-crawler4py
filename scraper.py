import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup as bs


def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]


def extract_next_links(url, resp):
    urlList = []
    subdomains = []
    parsed = urlparse(url)
    maxwords = 0
    longestpage = ""
    words = []

    if(200 <= resp.status <= 202 and is_valid(url)):
        #get the raw_response content and parse it into HTML using beautifulsoup
        html = bs(resp.raw_response.content, "html.parser")
        if(not html.find('embed', attrs={'type': "application/pdf"})):
            # find all links from the html and append it to the urlList list
            for link in html.findAll('a', attrs={'href': re.compile("^(http|https)://")}):
                urlList.append(link.get('href'))
                if "ics.uci.edu" in parsed.netloc: #4 
                    if parsed.netloc != "ics.uci.edu" and parsed.netloc != "www.ics.uci.edu":
                        subdomains.append(parsed.netloc.split('.')[0])
        words = tokenize(html.getText())
        if maxwords < len(words):
            maxwords = len(words)
            longestpage = url
    if(400 <= resp.status <= 599 and is_valid(url)):
        pass

    print("max words on one page:", maxwords)
    print("longest page:", longestpage) #2 
    print("50 most common words:", output(wordFreq(words))) #3 
    print("subdomains:", output_alpha(wordFreq(subdomains))) #4 

    return urlList


def is_valid(url):
    wanted = ['ics.uci.edu', 'cs.uci.edu','informatics.uci.edu','stat.uci.edu',
    'today.uci.edu/department/information_computer_sciences']
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        if "pdf" in url:
            return False
        if "publications" in url:
            return False
        for validDomain in wanted:
            # remove fragment
            if(parsed.fragment != ''):
                return False
            if validDomain in url:
                return not re.match(
                    r".*\.(css|js|bmp|gif|jpe?g|ico"
                    + r"|png|tiff?|mid|mp2|mp3|mp4"
                    + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
                    + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
                    + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
                    + r"|epub|dll|cnf|tgz|sha1"
                    + r"|thmx|mso|arff|rtf|jar|csv"
                    + r"|rm|smil|wmv|swf|wma|zip|rar|gz|ppsx)$", parsed.path.lower())
        return False
        

    except TypeError:
        print("TypeError for ", parsed)
        raise

# Ally's tokenize, wordfreq, and output functions 
def tokenize(contents):
    tokens = re.findall("[\w']+", contents)
    return tokens

def wordFreq(l):
    freq = []
    for w in l:
        freq.append(l.count(w))
    return list(set(zip(l,freq)))

def output(freq):
    stopwords = ["a", "able", "about", "above", "abst", "accordance",
        "according", "accordingly", "across", "act", "actually", "added", "adj", "affected",
        "affecting", "affects", "after", "afterwards", "again", "against", "ah", "all", "almost",
        "alone", "along", "already", "also", "although", "always", "am", "among", "amongst", "an",
        "and", "announce", "another", "any", "anybody", "anyhow", "anymore", "anyone", "anything", 
        "anyway", "anyways", "anywhere", "apparently", "approximately", "are", "aren", "arent", 
        "arise", "around", "as", "aside", "ask", "asking", "at", "auth", "available", "away", 
        "awfully", "b", "back", "be", "became", "because", "become", "becomes", "becoming", "been", 
        "before", "beforehand", "begin", "beginning", "beginnings", "begins", "behind", "being", 
        "believe", "below", "beside", "besides", "between", "beyond", "biol", "both", "brief", 
        "briefly", "but", "by", "c", "ca", "came", "can", "cannot", "can't", "cause", "causes", 
        "certain", "certainly", "co", "com", "come", "comes", "contain", "containing", "contains", 
        "could", "couldnt", "d", "date", "did", "didn't", "different", "do", "does", "doesn't", 
        "doing", "done", "don't", "down", "downwards", "due", "during", "e", "each", "ed", "edu", 
        "effect", "eg", "eight", "eighty", "either", "else", "elsewhere", "end", "ending", "enough", 
        "especially", "et", "et-al", "etc", "even", "ever", "every", "everybody", "everyone", 
        "everything", "everywhere", "ex", "except", "f", "far", "few", "ff", "fifth", "first", 
        "five", "fix", "followed", "following", "follows", "for", "former", "formerly", "forth", 
        "found", "four", "from", "further", "furthermore", "g", "gave", "get", "gets", "getting", 
        "give", "given", "gives", "giving", "go", "goes", "gone", "got", "gotten", "h", "had", 
        "happens", "hardly", "has", "hasn't", "have", "haven't", "having", "he", "hed", "hence", 
        "her", "here", "hereafter", "hereby", "herein", "heres", "hereupon", "hers", "herself", 
        "hes", "hi", "hid", "him", "himself", "his", "hither", "home", "how", "howbeit", "however", 
        "hundred", "i", "id", "ie", "if", "i'll", "im", "immediate", "immediately", "importance", 
        "important", "in", "inc", "indeed", "index", "information", "instead", "into", "invention", 
        "inward", "is", "isn't", "it", "itd", "it'll", "its", "itself", "i've", "j", "just", "k", 
        "keep", "keeps", "kept", "kg", "km", "know", "known", "knows", "l", "largely", "last", 
        "lately", "later", "latter", "latterly", "least", "less", "lest", "let", "lets", "like", 
        "liked", "likely", "line", "little", "'ll", "look", "looking", "looks", "ltd", "m", "made", 
        "mainly", "make", "makes", "many", "may", "maybe", "me", "mean", "means", "meantime", 
        "meanwhile", "merely", "mg", "might", "million", "miss", "ml", "more", "moreover", "most", 
        "mostly", "mr", "mrs", "much", "mug", "must", "my", "myself", "n", "na", "name", "namely", 
        "nay", "nd", "near", "nearly", "necessarily", "necessary", "need", "needs", "neither", 
        "never", "nevertheless", "new", "next", "nine", "ninety", "no", "nobody", "non", "none", 
        "nonetheless", "noone", "nor", "normally", "nos", "not", "noted", "nothing", "now", "nowhere", 
        "o", "obtain", "obtained", "obviously", "of", "off", "often", "oh", "ok", "okay", "old", 
        "omitted", "on", "once", "one", "ones", "only", "onto", "or", "ord", "other", "others", 
        "otherwise", "ought", "our", "ours", "ourselves", "out", "outside", "over", "overall", 
        "owing", "own", "p", "page", "pages", "part", "particular", "particularly", "past", "per", 
        "perhaps", "placed", "please", "plus", "poorly", "possible", "possibly", "potentially", "pp", 
        "predominantly", "present", "previously", "primarily", "probably", "promptly", "proud", 
        "provides", "put", "q", "que", "quickly", "quite", "qv", "r", "ran", "rather", "rd", "re", 
        "readily", "really", "recent", "recently", "ref", "refs", "regarding", "regardless", "regards", 
        "related", "relatively", "research", "respectively", "resulted", "resulting", "results", "right",
        "run", "s", "said", "same", "saw", "say", "saying", "says", "sec", "section", "see", "seeing", 
        "seem", "seemed", "seeming", "seems", "seen", "self", "selves", "sent", "seven", "several", 
        "shall", "she", "shed", "she'll", "shes", "should", "shouldn't", "show", "showed", "shown", 
        "showns", "shows", "significant", "significantly", "similar", "similarly", "since", "six", 
        "slightly", "so", "some", "somebody", "somehow", "someone", "somethan", "something", "sometime", 
        "sometimes", "somewhat", "somewhere", "soon", "sorry", "specifically", "specified", "specify", 
        "specifying", "still", "stop", "strongly", "sub", "substantially", "successfully", "such", 
        "sufficiently", "suggest", "sup", "sure", "t", "take", "taken", "taking", "tell", "tends", 
        "th", "than", "thank", "thanks", "thanx", "that", "that'll", "thats", "that've", "the", 
        "their", "theirs", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", 
        "thered", "therefore", "therein", "there'll", "thereof", "therere", "theres", "thereto", 
        "thereupon", "there've", "these", "they", "theyd", "they'll", "theyre", "they've", "think", 
        "this", "those", "thou", "though", "thoughh", "thousand", "throug", "through", "throughout", 
        "thru", "thus", "til", "tip", "to", "together", "too", "took", "toward", "towards", "tried", 
        "tries", "truly", "try", "trying", "ts", "twice", "two", "u", "un", "under", "unfortunately", 
        "unless", "unlike", "unlikely", "until", "unto", "up", "upon", "ups", "us", "use", "used", 
        "useful", "usefully", "usefulness", "uses", "using", "usually", "v", "value", "various", 
        "'ve", "very", "via", "viz", "vol", "vols", "vs", "w", "want", "wants", "was", "wasnt", "way", 
        "we", "wed", "welcome", "we'll", "went", "were", "werent", "we've", "what", "whatever", "what'll", 
        "whats", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", 
        "wheres", "whereupon", "wherever", "whether", "which", "while", "whim", "whither", "who", "whod", 
        "whoever", "whole", "who'll", "whom", "whomever", "whos", "whose", "why", "widely", "willing", 
        "wish", "with", "within", "without", "wont", "words", "world", "would", "wouldnt", "www", 
        "x", "y", "yes", "yet", "you", "youd", "you'll", "your", "youre", "yours", "yourself", 
        "yourselves", "you've", "z", "zero"]
    l = []
    count = 0
    freq.sort(key = lambda x: -x[1])
    for i in freq:
        if i[0] not in stopwords:
            l.append(str(i[0] + " " + str(i[1])))
            count += 1
            if count == 50: 
                break
    return l

def output_alpha(freq):
    l = []
    freq.sort()
    for i in freq:
        l.append(str(i[0] + ", " + str(i[1])))
    return l
