import streamlit as st
import random
import time

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Optimization Quiz", layout="wide")

# --- CSS: الإصلاح النهائي (The Final Fix) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
    }

    /* 1. إصلاح اتجاه المعادلات داخل النص العربي */
    /* نجبر العنصر الرياضي أن يكون معزولاً واتجاهه يسار-يمين دائماً */
    .katex {
        direction: ltr !important;
        unicode-bidi: isolate !important;
        font-family: 'Times New Roman', serif !important;
    }

    /* 2. تخصيص العنوان h4 ليكون هو "النص العربي" */
    /* Streamlit يعالج المعادلات في العناوين بشكل ممتاز، لذا سنستغله */
    h4 {
        direction: rtl !important;
        text-align: right !important;
        font-family: 'Cairo', sans-serif !important;
        font-weight: 700 !important;
        font-size: 22px !important;
        color: #1f77b4 !important; /* لون أزرق مميز */
        margin-bottom: 10px !important;
        line-height: 1.6 !important;
    }
    
    /* إخفاء رابط التثبيت الصغير بجانب العنوان */
    .css-1629p8f h4 a, .css-1629p8f h4 a:hover {
        display: none !important;
    }
    a.anchor-link { display: none !important; }

    /* 3. تنسيق النص الإنجليزي */
    .en-container {
        text-align: left;
        direction: ltr;
        background-color: #f8f9fa;
        padding: 15px;
        border-left: 5px solid #ff4b4b;
        border-radius: 5px;
        margin-bottom: 20px;
        font-family: 'Segoe UI', sans-serif;
        font-size: 18px;
        color: #333;
    }

    /* 4. تنسيق الخيارات */
    .stRadio label {
        direction: ltr; /* الأرقام والوحدات من اليسار لليمين */
        text-align: left;
        font-size: 20px !important;
        background-color: white;
        padding: 10px 15px;
        border-radius: 8px;
        border: 1px solid #ddd;
        margin-bottom: 8px;
    }

    /* المؤقت */
    .timer-box {
        font-size: 24px; font-weight: bold; text-align: center;
        padding: 10px; border: 2px solid #e74c3c; border-radius: 8px;
        color: #e74c3c;
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
    
    # ملاحظة هامة: نستخدم fr"" (f-string + raw string) 
    # لضمان عدم تداخل الأقواس والمعادلات
    
    # 1. Open Box
    s_box = random.choice([12, 18, 24, 30])
    ans_box = s_box / 6
    questions.append({
        # نستخدم h4 للعربي (تم تعديله بالـ CSS)
        "ar": fr"صفيحة مربعة الشكل طول ضلعها ${s_box}\text{{ cm}}$. قُصت مربعات متطابقة من الأركان طول ضلعها $x$. أوجد قيمة $x$ التي تجعل الحجم $V$ أكبر ما يمكن.",
        "en": fr"A square sheet of side ${s_box}\text{{ cm}}$. Squares of side $x$ are cut from corners. Find $x$ that maximizes the Volume $V$.",
        "correct": ans_box,
        "options": generate_distractors(ans_box, 1),
        "unit": "cm"
    })

    # 2. Shortest Distance
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
        "ar": fr"مزارع لديه ${p_river}\text{{ ft}}$ من السياج لإحاطة حقل مستطيل بجوار نهر (لا يحتاج سياج). أوجد أكبر مساحة ممكنة $A$.",
        "en": fr"A farmer has ${p_river}\text{{ ft}}$ of fence next to a river. Find the maximum area $A$.",
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
        "ar": fr"يراد تسييج منطقة مساحتها ${area}\text{{ ft}}^2$. تكلفة الجانبين المتقابلين $3\$ والآخرين $2\$. أوجد أقل تكلفة.",
        "en": fr"Area is ${area}\text{{ ft}}^2$. Two sides cost $3\$$, others $2\$$. Find min cost.",
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
    st.markdown(f'<div class="timer-box">{mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)
    st.markdown("---")
    if st.button("🔄 Reset Quiz"):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()

# --- التطبيق الرئيسي ---
st.title("📝 Optimization & Calculus Quiz")
st.markdown("---")

if not st.session_state.submitted:
    # 1. التنقل
    cols = st.columns(5)
    for i in range(5):
        done = st.session_state.user_answers[i] is not None
        active = (i == st.session_state.current_q)
        label = f"Q{i+1}" + (" ✅" if done else "")
        if cols[i].button(label, key=f"n{i}", type="primary" if active else "secondary", use_container_width=True):
            st.session_state.current_q = i
            st.rerun()

    # 2. عرض السؤال الحالي
    q_idx = st.session_state.current_q
    q_data = st.session_state.quiz_data[q_idx]

    # نستخدم الحاوية لتجميع السؤال
    with st.container(border=True):
        # --- السؤال العربي ---
        # نستخدم #### (h4) لأننا قمنا بتعديل خصائصه في CSS ليصبح يمين-يسار
        # هذا يخدع Streamlit ليقوم بمعالجة المعادلات (LaTeX) بشكل صحيح
        st.markdown(f"#### س{q_idx+1}: {q_data['ar']}")

        # --- السؤال الإنجليزي ---
        # نستخدم HTML عادي لأنه لا يحتاج معالجة خاصة للاتجاه، والمعادلات ستظهر جيداً
        st.markdown(f"""
        <div class="en-container">
            <strong>Q{q_idx+1}:</strong> {q_data['en']}
        </div>
        """, unsafe_allow_html=True)

    # 3. الاختيارات
    st.write("")
    st.info("👇 Select the correct answer:")
    
    opts = q_data['options']
    opts_labels = [f"{o} {q_data['unit']}" for o in opts]
    prev = st.session_state.user_answers[q_idx]
    
    idx = opts_labels.index(prev) if prev in opts_labels else None
    
    choice = st.radio("Options", opts_labels, index=idx, key=f"q{q_idx}", label_visibility="collapsed")

    # 4. الحفظ والتسليم
    c1, c2 = st.columns([1, 4])
    if c1.button("💾 Save Answer", use_container_width=True):
        st.session_state.user_answers[q_idx] = choice
        if q_idx < 4:
            st.session_state.current_q += 1
            st.rerun()
            
    st.markdown("---")
    if st.button("🚀 Submit Final Quiz", type="primary"):
        st.session_state.user_answers[q_idx] = choice
        st.session_state.submitted = True
        st.rerun()

else:
    # --- النتائج ---
    st.balloons()
    score = 0
    st.markdown("## 📊 Quiz Results")
    
    for i, q in enumerate(st.session_state.quiz_data):
        user_ans = st.session_state.user_answers[i]
        correct_val = q['correct']
        
        is_correct = False
        if user_ans:
            val = float(user_ans.split()[0])
            if abs(val - correct_val) < 0.1:
                is_correct = True
                score += 1
        
        icon = "✅" if is_correct else "❌"
        
        with st.expander(f"Q{i+1}: {icon}"):
            st.markdown(f"**Question:** {q['en']}")
            st.write(f"Your Answer: {user_ans}")
            if not is_correct:
                st.write(f"Correct Answer: {correct_val} {q['unit']}")

    st.success(f"Final Score: {score} / 5")
