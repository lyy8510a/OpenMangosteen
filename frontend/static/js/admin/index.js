var delay_table;
var log_path;

function getlog(task_id,type) {
    var csrf_token = $('#csrf_token').val();
    var task_interface_logarea = $('#task_interface_logarea');
    if (task_interface_logarea.length == 0) {
        layer.open({
            title: '查看日志',
            area: ['950px', '600px'],
            content: '<pre id="task_interface_logarea" style="background: black;color: green;height: 600px;"> </pre>'
        })
        task_interface_logarea = $('#task_interface_logarea');
    }
    task_interface_logarea.append('>>>>>>>>>>>>>>>>>>>>>start>>>>>>>>>>>>>>>>>>>>\r\n');


    setInterval(function () {
        $.ajax({
            url: '/task/get_task_log',
            type: 'get',
            data: {'task_id': task_id,'task_type':type,'csrf_token': csrf_token},
            dataType: 'json',
            async: false,
            // headers: {
            //     'Content-Type': 'application/json'
            // },
            success: function (o) {
                if (o.RESPONSE.RETURN_CODE == 'S') {
                    if(o.RESPONSE.RETURN_DATA){
                        task_interface_logarea.append('>' + o.RESPONSE.RETURN_DATA + '\r\n');
                    }else{
                        task_interface_logarea.append('>>>>>>>>>>>>>>>>>>>>pendding>>>>>>>>>>>>>>>>>>>>>>>>' + '\r\n');
                    }


                }
            }
        })


    }, 1000 * 2);
    //    2 s
}

function stop_task(task_id,type) {
    var csrf_token = $('#csrf_token').val();
    $.ajax({
        url: '/task/stop_task',
        type: 'post',
        data: {'task_id': task_id,'task_type':type, 'csrf_token': csrf_token},
        dataType: 'json',
        async: false,
        // headers: {
        //     'Content-Type': 'application/json'
        // },
        success: function (o) {
             window.location.reload()
        },
        error:function () {
            window.location.reload()
        }

    })
}

function start_task(task_id,type) {
    var csrf_token = $('#csrf_token').val();
    $.ajax({
        url: '/task/start_task',
        type: 'post',
        data: {'task_id': task_id,'task_type':type,'csrf_token': csrf_token},
        dataType: 'json',
        async: false,
        // headers: {
        //     'Content-Type': 'application/json'
        // },
        success: function (o) {
            if (o.RESPONSE.RETURN_CODE == 'S') {
                window.location.reload()
            }else {
                window.location.reload()
                layer.msg("启动失败")

            }
        }
    })
}

function del_task(task_id,type) {
    var csrf_token = $('#csrf_token').val();
    $.ajax({
        url: '/task/del_task',
        type: 'post',
        data: {'task_id': task_id,'task_type':type, 'csrf_token': csrf_token},
        dataType: 'json',
        // headers: {
        //     'Content-Type': 'application/json'
        // },
        success: function (o) {
            if (o.RESPONSE.RETURN_CODE == 'S') {
                window.location.reload()
            }else {
                window.location.reload()
                layer.msg("删除失败")

            }
        }


    })
}


function init_datatable() {
    delay_table = $('#task_runnning_tb').DataTable({
        destroy: true,
        order: [1, 'desc'],
        searching: true,
        bFilter: true,
        bInfo: true,
        buttons: [
            {extend: 'copy'},
            {extend: 'csv'},
            {extend: 'excel', title: 'ExampleFile'},
            {extend: 'pdf', title: 'ExampleFile'},

            {
                extend: 'print',
                customize: function (win) {
                    $(win.document.body).addClass('white-bg');
                    $(win.document.body).css('font-size', '10px');

                    $(win.document.body).find('table')
                        .addClass('compact')
                        .css('font-size', 'inherit');
                }
            }
        ]
    });
}

$(document).ready(function () {
    $('.dataTables-example').DataTable({
        destroy: true,
        order: [1, 'desc'],
        searching: true,
        bFilter: true,
        bInfo: true,
        buttons: [
            {extend: 'copy'},
            {extend: 'csv'},
            {extend: 'excel', title: 'ExampleFile'},
            {extend: 'pdf', title: 'ExampleFile'},

            {
                extend: 'print',
                customize: function (win) {
                    $(win.document.body).addClass('white-bg');
                    $(win.document.body).css('font-size', '10px');

                    $(win.document.body).find('table')
                        .addClass('compact')
                        .css('font-size', 'inherit');
                }
            }
        ]
    });


    //刷新当前表格和地图的数据
    setInterval(function () {

        $.ajax({
            url: '/api/get_job',
            type: 'get',
            dataType: 'json',
            headers: {
                'Content-Type': 'application/json'
            },
            success: function (o) {
                if (o.RESPONSE.RETURN_CODE == 'S') {
                    delay_table.destroy();
                    var _html = '';
                    for (i = 0; i < o.RESPONSE.RETURN_DATA.length; i++) {
                        _html += '<tr>' +
                            '<td>' + o.RESPONSE.RETURN_DATA[i].id + '</td>' +
                            '<td>' + o.RESPONSE.RETURN_DATA[i].name + '</td>' +
                            '<td>' + o.RESPONSE.RETURN_DATA[i].next_run_time + '</td>' +
                            '<td>' + o.RESPONSE.RETURN_DATA[i].interval + '</td>' +
                            '<td>' + o.RESPONSE.RETURN_DATA[i].start_date + '</td>' +
                            '<td>' + o.RESPONSE.RETURN_DATA[i].args + '</td>' +
                            '</tr>';
                    }
                    $('#tb').html(_html)

                }


                init_datatable();
            }


        })


    }, 1000 * 300);
    //    300 s


})

