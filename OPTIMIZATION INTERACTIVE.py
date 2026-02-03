import streamlit as st
import random
import time

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Optimization Quiz", layout="wide")

# --- CSS: فقط لتنسيق الاتجاهات (بدون التدخل في المعادلات) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
    }

    /* تنسيق خاص للنص العربي ليكون يمين-يسار */
    .ar-text {
        direction: rtl;
        text-align: right;
        font-size: 20px;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 10px;
    }

    /* تنسيق الإجابات */
    .stRadio label {
        font-size: 20px !important;
        background-color: #f8f9fa;
        padding: 10px 20px;
        border-radius: 8px;
        border: 1px solid #ddd;
        margin-bottom: 5px;
    }
    
    /* صندوق المؤقت */
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
    
    # 1. Open Box
    s_box = random.choice([12, 18, 24, 30])
    ans_box = s_box / 6
    questions.append({
        # نستخدم r"" (Raw String) لضمان قراءة الرموز الرياضية
        "ar": fr"صفيحة مربعة طول ضلعها {s_box} cm. قُصت مربعات من الأركان طول ضلعها $x$. أوجد قيمة $x$ ليكون الحجم $V$ أكبر ما يمكن.",
        "en": fr"A square sheet of side {s_box} cm. Squares of side $x$ are cut from corners. Find $x$ that maximizes the Volume $V$.",
        "correct": ans_box,
        "options": generate_distractors(ans_box, 1),
        "unit": "cm"
    })

    # 2. Shortest Distance
    k_val = random.choice([2, 3, 4, 5])
    ans_dist = k_val - 0.5
    questions.append({
        "ar": fr"أوجد الإحداثي السيني ($x$-coordinate) للنقطة الواقعة على المنحنى $y = \sqrt{{x}}$ الأقرب للنقطة $({k_val}, 0)$.",
        "en": fr"Find the $x$-coordinate on the curve $y = \sqrt{{x}}$ that is closest to the point $({k_val}, 0)$.",
        "correct": ans_dist,
        "options": generate_distractors(ans_dist, 0.5),
        "unit": ""
    })

    # 3. River Fence
    p_river = random.randrange(800, 1600, 200)
    ans_area = (p_river/4) * (p_river/2)
    questions.append({
        "ar": fr"مزارع لديه {p_river} ft من السياج لإحاطة حقل بجوار نهر. أوجد أكبر مساحة ممكنة $A$.",
        "en": fr"A farmer has {p_river} ft of fence next to a river. Find the maximum area $A$.",
        "correct": ans_area,
        "options": generate_distractors(ans_area, 500),
        "unit": "ft²"
    })

    # 4. Inscribed Rectangle
    r_circle = random.randint(6, 12)
    ans_rect = 2 * (r_circle**2)
    questions.append({
        "ar": fr"أوجد أكبر مساحة لمستطيل داخل دائرة نصف قطرها $r = {r_circle}$.",
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
        "ar": fr"مساحة منطقة ${area} \text{{ ft}}^2$. تكلفة الجانبين $3\$ والآخرين $2\$. أوجد أقل تكلفة.",
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

# --- Sidebar ---
with st.sidebar:
    st.markdown("### ⏳ Time")
    mins, secs = divmod(int(remaining), 60)
    st.markdown(f'<div class="timer-box">{mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)
    st.markdown("---")
    if st.button("🔄 New Quiz"):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()

# --- التطبيق الرئيسي ---
st.title("📝 Optimization Quiz")
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

    # 2. عرض السؤال (استخدام حاوية Streamlit الأصلية لضمان عمل المعادلات)
    q_idx = st.session_state.current_q
    q_data = st.session_state.quiz_data[q_idx]

    # الحاوية ذات الإطار (The Box)
    with st.container(border=True):
        # القسم العربي
        st.markdown(f'<div class="ar-text">س{q_idx+1}: {q_data["ar"]}</div>', unsafe_allow_html=True)
        # لاحظ: في العربي قد نحتاج لتعديل بسيط إذا لم تظهر المعادلات، لكن التركيز هنا على الإنجليزي كما طلبت
        
        st.divider()
        
        # القسم الإنجليزي (Native Markdown)
        # هذا هو الأهم: نستخدم st.markdown مباشرة لضمان ظهور المعادلات الإنجليزية بشكل صحيح 100%
        st.markdown(f"**Q{q_idx+1}:** {q_data['en']}")

    # 3. الاختيارات
    st.write("")
    st.info("👇 Select Answer:")
    
    opts = q_data['options']
    opts_labels = [f"{o} {q_data['unit']}" for o in opts]
    prev = st.session_state.user_answers[q_idx]
    
    idx = opts_labels.index(prev) if prev in opts_labels else None
    
    choice = st.radio("Options", opts_labels, index=idx, key=f"q{q_idx}", label_visibility="collapsed")

    # 4. حفظ وتسليم
    c1, c2 = st.columns([1, 4])
    if c1.button("💾 Save", use_container_width=True):
        st.session_state.user_answers[q_idx] = choice
        if q_idx < 4:
            st.session_state.current_q += 1
            st.rerun()
            
    st.markdown("---")
    if st.button("🚀 Submit Final", type="primary"):
        st.session_state.user_answers[q_idx] = choice
        st.session_state.submitted = True
        st.rerun()

else:
    # --- النتائج ---
    st.balloons()
    score = 0
    st.markdown("## 📊 Results")
    
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
                st.write(f"Correct: {correct_val} {q['unit']}")

    st.success(f"Final Score: {score} / 5")
