$(document).ready(function() {

	/* Shortcut hover */

	$(".inner.home").hover(function(){
		$("p.home").css("color", "white");
	}, function(){
		$("p.home").css("color", "none");
	});

	$(".inner.social").hover(function(){
		$("p.social").css("color", "white");
	}, function(){
		$("p.social").css("color", "none");
	});

	$(".inner.customize").hover(function(){
		$("p.customize").css("color", "white");
	}, function(){
		$("p.customize").css("color", "none");
	});

	$(".inner.interface").hover(function(){
		$("p.interface").css("color", "white");
	}, function(){
		$("p.interface").css("color", "none");
	});

	$(".inner.details").hover(function(){
		$("p.details").css("color", "white");
	}, function(){
		$("p.details").css("color", "none");
	});

	$(".inner.story").hover(function(){
		$("p.story").css("color", "white");
	}, function(){
		$("p.story").css("color", "none");
	});

	/* Shortcut click */

	var currentActiveShortcut = null;

	function makeShortcutActive(shortcut) {
		if (currentActiveShortcut) {
			$(".inner." + currentActiveShortcut).css(
				"background-image", "url('../static/img/" + currentActiveShortcut + "-blue-outline.png')"
			);
		}
		$(".inner." + shortcut).css(
			"background-image", "url('../static/img/" + shortcut + "-blue-fill.png')"
		);
		currentActiveShortcut = shortcut;
	}

	$(".inner.home").click(function() {
		makeShortcutActive("home");
	});

	$(".inner.social").click(function() {
		makeShortcutActive("social");
	});

	$(".inner.customize").click(function() {
		makeShortcutActive("customize");
	});

	$(".inner.interface").click(function() {
		makeShortcutActive("interface");
	});

	$(".inner.details").click(function() {
		makeShortcutActive("details");
	});

	$(".inner.story").click(function() {
		makeShortcutActive("story");
	});

	/* Scroll handler */
	var slideNames = ["home", "social", "customize", "interface", "details", "story"];

	$( window ).scroll(function() {
		var slideIndex = Math.floor(($(window).scrollTop() + 60) / 640);
		if (slideNames[slideIndex] != currentActiveShortcut) {
			makeShortcutActive(slideNames[slideIndex]);
		}
	});

	/* Smooth transition on shortcut click */
	$(document).ready(function(){
		$('a[href^="#"]').on('click',function (e) {
		    e.preventDefault();

		    var target = this.hash,
		    $target = $(target);

		    $('html, body').stop().animate({
		        'scrollTop': $target.offset().top - 100
		    }, 900, 'swing', function () {
		        window.location.hash = target;
		    });
		});
	});

	/* Play button click */
	$("#play-button").click(function() {
		$("#play-button").fadeOut("fast", function() {
			$("#video-container").css("opacity", "1");
			setTimeout(function() {
				$("#campaign-video").attr("src", "http://www.youtube.com/embed/uQnzm_uywxk?autoplay=1&color=white&showinfo=0");
			}, 250);
		});
	});

	/* Exit video play */
	$(".x").click(function() {
		$("#video-container").css("opacity", "0");
		$("#campaign-video").attr("src", "");
		$("#play-button").fadeIn("fast");
	});
});