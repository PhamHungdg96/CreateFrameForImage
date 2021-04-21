function get_data(_data, callback){
    var result=''
    $.ajax({
        url:"http://localhost:5000/framed_prints",
        type:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        data:_data,
        success:function(result){
            callback(result)
        }, 
        error:function(err){

        }
    })
}
$(document).ready(function(){
    var productPreviewImage=$('#productPreviewImage');
    var url_image=productPreviewImage.attr("data-url-image");
    var elem = document.createElement("img");
    elem.setAttribute("width", "100%");
    elem.setAttribute("height", "auto");
    productPreviewImage.append(elem)
    get_data(JSON.stringify({
        "url":"http://127.0.0.1:5000/static/img.jpg",
        "prints":{
            "zoom":1
        },
        "frame":{
            "name":"frame4",
            "size":30
        },
        "padding":{
            'size':Number($('#mat_value').val())*96,
            "color":"255,255,255"
        }
        }),(result)=>{
            elem.src=result
        })
    $('#zoom_value').on('change', function(){
        var size=$('#prints_value').val().split('*')
        get_data(JSON.stringify({
            "url":"http://127.0.0.1:5000/static/img.jpg",
            "prints":{
                "zoom":1+$('#zoom_value').val()/10,
                "imgW":Number(size[0])*100,
                "imgH":Number(size[1])*100
            },
            "frame":{
                "name":"frame4",
                "size":30
            },
            "padding":{
                'size':Number($('#mat_value').val())*96,
                "color":"255,255,255"
            }
            }),(result)=>{
                elem.src=result
            })
    })
    $('#prints_value').on('change', function(){
        var size=$('#prints_value').val().split('*')
        get_data(JSON.stringify({
            "url":"http://127.0.0.1:5000/static/img.jpg",
            "prints":{
                "zoom":1+$('#zoom_value').val()/10,
                "imgW":Number(size[0])*100,
                "imgH":Number(size[1])*100
            },
            "frame":{
                "name":"frame4",
                "size":30
            },
            "padding":{
                'size':Number($('#mat_value').val())*96,
                "color":"255,255,255"
            }
            }),(result)=>{
                elem.src=result
            })
    })
    $('#mat_value').on('change', function(){
        var size=$('#prints_value').val().split('*')
        get_data(JSON.stringify({
            "url":"http://127.0.0.1:5000/static/img.jpg",
            "prints":{
                "zoom":1+$('#zoom_value').val()/10,
                "imgW":Number(size[0])*100,
                "imgH":Number(size[1])*100
            },
            "frame":{
                "name":"frame4",
                "size":30
            },
            "padding":{
                'size':Number($('#mat_value').val())*96,
                "color":"255,255,255"
            }
            }),(result)=>{
                elem.src=result
            })
    })
})