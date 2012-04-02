from django.http import HttpResponse
from math import *
from double import *
import sys
from cStringIO import StringIO
from shutil import rmtree

safe_list = ['math','acos', 'asin', 'atan', 'atan2', 'ceil', 'cos', 'cosh', 'degrees', 'e', 'exp', 'fabs', 'floor', 'fmod', 'frexp', 'hypot', 'ldexp', 'log', 'log10', 'modf', 'pi', 'pow', 'radians', 'sin', 'sinh', 'sqrt', 'tan', 'tanh', 'print']
safe_dict = dict([ (k, locals().get(k, None)) for k in safe_list ])

def index(request):
    rmtree('cache')
    result = """
<html>
  <head>
    <title>Asp: First steps</title>
  </head>
  <body>
    <script src="/resources/jquery.js"></script>
    <script src="/resources/jquery.cookie.js"></script>
    <link rel="stylesheet" type="text/css" href="/resources/demo.css" />
    <script src="/resources/demo.js"></script>

    <div id="container">
        <div id="header">
            <h1 style="margin-bottom:0;">Asp: First steps</h1>
        </div>

        <table border="0" width="100%">
        <tr>
        <td width="100%" style="vertical-align:top"><div id="instructions"/></td>

        <td style="background-color:#EEEEEE; float:right;">

            <form id="form">
              <div id="applicationcodediv">
              Application code:<br/>
              <textarea id="code" cols="80" rows="3" readonly="readonly">
ad = ArrayDoubler()
doubled_array = ad.double_using_template([1.0, 2.0, 3.0, 4.0])
print(doubled_array)
</textarea><br></div>
              <div id="templatecodediv" style="display:none;">
              Template code (<code>double_template.mako</code>):<br/>
              <textarea id="templatecode" cols="80" rows="14">
PyObject* double_in_c(PyObject* arr) {
    PyObject* new_arr = PySequence_List(arr);
    Py_INCREF(new_arr);
    Py_ssize_t index = 0;
    for (int i=0; i<${num_items}; i++) {
        PyObject* item = PySequence_GetItem(arr, index);
        PyObject* two = PyFloat_FromDouble(2.0);
        PyObject* newnum = PyNumber_Multiply(item, two);
        Py_INCREF(newnum);
        PySequence_SetItem(new_arr, index, newnum);
        index++;
    }
    return new_arr;
}
</textarea><br></div>
              <input type="submit" value="Run" id="run" />
            </form>
            <div id="runningmessage"><p>&nbsp;</p></div>
            <div id="result"><p>&nbsp;</p></div>

        </td>
        </tr></table>

        <div id="footer"><i>To learn more about Asp and SEJITS, visit <a href="https://github.com/shoaibkamil/asp/wiki/">the Asp wiki.</a></i></div>
    </div>
  </body>
</html>
"""
    return HttpResponse(result)

class ExecWrapper:
    def __init__(self, code):
        self.str = code

    def run(self):
        exec(self.str)

def capture_output(f):
    # Based on http://stackoverflow.com/questions/5136611/capture-stdout-from-a-script-in-python
    # Save old stdout and replace with a StringIO() to capture
    backup = sys.stdout
    sys.stdout = StringIO()
    f.run()
    out = sys.stdout.getvalue() # get output
    sys.stdout.close()
    sys.stdout = backup # restore original stdout
    return out

def runsejits(request):
    result = ''
    set_template_text(request.GET['template'])
    output = capture_output(ExecWrapper(request.GET['input']))
    # ,{"__builtins__":None}, safe_dict)
    result += '<p>Output:</p>' + '<p>' + str(output.replace("\n", "<br/>")) + '</p>'
    return HttpResponse(result)
