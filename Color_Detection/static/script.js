$(function(){
	$('#submit').click(function(){
		var message_pri = $(".color:checked").val();
        var image = document.getElementById('file-up');
        var file = image.files[0];
        if(!file){
            alert('Must Select Image');
        }else{
            fr = new FileReader();
            fr.onload = function(e) {
                var data_send = {
                    color: message_pri,
                    image: e.target.result
                }
                $.ajax({
                    url: '/detect',
                    type: 'POST',
                    contentType: 'application/json',
                    dataType: "json",
                    success: function (data) {
                        var src = data.image;
                        var prev = document.getElementById("file-up-preview");
                        prev.src = src;
                        prev.style.display = "block";
                    },
                    data: JSON.stringify(data_send)
                });
            }
            fr.readAsDataURL(file);
        }
	});
});