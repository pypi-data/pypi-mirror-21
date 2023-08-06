(function($) {
	'use strict';
	
	$.fn.OHM2AccountsForm = function(options) {
		
		var opts = {
			form: null,
			defaultErrorTitle: "Ops",
			defaultErrorMessage: "Something went wrong",
			loginFailedTitle: "Wrong email/password",
			loginFailedMessage: "Please check your credencials and try again",
			signupFailedTitle: "Signup failed",
			signupFailedMessage: "Please try again later",
			onSuccessRedirect: "/",
			errors: {
				blocked: {
					code: undefined,
					title: "Too many tries",
					message: "Please try again in a few minutes",
					preTag: "ohm2Blocked",
				},
				userAlreadyLoggedIn: {
					code: 179265,
					title: "Already logged in",
					message: "",
					preTag: "ohm2UserAlreadyLoggedIn",
				},
				usernameTooLong: {
					code: 179266,
					title: "Your username is too long",
					message: "Please choose a shorter one",
					preTag: "ohm2SsernameTooLong",
				},
				userAlreadyExist: {
					code: 179267,
					title: "This user already exist",
					message: "Please choose a different one",
					preTag: "ohm2UserAlreadyExist",
				},
				passwordIsNotSecure: {
					code: 179268,
					title: "Your password is not secure",
					message: "Please choose a safer one",
					preTag: "ohm2PasswordIsNotSecure",
				},
				invalidEmail: {
					code: 179269,
					title: "Your email is not valid",
					message: "Please choose a valid one",
					preTag: "ohm2InvalidEmail",
				},
				signupsDisabled: {
					code: 179272,
					title: "Signups are current disabled",
					message: "Please try again later",
					preTag: "ohm2SignupsDisabled",
				},
				loginWrongCredentials: {
					code: 179279,
					title: "Login failed",
					message: "Check your credentials and try again",
					preTag: "ohm2LoginWrongCredentials",	
				}
			},
			lockScreen: function() {
				utility_block_screen()
			},
			unlockScreen: function() {
				utility_unblock_screen()
			},
			lockScreenOnRedirect: function() {
				utility_block_screen("Redirecting to site")
				//maybe add timeout if the redirect takes a long time
			},
			signupFailed: function() {
				global_warning(opts.signupFailedTitle, opts.signupFailedMessage)
			},
			loginFailed: function() {
				global_warning(opts.loginFailedTitle, opts.loginFailedMessage)
			},
			onError: function(title, message) {
				global_error(title, message)
			},
			beforeSubmit: function(arr, $form, options) {
				opts.lockScreen()
			},
			successSubmit: function(data) {
				opts.unlockScreen()

				var error = data.error;

				if (error == null) {
					var ret = data.ret;

					if (ret) {

						opts.lockScreenOnRedirect()
						window.location.replace( opts.onSuccessRedirect );
					
					} else {

						if (opts.form[0].action.indexOf("signup") != -1) {
							opts.signupFailed()
						} else if (opts.form[0].action.indexOf("login") != -1) {
							opts.loginFailed()
						} else {
							opts.onError(opts.defaultErrorTitle, opts.defaultErrorMessage)
						}
					
					}
					
				} else {
					errorHandler(form, error, opts.defaultErrorTitle, opts.defaultErrorMessage)
				}
			},
			errorSubmit: function(error) {
				opts.unlockScreen()
				errorHandler(opts.form, error, opts.defaultErrorTitle, opts.defaultErrorMessage)
			}
		}

		function errorHandler(form, error, title, message) {
			
			for (var errName in opts.errors) {
				var e = opts.errors[errName]

				if (e.code == error.code) {

					if (form.attr(e.preTag + "Title")) {
						title = form.attr(e.preTag + "Title")
					} else {
						title = e.title
					}

					if (form.attr(e.preTag + "Message")) {
						message = form.attr(e.preTag + "Message")
					} else {
						message = e.message
					}

				}
			}

			opts.onError(title, message)
		}
		

		var form = $(this);
		opts.form = form
		
		for (var paramName in options) {
			if (paramName in opts) {
				opts[paramName] = options[paramName]
			}
		}

		form.ajaxForm({
			dataType: "json",
			beforeSubmit: opts.beforeSubmit,
			success: opts.successSubmit,
			error: opts.errorSubmit,
		});
		return $(this)
	}

	$.fn.OHM2AccountsSettingsForm = function(options) {

		var opts = {
			form: null,
			defaultErrorTitle: "Ops",
			defaultErrorMessage: "Something went wrong",
			errors: {
			},
			lockScreen: function() {
				utility_block_screen()
			},
			unlockScreen: function() {
				utility_unblock_screen()
			},
			lockScreenOnRedirect: function() {
				utility_block_screen()
			},
			onError: function(title, message) {
				global_error(title, message)
			},
			beforeSubmit: function(arr, $form, options) {
				opts.lockScreen()
			},
			successSubmit: function(data) {
				opts.unlockScreen()

				var error = data.error;

				if (error == null) {
					var ret = data.ret;
					location.reload()
					
				} else {
					errorHandler(form, error, opts.defaultErrorTitle, opts.defaultErrorMessage)
				}
			},
			errorSubmit: function(error) {
				opts.unlockScreen()
			}
		}

		function errorHandler(form, error, title, message) {
			
			for (var errName in opts.errors) {
				var e = opts.errors[errName]

				if (e.code == error.code) {

					if (form.attr(e.preTag + "Title")) {
						title = form.attr(e.preTag + "Title")
					} else {
						title = e.title
					}

					if (form.attr(e.preTag + "Message")) {
						message = form.attr(e.preTag + "Message")
					} else {
						message = e.message
					}

				}
			}

			opts.onError(title, message)
		}

		var form = $(this);
		opts.form = form
		
		form.ajaxForm({
			dataType: "json",
			beforeSubmit: opts.beforeSubmit,
			success: opts.successSubmit,
			error: opts.successSubmit,
		});
		return $(this)
	}

	$.fn.OHM2AccountsAvatarsForm = function(options) {

		var opts = {
			form: null,
			defaultErrorTitle: "Ops",
			defaultErrorMessage: "Something went wrong",
			oriSelector: null,
			o_75x75Selector: null,
			o_100x100Selector: null,
			o_125x125Selector: null,
			o_150x150Selector: null,
			o_200x200Selector: null,
			errors: {
			},
			lockScreen: function() {
				utility_block_screen()
			},
			unlockScreen: function() {
				utility_unblock_screen()
			},
			lockScreenOnRedirect: function() {
				utility_block_screen()
			},
			onError: function(title, message) {
				global_error(title, message)
			},
			beforeSubmit: function(arr, $form, options) {
				opts.lockScreen()
			},
			successSubmit: function(data) {
				opts.unlockScreen()

				var error = data.error;

				if (error == null) {
					var ret = data.ret;
					
					if (opts.oriSelector) {
						$(opts.oriSelector).attr("src", ret.ori)
					}

					if (opts.o_75x75Selector) {
						$(opts.o_75x75Selector).attr("src", ret.o_75x75)
					}

					if (opts.o_100x100Selector) {
						$(opts.o_100x100Selector).attr("src", ret.o_100x100)
					}

					if (opts.o_125x125Selector) {
						$(opts.o_125x125Selector).attr("src", ret.o_125x125)
					}

					if (opts.o_150x150Selector) {
						$(opts.o_150x150Selector).attr("src", ret.o_150x150)
					}

					if (opts.o_200x200Selector) {
						$(opts.o_200x200Selector).attr("src", ret.o_200x200)
					}	
						

					
				} else {
					errorHandler(form, error, opts.defaultErrorTitle, opts.defaultErrorMessage)
				}
			},
			errorSubmit: function(error) {
				opts.unlockScreen()
			}
		}

		function errorHandler(form, error, title, message) {
			
			for (var errName in opts.errors) {
				var e = opts.errors[errName]

				if (e.code == error.code) {

					if (form.attr(e.preTag + "Title")) {
						title = form.attr(e.preTag + "Title")
					} else {
						title = e.title
					}

					if (form.attr(e.preTag + "Message")) {
						message = form.attr(e.preTag + "Message")
					} else {
						message = e.message
					}

				}
			}

			opts.onError(title, message)
		}

		var form = $(this);
		opts.form = form
		
		for (var paramName in options) {
			if (paramName in opts) {
				opts[paramName] = options[paramName]
			}
		}


		form.ajaxForm({
			dataType: "json",
			beforeSubmit: opts.beforeSubmit,
			success: opts.successSubmit,
			error: opts.successSubmit,
		});
		return $(this)
	}

	$.fn.OHM2AccountsChangePassForm = function(options) {

		var opts = {
			form: null,
			defaultErrorTitle: "Ops",
			defaultErrorMessage: "Something went wrong",
			onSuccessRedirect: "/",
			errors: {
				wrong_current_password: {
					code: 179273,
					title: "Invalid current password",
					message: "Please check your current password and try again",
					preTag: "ohm2CurrPass",
				},
				passwordIsNotSecure: {
					code: 179268,
					title: "Your password is not secure",
					message: "Please choose a safer one",
					preTag: "ohm2PasswordIsNotSecure",
				},
			},
			lockScreen: function() {
				utility_block_screen()
			},
			unlockScreen: function() {
				utility_unblock_screen()
			},
			lockScreenOnRedirect: function() {
				utility_block_screen()
			},
			onError: function(title, message) {
				global_error(title, message)
			},
			beforeSubmit: function(arr, $form, options) {
				opts.lockScreen()
			},
			successSubmit: function(data) {
				opts.unlockScreen()

				var error = data.error;

				if (error == null) {
					var ret = data.ret;
					opts.lockScreen()
					window.location.replace( opts.onSuccessRedirect );						

					
				} else {
					errorHandler(form, error, opts.defaultErrorTitle, opts.defaultErrorMessage)
				}
			},
			errorSubmit: function(error) {
				opts.unlockScreen()
			}
		}

		function errorHandler(form, error, title, message) {
			
			for (var errName in opts.errors) {
				var e = opts.errors[errName]

				if (e.code == error.code) {

					if (form.attr(e.preTag + "Title")) {
						title = form.attr(e.preTag + "Title")
					} else {
						title = e.title
					}

					if (form.attr(e.preTag + "Message")) {
						message = form.attr(e.preTag + "Message")
					} else {
						message = e.message
					}

				}
			}

			opts.onError(title, message)
		}

		var form = $(this);
		opts.form = form

		for (var paramName in options) {
			if (paramName in opts) {
				opts[paramName] = options[paramName]
			}
		}

		form.ajaxForm({
			dataType: "json",
			beforeSubmit: opts.beforeSubmit,
			success: opts.successSubmit,
			error: opts.successSubmit,
		});
	}

	$.fn.OHM2AccountsResetPasswordStepOneForm = function(options) {

		var opts = {
			form: null,
			defaultErrorTitle: "Ops",
			defaultErrorMessage: "Something went wrong",
			defaultOnSuccessTitle: "Instructions sent",
			defaultOnSuccessMessage: "Check your email to continue with the process",
			defaultOnWarningTitle: "Invalid email",
			defaultOnWarningMessage: "Please check the email you provided and try again",
			errors: {
				invalidUsername: {
					code: 179268,
					title: "The username is invalid",
					message: "Please check your credentials and try again",
					preTag: "ohm2ResetPassword",
				},
			},
			lockScreen: function() {
				utility_block_screen()
	 		},
			unlockScreen: function() {
				utility_unblock_screen()
			},
			lockScreenOnRedirect: function() {
				utility_block_screen()
			},
			onError: function(title, message) { 
				global_error(title, message)
			},
			beforeSubmit: function(arr, $form, options) {
				opts.lockScreen()
			},
			successSubmit: function(data) {
				opts.unlockScreen()

				var error = data.error;

				if (error == null) {
					var ret = data.ret;
					
					if (ret) {
					
						opts.form.clearForm()
						global_success(opts.defaultOnSuccessTitle, opts.defaultOnSuccessMessage)
					
					} else {

						global_warning(opts.defaultOnWarningTitle, opts.defaultOnWarningMessage)

					}
					
				} else {
					errorHandler(form, error, opts.defaultErrorTitle, opts.defaultErrorMessage)
				}
			},
			errorSubmit: function(error) {
				opts.unlockScreen()
			}
		}

		function errorHandler(form, error, title, message) {
			
			for (var errName in opts.errors) {
				var e = opts.errors[errName]

				if (e.code == error.code) {

					if (form.attr(e.preTag + "Title")) {
						title = form.attr(e.preTag + "Title")
					} else {
						title = e.title
					}

					if (form.attr(e.preTag + "Message")) {
						message = form.attr(e.preTag + "Message")
					} else {
						message = e.message
					}

				}
			}

			opts.onError(title, message)
		}

		var form = $(this);
		opts.form = form

		for (var paramName in options) {
			if (paramName in opts) {
				opts[paramName] = options[paramName]
			}
		}

		form.ajaxForm({
			dataType: "json",
			beforeSubmit: opts.beforeSubmit,
			success: opts.successSubmit,
			error: opts.successSubmit,
		});
	}

	$.fn.OHM2AccountsResetPasswordStepTwoForm = function(options) {

		var opts = {
			form: null,
			defaultErrorTitle: "Ops",
			defaultErrorMessage: "Something went wrong",
			onSuccessRedirect: "/",
			defaultOnSuccessTitle: "Password changed",
			defaultOnSuccessMessage: "",
			errors: {
				invalidResetPassword: {
					code: 179270,
					title: "Invalid request",
					message: "Please start the process again",
					preTag: "ohm2ResetPassword",
				},
				passwordIsNotSecure: {
					code: 179268,
					title: "Your new password is not secure",
					message: "Please choose a safer one",
					preTag: "ohm2PasswordIsNotSecure",
				},
			},
			lockScreen: function() {
				utility_block_screen()
	 		},
			unlockScreen: function() {
				utility_unblock_screen()
			},
			lockScreenOnRedirect: function() {
				utility_block_screen()
			},
			onError: function(title, message) { 
				global_error(title, message)
			},
			beforeSubmit: function(arr, $form, options) {
				opts.lockScreen()
			},
			successSubmit: function(data) {
				opts.unlockScreen()

				var error = data.error;

				if (error == null) {
					var ret = data.ret;
					
					
					global_success(opts.defaultOnSuccessTitle, opts.defaultOnSuccessMessage, function(isConfirm) {

						opts.lockScreenOnRedirect()
						window.location.replace( opts.onSuccessRedirect );

					})
					
					
				} else {
					errorHandler(form, error, opts.defaultErrorTitle, opts.defaultErrorMessage)
				}
			},
			errorSubmit: function(error) {
				opts.unlockScreen()
			}
		}

		function errorHandler(form, error, title, message) {
			
			for (var errName in opts.errors) {
				var e = opts.errors[errName]

				if (e.code == error.code) {

					if (form.attr(e.preTag + "Title")) {
						title = form.attr(e.preTag + "Title")
					} else {
						title = e.title
					}

					if (form.attr(e.preTag + "Message")) {
						message = form.attr(e.preTag + "Message")
					} else {
						message = e.message
					}

				}
			}

			opts.onError(title, message)
		}

		var form = $(this);
		opts.form = form

		for (var paramName in options) {
			if (paramName in opts) {
				opts[paramName] = options[paramName]
			}
		}

		form.ajaxForm({
			dataType: "json",
			beforeSubmit: opts.beforeSubmit,
			success: opts.successSubmit,
			error: opts.successSubmit,
		});
	}

})(jQuery);