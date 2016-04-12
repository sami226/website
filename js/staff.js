function renderArticles(articles) {
	var string = "";

	articles.forEach(function(article) {
		string += '<div class="article"><div class="title"><a href="article.php?'
				+ encodeURIComponent(article.id) + '">' + article.title
				+ '</a></div><div class="content">' + article.content + '</div></div>';
	});

	$("#articleBox").html(string);
}


function renderStaff(staff) {
	document.title = "HM Record: " + staff.name;

	$("#name").text(staff.name);
	$("#position").text(staff.position);

	renderArticles(getArticle.byStaff(staff.id));
}

$(document).ready(function() {
	var id = decodeURIComponent(window.location.href.split('?')[1]);
	renderStaff(getStaff.byID(id));
});