import requests


def test_create_section():
    json = {
        "query": '''   
        mutation {createSection(theme:"crew", description:"new"){
        ok
        }}
      '''
    }
    session = requests.Session()
    session.trust_env = False
    r = session.post('http://docker.for.mac.localhost:8080/graphql', json=json)
    assert r.json() == {'data': {'createSection': {'ok': True}}}


def test_get_section():
    json = {
        "query": '''
        query {getSection(id_:1){
        theme
        }}
      '''
    }
    r = requests.get('http://docker.for.mac.localhost:8080/graphql', json=json)
    assert r.json() == {'data': {'getSection': {'theme': 'crew'}}}


def test_create_posts():
    json = {
        "query": '''
        mutation {createPost(theme:"crew", description:"new", sectionId:1){
        ok
        }}
      '''
    }
    r = requests.post('http://docker.for.mac.localhost:8080/graphql', json=json)
    assert r.json() == {'data': {'createPost': {'ok': True}}}


def test_get_post():
    json = {
        "query": '''
        query {getPost(id_:1){
        theme
        }}
      '''
    }
    r = requests.get('http://docker.for.mac.localhost:8080/graphql', json=json)
    assert r.json() == {'data': {'getPost': {'theme': 'crew'}}}