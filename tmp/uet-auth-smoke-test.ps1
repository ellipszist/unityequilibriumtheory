$email = 'cascade-smoke-' + [guid]::NewGuid().ToString('N').Substring(0, 8) + '@example.com'
$password = 'SmokePass123!'

$signup = Invoke-WebRequest -UseBasicParsing -Uri 'http://localhost:3010/api/auth-uet/signup' -Method POST -ContentType 'application/json' -Body (@{
  email = $email
  password = $password
  name = 'Cascade Smoke'
} | ConvertTo-Json -Compress)

$session = New-Object Microsoft.PowerShell.Commands.WebRequestSession
$csrf = ((Invoke-WebRequest -UseBasicParsing -WebSession $session -Uri 'http://localhost:3010/api/auth/csrf').Content | ConvertFrom-Json).csrfToken

$signinBody = 'email=' + [uri]::EscapeDataString($email) + '&password=' + [uri]::EscapeDataString($password) + '&csrfToken=' + [uri]::EscapeDataString($csrf) + '&callbackUrl=' + [uri]::EscapeDataString('http://localhost:3010/community')

$signin = Invoke-WebRequest -UseBasicParsing -WebSession $session -Uri 'http://localhost:3010/api/auth/callback/credentials?json=true' -Method POST -ContentType 'application/x-www-form-urlencoded' -Body $signinBody
$me = Invoke-WebRequest -UseBasicParsing -WebSession $session -Uri 'http://localhost:3010/api/auth/check-user'

Write-Output ('EMAIL=' + $email)
Write-Output ('SIGNUP=' + $signup.Content)
Write-Output ('SIGNIN=' + $signin.Content)
Write-Output ('ME=' + $me.Content)
