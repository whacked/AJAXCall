Poor man's JavaScript ajax call generator

a barebones ajax function / call generator. Currently only targets jQuery ``$.ajax``

usage
-----

::
    
    from AJAXCall.jslib import jQuery
    jqajax = jQuery.JavaScript(
        endpoint = '/someURL',
        method = 'post',
        success = 'success_callback',
        param_list = ['foo', 'bar'],
    )

then use it in your HTML output or whatever

::

    >>> print(jqajax.create_named_function(success='override_callback'))
    function ajax_someURL(bar,foo) {$.ajax({ url:"/someURL"
    , method:"post"
    , data:{bar:bar,foo:foo}
    , success:override_callback })}

In the above example, the ``success`` parameter is being
overridden at render-time. **It is raw javascript**.  The
generator is NOT javascript syntax-aware. No parsing or checking
for the JS is done. This is mainly for eliminate repeatedly
writing ajax functions in small projects.

Here's a minimal example for Flask:

::
    
    from flask import Flask, render_template_string, request, url_for
    from jslib import jQuery

    app = Flask(__name__)

    @app.route('/echo', methods=['POST'])
    def echo():
        return str(request.values.to_dict())

    @app.route('/', methods=['GET','POST'])
    def index():
        return render_template_string('''\
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js" type="text/javascript"></script>
        <script>
        function mycallback(resp) {
            alert(resp)
        }
        {{ jqajax.create_named_function(success='mycallback')|safe }}
        </script>
        Note again, the param list is sorted!
        <button onclick="{{ jqajax.create_function_name() }}('Pumpkin', 'Scarecrow')">click me</button>
        ''',
            jqajax = jQuery.JavaScript(
                endpoint = url_for('.echo'),
                method = 'post',
                success = 'success_callback',
                ## note: these will be sorted, so
                ## in javascript you need to call the function with
                ## firstname, lastname
                param_list = ['lastname','firstname'],
            )
        )

    app.run()
