from string import Template

class JavaScript:
    _autogen_count = 0
    _function_prefix = 'ajax_'
    _tp_special_opt = (
        'method', 'contentType', 'dataType',
    )

    def __init__(self, **kw):
        self.id = self._autogen_count
        self.__class__._autogen_count += 1
        self._conf = kw
        self._param_list = tuple(sorted(kw.get('param_list', [])))

    def create_ajax_object(self, **override):
        tpl = Template('''{ url:${URL}${SPECIAL}${DATA}${ON_RETURN} }''')
        endpoint = self._conf.get('endpoint')
        return tpl.substitute(
            URL = endpoint and '"%s"'%endpoint or 'document.baseURI',
            SPECIAL = ''.join(
                '\n, {0}:"{1}"'.format(
                    opt, override.get(opt, self._conf[opt])
                ) for opt in self.__class__._tp_special_opt
                if opt in self._conf or opt in override
            ),
            DATA = self._param_list \
                    and '\n, data:{%s}' % (','.join('{0}:{0}'.format(p) for p in self._param_list))
                    or '',
            ON_RETURN = ''.join(
                '\n, {0}:{1}'.format(k, override.get(k, self._conf.get(k)))
                for k in ('success', 'error')
                if k in self._conf or k in override
            )
        )

    def create_ajax_call(self, **override):
        return '$.ajax(%s)' % ( self.create_ajax_object(**override) )
    
    def create_function_name(self):
        return '%s%s' % (
            self.__class__._function_prefix,
            self._conf.get('endpoint', 'auto%s'%self.id).replace('/', ''),
        )

    def create_named_function(self, **override):
        tpl = Template('''function ${FUNCTION_NAME}(${PARAM_LIST}) {${AJAX_CALL}}''')
        return tpl.substitute(
            FUNCTION_NAME = self.create_function_name(),
            PARAM_LIST = ','.join(self._param_list),
            AJAX_CALL = self.create_ajax_call(**override),
        )

