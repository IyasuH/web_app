document.getElementById('webview_data').innerHTML=JSON.stringify(window.Telegram.WebApp.initDataUnsafe.user, null, 2);
document.getElementById('welcome_by_name').innerHTML="Hello " + window.Telegram.WebApp.initDataUnsafe.user.first_name;
document.getElementById('user_id').innerHTML=window.Telegram.WebApp.initDataUnsafe.id;