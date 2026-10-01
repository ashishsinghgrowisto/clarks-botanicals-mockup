#!/usr/bin/env python3
"""Clark's Botanicals -> pixel-match self-contained static mockup generator."""
import json, os, re, sys, hashlib, shutil, urllib.request, html as H

HERE = os.path.dirname(os.path.abspath(__file__))
CAP  = os.path.join(os.path.dirname(HERE), 'cap')
OUT  = os.path.join(os.path.dirname(HERE), 'clarks-mockups')
ASSETS = os.path.join(OUT, 'assets')
PASSWORD = os.environ.get('CB_PW', 'clarks2026')

sys.path.insert(0, HERE)
from parts_css import CSS
from parts_js import JS

P = json.load(open(os.path.join(CAP, 'data_products.json')))
ACC = dict((t, b) for t, b in json.load(open(os.path.join(CAP, 'pdp_accordions.json'))))
BY = {p['handle']: p for p in P}
# Real Okendo rating + review count per handle, scraped from the live PDPs.
# Products the store shows no reviews for map to None and get no badge.
REV = json.load(open(os.path.join(CAP, 'reviews.json')))

CDN = 'https://clarksbotanicals.com/cdn/shop/files/'
LOGO      = CDN + 'Blue_Logo_560_x_160_px.png?v=1786465543&width=560'
HERO      = CDN + 'sale-edit-no-code-desktop.jpg?v=1788303416&width=2000'
JASMINE   = CDN + 'Untitled_design_2.png?v=1776197445&width=2400'
SUB_IMG   = CDN + 'SUB_8d4910c9-954c-4a29-a9f4-818dbc9e11fa.png?v=1751302285&width=2400'
STORY_IMG = CDN + '01_FRANCESCO_047_8f1057bb-04c0-4945-a8b2-4b08902cfe5b_2200x-opt.jpg?v=1650735066&width=2200'
HOME_BA_B = CDN + '3_f8ac3ea6-b6c6-4c16-9def-1b91bec146b4.png?v=1747423057&width=1800'
HOME_BA_A = CDN + '2_d662c562-833b-4968-a618-d2d559411051.png?v=1748581899&width=1800'
PDP_BA_B  = CDN + 'Screenshot_2026-04-06_at_10.35.28_AM.png?v=1775486192&width=1600'
PDP_BA_A  = CDN + 'Screenshot_2026-04-06_at_10.36.11_AM.png?v=1775486219&width=1600'
AMALFI    = CDN + 'EC9E489D-C8C8-4183-A154-3B0306715259.jpg?v=1775235185&width=1600'
FLAG      = 'https://cdn.shopify.com/static/images/flags/in.svg?format=jpg&width=60'

PRESS = [
  ('&ldquo;Completely reimagined without synthetic fragrances with a commitment to cleaner beauty.&rdquo;',
   CDN + 'white1200px-Gooponlinelogo.svg_copy.png?v=1614411634&width=600'),
  ('&ldquo;After a few days, my Walking Dead complexion began to return to the land of the living, '
   'and I was officially hooked.&rdquo;',
   CDN + 'Vogue_logo.png?v=1684255337&width=600'),
  ('&ldquo;Clark&rsquo;s Botanicals is a staple in my nighttime routine - it makes a noticeable difference '
   'in the brightness and smoothness after just one use.&rdquo;',
   CDN + 'byrdie-logo_copy.png?v=1614411634&width=600'),
]
BAND_1 = [CDN + x for x in [
  'RROC_1fb4410b-aeff-422f-898f-42666a1493a5.png?v=1749761474&width=2400',
  'HOMEPAGE_CLINICALS_55249e15-eda0-46ef-9e22-85989dcd21f3.png?v=1752783543&width=2400',
  'Smoothing_Marine_Cream_a8071ff3-376d-4be9-bcd6-627996e52b31.png?v=1752785810&width=2400',
  'jvc.png?v=1753296735&width=2400',
  'HOMEPAGE_CLINICALS_apec.png?v=1753295713&width=2400']]

ANNOUNCE = 'Early access until Sept 1 | Use code LABOR25'
# Rails added in the CRO revision. Handles only - product_card() supplies pricing,
# badges and review counts, so these stay in step with the catalogue.
# Anti-Puff Eye Cream is deliberately absent from both: it is in SOLD_OUT.
BESTSELLERS  = ['smooth-marine-cream', 'retinol-rescue-overnight-cream',
                'deep-moisture-mask', '3-minute-reset']
NEW_ARRIVALS = ['dna-42-clinicalift-serum', 'pdrn-retinol-liquid-facelift-duo',
                '7-acid-daily-glow-peel', 'the-longevity-lift-duo']
# PDP 'past purchases' rail. Reason copy is illustrative until real order data exists.
RECS = [('deep-moisture-mask',  'Pairs with your Marine Cream'),
        ('jasmine-vital-cream', 'Completes your morning routine'),
        ('smooth-marine-cream', 'You reordered this in March'),
        ('the-renewal-ritual',  'Based on your last two orders')]

FREE_SHIP = 75.0        # placeholder threshold for the sticky panel's progress bar
SUB_DISCOUNT = 0.15

NAV = [
 ('Shop', 'collection.html', [
    ('Shop All','collection.html'), ('Cleansers &amp; Exfoliators','collection.html'),
    ('Eye Cream','collection.html'), ('Moisturizers','collection.html'),
    ('Lip Treatment','collection.html'), ('Treatments and Masks','collection.html'),
    ('Sets','collection.html')]),
 ('Skin Benefit', 'collection.html', [
    ('Age Defying','collection.html'), ('Hydrating','collection.html'),
    ('Brightening','collection.html'), ('Soothing','collection.html'),
    ('Oil Control','collection.html')]),
 ('Skin Type', 'collection.html', [
    ('All Skin Types','collection.html'), ('Normal Skin','collection.html'),
    ('Oily Skin','collection.html'), ('Combination Skin','collection.html'),
    ('Very Drying &amp; Aging Skin','collection.html'), ('Dry / Redness Prone Skin','collection.html')]),
 ('Subscribe + Save', 'collection.html', [
    ('Subscribe + Save','collection.html'), ('Manage Subscription','#')]),
 ('Ritual Rewards', '#', []),
 ('Skincare Quiz', '#', []),
 ('Skin Edu', '#', [('Blog','#')]),
 ('About', '#', [
    ('Our Story','#'), ('Formulation Innovation','#'),
    ('FSA / HSA Eligibility','#'), ('Customer Service','#')]),
]

# label, hero image handle, product types it covers, extra handles (products with no type set)
CATEGORIES = [
  ('Cleansers &amp; Exfoliators', '7-acid-daily-glow-peel', ['Cleansers & Exfoliators'], []),
  ('Eye Cream',                   'anti-puff-eye-cream',    ['Eye Moisturizers'],        []),
  ('Moisturizers',                'smooth-marine-cream',    ['Moisturizers'],            []),
  ('Lip Treatment',               'travel-lip-duo',         ['Lip Treatment'],           []),
  ('Treatments and Masks',        'deep-moisture-mask',     ['Serums + Masks'],
                                                            ['dna-42-clinicalift-serum']),
  ('Sets',                        'the-renewal-ritual',     ['Sets'],  ['3-minute-reset']),
]

PLP_ORDER = ['dna-42-clinicalift-serum','retinol-rescue-overnight-cream','deep-moisture-mask',
             'smooth-marine-cream','jasmine-vital-cream','anti-puff-eye-cream',
             '7-acid-daily-glow-peel','pdrn-retinol-liquid-facelift-duo','power-couple',
             '24-hour-hormone-calm-ritual','the-glow-edit-set','regeneration-24-7-180-value',
             '3-minute-reset','travel-lip-duo','the-longevity-lift-duo','the-renewal-ritual']
SOLD_OUT = {'anti-puff-eye-cream'}
EDITORS = ['dna-42-clinicalift-serum','retinol-rescue-overnight-cream','deep-moisture-mask','smooth-marine-cream']
RELATED = ['3-minute-reset','retinol-rescue-overnight-cream','regeneration-24-7-180-value','deep-moisture-mask']
RECENT  = ['smooth-marine-cream','retinol-rescue-overnight-cream','jasmine-vital-cream','7-acid-daily-glow-peel']
# Complete-the-routine products offered under the PDP buy button. Cleanse, treat,
# moisturise, mask — the steps the serum sits between, not more serums.
PAIRS   = ['7-acid-daily-glow-peel','smooth-marine-cream','deep-moisture-mask',
           'retinol-rescue-overnight-cream','jasmine-vital-cream','travel-lip-duo',
           'anti-puff-eye-cream']

