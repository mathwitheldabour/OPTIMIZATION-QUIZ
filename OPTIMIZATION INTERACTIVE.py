import streamlit as st
import random
import time

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Optimization Quiz | Mr. Ibrahim", layout="wide")

# --- CSS: السحر الجمالي والتنسيق ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    
    /* تعميم الخط */
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
    }

    /* بطاقة السؤال */
    .question-card {
        background: linear-gradient(to right, #ffffff, #f9fbfd);
        padding: 30px;
        border-radius: 15px;
        border-top: 6px solid #2980b9; /* شريط علوي ملون */
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-bottom: 25px;
    }

    /* تنسيق النصوص داخل السؤال */
    .ar-text {
        text-align: right; direction: rtl;
        font-size: 22px; font-weight: 700; color: #2c3e50;
        margin-bottom: 15px;
        line-height: 1.6;
    }
    .en-text {
        text-align: left; direction: ltr;
        font-size: 18px; color: #555;
        font-family: 'Segoe UI', sans-serif;
        margin-bottom: 5px;
        padding-left: 15px;
        border-left: 4px solid #bdc3c7;
    }

    /* صندوق الاختيارات (The Options Box) */
    .options-box {
        background-color: #eaf2f8; /* خلفية زرقاء فاتحة جداً */
        border: 2px solid #a9cce3;
        border-radius: 12px;
        padding: 20px;
        margin-top: 10px;
    }
    .options-header {
        font-weight: bold; color: #2980b9; margin-bottom: 10px; font-size: 18px;
    }

    /* تحسين شكل الراديو (الاختيارات) */
    .stRadio > div {
        background-color: transparent;
    }
    .stRadio label {
        font-size: 20px !important;
        background-color: white;
        padding: 10px 15px;
        border-radius: 8px;
        margin-bottom: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border: 1px solid #eee;
        transition: all 0.3s;
    }
    .stRadio label:hover {
        border-color: #3498db;
        background-color: #fdfdfd;
    }

    /* صندوق المؤقت */
    .timer-box {
        font-size: 28px; font-weight: 800; text-align: center;
        padding: 15px; background-color: #fff;
        border: 3px solid #e74c3c; border-radius: 12px;
        color: #e74c3c; box-shadow: 0 4px 10px rgba(231, 76, 60, 0.2);
    }
    
    /* أزرار التنقل */
    .nav-btn {
        width: 100%; border-radius: 8px; font-weight: bold; margin: 2px;
    }
</style>
""", unsafe_allow_html=True)

# --- دوال المساعدة ---
def generate_distractors(correct_val, step=1):
    options = {correct_val}
    while len(options) < 4:
        fake = correct_val + random.choice([-step, step, step*2, -step*2, step*0.5, -step*0.5])
        if fake > 0:
            options.add(round(fake, 2))
    final_opts = list(options)
    random.shuffle(final_opts)
    return final_opts

def generate_questions():
    questions = []
    
    # 1. Open Box (معادلة تربيعية وتكعيبية)
    s_box = random.choice([12, 18, 24, 30])
    ans_box = s_box / 6
    questions.append({
        "ar": f"صفيحة مربعة طول ضلعها {s_box} cm. قُصت مربعات من الأركان طول ضلعها $x$. أوجد قيمة $x$ التي تجعل الحجم $V$ أكبر ما يمكن.",
        "en": f"A square sheet of side {s_box} cm. Squares of side $x$ are cut from corners. Find $x$ that maximizes Volume.",
        "correct": ans_box,
        "options": generate_distractors(ans_box, 1),
        "unit": "cm"
    })

    # 2. Shortest Distance (جذور)
    k_val = random.choice([2, 3, 4, 5])
    ans_dist = k_val - 0.5
    questions.append({
        "ar": f"أوجد الإحداثي السيني $x$ للنقطة الواقعة على المنحنى $y = \\sqrt{{x}}$ والتي تكون أقرب ما يمكن للنقطة $({k_val}, 0)$.",
        "en": f"Find the x-coordinate on the curve $y = \\sqrt{{x}}$ closest to the point $({k_val}, 0)$.",
        "correct": ans_dist,
        "options": generate_distractors(ans_dist, 0.5),
        "unit": ""
    })

    # 3. River Fence
    p_river = random.randrange(800, 1600, 200)
    ans_area = (p_river/4) * (p_river/2)
    questions.append({
        "ar": f"مزارع لديه {p_river} ft من السياج لإحاطة حقل مستطيل بجوار نهر. أوجد أكبر مساحة ممكنة $A$.",
        "en": f"Farmer has {p_river} ft of fence next to a river. Find the maximum area.",
        "correct": ans_area,
        "options": generate_distractors(ans_area, 500),
        "unit": "ft²"
    })

    # 4. Circle Inscribed (هندسة)
    r_circle = random.randint(6, 12)
    ans_rect = 2 * (r_circle**2)
    questions.append({
        "ar": f"أوجد أكبر مساحة لمستطيل يمكن رسمه داخل دائرة نصف قطرها $r = {r_circle}$.",
        "en": f"Find max area of rectangle inscribed in circle with radius $r = {r_circle}$.",
        "correct": ans_rect,
        "options": generate_distractors(ans_rect, 10),
        "unit": "units²"
    })

    # 5. Min Cost
    base_u = random.choice([10, 20])
    area = int(1.5 * base_u**2)
    cost = 12 * base_u
    questions.append({
        "ar": f"يراد تسييج منطقة مساحتها ${area} \\text{{ ft}}^2$. تكلفة الجانبين المتقابلين 3$ والآخرين 2$. أوجد أقل تكلفة.",
        "en": f"Area is ${area} \\text{{ ft}}^2$. Two sides cost $3, others $2. Find min cost.",
        "correct": cost,
        "options": generate_distractors(cost, 20),
        "unit": "$"
    })

    return questions

# --- إدارة الحالة ---
if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = generate_questions()
    st.session_state.user_answers = [None] * 5
    st.session_state.current_q = 0
    st.session_state.start_time = time.time()
    st.session_state.submitted = False

# --- المؤقت ---
DURATION = 15 * 60
elapsed = time.time() - st.session_state.start_time
remaining = max(0, DURATION - elapsed)
if remaining == 0 and not st.session_state.submitted:
    st.session_state.submitted = True
    st.rerun()

# --- الشريط الجانبي ---
with st.sidebar:
    st.markdown("### ⏳ Time Remaining")
    mins, secs = divmod(int(remaining), 60)
    color = "#e74c3c" if remaining < 60 else "#2c3e50"
    st.markdown(f'<div class="timer-box" style="color:{color}">{mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.caption("Advanced Calculus Quiz")
    st.markdown("**Mr. Ibrahim Eldabour**")
    if st.button("🔄 Reset Quiz"):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()

# --- التطبيق الرئيسي ---
st.title("📝 Optimization & Calculus Quiz")
st.markdown("---")

if not st.session_state.submitted:
    # 1. شريط التنقل (Navigation Bar)
    cols = st.columns(5)
    for i in range(5):
        done = st.session_state.user_answers[i] is not None
        active = (i == st.session_state.current_q)
        label = f"Q{i+1}"
        if done: label += " ✅"
        
        # تلوين الزر بناء على حالته
        type_btn = "primary" if active else "secondary"
        if cols[i].button(label, key=f"nav_{i}", type=type_btn, use_container_width=True):
            st.session_state.current_q = i
            st.rerun()

    # 2. عرض السؤال الحالي
    q_idx = st.session_state.current_q
    q_data = st.session_state.quiz_data[q_idx]

    # عرض بطاقة السؤال (HTML + LaTeX Rendered by Streamlit Logic)
    # ملاحظة: نستخدم st.markdown لعرض النصوص مع LaTeX
    st.markdown(f"""
    <div class="question-card">
        <div class="ar-text">س{q_idx+1}: {q_data['ar']}</div>
        <div class="en-text">Q{q_idx+1}: {q_data['en']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # تصحيح عرض المعادلات داخل الـ Markdown (Streamlit يرندر $...$ تلقائياً)
    # لا حاجة لتدخل إضافي لأن النصوص تحتوي بالفعل على $ للصيغ الرياضية

    # 3. صندوق الإجابة (The Answer Box)
    st.markdown('<div class="options-box"><div class="options-header">Select the correct answer / اختر الإجابة الصحيحة:</div>', unsafe_allow_html=True)
    
    opts = q_data['options']
    opts_labels = [f"{o} {q_data['unit']}" for o in opts]
    
    # الاحتفاظ بالإجابة السابقة
    prev = st.session_state.user_answers[q_idx]
    idx_sel = opts_labels.index(prev) if prev in opts_labels else None

    # عرض الراديو بتون
    choice = st.radio(
        "Hidden Label", # نخفي العنوان لأننا وضعنا واحداً مخصصاً
        opts_labels,
        index=idx_sel,
        key=f"q_{q_idx}",
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True) # إغلاق صندوق الخيارات

    # 4. أزرار التحكم
    st.write("")
    c1, c2 = st.columns([1, 4])
    if c1.button("💾 Save Answer", use_container_width=True):
        st.session_state.user_answers[q_idx] = choice
        if q_idx < 4:
            st.session_state.current_q += 1
            st.rerun()
        else:
            st.success("Answer Saved!")

    st.markdown("---")
    if st.button("🚀 Submit Final Quiz", type="primary"):
        st.session_state.user_answers[q_idx] = choice # حفظ السؤال الحالي قبل التسليم
        st.session_state.submitted = True
        st.rerun()

else:
    # --- شاشة النتائج ---
    st.balloons()
    score = 0
    st.markdown("""<h2 style="text-align:center; color:#27ae60;">🎉 Quiz Completed!</h2>""", unsafe_allow_html=True)
    
    for i, q in enumerate(st.session_state.quiz_data):
        user_ans = st.session_state.user_answers[i]
        correct_val = q['correct']
        
        is_correct = False
        if user_ans:
            val = float(user_ans.split()[0])
            if abs(val - correct_val) < 0.1:
                is_correct = True
                score += 1
        
        status_color = "#d4edda" if is_correct else "#f8d7da"
        status_icon = "✅" if is_correct else "❌"
        
        with st.expander(f"Question {i+1}: {status_icon}"):
            st.markdown(f"**Question:** {q['en']}")
            st.markdown(f"**Your Answer:** {user_ans}")
            if not is_correct:
                st.markdown(f"**Correct Answer:** {correct_val} {q['unit']}")

    final = (score/5)*100
    st.markdown(f"""
    <div style="background:#2c3e50; color:white; padding:20px; border-radius:10px; text-align:center; margin-top:20px;">
        <h1>Your Score: {score}/5 ({final}%)</h1>
    </div>
    """, unsafe_allow_html=True)
