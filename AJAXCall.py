from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

if __name__ == '__main__':

    from jslib import jQuery

    jqajax = jQuery.JavaScript(
        endpoint = '/someURL',
        method = 'post',
        success = 'success_callback',
        param_list = ['foo', 'bar'],
    )

    print(jqajax.create_named_function(success='write_outbox'))