# ---------------------------------------------------------------- icons
IC = {
 'burger': '<svg width="24" height="24" fill="none" viewBox="0 0 24 24"><path d="M1 19h22M1 12h22M1 5h22" stroke="currentColor" stroke-width="1.7" stroke-linecap="square"/></svg>',
 'account': '<svg width="23" height="23" fill="none" viewBox="0 0 24 24"><path d="M16.125 8.75c-.184 2.478-2.063 4.5-4.125 4.5s-3.944-2.021-4.125-4.5c-.187-2.578 1.64-4.5 4.125-4.5 2.484 0 4.313 1.969 4.125 4.5Z" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/><path d="M3.017 20.747C3.783 16.5 7.922 14.25 12 14.25s8.217 2.25 8.984 6.497" stroke="currentColor" stroke-width="1.6" stroke-miterlimit="10"/></svg>',
 'search': '<svg width="23" height="23" fill="none" viewBox="0 0 24 24"><path d="M10.364 3a7.364 7.364 0 1 0 0 14.727 7.364 7.364 0 0 0 0-14.727Z" stroke="currentColor" stroke-width="1.6" stroke-miterlimit="10"/><path d="M15.857 15.858 21 21.001" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>',
 'cart': '<svg width="23" height="23" fill="none" viewBox="0 0 24 24"><path d="M21.5 21.5v-15h-19v15h19ZM8 6V5a4 4 0 1 1 8 0v1" stroke="currentColor" stroke-width="1.6"/></svg>',
 'chev': '<svg width="11" height="11" fill="none" viewBox="0 0 10 10"><path d="m1 3 4 4 4-4" stroke="currentColor" stroke-linecap="square"/></svg>',
 'chevR': '<svg width="10" height="10" fill="none" viewBox="0 0 10 10"><path d="m3 1 4 4-4 4" stroke="currentColor" stroke-linecap="square"/></svg>',
 'chevL': '<svg width="10" height="10" fill="none" viewBox="0 0 10 10"><path d="m7 1-4 4 4 4" stroke="currentColor" stroke-linecap="square"/></svg>',
 'chevDown': '<svg width="14" height="14" fill="none" viewBox="0 0 10 10"><path d="m1 3 4 4 4-4" stroke="currentColor" stroke-linecap="square"/></svg>',
 'close': '<svg width="16" height="16" fill="none" viewBox="0 0 16 16"><path d="m1 1 14 14M1 15 15 1" stroke="currentColor" stroke-width="1.6"/></svg>',
 'fb': '<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M15 3h-2.5A3.5 3.5 0 0 0 9 6.5V9H7v3h2v9h3v-9h2.5l.5-3h-3V6.75c0-.41.34-.75.75-.75H15V3Z"/></svg>',
 'ig': '<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.4" cy="6.6" r=".9" fill="currentColor" stroke="none"/></svg>',
 'pin': '<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M9.5 20.5c-.4-1.4-.2-3 .1-4.3l1.3-5.4"/><path d="M12 3a7 7 0 0 0-2.6 13.5"/><path d="M10.6 13.4c.4.8 1.3 1.3 2.3 1.3 2.2 0 3.8-2.3 3.8-5.3C16.7 6.4 14.6 4.6 12 4.6"/></svg>',
 'play': '<svg width="11" height="11" viewBox="0 0 12 12" fill="currentColor"><path d="M3 1.5 10 6l-7 4.5V1.5Z"/></svg>',
 'arrowDown': '<svg width="14" height="14" fill="none" viewBox="0 0 14 14"><path d="M7 1v11M2.5 8 7 12.5 11.5 8" stroke="currentColor" stroke-width="1.4"/></svg>',
 'leaf': '<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3"><path d="M20 4C10 4 4 9 4 16c0 2 .7 3.4.7 3.4S8 12 18 9c0 0-6 3-9.5 8.5"/></svg>',
 'rabbit': '<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3"><path d="M8 12c-1-4-2-7-4-8 0 3 .5 6 2 8"/><path d="M13 12c1-4 2-7 4-8 0 3-.5 6-2 8"/><circle cx="11.5" cy="16" r="5"/><circle cx="10" cy="15" r=".7" fill="currentColor"/><circle cx="13" cy="15" r=".7" fill="currentColor"/></svg>',
 'wheat': '<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3"><path d="M12 21V9"/><path d="M12 9c0-3 2-5 4-5 0 3-2 5-4 5Zm0 0c0-3-2-5-4-5 0 3 2 5 4 5Zm0 5c0-2.5 2-4 4-4 0 2.5-2 4-4 4Zm0 0c0-2.5-2-4-4-4 0 2.5 2 4 4 4Z"/></svg>',
 'vegan': '<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3"><path d="M5 4l7 16 7-16"/></svg>',
 'flagus': '<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3"><rect x="3" y="6" width="18" height="12"/><path d="M3 10h18M3 14h18M3 6v12"/></svg>',
}

PAYMENTS = [('amazon','#FF9900'),('amex','#1F72CD'),('apple','#000000'),('diners','#0079BE'),
            ('discover','#FF6000'),('gpay','#5F6368'),('mc','#EB001B'),('paypal','#003087'),
            ('shop','#5A31F4'),('visa','#1A1F71')]
PAY_LABELS = {'amazon':'amazon','amex':'AMEX','apple':'Pay','diners':'Diners','discover':'DISCOVER',
              'gpay':'G Pay','mc':'MC','paypal':'PayPal','shop':'shop','visa':'VISA'}

USD_SUFFIX = re.compile(r'(\$[\d,]+(?:\.\d{2})?)\s*USD\b')

def strip_usd(txt):
    """Drop a trailing "USD" after a $ amount; the $ already says the currency."""
    return USD_SUFFIX.sub(r'\1', txt)


def money(v):
    return '${:,.2f}'.format(v)

def img_for(p, i=0):
    return p['imgs'][i] if len(p['imgs']) > i else p['imgs'][0]

# ---------------------------------------------------------------- chrome
def gate():
    return (
      '<div id="gate"><div class="gate-card">'
      '<img src="' + LOGO + '" alt="Clark&rsquo;s Botanicals">'
      '<p class="h h6" style="margin:0 0 18px">Private preview</p>'
      '<input type="password" placeholder="ENTER PASSWORD" autocomplete="off">'
      '<button class="btn btn--full" type="button">Enter</button>'
      '<p class="gate-err"></p>'
      '</div></div>')

def announce():
    return ('<div class="ann"><div class="ann__track">'
            '<span>' + ANNOUNCE + '</span>'
            '<span aria-hidden="true">' + ANNOUNCE + '</span>'
            '</div></div>')

def primary_nav():
    out = []
    for label, href, items in NAV:
        if not items:
            out.append('<li><a class="navtop" href="' + href + '">' + label + '</a></li>')
        else:
            links = ''.join('<a href="' + u + '">' + t + '</a>' for t, u in items)
            out.append('<li><a class="navtop" href="' + href + '">' + label + '</a>'
                       '<div class="mega"><div class="mega__in">' + links + '</div></div></li>')
    return '<nav class="pnav" aria-label="Primary"><ul>' + ''.join(out) + '</ul></nav>'

def header():
    return (
      '<header class="hdr"><div class="hdr__in">'
      '<button class="hdr__burger" data-open="#menu" aria-label="Navigation menu">' + IC['burger'] + '</button>'
      '<p class="hdr__logo"><a href="home.html"><img src="' + LOGO + '" alt="Clark&rsquo;s Botanicals"></a></p>'
      '<div class="hdr__icons">'
        '<button class="loc" type="button">USD $ ' + IC['chev'] + '</button>'
        '<a class="acct" href="#" aria-label="Login">' + IC['account'] + '</a>'
        '<button type="button" data-open-search aria-label="Search">' + IC['search'] + '</button>'
        '<button type="button" data-open="#cart" aria-label="Cart">' + IC['cart'] +
        '<span class="cartdot"></span></button>'
      '</div>' + primary_nav() + '</div></header>')

def mobile_drawer():
    root, subs = [], []
    for i, (label, href, items) in enumerate(NAV):
        if not items:
            root.append('<a class="dd__item" href="' + href + '">' + label + '</a>')
        else:
            root.append('<button class="dd__item" type="button" data-sub="s' + str(i) + '">'
                        + label + IC['chevR'] + '</button>')
            inner = ''.join('<a class="dd__item" href="' + u + '">' + t + '</a>' for t, u in items)
            subs.append('<div class="dd__view sub" data-view="s' + str(i) + '">'
                        '<button class="dd__back" type="button">' + IC['chevL'] + ' All categories</button>'
                        '<p class="h h5" style="margin:0 0 10px">' + label + '</p>' + inner + '</div>')
    return (
      '<aside class="panel panel--l" id="menu">'
      '<div class="panel__hd"><span class="h">Menu</span>'
      '<button data-close aria-label="Close">' + IC['close'] + '</button></div>'
      '<div class="panel__bd" style="padding:0">'
      '<div class="dd"><div class="dd__view">' + ''.join(root) +
      '<a class="dd__item" href="#">Login</a><a class="dd__item" href="#">USD $</a>'
      '</div>' + ''.join(subs) + '</div></div></aside>')

def search_panel():
    return (
      '<div class="search"><div class="search__in">'
      '<div class="search__row">' + IC['search'] +
      '<input type="search" placeholder="Search for..." aria-label="Search">'
      '<button data-close aria-label="Close">' + IC['close'] + '</button></div>'
      '<div class="search__res">'
        '<div><p class="search__hd">Suggestions</p><div class="search__sug"></div></div>'
        '<div><div class="search__tabwrap"><span class="search__tab">Products</span></div>'
        '<div class="search__tiles"></div></div>'
      '</div></div></div>')

