userData = Telegram.WebApp.initDataUnsafe.user || {};

document.getElementById("userId").value = userData.id;
document.getElementById('userName').value = userData.username;

document.getElementById('webview_data').innerHTML=JSON.stringify(userData, null, 2);
document.getElementById('welcome_by_name').innerHTML="Hello " + userData.first_name;