# -*- coding: utf-8 -*-

#from django.template.base import Template, RequestContext  # Library, Node

from obdjects.templates import MinamlTemplate #, StylusTemplate



admin_grid_page = MinamlTemplate ('''\
    %extends "admin/base_site.html"
    %block content_title
        h1 | Orders Grid (Admin)
    %block content
        table
            tr
                th | Check for new orders
            %for order in orders
                tr
                    th
                        =order.id
                    td | emails
                    td
                        =order.orderstatus
                    td width="10%"
                        =order.name
                    td width="10%"
                        =order.org
                    td
                        =order.total
                    td
                        =order.paymeth
                    td
                        =order.orderdate|date:"D m/d/y H:i"
                    td title="{{ order.internalnotes }}"
                        =order.costofgoods
                    td
                        =order.shipdate|date:"D m/d/y"
                    td
                        Actions
    ''',

    destination = 'admin_grid.html',
)


cart_page = MinamlTemplate ('''\
    %extends "base.html"
    %block content_row
        ::comment
            %load linkedin
            %linkedin_button
            <a href="{% url socialauth_begin 'linkedin' %}">Enter using LinkedIn</a>
            <a href="{% url socialauth_begin 'facebook' %}">Enter using FaceBook</a>
            <a href="{% url socialauth_begin 'twitter' %}">Enter using Twitter</a>
            <a href="{% url socialauth_begin 'github' %}">Enter using Github</a>
            <a href="{% url socialauth_begin 'dropbox' %}">Enter using DropBox</a>
            <a href="{% url socialauth_begin 'google' %}">Enter using Google</a>
        form#cartform action="/cart/" method=POST
            .row#title_row
                .two.columns
                    #back
                        a href=/showroom/ | Continue Shopping
                .eight.columns
                    %block content_title
                        h1 | Your Cart
                .two.columns
                    #next
                        a href=/checkout/ | Check<br>Out
            .row#content_row
                .one.columns
                    &nbsp;
                .ten.columns
                    %block content
                        > br
                        %if content
                            =content|safe
                            > input.nice.green.radius.button type=submit name=update value="Update Quantities"
                            > input.nice.green.radius.button type=submit name=delete value="Empty Cart"
                            > br
                            > br
                        %if not content
                            h3 | Your cart is empty!
                            h5
                                a href=/ | Return to shopping
                            > br
                            > br
                .one.columns
                    &nbsp;
    ''',

    destination = 'cart.html',
    #compile_if_newer=__file__,
)


checkout_form = MinamlTemplate ('''\
    thead
        tr
            th colspan=3
                =form.header|safe
    tr
        td colspan=3
            =form.non_field_errors
    %for field in form
        tr
            th
                =field.label
            td
                =field.errors
                =field
            td title="{{ field.help_text|striptags }}"
                =field.help_text|safe
            ::comment
                |truncatechars:50
    ''',

    destination = '_checkout_form.html',
)


checkout_page = MinamlTemplate ('''\
    %extends "base.html"
    %block head_bottom
        <script>var aha;</script>
    %block content_row
        form.nice#checkoutform action="/checkout/confirm/" method=POST
            .row#title_row
                .two.columns
                    #back
                        a href=/cart/ | Your Cart
                .eight.columns
                    %block content_title
                        h1 | Checkout
                .two.columns
                    #next
                        a href=/checkout/ | Confirm<br>Order
                        ::comment
                            > input type=submit value="Confirm<br>Order"
            .row#content_row
                .two.columns
                    &nbsp;
                .eight.columns
                    %block content
                        > br
                        h3
                            Your Order: {{ totqty }} item{{ totqty|pluralize }}, US${{ grandtot|floatformat:2 }} pretax/shipping
                        h5
                            Name:
                            =user.first_name
                            =user.last_name
                            User:
                            =user
                            eMail:
                            =user.email
                        > br
                        %for form in formlist
                            table
                                ::comment
                                    %include "_checkout_form.html"
                                =form
                        > input.nice.green.radius.button type=submit name=update value="Update"
                        > br
                        > br
                .two.columns
                    &nbsp;
    %block js_bottom
        =customer_form.media
        script type=text/javascript VERBATIM
            $('#next a').click (function(event) {
                event.preventDefault();
                $('#checkoutform').submit();
            });
    ''',

    destination = 'checkout.html',
)



addr = MinamlTemplate ('''\
    tr
        td
            %firstof addr.name '&nbsp;'
    tr
        td
            =addr.address1
    %if addr.address2
        tr
            td
                =addr.address2
    tr > td | {{ addr.city }}, {{ addr.state }}
    tr
        td
            =addr.zip
            =addr.country
    tr
        td
            =addr.customer.email

    ''',
    destination = '_addr.html',
)


#addr_header = MinamlTemplate ('''\
#   ''',
#    destination = '_addr_header.html',
#)