def cart_drawer():
    return (
      '<aside class="panel panel--r" id="cart">'
      '<div class="panel__hd"><span class="h">Cart</span>'
      '<button data-close aria-label="Close">' + IC['close'] + '</button></div>'
      '<div class="panel__bd"></div><div class="panel__ft"></div></aside>')

def footer():
    svc = ['Search','About Us','Customer Service','Where to Find Us','Corporate Gifting','Contact Us']
    hlp = ['Terms &amp; Conditions','Shipping and Returns','FAQs','Privacy Policy','Accessibility Statement']
    pay = ''.join('<span style="color:' + c + '">' + PAY_LABELS[k] + '</span>' for k, c in PAYMENTS)
    return (
      '<footer class="ft"><div class="wrap wrap--wide">'
      '<div class="ft__grid">'
        '<div><p class="h h6">About Clark&rsquo;s Botanicals</p>'
        '<p class="ft__about">Doctor-formulated skincare that gets stronger the longer you use it. '
        'Founded by Francesco Clark after a spinal cord injury transformed how he understood skin, healing, '
        'and what formulas should actually do. Sourced and studied at our research estate on the Amalfi Coast. '
        'Tested on sensitive skin. 74% of customers come back.</p></div>'
        '<div><p class="h h6">Service</p><ul>'
          + ''.join('<li><a href="#">' + x + '</a></li>' for x in svc) + '</ul></div>'
        '<div><p class="h h6">Help</p><ul>'
          + ''.join('<li><a href="#">' + x + '</a></li>' for x in hlp) + '</ul></div>'
        '<div><p class="h h6">From the Lab</p>'
        '<p class="ft__about">Subscribe for formulation insights, new science, and first access to what '
        'we are building next.</p>'
        '<div class="ft__form"><input type="email" placeholder="E-mail" aria-label="E-mail">'
        '<button class="btn btn--yellow" type="button">Subscribe</button></div></div>'
      '</div>'
      '<div class="ft__soc"><a href="#" aria-label="Follow on Facebook">' + IC['fb'] + '</a>'
      '<a href="#" aria-label="Follow on Instagram">' + IC['ig'] + '</a>'
      '<a href="#" aria-label="Follow on Pinterest">' + IC['pin'] + '</a></div>'
      '<div class="ft__aside">'
        '<span class="ft__loc"><img src="' + FLAG + '" alt="">India (USD $) ' + IC['chev'] + '</span>'
        '<span class="ft__cc">&copy; 2026 &ndash; Clark&rsquo;s Botanicals</span>'
        '<span class="ft__pay">' + pay + '</span>'
      '</div></div></footer>')

def page(title, body):
    products_js = json.dumps([
      {'handle': p['handle'], 'title': p['title'], 'price': p['price'], 'cmp': p['cmp'],
       'img': p['imgs'][0], 'opts': p['opts'],
       'rating': (REV.get(p['handle']) or {}).get('rating'),
       'rev': (REV.get(p['handle']) or {}).get('count')} for p in P])
    return (
      '<!doctype html><html lang="en"><head><meta charset="utf-8">'
      '<meta name="viewport" content="width=device-width,initial-scale=1">'
      '<title>' + title + '</title>'
      '<link rel="preconnect" href="https://fonts.googleapis.com">'
      '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
      '<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap" rel="stylesheet">'
      '<style>' + CSS + '</style></head><body class="locked">'
      + gate() +
      '<div class="site">' + announce() + header() + '<main>' + body + '</main>' + footer() + '</div>'
      + mobile_drawer() + search_panel() + cart_drawer() + variant_panel()
      + mobile_bottom_nav() +
      '<div class="ov"></div>'
      '<script>window.CB_PRODUCTS=' + products_js + ';</script>'
      '<script>' + JS.replace('__PW__', PASSWORD) + '</script>'
      '</body></html>')

def mobile_bottom_nav():
    """Fixed bottom navigation, shown below 1000px where the header carries only
    the logo. Reuses the existing drawer/search/cart handlers rather than adding
    new ones. The auth pill is a demo affordance for the signed-in PDP rail and
    should be removed once real accounts exist."""
    return (
      '<nav class="mobnav" aria-label="Primary">'
      '<button class="mobnav__item" type="button" data-open="#menu" aria-label="Open navigation menu">'
      + ICON_BURGER + 'Menu</button>'
      '<a class="mobnav__item" href="collection.html">' + ICON_GRID + 'Shop</a>'
      '<button class="mobnav__item" type="button" data-open-search aria-label="Search">'
      + ICON_SEARCH + 'Search</button>'
      '<button class="mobnav__item" type="button" data-open="#cart" aria-label="Open cart">'
      + ICON_BAG + '<span class="mobnav__dot" style="display:none"></span>Cart</button>'
      '<a class="mobnav__item" href="#" aria-label="My account">' + ICON_USER + 'Account</a>'
      '</nav>'
      '<button class="authtoggle" type="button">Signed out &middot; demo</button>')


ICON_BURGER = ('<svg width="21" height="21" fill="none" viewBox="0 0 24 24">'
  '<path d="M1 19h22M1 12h22M1 5h22" stroke="currentColor" stroke-width="1.7" stroke-linecap="square"/></svg>')
ICON_GRID = ('<svg width="21" height="21" fill="none" viewBox="0 0 24 24">'
  '<path d="M3.5 3.5h7v7h-7zM13.5 3.5h7v7h-7zM3.5 13.5h7v7h-7zM13.5 13.5h7v7h-7z" '
  'stroke="currentColor" stroke-width="1.6"/></svg>')
ICON_SEARCH = ('<svg width="21" height="21" fill="none" viewBox="0 0 24 24">'
  '<path d="M10.364 3a7.364 7.364 0 1 0 0 14.727 7.364 7.364 0 0 0 0-14.727Z" stroke="currentColor" '
  'stroke-width="1.6" stroke-miterlimit="10"/><path d="m15.857 15.858 5.143 5.143" stroke="currentColor" '
  'stroke-width="1.6" stroke-linecap="round"/></svg>')
ICON_BAG = ('<svg width="21" height="21" fill="none" viewBox="0 0 24 24">'
  '<path d="M4.5 7.5h15l-1.2 12.2a1.4 1.4 0 0 1-1.4 1.3H7.1a1.4 1.4 0 0 1-1.4-1.3z" stroke="currentColor" '
  'stroke-width="1.6"/><path d="M8.6 9.6V6.4a3.4 3.4 0 0 1 6.8 0v3.2" stroke="currentColor" '
  'stroke-width="1.6" stroke-linecap="round"/></svg>')
ICON_USER = ('<svg width="21" height="21" fill="none" viewBox="0 0 24 24">'
  '<path d="M16.125 8.75c-.184 2.478-2.063 4.5-4.125 4.5s-3.944-2.021-4.125-4.5c-.187-2.578 1.64-4.5 '
  '4.125-4.5 2.484 0 4.313 1.969 4.125 4.5Z" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" '
  'stroke-linejoin="round"/><path d="M3.017 20.747C3.783 16.5 7.922 14.25 12 14.25s8.217 2.25 8.984 6.497" '
  'stroke="currentColor" stroke-width="1.6" stroke-miterlimit="10"/></svg>')


def product_rail(section_id, heading, handles, extra_class='', reasons=None):
    """A titled rail of product cards, reusing product_card() so pricing, badges
    and review counts stay in step with the rest of the site."""
    cards = ''
    for h in handles:
        if h not in BY:
            raise SystemExit('!! product_rail: unknown handle ' + h)
        c = product_card(BY[h])
        if reasons and h in reasons:
            c = c.replace('</a><div class="price',
                          '</a><span class="recs__reason">' + reasons[h] + '</span><div class="price', 1)
        cards += c
    return ('<section class="sec ' + extra_class + '" id="' + section_id + '">'
            '<div class="wrap wrap--wide">'
            '<h2 class="h h2 sec__title">' + heading + '</h2>'
            '<div class="rail">' + cards + '</div>'
            '</div></section>')


# ---------------------------------------------------------------- cards
def review_badge(handle):
    """Star rating over the card image, bottom left. Omitted where the store
    has no reviews for the product rather than inventing one."""
    r = REV.get(handle)
    if not r:
        return ''
    return ('<span class="pc__rev"><span class="pc__star">&#9733;</span> ' + ('%.1f' % r['rating']) +
            ' <i>(' + str(r['count']) + ')</i></span>')


def add_button(p):
    """A sold-out product gets a disabled button that says so. Previously the
    card carried a "Sold out" badge over an active "Add to cart", which opened
    the variant modal for something nobody can buy."""
    if p['handle'] in SOLD_OUT:
        return ('<button class="btn pc__add" type="button" disabled '
                'aria-disabled="true">Sold out</button>')
    return ('<button class="btn pc__add" type="button" data-quick="' + p['handle'] +
            '">Add to cart</button>')


