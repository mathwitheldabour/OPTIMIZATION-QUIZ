import streamlit as st
import random
import time

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Optimization Quiz | Mr. Ibrahim", layout="wide")

# --- CSS لتجميل التصميم وتنسيق الاتجاهات ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    * { font-family: 'Cairo', sans-serif; }
    
    .stButton button {
        width: 100%;
        border-radius: 5px;
        font-weight: bold;
    }
    
    /* تنسيق السؤال */
    .question-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-right: 5px solid #2980b9; /* لون مميز للعربي */
        border-left: 5px solid #c0392b; /* لون مميز للإنجليزي */
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    
    .ar-text {
        text-align: right;
        direction: rtl;
        font-size: 20px;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 15px;
    }
    
    .en-text {
        text-align: left;
        direction: ltr;
        font-size: 18px;
        font-family: 'Segoe UI', sans-serif;
        color: #555;
        margin-bottom: 10px;
    }

    .nav-active {
        background-color: #27ae60 !important;
        color: white !important;
    }
    
    .timer-box {
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        padding: 10px;
        border: 2px solid #e74c3c;
        border-radius: 10px;
        color: #e74c3c;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- دوال توليد الأسئلة (تغيير الأرقام تلقائياً) ---
def generate_questions():
    questions = []
    
    # س1: سياج النهر (River Fence)
    # 2x + y = P, Max Area
    p_river = random.randrange(800, 2000, 100) # رقم عشوائي للمحيط
    ans_river = (p_river / 4) * (p_river / 2) # المساحة القصوى
    questions.append({
        "type": "River",
        "ar": f"مزارع لديه {p_river} قدم من السياج ويريد إحاطة حقل مستطيل يحده من أحد الجوانب نهر (لا يحتاج سياج). أوجد أكبر مساحة ممكنة لهذا الحقل.",
        "en": f"A farmer has {p_river} ft of fence and wants to enclose a rectangular field bounded by a river on one side. Find the maximum possible area.",
        "correct": round(ans_river, 2),
        "unit": "ft²"
    })

    # س2: مجموع وضرب (Numbers)
    # x + y = S, Max x*y
    s_num = random.randrange(20, 100, 2)
    ans_num = (s_num / 2) * (s_num / 2)
    questions.append({
        "type": "Numbers",
        "ar": f"أوجد عددين موجبين مجموعهما {s_num} وحاصل ضربهما أكبر ما يمكن. ما هو حاصل الضرب الأكبر؟",
        "en": f"Find two positive numbers whose sum is {s_num} and whose product is a maximum. What is the maximum product?",
        "correct": round(ans_num, 2),
        "unit": ""
    })

    # س3: تكلفة السياج (Fence Cost)
    # Area = A, Cost1 = $3, Cost2 = $2. Min Cost.
    area_cost = random.choice([600, 1200, 2400, 5400]) # مساحات تعطي أرقاماً لطيفة
    # Dimensions for min cost: ratio implies sides related to sqrt(cost)
    # Simplified logic: C = 2*3*x + 2*2*y. xy=A. 
    # Min Cost happens when Cost_x = Cost_y => 6x = 4y => y = 1.5x
    # x(1.5x) = A => x = sqrt(A/1.5).
    # Total Cost = 6x + 4(1.5x) = 12x.
    import math
    x_val = math.sqrt(area_cost / 1.5)
    min_cost = 12 * x_val
    questions.append({
        "type": "Cost",
        "ar": f"يراد تسييج منطقة مستطيلة مساحتها {area_cost} قدم مربع. تكلفة السياج للجانبين المتقابلين 3$ للقدم، وللجانبين الآخرين 2$ للقدم. أوجد أقل تكلفة ممكنة للسياج.",
        "en": f"A rectangular area of {area_cost} ft² is to be fenced. Two opposite sides cost $3/ft, and the other two cost $2/ft. Find the minimum cost.",
        "correct": round(min_cost, 2),
        "unit": "$"
    })

    # س4: مستطيل داخل دائرة (Inscribed Rect)
    # Radius = R. Max Area = 2R^2
    radius = random.randint(5, 20)
    max_area_circle = 2 * (radius ** 2)
    questions.append({
        "type": "Geometry",
        "ar": f"أوجد أكبر مساحة لمستطيل يمكن رسمه داخل دائرة نصف قطرها {radius} سم.",
        "en": f"Find the maximum area of a rectangle that can be inscribed in a circle of radius {radius} cm.",
        "correct": round(max_area_circle, 2),
        "unit": "cm²"
    })

    # س5: سلك يقطع (Wire Cut) - نسخة مبسطة (مجموع المساحات أقل ما يمكن)
    # L = length. Min Area occurs at x = (pi * L) / (pi + 4) for circle circumference
    # But usually asking for length used for circle.
    l_wire = random.choice([10, 20, 100])
    # Min area answer (Length for circle)
    ans_wire = (math.pi * l_wire) / (math.pi + 4)
    questions.append({
        "type": "Wire",
        "ar": f"سلك طوله {l_wire} م تم قطعه لتكوين دائرة ومربع. كم يجب أن يكون طول الجزء المستخدم للدائرة لتكون المساحة الكلية **أقل ما يمكن**؟ (قرّب لأقرب منزلتين)",
        "en": f"A wire of length {l_wire} m is cut to form a circle and a square. How much wire should be used for the circle to **minimize** the total area? (Round to 2 decimals)",
        "correct": round(ans_wire, 2),
        "unit": "m"
    })

    return questions

# --- إدارة الجلسة (Session State) ---
if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = generate_questions()
    st.session_state.user_answers = [None] * 5 # لتخزين إجابات الطالب
    st.session_state.current_q = 0
    st.session_state.start_time = time.time()
    st.session_state.quiz_submitted = False

# --- المنطق الزمني (Timer Logic) ---
QUIZ_DURATION = 15 * 60 # 15 دقيقة بالثواني
elapsed_time = time.time() - st.session_state.start_time
time_left = QUIZ_DURATION - elapsed_time

if time_left <= 0:
    st.session_state.quiz_submitted = True
    time_left = 0

# --- الشريط الجانبي (المعلومات والمؤقت) ---
with st.sidebar:
    st.header("⏳ Quiz Info")
    
    # عرض المؤقت
    mins, secs = divmod(int(time_left), 60)
    timer_color = "red" if time_left < 60 else "#2c3e50"
    st.markdown(f'<div class="timer-box" style="color:{timer_color}">{mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)
    
    st.write(f"**Student:** Guest Student")
    st.write("**Subject:** Calculus (Optimization)")
    st.write("**Instructor:** Mr. Ibrahim Eldabour")
    
    if st.button("🔄 Restart Quiz (توليد أسئلة جديدة)"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# --- الجسم الرئيسي (Header & Navigation) ---
st.title("📝 اختبار القيم القصوى (Optimization Quiz)")
st.markdown("---")

if not st.session_state.quiz_submitted:
    # أزرار التنقل في الأعلى
    cols = st.columns(5)
    for i in range(5):
        # تمييز الزر النشط (السؤال الحالي) وتلوين الأزرار المجابة
        btn_label = f"Q {i+1}"
        is_answered = st.session_state.user_answers[i] is not None
        if i == st.session_state.current_q:
            cols[i].markdown(f"<button style='background-color:#2980b9; color:white; border:none; padding:10px; width:100%; border-radius:5px;'>{btn_label}</button>", unsafe_allow_html=True)
        elif is_answered:
            if cols[i].button(f"✅ {btn_label}", key=f"nav_{i}"):
                st.session_state.current_q = i
                st.rerun()
        else:
            if cols[i].button(btn_label, key=f"nav_{i}"):
                st.session_state.current_q = i
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # --- عرض السؤال الحالي ---
    q_index = st.session_state.current_q
    q_data = st.session_state.quiz_data[q_index]

    # بطاقة السؤال
    st.markdown(f"""
    <div class="question-card">
        <div class="ar-text">س{q_index+1}: {q_data['ar']}</div>
        <hr>
        <div class="en-text">Q{q_index+1}: {q_data['en']}</div>
    </div>
    """, unsafe_allow_html=True)

    # حقل الإدخال
    # نستخدم قيمة افتراضية محفوظة إذا كان الطالب قد أجاب سابقاً
    prev_ans = st.session_state.user_answers[q_index]
    val = prev_ans if prev_ans is not None else 0.0
    
    user_input = st.number_input(
        f"Enter Answer / أدخل الإجابة ({q_data['unit']}):", 
        value=float(val), 
        step=0.1, 
        format="%.2f",
        key=f"input_{q_index}"
    )

    # زر حفظ الإجابة والانتقال
    col_prev, col_next = st.columns([1, 1])
    
    if col_next.button("Save & Next ➡️"):
        st.session_state.user_answers[q_index] = user_input
        if q_index < 4:
            st.session_state.current_q += 1
        st.rerun()

    # زر الإنهاء
    st.markdown("---")
    if st.button("📤 Submit Quiz / تسليم الاختبار", type="primary"):
        # حفظ الإجابة الحالية أولاً
        st.session_state.user_answers[q_index] = user_input
        st.session_state.quiz_submitted = True
        st.rerun()

else:
    # --- شاشة النتائج (بعد التسليم أو انتهاء الوقت) ---
    st.success("تم تسليم الاختبار بنجاح! | Quiz Submitted Successfully")
    
    score = 0
    st.write("### تقرير النتيجة:")
    
    for i, q in enumerate(st.session_state.quiz_data):
        user_ans = st.session_state.user_answers[i]
        correct_ans = q['correct']
        
        # السماح بنسبة خطأ بسيطة في التقريب (Tolerance)
        is_correct = False
        if user_ans is not None:
            if abs(user_ans - correct_ans) <= 0.2: # هامش خطأ بسيط
                score += 1
                is_correct = True
        
        # عرض حالة السؤال (بدون الإجابة الصحيحة)
        status = "✅ Correct" if is_correct else "❌ Incorrect"
        st.markdown(f"**Question {i+1}:** {status}")
    
    final_grade = (score / 5) * 100
    st.markdown(f"""
    <div style="background-color:#d4edda; padding:20px; border-radius:10px; text-align:center; border:2px solid #28a745;">
        <h1 style="color:#155724; margin:0;">Your Score: {score} / 5</h1>
        <h3 style="color:#155724;">Grade: {final_grade}%</h3>
    </div>
    """, unsafe_allow_html=True)
    
    if final_grade == 100:
        st.balloons()
