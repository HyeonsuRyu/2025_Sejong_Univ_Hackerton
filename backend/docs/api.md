📌 API 문서
Base URL
https://hsryu.pe.kr:10443/api/



# 사용자 계정 관련
## 회원가입 (Register)
- URL: /user/register/
- Method: POST
- Auth: 필요 없음 (AllowAny)
- Request Body
{
  "username": "example",
  "password": "AaBb1123",
  "password2": "AaBb1123",
  "email": "example@example.com",
  "nickname": "nick"
}
- Response (201 Created)
{
  "id": 1,
  "username": "example",
  "email": "example@example.com"
}
- Error (400 Bad Request)
{
  "password": ["Password fields didn't match."]
}



## 로그인 (Login)
- URL: /user/login/
- Method: POST
- Auth: 필요 없음 (AllowAny)
- Request Body
{
  "username": "example",
  "password": "AaBb1123"
}
- Response (200 OK)
{
  "token": "<token value>"
}
- Error (400 Bad Request)
{
  "error": "Unable to log in with provided credentials."
}



## 로그인 회원 정보 (My Profile)
- URL: /user/profile/me/
- Method: GET
- Auth: 필요 (Authorization: Token <토큰값>)
- Request Header
Authorization: Token <token value>
- Response (200 OK)
{
  "nickname": "example"
}
- Error (404 Not Found)
{
  "detail": "Profile not found."
}



## 닉네임으로 유저 정보 조회 (Public Profile)
- URL: /user/profile/<username>/
- Method: GET
- Auth: 필요 없음 (AllowAny)
- Response (200 OK)
{
  "nickname": "다른유저닉네임"
}
- Error (404 Not Found)
{
  "detail": "Not found."
}




