window.setTimeout(function() {
    $(".alert").fadeTo(400, 0).slideUp(300, function () {
		$(this).remove();
	  });
	}, 4000);