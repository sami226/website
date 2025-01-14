from flask import Blueprint, request
from bson.json_util import dumps
from bson.objectid import ObjectId
import database as db

publicAPI = Blueprint('publicAPI', __name__)

@publicAPI.route('/api/article', methods=['GET'])
def article():
    if request.args.get('articleID') is not None:
        return dumps(db.getArticles({"_id": ObjectId(request.args.get('articleID'))}))
    if request.args.get('lastArticleID') is not None and request.args.get('sectionID') is not None and request.args.get('numArticles') is not None:
        return dumps(db.getArticles({"_id":{"$lt": ObjectId(request.args.get('lastArticleID'))}, "sectionID": ObjectId(request.args.get('sectionID'))}, number=int(request.args.get("numArticles"))))
    if request.args.get('numArticles') is not None and request.args.get('sectionID') is not None:
        return dumps(db.getArticles({"sectionID": ObjectId(request.args.get('sectionID'))},number=int(request.args.get("numArticles"))))
    if (request.args.get('sectionID') is not None) and (request.args.get('sectionID') != "undefined"):
        if request.args.get('sectionID') == "opinions":
            return dumps(db.getArticles({"$or":[{"sectionID": ObjectId('5876f88977e0ad0674052a4a')},{"sectionID": ObjectId('5876f88977e0ad0674052a4b')},{"sectionID":ObjectId('5876f88977e0ad0674052a49')}]}))
        else:
            return dumps(db.getArticles({"sectionID": ObjectId(request.args.get('sectionID'))}))
    if request.args.get('staffID') is not None:
        return dumps(db.getArticles({"staffIDs": {"$elemMatch": {"$in": [ObjectId(request.args.get('staffID'))]}}}))
    if request.args.get('title') is not None:
        return dumps(db.getArticles({"title": request.args.get('title')}))
    if request.args.get('lastArticleID') is not None and request.args.get('numArticles') is not None:
        return dumps(db.getArticles({"_id":{"$lt": ObjectId(request.args.get('lastArticleID'))}}, number=int(request.args.get("numArticles"))))
    if request.args.get('numArticles') is not None:
        return dumps(db.getArticles({},number=int(request.args.get("numArticles"))))
    return dumps(db.getArticles({}))


@publicAPI.route('/api/staff', methods=['GET'])
def staff():
    if request.args.get('staffID') is not None:
        return dumps(db.getStaffs({"_id": ObjectId(request.args.get('staffID'))}))
    elif request.args.get('name') is not None:
        return dumps(db.getStaffs({"name": request.args.get('name')}))
    return dumps(db.getStaffs({}))


@publicAPI.route('/api/section', methods=['GET'])
def section():
    if request.args.get('sectionID') is not None:
        return dumps(db.getSections({"_id": ObjectId(request.args.get('sectionID'))}))
    if request.args.get('title') is not None:
        return dumps(db.getSections({'title': request.args.get('title')}))
    return dumps(db.getSections({}))
