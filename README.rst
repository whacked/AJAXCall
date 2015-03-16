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


