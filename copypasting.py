import pyperclip
import requests
from bs4 import BeautifulSoup
import requests
import json
import requests
import lxml
import webbrowser
import web


# do a brave search from the output of pyperclip.paste()


def get_organic_results():
    dunefilm = pyperclip.paste()
    # https://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls
    params = {
        'q': dunefilm,       # query
        'source': 'web',        # source
        'tf': 'at',             # publish time (by default any time)
        'offset': 0             # pagination (start from page 1)
    }

    # https://docs.python-requests.org/en/master/user/quickstart/#custom-headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }

    brave_organic_search_results = []

    while True:
        html = requests.get('https://search.brave.com/search',
                            headers=headers, params=params)
        soup = BeautifulSoup(html.text, 'lxml')

        if soup.select_one('.ml-15'):
            params['offset'] += 1
        else:
            break

        page = {}
        page['page'] = params['offset']
        page['items'] = []

        for result in soup.select('.snippet'):
            title = result.select_one('.snippet-title').get_text().strip()
            favicon = result.select_one('.favicon').get('src')
            link = result.select_one('.result-header').get('href')
            displayed_link = result.select_one(
                '.snippet-url').get_text().strip().replace('\n', '')

            snippet = result.select_one(
                '.snippet-content .snippet-description , .snippet-description:nth-child(1)').get_text()
            snippet = snippet.strip().split(
                '\n')[-1].lstrip() if snippet else None

            snippet_image = result.select_one('.video-thumb img , .thumb')
            snippet_image = snippet_image.get('src') if snippet_image else None

            rating_and_votes = result.select_one('.ml-10')
            rating = rating_and_votes.get_text().strip().split(
                ' - ')[0] if rating_and_votes else None
            votes = rating_and_votes.get_text().strip().split(
                ' - ')[1] if rating_and_votes else None

            sitelinks_container = result.select(
                '.deep-results-buttons .deep-link')
            sitelinks = None

            if sitelinks_container:
                sitelinks = []
                for sitelink in sitelinks_container:
                    sitelinks.append({
                        'title': sitelink.get_text().strip(),
                        'link': sitelink.get('href')
                    })

            page['items'].append({
                'title': title,
                'favicon': favicon,
                'link': link,
                'displayed_link': displayed_link,
                'snippet': snippet,
                'snippet_image': snippet_image,
                'rating': rating,
                'votes': votes,
                'sitelinks': sitelinks
            })

        brave_organic_search_results.append(page)

    print(json.dumps(brave_organic_search_results, indent=2, ensure_ascii=False))
# open the search results in the browser
    webbrowser.open('https://search.brave.com/search?q='+dunefilm)

# open the first five links in the browser
    for i in range(5):
        webbrowser.open(brave_organic_search_results[0]['items'][i]['link'])
    # for page in brave_organic_search_results:
    #     items = min(5, len(page['items']))
    #     for item in range(items):

    #         webbrowser.open(page['items'][item]['link'])


if __name__ == '__main__':
    get_organic_results()
