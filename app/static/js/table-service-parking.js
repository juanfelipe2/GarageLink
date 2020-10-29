lastRow = -1;

$(document).ready( function () {
    var table = $('#serviceParking').DataTable({
        responsive: true,
        scrollY: "50vh",
        scrollCollapse: true,
        searching: false,
        ordering: false,
        lengthChange: false,
        paging: false,
        bInfo: false,
        columns: [
            {'name': 'id'},
            {'name': 'nome'},
            {'name': 'descricao'},
            {'name': 'preco'},
            {'name': 'tipo'}
        ]

    });
    
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
                                $.ajax({
                                    type: "GET",
                                    url: "/busca-servico/"+newContent,
                                    data: '',
                                    dataType: "dataType",
                                    complete: function(response) {
                                        if (response.status == 200) {
                                            var service = JSON.parse(response.responseText)
                                            object.parent().html(newContent);
                                            table.cell({row:rowIdx, column:0}).data(service.id);
                                            table.cell({row:rowIdx, column:1}).data(service.nome);
                                            table.cell({row:rowIdx, column:2}).data(service.descricao);
                                            table.cell({row:rowIdx, column:3}).data(service.preco);
                                            table.cell({row:rowIdx, column:4}).data(service.tipo);
                                        } else {
                                            console.log(response);
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
        var len = table.$('tr').length - 1;
        var index = table.row('.bg-selected').index()

        if (index >= len) {
            index = table.row('.bg-selected').index() - 1
        }

        if (len > 0)  {
            table.row('.bg-selected').remove().draw( false );
            $( table.row(index).nodes() ).addClass( 'bg-selected' );
        }
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
                ''
            ] ).draw( false );
        }
    } );
    

    $('#buttonSubmit').on('keydown', function(e) { 
        var keyCode = e.which;
        if (keyCode == 13) {
            return false;
         }
    })

    $('#buttonSubmit').click( function() {
        var len = table.$('tr').length;
        var column = table.settings().init().columns;
        var result = '[{"';
        
        for (let i = 0; i < len; i++) {
            for (let j = 0; j < 5; j++) {
                var middle = '":"';
                var end = '","';
                
                if (j == 3) {
                    middle = '":';
                    end = ',"';
                }else if (j == 4) {
                    middle = '":"';
                    end = '"';
                }

                result += column[j].name + middle + table.cell({row:i, column:j}).data() + end;
            }

            if (len - 1 == i ) {
                result += '}';
            } else {
                result += '},{"';
            }
        }
        result += ']';

        $("#services").val(result);

    } );

} );
