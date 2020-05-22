
$('.open-form').click(function() {
	$('.form-popup').show();
});

$('.close-form').click(function() {
	$('.form-popup').hide();
});

$('.reset-form').click(function() {
	$('.success-message').show();
	$('#my-form').trigger( 'reset' );

	setTimeout(function() {
		$('.success-message').hide()
	}, 1500);
});

// $(document).mouseup(function(e) {
// 	var container = $(".form-wrapper");
// 	var form = $(".form-popup");

// 	if (!container.is(e.target) && container.has(e.target).length === 0) {
// 		form.hide();
// 	}
// });

// $('.open-form').on('click', function(event) {
//     $('.form-popup').show();
//   });

function myFunction() {
	var popup = document.getElementById("myPopup");
	popup.classList.toggle("show");
  }