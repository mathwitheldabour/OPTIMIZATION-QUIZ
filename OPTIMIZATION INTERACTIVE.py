import streamlit as st
import random
import time

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Optimization Quiz | Mr. Ibrahim", layout="wide")

# --- CSS: الإصلاح الجذري للمعادلات والتنسيق ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    
    /* تعميم الخط */
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
    }

    /* ----------------------------------------------------
       FIX: إجبار المعادلات الرياضية أن تكون دائماً من اليسار لليمين
       حتى لو كانت داخل نص عربي
    ---------------------------------------------------- */
    .katex, .katex-display {
        direction: ltr !important;
        unicode-bidi: isolate !important;
        font-family: 'KaTeX_Main', 'Times New Roman', serif !important;
        font-size: 1.1em !important; /* تكبير المعادلات قليلاً */
    }

    /* حيلة العناوين للنص العربي (Header Hack) */
    h5 {
        direction: rtl;
        text-align: right;
        font-family: 'Cairo', sans-serif;
        font-weight: 700;
        font-size: 24px !important; /* تكبير الخط العربي */
        color: #2c3e50;
        line-height: 1.8;
        padding-right: 15px;
        border-right: 6px solid #2980b9;
        margin-bottom: 15px;
    }
    
    /* تنسيق النص الإنجليزي - تكبير وتوضيح */
    .en-text {
        text-align: left;
        direction: ltr;
        font-family: 'Segoe UI', Arial, sans-serif; /* خط أوضح للإنجليزي */
        font-size: 20px; /* تكبير الخط */
        font-weight: 500;
        color: #444;
        margin-top: 10px;
        padding: 15px;
        background-color: #f8f9fa; /* خلفية خفيفة جداً لتمييزه */
        border-left: 6px solid #c0392b;
        border-radius: 5px;
    }

    /* بطاقة السؤال */
    .question-card {
        background-color: #fff;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border: 1px solid #e1e1e1;
        margin-bottom: 25px;
    }

    /* تحسين أزرار الراديو */
    .stRadio label {
        font-size: 22px !important; /* تكبير الاختيارات */
        background-color: #ffffff;
        padding: 15px 20px;
        border-radius: 10px;
        border: 2px solid #eee;
        margin-bottom: 10px;
        cursor: pointer;
        transition: all 0.2s;
        display: block;
        direction: ltr; /* الاختيارات (أرقام) تكون من اليسار لليمين */
        text-align: left;
        font-weight: bold;
        color: #2c3e50;
    }
    .stRadio label:hover {
        border-color: #3498db;
        background-color: #f0f8ff;
    }

    /* المؤقت */
    .timer-box {
        font-size: 30px; font-weight: 800; text-align: center;
        padding: 15px; border: 3px solid #e74c3c; border-radius: 12px;
        color: #e74c3c; background: white;
    }
    
    /* إخفاء روابط التثبيت المزعجة */
    a.anchor-link { display: none; }
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
    
    # 1. Open Box
    s_box = random.choice([12, 18, 24, 30])
    ans_box = s_box / 6
    questions.append({
        # المعادلات مكتوبة بصيغة LaTeX بين علامات $
        "ar": fr"صفيحة مربعة الشكل طول ضلعها ${s_box} \text{{ cm}}$. قُصت مربعات متطابقة من الأركان طول ضلعها $x$. أوجد قيمة $x$ التي تجعل حجم الصندوق $V$ أكبر ما يمكن.",
        "en": fr"A square sheet of side ${s_box} \text{{ cm}}$. Squares of side $x$ are cut from corners. Find $x$ that maximizes the Volume $V$.",
        "correct": ans_box,
        "options": generate_distractors(ans_box, 1),
        "unit": "cm"
    })

    # 2. Shortest Distance (تم تعديل المعادلة لتكون واضحة)
    k_val = random.choice([2, 3, 4, 5])
    ans_dist = k_val - 0.5
    questions.append({
        "ar": fr"أوجد الإحداثي السيني ($x$-coordinate) للنقطة الواقعة على المنحنى $y = \sqrt{{x}}$ والتي تكون أقرب ما يمكن للنقطة $({k_val}, 0)$.",
        "en": fr"Find the $x$-coordinate on the curve $y = \sqrt{{x}}$ that is closest to the point $({k_val}, 0)$.",
        "correct": ans_dist,
        "options": generate_distractors(ans_dist, 0.5),
        "unit": ""
    })

    # 3. River Fence
    p_river = random.randrange(800, 1600, 200)
    ans_area = (p_river/4) * (p_river/2)
    questions.append({
        "ar": fr"مزارع لديه ${p_river} \text{{ ft}}$ من السياج لإحاطة حقل مستطيل بجوار نهر (لا يحتاج سياج). أوجد أكبر مساحة ممكنة $A$.",
        "en": fr"A farmer has ${p_river} \text{{ ft}}$ of fence next to a river. Find the maximum area $A$.",
        "correct": ans_area,
        "options": generate_distractors(ans_area, 500),
        "unit": "ft²"
    })

    # 4. Inscribed Rectangle
    r_circle = random.randint(6, 12)
    ans_rect = 2 * (r_circle**2)
    questions.append({
        "ar": fr"أوجد أكبر مساحة لمستطيل يمكن رسمه داخل دائرة نصف قطرها $r = {r_circle}$.",
        "en": fr"Find max area of a rectangle inscribed in a circle with radius $r = {r_circle}$.",
        "correct": ans_rect,
        "options": generate_distractors(ans_rect, 10),
        "unit": "units²"
    })

    # 5. Min Cost
    base_u = random.choice([10, 20])
    area = int(1.5 * base_u**2)
    cost = 12 * base_u
    questions.append({
        "ar": fr"يراد تسييج منطقة مساحتها ${area} \text{{ ft}}^2$. تكلفة الجانبين المتقابلين $3\$ والآخرين $2\$. أوجد أقل تكلفة.",
        "en": fr"Area is ${area} \text{{ ft}}^2$. Two sides cost $3\$$, others $2\$$. Find min cost.",
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
    # 1. شريط التنقل
    cols = st.columns(5)
    for i in range(5):
        done = st.session_state.user_answers[i] is not None
        active = (i == st.session_state.current_q)
        label = f"Q{i+1}"
        if done: label += " ✅"
        type_btn = "primary" if active else "secondary"
        if cols[i].button(label, key=f"nav_{i}", type=type_btn, use_container_width=True):
            st.session_state.current_q = i
            st.rerun()

    # 2. عرض السؤال الحالي
    q_idx = st.session_state.current_q
    q_data = st.session_state.quiz_data[q_idx]

    # الحاوية الرئيسية
    with st.container():
        st.markdown('<div class="question-card">', unsafe_allow_html=True)
        
        # العربي - المعادلات ستظهر الآن من اليسار لليمين بفضل CSS
        st.markdown(f"##### س{q_idx+1}: {q_data['ar']}")
        
        # الإنجليزي - خط أكبر وخلفية مميزة
        st.markdown(f"""
        <div class="en-text">
            <strong>Q{q_idx+1}:</strong> {q_data['en']}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # 3. الاختيارات
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("👇 Select the correct answer / اختر الإجابة الصحيحة:")
    
    opts = q_data['options']
    opts_labels = [f"{o} {q_data['unit']}" for o in opts]
    
    prev = st.session_state.user_answers[q_idx]
    idx_sel = opts_labels.index(prev) if prev in opts_labels else None

    choice = st.radio(
        "Hidden Label",
        opts_labels,
        index=idx_sel,
        key=f"q_{q_idx}",
        label_visibility="collapsed"
    )

    # 4. الأزرار
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
        st.session_state.user_answers[q_idx] = choice 
        st.session_state.submitted = True
        st.rerun()

else:
    # --- النتائج ---
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
        
        status_icon = "✅" if is_correct else "❌"
        
        with st.expander(f"Question {i+1}: {status_icon}"):
            st.markdown(f"**Question:** {q['en']}")
            st.markdown(f"**Your Answer:** {user_ans}")
            if not is_correct:
                st.markdown(f"**Correct Answer:** {correct_val} {q['unit']}")

    final = (score/5)*100
    st.markdown(f"""
    <div style="background:#2c3e50; color:white; padding:30px; border-radius:15px; text-align:center; margin-top:20px;">
        <h1>Final Score</h1>
        <h2 style="font-size: 50px; margin: 10px 0;">{score} / 5</h2>
        <h3>({final}%)</h3>
    </div>
    """, unsafe_allow_html=True)
