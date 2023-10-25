function confirmDeletion(url) {
    Swal.fire({
        title: '本当に削除しますか？',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: '削除',
        cancelButtonText: 'キャンセル'
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = url;
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    var taskDetailModal = document.getElementById('taskDetailModal');
    if(taskDetailModal) {
        taskDetailModal.addEventListener('show.bs.modal', function(event) {
            var button = event.relatedTarget;
            var description = button.getAttribute('data-description');
            var modalDescription = document.getElementById('taskDetailDescription');
            modalDescription.textContent = description;
        });
    }
});



document.addEventListener('DOMContentLoaded', function() {
    var deleteAccountButton = document.getElementById('deleteAccountButton');
    if(deleteAccountButton) {
        deleteAccountButton.addEventListener('click', function() {
            Swal.fire({
                title: '本当に削除しますか？',
                text: "この操作は戻せません！",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'はい、削除します！',
                cancelButtonText: 'いいえ、キャンセルします！'
            }).then((result) => {
                if (result.isConfirmed) {
                    document.getElementById('deleteAccountForm').submit();
                }
            });
        });
    }
});
 

 




  