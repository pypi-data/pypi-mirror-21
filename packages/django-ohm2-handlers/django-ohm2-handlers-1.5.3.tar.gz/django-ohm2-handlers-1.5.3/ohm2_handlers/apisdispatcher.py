from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from . import utils as h_utils
from . import settings
from .decorators import ohm2_handlers_safe_request
from . import definitions as handlers_definitions
from . import errors as handlers_errors
from operator import itemgetter
import os, time, random, datetime



@ohm2_handlers_safe_request
def view_base(request, version, method, function, keys):
	if request.method == method:
		params, holder = {"request" : request, "version" : version}, getattr(request, method)
		for o in keys:
			params[o[0]] = holder.get(o[1],o[2])
		return function(params)
	raise handlers_definitions.HandlersMethodException(request.method, request.META.get("REMOTE_ADDR", ""))

@ohm2_handlers_safe_request
def view_base_json(request, version, method, function, keys):
	if request.method == method:
		try:
			holder = json.loads(request.body)
		except ValueError:
			return {"error" : {"code" : -1, "message": "Invalid JSON object"}}
		params = {"request" : request, "version" : version}
		for o in keys:
			params[o[0]] = holder.get(o[1],o[2])
		return function(params)
	raise handlers_definitions.HandlersMethodException(request.method, request.META.get("REMOTE_ADDR", ""))


@ohm2_handlers_safe_request
def view_base_data(request, version, method, function, keys):
	if request.method == method:
		params = {"request" : request, "version" : version}
		for o in keys:
			params[o[0]] = request.data.get(o[1],o[2])
		return function(params)
	raise handlers_definitions.HandlersMethodException(request.method, request.META.get("REMOTE_ADDR", ""))


def create_landing_message(params):
	p = h_utils.cleaned(params, (
							("request", "request", ""),
							("string", "version", 1),
							("string", "name", 1),
							("string", "subject", 1),
							("string", "message", 1),
							("string", "g-recaptcha-response", 0),
					 	))

	request = p["request"]

	if len(p["g-recaptcha-response"]) > 0:
		success = h_utils.check_google_recaptcha(p["g-recaptcha-response"], request.META.get("REMOTE_ADDR", "127.0.0.1"))
		if not success:
			return {"error" : handlers_definitions.HandlersRunException(**handlers_errors.INVALID_GOOGLE_RECHAPTCHA).regroup()}

	message = h_utils.create_landingmessage(p["name"], p["subject"], p["message"], request.META.get("REMOTE_ADDR", "127.0.0.1"))

	if settings.NOTIFY_LANDING_MESSAGE:

		try:

			for admin in settings.ADMINS:
				
				h_utils.send_html_email(admin[1],
										"no-replay@" + settings.HOST,
										admin[0] + ": new landing message",
										"identity: {0}".format(message.identity))

			
		except Exception as e:
			pass


	ret = {
		"error" : None,
		"ret" : True,
	}
	return ret


def create_landing_email(params):
	p = h_utils.cleaned(params, (
							("request", "request", ""),
							("string", "version", 1),
							("string", "email", 5),
							("string", "g-recaptcha-response", 0),
					 	))
		
	request = p["request"]

	if len(p["g-recaptcha-response"]) > 0:
		success = h_utils.check_google_recaptcha(p["g-recaptcha-response"], request.META.get("REMOTE_ADDR", "127.0.0.1"))
		if not success:
			return {"error" : handlers_definitions.HandlersRunException(**handlers_errors.INVALID_GOOGLE_RECHAPTCHA).regroup()}

	email = h_utils.create_landingemail(p["email"], request.META["REMOTE_ADDR"])


	if settings.NOTIFY_LANDING_EMAIL:

		try:

			for admin in settings.ADMINS:
				
				h_utils.send_html_email(admin[1],
										"no-replay@" + settings.HOST,
										admin[0] + ": new landing email",
										"identity: {0}".format(email.identity))
				
			
		except Exception as e:
			pass

	ret = {
		"error" : None,
		"ret" : True,
	}
	return ret	


