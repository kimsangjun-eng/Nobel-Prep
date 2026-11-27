import json, base64, sys

VERSION = sys.argv[1]  # "A" or "B"
MOCK_NUM = "__MOCK_NUM__"
OTHER = "B" if VERSION == "A" else "A"
DATA_FILE = f"quiz_{VERSION.lower()}_data.json"
OUT_FILE = f"vocab_quiz_{VERSION.lower()}.html"

with open(DATA_FILE, encoding="utf-8") as f:
    qs = json.load(f)

N = len(qs)
PASS_SCORE = round(N * 0.8)  # 80%

def b64(s):
    return base64.b64encode(s.encode("utf-8")).decode("ascii")

js_items = []
for q in qs:
    hashes_js = json.dumps(q["hashes"])
    js_items.append(
        "  { id:%d, word:%s, hashes:%s, displayB64:%s }"
        % (q["id"], json.dumps(q["word"]), hashes_js, json.dumps(b64(q["display"])))
    )
questions_js = ",\n".join(js_items)

html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Nobel Prep — SAT Vocabulary Quiz {VERSION} (Mock Test {MOCK_NUM})</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
  :root {{
    --navy:#1B2A4A; --navy2:#243660; --gold:#C9A84C; --gold2:#e8c56a;
    --white:#FFFFFF; --off:#F7F8FA; --gray1:#E8EAF0; --gray2:#9AA0B2;
    --gray3:#555D72; --green:#2D7D46; --green-bg:#EBF7EF;
    --red:#C0392B; --red-bg:#FDECEA; --radius:10px;
    --shadow:0 2px 12px rgba(27,42,74,0.10);
  }}
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ font-family:'Inter',sans-serif; background:var(--off); color:var(--navy); min-height:100vh; }}
  header {{ background:var(--navy); padding:18px 28px; display:flex; align-items:center; justify-content:space-between; position:sticky; top:0; z-index:100; box-shadow:0 2px 10px rgba(0,0,0,0.25); }}
  .logo {{ display:flex; align-items:center; gap:12px; }}
  .logo-badge {{ width:38px; height:38px; background:var(--gold); border-radius:8px; display:flex; align-items:center; justify-content:center; font-weight:700; font-size:15px; color:var(--navy); }}
  .logo-text h1 {{ font-size:16px; font-weight:700; color:var(--white); }}
  .logo-text p  {{ font-size:11px; color:var(--gold); margin-top:1px; }}
  .header-right {{ display:flex; flex-direction:column; align-items:flex-end; gap:4px; }}
  .timer {{ background:rgba(255,255,255,0.12); color:var(--white); border-radius:8px; padding:7px 14px; font-family:'JetBrains Mono',monospace; font-size:15px; }}
  .quiz-badge {{ background:var(--gold); color:var(--navy); font-size:10px; font-weight:700; padding:3px 10px; border-radius:20px; letter-spacing:0.8px; }}
  .progress-bar-wrap {{ width:100%; height:3px; background:rgba(255,255,255,0.15); }}
  .progress-bar {{ height:3px; background:var(--gold); transition:width 0.4s ease; width:0%; }}
  .container {{ max-width:760px; margin:0 auto; padding:28px 20px 60px; }}
  .info-card {{ background:var(--white); border-radius:var(--radius); box-shadow:var(--shadow); padding:24px 28px; margin-bottom:20px; border-top:3px solid var(--gold); }}
  .info-card h2 {{ font-size:16px; font-weight:700; margin-bottom:4px; }}
  .info-card p  {{ font-size:13px; color:var(--gray3); margin-bottom:18px; }}
  .form-row {{ display:flex; gap:14px; flex-wrap:wrap; }}
  .form-group {{ flex:1; min-width:180px; }}
  .form-group label {{ display:block; font-size:11px; font-weight:600; color:var(--gray3); margin-bottom:6px; text-transform:uppercase; letter-spacing:0.5px; }}
  .form-group input, .form-group select {{ width:100%; padding:10px 13px; border:1.5px solid var(--gray1); border-radius:7px; font-size:14px; font-family:'Inter',sans-serif; color:var(--navy); background:var(--off); outline:none; transition:border-color 0.2s; }}
  .form-group input:focus, .form-group select:focus {{ border-color:var(--gold); background:var(--white); }}
  .instructions {{ background:var(--white); border-radius:var(--radius); padding:16px 20px; margin-bottom:20px; box-shadow:var(--shadow); font-size:13px; color:var(--gray3); border-left:3px solid var(--gold); line-height:1.7; }}
  .q-card {{ background:var(--white); border-radius:var(--radius); box-shadow:var(--shadow); padding:20px 24px; margin-bottom:12px; border-left:4px solid var(--gray1); transition:border-color 0.2s; }}
  .q-card:focus-within {{ border-left-color:var(--gold); }}
  .q-card.correct   {{ border-left-color:var(--green); background:var(--green-bg); }}
  .q-card.incorrect {{ border-left-color:var(--red);   background:var(--red-bg); }}
  .q-header {{ display:flex; align-items:flex-start; gap:14px; margin-bottom:14px; }}
  .q-num {{ min-width:28px; height:28px; background:var(--navy); color:var(--white); border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700; flex-shrink:0; margin-top:2px; }}
  .q-num.correct   {{ background:var(--green); }}
  .q-num.incorrect {{ background:var(--red); }}
  .q-word {{ font-size:19px; font-weight:700; color:var(--navy); margin-bottom:2px; font-family:'JetBrains Mono',monospace; }}
  .q-text {{ font-size:13px; color:var(--gray3); }}
  .answer-input {{ width:100%; padding:10px 14px; border:1.5px solid var(--gray1); border-radius:7px; font-size:14px; font-family:'Inter',sans-serif; color:var(--navy); background:var(--off); outline:none; transition:border-color 0.2s; margin-top:10px; }}
  .answer-input:focus    {{ border-color:var(--navy); background:var(--white); }}
  .answer-input.correct  {{ border-color:var(--green); background:var(--green-bg); }}
  .answer-input.incorrect{{ border-color:var(--red);   background:var(--red-bg); }}
  .answer-input:disabled {{ cursor:not-allowed; }}
  .feedback {{ margin-top:10px; padding:8px 12px; border-radius:6px; font-size:13px; display:none; }}
  .feedback.correct   {{ display:block; background:rgba(45,125,70,0.12); color:var(--green); }}
  .feedback.incorrect {{ display:block; background:rgba(192,57,43,0.10); color:var(--red); }}
  .submit-wrap {{ text-align:center; margin-top:28px; }}
  .submit-wrap p {{ font-size:12px; color:var(--gray2); margin-top:10px; }}
  .btn-primary {{ background:var(--gold); color:var(--navy); font-size:15px; font-weight:700; padding:14px 36px; border:none; border-radius:8px; cursor:pointer; transition:background 0.2s; }}
  .btn-primary:hover {{ background:var(--gold2); }}
  .btn-primary:disabled {{ opacity:0.5; cursor:not-allowed; }}
  .btn-secondary {{ background:var(--navy); color:var(--white); font-size:14px; font-weight:600; padding:12px 28px; border:none; border-radius:8px; cursor:pointer; }}
  #results-section {{ display:none; }}
  .results-card {{ background:var(--navy); border-radius:14px; padding:32px; text-align:center; color:var(--white); margin-bottom:20px; }}
  .score-ring {{ width:110px; height:110px; border-radius:50%; border:5px solid var(--gold); display:flex; flex-direction:column; align-items:center; justify-content:center; margin:0 auto 18px; }}
  .score-ring .big   {{ font-size:30px; font-weight:700; color:var(--gold); }}
  .score-ring .denom {{ font-size:12px; color:var(--gray2); }}
  .results-card h2   {{ font-size:20px; font-weight:700; margin-bottom:4px; }}
  .results-card .sub {{ font-size:13px; color:var(--gray2); }}
  .pass-banner {{ margin-top:14px; padding:12px 20px; border-radius:8px; font-size:15px; font-weight:700; }}
  .pass-banner.pass {{ background:var(--green); color:var(--white); }}
  .pass-banner.fail {{ background:var(--red);   color:var(--white); }}
  .breakdown-grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:10px; margin-bottom:20px; }}
  .breakdown-item {{ background:var(--white); border-radius:var(--radius); padding:14px; text-align:center; box-shadow:var(--shadow); }}
  .breakdown-item .val {{ font-size:20px; font-weight:700; }}
  .breakdown-item .lbl {{ font-size:11px; color:var(--gray2); margin-top:2px; text-transform:uppercase; }}
  .sheet-status {{ margin-top:12px; padding:10px 16px; border-radius:7px; font-size:13px; display:none; }}
  .sheet-status.sending {{ display:block; background:#EEF2FF; color:#3B5BDB; }}
  .sheet-status.success {{ display:block; background:var(--green-bg); color:var(--green); }}
  .sheet-status.error   {{ display:block; background:var(--red-bg);   color:var(--red); }}
  .results-actions {{ display:flex; gap:12px; justify-content:center; margin-top:18px; flex-wrap:wrap; }}
  .progress-text {{ font-size:11px; color:var(--gray2); }}
  @media(max-width:560px){{ .container{{padding:16px 14px 50px;}} header{{padding:14px 16px;}} }}
</style>
</head>
<body>
<header>
  <div class="logo">
    <div class="logo-badge">NP</div>
    <div class="logo-text">
      <h1>Nobel Prep</h1>
      <p>SAT Vocabulary &middot; Mock Test {MOCK_NUM} (R&amp;W)</p>
    </div>
  </div>
  <div class="header-right">
    <div class="timer" id="timer">00:00</div>
    <div class="quiz-badge">VOCAB QUIZ {VERSION}</div>
    <div class="progress-text" id="progress-text">0 / {N} answered</div>
  </div>
</header>
<div class="progress-bar-wrap"><div class="progress-bar" id="progress-bar"></div></div>

<div class="container">
  <div class="info-card">
    <h2>Student Information</h2>
    <p>Enter your information before starting the quiz.</p>
    <div class="form-row">
      <div class="form-group">
        <label>Full Name</label>
        <input type="text" id="student-name" placeholder="e.g. Kim Minjun">
      </div>
      <div class="form-group">
        <label>Period / Class</label>
        <select id="student-period">
          <option value="">Select period</option>
          <option>Period 1</option><option>Period 2</option>
          <option>Period 3</option><option>Period 4</option>
          <option>Period 5</option><option>Afternoon</option><option>Weekend</option>
        </select>
      </div>
    </div>
  </div>

  <div class="instructions">
    <strong>Directions:</strong> For each word below, type its meaning <strong>in Korean or English</strong>.
    Pass standard: <strong>{PASS_SCORE}/{N} ({PASS_PCT}%) or above</strong>.
    If you do not pass Quiz {VERSION}, please retake with <strong>Quiz {OTHER}</strong>.
  </div>

  <div id="quiz-form"></div>

  <div class="submit-wrap">
    <button class="btn-primary" id="submit-btn" onclick="submitQuiz()">Submit Quiz {VERSION}</button>
    <p>Once submitted, your answers cannot be changed.</p>
  </div>

  <div id="results-section">
    <div class="results-card">
      <div class="score-ring">
        <span class="big" id="res-score">&mdash;</span>
        <span class="denom">/ {N}</span>
      </div>
      <h2 id="res-name">&mdash;</h2>
      <p class="sub" id="res-period">&mdash;</p>
      <div class="pass-banner" id="pass-banner">&mdash;</div>
    </div>
    <div class="breakdown-grid">
      <div class="breakdown-item"><div class="val" id="bd-correct" style="color:var(--green)">&mdash;</div><div class="lbl">Correct</div></div>
      <div class="breakdown-item"><div class="val" id="bd-wrong" style="color:var(--red)">&mdash;</div><div class="lbl">Incorrect</div></div>
      <div class="breakdown-item"><div class="val" id="bd-pct">&mdash;</div><div class="lbl">Score %</div></div>
    </div>
    <div class="sheet-status" id="sheet-status"></div>
    <div class="results-actions">
      <button class="btn-secondary" onclick="reviewAnswers()">Review Answers</button>
      <button class="btn-primary" onclick="retakeQuiz()">Retake Quiz {VERSION}</button>
    </div>
  </div>
</div>

<script>
// 기존 Google Sheet / Apps Script 웹앱(Mock Test 41부터 사용 중)을 재사용합니다.
// quizId를 "42A"/"42B"로 구분해 같은 시트 안에서도 어느 Mock Test 결과인지 알 수 있게 했습니다.
const SHEET_URL  = "https://script.google.com/macros/s/AKfycby0zkbo5tF7m0Xic3aagKH2pYwCOKselDjD8odu2qozlaA7t_joXTbuxIC5lZGUy_-xaQ/exec";
const QUIZ_ID    = "{MOCK_NUM}{VERSION}";
const PASS_SCORE = {PASS_SCORE};
const TOTAL_Q    = {N};

// 정답은 SHA-256 해시로만 저장 (평문 노출 금지). 화면 표시용 뜻은 base64로만 보관하고
// 채점 후에만 디코딩해서 보여줍니다.
const questions = [
{QUESTIONS_JS}
];

let timerInterval, seconds=0, submitted=false;
function startTimer(){{ timerInterval=setInterval(()=>{{ seconds++; const m=String(Math.floor(seconds/60)).padStart(2,'0'),s=String(seconds%60).padStart(2,'0'); document.getElementById('timer').textContent=`${{m}}:${{s}}`; }},1000); }}

function buildQuiz(){{
  const form=document.getElementById('quiz-form');
  questions.forEach(q=>{{
    const card=document.createElement('div'); card.className='q-card'; card.id=`card-${{q.id}}`;
    card.innerHTML=`<div class="q-header"><div class="q-num" id="num-${{q.id}}">${{q.id}}</div><div class="q-meta" style="flex:1">
        <div class="q-word">${{q.word}}</div>
      </div></div>
      <input class="answer-input" type="text" id="ans-${{q.id}}" placeholder="Type your answer" autocomplete="off" autocorrect="off" spellcheck="false" oninput="updateProgress()">
      <div class="feedback" id="fb-${{q.id}}"></div>`;
    form.appendChild(card);
  }});
  startTimer();
}}

function updateProgress(){{
  let filled=0;
  questions.forEach(q=>{{ const e=document.getElementById(`ans-${{q.id}}`); if(e&&e.value.trim()!=='') filled++; }});
  document.getElementById('progress-text').textContent=`${{filled}} / ${{TOTAL_Q}} answered`;
  document.getElementById('progress-bar').style.width=`${{(filled/TOTAL_Q)*100}}%`;
}}

function normalize(str){{
  return str.trim().toLowerCase().replace(/[\\s,./·\\-()]/g,'');
}}

async function sha256Hex(message){{
  const data = new TextEncoder().encode(message);
  const hashBuffer = await crypto.subtle.digest('SHA-256', data);
  return Array.from(new Uint8Array(hashBuffer)).map(b=>b.toString(16).padStart(2,'0')).join('');
}}

async function submitQuiz(){{
  if(submitted)return;
  const name=document.getElementById('student-name').value.trim();
  const period=document.getElementById('student-period').value;
  if(!name){{ document.getElementById('student-name').style.borderColor='var(--red)'; alert('Please enter your name before submitting.'); return; }}
  clearInterval(timerInterval); submitted=true;
  document.getElementById('submit-btn').disabled=true;
  let correct=0; const details=[];

  for(const q of questions){{
    const card=document.getElementById(`card-${{q.id}}`);
    const numEl=document.getElementById(`num-${{q.id}}`);
    const fb=document.getElementById(`fb-${{q.id}}`);
    const input=document.getElementById(`ans-${{q.id}}`);
    const studentAns=input.value.trim();
    const studentHash= studentAns==='' ? '' : await sha256Hex(normalize(studentAns));
    const isOK = studentAns!=='' && q.hashes.includes(studentHash);
    const displayAns = decodeURIComponent(escape(atob(q.displayB64)));

    input.disabled=true;
    input.classList.add(isOK?'correct':'incorrect');

    if(isOK){{ correct++; card.classList.add('correct'); numEl.classList.add('correct'); fb.className='feedback correct'; fb.innerHTML=`&#10003; Correct! <small>${{displayAns}}</small>`; }}
    else {{ card.classList.add('incorrect'); numEl.classList.add('incorrect'); fb.className='feedback incorrect'; fb.innerHTML=`&#10007; Incorrect &mdash; Answer: <strong>${{displayAns}}</strong>`; }}
    details.push({{ qNum:q.id, word:q.word, studentAns: studentAns||'(no answer)', correctAns:displayAns, result:isOK?'O':'X' }});
  }}

  const pct=Math.round((correct/TOTAL_Q)*100);
  const passed=correct>=PASS_SCORE;
  const mm=String(Math.floor(seconds/60)).padStart(2,'0'), ss=String(seconds%60).padStart(2,'0');
  const timeStr=`${{mm}}:${{ss}}`;
  document.getElementById('submit-btn').style.display='none';
  const rs=document.getElementById('results-section'); rs.style.display='block';
  document.getElementById('res-score').textContent=correct;
  document.getElementById('res-name').textContent=name;
  document.getElementById('res-period').textContent=`${{period||'No period'}} &middot; Time: ${{timeStr}}`;
  const banner=document.getElementById('pass-banner');
  banner.className=`pass-banner ${{passed?'pass':'fail'}}`;
  banner.textContent=passed?`PASS — Great work! (${{correct}}/${{TOTAL_Q}})`:`FAIL — Please take Quiz {OTHER} (${{correct}}/${{TOTAL_Q}})`;
  document.getElementById('bd-correct').textContent=correct;
  document.getElementById('bd-wrong').textContent=TOTAL_Q-correct;
  document.getElementById('bd-pct').textContent=pct+'%';
  rs.scrollIntoView({{behavior:'smooth'}});
  sendToSheets(name,period,correct,pct,passed,timeStr,details);
}}

function sendToSheets(name,period,score,pct,passed,time,details){{
  if(SHEET_URL.indexOf('REPLACE_WITH')===0){{ showSheetStatus('error','⚠️ Google Sheets 연동 URL이 아직 설정되지 않았습니다. (SHEET_URL을 교체해 주세요)'); return; }}
  showSheetStatus('sending','⏳ 결과를 Google Sheets에 저장하는 중...');
  const now=new Date().toLocaleString('ko-KR',{{timeZone:'Asia/Seoul'}});
  fetch(SHEET_URL,{{ method:'POST', mode:'no-cors', headers:{{'Content-Type':'application/json'}}, body:JSON.stringify({{name,period,score,pct,passed:passed?'PASS':'FAIL',quizId:QUIZ_ID,time,date:now,details}}) }})
  .then(()=>showSheetStatus('success','✅ 결과가 Google Sheets에 저장되었습니다.'))
  .catch(()=>showSheetStatus('error','⚠️ Sheets 저장 실패'));
}}
function showSheetStatus(t,m){{ const el=document.getElementById('sheet-status'); el.className=`sheet-status ${{t}}`; el.textContent=m; }}
function reviewAnswers(){{ document.querySelector('.q-card').scrollIntoView({{behavior:'smooth'}}); }}
function retakeQuiz(){{ if(confirm('모든 답안이 초기화됩니다. 다시 시작할까요?')) location.reload(); }}
buildQuiz();
</script>
</body>
</html>
""".format(
    VERSION=VERSION, OTHER=OTHER, N=N, PASS_SCORE=PASS_SCORE,
    PASS_PCT=round(PASS_SCORE/N*100), QUESTIONS_JS=questions_js, MOCK_NUM=MOCK_NUM
)

with open(OUT_FILE, "w", encoding="utf-8") as f:
    f.write(html)
print("wrote", OUT_FILE, "N=", N, "PASS_SCORE=", PASS_SCORE)
