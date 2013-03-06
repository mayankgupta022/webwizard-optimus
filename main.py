#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import webapp2
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
import wsgiref.handlers
from google.appengine.ext.webapp import template


import atom.url

import gdata.service
import gdata.alt.appengine
import gdata.photos.service
import gdata.media
import gdata.geo
import gdata.youtube
import gdata.youtube.service

from getdata import *
from pygooglechart import Chart
from pygooglechart import SimpleLineChart
from pygooglechart import Axis


class IndexHandler(webapp2.RequestHandler):
    def get(self):
        username = 'aayushahuja'
        gd_client = gdata.photos.service.PhotosService()
        
        albums = gd_client.GetUserFeed(user=username)
        for album in albums.entry:
            if album.title.text == 'test':
                photos = gd_client.GetFeed(
                                   '/data/feed/api/user/%s/albumid/%s?kind=photo' % (
                                                                     username, album.gphoto_id.text))
        title  = 'about'
        subtitle = getdata(title,'NGOData').custom['subtitle'].text
        content = getdata(title,'NGOData').custom['content'].text
        self.response.content_type='text/html'
        self.response.out.write(template.render('template/index.html',{
                                                'photolist':photos.entry,
                                                'page_title':title.title(),
                                                'page_subtitle':subtitle,
                                                'page_content':content,
                                                                                   }))
class CharitiesHandler(webapp2.RequestHandler):
    def get(self):
        
        title  = 'charities'
        subtitle = getdata(title,'NGOData').custom['subtitle'].text
        content = getdata(title,'NGOData').custom['content'].text
        self.response.content_type='text/html'
        self.response.out.write(template.render('template/standard.html',{
                                            
                                                'page_title':title.title(),
                                                'page_subtitle':subtitle,
                                                'page_content':content,
                                                                                   }))

class ProgramsHandler(webapp2.RequestHandler):
    def get(self):
        title  = 'programs'
        subtitle = getdata(title,'NGOData').custom['subtitle'].text
        content = getdata(title,'NGOData').custom['content'].text
        self.response.content_type='text/html'
        self.response.out.write(template.render('template/standard.html',{
                                            
                                                'page_title':title.title(),
                                                'page_subtitle':subtitle,
                                                'page_content':content,
                                                                                   }))
class ActivitiesHandler(webapp2.RequestHandler):
    def get(self):
        
        title  = 'activities'
        subtitle = getdata(title,'NGOData').custom['subtitle'].text
        content = getdata(title,'NGOData').custom['content'].text
        self.response.content_type='text/html'
        self.response.out.write(template.render('template/standard.html',{
                                            
                                                'page_title':title.title(),
                                                'page_subtitle':subtitle,
                                                'page_content':content,
                                                                                   }))


class YoutubeHandler(webapp2.RequestHandler):
    def PrintVideoFeed(feed):
        for entry in feed.entry:
            PrintEntryDetails(entry)
    def get(self):
        username = 'tseries' # to be changed to NGO's username
        yt_service = gdata.youtube.service.YouTubeService()
        uri = 'http://gdata.youtube.com/feeds/api/users/%s/uploads' % username
        feed = yt_service.GetYouTubeVideoFeed(uri)
        list = []
        for entry in feed.entry:
            list.append(entry.GetSwfUrl())
        list = list[0:4]
        self.response.out.write(template.render('template/videos.html',{
                                                'list':list,
                                                                                   }))
        

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.redirect('/index')  
        
class ContactsHandler(webapp2.RequestHandler):
    def get(self):
        title  = 'contacts'
        subtitle = getdata(title,'NGOData').custom['subtitle'].text
        content = getdata(title,'NGOData').custom['content'].text
        self.response.content_type='text/html'
        self.response.out.write(template.render('template/contacts.html',{
                                                
                                                                 'page_title':title.title(),
                                                                 'page_subtitle':subtitle,
                                                                 'page_content':content,                  }))
        
class DonationHandler(webapp2.RequestHandler):
    def get(self):
        list = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep']
        list2 = []
        for title in list:
            list2.append( int(getdata(title,'funds').custom['amount'].text))
        max_y = 10000
        chart = SimpleLineChart(200, 125, y_range=[0, max_y])
        
        chart.add_data([2000,3000,5000,1200,5000,4000,1000,3000,5900])
        
        # Set the line colour to blue
        chart.set_colours(['0000FF'])
        
        # Set the vertical stripes
        chart.fill_linear_stripes(Chart.CHART, 0, 'CCCCCC', 0.2, 'FFFFFF', 0.2)
        
        # Set the horizontal dotted lines
        chart.set_grid(0, 25, 5, 5)
        
        # The Y axis labels contains 0 to 100 skipping every 25, but remove the
        # first number because it's obvious and gets in the way of the first X
        # label.
        left_axis = range(0, max_y + 1, 25)
        left_axis[0] = ''
        chart.set_axis_labels(Axis.LEFT, left_axis)
        
        # X axis labels
        chart.set_axis_labels(Axis.BOTTOM, list)
        
        url2 = chart.get_url()
        self.response.out.write(template.render('template/donate.html',{
                                                
                                                                 'url2' :url2,                }))
    

                          

                                                                          
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/index', IndexHandler),
    ('/activities', ActivitiesHandler),
    ('/charities', CharitiesHandler),
    ('/programs', ProgramsHandler),
    ('/contacts', ContactsHandler),
    ('/donate', DonationHandler),
    ('/videos', YoutubeHandler),
], debug=True)
