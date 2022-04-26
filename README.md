# 821_Final_Project

Team members: Gloria Gu, Jingya Cheng, Yvonne Feng


## Descrption:

A graphical user interface (GUI) created as front end by connecting Redis that allows users to interact with electronic devices through graphical icons and audio indicator such as primary notation, instead of text-based user interfaces, typed command labels or text navigation. 

What is Redis? An in-memory database that persists on disk. Redis is an open source, BSD licensed, advanced key-value store. It is often referred to as a data structure server since keys can contain strings, hashes, lists, sets and sorted sets. SQLite is an embedded SQL database engine. Unlike most other SQL databases, SQLite does not have a separate server process. SQLite reads and writes directly to ordinary disk files. Redis can be classified as a tool in the "In-Memory Databases" category, while SQLite is grouped under "Databases". We choose Redis rather than SQLite.


## GUI Library System:
The tkinter package is used in creation of GUI.

<img width="556" alt="GUI" src="https://user-images.githubusercontent.com/97641311/165377539-c2c8015e-f922-412f-8f06-12872568e527.png">

### Book options:
* Add a book to the redis db
* Delete the book given the book_key
* Edit book information
* Search book based on the given info
* Sort the books in the system by a field

### Person options:
* Add a person to the redis db
* Delete a person from the db by person_key
* Edit person information
* Search person based on the username
* Enable a person to check a book using username and isbn
* Enable a person to return a book using username and isbn




