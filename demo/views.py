from django.http import HttpResponse
from math import *
from double import *

safe_list = ['math','acos', 'asin', 'atan', 'atan2', 'ceil', 'cos', 'cosh', 'degrees', 'e', 'exp', 'fabs', 'floor', 'fmod', 'frexp', 'hypot', 'ldexp', 'log', 'log10', 'modf', 'pi', 'pow', 'radians', 'sin', 'sinh', 'sqrt', 'tan', 'tanh']
safe_dict = dict([ (k, locals().get(k, None)) for k in safe_list ])

def index(request):
    input = request.GET['input']
    result = """
<html>
  <head>
    <title>SEJITS training demo</title>
  </head>
  <body>
    <script src="/resources/jquery.js"></script>
    <script>
      $.get('runsejits/', {input: '""" + input + """'}, function(result){
        $("#result").html(result);
      });
    </script>
"""
    result += '<p>Running SEJITS...</p>'
    result += '<div id="result"></div>'
    result += """
  </body>
</html>
"""
    return HttpResponse(result)

def runsejits(request):
    result = ''
    result += "Running test_generated" + '<br/>'
    arr = eval(request.GET['input'],{"__builtins__":None}, safe_dict)
    result += str(arr) + '<br/>'
    doubledarr = ArrayDoubler().double_using_template(arr)
    result += str(doubledarr) + '<br/>'
    return HttpResponse(result)
