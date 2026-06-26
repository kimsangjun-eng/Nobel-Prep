// ================================================================
// Nobel Prep — IB HL Chemistry Quiz
// Google Apps Script (Apps Script Web App)
//
// 설치 방법:
// 1. Google Sheets 새 파일 생성
// 2. 확장 프로그램 → Apps Script
// 3. 이 코드 전체 붙여넣기
// 4. 저장 → 배포 → 새 배포 → 웹 앱
//    - 액세스 권한: 모든 사용자
// 5. 배포 URL을 퀴즈 HTML의 SHEETS_URL에 붙여넣기
// ================================================================

const SUMMARY_SHEET = "Summary";
const TOTAL_QUESTIONS = 20;

// ── 진입점 ──────────────────────────────────────────────────────
function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);
    const ss = SpreadsheetApp.getActiveSpreadsheet();

    setupSummarySheet(ss);
    appendToSummary(ss, data);
    updateStudentTab(ss, data);

    return ContentService
      .createTextOutput(JSON.stringify({ status: "ok" }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ status: "error", message: err.message }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet(e) {
  return ContentService
    .createTextOutput("Nobel Prep IB Quiz — Sheets API is running.")
    .setMimeType(ContentService.MimeType.TEXT);
}

// ── Summary 시트 초기 설정 ───────────────────────────────────────
function setupSummarySheet(ss) {
  let sheet = ss.getSheetByName(SUMMARY_SHEET);
  if (!sheet) {
    sheet = ss.insertSheet(SUMMARY_SHEET, 0);
  }

  // 헤더가 없으면 생성
  if (sheet.getLastRow() === 0 || sheet.getRange("A1").getValue() === "") {
    const headers = [
      "Timestamp", "Name", "Period", "Quiz",
      "Score", "Total", "Percent", "Pass/Fail",
      "MCQ Score", "SA Score"
    ];
    // Q1~Q20 헤더 추가
    for (let i = 1; i <= TOTAL_QUESTIONS; i++) {
      headers.push(`Q${i}`);
    }

    const headerRow = sheet.getRange(1, 1, 1, headers.length);
    headerRow.setValues([headers]);

    // 헤더 스타일
    headerRow.setBackground("#1B2A4A");
    headerRow.setFontColor("#FFFFFF");
    headerRow.setFontWeight("bold");
    headerRow.setFontSize(10);
    sheet.setFrozenRows(1);
    sheet.setColumnWidth(1, 160); // Timestamp
    sheet.setColumnWidth(2, 130); // Name
    sheet.setColumnWidth(4, 220); // Quiz
  }
}

// ── Summary 시트에 행 추가 ───────────────────────────────────────
function appendToSummary(ss, data) {
  const sheet = ss.getSheetByName(SUMMARY_SHEET);

  // details 파싱: "Q1:O,Q2:X,Q3:O,..."
  const qResults = parseDetails(data.details);

  const row = [
    new Date(data.timestamp),
    data.name,
    data.period || "—",
    data.quiz,
    data.score,
    data.total,
    data.percent + "%",
    data.pass,
    data.mcq,
    data.sa
  ];

  // Q1~Q20 O/X 추가
  for (let i = 1; i <= TOTAL_QUESTIONS; i++) {
    row.push(qResults[`Q${i}`] || "—");
  }

  const newRow = sheet.getLastRow() + 1;
  const range = sheet.getRange(newRow, 1, 1, row.length);
  range.setValues([row]);

  // Pass/Fail 색상
  const passCell = sheet.getRange(newRow, 8);
  if (data.pass === "Pass") {
    passCell.setBackground("#EBF7EF").setFontColor("#2D7D46").setFontWeight("bold");
  } else {
    passCell.setBackground("#FDECEA").setFontColor("#C0392B").setFontWeight("bold");
  }

  // O/X 색상 (Q1~Q20 컬럼: col 11부터)
  for (let i = 0; i < TOTAL_QUESTIONS; i++) {
    const cell = sheet.getRange(newRow, 11 + i);
    const val = qResults[`Q${i+1}`];
    if (val === "O") {
      cell.setBackground("#EBF7EF").setFontColor("#2D7D46").setFontWeight("bold");
    } else if (val === "X") {
      cell.setBackground("#FDECEA").setFontColor("#C0392B").setFontWeight("bold");
    }
  }

  // 퍼센트 색상
  const pct = parseInt(data.percent);
  const pctCell = sheet.getRange(newRow, 7);
  if (pct >= 70) {
    pctCell.setFontColor("#2D7D46").setFontWeight("bold");
  } else {
    pctCell.setFontColor("#C0392B").setFontWeight("bold");
  }
}

// ── 학생별 개인 탭 생성/업데이트 ────────────────────────────────
function updateStudentTab(ss, data) {
  const tabName = sanitizeName(data.name);
  let sheet = ss.getSheetByName(tabName);

  if (!sheet) {
    sheet = ss.insertSheet(tabName);
    setupStudentTab(sheet, data.name);
  }

  appendStudentRecord(sheet, data);
}

function setupStudentTab(sheet, name) {
  // 학생 탭 헤더
  sheet.getRange("A1").setValue(`📋 ${name}`);
  sheet.getRange("A1").setFontSize(14).setFontWeight("bold").setFontColor("#1B2A4A");

  const headers = ["Date", "Quiz", "Period", "Score", "Total", "Percent", "Pass/Fail", "MCQ", "SA"];
  for (let i = 1; i <= TOTAL_QUESTIONS; i++) headers.push(`Q${i}`);

  const headerRange = sheet.getRange(2, 1, 1, headers.length);
  headerRange.setValues([headers]);
  headerRange.setBackground("#1A7A8A").setFontColor("#FFFFFF").setFontWeight("bold").setFontSize(10);
  sheet.setFrozenRows(2);
  sheet.setColumnWidth(1, 130);
  sheet.setColumnWidth(2, 220);
}

function appendStudentRecord(sheet, data) {
  const qResults = parseDetails(data.details);

  const row = [
    new Date(data.timestamp),
    data.quiz,
    data.period || "—",
    data.score,
    data.total,
    data.percent + "%",
    data.pass,
    data.mcq,
    data.sa
  ];
  for (let i = 1; i <= TOTAL_QUESTIONS; i++) {
    row.push(qResults[`Q${i}`] || "—");
  }

  const newRow = sheet.getLastRow() + 1;
  const range = sheet.getRange(newRow, 1, 1, row.length);
  range.setValues([row]);

  // Pass/Fail 색상
  const passCell = sheet.getRange(newRow, 7);
  if (data.pass === "Pass") {
    passCell.setBackground("#EBF7EF").setFontColor("#2D7D46").setFontWeight("bold");
  } else {
    passCell.setBackground("#FDECEA").setFontColor("#C0392B").setFontWeight("bold");
  }

  // O/X 색상
  for (let i = 0; i < TOTAL_QUESTIONS; i++) {
    const cell = sheet.getRange(newRow, 10 + i);
    const val = qResults[`Q${i+1}`];
    if (val === "O") {
      cell.setBackground("#EBF7EF").setFontColor("#2D7D46").setFontWeight("bold");
    } else if (val === "X") {
      cell.setBackground("#FDECEA").setFontColor("#C0392B").setFontWeight("bold");
    }
  }
}

// ── 유틸리티 ────────────────────────────────────────────────────
function parseDetails(details) {
  // "Q1:O,Q2:X,Q3:O,..." → { Q1: "O", Q2: "X", ... }
  const result = {};
  if (!details) return result;
  details.split(",").forEach(part => {
    const [key, val] = part.split(":");
    if (key && val) result[key.trim()] = val.trim();
  });
  return result;
}

function sanitizeName(name) {
  // 시트 탭 이름 유효성 처리 (특수문자 제거, 최대 31자)
  return (name || "Unknown")
    .replace(/[:\\\/\?\*\[\]]/g, "")
    .substring(0, 31)
    .trim() || "Unknown";
}
