//device_manager


//device_settings
//hide buttons
$('#Submit').hide();
$('#Cancel-Info').hide();
$('#Update').hide();
$('#Cancel-Sec').hide();

//edit device
$('#Edit').click(function () {
    $("input.edit").prop('disabled', false)
    $('#Submit').show();
    $('#Cancel-Info').show();
    $('#Edit').hide();
    $('button.delete').hide();
});

$("#Cancel-Info").click(function () {
    $("input.edit").prop('disabled', true)
    $('#Edit').show();
    $('button.delete').show();
    $('#Submit').hide();
    $('#Cancel-Info').hide();
    $('form')[0].reset();
});

// edit security settings
$("#Security").click(function () {
    $("input.security").prop('disabled', false)
    $('#Update').show();
    $('#Cancel-Sec').show();
    $('#Security').hide();
    $('form')[0].reset();
});

$("#Cancel-Sec").click(function () {
    $("input.security").prop('disabled', true)
    $('#Update').hide();
    $('#Cancel-Sec').hide();
    $('#Security').show();
    $('form')[1].reset();
});

// get device for id for deletion
function getID(id) {
    document.getElementById('delete').value = id;
}

$('#Submit').hide();
    $('#Cancel').hide();

$('#Edit').click(function () {
    $("input.detail").prop('disabled', false)
    $('#Submit').show();
    $('#Cancel').show();
    $('#Edit').hide();
    $('button.delete').hide();
});

$("#Cancel").click(function () {
    $("input.detail").prop('disabled', true)
    $('#Edit').show();
    $('button.delete').show();
    $('#Submit').hide();
    $('#Cancel').hide();
    $('form')[0].reset();
});


