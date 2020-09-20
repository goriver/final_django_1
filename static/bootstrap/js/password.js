var passwordText = localStorage.getItem('password');
if (passwordText != "korea123") {
	alert("Access denied! Incorrect password!");
	window.location.assign("signin.html", "_self");              
}