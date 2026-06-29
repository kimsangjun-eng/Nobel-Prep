-- ① 학생 프로필 테이블
CREATE TABLE student_profiles (
  id UUID REFERENCES auth.users PRIMARY KEY,
  name TEXT NOT NULL,
  school TEXT,
  grade TEXT,
  parent_email TEXT,
  is_admin BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ② 시험 결과 테이블
CREATE TABLE exam_results (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users NOT NULL,
  exam_id TEXT NOT NULL,
  completed BOOLEAN DEFAULT FALSE,
  rw_m1_raw INTEGER,
  answers JSONB,
  submitted_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(user_id, exam_id)
);

-- ③ RLS (Row Level Security) 활성화
ALTER TABLE student_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE exam_results ENABLE ROW LEVEL SECURITY;

-- ④ 정책: 본인 데이터만 읽기/쓰기
CREATE POLICY "본인 프로필 읽기" ON student_profiles
  FOR SELECT USING (auth.uid() = id);

CREATE POLICY "본인 결과 읽기" ON exam_results
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "본인 결과 쓰기" ON exam_results
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "본인 결과 업데이트" ON exam_results
  FOR UPDATE USING (auth.uid() = user_id);

-- ⑤ 관리자: 전체 조회 가능
CREATE POLICY "관리자 전체 읽기 profiles" ON student_profiles
  FOR SELECT USING (
    EXISTS (
      SELECT 1 FROM student_profiles
      WHERE id = auth.uid() AND is_admin = TRUE
    )
  );

CREATE POLICY "관리자 전체 읽기 results" ON exam_results
  FOR SELECT USING (
    EXISTS (
      SELECT 1 FROM student_profiles
      WHERE id = auth.uid() AND is_admin = TRUE
    )
  );
