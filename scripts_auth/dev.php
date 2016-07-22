<?php
$SCRIPTS_AUTH_KEY = "DO_NOT_USE_IN_PRODUCTION";
$REDIRECT_URL = "http://127.0.0.1:8000/login/";

if($_GET['token'] && @$_SERVER['SSL_CLIENT_S_DN_Email']) {
  $token = $_GET['token'];
  $email = $_SERVER['SSL_CLIENT_S_DN_Email'];
  $signature = hash_hmac("sha256", "$token:$email", $SCRIPTS_AUTH_KEY);
  $url = "$REDIRECT_URL?email=" . urlencode($email) . "&signature=" . urlencode($signature);
  header("Location: $url");
  exit();
}

header("Location: $REDIRECT_URL?failed=true");
exit();
