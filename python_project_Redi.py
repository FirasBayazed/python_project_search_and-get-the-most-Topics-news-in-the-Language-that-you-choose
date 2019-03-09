import requests

# Uses Microsoft Cognitive Services API to translate text
# Language of source text is automatically detected
def translate_text(mytext, language='en'):
    # Key to use the translation API
    api_key = '8fd8ff9007414b75883d140d0439fd12'
    # URL of the request to send
    api_url = 'https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&to=' + language
    # HTTP headers of the request to send
    my_headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Ocp-Apim-Subscription-Key': api_key
    }
    # Remove quotes from input string (the translate API does not like them)
    mytext = mytext.replace('"', '-')
    # Body of the request to send
    my_data = '[{"Text":"' + mytext + '"}]'
    print("*", my_data[10:], "*")
    my_data = my_data.encode('utf-8')
    # We have everything now, we can send the request
    r = requests.post(api_url, headers=my_headers, data=my_data)
    # Convert the answer to Python objects (lists and dictionaries)
    response = r.json()
    # Try block, in case translation did not work
    try:
        return response[0]['translations'][0]['text']
    except:
        print('Full API response:', response)
        return "Could not translate this: " + mytext

# Uses the Microsoft Bing Search API to get news on a certain topic, on the default market
# News could come in different languages
# The function returns a list of dictionaries, each with a headline ('name') and URL ('url')
def get_news(topic):
    bingSearchKey = 'eef845eb4ab148cda62da18b4b807d0f'
    url = 'https://api.cognitive.microsoft.com/bing/v7.0/news/search?q=' + text
    my_headers = {
        'Accept': 'application/json',
        'Ocp-Apim-Subscription-Key': bingSearchKey
    }
    r = requests.get(url, headers=my_headers)
    return r.json()['value']

def print_news(news_list, dest_language='en'):
    for news in news_list:
        print(translate_text(news['name'], dest_language))
        print(news['url'])

def print_news_tofile(news_list, filename, dest_language='en'):
    f = open(filename, 'wb')
    f.write('<html><head><title>your search results of topic News</title><meta http-equiv="Content-Type" content="text/html;charset=UTF-8"></head><body>\n'.encode('utf-8'))
    f.write('<h1>Latest news:<h1>\n<br>\n'.encode('utf-8'))
    f.write('<ul>\n'.encode('utf-8'))
    for news in news_list:
        f.write('<li><a href="'.encode('utf-8'))
        f.write(news['url'].encode('utf-8'))
        f.write(u'">'.encode('utf-8'))
        f.write(translate_text(news['name'], dest_language).encode('utf-8'))
        f.write('</a></li>\n'.encode('utf-8'))
    f.write('</ul></body>'.encode('utf-8'))
    f.close()


text = input('On what topic would you like to get some news?\n ')
dest_language = input('To which language would you like your news (2-letter code)?: ')

news_list = get_news(text)

print_news(news_list, dest_language)
print_news_tofile(news_list,  'TopicNews.html', dest_language)

optional=input("do you want to see the most popular results of your search in your Browser in the language you chosen earlier:(yes) or (no)\n").lower()
if optional == "yes":
    import webbrowser, os
    filename = 'file:///' + os.getcwd() + '/' + 'TopicNews.html'
    webbrowser.open_new_tab(filename)
else:
    print("ok you can see your all search results in your console with the original language too ")



