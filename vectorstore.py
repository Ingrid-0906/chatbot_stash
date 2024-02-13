import numpy as np
import requests
import re
import os
import secrets
import time
from datetime import datetime
from bs4 import BeautifulSoup
import chromadb
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
os.environ['OPENAI_API_KEY']='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'

class NewVectorstore:
    def main(self, website):
        website_url=website
        # Parse links to load text
        parse_links = self.get_links(website_url)
        # Create chunks
        chunks = self.get_vectorstore_from_url(parse_links)
        # Embbed chunks and create a vectorstore
        namevector = self.create_embeddings(chunks)
        # Lets say this is the database where the metadata is hosted Metadata do chatbot 
        # # save into a noSQL like mongodb
        metadata={'last_update': datetime.now(), 'namevector': namevector}
        return metadata
    
    def get_links(self, website):
        """
            Function to get the links in a webpage and save them into a dictionary.
            Here, user can select the url that wanna create the chatbot.
            
            Return:
            A list of links and its titles
        """
        
        list_links = list()
        response = requests.get(website)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        if soup.footer or (soup.header or soup.nav): # Look for footer and all links there
            links = soup.find_all("a")
            for link in links:
                if re.match(r"(^/[a-z])", str(link.get("href"))): # Getting just the inner-links
                    if f'{website}{link.get("href")}' not in list_links:
                        list_links.append(f'{website}{link.get("href")}')
                    else:
                        pass
        return list_links
        
    def get_vectorstore_from_url(self, vector_list):
        """
            Split all the website page links into chunks.
            
            Return:
            A list of website chopped into chunks
        """
        website_doc=list()
        website_chunks=list()

        for page_link in vector_list:
            try:
                loader = WebBaseLoader(page_link)
                doc = loader.load()
                website_doc.append(doc)
                time.sleep(3)
            except:
                website_doc.append(np.nan)
        
        for pages in website_doc:
            text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n", "(?<=\. )", " ", ""],
                                                           chunk_size=360,
                                                           chunk_overlap=100)
            all_splits = text_splitter.split_documents(pages)
            website_chunks.append(all_splits)
        return website_chunks
    
    def create_embeddings(self, chunks):
        """
            Function to create the embbeding and save the ids of those the lenght is higher than 2m.
            Here, i setup CHROMADB, but can be any other one.
            
            Return:
            The name of new vectorsctore.
            
            # TO-DO:
            maybe set a limit to hw many text the website must have, like 1M chars?
        """
        
        embeddings=OpenAIEmbeddings()
        namevector = str(secrets.token_hex(15))
        
        # Setup to run locally. Must be used in a Docker file and hosted on AWS EC2
        # or create a server and let it running
        #chroma_client = chromadb.EphemeralClient()
        # Uncomment for persistent client // run on disk
        chroma_client = chromadb.PersistentClient(path="/db")
        Chroma.from_documents(
            chunks[0],
            embeddings,
            client=chroma_client,
            collection_name=namevector
        )
        return namevector

if __name__=='__main__':
    new_vector = NewVectorstore()
    main = new_vector.main('https://magnetis.com.br')
    print(main)