from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'search-buzzni-hnnrarosn63fw5tcbxoh4bpare.ap-northeast-2.es.amazonaws.com', 'port': 80}])


def search(keyword):
    search_body = {"query": {"match": {'key': keyword}}}
    return es.search(index='review', doc_type='noun', body=search_body)