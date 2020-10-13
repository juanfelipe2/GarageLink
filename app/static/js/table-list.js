$(document).ready( function () {
    var table = $('#table').DataTable({
        responsive: true
    });
    
    $('#table tbody')
        .on( 'mouseenter', 'td', function () {
            var colIdx = table.cell(this).index().row;

            $( table.rows().nodes() ).removeClass( 'bg-gray' );
            $( table.row( colIdx ).nodes() ).addClass( 'bg-gray' );
        } );
} );