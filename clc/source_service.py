#!/usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:quincy qiang
@license: Apache Licence
@file: search.py
@time: 2023/04/17
@contact: yanqiangmiffy@gamil.com
@software: PyCharm
@description: coding..
"""

import os
import docx2txt

# from duckduckgo_search import ddg
from langchain_community.document_loaders import PyPDFLoader
from langchain.schema import Document
from langchain.document_loaders import UnstructuredWordDocumentLoader
from langchain.document_loaders import UnstructuredFileLoader
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS



class SourceService(object):
    def __init__(self, config):
        self.vector_store = None
        self.config = config
        self.embeddings = HuggingFaceEmbeddings(model_name=self.config.embedding_model_name)
        self.docs_path = self.config.docs_path
        self.vector_store_path = self.config.vector_store_path

    def init_source_vector(self):
        """
        初始化本地知识库向量
        :return:
        """
        docs = []
        for doc in os.listdir(self.docs_path):
            if doc.endswith('.txt'):
                print(doc)
                loader = UnstructuredFileLoader(f'{self.docs_path}/{doc}', mode="elements")
                doc = loader.load()
                docs.extend(doc)
            elif doc.endswith(".pdf"):
                print(doc)
                loader = PyPDFLoader(f'{self.docs_path}/{doc}')
                doc = loader.load()
                docs.extend(doc)
            elif doc.endswith(".docx"):
                print(doc)
                text = docx2txt.process(f'{self.docs_path}/{doc}')
                print(text)
                doc = [Document(page_content=text)]
                # loader = UnstructuredWordDocumentLoader(f'{self.docs_path}/{doc}', mode="elements")
                # doc = loader.load()
                docs.extend(doc)
            # elif doc.endswith("rel18"):
            #     files = []
            #     for file in os.listdir("/home/xiaziyun/Chinese-LangChain/docs/rel18"):
            #         if file.endswith('.docx'):
            #             text = docx2txt.process(f'{self.docs_path}/{doc}/{file}')
            #             doc = [Document(page_content=text)]
            #             docs.extend(doc)
        # print(docs)
        self.vector_store = FAISS.from_documents(docs, self.embeddings)
        exit("done")
        self.vector_store.save_local(self.vector_store_path)


    def add_document(self, document_path):
        doc = ''
        if document_path.endswith('.txt'):
            loader = UnstructuredFileLoader(document_path, mode="elements")
            doc = loader.load()
        elif document_path.endswith('.pdf'):
            loader = PyPDFLoader(document_path)
            doc = loader.load()
        elif document_path.endswith(".docx"):
            # loader = UnstructuredWordDocumentLoader(document_path, mode="elements")
            # doc = loader.load()
            text = docx2txt.process(f'{self.docs_path}/{doc}')
            doc = [Document(page_content=text)]
        # elif doc.endswith("rel18"):
        #     files = []
        #     for file in os.listdir("/home/xiaziyun/Chinese-LangChain/docs/rel18"):
        #         if file.endswith('.docx'):
        #             text = docx2txt.process(f'{self.docs_path}/{doc}/{file}')
        #             doc = [Document(page_content=text)]
        self.vector_store.add_documents(doc)
        self.vector_store.save_local(self.vector_store_path)

    def load_vector_store(self, path):
        if path is None:
            self.vector_store = FAISS.load_local(self.vector_store_path, self.embeddings)
        else:
            self.vector_store = FAISS.load_local(path, self.embeddings)
        return self.vector_store

    def search_web(self, query):

        # SESSION.proxies = {
        #     "http": f"socks5h://localhost:7890",
        #     "https": f"socks5h://localhost:7890"
        # }
        try:
            results = ddg(query)
            web_content = ''
            if results:
                for result in results:
                    web_content += result['body']
            return web_content
        except Exception as e:
            print(f"网络检索异常:{query}")
            return ''
# if __name__ == '__main__':
#     config = LangChainCFG()
#     source_service = SourceService(config)
#     source_service.init_source_vector()
#     search_result = source_service.vector_store.similarity_search_with_score('科比')
#     print(search_result)
#
#     source_service.add_document('/home/searchgpt/yq/Knowledge-ChatGLM/docs/added/科比.txt')
#     search_result = source_service.vector_store.similarity_search_with_score('科比')
#     print(search_result)
#
#     vector_store=source_service.load_vector_store()
#     search_result = source_service.vector_store.similarity_search_with_score('科比')
#     print(search_result)