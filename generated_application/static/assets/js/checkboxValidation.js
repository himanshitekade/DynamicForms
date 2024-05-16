
function ifChecked(checkbox_name){
	console.log(checkbox_name)
	var isValid = document.getElementsByName(checkbox_name)
	var isCheck = 0;
	var isUnCheck = 0;

	for(var i=0; i<isValid.length; i++){

		console.log(isValid[i].checked)
		if(isValid[i].checked===true){
			isCheck += 1
		}
	}
	if(isCheck === 0){
		for(var i=0; i<isValid.length; i++){
			isValid[i].setAttribute('required','true')
		}				
	}else{
		for(var i=0; i<isValid.length; i++){
			isValid[i].removeAttribute('required')
		}
	}
}

$(document).ready(function(){
	form = document.getElementsByTagName('input')
	console.log(form)
	for(var i =0; i<form.length;i++){
		// console.log(form[i])
		
			if(form[i].type == 'checkbox'){

				ifChecked(form[i].name)
			}	

	}
})
			
