function testConn() {
    var method = $('#task_interface_method').val();
    var url = $('#task_interface_url').val();
    var params = $('#task_interface_params').val();

    $.ajax({
        url: '/api/testconn',
        type: 'get',
        dataType: 'json',
        headers: {
            'Content-Type': 'application/json'
        },
        data: {'url': url, 'params': params, 'method': method},
        beforeSend: function(){
             // Handle the beforeSend event
                var index = layer.load(1, {
                  shade: [0.1,'#fff'] //0.1透明度的白色背景
                });
            },
        success: function (o) {
            layer.closeAll('loading');
            if (o.RESPONSE.RETURN_CODE == 'S') {
                $('#icon_cicle').css({color: "#097a1f"})
                layer.msg('测试通过')
            } else {
                $('#icon_cicle').css({color: "#9c000a"})
            }

        }


    })


}

$(document).ready(function () {


    $("#form").steps({
        bodyTag: "fieldset",
        onStepChanging: function (event, currentIndex, newIndex) {
            // Always allow going backward even if the current step contains invalid fields!
            if (currentIndex > newIndex) {
                return true;
            }

            // Forbid suppressing "Warning" step if the user is to young
            if (newIndex === 3 && Number($("#age").val()) < 18) {
                return false;
            }

            var form = $(this);

            // Clean up if user went backward before
            if (currentIndex < newIndex) {
                // To remove error styles
                $(".body:eq(" + newIndex + ") label.error", form).remove();
                $(".body:eq(" + newIndex + ") .error", form).removeClass("error");
            }

            // Disable validation on fields that are disabled or hidden.
            form.validate().settings.ignore = ":disabled,:hidden";

            // Start validation; Prevent going forward if false
            return form.valid();
        },
        onStepChanged: function (event, currentIndex, priorIndex) {
            // Suppress (skip) "Warning" step if the user is old enough.
            if (currentIndex === 2 && Number($("#age").val()) >= 18) {
                $(this).steps("next");
            }

            // Suppress (skip) "Warning" step if the user is old enough and wants to the previous step.
            if (currentIndex === 2 && priorIndex === 3) {
                $(this).steps("previous");
            }
        },
        onFinishing: function (event, currentIndex) {
            var form = $(this);

            // Disable validation on fields that are disabled.
            // At this point it's recommended to do an overall check (mean ignoring only disabled fields)
            form.validate().settings.ignore = ":disabled";

            // Start validation; Prevent form submission if false
            return form.valid();
        },
        onFinished: function (event, currentIndex) {
            var form = $(this);

            // Submit form input
            form.submit();
        }
    }).validate({
        errorPlacement: function (error, element) {
            element.before(error);
        },
        rules: {
            confirm: {
                equalTo: "#password"
            }
        }
    });
});