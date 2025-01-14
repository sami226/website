var lastArticleID = null;
var section = "";

function setDate() {
	var monthNames = [
		"January", "February", "March",
		"April", "May", "June", "July",
		"August", "September", "October",
		"November", "December"
	];

	var date = new Date();
	var day = date.getDate();
	var monthIndex = date.getMonth();
	var year = date.getFullYear();

	$("#headerDate").text(monthNames[monthIndex] + " " + day + ", " + year);
}

function stringifyArticle(article, words) {
	var string = "<div class='article'>";
	if (article.hasOwnProperty('imgID') && article.imgID != "") {
		string += "<div class='image' style=\'background-image: url(\"/storage/" + article.imgID + "\");\'></div>";
	}

	string += "<div class='heading'><a href='article.php?";
	string += article._id.$oid + "'>" + article.title;
	string += "</a></div><div><span class='author'>by ";
	string += getStaffLink(article.staffs);
	string += " |</span> <a class='category' href='/?";
	string += article.sectionID.$oid + "'>" + article.section.title;
	string += "</a></div><div class='content'>";
	string += getNWords(article.content,words) + "</div></div>";
	return string;
}

function populateArticles(articles,append) {
	var left = "", middle = "", right = "";

	for (var i=1; i<=articles.length; i++) {
		if (i%3 == 1) left += stringifyArticle(articles[i-1], 50);
		else if (i%3 == 2) middle += stringifyArticle(articles[i-1], 150);
		else right += stringifyArticle(articles[i-1], 50);
	}

	lastArticleID = articles[articles.length-1]._id.$oid;

	if (append) {
		$("#leftColumn").append(left);
		$("#middleColumn").append(middle);
		$("#rightColumn").append(right);
	} else {
		$("#leftColumn").html(left);
		$("#middleColumn").html(middle);
		$("#rightColumn").html(right);
	}
}

function refreshArticles(append) {
	if (!section || section == "undefined") {
		console.log("Get all")
		getArticle.all(lastArticleID,6,function(articles) {
			populateArticles(articles,append);
		});
	}
	else {
		console.log("get section")
		getArticle.bySection(section,lastArticleID,3,function(articles) {
			populateArticles(articles,append);
		});
	}
	console.log("Done refreshing articles")
}

$(document).ready(function() {
	section = getQuery();
	refreshArticles(false);

	$("#loadMoreBtn").click(function(e) {
		e.preventDefault();
		refreshArticles(true);
	});

	//setDate();
});
