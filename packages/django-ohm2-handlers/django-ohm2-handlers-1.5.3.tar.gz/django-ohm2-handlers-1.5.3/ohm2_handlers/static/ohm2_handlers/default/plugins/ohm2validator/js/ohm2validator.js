


(function($) {
	'use strict';
	
	$.fn.OHM2Validate = function(options) {
		
		var opts = {
			formSubmitButton: 'button[type="submit"]',
			inputs: {
				validClass: "has-success",
				invalidClass: "has-error",
				inputSelector: 'input[type!="hidden"]',
				findInputContainer: function(input) {
					return input.parent().parent()
				},
				validate: function(input) {
					var type = input.prop('type');
					var value = input.val()
					var valid = true;

					
					if (type === "email") {
						var pattern = /^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$/
						if (value.match(pattern) == null)
							valid = false;

					} else if (type === 'password') {
						
						var minlength = input.attr('minLength');
						if (!isNaN(minlength) && value.length < minlength)
							valid = false;

						var pattern = /(?=.*[a-z])/;
						var lower = input.attr('lower');
						if (!isNaN(lower) && value.match(pattern) == null)
							valid = false;

						var pattern = /(?=.*[A-Z])/;
						var upper = input.attr('upper');
						if (!isNaN(upper) && value.match(pattern) == null)
							valid = false;

						var pattern = /(?=.*[0-9])/;
						var digits = input.attr('digits');
						if (!isNaN(digits) && value.match(pattern) == null)
							valid = false;

					} else if (type === 'file') {
						
						if (value.length == 0)
							valid = false;
					
					} else if (type === 'text') {
						
						var minlength = input.attr('minLength');
						if (!isNaN(minlength) && value.length < minlength)
							valid = false;

					}


					return valid
				}

			}
		}

		function updateSubmitButton(valid, input) {
			var form = input.closest("form")
			var submitBtn = form.find(':submit').first()
			submitBtn.prop( "disabled", !valid );
		}
		function updateGraphics(valid, input, validClass, invalidClass) {
			validClass = typeof validClass === "undefined" ? "" : validClass
			invalidClass = typeof invalidClass === "undefined" ? "" : invalidClass
			var container = opts.inputs.findInputContainer(input)
			if (valid) {
				container.removeClass(invalidClass)
				container.addClass(validClass)
			} else {
				container.removeClass(validClass)
				container.addClass(invalidClass)
			}
		}
		function validateSelect(select) {
			var value = select.val()
			var valid = true;
			
			if(value == null || value.length == 0)
				valid = false

			return valid
		}
		
		function selectListener() {
			var input = $(this)
			return validateSelect(input)
		}
		function inputListener() {
			var input = $(this)
			var valid = opts.inputs.validate(input);
			
			updateGraphics(valid, input, opts.inputs.validClass, opts.inputs.invalidClass)
			updateSubmitButton(valid, input)
		}
		function bindListeners(element, form) {

			element[0].checkValidity = function() {
				return opts.inputs.validate($(this))
			}

			if ( element.is('input') ) {

				if (element.is('input[type="checkbox"]')) {

					element
					.on('change', inputListener)

				} else {

					element
					.on('keyup', inputListener)
					.on('focusout', inputListener)
					
				}
				
			} else if ( element.is('select') ) {
				element
				.on('change', selectListener)
			}
		}
		
		
		var form = $(this);
		var inputs = form.find(opts.inputs.inputSelector);
		var selects = form.find('select')

		var elements = $.merge( inputs, selects )
		elements.each(function(i, element) {
			bindListeners( $(element), form )
		})

		
		form.find(opts.formSubmitButton).on('click', function(e) {
			e.preventDefault()
			
			var validForm = true;

			inputs.each(function(i, input) {
				validForm &= opts.inputs.validate($(input))
			})

			if (!validForm) return false

				
			form.submit()

		})		
		return $(this)

	}

})(jQuery);
