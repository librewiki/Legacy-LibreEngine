function importScript(src)
{
	
}
function importStyle(src)
{
	
}
function onSearchAjaxDone(res)
{
	var result_list = res.hit;
	var list_element = document.createElement("ul");
	$(result_list).each(function(idx,iter){
		var link_element = document.createElement("a");
		
		$(link_element).html(iter._source.document);
		$(link_element).attr("href","/wiki/" + encodeURIComponent(iter._source.document) );
		$(list_element).append("<li>" + list_item_element + "</li>");
	});
	$("#search-result-pos").html(list_element);
}
function onSearchAjaxRequest()
{
	var search_text = $("#search-text-box").val();
	if(search_text[0] != "*" && search_text[search_text.length - 1] != "*")
	{
		search_text "*" + search_text + "*";
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