# django-wedsite

## Overview

`django-wedsite` aims to provide a quick, easy-to-use open source django app
that allows you to flexibly build a custom website for your wedding without
needing to jump through the typical hoops of getting a site up and running.

You can see an [example of the app running on Heroku](https://django-wedsite.herokuapp.com)
and can see the source of that app on [Github](https://github.com/dpipemazo/django-wedsite).

`django-wedsite` ships with default settings/text that can easily be overriden
in your main web app.

## Quick setup

To test out the package and see the default site, you can simply do the
following:

### Add app to `installed_apps`:

In your site's `settings.py` file you'll need to add the following apps

```
import wedsite

...

INSTALLED_APPS = [
    ...
    'wedsite',
    'easy_maps',
    'raven.contrib.django.raven_compat',
    'tz_detect',
    'django_inlinecss',
    ...
]
```

### Add URLS

Modify your `urls.py` to contain the `wedsite` URLS.

```
import wedsite

...

urlpatterns = [

    # Wedding app will be at top-levels
    url(r'', include('wedsite.urls')),

    ...
]
```

### Launch

With that done you should be all set and your site should be serving
the default `django-wedsite` app. Launch and test!

### Customization

Once the basic site is launched, it's fun to try out some quick customization
that will give you a feel for how the more advanced customization will work. In
your django app, add a file that will be used for configuring wedsite. You
can use any name, but something like `wedsite_conf.py` is recommended. In this
file, try out the following code:

```
from wedsite.settings import DEFAULT_JSON

CUSTOMIZED_JSON = DEFAULT_JSON
CUSTOMIZED_JSON['broom']['last_name'] = "Pandas"
```

And now in your `settings.py` file, add the following
```
from myapp.wedsite_conf import CUSTOMIZED_JSON

...

WEDSITE_JSON = CUSTOMIZED_JSON
```

You should now see that the Broom's last name on the landing page is "Pandas".
The concept for customizing the whole site would then be to add as much detail
as you'd like to your `CUSTOMIZED_JSON`. You should find that everything you
need is in there. See [`settings.py`](wedsite/settings.py) for all of the
fields you can change.

## Package Architecture

### Overview

The site primarily serves up static pages of django-templated HTML. The main
dynamic features of the site are:

1. User Accounts
2. User RSVPs
3. User mass emailing
4. Page view restriction to authorized users
5. Admin UI

### Static Pages

#### Templates

Page templates are split into two categories: blocks and pages. Blocks are pieces of
code that are utilized in multiple pages and pages utilize blocks to build a full
web page.

The main block for the site is [`base.html`](templates/wedding/blocks/base.html)
which defines the navbar, javascript, title, footer and all other shared resources for
the site. 

Each of the [`pages`](wedding/blocks/pages) then imports the base template and generally
just fills in the page title and content.

#### URLs and access restriction

The site map is defined in [`urls.py`](wedding/urls.py). If you were going to add/remove
a page it should be done here. For each page that you want to serve on the site, add a
line to the `urlpatterns` list. In the line you'll need to specify the page template
for the site as well as the view class you'd like to use to serve the template. Note that
for static HTML pages there are two view choices:

1. `StaticView`
2. `StaticViewNoAuth`

If you choose `StaticView` then it will require a user to log in to access the page, else
if you choose `StaticViewNoAuth` the page will be accessible without login.

#### Adding a basic page to the site

Using just your knowledge of templates and URLS from above you can go ahead and add a new
page to the site! Simply make a new template in the `pages` directory and add its
desired URL to the `urlpatterns` with either `StaticView` or `StaticViewNoAuth` and you
should be good to go!

### Users and RSVPs

#### User Model

This site uses the standard Django user model. The standard django account
pages have been skinned in the theme of the site in the
[`registration` templates](templates/registration). In order to get some
flexibility in the user data a [`Profile`](wedding/models.py) model has been
added as a 1:1 field with a user, created when the user is created. Eventually
the goal is to add a "user account" page to the site where users can update their
address and contact info using this profile but those features aren't yet built.

#### User Account Creation

A custom account creation view has been built such that only users who have
a valid RSVP in the system can create an account. The site currently checks
a user's last name and the numerical digits of their address for a match
in the "unclaimed" RSVPs in the database. An "uncliamed" RSVP is an RSVP
which does not have a Foreign Key to a user. The admin of the site needs to
manually enter all of their  

#### RSVP Models

The RSVP system consists of two models: RSVP and RSVP Person

##### RSVP Model

The RSVP maps 1:1 to an invitation you sent out. It has the following important
fields:

| Field | Description |
|-------|-------------|
| `last_names` | Comma-separated last names for anyone expected to claim the invite |
| `address` | Full address that the invite was sent to. Only the numbers really matter |
| `response` | Coment section the user can fill out when submitting their response |

An RSVP contains a 1:many relationship with RSVP Persons

##### RSVP Person Models

Each RSVP Person has the following important fields

| Field | Description |
|-------|-------------|
| `name` | Person's Name |

Along with the above fields, the RSVP person model should and can be modified to contain
any/all of the information you'd like to gather from the person when they submit their 
response on the web site. The default RSVP person contains the following additional fields

| Field | Type | Description |
| `is_attending_rehearsal` | Boolean | Whether or not they're attending the rehearsal dinner |
| `is_attending_wedding` | Boolean | Whether or not they're attending the wedding |
| `is_child` | Boolean | Whether or not the guest counts as a child |
| `dietary_*` | Boolean | Various dietary restrictions |
| `table` | Integer | Currently unused, but would be nice for building a seating assignment chart |

#### Loading RSVPs into the site

With a basic understanding of the above RSVP system, you'll want to go ahead and load your
RSVPs into the system so that your users can claim them. To do this, log into the admin
UI at
```
https://my_site/admin
```
using your superuser credentials. Then go to the `RSVP` page and you can manually add
RSVPs. This can indeed be a bit tedious; it would be nice to create a management command
to take in a CSV or JSON data file and make all of the RSVP objects.

