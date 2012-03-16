from django.http import HttpResponse
from math import *
from double import *
import sys
from cStringIO import StringIO

safe_list = ['math','acos', 'asin', 'atan', 'atan2', 'ceil', 'cos', 'cosh', 'degrees', 'e', 'exp', 'fabs', 'floor', 'fmod', 'frexp', 'hypot', 'ldexp', 'log', 'log10', 'modf', 'pi', 'pow', 'radians', 'sin', 'sinh', 'sqrt', 'tan', 'tanh', 'print']
safe_dict = dict([ (k, locals().get(k, None)) for k in safe_list ])

def index(request):
    result = """
<html>
  <head>
    <title>SEJITS training demo</title>
  </head>
  <body>
    <script src="/resources/jquery.js"></script>
    <script>
      $(document).ready(function() {
        $("#form").submit(function(event) {
          $("#runningmessage").html('Running SEJITS...');
          $("#result").html('');
          event.preventDefault();
          $.get('runsejits/', {input: $("#code").val()}, function(result){
            $("#runningmessage").html('Running SEJITS... done.');
            $("#result").html(result);
          });
        });
      });
    </script>
    <form id="form">
      <textarea id="code" cols="80" rows="5">
print(ArrayDoubler().double_using_template([1.0, 2.0, 3.0, 2.0]))
</textarea><br>
      <input type="submit" value="Run" id="run" />
    </form> 
"""
    result += '<div id="runningmessage"></div>'
    result += '<div id="result"></div>'
    result += """
  </body>
</html>
"""
    return HttpResponse(result)

class ExecWrapper:
    def __init__(self, str):
        self.str = str

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
    output = capture_output(ExecWrapper(request.GET['input']))
    # ,{"__builtins__":None}, safe_dict)
    result += '<p>Output:</p>' + '<p>' + str(output.replace("\n", "<br/>")) + '</p>'
    return HttpResponse(result)
