function utility_get_metric_currencies() {
	return ['EUR', 'CLP', 'SEK', 'NOK'];
}

function utility_get_non_metric_currencies() {
	return ['USD'];
}

function utility_is_email_valid(email) {
  var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
  return regex.test(email);
}
function utility_is_password_valid(password) {

	if (password.length < 6)
		return false


	return true;
}
function utility_get_parameter_by_name(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}
function utility_block_screen(message, css) {

	var html = ""
	if (typeof message === "undefined") {

		html += "<div class='block-screen-container'>"
		html += 	'<i class="zmdi zmdi-rotate-right zmdi-hc-spin zmdi-hc-5x"></i>'
		html += "</div>"

	} else {
		html += message
	}
	

	

	$.blockUI({
		message: html,
		css: css,
	});
}
function utility_unblock_screen() {
	$.unblockUI();
}
function utility_normalize_number(string, thousands, decimal) {

	var decimal_nums = '0';
	var thousand_nums = '0';

	var splitted = string.split(decimal);
	thousand_nums = splitted[0];
	
	if (splitted.length == 2)
		decimal_nums = splitted[1];
	

	return parseInt( thousand_nums.replace( new RegExp( '[' + thousands +']', 'g'), '' ) ) + parseFloat('0.' + decimal_nums);


}
function utility_postJSON(url, func) {
	return $.post(url,
				 {
				 	csrfmiddlewaretoken : $.cookie('csrftoken'),
				 },
				 func, 'json');
}
function postJSON(url, onSuccess, onError, data) {
	onSuccess = typeof onSuccess === "undefined" ? function(){} : onSuccess;
	onError = typeof onError === "undefined" ? function(){} : onError;
	data = typeof data === "undefined" ? {} : data;
	data.csrfmiddlewaretoken = $.cookie('csrftoken')
	
	return $.ajax({
		type: "POST",
		url: url,
		data: data,
		success: onSuccess,
		error: onError,
		dataType: 'json',
	})
}
function getJSON(url, onSuccess, onError, data) {
	onSuccess = typeof onSuccess === "undefined" ? function(){} : onSuccess;
	onError = typeof onError === "undefined" ? function(){} : onError;
	data = typeof data === "undefined" ? {} : data;
	
	return $.ajax({
		type: "GET",
		url: url,
		data: data,
		success: onSuccess,
		error: onError,
		dataType: 'json',
	})
}
function global_error(title, text, onConfirm) {
	swal({
		title: title,
		text: text,
		type: "error",
		confirmButtonColor: "#337ab7",
		closeOnConfirm: false,
  		closeOnCancel: false,
		allowOutsideClick: false,
	}, onConfirm);
}
function global_success(title, text, onConfirm) {
	swal({
		title: title,
		text: text,
		type: "success",
		confirmButtonColor: "#337ab7",
		closeOnConfirm: false,
  		closeOnCancel: false,
  		allowOutsideClick: false,
	}, onConfirm);
}
function global_warning(title, text, onConfirm) {
	swal({
		title: title,
		text: text,
		type: "warning",
		showCancelButton: true,
		confirmButtonColor: "#337ab7",
		closeOnConfirm: false,
  		closeOnCancel: false,
		allowOutsideClick: false,

	}, onConfirm);
}

function materialShowWarning(options, onClick) {
	options.cancelButtonClass = "btn-material btn-material-cancel"
	options.confirmButtonClass = "btn-material btn-material-confirm"
	options.showCancelButton = true
	options.closeOnConfirm = true
	options.type = 'warning'
	swal(options, onClick);
}

function materialShowError(options, onClick) {
	options.confirmButtonClass = "btn-material btn-material-confirm"
	options.showCancelButton = false
	options.closeOnConfirm = true
	options.type = 'error'
	swal(options, onClick);
}

