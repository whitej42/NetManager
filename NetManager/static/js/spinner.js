
const spinnerBox = document.getElementById('spinner-box')

$.ajax({
    type:'GET',
    url: '/devices',
    success: function (response){
        console.log(response)
    }
})
