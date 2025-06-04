-- 사용자 정보 테이블: 모든 사용자(회원/관리자 등) 계정 정보 관리
CREATE TABLE users (
    id SERIAL PRIMARY KEY,                    -- 사용자 고유번호 (자동증가)
    username VARCHAR(50) UNIQUE NOT NULL,     -- 로그인용 ID (중복 불가)
    password VARCHAR(256) NOT NULL,           -- 암호화된 비밀번호
    email VARCHAR(100) UNIQUE,                -- 이메일 (중복 불가, 선택 입력)
    user_type VARCHAR(30),                    -- 사용자 유형 (학생/공공기관/사업자/기타)
    is_active BOOLEAN DEFAULT TRUE,           -- 계정 활성화 여부 (탈퇴, 비활성화 지원)
    is_admin BOOLEAN DEFAULT FALSE,           -- 관리자 계정 여부 (추후 관리자 권한 분리 용)
    created_at TIMESTAMP DEFAULT NOW(),       -- 가입 일시
    last_login TIMESTAMP                      -- 마지막 로그인 일시
);

-- 사용자 역할(권한) 테이블: 한 명이 여러 역할을 가질 수 있도록 확장 (ex. 관리자+정책관리자 등)
CREATE TABLE user_roles (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),         -- users 테이블 참조(외래키)
    role VARCHAR(30),                         -- 역할명 (ex. ADMIN, POLICY, MEMBER 등)
    assigned_at TIMESTAMP DEFAULT NOW()       -- 역할 부여 일시
);

-- 지역 정보 테이블: 지도/주소 등 위치정보 관리. 법정동/행정동/위경도/계층구조 지원
CREATE TABLE region_info (
    region_code VARCHAR(20) PRIMARY KEY,      -- 법정동/행정동 코드
    region_name VARCHAR(50) NOT NULL,         -- 지역명(시군구/읍면동)
    parent_code VARCHAR(20),                  -- 상위 행정구역 코드 (ex. 구, 시, 도)
    latitude DOUBLE PRECISION,                -- 위도
    longitude DOUBLE PRECISION                -- 경도
);

-- 사고 상세 정보 테이블: 지도 마커, 상세보기, 분석용 상세 데이터 저장
CREATE TABLE accident_detail (
    id SERIAL PRIMARY KEY,
    region_code VARCHAR(20) REFERENCES region_info(region_code),  -- 사고 위치(지역 코드)
    region_name VARCHAR(50),              -- 사고 위치(지역명)
    latitude DOUBLE PRECISION,            -- 사고 위도
    longitude DOUBLE PRECISION,           -- 사고 경도
    risk_level VARCHAR(10),               -- 위험도 등급(고/중/저 등)
    accident_count INT,                   -- 해당 지역 사고 건수
    elderly_ratio FLOAT,                  -- 해당 지역 고령자 비율
    accident_type_stats JSONB,            -- 사고 유형별 분포 (예시: {"차대차": 8, "보행자": 3})
    hourly_stats JSONB,                   -- 시간대별 사고 통계 (예시: {"0":1, "2":2, ...})
    road_env VARCHAR(100),                -- 도로 환경 키워드(예: 교차로, 횡단보도 등)
    poi JSONB,                            -- 주변 시설/정책 등 (예: {"CCTV":2, "횡단보도":true})
    report_file VARCHAR(255),             -- 리포트 다운로드 파일 경로
    created_at TIMESTAMP DEFAULT NOW()    -- 데이터 생성 일시
);

-- 사고 집계 테이블: 분석/모델링/통계용 데이터 (DuckDB/ML용과 구조 동일)
CREATE TABLE accident_summary (
    id SERIAL PRIMARY KEY,
    region VARCHAR(50),                   -- 시군구명
    elderly_ratio FLOAT,                  -- 고령자 비율
    year INT,                             -- 연도
    month INT,                            -- 월(필요시, 없으면 NULL)
    hour INT,                             -- 기준 시간 (0,2,4,...)
    accident_count INT                    -- 사고 건수
);

-- 지도 테마/토글 기록 테이블: 회원별 최근 조회 테마, 향후 로그분석·추천·설정 등 확장 가능
CREATE TABLE map_theme (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),         -- 회원 ID
    selected_theme VARCHAR(50),               -- 선택 테마 (위험도/사고유형/시간대/실제사고유무)
    selected_at TIMESTAMP DEFAULT NOW()       -- 선택 일시
);

