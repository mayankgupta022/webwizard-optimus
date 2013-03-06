import gdata.docs
import gdata.docs.service
import gdata.spreadsheet.service
import re, os

#Gets data from a specific spreadsheet with the required title
def getdata(title,chartname):
    gd_client = gdata.spreadsheet.service.SpreadsheetsService()
    #gd_client.source = 'appspotsite.com'
    gd_client.email = 'webwizarddummy@gmail.com'
    gd_client.password = 'webwizarddummy'
    gd_client.ProgrammaticLogin()
    q = gdata.spreadsheet.service.DocumentQuery()
    q['title'] = chartname
    q['title-exact'] = 'true'
    feed = gd_client.GetSpreadsheetsFeed(query=q)
    spreadsheet_id = feed.entry[0].id.text.rsplit('/',1)[1]
    #spreadsheet_id = '0AsgIq4778ozjdE9oZFZ0Sk4xbU5GOUpzcHhpenZhWEE'
    feed = gd_client.GetWorksheetsFeed(spreadsheet_id)
    worksheet_id = feed.entry[0].id.text.rsplit('/',1)[1]
    rows = gd_client.GetListFeed(spreadsheet_id, worksheet_id).entry
    for row in rows:
        if row.custom['title'].text == title:
            #print row.custom['content'].text
            return row
            
#getdata('about')