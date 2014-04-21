$(document).ready(function(){

	$("div.home").hover(function(){
		$("p.home").css("color", "white");
	}, function(){
		$("p.home").css("color", "none");
	});

	$("div.social").hover(function(){
		$("p.social").css("color", "white");
	}, function(){
		$("p.social").css("color", "none");
	});

	$("div.customize").hover(function(){
		$("p.customize").css("color", "white");
	}, function(){
		$("p.customize").css("color", "none");
	});

	$("div.interface").hover(function(){
		$("p.interface").css("color", "white");
	}, function(){
		$("p.interface").css("color", "none");
	});

	$("div.details").hover(function(){
		$("p.details").css("color", "white");
	}, function(){
		$("p.details").css("color", "none");
	});

	$("div.story").hover(function(){
		$("p.story").css("color", "white");
	}, function(){
		$("p.story").css("color", "none");
	});

	$("#play-button").hover(function() {
		console.log("hello");
		$("#play-button .inner").css("background-color", "#00bccc");
		$("#play-symbol").css("border-left-color", "white");
	}, function(){
		$("#play-button .inner").css("background-color", "none");
		$("#play-symbol").css("border-left-color", "#00bccc");

	});

});
