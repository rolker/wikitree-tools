
$( document ).ready(function(){
	if(localStorage["confirmExit"]=="true")
		$("#confirmExit").prop('checked',true);
	
	$("#confirmExit").change(function(event){
		var confirm = $("#confirmExit:checked").val();
		if(confirm)
			localStorage["confirmExit"] = true;
		else
			localStorage["confirmExit"] = false;
	});
});
