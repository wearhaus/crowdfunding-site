$(document).ready(function() {

	/* Shortcut hover */

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

	/* Shortcut click */

	var currentActiveShortcut = null;

	function makeShortcutActive(shortcut) {
		if (currentActiveShortcut) {
			$("div.inner." + currentActiveShortcut).css(
				"background-image", "url('../static/img/" + currentActiveShortcut + "-blue-outline.png')"
			);
		}
		$("div.inner." + shortcut).css(
			"background-image", "url('../static/img/" + shortcut + "-blue-fill.png')"
		);
		currentActiveShortcut = shortcut;
	}

	$("div.inner.home").click(function() {
		makeShortcutActive("home");
	});

	$("div.inner.social").click(function() {
		makeShortcutActive("social");
	});

	$("div.inner.customize").click(function() {
		makeShortcutActive("customize");
	});

	$("div.inner.interface").click(function() {
		makeShortcutActive("interface");
	});

	$("div.inner.details").click(function() {
		makeShortcutActive("details");
	});

	$("div.inner.story").click(function() {
		makeShortcutActive("story");
	});


	/* Play button hover */

	$("#play-button").hover(function() {
		$("#play-button .inner-play").css("background-color", "#00bccc");
		$("#play-symbol").css("border-left-color", "white");
	}, function(){
		$("#play-button .inner-play").css("background-color", "none");
		$("#play-symbol").css("border-left-color", "#00bccc");

	});
});
