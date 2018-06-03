from wedsite.conf import settings

def wedsite_context(request):
	"""
	Automatically adds all wedsite data to the template context s.t. we don't
	need custom views to do so.
	"""
	return settings.WEDSITE_JSON