//populate la page avec les donnees.
$(function(){
	for(i in data)
	{
		var line = "<div class=row index='"+i+"'>";
		line = line+"<div class='column_names col-md-12'>";
		line = line+"<div class='col-md-4 table_header'>Source image</div>";
		line = line+"<div class='col-md-8 table_header'>Recognised text</div>";
		line = line+"</div>";
		
		line=line+"<div class='col-md-4'>"+
		"<a href='file:///"+data[i][3]+"'><img src='file:///"+data[i][3]+"' class='col-md-12'></a><p class='col-md-12'><a href='file:///"+data[i][0]+"'>"+data[i][0]+"</a></p>"+
		"<div class=clearfix><span class=lefttext>MD5:</span><span class=righttext>"+data[i][4]+"</span></div>"+
		"</div>";
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

//cree le slider de la navbar.
$(function(){
	$('#exactitude_slider').slider({
		tooltip:"none",
		min:0,
		max:100,
		value:0
	}).on('slide', function(ev)
	{
		var val = ev['value'];
		$('#min').text(val);

	}).on('slideStop', function(ev)
	{
		var min = ev['value'];
		$('.row').each(function() {
			var exactitude = parseInt($(this).find('.progress-bar').attr('aria-valuenow'));
			if (exactitude>=min)
			{
				$(this).removeClass('filterhide');
			}
			else
			{
				$(this).addClass('filterhide');
			}
		});

	});
});


$(function() {
	$("#standard_search").click(function() {
		reset_highlights();
		standard_search();

	});
	$("#regex_search").click(function() {
		reset_highlights();
		regex_search();
	});
	$("#fuzzy_search").click(function() {
		reset_highlights();
		fuzzy_search();
	});
	$('#keyword_form').submit(function(e){
		e.preventDefault();
		reset_highlights();
		standard_search();
	});
});


function standard_search()
{
	var filter = $('#filter').val();

	$('.row').each(function() {
		var text = $(this).find('.textbox').text();
		if ( text.toLowerCase().indexOf(filter.toLowerCase()) != -1 )
		{
			if(filter.length>0)
				highlight($(this).find('.textbox'), text.toLowerCase().indexOf(filter.toLowerCase()), filter.length);
			$(this).removeClass('searchhide');
		}
		else
		{
			$(this).addClass('searchhide');
		}
	});
}


function regex_search()
{
	var filter = $('#filter').val();
	var regex = new RegExp(filter);
	
	$('.row').each(function() {
		var text = $(this).find('.textbox').text();
		if ( regex.test(text) )
		{
			if(filter.length>0)
				highlight($(this).find('.textbox'), text.indexOf(text.match(filter)[0]), text.match(filter)[0].length);

			$(this).removeClass('searchhide');
		}
		else
		{
			$(this).addClass('searchhide');
		}
	});
}

function fuzzy_search()
{
	var THRESHOLD = 0.6;
	var filter = $('#filter').val();
	$('.row').each(function() {
		var text = $(this).find('.textbox').text();

		var similarity = 0;
		var index = 0;
		if(filter.length>0)
			for(var i=0;i<text.length;i++)
			{
				var substring = text.substring(i,Math.min(i+filter.length, text.length));
				var a = FuzzySet([substring]);
				console.log(substring);
				console.log(filter);
				var result = a.get(filter);
				console.log(result);
				if(result != null)
				{
					if(similarity<result[0][0])
						index = i;
					similarity = Math.max(similarity, result[0][0]);
				}
			}

		if (similarity >= THRESHOLD || filter.length==0)
		{
			if(similarity >= THRESHOLD)
				highlight($(this).find('.textbox'), index, filter.length);
			$(this).removeClass('searchhide');
		}
		else
		{
			$(this).addClass('searchhide');
		}
	});
}

//textBlock = jQuery elem for div.textbox
function highlight(textBlock, index, length)
{
	var before = textBlock.text().substring(0, index);
	console.log(before);
	var content = textBlock.text().substring(index, index+length);	
	console.log(content);
	var after = textBlock.text().substring(index+length);
	console.log(after);

	var newText = before+"<span class=highlight>"+content+"</span>"+after;
	textBlock.html(newText);
}

function reset_highlights()
{
	$('span.highlight').contents().unwrap();
}