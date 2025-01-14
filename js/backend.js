console.log(window.location.hostname)
var API_URL = "/api/";
var ADMIN_URL = "/api/admin/";
var ARTICLE_URL = API_URL+"article";
var SECTION_URL = API_URL+"section";
var STAFF_URL = API_URL+"staff";

var getArticle = {
    ajaxCall: function(params, callback) {
	console.log(params)
        $.ajax({
            url: ARTICLE_URL,
            cache: false,
            method: "GET",
            data: params,
            async: true,
            success: function(result) {
                callback($.parseJSON(result));
            },
            error: function(xhr, status, error) {
                console.log(xhr)
                console.log(status)
                console.log(error)
                callback([]);
            }
        }).done(function(){
            console.log("done")
        }).fail(function(){
            console.log("fail")
        }).always(function(){
            console.log("all")
        });
        console.log("Done with request")
    },
    all: function(lastArticleID, articles, callback) {
        if (lastArticleID == null) this.ajaxCall({numArticles: articles},callback);
        else this.ajaxCall({lastArticleID: lastArticleID, numArticles: articles}, callback)
    },
    bySection: function(sectionID, lastArticleID, articles, callback) {
        if (lastArticleID == null) this.ajaxCall({sectionID: sectionID, numArticles: articles}, callback);
        else this.ajaxCall({sectionID: sectionID, lastArticleID: lastArticleID, numArticles: articles}, callback);
    },
    byID: function(articleID, callback) {
        this.ajaxCall({articleID: articleID}, function(articleArray) {
            if(articleArray.length == 0) callback(null);
            else callback(articleArray[0]);
        });
    },
    byQuery: function(query) {
        return null;
    },
    byStaff: function(staffID, callback) {
        this.ajaxCall({staffID: staffID}, callback);
    }
};

var getStaff = {
    ajaxCall: function(params) {
        return $.parseJSON($.ajax({
            url: STAFF_URL,
            data: params,
            async: false
        }).responseText);
    },
    byID: function(id) {
        return this.ajaxCall({staffID: id})[0];
    },
    byName: function(name) {
        return this.ajaxCall({name: name})[0];
    }
};

var getSection = {
    ajaxCall: function(params) {
        return $.parseJSON($.ajax({
            url: SECTION_URL,
            data: params,
            async: false
        }).responseText);
    },
    all: function() {
        return this.ajaxCall({});
    },
    byTitle: function(title) {
        return this.ajaxCall({title: title})[0];
    }
};

var admin = {
    password: "",
    ajaxCall: function(endpoint, method, params) {
        console.log("Start")
        console.log(ADMIN_URL+endpoint)
        return $.ajax({
            url: ADMIN_URL+endpoint,
            data: JSON.stringify(params),
            contentType: "application/json",
            headers: {
                "Authorization": "Basic " + btoa("admin:" + this.password)
            },
            method: method,
            async: false
        });
    },
    login: function(pass) {
        this.password = pass;
        var statusCode = this.ajaxCall("test", 'GET', {}).status;
        return statusCode == 200;
    },
    newStaff: function(staff) {
        return this.ajaxCall("staff", 'POST', staff).responseText;
    },
    editStaff: function(staff) {
        return this.ajaxCall("staff", 'PUT', staff).responseText;
    },
    newArticle: function(article) {
        return this.ajaxCall("article", 'POST', article).responseText;
    },
    deleteArticle: function(articleID) {
        return this.ajaxCall("article/"+articleID, 'DELETE', {}).responseText;
    },
    deleteSection: function(sectionID) {
        return this.ajaxCall("section/"+sectionID, 'DELETE', {}).responseText;
    },
    newSection: function(section) {
        return this.ajaxCall("section", 'POST', section).responseText;
    },
    uploadImages: function(formID, callback) {
        console.log($("#"+formID)[0])
	var formData = new FormData($("#"+formID)[0]);
        console.log(formData)
	return $.ajax({
            url: ADMIN_URL+"file",
	    async: false,
	    method: "POST",
	    data: formData,
	    processData: false,
	    contentType: false,
            headers: {
                "Authorization": "Basic " + btoa("admin:" + this.password)
            },
	    xhr: function() {
		var myXhr = $.ajaxSettings.xhr();
		return myXhr;
	    }
	}).responseText;
    },
    uploadIssues: function(issues) {
        return true;
    }
};