PDP_FILE = {
  'dna-42-clinicalift-serum': 'product.html',
  'jasmine-vital-cream': 'product-jasmine-vital-cream.html',
  'retinol-rescue-overnight-cream': 'product-retinol-rescue.html',
  'smooth-marine-cream': 'product-smoothing-marine-cream.html',
  'deep-moisture-mask': 'product-deep-moisture-mask.html',
}


def pdp_href(handle):
    """Products with their own page link to it; everything else to the serum."""
    return PDP_FILE.get(handle, 'product.html')


def product_card(p):
    badge = ''
    if p['handle'] in SOLD_OUT:
        badge = '<span class="badge">Sold out</span>'
    elif p['cmp']:
        badge = '<span class="badge">Save ' + str(round((1 - p['price'] / p['cmp']) * 100)) + '%</span>'
    if p['cmp']:
        price = ('<div class="price"><b>' + money(p['price']) +
                 '</b><s>' + money(p['cmp']) + '</s></div>')
    else:
        price = '<div class="price plain"><b>' + money(p['price']) + '</b></div>'
    title = H.escape(p['title'], quote=True)
    return (
      '<article class="pc" data-type="' + (p['type'] or 'Other') + '" data-price="' + str(p['price']) +
      '" data-title="' + title + '">'
      '<div class="pc__fig">' + badge +
      '<a href="' + pdp_href(p['handle']) + '" aria-label="' + title + '">'
      '<img src="' + p['imgs'][0] + '" alt="' + title + '" loading="lazy">'
      '<img class="sec" src="' + img_for(p, 1) + '" alt="" loading="lazy"></a>'
      + review_badge(p['handle']) +
      '</div>'
      '<div class="pc__info">'
      '<a class="pc__title" href="' + pdp_href(p['handle']) + '">' + p['title'] + '</a>'
      + price
      + add_button(p) +
      '</div></article>')

def category_from(types, extra):
    """Lowest live price across the products in a category."""
    prices = [p['price'] for p in P if p['type'] in types]
    prices += [BY[h]['price'] for h in extra if h in BY]
    return min(prices) if prices else None

def category_row():
    """Shop-by-category tiles, directly under the hero banner."""
    tiles = ''
    for label, h, types, extra in CATEGORIES:
        low = category_from(types, extra)
        tag = ('<span class="cat__from">From ' + money(low) + '</span>') if low else ''
        tiles += ('<a class="cat" href="collection.html">'
                  '<span class="cat__fig">'
                  '<img src="' + BY[h]['imgs'][0] + '" alt="' + H.unescape(label) + '" loading="lazy">'
                  + tag + '</span>'
                  '<p>' + label + '</p></a>')
    return ('<section class="sec sec--tight"><div class="wrap wrap--wide">'
            '<h2 class="h h2 sec__title" style="margin-bottom:30px">Shop by category</h2>'
            '<div class="cats">' + tiles + '</div></div></section>')


def press_band(cls):
    # Desktop: the three quotes sit in a static 3-up grid. Mobile: the same
    # markup becomes a continuous marquee, so the set is emitted twice and the
    # copy is aria-hidden; CSS hides it again above 1000px.
    item = ''.join('<div><blockquote>' + q + '</blockquote>'
                   '<img src="' + l + '" alt="" loading="lazy"></div>' for q, l in PRESS)
    dup = ''.join('<div aria-hidden="true"><blockquote>' + q + '</blockquote>'
                  '<img src="' + l + '" alt="" loading="lazy"></div>' for q, l in PRESS)
    return ('<section class="band ' + cls + '"><div class="wrap wrap--wide">'
            '<div class="press"><div class="press__track">' + item + dup +
            '</div></div></div></section>')

# ---------------------------------------------------------------- pages
def home():
    editors = ''.join(product_card(BY[h]) for h in EDITORS)
    ugc_src = [BY['smooth-marine-cream'], BY['deep-moisture-mask'], BY['jasmine-vital-cream'],
               BY['7-acid-daily-glow-peel'], BY['retinol-rescue-overnight-cream']]
    ugc = ''.join(
      '<div class="ugc__card"><img src="' + img_for(pr, min(2, len(pr['imgs']) - 1)) + '" alt="" loading="lazy">'
      '<span class="ugc__play">' + IC['play'] + '</span>'
      '<div class="ugc__tag"><img src="' + pr['imgs'][0] + '" alt="" loading="lazy">'
      '<p>' + pr['title'] + '<span>' + money(pr['price']) + '</span></p></div></div>' for pr in ugc_src)
    band = ('<section class="slider"><div class="slider__track">' +
            ''.join('<div><img src="' + u + '" alt="" loading="lazy"></div>' for u in BAND_1) +
            '</div><div class="dots"></div></section>')
    return (
      '<section class="bleed"><a href="collection.html">'
      '<img src="' + HERO + '" alt="The Sale Edit &ndash; 25% off select formulas" fetchpriority="high"></a>'
      '<span class="scrollcue">' + IC['arrowDown'] + '</span></section>'

      + category_row() +

      '<section class="sec sec--tight"><div class="wrap wrap--wide">'
      '<p class="intro">The first skincare brand built on regenerative coastal biotechnology, '
      'physician-formulated to make skin more resilient with every use.</p></div></section>'

      '<section class="sec" style="padding-top:0"><div class="wrap wrap--wide">'
      '<h2 class="h h2 sec__title">Editor&rsquo;s Favorites</h2>'
      '<div class="rail" id="edit-rail">' + editors + '</div>'
      '<div class="arrows"><button type="button" data-rail="#edit-rail" data-dir="-1" aria-label="Previous">'
      + IC['chevL'] + '</button>'
      '<button type="button" data-rail="#edit-rail" data-dir="1" aria-label="Next">' + IC['chevR'] +
      '</button></div></div></section>'

      + product_rail('bestsellers', 'Bestsellers', BESTSELLERS)
      + product_rail('new-arrivals', 'New Arrivals', NEW_ARRIVALS, 'sec--tight')

      + press_band('band--maroon') +

      '<section class="ovb"><img src="' + JASMINE + '" alt="" loading="lazy">'
      '<div class="ovb__t">'
      '<h2 class="h h1">Powered by Jasmine Catalyst Complex&trade;</h2>'
      '<p class="lede">A clinically advanced fusion where innovation meets intention&mdash;to unlock '
      'and reprogram your skin&rsquo;s healthiest glow.</p>'
      '<a class="btn btn--ghost" href="collection.html">Learn more</a></div></section>'

      '<section class="sec"><div class="wrap wrap--wide">'
      '<h2 class="h h2 sec__title">Real people, real results.</h2>'
      '<div class="ugc">' + ugc + '</div></div></section>'

      + band +

      '<section class="sec"><div class="wrap wrap--narrow">'
      '<div style="text-align:center;margin-bottom:28px">'
      '<p class="h h6 sub" style="margin:0 0 10px">Anti-Puff Eye Cream</p>'
      '<h2 class="h h2" style="margin:0">Doctor-Formulated 2mm Eyelid Lift</h2></div>'
      '<div class="ba" style="max-width:620px">'
      '<img src="' + HOME_BA_B + '" alt="Before">'
      '<div class="ba__after"><img src="' + HOME_BA_A + '" alt="After"></div>'
      '<div class="ba__handle"></div></div>'
      '<p style="text-align:center;margin:30px 0 0">'
      '<button class="btn" type="button" data-quick="anti-puff-eye-cream">Shop the eye cream</button></p>'
      '</div></section>'

      '<section class="ovb"><img src="' + SUB_IMG + '" alt="" loading="lazy">'
      '<div class="ovb__t"><p class="h h6">Subscription</p>'
      '<h2 class="h h1">Great skin, automatically</h2>'
      '<p class="lede">Subscribe to get your Clark&rsquo;s Botanicals essentials on your schedule&mdash;and '
      'lock in up to 20% off every order, plus free shipping for life. No commitment required.</p>'
      '<a class="btn" href="collection.html">Subscribe now</a></div></section>'

      + press_band('band--teal') +

      '<section class="split"><img src="' + STORY_IMG + '" alt="Francesco Clark" loading="lazy">'
      '<div class="split__t">'
      '<h2 class="h h1">Born from injury, built to outsmart inflammation.</h2>'
      '<p>After an injury left Francesco Clark unable to sweat, his skin reacted with eczema, rosacea, '
      'and severe inflammation. When traditional medicine fell short, Francesco teamed up with his father, '
      'a physician, to create Clark&rsquo;s Botanicals&mdash;a skincare line built to defy convention. '
      'Eighteen years later, the brand thrives precisely because it was never designed to fit in.</p>'
      '<a class="ulink" href="#">Read our story</a></div></section>')

