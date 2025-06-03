# API 문서
## 고령자 교통사고 위험 예측 시스템 API 명세서
> 각 섹션을 클릭하여 상세 정보를 확인하세요.

<details><summary>🔐 인증 (Authentication)</summary>

- **POST** `/api/auth/login/`  
  - 설명: 사용자 로그인하여 JWT 토큰을 발급받습니다.  
  - 요청 본문 (JSON):
    ```json
    {
      "username": "사용자명",
      "password": "비밀번호"
    }
    ```
  - 응답 예시:
    ```json
    {
      "token": "eyJ0eXAi..."
    }
    ```
- **POST** `/api/auth/logout/`  
  - 설명: 토큰 만료/로그아웃
  - 헤더: `Authorization: Bearer <token>`
    ```json
    {
      "success": true
    }
    ```

</details>
