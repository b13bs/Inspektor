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
		line=line+"<div class='col-md-8'><div class=textbox>"+data[i][1]+"</div>";
		line=line+"<label>Exactitude: </label>";
		line=line+"<div class='progress'>";
	  		line=line+"<div class='progress-bar' role='progressbar' aria-valuenow='"+data[i][2]+"' aria-valuemin='0' aria-valuemax='100' style=\"width: "+data[i][2]+"%;\">";
	   	 		line=line+"<span>"+data[i][2]+"%</span>";
	  		line=line+"</div>";
		line=line+"</div>";
		
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