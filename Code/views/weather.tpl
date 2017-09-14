<!DOCTYPE HTML5>
<html>
<head>
<meta http-equiv="refresh" content="5" >
<title>weatherstation</title>
  <style type="text/css">
  h1 {
	font-family: Calibri;
	font-stretch:ultra-expanded;
	font-variant: small-caps;
	font-size: xxx-large;}
  h2 {
	font-family: Calibri;
	font-size: xx-large;
	font-weight: 300}
  body {
    color: #FFFFFF;
    background-color: #2E9AFE;
	text-align: center;
	font-family: Calibri;
	font-size: x-large;
	font-weight: 200;}
  </style>
</head>
<body>
	<h1>Weatherstation</h1>
	<br />
	<h2>This pages shows you the current room temperature, the humidity and the pressure.</h2>
	<br />
	<p>Temperature: {{temp}} °C</p>
	<p><img src='/img/temp.png' alt="Temperature", width="40%" /></p>
	<p>Presure: {{pres}} hPa</p>
	<p><img src="img/pres.png" alt="Presure", width="40%" /></p>
	<p>Humidity: {{hum}} %</p>
	<p><img src="img/hum.png" alt="Humidity", width="40%" /></p>
</body>
</html>