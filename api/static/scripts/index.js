userData = Telegram.WebApp.initDataUnsafe.user || {};

document.getElementById("userId").value = userData.id;
document.getElementById('userName').value = userData.username;

document.getElementById('webview_data').innerHTML=JSON.stringify(userData, null, 2);
document.getElementById('welcome_by_name').innerHTML="Hello 👋, " + userData.first_name;

document.getElementById("waiting_msg").innerHTML = "Hi " + userData.first_name+ " approval is sent to admin please be patient 😊."