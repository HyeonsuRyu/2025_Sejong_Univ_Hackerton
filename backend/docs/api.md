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

# AI 호출
- URL: /api/OpenRouter/analyze/
- Method: POST
- AUTH: 원래는 필요한데 일단 AllowAny
- Request Body
{ 
	"session_id": "sess-123", // 아무 값이나 고정해서 사용
    "api_key": "sk-XXXXXXXXXXX",
    "text": "~~~~~~~~~~~~~~~~~~~~~~~~"
}
- Response (200 OK)
{
	"reply": "죄송합니다. 현재 시스템에서 AI 윤리 주제 선정에 대한 도구 추천을 제공할 수 없는 상태입니다. 하지만, 주제를 선정하는 데 도움이 될 수 있는 몇 가지 도구를 추천해 드리겠습니다.\n\n### 도구 추천\n\n1. **Free Version (무료 도구)**:\n   - **Google Scholar**: 학술 자료를 검색하여 AI 윤리와 관련된 최신 연구를 찾아볼 수 있습니다.\n\n2. **Best Performance (최고 성능 도구)**:\n   - **JSTOR**: 다양한 학술 논문을 제공하며, AI 윤리와 관련된 깊이 있는 자료를 찾는 데 유용합니다. (일부 자료는 유료)\n\n3. **Cost-Efficiency (가성비 도구)**:\n   - **ResearchGate**: 연구자들이 자신의 논문을 공유하는 플랫폼으로, 무료로 다양한 자료를 찾을 수 있습니다.\n\n이 도구들을 활용하여 AI 윤리 주제를 선정하는 데 도움이 되길 바랍니다. 추가적인 질문이나 도움이 필요하시면 언제든지 말씀해 주세요!"
}