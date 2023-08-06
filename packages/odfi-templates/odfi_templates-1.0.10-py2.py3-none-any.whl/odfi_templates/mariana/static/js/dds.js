var odfi = {

	mariana: {

		attributeStack: []
	}
}

$(function() {


	$('#nav-sticky').sticky({
	    context: '#page-body'
	  });

	console.info("Converting TOC 2");
	//$('ul.current>li').unwrap().wrap("<div/>");
	$("ul.current").wrap("<div class='ui vertical pointing menu'/>").contents().unwrap();
	$('.toctree-l1>a').unwrap().wrap("<div class='item'/>").wrap("<div class='header'/>");
	//.addClass("item");


	$.fn.pattr = function(name,value) {

		var attrId = this.attr('id')+"."+name;
		var oldValue = odfi.mariana.attributeStack[attrId];
		console.log("pattr "+name+" -> "+value+" , old= "+oldValue);
		if (value) {
			odfi.mariana.attributeStack[attrId] = this.attr(name);
			this.attr(name,value);
		} else if (odfi.mariana.attributeStack[attrId] ) {
			this.attr(name,odfi.mariana.attributeStack[attrId]);
		} else {
			this.attr(name,"");
		}
		
    	
	};


	$('svg').each(function(i,e) {

		var p = $(e).parent();
		console.info("SVG Width: "+p.width());
		//$(e).attr("width",""+p.width()+"px");
	});
	

});