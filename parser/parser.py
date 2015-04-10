import multiprocessing
import bz2
import sys, os
import py_compile
from codecs import open

py_compile.compile(
    "/home/daria/anaconda/lib/python2.7/site-packages/gensim-0.10.3-py2.7-linux-x86_64.egg/gensim/utils.py")
import gensim

'''sys.stdout = open("/home/daria/PycharmProjects/first/Anarchism", 'w', 'utf8')'''


def process_article((title, text, number)):
    text = gensim.corpora.wikicorpus.filter_wiki(text)
    return title.encode('utf8'), gensim.utils.simple_preprocess(text)


def convert_wiki(infile, processes=multiprocessing.cpu_count()):
    if __name__ == '__main__':
        pool = multiprocessing.Pool(processes)
        texts = gensim.corpora.wikicorpus._extract_pages(bz2.BZ2File(infile)) # generato
        #texts = gensim.corpora.wikicorpus._extract_pages(infile)  # generator
        ignore_namespaces = 'Wikipedia Category File Portal Template MediaWiki User Help Book Draft'.split()
        # process the corpus in smaller chunks of docs, because multiprocessing.Pool
        # is dumb and would try to load the entire dump into RAM...
        for group in gensim.utils.chunkize(texts, chunksize=10 * processes):
            for title, tokens in pool.imap(process_article, group):
                '''print tokens'''
                if len(tokens) >= 50 and not any(title.startswith(ignore + ':') for ignore in ignore_namespaces):
                    yield title.replace('\t', ' '), tokens
        pool.terminate()

i = 0
for title, tokens in convert_wiki('/home/daria/enwiki-20150304-pages-articles.xml.bz2'):
    i = i + 1
    '''print "%s\t%s" % (title, ' '.join(tokens))'''
    file = open("/home/daria/articles/" +title.replace('/', '_'), "w+", "utf8")
    file.write(' '.join(tokens))
    file.close()
    print title.replace('/', '_')
    if i == 5000:
        break