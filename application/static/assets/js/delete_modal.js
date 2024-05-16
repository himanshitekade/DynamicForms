function confirmDelete(id){
    console.log(id)
    Swal.fire({
    title: 'Are you sure?',
    text: "You won't be able to revert this!",
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'Yes, delete it!'
        }).then((result) => {
        console.log(result)
        /* Read more about isConfirmed, isDenied below */
        if (result.isConfirmed) {
            deleteObject(id);
        } else if (result.isDenied){
            
        }
    });
    }

function deleteObject(id){
    var id = id
    var endpoint =  $("#delete-obj").attr("data-url");
    $.ajax({
        method:'GET',
        url: endpoint,
        data:{
            id:id,
            action:"delete",
        },      
        success:function(data){
            if(data.status === 'Deleted'){
                
                Swal.fire('Deleted!', 'Requested data has been deleted.', 'success')
                .then((result) => {
                    /* Read more about isConfirmed, isDenied below */
                    if (result.isConfirmed) {
                        location.reload()
                    } else {
                        location.reload()
                    }
                });

            }else
            {
                Swal.fire('Not Deleted!', data.message, 'error');
                }
            
            }

    })
}
