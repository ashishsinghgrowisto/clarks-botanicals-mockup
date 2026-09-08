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

PLP_ORDER = ['dna-42-clinicalift-serum','retinol-rescue-overnight-cream','deep-moisture-mask',
             'smooth-marine-cream','jasmine-vital-cream','anti-puff-eye-cream',
             '7-acid-daily-glow-peel','pdrn-retinol-liquid-facelift-duo','power-couple',
             '24-hour-hormone-calm-ritual','the-glow-edit-set','regeneration-24-7-180-value',
             '3-minute-reset','travel-lip-duo','the-longevity-lift-duo','the-renewal-ritual']
SOLD_OUT = {'anti-puff-eye-cream'}
EDITORS = ['dna-42-clinicalift-serum','retinol-rescue-overnight-cream','deep-moisture-mask','smooth-marine-cream']
RELATED = ['3-minute-reset','retinol-rescue-overnight-cream','regeneration-24-7-180-value','deep-moisture-mask']
RECENT  = ['smooth-marine-cream','retinol-rescue-overnight-cream','jasmine-vital-cream','7-acid-daily-glow-peel']

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

def money(v):
    return '${:,.2f}'.format(v)

def img_for(p, i=0):
    return p['imgs'][i] if len(p['imgs']) > i else p['imgs'][0]

def has_from(p):
    return sum(len(o['values']) for o in p['opts']) > 1 if p['opts'] else False

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
    return '<div class="ann">' + ANNOUNCE + '</div>'

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

def variant_modal():
    return (
      '<div class="modal" id="vmodal"><div class="modal__bg"></div>'
      '<div class="modal__card"><button class="modal__close" aria-label="Close">' + IC['close'] + '</button>'
      '<div class="modal__img"><img alt=""></div>'
      '<div class="modal__body"></div></div></div>')

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
       'img': p['imgs'][0], 'opts': p['opts'], 'rev': 6} for p in P])
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
      + mobile_drawer() + search_panel() + cart_drawer() + variant_modal() +
      '<div class="ov"></div>'
      '<script>window.CB_PRODUCTS=' + products_js + ';</script>'
      '<script>' + JS.replace('__PW__', PASSWORD) + '</script>'
      '</body></html>')

# ---------------------------------------------------------------- cards
def product_card(p):
    badge = ''
    if p['handle'] in SOLD_OUT:
        badge = '<span class="badge">Sold out</span>'
    elif p['cmp']:
        badge = '<span class="badge">Save ' + str(round((1 - p['price'] / p['cmp']) * 100)) + '%</span>'
    if p['cmp']:
        price = ('<div class="price"><b>' + ('From ' if has_from(p) else '') + money(p['price']) +
                 ' USD</b><s>' + money(p['cmp']) + ' USD</s></div>')
    else:
        price = '<div class="price plain"><b>' + money(p['price']) + ' USD</b></div>'
    title = H.escape(p['title'], quote=True)
    return (
      '<article class="pc" data-type="' + (p['type'] or 'Other') + '" data-price="' + str(p['price']) +
      '" data-title="' + title + '">'
      '<div class="pc__fig">' + badge +
      '<a href="product.html" aria-label="' + title + '">'
      '<img src="' + p['imgs'][0] + '" alt="' + title + '" loading="lazy">'
      '<img class="sec" src="' + img_for(p, 1) + '" alt="" loading="lazy"></a>'
      '<button class="btn btn--ghost pc__quick" type="button" data-quick="' + p['handle'] + '">Quick add</button>'
      '</div>'
      '<div class="pc__info">'
      '<a class="pc__title" href="product.html">' + p['title'] + '</a>'
      + price + '</div></article>')

def press_band(cls):
    inner = ''.join('<div><blockquote>' + q + '</blockquote>'
                    '<img src="' + l + '" alt="" loading="lazy"></div>' for q, l in PRESS)
    return ('<section class="band ' + cls + '"><div class="wrap wrap--wide">'
            '<div class="press">' + inner + '</div></div></section>')

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

def product():
    p = BY['dna-42-clinicalift-serum']
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
            body = ACC.get(t, '<p></p>')
            out.append('<details' + (' open' if (open_first and i == 0) else '') + '>'
                       '<summary>' + t + '<i>+</i></summary>'
                       '<div class="acc__c">' + body + '</div></details>')
        return ''.join(out)

    lede = ('In 42 days, skin appears up to 8 years younger, without irritation.<br><br>'
            'The first serum powered by Vegan dual PDRN regenerative science and plant-derived exosome '
            'delivery technology, clinically engineered to visibly lift, redensify, and restore skin by '
            'activating cellular renewal at its source.<br><br>'
            'Not slowing the aging process. Biologically reversing it.<br><br>'
            'Designed around your skin&rsquo;s natural 42-day turnover cycle, this formula allows collagen '
            'stimulation, cellular repair, and visible structural renewal to unfold completely and without '
            'irritation. The result is skin that looks smoother, firmer, and luminous because its own '
            'vitality has been rebuilt.<br><br>'
            '42 days. Proven. Measured.')

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
        '<span class="pinfo__price">' + money(p['price']) + ' USD</span></div>'
        '<div class="rr"><span class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span>'
        '<span class="xxs sub">(6)</span></div>'
        '<p class="afterpay">or 4 interest-free payments of <b>' + money(p['price'] / 4) + '</b> with '
        '<span class="chipdark">Afterpay</span></p>'
        '<p class="lede">' + lede + '</p>'
        '<div class="acc">' + acc_block(["Why Clark's Botanicals", 'Shipping and Returns']) + '</div>'
        '<div class="qtyrow"><span class="qty" data-pdp-qty>'
        '<button type="button" data-step="-1" aria-label="Decrease quantity">&minus;</button>'
        '<span>1</span><button type="button" data-step="1" aria-label="Increase quantity">+</button></span></div>'
        + subs +
        '<button class="btn btn--full" type="button" data-pdp-add="' + p['handle'] + '"'
        ' style="margin-top:20px">Add to cart</button>'
        '<div class="acc">' + acc_block(['Description','How to Use','BENEFITS','CLINICALS',
                                         'VISIBLE PROGRESSION','KEY INGREDIENTS']) + '</div>'
        '<div style="margin-top:30px"><p class="h h6" style="margin:0">Don&rsquo;t just take our word for it.</p>'
        '<div class="vidcard"><div><img src="' + img_for(p, 2) + '" alt="" loading="lazy">'
        '<i><b>' + IC['play'] + '</b></i></div></div></div>'
      '</div></div></div></section>'

      '<section class="sec" style="background:var(--soft)"><div class="wrap wrap--narrow">'
      '<div style="text-align:center;margin-bottom:26px">'
      '<h2 class="h h2" style="margin:0 0 8px">Before / After</h2>'
      '<p class="xxs sub" style="margin:0">Visible improvement of aging signs after 42 days</p></div>'
      '<div class="ba" style="max-width:900px"><img src="' + PDP_BA_B + '" alt="Before">'
      '<span class="ba__lbl" style="left:16px">Before</span>'
      '<div class="ba__after"><img src="' + PDP_BA_A + '" alt="After"></div>'
      '<span class="ba__lbl" style="right:16px">After</span>'
      '<div class="ba__handle"></div></div></div></section>'

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

      + sticky_bar(p) + sticky_atc(p))

