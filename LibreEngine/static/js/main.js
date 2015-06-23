function importScript(src)
{
	
}
function importStyle(src)
{
	
}
function onSearchAjaxDone(res)
{
	var result_list = res.hits.hits;
	var list_element = document.createElement("ul");
	for(var i = 0 ; i < result_list.length ; i++)
	{
		it = result_list[i];
		var link_element = document.createElement("a");
		
		$(link_element).html(iter._source.document);
		$(link_element).attr("href","/wiki/" + encodeURIComponent(iter._source.document) );
		$(list_element).append("<li>" + list_item_element + "</li>");
	}
	$("#search-result-pos").html(list_element);
}
function onSearchAjaxRequest()
{
	var search_text = $("#search-text-box").val();
	search_text = search_text.trim();
	if(search_text.length == 0)
	{
		return;
	}
	if(search_text[0] != "*" && search_text[search_text.length - 1] != "*")
	{
		search_text = "*" + search_text + "*";
	}
	var param = 
	{
		url : "http://68.195.46.102:9200/search/mysql/_search",
		data : {
		   "q" : search_text,
		  "size":1048576
		},
		method:"GET",
		dataType : "json"
	};
	$.ajax(param).done(onSearchAjaxDone);
}
$(document).ready(
function()
{
	$("#search-text-box").on('paste',onSearchAjaxRequest);
	$("#search-text-box").on('keydown',onSearchAjaxRequest);
}
);