import ollama
import sys_msgs
import requests
import trafilatura
from bs4 import BeautifulSoup

assistant_convo = [sys_msgs.assistant_msg]

def search_or_not():
    sys_msg=sys_msgs.search_or_not_msg

    response=ollama.chat(
        model='mistral',
        messages=[{'role':'assistant','content':sys_msg},assistant_convo[-1]]
    )

    content =response['message']['content']

    if 'true' in content.lower():
        return True
    else:
        return False

def query_generator():
    sys_msg = sys_msgs.query_msg
    query_msg = f'CREATE A SEARCH QUERY FOR THIS PROMPT: \n{assistant_convo[-1]}'

    response = ollama.chat(
        model='mistral',
        messages=[{'role':'assistant','content':sys_msg},{'role':'assistant','content':query_msg}]
    )
    

def Duckduckgo_search(query):
    headers={
        "User-Agent":"Mozilla/5.O (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.ø.3029. llø Safari/537.36"
    }
    url= f'https://html.duckduckgo.com/html/?q={query}'
    responese= requests.get(url,headers=headers)
    responese.raise_for_status()

    soup=BeautifulSoup(responese.text,'html.parser')
    results=[]
    
    for i, result in enumerate(soup.find_all('div',class_='result'),start=1):
        if i>10:
            break

        title_tag=result.find('a',class_='result_a')
        if not title_tag:
            continue

        link=title_tag['href']
        snippet_tag=result.find('a',class_='result_snippet')
        snippet=snippet_tag.text.strip() if snippet_tag else 'No description available'

        results.append({
            'id':i,
            'link':link,
            'search_decription':snippet
        })

    return results

def best_search_result(s_results, query):
    sys_msg = sys_msgs.best_search_msg

    best_msg = f'SEARCH_RESULTS: {s_results} \nUSER_PROMPT: {assistant_convo[-1]} \nSEARCH_QUERY: {query}'

    for _ in range(2):
        try:
            response = ollama.chat(
                model='deepseek-r1:8b',
                messages=[{'role': 'system', 'content': sys_msg}, {'role': 'user', 'content': best_msg}]
            )
            return int(response['message']['content'])
        except:
            continue

    return 0

def scrape_webpage(url):
    try:
        download= trafilatura.fetch_url(url=url)
        return trafilatura.extract(download, include_formatting=True,include_links=True)
    except Exception as e:
        return None
    
def ai_search():
    context = None
    print('GENERATING SEARCH QUERY')
    search_query = query_generator()

    if not search_query:  # Handle None case
        print("ERROR: Search query generation failed.")
        return None

    if search_query[0] == '"':
        search_query = search_query[1:-1]  # Fix slicing issue

    search_results = Duckduckgo_search(search_query)
    context_found = False

    while not context_found and len(search_results) > 0:
        best_result = best_search_result(s_results=search_results, query=search_query)

        try:
            page_link = search_results[best_result]['link']
        except IndexError:
            print("FAILED TO SELECT BEST SEARCH RESULT, TRYING AGAIN.")
            continue

        page_text = scrape_webpage(page_link)
        search_results.pop(best_result)

        if page_text and contains_data_needed(search_content=page_text, query=search_query):
            context = page_text
            context_found = True

    return context


def contains_data_needed(search_content, query):
    sys_msg = sys_msgs.contains_data_msg

    needed_prompt = f'PAGE_TEXT: {search_content} \nUSER_PROMPT: {assistant_convo[-1]} \nSEARCH_QUERY: {query}'

    response = ollama.chat(
        model='deepseek-r1:8b',
        messages=[{'role': 'system', 'content': sys_msg}, {'role': 'user', 'content': needed_prompt}]
    )

    content = response['message']['content']

    if 'true' in content.lower():
        return True
    else:
        return False

def stream_assistant_response():
    global assistant_convo
    response_stream = ollama.chat(model='mistral', messages=assistant_convo, stream=True)
    complete_response=''
    print('ASSISTANST:')
    
    for chunk in response_stream:
        print(chunk['message']['content'], end='', flush=True)
        complete_response += chunk['message']['content']
    
    assistant_convo.append({'role':'assistant','content':complete_response})
    print('\n\n')

def main():
    global assistant_convo

    while True:
        prompt = input('USER: \n')
        assistant_convo.append({'role':'user','content':prompt})
        stream_assistant_response()

        if search_or_not():
            context= ai_search()
            assistant_convo=assistant_convo[:-1]

            if context:
                prompt = f'SEARCH RESULT: {context} \n\nUSER PROMPT: {prompt}'
            else:
                prompt = (
                    f'USER PROMPT: \n{prompt} \n\nFAILED SEARCH: \nThe '
                    'AI search model was unable to extract any reliable data. Explain that '
                    'and ask if the user would like you to search again or respond '
                    'without web search context. Do not respond if a search was needed '
                    'and you are getting this message with anything but the above request '
                    'of how the user would like to proceed'
                )

            assistant_convo.append({'role':'user','content':prompt})


if __name__ == '__main__':
  main()