def collection():
    cards = ''.join(product_card(BY[h]) for h in PLP_ORDER)
    types = sorted({(p['type'] or 'Other') for p in P})
    fopts = ''.join(
      '<label class="fopt"><input type="checkbox" data-filter value="' + t + '">' + t + '</label>'
      for t in types)
    sorts = [('manual','Featured'),('price-asc','Price, low to high'),('price-desc','Price, high to low'),
             ('az','Alphabetically, A-Z'),('za','Alphabetically, Z-A')]
    sopts = ''.join('<button type="button" class="sortopt ' + ('on' if v == 'manual' else '') +
                    '" data-sort="' + v + '">' + l + '</button>' for v, l in sorts)
    return (
      '<div class="ctool"><div class="ctool__in">'
      '<button type="button" data-open="#sorts">Sort by ' + IC['chevDown'] + '</button>'
      '<button type="button" data-open="#filters">Filter</button></div></div>'
      '<section class="sec" style="padding-top:clamp(30px,3.5vw,54px)"><div class="wrap wrap--wide">'
      '<div id="achips" class="achips"></div>'
      '<div class="grid" id="plist">' + cards + '</div>'
      '</div></section>'
      '<aside class="sheet" id="filters">'
      '<div class="panel__hd"><span class="h">Filters</span>'
      '<button data-close aria-label="Close">' + IC['close'] + '</button></div>'
      '<div class="panel__bd"><div class="fgroup"><p>Product type</p>' + fopts + '</div></div>'
      '<div class="panel__ft"><button class="cart__co" type="button" data-close>View results</button></div>'
      '</aside>'
      '<aside class="sheet" id="sorts">'
      '<div class="panel__hd"><span class="h">Sort by</span>'
      '<button data-close aria-label="Close">' + IC['close'] + '</button></div>'
      '<div class="panel__bd">' + sopts + '</div></aside>')

def product(handle='dna-42-clinicalift-serum'):
    p = BY[handle]
    imgs = p['imgs'][:8]
    thumbs = ''.join('<button type="button" data-i="' + str(i) + '" class="' + ('on' if i == 0 else '') + '"'
                     ' aria-label="Image ' + str(i + 1) + '">'
                     '<img src="' + u + '" alt="" loading="lazy"></button>' for i, u in enumerate(imgs))
    mains = ''.join('<img src="' + u + '" class="' + ('on' if i == 0 else '') + '" alt="' +
                    H.escape(p['title'], quote=True) + '"' + ('' if i == 0 else ' loading="lazy"') + '>'
                    for i, u in enumerate(imgs))

    def acc_block(titles, open_first=False):
        out = []
        for i, t in enumerate(titles):
            # The capture in cap/ keeps the store's raw "$5.00 USD" wording; the
            # site-wide rule is $ only, so strip the suffix at render time rather
            # than mutating the scrape.
            body = strip_usd(ACC.get(t, '<p></p>'))
            out.append('<details' + (' open' if (open_first and i == 0) else '') + '>'
                       '<summary>' + t + '<i>+</i></summary>'
                       '<div class="acc__c">' + body + '</div></details>')
        return ''.join(out)

    lede = LEDE.get(handle) or ('<b>' + p['title'] + '</b><br><br>' +
            H.escape(p['desc'][:420], quote=False) + '&hellip;')

    sub_price = round(p['price'] * (1 - SUB_DISCOUNT), 2)
    subs = (
      '<div class="subs">'
      '<label class="on"><input type="radio" name="purchase" checked data-price="' + str(p['price']) + '">'
      'One-time purchase<span class="sp">' + money(p['price']) + '</span></label>'
      '<label><input type="radio" name="purchase" data-price="' + str(sub_price) +
      '" data-sub="Delivery every 1 Month">Subscribe + Save ' + str(int(SUB_DISCOUNT * 100)) + '%<span class="sp">' + money(sub_price) + '</span></label>'
      '<span class="tiny">subscription details</span></div>')

    love = [('rabbit','Cruelty free'),('leaf','Clean ingredients'),('wheat','Gluten free'),
            ('vegan','Vegan'),('flagus','Made in USA')]
    love_html = ''.join('<div><span>' + IC[k] + '</span><p>' + t + '</p></div>' for k, t in love)

    related = ''.join(product_card(BY[h]) for h in RELATED)
    recent = ''.join(product_card(BY[h]) for h in RECENT)

    return (
      '<section class="sec sec--tight"><div class="wrap wrap--pdp"><div class="pdp">'
      '<div class="gal"><div class="gal__thumbs">' + thumbs + '</div>'
      '<div class="gal__main"><div class="gal__mrail">' + mains + '</div></div></div>'
      '<div class="pinfo">'
        '<div class="pinfo__top"><h1 class="h">' + p['title'] + '</h1>'
        '<span class="pinfo__price">' + money(p['price']) + '</span></div>'
        '<div class="rr"><span class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span>'
        '<span class="xxs sub">(6)</span></div>'
        + award_band(handle) +
        '<p class="afterpay">or 4 interest-free payments of <b>' + money(p['price'] / 4) + '</b> with '
        '<span class="chipdark">Afterpay</span></p>'
        '<p class="lede">' + lede + '</p>'
        '<div class="acc">' + acc_block(["Why Clark's Botanicals", 'Shipping and Returns']) + '</div>'
        '<div class="qtyrow"><span class="qty" data-pdp-qty>'
        '<button type="button" data-step="-1" aria-label="Decrease quantity">&minus;</button>'
        '<span>1</span><button type="button" data-step="1" aria-label="Increase quantity">+</button></span></div>'
        + subs +
        '<button class="btn btn--full" type="button" data-pdp-add="' + p['handle'] + '"'
        ' style="margin-top:16px">Add to cart</button>'
        + trust_strip() +
        pairs_rail(p) +
        '<div class="acc">' + (acc_block(['Description','How to Use','BENEFITS','CLINICALS',
                                         'VISIBLE PROGRESSION','KEY INGREDIENTS'])
                               if handle == 'dna-42-clinicalift-serum' else '') + '</div>'
        '<div style="margin-top:30px"><p class="h h6" style="margin:0">Don&rsquo;t just take our word for it.</p>'
        '<div class="vidcard"><div><img src="' + img_for(p, 2) + '" alt="" loading="lazy">'
        '<i><b>' + IC['play'] + '</b></i></div></div></div>'
      '</div></div></div></section>'

      + '<p class="vlbl">Layout A &mdash; current</p>' + clinical_band(handle) +
      '<p class="vlbl">Layout B &mdash; Augustinus Bader pattern</p>' + proven_band(handle) +

      (('<section class="sec" style="background:var(--soft)"><div class="wrap wrap--narrow">'
      '<div style="text-align:center;margin-bottom:26px">'
      '<h2 class="h h2" style="margin:0 0 8px">Before / After</h2>'
      '<p class="xxs sub" style="margin:0">Visible improvement of aging signs after 42 days</p></div>'
      '<div class="ba" style="max-width:900px"><img src="' + PDP_BA_B + '" alt="Before">'
      '<span class="ba__lbl" style="left:16px">Before</span>'
      '<div class="ba__after"><img src="' + PDP_BA_A + '" alt="After"></div>'
      '<span class="ba__lbl" style="right:16px">After</span>'
      '<div class="ba__handle"></div></div></div></section>')
      if handle == 'dna-42-clinicalift-serum' else '') +

      '<section class="split"><img src="' + AMALFI + '" alt="Amalfi Coast" loading="lazy">'
      '<div class="split__t"><h2 class="h h2">Amalfi Born Biotechnology&trade;</h2>'
      '<p>The Amalfi Coast is not just one of the world&rsquo;s most beautiful coastlines. It is one of its '
      'most demanding. Shaped by the Campanian volcanic arc, its soils are saturated with ancient mineral '
      'deposits: sulfur, potassium, magnesium, and trace elements forged under intense geological pressure.</p>'
      '<p>The species that thrive anyway are classified as extremophiles: organisms that have evolved not '
      'just to tolerate extreme conditions, but to flourish under them. Amalfi Born Biotechnology&trade; is '
      'our proprietary research platform for translating those cellular resilience mechanisms into '
      'measurable pathways for human skin.</p></div></section>'

      '<section class="sec"><div class="wrap wrap--wide">'
      '<h2 class="h h2 sec__title">Why you will love it</h2>'
      '<div class="wyl">' + love_html + '</div></div></section>'

      '<section class="sec" style="padding-top:0"><div class="wrap wrap--wide">'
      '<h2 class="h h2 sec__title">You may also like</h2>'
      '<div class="grid grid--4">' + related + '</div></div></section>'

      '<section class="sec" style="padding-top:0"><div class="wrap wrap--wide">'
      '<h2 class="h h2 sec__title">Recently viewed products</h2>'
      '<div class="grid grid--4">' + recent + '</div></div></section>'

      + sticky_bar(p)

      + recs_rail())


def recs_rail():
    """'Based on your past purchases' - hidden until body.is-signed-in is set.
    Real personalisation needs order history; this is the placement and the
    reason-copy pattern, wired to a demo toggle."""
    cards = ''
    for h, why in RECS:
        c = product_card(BY[h])
        c = c.replace('</a><div class="price',
                      '</a><span class="recs__reason">' + why + '</span><div class="price', 1)
        cards += c
    return ('<section class="sec recs" id="recs"><div class="wrap wrap--wide">'
            '<div class="recs__head">'
            '<h2 class="h h2" style="margin:0">Picked up where you left off</h2>'
            '<span class="recs__why">Based on your past purchases</span></div>'
            '<div class="rail">' + cards + '</div></div></section>')


