"""
Reflected XSS 워게임 - 학습용 취약 웹앱
--------------------------------------
'사용자 조회' 페이지: 입력한 아이디가 존재하지 않으면 alert()로 안내 메시지를 띄운다.
이 alert() 문자열 안에 입력값이 검증 없이 그대로 삽입되는 것이 이 문제의 취약점이다.

절대 실제 서비스나 외부에 노출된 서버에 배포하지 마세요.
로컬(127.0.0.1) 학습 환경에서만 실행하세요.
"""

from flask import Flask, request, render_template_string

app = Flask(__name__)

# 문제를 풀면 얻게 되는 플래그
FLAG = "FLAG{j5_5tr1ng_c0nt3xt_xss_1s_tr1cky}"

# 실제로 존재하는 것으로 취급할 아이디 (테스트용)
EXISTING_USERS = {"admin", "guest"}

INDEX_HTML = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>사용자 조회</title>
</head>
<body>
    <h1> 사용자 조회 </h1>
    <p>존재하는 사용자인지 조회합니다.</p>
    <form action="/check" method="GET">
        <input type="text" name="username" placeholder="사용자 이름 입력" size="30">
        <button type="submit">조회</button>
    </form>
</body>
</html>
"""

# ⚠️ 취약한 템플릿
# username 값이 <script> 안, 그것도 큰따옴표로 감싼 JS 문자열 리터럴
# 내부에 |safe 필터로 이스케이프 없이 그대로 삽입되고 있다.
#
# Jinja2의 기본 자동 이스케이프는 HTML 특수문자(<, >, &, ", ')를
# &lt; &gt; &amp; &quot; &#39; 로 바꿔주지만, 이는 "HTML 텍스트/속성"
# 컨텍스트를 기준으로 한 방어다. 여기서는 |safe로 그 방어 자체를 꺼버렸기
# 때문에, 사용자가 큰따옴표(")를 입력하면 JS 문자열 리터럴을 그대로
# 조기 종료시키고 그 뒤에 새로운 JS 코드를 이어 쓸 수 있게 된다.
RESULT_HTML = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>조회 결과</title>
</head>
<body>
    <h1>조회 결과</h1>

    <script>
        alert("'{{ username|safe }}' 는 존재하지 않는 사용자입니다.");
    </script>

    {% if solved %}
    <p>🎉 성공! FLAG: {{ flag }}</p>
    {% endif %}

    <a href="/">다시 조회하기</a>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(INDEX_HTML)


@app.route("/check")
def check():
    username = request.args.get("username", "")

    if username in EXISTING_USERS:
        # 존재하는 아이디는 그냥 안내만 하고 취약한 분기를 타지 않는다
        return f"<p>'{username}' 는 존재하지 않는 사용자입니다.</p><a href='/'>돌아가기</a>"

    # 아주 단순한 "성공 판정" 로직 (실제 XSS 탐지가 아니라 워게임용 편의 로직)
    # 큰따옴표나 작은따옴표로 문자열을 탈출하면서 alert(를 추가로 넣었는지 확인한다.
    solved = username.lower().count("alert(") >= 1 and ('"' in username or "'" in username)

    return render_template_string(
        RESULT_HTML, username=username, solved=solved, flag=FLAG
    )


if __name__ == "__main__":
    # debug=True는 개발/학습 환경에서만 사용. 절대 운영 환경에 쓰지 말 것.
    app.run(debug=True)