-- 데이터 다운로드 기록 테이블: 어떤 사용자가 어떤 지역 데이터 내려받았는지 기록 (정책기관, 이용자별 통계 활용 가능)
CREATE TABLE download_log (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),         -- 회원 ID
    region_code VARCHAR(20),                  -- 다운로드한 지역 코드
    downloaded_at TIMESTAMP DEFAULT NOW(),    -- 다운로드 일시
    file_type VARCHAR(20)                     -- 파일 종류 (csv, excel 등)
);

-- 리포트 파일 관리 테이블: 각 지역별 리포트 PDF/CSV 등 파일경로 저장 (다운로드/공유 지원)
CREATE TABLE report_file (
    id SERIAL PRIMARY KEY,
    region_code VARCHAR(20),                  -- 지역 코드
    file_path VARCHAR(255),                   -- 파일 저장 경로
    created_at TIMESTAMP DEFAULT NOW()
);

-- 관리자/시스템 로그: 관리자 행위/데이터 변경/모델학습 등 기록 (향후 확장, 감시/감사)
CREATE TABLE admin_log (
    id SERIAL PRIMARY KEY,
    admin_id INT REFERENCES users(id),        -- 관리자 ID
    action VARCHAR(100),                      -- 작업명 (ex. 데이터 업로드, 파이프라인 제어 등)
    target_table VARCHAR(50),                 -- 대상 테이블명
    log_detail JSONB,                         -- 상세 내용(JSON 형태)
    created_at TIMESTAMP DEFAULT NOW()
);

-- 사용자 행동 로그 테이블
-- 서비스 내 사용자의 각종 행동(로그인, 데이터 조회, 다운로드 등) 기록용
CREATE TABLE user_log (
    log_id SERIAL PRIMARY KEY,                -- 로그 고유 식별자(자동 증가)
    user_id INTEGER REFERENCES user(user_id), -- 행동한 사용자 (비회원이면 NULL)
    action VARCHAR(100),                      -- 수행한 행동 유형 (예: login, view_detail, download)
    target VARCHAR(100),                      -- 대상 데이터/기능명 (예: region_download, map_view 등)
    detail TEXT,                              -- 상세 정보(파라미터, 오류 내용 등 선택적 기록)
    ip_address VARCHAR(50),                   -- 사용자 접속 IP
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- 로그 기록 시각
);

-- 서비스 정책 및 공지/약관 관리 테이블
-- 서비스 이용약관, 개인정보처리방침, 안내 공지 등 정책성 문서 관리용
CREATE TABLE policy_notice (
    policy_id SERIAL PRIMARY KEY,         -- 정책 고유 식별자(자동 증가)
    title VARCHAR(100),                   -- 정책 제목(예: 개인정보처리방침)
    content TEXT,                         -- 정책 내용 (HTML 혹은 plain text)
    version VARCHAR(20),                  -- 정책 버전 (예: v1.0)
    is_active BOOLEAN DEFAULT TRUE,       -- 현재 서비스 중인 정책 여부
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- 등록 시각
);

-- 메인화면 배너 관리 테이블
-- 주요 공지, 이벤트, 배너(이미지) 등 사용자에게 노출할 컨텐츠 관리용
CREATE TABLE main_banner (
    banner_id SERIAL PRIMARY KEY,         -- 배너 고유 식별자(자동 증가)
    image_url VARCHAR(300),               -- 배너 이미지 경로(URL)
    link_url VARCHAR(300),                -- 클릭 시 이동할 URL
    description VARCHAR(200),             -- 배너 간단 설명 (에디터가 보는 용도)
    is_active BOOLEAN DEFAULT TRUE,       -- 현재 노출중인 배너인지 여부
    start_date DATE,                      -- 배너 노출 시작일
    end_date DATE,                        -- 배너 노출 종료일
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- 등록 시각
);


-- 보조성 테이블 

-- [에러/시스템 로그 기록 테이블]
CREATE TABLE error_log (
    error_id SERIAL PRIMARY KEY,              -- 에러 로그 고유 ID
    user_id INTEGER REFERENCES user(user_id), -- 에러를 유발한 사용자 (비회원이면 NULL)
    error_type VARCHAR(100),                  -- 에러 분류 (API, DB, 권한 등)
    message TEXT,                             -- 에러 메시지(간단 설명)
    stack_trace TEXT,                         -- 상세 오류 내용(백엔드 로그 등)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- 에러 발생 일시
);
