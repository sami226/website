from flask import Blueprint, request
from bson.json_util import dumps
from bson.objectid import ObjectId
import database as db

publicAPI = Blueprint('publicAPI', __name__)


@publicAPI.route('/api/article', methods=['GET'])
def article():
    if request.args.get('articleID') is not None:
        return dumps(db.getArticles({"_id": ObjectId(request.args.get('articleID'))}))
    if request.args.get('sectionID') is not None:
        return dumps(db.getArticles({"sectionID": ObjectId(request.args.get('sectionID'))}))
    if request.args.get('authorID') is not None:
        return dumps(db.getArticles({"authorIDs": {"$elemMatch": {"$in": [ObjectId(request.args.get('authorID'))]}}}))
    if request.args.get('title') is not None:
        return dumps(db.getArticles({"title": request.args.get('title')}))
    return dumps(db.getArticles({}))


@publicAPI.route('/api/staff', methods=['GET'])
def staff():
    if request.args.get('staffID') is not None:
        return dumps(db.getStaffs({"_id": ObjectId(request.args.get('staffID'))}))
    elif request.args.get('name') is not None:
        return dumps(db.getStaffs({"name": ObjectId(request.args.get('name'))}))
    return dumps(db.getStaffs({}))


@publicAPI.route('/api/section', methods=['GET'])
def section():
    try:
        if request.args.get('sectionID') is not None:
            return dumps(db.getSections({"_id": ObjectId(request.args.get('sectionID'))}))
    except:
        pass
    return dumps(db.getSections({}))