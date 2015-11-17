# -*- coding: utf-8 -*-

from obdjects.templates import MinamlTemplate #, StylusTemplate

#import settings

#product_css = StylusTemplate('''\
#
#''',
#    destination = 'product.css',
#)


# product list sidebar partial
product_list = MinamlTemplate ('''\
    %load cache
    %cache 36000 product_list
        .box#product_list
            h4
                eRacks Products

            ul.nav-bar.vertical
                %for cat in Categories_objects.published
                    li.has-flyout
                        ::comment
                            #class="has-tip tip-top"
                        a class="main" href="{{ cat.url }}"
                            =cat.name
                        a class=flyout-toggle href=#
                            span ||
                        div.flyout.small
                            div.text_center
                                strong.hdr title="{{ cat.title }}"
                                    =cat.name
                            > hr
                            =cat.prods_as_divs
            div style="clear:both" ||
    ''',

    destination = '_product_list.html'
)

product_config_summary = MinamlTemplate ('''\
    .box#config_summary
        h4 | Current Configuration
        #current
            .baseprice
                Base Price:
                b
                    $
                    =product.baseprice|floatformat:2
            .price
                As Configured:
                b
                    $
                    =product.baseprice|floatformat:2
            .summary | <b>Configuration Summary:</b><br>Default Configuration
            a.nice.small.green.radius.button onclick='$("#config-tab").click();' href="#config" | Configure Now
            a.nice.small.green.radius.button onclick='$("#add_to_cart").click();' href="#add" | Add to Cart
            ::comment
                a.nice.green.radius.button href="/add-to-wishlist/" | Add to Wishlist
                a.nice.green.radius.button href="/request-quote/"   | Get a Quote
            %comment
                =product.as_config_tab
            .clear style="clear:both" | &nbsp;
    ''',

    destination = '_product_config_summary.html'
)


product_config_tab = MinamlTemplate ('''\
    table.configgrid
        thead
            tr
                th title='Hover over option to see more info' | Option
                th | Choices
                th title='Hover over choice to see more info' | More Info
                th title='Additions / subtactions from base price' | Add/Subtract
                =product.prodopts_as_table|safe
            tr
                td
                    Notes
                td
                    > input id=notes name=notes placeholder="Enter notes here"
                td
                    Enter notes or custom instructions for this item here
                td
                    &nbsp;
    ''',

    destination = '_product_config_tab.html'
)


product_main = MinamlTemplate ('''\
    %extends "base_twocolumns.html"
    ::comment
        // %load aloha_tags

    %block sidebar_one
        %include "_product_config_summary.html"
        =block.super

    %block content
        =block.super

        .content
            h1
                =product.name

            dl.nice.tabs.edt-tabs#product_tabs
                <dt></dt>
                dd
                    a.active#overview-tab href="#overview" | Overview
                dd
                    a#specs-tab href="#specs" | Specifications
                dd
                    a#photos-tab href="#photos" | Photos
                dd
                    a#config-tab href="#config" | Configure

            ul.nice.tabs-content
                li.active#overviewTab
                    ::comment
                        // %aloha product 'description'
                    =product.description|safe
                li#specsTab
                    ::comment
                        // %aloha product 'features'
                    %firstof product.features "Product features / specs are in Overview tab"
                li#photosTab
                    =photos
                li#configTab
                    form.configform action="/cart/" method=POST
                        > input type=hidden name=sku id=sku value="{{ product.sku }}"
                        %include "_product_config_tab.html"
                        > input.nice.green.radius.button#add_to_cart type=submit name=add value="Add to Cart"
                        %if user.is_staff
                            > input.nice.green.radius.button#get_quote type=submit name=quote value="Get a Quote" title="Get a quote on this configuration, or ask eRacks a question about it"
                        ::comment
                            a.nice.green.radius.button href="/add-to-wishlist/"
                                Add to Wishlist
                            a.nice.green.radius.button href="/request-quote/"
                                Get a Quote
    ''',

    destination = 'product.html'
)


products_list = MinamlTemplate ('''\
    %extends "base_onecolumn.html"

    %block content
        =block.super

        .content
            h1
                Products

            dl.nice.tabs#products_tabs
                dd
                    a.active href="#bycat" | By Category
                dd
                    a href="#byapp" | By Application

            ul.nice.tabs-content
                li.active#bycatTab
                    ul.block-grid.three-up
                        %for cat in categories
                            li.panel
                                =cat.blurb|safe
                                a href="{{ cat.url }}" title="{{ cat.title }}"
                                    =cat.name
                li#byappTab
                    Implement b's tags idea here
    ''',

    destination = 'products.html'
)


category_main = MinamlTemplate ('''\
    %extends "base_twocolumns.html"

    %block content
        =block.super

        .content
            h1
                =category.name

            =category.description|safe
    ''',

    destination = 'category.html'
)
