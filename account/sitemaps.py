
from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from .models import *


class StaticViewSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0
    protocol = 'https'

    def items(self):
        return ['aboutus', 'contact', 'logout', 'error', 'login', 'signup', 'success']

    def location(self, item):
        return reverse(item)
