lastRow = -1;

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
            {'name': 'excluido', 'visible': false}
        ]
    });

    $('#entrada').val(getTime)
    var timer = setInterval(timerEntrada, 1000);

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
        var columnIdx = table.cell(this).index().column

        if ($('td > input').length == 0) {

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
                if (columnIdx == 0) {
                    var originContent = $(this).text()
                    var input = $('<input/>', {type:'text', value: originContent})

                    $(this).html(input.bind('blur keydown', function (e){
                        var keyCode = e.which;
                        var object = $(this);

                        if (keyCode == 27) {
                            $(this).parent().html(originContent);
                        }else if (keyCode == 13 || e.type == 'blur') {
                            var newContent = $(this).val();

                            if (newContent != originContent) {
                                // Busca informações do serviço no banco
                                $.ajax({
                                    type: "GET",
                                    url: "/busca-servico/"+newContent,
                                    data: '',
                                    dataType: "dataType",
                                    complete: function(response) {
                                        //atribui as informações resgatadas nas células da tabela
                                        if (response.status == 200) {
                                            var service = JSON.parse(response.responseText)
                                            object.parent().html(newContent);
                                            table.cell({row:rowIdx, column:0}).data(service.id);
                                            table.cell({row:rowIdx, column:1}).data(service.nome);
                                            table.cell({row:rowIdx, column:2}).data(service.descricao);
                                            table.cell({row:rowIdx, column:3}).data(service.preco);
                                            table.cell({row:rowIdx, column:4}).data(service.tipo);
                                            table.cell({row:rowIdx, column:5}).data(false); 

                                            var totalValue = parseFloat($("#valor_total").val()) + service.preco;
                                            $("#valor_total").val(totalValue.toString());
                                            
                                        } else {
                                            //console.log(response);
                                        }
                                    }
                                });
                                return false;
                            } else {
                                object.parent().html(originContent);
                            }
                        }
                    }));

                    $(this).children().select();
                }
            }

            lastRow = rowIdx;
        }
    } );
    
    $('#removeService').click( function () {
        var info = table.page.info();
        var rowstot = info.recordsDisplay;
        var index = table.row('.bg-selected').index();
        
        if (rowstot > 1)  {
            table.cell({row:index, column:5}).data(true);
            
            var totalValue = $('#valor_total').val();
            var serviceValue = table.cell({row:index, column:3}).data();

            $('#valor_total').val(totalValue - serviceValue);

            $( table.row(index).nodes() ).removeClass( 'bg-selected' );
            table.search( false ).draw();
            
            info = table.page.info();
            rowstot = info.recordsDisplay;

            if (index >= rowstot) {
                $( table.row(index - 1).nodes() ).addClass( 'bg-selected' );
            }
        }
        table.cell({row:index, column:5}).data();
    } );
    
    $('#addService').on('click', function () {
        lastRow = table.row(':last').data();

        //adiciona apenas se a ultima linha estiver preenchida
        if (lastRow[1]) {
            table.row.add( [
                '',
                '',
                '',
                0,
                '',
                false
            ] ).draw( false );
        }
    } );

    $('#buttonSubmit').click( function() {
        var len = table.$('tr').length;
        var column = table.settings().init().columns;
        var result = '[{"';
        
        // Monta JSON para atribuição no campo #services
        for (let i = 0; i < len; i++) {
            for (let j = 0; j < 6; j++) {
                var end = '","';
                
                if (j == 5) {
                    end = '"';
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
        var json = JSON.parse($("#services").val());
        var hasService = json[0]['id'] != ''

        if (hasService) {
            clearInterval(timer);
        }

        return hasService;
    } );

    
} );

function timerEntrada() {
    $('#entrada').val(getTime)
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

    if (minute.toString().length == 1) {
        minute = '0' + minute.toString();
    };

    if (second.toString().length == 1) {
        second = '0' + second.toString();
    };

    var localdate = year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + second;
    return localdate;
}
