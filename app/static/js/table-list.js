$(document).ready( function () {
    var table = $('#table').DataTable({
        responsive: true,
        scrollY: "50vh",
        scrollCollapse: true
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