def sticky_bar(p):
    """Slim sticky bar shown once the main Add to cart leaves the viewport.
    Both buttons open the sticky panel."""
    first = ' &middot; '.join(o['values'][0] for o in p['opts']) if p['opts'] else ''
    return (
      '<div class="satcbar" data-satcbar data-handle="' + p['handle'] + '">'
      '<div class="satcbar__in">'
        '<img class="satcbar__img" src="' + p['imgs'][0] + '" alt="" loading="lazy">'
        '<div class="satcbar__t"><p>' + p['title'] + '</p>'
        '<span data-satcbar-opt>' + first + '</span></div>'
        '<span class="satcbar__price" data-satcbar-price>' + money(p['price']) + '</span>'
        '<div class="satcbar__act">'
          '<button class="btn" type="button" data-satcbar-open="cart">Add to cart</button>'
          '<button class="btn btn--ghost" type="button" data-satcbar-open="buy">Buy now</button>'
        '</div>'
      '</div></div>')


# Lede copy per PDP. Only approved wording from the claims package: appearance
# language, no "reverses aging", no "only"/"first"/"#1" without a dated basis.
LEDE = {
 'dna-42-clinicalift-serum': (
   'In 42 days, skin appears up to 8 years younger.<br><br>'
   'A serum powered by vegan dual PDRN regenerative science and plant-derived exosome delivery '
   'technology, engineered to visibly lift, redensify and restore skin by activating cellular '
   'renewal at its source.<br><br>'
   'Not slowing how skin ages. Visibly turning back how it looks.<br><br>'
   '42 days. Proven. Measured.'),

 'jasmine-vital-cream': (
   'Nearly a third fewer visible lines and wrinkles in 28 days, measured on the finished '
   'formula.<br><br>'
   'Our most-repurchased moisturizer, clinically tested non-irritating and non-sensitizing on a '
   '50-subject patch test.<br><br>'
   'The fullest clinical record in the line.'),

 'retinol-rescue-overnight-cream': (
   'Retinol results without the retinol reaction.<br><br>'
   'A time-release retinol and encapsulated vitamin C delivery system, so renewal disperses '
   'through the night instead of arriving in one surge. Niacinamide, colloidal oatmeal and arnica '
   'are formulated to calm the look of redness.<br><br>'
   'Six weeks of clinical use. Zero adverse effects.'),

 'smooth-marine-cream': (
   '95% saw more hydrated skin in four weeks.<br><br>'
   'A marine-derived moisturizer with glycolic acid and algae, formulated to smooth and soften '
   'the look of skin while it hydrates.'),

 'deep-moisture-mask': (
   '91% saw smoother, softer and more moisturized skin after one use.<br><br>'
   'An intensive treatment mask built for an immediate, visible change in how skin looks '
   'and feels.'),
}


# ---------------------------------------------------------------- clinical results
# Figures come from the PDP Efficacy and Claims Package (Clark's Botanicals for
# Growisto, Sept 25 2026) and nowhere else. Tier A = clinical on the finished
# Clark's formula, B = clinical on a key active, C = laboratory, D = consumer
# survey. The band is deliberately almost wordless: a timeframe, the number, and
# three or four words. Everything that qualifies a number lives in the footnotes.

# handle -> {awards, groups: [(timeframe, [(value, label, note_idx)])], notes}
CLINICAL = {

 'dna-42-clinicalift-serum': {
   'awards': [('Harper&rsquo;s Bazaar', 'Best New Serum 2026'),
              ('Allure', 'Best for Sensitive Skin 2026')],
   'groups': [
     ('In 42 days', [('8', 'years younger', ''),
                     ('15.3', 'less wrinkle depth', '%')]),
     ('In 56 days', [('11', 'less wrinkle depth vs placebo', '%'),
                     ('+6', 'more skin density', '%')]),
   ],
   'notes': [
     'Randomized, placebo-controlled study of the serum&rsquo;s key regenerative active at 2%, '
     'women aged 52&ndash;65, twice daily, 42 days. Primos 3D wrinkle analysis; 8.2 years at day 42 '
     'against a reference dataset of 300+ women. Results are for the active, not the finished formula.',
     'PhytoCellTec&trade; Exosomes at 0.4%, half-face versus placebo, 23 women aged 41&ndash;69, '
     'twice daily, 56 days, PRIMOS lite. Density by ultrasound, 28 days. Results are for the '
     'active, not the finished formula.',
   ],
 },

 'jasmine-vital-cream': {
   'awards': [('Allure', 'Editors&rsquo; Favorites'),
              ('Harper&rsquo;s Bazaar', 'March 2020')],
   'groups': [
     ('In 28 days', [('32', 'fewer visible wrinkles', '%'),
                     ('73', 'best individual result', '%')]),
     ('Tolerability', [('50', 'subjects patch tested', ''),
                       ('None', 'adverse reactions recorded', '')]),
   ],
   'notes': [
     'Instrumental clinical on the finished formula. n=32 women aged 46&ndash;65, twice daily on '
     'face and neck after a 7-day washout, Visioscan SEw parameter, 32.45% mean reduction, p&lt;0.05, '
     'maximum individual reduction 72.94%. Advanced Science Laboratories, Jan 31 2022.',
     'Repeat insult patch test, open patch, 71 enrolled and 56 completed, ages 20&ndash;76, no '
     'adverse reactions. Report signed by the laboratory&rsquo;s clinical director, M.D., Feb 23 2022.',
   ],
 },

 'retinol-rescue-overnight-cream': {
   'awards': [('O, The Oprah Magazine', 'Fall Beauty O-Ward 2017')],
   'groups': [
     ('Clinical tolerability', [('None', 'adverse effects or unexpected reactions, '
                                 'across 6 weeks of use', ''),
                                ('26', 'panelists monitored', '')]),
     ('Reviews', [('4.9', 'average rating', ''),
                  ('184', 'customer reviews', '')]),
   ],
   'notes': [
     'Clinical tolerability record. AMA Laboratories, Lot Q107, 26 panelists, Chromameter readings '
     'at weeks 2 and 6, July 17 2017. Retinol results without the retinol reaction.',
     'Verified customer reviews on clarksbotanicals.com, the deepest review base in the line.',
   ],
 },

 'smooth-marine-cream': {
   'awards': [('WWD', 'Top 100 Anti-Aging Moisturizers of All Time'),
              ('Allure', 'Best of Beauty')],
   'groups': [
     ('In 4 weeks', [('95', 'saw more hydrated skin', '%')]),
     ('Reviews', [('4.8', 'average rating', ''),
                  ('258', 'customer reviews', '')]),
   ],
   'notes': [
     'Consumer perception survey, n=23, 4 weeks, 2018. Self-reported.',
     'Verified customer reviews on clarksbotanicals.com.',
   ],
 },

 'deep-moisture-mask': {
   'awards': [('Allure', 'Best of Beauty'),
              ('WWD', 'Beauty Inc. Icons 2023')],
   'groups': [
     ('After one use', [('91', 'smoother, softer, more moisturized', '%')]),
     ('Reviews', [('4.8', 'average rating', ''),
                  ('133', 'customer reviews', '')]),
   ],
   'notes': [
     'Consumer perception survey, n=22, after a single use. Self-reported.',
     'Verified customer reviews on clarksbotanicals.com.',
   ],
 },
}

# Which tier each group is, for the one-line qualifier under the band
TIER_NOTE = {
  'dna-42-clinicalift-serum':
    'Clinical studies of the serum&rsquo;s key actives, not the finished formula.',
  'jasmine-vital-cream':
    'Instrumental clinical study on the finished Jasmine Vital Cream formula.',
  'retinol-rescue-overnight-cream':
    'Clinical tolerability study on the finished formula.',
  'smooth-marine-cream':
    'Consumer perception survey. Self-reported results.',
  'deep-moisture-mask':
    'Consumer perception survey. Self-reported results.',
}

# Index into the product's own gallery for the band's full-bleed image. Picked
# for texture and skin, not packshot: the number needs something to sit against.
BAND_IMG = {
  'dna-42-clinicalift-serum': 1,      # serum droplet on stone
  'jasmine-vital-cream': 6,           # lifestyle alt
  'retinol-rescue-overnight-cream': 5,
  'smooth-marine-cream': 3,
  'deep-moisture-mask': 0,
}

RETAILERS = ['Bluemercury', 'Credo', 'Saks Fifth Avenue', 'Goop']


def award_band(handle):
    """Reusable award band, above the fold on every PDP that has one."""
    aw = (CLINICAL.get(handle) or {}).get('awards') or []
    if not aw:
        return ''
    return ('<div class="awb">' +
            ''.join('<div class="awb__i"><b>' + n + '</b><span>' + d + '</span></div>'
                    for n, d in aw) + '</div>')


