public: yes
tags: [python, JSON, web]
summary: |
  Pages and components are nice abstractions to work with when testing web
  applications. But manually switching pages and working with modern JavaScript
  pages requires a lot of annoying boiler plate. Keteparaha is a toolkit that
  abstracts much of that annoyance away.

Keteparaha - A testing framework for modern web apps
====================================================

I started writing `Keteparaha <http://keteparaha.aychedee.com/>`_ earlier this
year after joining a new startup where I was attempting to teach the rest of
the team functional testing techniques.

Using the `Selenium Webdriver API <http://selenium-python.readthedocs.org/en/latest/api.html>`_
directly felt so... *clunky*. Explaining to someone who isn't already sold on
functional testing that the reason the button click failed was *probably*
because the JavaScript that was meant to bind the click event didn't run fast
enough. Well that was probably why it worked on my machine but not theirs. Or
that I wanted them to use Page objects to hold the logic associated with each
page and Component objects to represesnt parts of the page. **But** they would
have to manage creating and returning these themselves.

So Keteparaha does that stuff for you. When the URL of the browser changes it
looks up to see if it knows which page object it should be on now. When you
click a button you can tell it to wait for a new component to appear and then
it will return it to you. When you ask to click a link. It will make sure that
the link is actually clickable. And tell you if it isn't. You can see a usage
example below. But `full keteparaha API documentation can be found here <http://keteparaha.aychedee.com/>`_.

.. code-block::  python

    from keteparaha import BrowserTestCase, Component, Page

    SERVER_URL = 'http://www.simple.com/{}'


    class LoginPage(Page):
        url = SERVER_URL.format('login/')

        def login(self, email, password):
            self.enter_text('input[name=email]', email)
            self.enter_text('input[name=password]', email)
            return self.click('input[name=submut]')


    class Dashboard(Page):
        url = SERVER_URL.format('dashboard/')

        def logged_in_username(self):
            return self.get_component('.username').text

        def open_comment_modal(self, comment):
            return self.click_button('Feedback', opens='#comment')


    class CommentModal(Component)
        selector = '#comment'

        def comment(self, message):
            self.enter_text('input[name=message]', message)
            self.click('input[type=submit]')


    # User logs in and is redirected to the dashboard
    dashboard = LoginPage(self.driver).login('a@b.com', 'xxxxx')

    # Their username is in the top menu
    self.assertEqual(dashboard.logged_in_username(), 'aychedee')

    # They can leave some feedback for the site owner
    comment_modal = dashboard.open_comment_modal()
    comment_modal.comment("Is it tea you're looking for?")

If an input field is inactive, it'll wait for it to become active, in the
hope that a bit of JavaScript hasn't yet been run.

Hopefully it makes functionally testing a modern JS heavy web app a lot easier.
