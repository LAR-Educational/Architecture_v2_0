#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wikipedia
import re
import database
import warnings
import threading

from collections import deque

warnings.simplefilter("ignore", UserWarning)

DEFAULT_ANSWER = 'Me desculpe amiguinho, mas não consigo te reponder isso.'


def joinQuery(query):
    newquery = ''
    for x in query:
        newquery += x + ' '
    newquery = newquery[:-1]

    return newquery


class fileHelper(object):
    def __init__(self):
        self.general = database.File()
        self.personal = None
        self.queue = deque()

        self.searchThread = threading.Thread(target=self._searchThread)
        self.searchThread.start()

    def _searchThread(self):
        self.running = True
        while self.running or len(self.queue) > 0:
            if len(self.queue) > 0:
                query = self.queue.popleft()
                self.searchFile(
                    query[0], sentences=2, person=query[1], preference=query[2]
                    )

    def addSearchQueue(self, query, person=None, preference=''):
        self.queue.append((query, person, preference))

    # Pesquisa a página mais próxima de query da wikipedia
    # e procura a seção query, se não achado devolver o resumo.
    def searchFile(
            self, query, section='', sentences=0, person=None, preference=''):
        query = joinQuery(query)

        try:
            query = query.decode('utf-8')
            section = section.decode('utf-8')
        except UnicodeDecodeError as e:
            print(e)

        if query is '':
            return 'Por favor coloque algo para pesquisar.'

        ret = self.general.search(query+section)

        if person is not None:
            if not self.checkPreference(person, preference):
                self.addPreference(person, query, preference)

        if ret:
            return ret

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

        if(found):
            # Separa as sentenças que foram requisitado.
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

        self.general.write(query+section, ret)

        return ret

    def linkPerson(self, person):
        if self.personal is None:
            self.personal = database.File(person)
            return
        self.personal.close()
        self.personal = database.File(person)

    def addPreference(self, person, answer, preference):
        self.linkPerson(person)
        self.personal.write(preference, answer)

    def checkPreference(self, person, preference):
        self.linkPerson(person)
        if self.personal.search(preference) is None:
            return False
        return True

    def getPreferences(self, person):
        self.linkPerson(person)
        return self.personal.ram

    def join(self):
        self.running = False
        self.searchThread.join()

    def close(self):
        self.general.close()
        if self.personal is not None:
            self.personal.close()


def example():
    helper = fileHelper()
    print(u'Olá abiguinhos')
    print(u'Qual é seu nome?')
    nome = raw_input()

    print(u'Qual é a sua idade?')
    answer = raw_input()
    helper.addPreference(nome, answer, 'idade')

    print(u'Qual é o seu esporte favorito?')
    answer = raw_input()
    helper.addSearchQueue([answer], nome, 'esporte favorito')

    print(u'Qual é a sua comida favorita?')
    answer = raw_input()
    helper.addSearchQueue([answer], nome, 'comida favorita')

    print(u'Qual é a sua música favorita?')
    answer = raw_input()
    helper.addSearchQueue([answer], nome, 'musica favorita')

    helper.join()

    preferences = helper.getPreferences(nome)
    try:
        print(u'Sobre seu esporte preferido: {}'.format(
            helper.searchFile(
                [preferences['esporte favorito'].encode('utf-8')])))
        print(u'Sobre sua comida preferida: {}'.format(
            helper.searchFile(
                [preferences['comida favorita'].encode('utf-8')])))
        print(u'Sobre sua música preferida: {}'.format(
            helper.searchFile(
                [preferences['musica favorita'].encode('utf-8')])))
    except Exception as e:
        print(e)

    helper.close()


if __name__ == "__main__":
    example()