def sticky_bar(p):
    """Slim sticky bar shown once the main Add to cart leaves the viewport.
    Both buttons open the sticky panel."""
    first = ' &middot; '.join(o['values'][0] for o in p['opts']) if p['opts'] else ''
    return (
      '<div class="satcbar" data-satcbar>'
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


def sticky_atc(p):
    """Sticky add-to-cart panel: appears once the main Add to cart scrolls out of view."""
    groups = ''
    for o in p['opts']:
        btns = ''.join(
          '<button type="button" data-satc-opt="' + o['name'] + '" data-satc-val="' + v + '"'
          + (' class="on"' if i == 0 else '') + '>' + v + '</button>'
          for i, v in enumerate(o['values']))
        groups += ('<div class="satc__grp"><p class="satc__lbl"><b>' + o['name'] + '</b>'
                   '<span data-satc-selname="' + o['name'] + '"></span></p>'
                   '<div class="satc__opts">' + btns + '</div></div>')
    freqs = ['1 week', '2 weeks', '1 month', '2 months', '3 months']
    opts = ''.join('<option' + (' selected' if f == '1 month' else '') + '>Deliver every ' + f + '</option>'
                   for f in freqs)
    return (
      '<aside class="satc" data-handle="' + p['handle'] + '" data-freeship="' + str(FREE_SHIP) +
      '" data-suboff="' + str(SUB_DISCOUNT) + '" aria-label="Add to cart">'
      '<button class="satc__close" type="button" data-satc-close aria-label="Dismiss">'
      + IC['close'] + '</button>'
      '<div class="satc__in">'
        '<div class="satc__hd"><img src="' + p['imgs'][0] + '" alt="" loading="lazy">'
        '<div><h3 class="h">' + p['title'] + '</h3>'
        '<p class="satc__rate"><span class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span>'
        '4.9 (6 reviews)</p>'
        '<p class="satc__price" data-satc-price></p></div></div>'
        + groups +
        '<div class="satc__qty"><p class="satc__lbl" style="margin:0"><b>Quantity</b></p>'
        '<span class="qty" data-satc-qty>'
        '<button type="button" data-satc-step="-1" aria-label="Decrease quantity">&minus;</button>'
        '<span>1</span>'
        '<button type="button" data-satc-step="1" aria-label="Increase quantity">+</button></span></div>'
        '<div class="satc__ship"><p data-satc-ship></p>'
        '<span class="satc__bar"><i data-satc-bar></i></span></div>'
      '</div>'
      '<div class="satc__foot">'
        '<div class="satc__sub on">'
          '<label><span class="satc__sw" data-satc-sub role="switch" aria-checked="true"></span>'
          '<span><b>Subscribed.</b> Saving ' + str(int(SUB_DISCOUNT * 100)) + '%</span></label>'
          '<select data-satc-freq aria-label="Delivery frequency">' + opts + '</select>'
        '</div>'
        '<button class="satc__cta" type="button" data-satc-cta>Add to cart</button>'
      '</div></aside>')


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
        cache[u] = 'assets/' + stem + '.' + ext
        ok += 1
    for f in files:
        pth = os.path.join(OUT, f)
        s = open(pth, encoding='utf-8').read()
        for u, local in cache.items():
            s = s.replace(u, local)
        open(pth, 'w', encoding='utf-8').write(s)
    print('localised %d/%d' % (ok, len(urls)))

def main():
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(hub())
    open(os.path.join(OUT, 'home.html'), 'w', encoding='utf-8').write(
        page('Clark&rsquo;s Botanicals', home()))
    open(os.path.join(OUT, 'collection.html'), 'w', encoding='utf-8').write(
        page('Best Sellers &ndash; Clark&rsquo;s Botanicals', collection()))
    open(os.path.join(OUT, 'product.html'), 'w', encoding='utf-8').write(
        page('DNA-42 Clinicalift Serum&trade; &ndash; Clark&rsquo;s Botanicals', product()))
    print('pages written to', OUT)
    if '--no-assets' not in sys.argv:
        localise()

if __name__ == '__main__':
    main()