# ---------------------------------------------------------------- variant B
# Augustinus Bader "Proven Results" pattern: a dark full-bleed band, three
# headline figures, an evidence-type toggle, and a drawer holding every approved
# figure. The toggle maps onto the package's tiers - a clinical result and a
# laboratory result must never read as the same kind of proof - and a tab only
# appears when that evidence type actually has figures for the product.
#
# set key -> (tab label, [(value, caption)], footnote, [every approved line])
PROVEN = {

 'dna-42-clinicalift-serum': [
   ('clinical', 'Clinical trials',
    [('8', 'Years younger in 42 days', ''),
     ('15.3', 'Less wrinkle depth in 42 days', '%'),
     ('11', 'Less wrinkle depth vs placebo in 56 days', '%')],
    'Based on randomized, placebo-controlled clinical studies of the serum&rsquo;s key '
    'actives. Results are for the actives, not the finished formula.',
    ['Skin appears up to 8 years younger at day 42, and 4.9 years at day 28',
     'Wrinkle depth reduced 15.3% at day 42, and 9.2% at day 28, significantly ahead of placebo',
     'A measurable lifting effect at the jawline, vertical facial reference lines reduced vs placebo',
     'Smoother texture and reduced age-spot area and contrast at day 42',
     'Visible reduction of crow&rsquo;s feet, nasolabial folds and marionette lines at day 42',
     'Wrinkle depth reduced 11% versus placebo in 56 days with the plant exosome active',
     'Skin density up 6%, and a 6% improvement in the V-shape of the face, in 28 days']),
   ('lab', 'Laboratory',
    [('+266', 'Regeneration vs salmon-derived PDRN', '%'),
     ('+111', 'NAMPT expression, the enzyme that recycles NAD+', '%'),
     ('+161', 'FGF7 growth-factor expression', '%')],
    'In vitro and ex vivo laboratory testing. Laboratory data is not a clinical result.',
    ['+266% regeneration versus salmon-derived PDRN in a wound-healing assay',
     '+105% wrinkle-improvement efficacy and +95% moisturizing efficacy versus salmon-derived PDRN',
     '+111% NAMPT expression, the enzyme that recycles NAD+, in human dermal fibroblasts',
     'Higher ATP in aged skin models, and mitochondrial protection under UVA',
     'Higher collagen density and Collagen XVII in UV-damaged skin explants',
     '+161% FGF7 and +108% EGF growth-factor expression, and +64% SOD3 antioxidant defense']),
 ],

 'jasmine-vital-cream': [
   ('clinical', 'Clinical trial',
    [('32', 'Fewer visible wrinkles in 28 days', '%'),
     ('73', 'Best individual reduction recorded', '%'),
     ('50', 'Subject patch test, no adverse reactions', '')],
    'Based on a 28-day instrumental clinical study of 32 women, measured on the finished '
    'Jasmine Vital Cream formula.',
    ['Nearly a third fewer visible lines and wrinkles in 28 days, a 32.45% mean reduction, p&lt;0.05',
     'Individual results up to 72.94% reduction',
     'Measured by Visioscan SEw on women aged 46&ndash;65, twice daily on face and neck',
     'Clinically tested non-irritating and non-sensitizing on a 50-subject repeat insult patch test',
     'No adverse reactions across 56 completed subjects, ages 20&ndash;76']),
 ],

 'retinol-rescue-overnight-cream': [
   ('clinical', 'Clinical trial',
    [('None', 'Adverse effects across 6 weeks', ''),
     ('26', 'Panelists monitored', ''),
     ('6', 'Weeks of clinical use', '')],
    'Based on a 6-week clinical tolerability study of 26 panelists on the finished formula.',
    ['Zero adverse effects or unexpected reactions across 6 weeks of clinical use',
     'Chromameter readings taken at weeks 2 and 6',
     'Retinol results without the retinol reaction',
     'Niacinamide, colloidal oatmeal and arnica, formulated to calm the look of redness',
     'Time-release retinol with encapsulated vitamin C, so renewal disperses through the night']),
 ],

 'smooth-marine-cream': [
   ('user', 'User results',
    [('95', 'Saw more hydrated skin in 4 weeks', '%'),
     ('4.8', 'Average customer rating', ''),
     ('258', 'Customer reviews', '')],
    'Based on a 4-week consumer perception study of 23 participants. Self-reported.',
    ['95% saw more hydrated skin in 4 weeks',
     '4.8 average rating across 258 verified customer reviews',
     'WWD Top 100 Anti-Aging Moisturizers of All Time',
     'Allure Best of Beauty']),
 ],

 'deep-moisture-mask': [
   ('user', 'User results',
    [('91', 'Smoother, softer, more moisturized after one use', '%'),
     ('4.8', 'Average customer rating', ''),
     ('133', 'Customer reviews', '')],
    'Based on a consumer perception study of 22 participants after a single use. Self-reported.',
    ['91% saw smoother, softer, more supple and more moisturized skin after one use',
     '4.8 average rating across 133 verified customer reviews',
     'Allure Best of Beauty',
     'WWD Beauty Inc. Icons 2023']),
 ],
}


def proven_band(handle):
    """Variant B. Dark band, three headline figures, evidence-type toggle, and a
    drawer with every approved figure for that product."""
    sets = PROVEN.get(handle)
    if not sets:
        return ''
    p = BY[handle]
    idx = BAND_IMG.get(handle, 0)
    img = p['imgs'][idx] if idx < len(p['imgs']) else p['imgs'][0]

    tabs, panels, dtabs, dpanels = '', '', '', ''
    for i, (key, label, stats, note, every) in enumerate(sets):
        on = ' on' if i == 0 else ''
        tabs += ('<button type="button" class="pr__tab' + on + '" data-pr-tab="' + key +
                 '">' + label + '</button>')
        figs = ''
        for value, cap, unit in stats:
            word = not value.replace('.', '').replace('+', '').isdigit()
            u = ('<span class="pr__u">' + unit + '</span>') if unit else ''
            figs += ('<div class="pr__s"><p class="pr__n' + (' pr__n--word' if word else '') +
                     '">' + value + u + '</p>'
                     '<p class="pr__c">' + cap + '</p></div>')
        panels += ('<div class="pr__panel' + on + '" data-pr-panel="' + key + '">'
                   '<div class="pr__g">' + figs + '</div>'
                   '<p class="pr__fn">' + note + '</p></div>')
        dtabs += ('<button type="button" class="prd__tab' + on + '" data-pr-dtab="' + key +
                  '">' + label + '</button>')
        dpanels += ('<div class="prd__panel' + on + '" data-pr-dpanel="' + key + '">'
                    '<ul>' + ''.join('<li>' + x + '</li>' for x in every) + '</ul>'
                    '<p class="prd__fn">' + note + '</p></div>')

    multi = ' pr--multi' if len(sets) > 1 else ''
    return (
      '<section class="pr' + multi + '" id="results-b">'
        '<div class="pr__bg"><img src="' + img + '" alt="" loading="lazy"></div>'
        '<div class="pr__in">'
          '<div class="pr__hd"><h2 class="pr__title">Proven results</h2>'
          '<div class="pr__tabs">' + tabs + '</div></div>'
          + panels +
          '<div class="pr__act">'
          '<button class="pr__all" type="button" data-pr-open>See all results</button></div>'
        '</div>'
      '</section>'
        '<aside class="prd" data-pr-drawer aria-label="Clinical and user results">'
          '<div class="prd__hd"><p>Clinical &amp; user results</p>'
          '<button type="button" data-pr-close aria-label="Close">'
          '<svg width="15" height="15" fill="none" viewBox="0 0 16 16">'
          '<path d="m1 1 14 14M1 15 15 1" stroke="currentColor" stroke-width="1.6"/>'
          '</svg></button></div>'
          '<div class="prd__tabs">' + dtabs + '</div>'
          '<div class="prd__bd">' + dpanels + '</div>'
        '</aside>')


def clinical_band(handle):
    """Numbers-first results band, set against the product's own imagery so the
    figures have something to land on. One timeframe per block, the figure large,
    the qualifying detail in the footnotes."""
    c = CLINICAL.get(handle)
    if not c:
        return ''
    p = BY[handle]
    idx = BAND_IMG.get(handle, 0)
    img = p['imgs'][idx] if idx < len(p['imgs']) else p['imgs'][0]

    blocks = ''
    for label, stats in c['groups']:
        items = ''
        for value, cap, unit in stats:
            u = ('<span class="cb__u">' + unit + '</span>') if unit else ''
            # A bare "0" reads as missing data rather than a clean safety record,
            # so word values are set as words and marked as a result.
            word = not value.replace('.', '').replace('+', '').isdigit()
            cls = ' cb__n--word' if word else ''
            items += ('<div class="cb__s' + (' cb__s--word' if word else '') + '">'
                      '<p class="cb__n' + cls + '">' + value + u + '</p>'
                      '<p class="cb__c">' + cap + '</p></div>')
        blocks += ('<div class="cb__col"><p class="cb__t">' + label + '</p>'
                   '<div class="cb__ss">' + items + '</div></div>')

    # Footnote markers on the figures made them look annotated rather than
    # confident, so each note names the block it belongs to instead.
    labels = [g[0] for g in c['groups']]
    notes = ''.join('<li><b>' + (labels[i] if i < len(labels) else '') + '.</b> ' + n + '</li>'
                    for i, n in enumerate(c['notes']))

    return ('<section class="cb" id="results">'
            '<div class="cb__media"><img src="' + img + '" alt="' +
            H.escape(p['title'], quote=True) + '" loading="lazy"></div>'
            '<div class="cb__body">'
              '<p class="cb__hd">Clinical results</p>'
              '<div class="cb__g">' + blocks + '</div>'
              '<p class="cb__tier">' + TIER_NOTE.get(handle, '') + '</p>'
              '<ol class="cb__fn">' + notes + '</ol>'
            '</div></section>')


