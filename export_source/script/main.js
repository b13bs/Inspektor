//populate la page avec les donnees.
$(function(){
	for(i in data)
	{
		var line = "<div class=row index='"+i+"'>";
		line = line+"<div class='column_names col-md-12'>";
		line = line+"<div class='col-md-4 table_header'>Image source</div>";
		line = line+"<div class='col-md-8 table_header'>Texte extrait</div>";
		line = line+"</div>";
		
		line=line+"<img src='file:///"+data[i][0]+"' class='col-md-4'>";
		line=line+"<div class='col-md-8'><div class=textbox>"+data[i][1]+"</div><label>Confidence: </label><progress value="+data[i][2]+" max=100></progress></div>";
		line = line+"</div>";
		
		$("#data").append($(line));
	}
});

//listeners pour le keyword filter
$(function(){
	$('#keyword_form').submit(function(e){
		e.preventDefault();
		var filtre = $('#filtre').val();

		$('.row').each(function(){
			var text = $(this).find('.textbox').text();
			if(text.search(filtre)==-1)
			{
				$(this).hide();
			}
			else
			{
				$(this).show();
			}
		});
	});
});