var getStep = function() {
    result = $.cookie("step");
    return result;
}

var setStep = function(stepNum) {
    $.cookie("step", stepNum, { path: '/' });
}

var update = function() {
    var instructions = $('#instructions')[0];
    if (getStep() == 'start') {
        instructions.innerHTML = '<p>Welcome to the Asp tutorial! Asp is a Python platform that makes it easy for you to build <i>specializers</i>, ' +
                                 'simple compilers for high-performance domain-specific languages embedded in Python.</p>' +
                                 '<p>We begin with a very simple specializer, ArrayDoubler, which takes an array and multiplies each element by 2. ' +
                                 'The code to the right invokes ArrayDoubler on a particular input array. Click <i>Run</i> to see what happens.</p>';
        $('#code')[0].readOnly = true;
        nextStepAfterRun = 'array-doubler-modify-input';
    } else if (getStep() == "array-doubler-modify-input") {
        instructions.innerHTML = '<p>Asp generated a C++ source file <b>module.cpp</b> and then compiled it on-the-fly using g++ to a shared library. ' +
                                 'It then passed the input array to that library.</p><p>Try <b>changing an element of the input array</b> and clicking <b>Run</b> again.</p>';
        $('#code')[0].readOnly = false;
        nextStepAfterRun = 'array-doubler-extend-input';
    } else if (getStep() == "array-doubler-extend-input") {
        instructions.innerHTML = '<p>Notice that Asp did not need to compile again - it just called the same shared library it generated before, allowing it to run quickly.</p>' +
                                 '<p>Now, try <b>adding an element to the input array</b>, making it one element longer, and clicking <b>Run</b> again.</p>';
        nextStepAfterRun = 'array-doubler-explain';
    } else if (getStep() == "array-doubler-explain") {
        instructions.innerHTML = '<p>This time Asp did need to compile again. To find out why, we will investigate how ArrayDoubler works. Click Next below to continue.</p>';
        instructions.innerHTML += '<p><a href="." onclick="goToStep(\'array-doubler-tweak-template-code\'); return false;">Next</a></p>';
        $("#run")[0].disabled = true;
    } else if (getStep() == "array-doubler-tweak-template-code") {
        $('#code')[0].readOnly = true;
        $('#code').val("ad = ArrayDoubler()\n" +
                       "doubled_array = ad.double_using_template([1.0, 2.0, 3.0, 4.0])\n" +
                       "print(doubled_array)\n")
        $("#runningmessage").html('');
        $("#result").html('');
        $('#templatecodediv')[0].style.display = 'inline';
        $("#run")[0].disabled = false;

        instructions.innerHTML = '<p>To the right is the <i>template code</i> used to generate the C++ code. It looks like C++, but with one small difference: ' +
                                 'there is a <b>placeholder</b> <code>${num_items}</code> that gets replaced by the length of the array when code is generated.</p>'
        instructions.innerHTML += '<p><b>Press the Run button</b> to see the generated C++ code.</p>';
        nextStepAfterRun = 'array-doubler-template-explain';
    } else if (getStep() == "array-doubler-template-explain") {
        instructions.innerHTML = '<p>In the generated C++ code, <code>${num_items}</code> has been replaced by 4, the input array length. So it will only work for input vectors of length 4.</p>';
        instructions.innerHTML = '<p>Next, we\'re going to change what this specializer does. <b>Modify the template</b> to multiply the input vector by 3 instead of 2, then click <b>Run</b>.</p>';
        nextStepAfterRun = 'array-doubler-tweak-template-code';
    } else if (getStep() == "array-doubler-tweak-template-code") {
        instructions.innerHTML = '<p>More coming.</p>';
    }
}

var goToStep = function(stepNum) {
    setStep(stepNum);
    update();
}

$(document).ready(function() {
  goToStep('start');
  $("#form").submit(function(event) {
    $("#runningmessage").html('Running Asp...');
    $("#run")[0].disabled = true;
    $("#result").html('');
    event.preventDefault();
    $.get('runsejits/', {input: $("#code").val(), template: $("#templatecode").val()}, function(result){
      $("#runningmessage").html('Running Asp... done.');
      $("#result").html(result);
      $("#run")[0].disabled = false;
      goToStep(nextStepAfterRun);
    });
  });
});
