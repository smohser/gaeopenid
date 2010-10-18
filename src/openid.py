# -*- coding: utf-8 -*-
'''
Created on Oct 17, 2010

@author: yejun
'''
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

ID_PROVIDERS = {
               'google' : 'http://google.com/accounts/o8/id',
               'myopenid'  : 'http://myopenid.com/',
               'aol' : 'http://openid.aol.com/',
               'myspace' : 'http://myspace.com/',
               'yahoo' : 'http://me.yahoo.com/', 
               'versign' : 'http://pip.verisignlabs.com/',
               'launchpad' : 'http://login.launchpad.net/'
               }


class OpenID(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            self.response.out.write('''<!DOCTYPE html>
<html>
<head>
<title>Authorized</title>
    <script language="Javascript" type="text/javascript">
        //<![CDATA[
        if (window.opener && !window.opener.closed) {
            window.opener.location.reload();
        }
        window.close();
        //]]>
    </script>
</head>
<body>
</body>
</html>''')
            return 
        openid_url = self.request.get('openid_url', None)
        if openid_url is None or len(openid_url.strip()) == 0:
            openid_url = ID_PROVIDERS.get(self.request.get('provider'), None)
        if openid_url is not None:
            self.redirect(users.create_login_url(self.request.uri, 
                            federated_identity = openid_url))
            return
        else:
            self.response.out.write('''<!DOCTYPE html>
<html>
<head>
<title>What's Your OpenID URL</title>
    <!--[if lt IE 9]>
        <script src="/static/js/IE9.js" type="text/javascript"></script><![endif]-->
<style type="text/css">
    html, body, h1, form, fieldset, legend, ol, li {
    margin: 0;
    padding: 0;
    }
    body {
    background: #ffffff;
    color: #111111;
    padding: 20px;
    }
    #openid_url{background:url(/static/image/openid.png) no-repeat #FFF 2px; font-size: 16px; font-family: Calibri,sans-serif; padding-left:26px; width: 350px; height: 24px}
    button {font-size: 16px; font-family: Calibri,sans-serif; margin:10px}
</style>
</head>
<body>
<form id="provider" method="post" name="provider">
<div style="text-align: center; border-radius: 15px;background: #eeeeee; margin:150px 80px 0 80px">
<input id="openid_url" name="openid_url" type="text" placeholder="Please Enter Your OpenID" required autofocus/>
<button type="submit"/>Sign in</button>
</div>
</form>
</body>
</html>
            ''')
    post = get

application = webapp.WSGIApplication([('/openid', OpenID)], debug=True)

def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()
