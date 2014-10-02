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
		        'scrollTop': $target.offset().top - 40
		    }, 500, 'swing', function () {
		        window.location.hash = target;
		    });
		});
	});

	/* Play button click */
	$("#play-button").click(function() {
		$("#play-button").fadeOut("fast", function() {
			$("#video-container").css("display", "block");
			$("#video-container").css("opacity", "1");
			$("#video-container").css("z-index", "3");
			setTimeout(function() {
				$("#campaign-video").attr("src", "http://www.youtube.com/embed/_Fo8CYQ2lpk?list=PLs0rLWE-xlJDJ14C0fJVMVLMgkcuGBRgC&rel=0&loop=1&autoplay=1&color=white&showinfo=0");
			}, 250);
		});
	});

	/* Exit video play */
	$(".x").click(function() {
		$("#video-container").css("opacity", "0");
		$("#video-container").css("z-index", "1");
		$("#campaign-video").attr("src", "");
		$("#play-button").fadeIn("fast");
		$("#video-container").css("display", "none");
	});

	/* Color picker */
	$("#customize .circle").click(function() {
		$("#customize .circle").removeClass("active");
		$(this).addClass("active");
	});


	/* Details slideshow */
	$("#details #image-container > div:gt(0)").hide();

	setInterval(function() { 
		$('#details #image-container > div:first')
		.fadeOut(1000)
		.next()
		.fadeIn(1000)
		.end()
		.appendTo('#image-container');
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
		if ($(window).scrollTop() > 200) {
			$(".navbar-default").css("background", "#111");
			$(".navbar-collapse").css("background", "#111");
		} else {
			$(".navbar-default").css("background", "transparent");
			$(".navbar-collapse").css("background", "transparent");
		}
	});
});