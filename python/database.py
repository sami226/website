from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug import secure_filename
import os

client = MongoClient()
db = client.record

UPLOAD_FOLDER = "../storage"

REQUIRED_ARTICLE_FIELDS = ['title', 'content', 'sectionID', 'authorIDs', 'date']
REQUIRED_STAFF_FIELDS = ['name', 'position']
REQUIRED_SECTION_FIELDS = ['title']


def updateDB(newDatabase):
    global db
    db = newDatabase


def getArticles(query):
    articles = [a for a in db.article.find(query)]
    validArticles = []
    for article in articles:
        article['authors'] = []

        # Get authors
        for authorID in article['authorIDs']:
            authors = getStaffs({"_id": authorID})
            if len(authors) == 0:
                break
            else:
                article['authors'].append(authors[0])
        if len(article['authors']) < len(article['authorIDs']):
            print("INVALID AUTHOR")
            continue

        # Get section
        sections = getSections({"_id": article['sectionID']})
        if len(sections) == 0:
            print("INVALID SECTION")
            continue
        else:
            article['section'] = sections[0]

        validArticles.append(article)
    return validArticles


def createArticle(article):
    print(article)
    if all(a in article for a in REQUIRED_ARTICLE_FIELDS) is False:
        print("Not all fields")
        return False
    elif db.section.find_one({"_id": article['sectionID']}) is None:
        print("Invalid section")
        return False
    elif any([db.staff.find_one({"_id": authorID}) is None for authorID in article['authorIDs']]):
        print("Invalid author")
        return False
    else:
        db.article.insert_one(article)
        return True


def updateArticle(article):
    if all(a in article for a in ['_id'] + REQUIRED_ARTICLE_FIELDS) is False:
        return False
    else:
        db.article.insert_one(article)
        return True


def deleteArticle(_id):
    db.article.remove({'_id': ObjectId(_id)})


def getStaffs(query):
    staffs = [a for a in db.staff.find(query)]
    return staffs


def createStaff(newStaff):
    print(newStaff)
    if all(a in newStaff for a in REQUIRED_STAFF_FIELDS) is False:
        return False
    else:
        db.staff.insert_one(newStaff)
        return True


def updateStaff(newStaff):
    if all(a in newStaff for a in ['_id'] + REQUIRED_STAFF_FIELDS) is False:
        return False
    else:
        db.staff.update({'_id': ObjectId(newStaff._id)}, newStaff)
        return True


def getSections(query):
    sections = [a for a in db.section.find(query)]
    return sections


def createSection(section):
    if all(a in section for a in REQUIRED_SECTION_FIELDS) is False:
        return False
    else:
        db.section.insert_one(section)
        return True


def deleteSection(_id):
    db.section.remove({'_id': ObjectId(_id)})


def saveFile(file):
    def allowed_file(filename):
        return '.' in filename and \
           filename.rsplit('.', 1)[1] == 'jpg'

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return filename
    else:
        return None