$(document).ready(function (){
    $('#sendComment').click(function (){
        var btn = $(this);
        $.ajax(btn.data('url'), {
            'type': 'POST',
            'async': true,
            'dataType': 'json',
            'data': {
                'comment': $('#comment').val(),
            },
            'success': function (response){
               var comments = document.getElementById('comments');
               comments.innerHTML = `<p>${$('#comment').val()}</p>` + comments.innerHTML;
               $('#comment').val('');
            }
        });
    });

    $('.btnDelete').click(function (){
        var btn = $(this);
        document.getElementById('id').outerHTML = '';
    })
})
