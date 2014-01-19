$(document).ready(function() {
	$('#imdb-slider').slider({
		formater: function(value) {
			$('#imdb-rating-label').text(value/10);
			$('#imdb_value').text(value);
		}
	});

	$('#metacritic-slider').slider({
		formater: function(value) {
			$('#metacritic-rating-label').text(value);
			$('#metacritic_value').text(value);
		}
	});
})