# 배포 가이드

이 문서는 메모짱의 프로덕션 배포 시 고려 사항을 정리합니다.

## 환경 변수
- `DEBUG=false`
- `SECRET_KEY` (강력한 랜덤값)
- `ALLOWED_HOSTS` (도메인 또는 IP)
- `DATABASE_URL` (예: Postgres 등 프로덕션 DB)

## 정적 파일
```
python manage.py collectstatic --noinput
```

## WSGI 예시(Gunicorn)
- Ubuntu 예시
```
pip install gunicorn
export DJANGO_SETTINGS_MODULE=memojjang.settings
export DEBUG=false
export SECRET_KEY=your-secret
export ALLOWED_HOSTS=your.domain
export DATABASE_URL=postgres://user:pass@host:5432/dbname

gunicorn memojjang.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

## 리버스 프록시(Nginx) 개요
- /static은 Nginx에서 정적 서빙
- /는 Gunicorn으로 프록시 패스

## 데이터베이스
- 관리형 DB 사용 권장
- 연결 정보는 반드시 환경 변수로 주입

## 모니터링/로깅
- Access/Error 로그 수집
- 애플리케이션 예외 로깅 구성
