# 메모짱 (Django)

간단한 메모장 웹 애플리케이션. 로그인/회원가입, 메모 CRUD, 공개/비공개 지원.

## 빠른 시작

1) 가상환경 및 설치

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2) 환경 변수 준비

`.env` 파일 생성 (예시는 `.env.example` 참고):

```dotenv
DEBUG=true
SECRET_KEY=replace-with-a-secure-random-string
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

3) DB 마이그레이션 & 실행

```powershell
python manage.py migrate
python manage.py runserver
```

## 테스트

```powershell
pip install -r requirements-dev.txt
python manage.py test -v 2
```

## 코드 품질(선택)

```powershell
pip install -r requirements-dev.txt
ruff check .
black --check .
```

## 배포 참고
- `DEBUG=false`, 강력한 `SECRET_KEY` 설정
- 정적파일: `python manage.py collectstatic`
- 환경 변수로 DB/시크릿 관리(`DATABASE_URL`, `ALLOWED_HOSTS` 등)

## 보안 노트
- 세션/CSRF HttpOnly, XSS/NoSniff 플래그 기본 활성화 (환경변수로 조정)
- 비공개 메모는 소유자 외 404 처리

## 라이선스
본 저장소의 라이선스 정책이 정해지지 않았다면 사용 전 확인 바랍니다.