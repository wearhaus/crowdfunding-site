$(document).ready(function() {

	var slideNames = ["home", "social", "customize", "interface", "touch", "details", "story"];

	/* Shortcut hover */

	function onMouseHoverGenerator(s) {
		return function() {
			$("p." + s).fadeIn("fast");
		};
	};

	function onMouseExitGenerator(s) {
		return function() {
			if ($(window).scrollTop() > 200) {
				$("p." + s).fadeOut("fast");
			}
		};
	}

	for (var i = 0; i < slideNames.length; i++) {
		var slideName = slideNames[i];

		$(".inner." + slideName).hover(
			onMouseHoverGenerator(slideName),
			onMouseExitGenerator(slideName)
		);
	};


	/* Shortcut click */

	var currentActiveShortcut = null;

	function makeShortcutActive(shortcut) {
		return function() {
			if (currentActiveShortcut) {
				$(".inner." + currentActiveShortcut).css(
					"background-image", "url('../static/img/" + currentActiveShortcut + "-blue-outline.png')"
				);
			}
			$(".inner." + shortcut).css(
				"background-image", "url('../static/img/" + shortcut + "-blue-fill.png')"
			);
			currentActiveShortcut = shortcut;
		};
	}

	for (var i = 0; i < slideNames.length; i++) {
		$(".inner." + slideNames[i]).click(makeShortcutActive(slideNames[i]));
	}

	/* Shortcut scroll handler */
	$(window).scroll(function() {
		if ($(window).scrollTop() > 200) {
			$("#shortcuts li p").fadeOut("fast");
		} else {
			$("#shortcuts li p").fadeIn("fast");
		}
	});



	/* Scroll handler */
	function updateShortCutOnScroll() {
		var slideIndex = Math.floor(($(window).scrollTop() + 60) / 640);
		if (slideNames[slideIndex] != currentActiveShortcut) {
			makeShortcutActive(slideNames[slideIndex])();
		}
	};

	updateShortCutOnScroll();
	$( window ).scroll(updateShortCutOnScroll);


	/* Smooth transition on shortcut click */
	$(document).ready(function(){
		$('a[href^="#"]').on('click',function (e) {
		    e.preventDefault();

		    var target = this.hash,
		    $target = $(target);

		    $('html, body').stop().animate({
		        'scrollTop': $target.offset().top - 100
		    }, 500, 'swing', function () {
		        window.location.hash = target;
		    });
		});
	});

	/* Play button click */
	$("#play-button").click(function() {
		$("#play-button").fadeOut("fast", function() {
			$("#video-container").css("opacity", "1");
			$("#video-container").css("z-index", "3");
			setTimeout(function() {
				$("#campaign-video").attr("src", "http://player.youku.com/embed/XNzEyNTc2ODgw");
			}, 250);
		});
	});

	/* Exit video play */
	$(".x").click(function() {
		$("#video-container").css("opacity", "0");
		$("#video-container").css("z-index", "1");
		$("#campaign-video").attr("src", "");
		$("#play-button").fadeIn("fast");
	});

	/* Details slideshow */
	$("#details-headphone-container > div:gt(0)").hide();

	setInterval(function() { 
		$('#details-headphone-container > div:first')
		.fadeOut(1000)
		.next()
		.fadeIn(1000)
		.end()
		.appendTo('#details-headphone-container');
	},  3000);

	/* Call to action */
	$("#button").hover(function () {
		$("#cta").fadeIn("fast");
	}, function() {
		if ($(window).scrollTop() > 50) {
			$("#cta").fadeOut("fast");
		}
	});

	$(window).scroll(function() {
		if ($(window).scrollTop() > 50) {
			$("#cta").fadeOut("fast");
		} else {
			$("#cta").fadeIn("fast");
		}
	});
});
