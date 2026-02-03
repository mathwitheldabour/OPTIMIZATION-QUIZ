import streamlit as st
import random
import math
import time

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Optimization MCQ Quiz", layout="wide")

# --- CSS للتجميل وتنسيق الأسئلة ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    * { font-family: 'Cairo', sans-serif; }
    
    .question-card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .ar-text {
        text-align: right; direction: rtl; font-size: 20px; font-weight: bold;
        color: #2c3e50; margin-bottom: 10px; border-right: 5px solid #3498db; padding-right: 15px;
    }
    .en-text {
        text-align: left; direction: ltr; font-size: 18px; color: #555;
        font-family: 'Segoe UI', sans-serif; margin-bottom: 20px; border-left: 5px solid #e74c3c; padding-left: 15px;
    }
    .timer-box {
        font-size: 24px; font-weight: bold; text-align: center;
        padding: 10px; border: 2px solid #e74c3c; border-radius: 10px; color: #e74c3c;
    }
    /* تنسيق خيارات الراديو لتكون أكبر وأوضح */
    .stRadio label { font-size: 18px !important; padding: 10px; }
</style>
""", unsafe_allow_html=True)

# --- دوال مساعدة للحسابات وتوليد المشتتات ---
def generate_distractors(correct_val, step=1):
    """توليد خيارات خاطئة قريبة من الإجابة الصحيحة"""
    options = {correct_val}
    while len(options) < 4:
        # توليد قيم خاطئة بضرب أو جمع بسيط لتبدو منطقية
        fake = correct_val + random.choice([-step, step, step*2, -step*2])
        if fake > 0: # نتجنب القيم السالبة في الأبعاد
            options.add(round(fake, 2))
    
    final_opts = list(options)
    random.shuffle(final_opts)
    return final_opts

# --- مولد الأسئلة الذكي ---
def generate_questions():
    questions = []
    
    # 1. الصندوق المفتوح (Open Box) - Max Volume
    # Sheet side = S (Square). Cut x. V = x(S-2x)^2.
    # Critical point x = S/6.
    # نختار S يقبل القسمة على 6 لسهولة الأرقام
    s_box = random.choice([12, 18, 24, 30, 36])
    ans_box_x = s_box / 6
    questions.append({
        "type": "Open Box",
        "ar": f"صفيحة مربعة الشكل طول ضلعها {s_box} سم. يراد صنع صندوق مفتوح من الأعلى بقص مربعات متطابقة طول ضلعها (x) من الأركان وثني الجوانب. أوجد قيمة x التي تجعل حجم الصندوق أكبر ما يمكن.",
        "en": f"A square sheet of side {s_box} cm is to be made into an open-top box by cutting equal squares of side (x) from the corners and folding up the flaps. Find x that maximizes the volume.",
        "options": generate_distractors(ans_box_x, step=1),
        "correct": ans_box_x,
        "unit": "cm"
    })

    # 2. أقصر مسافة (Shortest Distance) - Point to Curve
    # Point (k, 0) to curve y = sqrt(x).
    # Distance squared D^2 = (x-k)^2 + x.
    # Derivative: 2(x-k) + 1 = 0 => 2x - 2k + 1 = 0 => x = k - 0.5.
    k_val = random.choice([2, 3, 4, 5, 6]) # نختار أرقام صحيحة
    ans_dist_x = k_val - 0.5
    questions.append({
        "type": "Shortest Distance",
        "ar": f"أوجد الإحداثي السيني (x-coordinate) للنقطة الواقعة على المنحنى $y = \\sqrt{{x}}$ والتي تكون أقرب ما يمكن للنقطة ({k_val}, 0).",
        "en": f"Find the x-coordinate of the point on the curve $y = \\sqrt{{x}}$ that is closest to the point ({k_val}, 0).",
        "options": generate_distractors(ans_dist_x, step=0.5),
        "correct": ans_dist_x,
        "unit": ""
    })

    # 3. سياج النهر (River Fence) - Max Area
    # 2x + y = P. Max Area => x = P/4, y = P/2.
    p_river = random.randrange(800, 2000, 200)
    ans_river_area = (p_river / 4) * (p_river / 2)
    questions.append({
        "type": "River Fence",
        "ar": f"مزارع لديه {p_river} قدم من السياج لإحاطة حقل مستطيل بجوار نهر (لا يحتاج سياج). أوجد أكبر مساحة ممكنة.",
        "en": f"A farmer has {p_river} ft of fencing to enclose a rectangular field next to a river. Find the maximum area.",
        "options": generate_distractors(ans_river_area, step=p_river*10),
        "correct": ans_river_area,
        "unit": "ft²"
    })

    # 4. مستطيل داخل دائرة (Inscribed Rectangle)
    # Radius R. Max Area Square side = R*sqrt(2). Area = 2R^2.
    r_circle = random.randint(5, 12)
    ans_rect_area = 2 * (r_circle ** 2)
    questions.append({
        "type": "Inscribed Rect",
        "ar": f"أوجد أكبر مساحة لمستطيل يمكن رسمه داخل دائرة نصف قطرها {r_circle} وحدات.",
        "en": f"Find the maximum area of a rectangle inscribed in a circle of radius {r_circle}.",
        "options": generate_distractors(ans_rect_area, step=10),
        "correct": ans_rect_area,
        "unit": "sq units"
    })

    # 5. تكلفة (Minimum Cost)
    # Area A. Cost: 3$ (2 sides), 2$ (2 sides). Min Cost = 12 * sqrt(A/1.5).
    # نختار A بحيث يكون الجذر مربع كامل لسهولة الأرقام: A = 1.5 * k^2
    k_cost = random.choice([10, 20, 30]) 
    area_cost = int(1.5 * (k_cost**2))
    ans_min_cost = 12 * k_cost
    questions.append({
        "type": "Min Cost",
        "ar": f"يراد تسييج منطقة مساحتها {area_cost} قدم مربع. سياج الجانبين المتقابلين 3$/قدم، والآخرين 2$/قدم. أوجد أقل تكلفة.",
        "en": f"Area {area_cost} ft². Two opposite sides cost $3/ft, others $2/ft. Find minimum cost.",
        "options": generate_distractors(ans_min_cost, step=50),
        "correct": ans_min_cost,
        "unit": "$"
    })

    return questions

# --- إدارة الحالة (Session State) ---
if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = generate_questions()
    st.session_state.user_answers = [None] * 5
    st.session_state.current_q = 0
    st.session_state.start_time = time.time()
    st.session_state.quiz_submitted = False

# --- المؤقت ---
QUIZ_DURATION = 15 * 60
elapsed = time.time() - st.session_state.start_time
time_left = max(0, QUIZ_DURATION - elapsed)

if time_left == 0 and not st.session_state.quiz_submitted:
    st.session_state.quiz_submitted = True
    st.rerun()

# --- Sidebar ---
with st.sidebar:
    st.header("⏳ Quiz Timer")
    mins, secs = divmod(int(time_left), 60)
    color = "red" if time_left < 60 else "#2c3e50"
    st.markdown(f'<div class="timer-box" style="color:{color}">{mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.write("**Mr. Ibrahim Eldabour**")
    if st.button("🔄 New Quiz / اختبار جديد"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()

# --- Main App ---
st.title("📝 Optimization MCQ Quiz")
st.markdown("---")

if not st.session_state.quiz_submitted:
    # Navigation Buttons
    cols = st.columns(5)
    for i in range(5):
        label = f"Q{i+1}"
        style = "background-color:#2980b9; color:white;" if i == st.session_state.current_q else ""
        if st.session_state.user_answers[i] is not None: label += " ✅"
        if cols[i].button(label, key=f"nav_{i}"):
            st.session_state.current_q = i
            st.rerun()

    # Display Question
    q_idx = st.session_state.current_q
    q_data = st.session_state.quiz_data[q_idx]

    st.markdown(f"""
    <div class="question-card">
        <div class="ar-text">س{q_idx+1}: {q_data['ar']}</div>
        <div class="en-text">Q{q_idx+1}: {q_data['en']}</div>
    </div>
    """, unsafe_allow_html=True)

    # MCQ Logic
    options = q_data['options']
    # نحتاج تحويل الخيارات لنصوص للعرض
    options_str = [f"{opt} {q_data['unit']}" for opt in options]
    
    # استرجاع الإجابة السابقة إن وجدت
    previous_selection = st.session_state.user_answers[q_idx]
    
    # عرض الراديو
    choice = st.radio(
        "Select the correct answer / اختر الإجابة الصحيحة:",
        options_str,
        index=options_str.index(previous_selection) if previous_selection in options_str else None,
        key=f"radio_{q_idx}"
    )

    # أزرار التحكم
    c1, c2 = st.columns([1, 4])
    if c1.button("Save 💾"):
        st.session_state.user_answers[q_idx] = choice
        if q_idx < 4:
            st.session_state.current_q += 1
            st.rerun()
        else:
            st.success("Saved! Review or Submit.")
    
    st.markdown("---")
    if st.button("📤 Submit Final / تسليم نهائي", type="primary"):
        st.session_state.user_answers[q_idx] = choice # Save current before submit
        st.session_state.quiz_submitted = True
        st.rerun()

else:
    # --- صفحة النتائج ---
    st.balloons()
    score = 0
    st.write("### 📊 Quiz Results / نتائج الاختبار")
    
    for i, q in enumerate(st.session_state.quiz_data):
        user_choice_str = st.session_state.user_answers[i]
        correct_val = q['correct']
        
        # استخراج الرقم من نص اختيار الطالب للمقارنة
        is_correct = False
        if user_choice_str:
            # نحاول استخراج الرقم من النص (مثلا "250.0 ft" -> 250.0)
            try:
                user_val = float(user_choice_str.split()[0])
                if abs(user_val - correct_val) < 0.1:
                    is_correct = True
                    score += 1
            except:
                pass
        
        status = "✅ Correct" if is_correct else "❌ Wrong"
        with st.expander(f"Question {i+1}: {status}"):
            st.write(q['en'])
            st.write(f"**Your Answer:** {user_choice_str}")
            if not is_correct:
                st.write(f"**Correct Answer:** {correct_val} {q['unit']}")

    final_score = (score / 5) * 100
    color = "#d4edda" if final_score >= 60 else "#f8d7da"
    text_color = "#155724" if final_score >= 60 else "#721c24"
    
    st.markdown(f"""
    <div style="background-color:{color}; padding:20px; border-radius:10px; text-align:center; margin-top:20px;">
        <h2 style="color:{text_color};">Final Grade: {score} / 5 ({final_score}%)</h2>
    </div>
    """, unsafe_allow_html=True)