def trust_strip():
    """Repurchase rate, guarantee, certification, stockists."""
    return (
      '<div class="tst">'
        '<div class="tst__r"><b>76%</b><span>repurchase rate</span></div>'
        '<div class="tst__r"><b>60-day</b><span>money-back guarantee</span></div>'
        '<div class="tst__r"><b>Leaping Bunny</b><span>certified cruelty free</span></div>'
      '</div>'
      '<p class="avail">Available at ' +
      ' &middot; '.join('<b>' + r + '</b>' for r in RETAILERS) + '</p>')


def pairs_rail(p):
    """'Pairs well with' — routine add-ons directly under the PDP Add to cart.
    Products with options open the shared variant panel; single-variant products
    drop straight into the cart."""
    items = ''
    for h in PAIRS:
        if h == p['handle'] or h not in BY:
            continue
        q = BY[h]
        title = H.escape(q['title'], quote=True)
        if h in SOLD_OUT:
            act = '<button class="pw__add" type="button" disabled>Sold out</button>'
        elif q['opts']:
            act = ('<button class="pw__add" type="button" data-quick="' + h + '">'
                   'Add to cart</button>')
        else:
            act = ('<button class="pw__add" type="button" data-add="' + h + '">'
                   'Add to cart</button>')
        # always rendered, so buttons across the rail share one baseline
        note = ('<span class="pw__opt">' +
                (' &middot; '.join(o['name'] for o in q['opts']) if q['opts'] else '&nbsp;') +
                '</span>')
        items += ('<article class="pw" data-handle="' + h + '">'
                  '<a class="pw__fig" href="' + pdp_href(h) + '" aria-label="' + title + '">'
                  '<img src="' + q['imgs'][0] + '" alt="' + title + '" loading="lazy"></a>'
                  '<a class="pw__title" href="' + pdp_href(h) + '">' + q['title'] + '</a>'
                  '<span class="pw__price">' + money(q['price']) + '</span>'
                  + note + act + '</article>')
    return ('<section class="pw-wrap">'
            '<div class="pw-hd"><h2 class="h h6">Pairs well with</h2>'
            '<div class="pw-arr">'
            '<button type="button" data-rail="#pairs-rail" data-dir="-1" aria-label="Previous">'
            + IC['chevL'] + '</button>'
            '<button type="button" data-rail="#pairs-rail" data-dir="1" aria-label="Next">'
            + IC['chevR'] + '</button></div></div>'
            '<div class="pw-rail rail" id="pairs-rail">' + items + '</div></section>')


def variant_panel():
    """Shared variant-selection panel. Contents are rendered by JS for whichever
    product was clicked, so every card and the PDP sticky bar reuse one modal."""
    return ('<aside class="satc" id="vpanel" data-freeship="' + str(FREE_SHIP) +
            '" data-suboff="' + str(SUB_DISCOUNT) + '" data-subword="' +
            str(int(SUB_DISCOUNT * 100)) + '" aria-label="Choose options"></aside>')


def hub():
    cards = [('home.html', 'Home', 'Hero, Editor&rsquo;s Favorites, press bands, Real People rail, before/after'),
             ('collection.html', 'Collection (PLP)', 'Sticky Sort/Filter toolbar, 16 products, filter chips'),
             ('product.html', 'Product (PDP)', 'Gallery, subscribe + save, accordions, before/after, Amalfi')]
    grid = ''.join('<a class="hub__card" href="' + u + '"><p>' + t + '</p><span>' + d + '</span></a>'
                   for u, t, d in cards)
    return (
      '<!doctype html><html lang="en"><head><meta charset="utf-8">'
      '<meta name="viewport" content="width=device-width,initial-scale=1">'
      '<title>Clark&rsquo;s Botanicals &ndash; Mockup</title>'
      '<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap" rel="stylesheet">'
      '<style>' + CSS + '</style></head><body class="locked">' + gate() +
      '<div class="site"><div class="hub"><div class="hub__in">'
      '<img src="' + LOGO + '" alt="Clark&rsquo;s Botanicals">'
      '<p class="h h6 sub" style="margin:0">Interactive mockup &middot; Growisto</p>'
      '<div class="hub__grid">' + grid + '</div>'
      '<p class="hub__note">Header, mega menus, mobile drawer, predictive search, mini-cart and footer '
      'are shared across every page. Content and imagery replicated from the live site.</p>'
      '</div></div></div>'
      '<script>' + JS.replace('__PW__', PASSWORD) + '</script></body></html>')

# ---------------------------------------------------------------- localiser
def sniff_ext(path):
    """Real image type from the file's magic bytes, or None if unrecognised."""
    with open(path, 'rb') as fh:
        head = fh.read(16)
    if head[:3] == b'\xff\xd8\xff':                       return 'jpg'
    if head[:8] == b'\x89PNG\r\n\x1a\n':                 return 'png'
    if head[:6] in (b'GIF87a', b'GIF89a'):                 return 'gif'
    if head[:4] == b'RIFF' and head[8:12] == b'WEBP':      return 'webp'
    if head[4:8] == b'ftyp':                               return 'mp4'
    t = head.lstrip()[:5].lower()
    if t.startswith(b'<svg') or t.startswith(b'<?xml'):    return 'svg'
    return None


def localise():
    os.makedirs(ASSETS, exist_ok=True)
    cache = {}
    pat = re.compile(r'https://[^\s"\')]+?\.(?:jpg|jpeg|png|webp|gif|mp4|svg)(?:\?[^\s"\')]*)?(?=["\')\s]|$)')
    files = [f for f in os.listdir(OUT) if f.endswith('.html')]
    urls = set()
    for f in files:
        urls |= set(pat.findall(open(os.path.join(OUT, f), encoding='utf-8').read()))
    urls = {u for u in urls if 'fonts.g' not in u}
    print('localising %d assets' % len(urls))
    ok = 0
    for u in sorted(urls):
        ext = re.search(r'\.(jpg|jpeg|png|webp|gif|mp4|svg)', u).group(1)
        stem = hashlib.md5(u.encode()).hexdigest()
        for cand in (stem + '.jpg', stem + '.png', stem + '.' + ext):
            if os.path.exists(os.path.join(ASSETS, cand)):
                cache[u] = 'assets/' + cand
                break
        if u in cache:
            ok += 1
            continue
        dest = os.path.join(ASSETS, stem + '.' + ext)
        try:
            req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=60) as r, open(dest, 'wb') as fh:
                shutil.copyfileobj(r, fh)
        except Exception as e:
            print('  FAIL', u[:90], e)
            continue
        # The URL path extension can lie: Shopify serves .svg?format=jpg as JPEG.
        # Trust the bytes, or the file is served with the wrong MIME type and
        # the browser refuses to render it.
        real = sniff_ext(dest)
        if real and real != ext:
            fixed = os.path.join(ASSETS, stem + '.' + real)
            os.replace(dest, fixed)
            print('  ext %s -> %s for %s' % (ext, real, u[:70]))
            ext, dest = real, fixed
        cache[u] = 'assets/' + stem + '.' + ext
        ok += 1
    for f in files:
        pth = os.path.join(OUT, f)
        s = open(pth, encoding='utf-8').read()
        for u, local in cache.items():
            s = s.replace(u, local)
        open(pth, 'w', encoding='utf-8').write(s)
    print('localised %d/%d' % (ok, len(urls)))

def write_page(name, html):
    # Trailing newline so the output matches what editors and GitHub produce;
    # without it every hand-touched copy shows a spurious end-of-file diff.
    with open(os.path.join(OUT, name), 'w', encoding='utf-8') as fh:
        fh.write(html.rstrip('\n') + '\n')

def main():
    os.makedirs(OUT, exist_ok=True)
    write_page('index.html', hub())
    write_page('home.html', page('Clark&rsquo;s Botanicals', home()))
    write_page('collection.html', page('Best Sellers &ndash; Clark&rsquo;s Botanicals', collection()))
    for h, fname in PDP_FILE.items():
        write_page(fname, page(H.unescape(BY[h]['title']) + ' &ndash; Clark&rsquo;s Botanicals',
                               product(h)))
    print('pages written to', OUT)
    if '--no-assets' not in sys.argv:
        localise()

if __name__ == '__main__':
    main()
