1) Deploy docker-compose up --build -d(if you want daemon)
2) run tests after deploy docker-compose run web pytest forum/tests.py

API:
link with graphiql : http://0.0.0.0:8080/graphiql
link without graphiql : http://0.0.0.0:8080/graphql

Queries:

1. Section
1)Create Section:

mutation{
  createSection(theme:"section_theme", description:"sectiondescription"){
    ok
  }
}

2)Change Section:

mutation{
  changeSection(id_:1, theme:"updated_section_theme", description:"sectiondescription"){
    ok
  }
}

3)Delete Section:

mutation{
deleteSection(id_:1){
  ok
}
}

4) Section Pagination

{
  sectionPagination(page:1,number:1) {
    totalPages
    sections {
      id
    }
  }
}

with search by theme:

{
  sectionPagination(page:1,number:1, search: "new") {
    totalPages
    sections {
      id
    }
  }
}

5) Get certain Section by id:
{
	getSection(id_:1){
    id
    theme
    description
  }
}

2. Post
1) Create Post:

mutation{
  createPost(sectionId:1 ,theme:"post_theme", description:"post_description"){
    ok
  }
}

2)Change Post:

mutation{
  changePost(id_:1 ,theme:"post_theme"){
    ok
  }
}

3)Delete Post:

mutation{
deletePost(id_:1){
  ok
}
}

4) Post Pagination

{
  postPagination(page:1,number:2, sectionId:1) {
    totalPages
    posts {
      id
      theme
    }
  }
}

with search by theme:

{
  postPagination(page:1,number:2, sectionId:1, search:"th") {
    totalPages
    posts {
      id
      theme
    }
  }
}

5) Get certain Post by id:
{
	getPost(id_:1){
    theme
    id
    description
    comments
  }
}

3. Comment

1) Create Comment:
mutation{
  createComment(postId:1, text:"ss"){
    ok
  }
}

2) Answer to Comment:
mutation{
  createComment(postId:1, text:"ss", parentId:1){
    ok
  }
}

3) Delete Comment:
mutation{
	deleteComment(id_:1){
    ok
  }
}