final_cart = MinamlTemplate ('''\
    %load expr
    #final_cart
        %if order.id
            table border=0 cellpading=5 cellspacing=0
                tr
                    th align=left | Order Number
                    td |= order.id
                tr
                    th align=left | Order Date
                    td |= order.created
        table width=100% border=1 style="border:0; margin:0; padding:0;"
            tr
                td style="padding:0"
                    table width=100%
                        thead > tr > th | Ship To
                        tbody
                            %with addr=ses.shipping_address
                                %include "_addr.html"
                td style="padding:0"
                    table width=100%
                        thead > tr > th | Bill To
                        tbody
                            %with addr=ses.billing_address
                                %include "_addr.html"
                    ::comment
                        =seshelp.cart_details|safe
        table width=100% border=0
            thead
                tr
                    th | Reference / PO Number
                    th | Payment Meth
                    th | Payment Terms
                    th | Special Instructions
            tr
                td style="text-align:center" |= order.reference_number
                td style="text-align:center" |= payment.get_payment_method_display
                td style="text-align:center"
                    %firstof payment.get_payment_terms_display 'TBD'
                    = payment.last_4
                td style="text-align:center" |= order.special_instructions
        table border=0
            thead
                tr
                    th | Line
                    th | Sku
                    th | Summary
                    th | Notes
                    th | Qty
                    th | Price
                    th | Ext
            %for line in ses.cart
                tr
                    td |= forloop.counter
                    td |= line.sku
                    td |= line.summary|safe
                    td |= line.notes
                    td |= line.qty
                    td | ${{ line.totprice|floatformat:2 }}
                    td | {% expr line['totprice']*line['qty'] as extprice %}${{ extprice|floatformat:2 }}
                    ::comment
                        {{ line.qty*line.totprice }}
            tr
                ::comment
                    %with smry=seshelp.cart_summary
                td colspan=6 > strong | Subtotal for {{ totqty }} item{{ totqty|pluralize }}:
                td > strong | ${{ grandtot|floatformat:2 }}
            %if ses.order.california_tax
                tr
                    td colspan=6 | Sales Tax ({{ ses.order.california_tax }}, {{ ses.order.california_tax.tax }})
                    ::comment
                        td | {% expr float(ses['order'].california_tax.tax)*seshelp.cart_summary() ['grandtot']/100.0 as tax %}${{ tax|floatformat:2 }}
                    td | ${{ tax|floatformat:2 }}
            %if ses.order.shipping_payment == "included"
                tr
                    td colspan=6 | Shipping & Handling ({{ ses.order.shipping_method }}, {{ ses.order.preferred_shipper }})
                    td | ${{ ses.order.shipping|floatformat:2 }}
            tr
                ::comment
                    %with smry=seshelp.cart_summary
                td colspan=6 > strong | Grand Total for {{ totqty }} item{{ totqty|pluralize }} with tax & shipping:
                ::comment
                    td > strong | {% expr smry['grandtot']+tax as gtts %}${{ gtts|floatformat:2 }}
                    td > strong | {% expr grandtot+tax+float(shipping) as gtts %}${{ gtts|floatformat:2 }}
                td > strong | ${{ gtts|floatformat:2 }}
    ''',
    destination = '_final_cart.html',
)


confirm_page = MinamlTemplate ('''\
    %extends "base.html"
    %block content_row
        form.nice#confirmform action="/checkout/order/" method=POST
            .row#title_row
                .two.columns
                    #back
                        a href=/checkout/ | Edit<br>Info
                .eight.columns
                    %block content_title
                        h1 | Confirm Your Order
                .two.columns
                    #next
                        a href=/checkout/order/ | Place<br>Order
            .row#content_row
                .two.columns
                    &nbsp;
                .eight.columns
                    %block content
                        .panel
                            %include "_final_cart.html"
                            p.clearfix
                                &nbsp;
                        > br
                        h3
                            Your Order: {{ totqty }} item{{ totqty|pluralize }}, US${{ gtts|floatformat:2 }} with tax & shipping
                        h5
                            Name:
                            =user.first_name
                            =user.last_name
                            User:
                            =user
                            eMail:
                            =user.email
                        > br
                        > input.nice.green.radius.button type=submit name=order value="Place Order"
                        > br
                        > br
                .two.columns
                    &nbsp;
    %block js_bottom
        =customer_form.media
    ''',

    destination = 'confirm.html',
)

email_order = MinamlTemplate ('''\
    html
        body
            h1
                Your eRacks Order
            %include "_final_cart.html"
    ''',
    destination = 'email_order.html',
)


ordered_page = MinamlTemplate ('''\
    %extends "base.html"
    %block content_row
        .row#content_row
            .two.columns
                &nbsp;
            .eight.columns
                %block content
                    h1
                        Thank you for your order!
                    .panel
                        %include "_final_cart.html"
                        p.clearfix
                            &nbsp;
                    > br
                    h4
                        Please print this page for your records.
                    p
                        An email confirmation has also been sent to
                        %firstof order.customer.email order.customer.user.email
            .two.columns
                &nbsp;
    ''',
    destination = 'ordered.html',
)

#cart_details = MinamlTemplate ('''\
#    =content|safe
#    > input.nice.green.radius.button type=submit name=update value="Update Quantities"
#    > input.nice.green.radius.button type=submit name=delete value="Empty Cart"
#    > br
#    ''',
#    destination = '_cart_details.html',
#)



out = """
content_row = MinamlTemplate ('''\
.row style="background:wheat"
    #next
        a href=/checkout/confirm/ | Next<br>Step

    #back
        a href=/products/ | Continue Shopping


    .eight.columns.centered.panel

        h1
            Checkout

        form.nice

            {{ checkoutform.as_p }}

        table
            tr
                th | This is the MINAML FILTER.
                th | this is column 2.
                th | this is column 3.

            tr
                {% for cust in CustomerImage_objects.published %}
                td | {{ cust.caption }}{% endfor %}

        let's see where this text appears

        <ul>
            {% for cust in customers %}
                <li>{{ cust.caption }}</li>
            {% endfor %}
        </ul>
''')

"""