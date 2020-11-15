var lastRow = -1;
var fieldTimer = "";
var isExit = window.location.pathname.includes('saida');

$(document).ready( function () {
    var table = $('#serviceParking').DataTable({
        responsive: true,
        scrollY: "50vh",
        scrollCollapse: true,
        ordering: false,
        lengthChange: false,
        paging: false,
        bInfo: false,
        columns: [
            {'name': 'id'},
            {'name': 'nome'},
            {'name': 'descricao'},
            {'name': 'preco'},
            {'name': 'tipo'},
            {'name': 'id_origem','visible': false},
            {'name': 'excluido', 'visible': false}
        ]
    });

    toastr.options = {
        "closeButton": true,
        "debug": false,
        "newestOnTop": false,
        "progressBar": false,
        "positionClass": "toast-top-full-width",
        "preventDuplicates": true,
        "onclick": null,
        "showDuration": "300",
        "hideDuration": "1000",
        "timeOut": "5000",
        "extendedTimeOut": "5000",
        "showEasing": "swing",
        "hideEasing": "linear",
        "showMethod": "fadeIn",
        "hideMethod": "fadeOut"
    }

    $('#serviceParking tbody')
    .on( 'mouseenter mouseleave', 'td', function (e) {
        var rowIdx = table.cell(this).index().row;
        var len = table.$('tr').length;
        
        if (e.type == 'mouseenter') {
            if (len > 1) {
                if (  $( table.row( rowIdx ).nodes() ).hasClass('bg-selected') ) {
                    $( table.rows().nodes() ).removeClass( 'bg-grey' );
                    $( table.row( rowIdx ).nodes() ).addClass( 'bg-selected' );
                } else {
                    $( table.rows().nodes() ).removeClass( 'bg-grey' );
                    $( table.row( rowIdx ).nodes() ).addClass( 'bg-grey' );
                }
            }
        } else {
            $( table.rows().nodes() ).removeClass( 'bg-grey' );
        }
    } );

    $('#serviceParking tbody').on( 'click dblclick', 'td', function (event) {
        var rowIdx = table.cell(this).index().row;
        var columnIdx = table.cell(this).index().column;

        if ($('td > select').length == 0) {

            if (event.type == 'click' && lastRow != rowIdx) {
                if (  $( table.row( rowIdx ).nodes() ).hasClass('bg-selected') ) {
                    $( table.row(rowIdx).nodes() ).removeClass( 'bg-selected' );
                }
                else {
                    $( table.rows().nodes() ).removeClass( 'bg-selected' );
                    $( table.row(rowIdx).nodes() ).removeClass( 'bg-grey' );
                    $( table.row( rowIdx ).nodes() ).addClass( 'bg-selected' );
                }
            } else if (event.type == 'dblclick') { 
                var isParking = table.cell({row:rowIdx, column:4}).data().toLowerCase() == 'estacionamento';
                if (columnIdx == 0  && !isParking || !isExit) {
                    var originContent = $(this).val();
                    var select = $('<select id="select_service"></select>');
                    var element = $(this);
                    $.ajax({
                        type: "GET",
                        url: "/todos-servicos",
                        data: '',
                        complete: function(response) {
                            // Parse the returned json data
                            var opts = $.parseJSON(response.responseText);
                            // Use jQuery's each to iterate over the opts value
                            $.each(opts, function(i, d) {
                                // You will need to alter the below to get the right values from your json object.  Guessing that d.id / d.modelName are columns in your carModels data
                                select.append('<option value="' + d.id + '">' + d.nome + '</option>');
                            });

                            element.html(select);

                            $("#select_service").select2();

                            $("#select_service").bind('select2:closing select2:close', function (e){
                                var object = $(this);
                                
                                if (e.type == 'select2:close') {
                                    var newContent = $(this).val();
                                    
                                    if (newContent) {
                                        // Busca informações do serviço no banco
                                        $.ajax({
                                            type: "GET",
                                            url: "/busca-servico/"+newContent,
                                            data: '',
                                            dataType: "dataType",
                                            complete: function(response) {
                                                //atribui as informações resgatadas nas células da tabela
                                                if (response.status == 200) {
                                                    var service = JSON.parse(response.responseText);
                                                    var originValue = table.cell({row:rowIdx, column:3}).data();
                                                    object.parent().html(newContent);
                                                    table.cell({row:rowIdx, column:0}).data(service.id);
                                                    table.cell({row:rowIdx, column:1}).data(service.nome);
                                                    table.cell({row:rowIdx, column:2}).data(service.descricao);
                                                    table.cell({row:rowIdx, column:3}).data(service.preco);
                                                    table.cell({row:rowIdx, column:4}).data(service.tipo);
                                                    table.cell({row:rowIdx, column:6}).data("false"); 
        
                                                    if (service.tipo.toLowerCase() == 'servico') {
                                                        var totalValue = parseFloat($("#valor_total").val()) - parseFloat(originValue) + service.preco;
                                                        $("#valor_total").val(totalValue);
                                                    }
                                                    
                                                }
                                            }
                                        });
                                    } else {
                                        // object.parent().html(originContent);
                                        // object.select2('close');
                                    }
                                }
                            });
                        }
                    });


                    $(this).children().select();
                } else if (columnIdx == 0  && isParking && isExit) {
                    toastr.info('<b style="color:black; font-size:18px">Não é permitido editar o serviço do tipo estacionamento no registro da saída.</b>')  
                }
            }

            lastRow = rowIdx;
        }
    } );
    
    $('#removeService').click( function () {
        var info = table.page.info();
        var rowstot = info.recordsDisplay;
        var index = table.row('.bg-selected').index();
        var isParking = table.cell({row:index, column:4}).data().toLowerCase() == 'estacionamento';
        var isExit = window.location.pathname.includes('saida');
        
        if (rowstot > 1 && index != undefined && !isParking || !isExit)  {
            table.cell({row:index, column:6}).data("true");
            
            var totalValue = parseFloat($('#valor_total').val());
            var liquidValue = parseFloat($('#valor_liquido').val());
            var serviceValue = parseFloat(table.cell({row:index, column:3}).data());

            $('#valor_total').val(totalValue - serviceValue);
            $('#valor_liquido').val(liquidValue - serviceValue);

            $( table.row(index).nodes() ).removeClass( 'bg-selected' );
            table.search( "false" ).draw();
            
            info = table.page.info();
            rowstot = info.recordsDisplay;

            if (index >= rowstot) {
                $( table.row(index - 1).nodes() ).addClass( 'bg-selected' );
            }
        } else if (index != undefined && isParking && isExit) {
            toastr.info('<b style="color:black; font-size:18px">Não é permitido remover o serviço do tipo estacionamento no registro da saída.</b>')  
        }
    } );
    
    $('#addService').on('click', function () {
        var lastRow = table.row(':last').data();

        //adiciona apenas se a ultima linha estiver preenchida
        if (lastRow[1] || lastRow[6]) {
            table.row.add( [
                '',
                '',
                '',
                0,
                '',
                '',
                "false"
            ] ).draw( false );
        }
    } );

    $('#buttonSubmit').click( function() {
        var len = table.$('tr').length;
        var column = table.settings().init().columns;
        var result = '[{"';
        var qtParking = 0;
        // Monta JSON para atribuição no campo #services
        for (let i = 0; i < len; i++) {
            for (let j = 0; j < 7; j++) {
                var end = '","';
                
                if (column[j].name.toLowerCase() == 'excluido') {
                    end = '"';
                }

                if (column[j].name.toLowerCase() == 'tipo') {
                    var isParking = table.cell({row:i, column:j}).data().toLowerCase() == 'estacionamento';
                    var isDeleted = table.cell({row:i, column:6}).data() == 'true';

                    if (isParking && !isDeleted) {
                        qtParking ++;
                    }
                }
                result += column[j].name + '":"' + table.cell({row:i, column:j}).data() + end;
            }

            if (len - 1 == i ) {
                result += '}';
            } else {
                result += '},{"';
            }
        }
        result += ']';

        $("#services").val(result);
        var ret = true;
        var json = JSON.parse($("#services").val());
        var hasService = json[0]['id'] != ''
        var value = parseFloat($("#valor_recebido").val());
        var liquidValue = parseFloat($("#valor_liquido").val());
        var discount = parseFloat($("#desconto").val());

        if (value < liquidValue) {
            var missingValue = liquidValue - value;
            toastr.warning('<b style="color:black; font-size:18px">Faltam R$ '+ missingValue +'</b>');
            ret = false;
        } else if (discount > liquidValue) {
            toastr.warning('<b style="color:black; font-size:18px">O desconto de R$ '+ discount +' é maior que o valor líquido de R$ '+ liquidValue +'</b>');
            ret = false;
        } else if (qtParking == 0 || !hasService) {
            toastr.warning('<b style="color:black; font-size:18px;">Preencha ao menos 1 serviço do tipo estacionamento.</b>');
            ret = false;
        }else if (qtParking > 1) {
            toastr.warning('<b style="color:black; font-size:18px">Permitido apenas 1 serviço do tipo estacionamento.</b>');
            ret = false;
        }

        return ret;
    } );

    var originDesc = 0;

    $("#desconto").on('keydown', function () { 
        originDesc = parseFloat($(this).val());
    });

    $("#desconto").on('keyup', function () {
        var totalValue = parseFloat($("#valor_total").val());
        var value = parseFloat($(this).val());

        if (totalValue > value && originDesc != value && value > -1) {
            $("#valor_liquido").val(totalValue - value);
        }

        var reciveValue = parseFloat($("#valor_recebido").val());
        calcChange(reciveValue);
    });

    $("#valor_recebido").on('keyup', function () { 
        var reciveValue = parseFloat($("#valor_recebido").val());
        calcChange(reciveValue);
    });
} );

