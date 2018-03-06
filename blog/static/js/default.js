function login()
{
    username = $("#username").val();
    password = $("#password").val();
    var formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);
    $.ajax({
        url: '/login',
        data: formData,
        type: "POST",
        contentType: false,
        async: false,
        processData: false,
        success: function(res){
            if (res == "success"){
                var s = new String(window.location.href);
                if (s.indexOf("/signup")==-1){
                    location.reload();
                }
                else{
                    window.location.href="/";
                }
            }
            else if (res == "username"){
                alert("用户名不存在");
            }
            else if (res == "password"){
                alert("密码错误(用户名存在)");
            }
            else{
                alert("未知错误");
            }
        },
        fail: function(){
            alert("未知错误");
        }
    });
};

function logout(){
    $.get('/logout', function(){
        var s = new String(window.location.href);
        if (s.indexOf("/edit")==-1){
            location.reload();
        }
        else{
            window.location.href="/";
        }
    });
};

function signup()
{
    nickname = $("#nnickname").val();
    username = $("#nusername").val();
    password = $("#npassword").val();
    email_addr = $("#email_addr").val();
    var formData = new FormData();
    formData.append("nickname", nickname);
    formData.append("username", username);
    formData.append("password", password);
    formData.append("email_addr", email_addr);
    $.ajax({
        url: '/signup',
        data: formData,
        type: "POST",
        contentType: false,
        async: false,
        processData: false,
        success: function(res){
            if (res == "success"){
                var s = new String(window.location.href);
                if (s.indexOf("/signup")==-1){
                    location.reload();
                }
                else{
                    window.location.href="/";
                }
            }
            else{
                alert("用户名已存在");
            }
        },
        fail: function(){
            alert("未知错误");
        }
    });
};

//This is a pen based off of Codewoofy's eyes follow mouse. It is just cleaned up, face removed, and then made to be a little more cartoony. https://codepen.io/Codewoofy/pen/VeBJEP

document.onmousemove = function(event) {
  var eye = $(".eye");
  var x = (eye.offset().left) + (eye.width() / 2);
  var y = (eye.offset().top) + (eye.height() / 2);
  var rad = Math.atan2(event.pageX - x, event.pageY - y);
  var rot = (rad * (180 / Math.PI) * -1) + 180;
  eye.css({
    '-webkit-transform': 'rotate(' + rot + 'deg)',
    '-moz-transform': 'rotate(' + rot + 'deg)',
    '-ms-transform': 'rotate(' + rot + 'deg)',
    'transform': 'rotate(' + rot + 'deg)'
  });
};