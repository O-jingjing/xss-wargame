from flask import Flask, request, render_template_string

app = Flask(__name__)

# 문제를 풀면 얻게 되는 플래그
FLAG = "FLAG{j5_5tr1ng_c0nt3xt_xss_1s_tr1cky}"

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
    <p>해당 사용자가 존재하는지 확인합니다.</p>
    <form action="/check" method="GET">
        <input type="text" name="username" placeholder="사용자 이름 입력" size="30">
        <button type="submit">조회</button>
    </form>
</body>
</html>
"""

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
    <p> 성공! FLAG: {{ flag }}</p>
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
        return f"<p>'{username}' 는 존재하지 않는 사용자입니다.</p><a href='/'>돌아가기</a>"

    solved = username.lower().count("alert(") >= 1 and ('"' in username or "'" in username)

    return render_template_string(
        RESULT_HTML, username=username, solved=solved, flag=FLAG
    )


if __name__ == "__main__":
    app.run(debug=True)
