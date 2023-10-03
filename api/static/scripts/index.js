userData = Telegram.WebApp.initDataUnsafe.user || {};

document.getElementById("userId").value = userData.id;
document.getElementById('userName').value = userData.username;
document.getElementById('firstName').value = userData.first_name;
document.getElementById('lastName').value = userData.last_name;
document.getElementById('isBot').value = userData.is_bot;
document.getElementById('allowWrite').value = userData.allows_write_to_pm;

document.getElementById('webview_data').innerHTML=JSON.stringify(userData, null, 2);
document.getElementById('welcome_by_name').innerHTML="Hello 👋, " + userData.first_name;

// document.getElementById("waiting_msg").innerHTML = "Hi " + userData.first_name+ " approval is sent to admin please be patient 😊."