# -*- coding: utf-8 -*-

import wikipedia
import re
import warnings

warnings.simplefilter("ignore", UserWarning)

DEFAULT_ANSWER = 'Me desculpe amiguinho, mas não consigo te reponder isso.'.decode('utf-8')

def search(query, section='', sentences=0):


    try:
        query = query#.decode('utf-8')
        section = section.decode('utf-8')
    except UnicodeDecodeError as e:
        print(e)

    if query is '':
        return 'Por favor coloque algo para pesquisar.'

        # Coloca a linguagem da wikipedia em português
    wikipedia.set_lang("pt")

        # Pega a página e as seções da página
    try:
        page = wikipedia.page(query)
        ret = wikipedia.summary(query, sentences=sentences)
    except wikipedia.exceptions.DisambiguationError as e:
        if len(e.options) > 0:
            nquery = e.options[0]
        else:
            return DEFAULT_ANSWER
        page = wikipedia.page(nquery)
        ret = wikipedia.summary(nquery, sentences=sentences)
    except wikipedia.exceptions.PageError:
        return DEFAULT_ANSWER

    sections = page.sections
    found = None

    # Procura a seção requesitada
    for sec in sections:
        if(sec.lower() == section.lower()):
            ret = page.section(sec)
            found = True
            break

        # Retira todos as partes que estão entre chaves de dentro para fora.
    while re.search(r'\{[^{}]*\}', ret):
        ret = re.sub(r'\{[^{}]*\}', '', ret)

        # Retira os espaços extras.
    ret = re.sub(r'\s{2,}|[\t\n\r\f\v]', ' ', ret)

        # Retira os espaços extras.
    ret = re.sub('=', ' ', ret)
        
    if(found):
            # Separa as sentenças que foram requisitadas.
        temp = ret
        ret = ''
        for i in range(sentences):
            m = re.findall(r'([^.]*).(.*)', temp)
            if(len(m[0]) == 2):
                ret += m[0][0] + '.'
                temp = m[0][1]
            elif(len(m[0]) == 1):
                ret += m[0][0] + '.'
            else:
                break

    return ret

if __name__ == "__main__":
    print(search('batata'))