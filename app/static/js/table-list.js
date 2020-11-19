$(document).ready( function () {
    var table = $('#table').DataTable({
        responsive: true,
        scrollY: "50vh",
        scrollCollapse: true,
        "language": {
            "sEmptyTable":   "Não foi encontrado nenhum registo",
            "sLoadingRecords": "A carregar...",
            "sProcessing":   "A processar...",
            "sLengthMenu":   "Mostrar _MENU_ registos",
            "sZeroRecords":  "Não foram encontrados resultados",
            "sInfo":         "Mostrando de _START_ até _END_ de _TOTAL_ registos",
            "sInfoEmpty":    "Mostrando de 0 registros",
            "sInfoFiltered": "(filtrado de _MAX_ registos no total)",
            "sInfoPostFix":  "",
            "sSearch":       "Procurar:",
            "sUrl":          "",
            "oPaginate": {
                "sFirst":    "Primeiro",
                "sPrevious": "Anterior",
                "sNext":     "Seguinte",
                "sLast":     "Último"
            },
            "oAria": {
                "sSortAscending":  ": Ordenar colunas de forma ascendente",
                "sSortDescending": ": Ordenar colunas de forma descendente"
            }
        }
    });
    
    $('#table tbody')
        .on( 'mouseenter mouseleave', 'td', function (e) {
            var colIdx = table.cell(this).index().row;

            if (e.type == 'mouseenter') {
                $( table.rows().nodes() ).removeClass( 'bg-grey' );
                $( table.row( colIdx ).nodes() ).addClass( 'bg-grey' );
            } else {
                $( table.rows().nodes() ).removeClass( 'bg-grey' );
            }
        } );
} );