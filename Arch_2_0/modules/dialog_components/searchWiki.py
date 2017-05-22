#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wikipedia
import re

# Pesquisa a página mais próxima de query da wikipedia e procura a seção query, se não achado devolver o resumo.
def searchWiki(query, section='', sentences = 0):
    # Coloca a linguagem da wikipedia em português
    wikipedia.set_lang("pt")
    
    # Pega a página e as seções da página
    try:
        page = wikipedia.page(query)
    except:
        topics = wikipedia.search(query)
        page = wikipedia.page(topics[1])
        
    sections = page.sections
    found = None

    ret = wikipedia.summary(query, sentences=sentences)

    # Procura a seção requesitada
    for sec in sections:
        if(sec.lower() == section.lower()):
            ret = page.section(sec)
            foud = True
            break

    # Retira todos as partes que estão entre chaves de dentro para fora.
    while re.search('\{[^{}]*\}', ret):
        ret = re.sub('\{[^{}]*\}', '', ret)

    # Retira os espaços extras.
    ret = re.sub('\s{2,}|[\t\n\r\f\v]', ' ', ret)
    
    if(found):
        # Separa as sentenças que foram requisitado.
        temp = ret
        ret = ''
        for i in range(sentences):
            m = re.findall("([^.]*).(.*)", temp)
            if(len(m[0]) == 2):
                ret += m[0][0] + '.'
                temp = m[0][1]
            elif(len(m[0]) == 1):
                ret += m[0][0] + '.'
            else:
                break

    return ret
