# Simple example of using templates

import os

class ArrayDoubler(object):
    def __init__(self):
        self.pure_python = True

    def double_using_template(self, arr):
        import asp.codegen.templating.template as template
        # mytemplate = template.Template(filename=os.path.dirname(__file__) + "/double_template.mako", disable_unicode=True)
        # template.Template("")
        mytemplate = template.Template(template_text)
        rendered = mytemplate.render(num_items=len(arr))

        import asp.jit.asp_module as asp_module
        try:
            os.mkdir("cache")
        except OSError:
            pass
        mod = asp_module.ASPModule(cache_dir = "cache")
        mod.add_function("double_in_c", rendered)
        return mod.double_in_c(arr)

    def double(self, arr):
        return map (lambda x: x*2, arr)

def set_template_text(text):
    global template_text
    template_text = text
