#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs


# Classe criada para gerenciar os arquivos que servirão
# para guardar as perguntas e repostas.
class File(object):
    def __init__(self, filename='knowledge'):
        # Inicializa as varáveis usadas no código.
        self.filename = filename
        self.ram = {}

        # Confere se existe o folder que será salvo os arquivos.
        if os.path.isdir('./Usuarios') is False:
            os.mkdir('./Usuarios')

        # Confere se já existe algo guardado e o coloca na ram
        # se não só criar um arquivo novo.
        try:
            self.file = codecs.open(
                './Usuarios/{}.dat'.format(self.filename),
                'r+', encoding='utf-8')

            # Le as entradas do arquivo.
            for line in self.file:
                temp = self.file.readline().splitlines()
                line = line.splitlines()
                self.ram[line[0]] = temp[0]
        except Exception as e:
            print(e)
            self.file = codecs.open(
                './Usuarios/{}.dat'.format(
                    self.filename), 'w+', encoding='utf-8')

    # Escreve a entrada no arquivo.
    def write(self, key, content):
        if(self.file is None):
            self.file = codecs.open(
                './Usuarios/{}.dat'.format(
                    self.filename), 'a+', encoding='utf-8')

        if key not in self.ram:
            self.ram[key] = content

            self.file.write(key + '\n')
            self.file.write(content + '\n')

    # Procura uma pergunta na ram, retorna a resposta
    # ou nada se não ele não tiver ela.
    def search(self, query):
        if query in self.ram:
            return self.ram[query]
        else:
            return None

    # Limpa todos os arquivos utilizados.
    def clean(self):
        self.close()
        self.file = codecs.open(
            './Usuarios/{}.dat'.format(self.filename), 'w+', encoding='utf-8')

    # Fecha todos os arquivos utilizados.
    def close(self):
        self.file.close()