function calcChange(value) {
    var reciveValue = parseFloat(value);
    var liquidValue = parseFloat($("#valor_liquido").val());
    var change = reciveValue - liquidValue;

    if (change < 0) {
        $("#troco").val(0);
    } else if (change) {
        $("#troco").val(change);
    } else {
        $("#troco").val(0);
    }
}
function setTimerEntry() {
    $("#entrada").val(getTime);
    setInterval(
        function () {
            $('#entrada').val(getTime);
        }, 1000
    );
}

function setTimerExit() {
    $("#saida").val(getTime);
}

function calcExit() {
    var totalValue = parseFloat($("#valor_total").val());
    var valueHour = parseFloat($("#valor_hora").val());
    var entry = $("#entrada").val().replace('/', '-');
    var exit = $("#saida").val().replace('/', '-');

    var hour = difDate(exit, entry);

    if (hour[0] < 1) {
        if (hour[1] > 15) {
            $("#valor_total").val(totalValue + (valueHour *  1));
            $("#valor_liquido").val(totalValue + (valueHour *  1));
        }
    } else {
        $("#valor_total").val(parseFloat(totalValue + (valueHour *  parseInt(hour[0]))));
        $("#valor_liquido").val(parseFloat(totalValue + (valueHour *  parseInt(hour[0]))));
    }

    $("#tempo_permanencia").val(parseInt(hour[0]) + "h " + parseInt(hour[1]) + "m");

}

function difDate(today, day){
    today  = moment(today.replace('/', '-'));
    day = moment(day.replace('/', '-'));

    var duracao = moment.duration(today.diff(day));
    var horas = duracao.get('hour');
    var minutos = duracao.get('minute');;
    return [horas, minutos];
}

function getTime() {
    var dNow = new Date();
    var year = dNow.getFullYear();
    var month = (dNow.getMonth()+1);
    var day = dNow.getDate();
    var hour = dNow.getHours();
    var minute = dNow.getMinutes();
    var second = dNow.getSeconds();

    if (day.toString().length == 1) {
        day = '0' + day.toString();
    };

    if (month.toString().length == 1) {
        month = '0' + month.toString();
    };

    if (hour.toString().length == 1) {
        hour = '0' + hour.toString();
    };

    if (minute.toString().length == 1) {
        minute = '0' + minute.toString();
    };

    if (second.toString().length == 1) {
        second = '0' + second.toString();
    };

    var localdate = year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + second;
    return localdate;
}
