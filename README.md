## 필요한 소프트웨어

- Python 3.11.3
- Node.js 18.16.0

## 시작하는 법

git clone https://github.com/iankimdev/e-commerce.git

패키지를 설치하고 명령어를 실행하기 위해[rav]를 사용합니다. (https://github.com/jmitchel3/rav)
`rav`를 사용하지 않으려면 `rav.yaml`을 열어 사용 가능한 명령어를 확인하십시오.

_macOS/Linux Users_

```bash
python3 -m venv venv
source venv/bin/activate
venv/bin/python -m pip install pip pip-tools rav --upgrade
venv/bin/rav run installs
rav run freeze
```

_Windows Users_

```powershell
c:\Python311\python.exe -m venv venv
.\venv\Scripts\activate
python -m pip install pip pip-tools rav --upgrade
rav run win_installs
rav run win_freeze
```

모든 구성이 완료되면 실행할 기본 명령은 다음과 같습니다.

```
rav run server
rav run watch
rav run vendor_pull
```

- `rav run server`는 `django` 폴더의 `python manage.py runserver`에 매핑됩니다.
- `rav run watch`는 tailwind를 트리거하여 `tailwind-input.css`파일을 통해 `output.css` 스타일 파일을 출력합니다.
- `rav run vendor_pull`은 `htmx`와 `flowbite` 사용을 위한 명령어입니다.
