import streamlit as st
import random
import time

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Optimization Quiz", layout="wide")

# --- CSS: العزل والفصل (Isolation Strategy) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
    }

    /* 1. تخصيص h4 ليكون الحاوية العربية الآمنة */
    h4 {
        direction: rtl !important;
        text-align: right !important;
        font-family: 'Cairo', sans-serif !important;
        color: #1f77b4 !important;
        font-weight: 700 !important;
        margin-bottom: 15px !important;
        line-height: 1.8 !important;
    }

    /* 2. حماية المعادلات داخل العربي (The Critical Fix) */
    /* نجبر المعادلة أن تكون LTR دائماً ومعزولة عن سياق العربي */
    h4 .katex {
        direction: ltr !important;
        unicode-bidi: isolate !important;
    }

    /* 3. تنسيق الإنجليزي (يبقى LTR كما هو) */
    .en-box {
        background-color: #f4f6f8;
        padding: 15px;
        border-left: 5px solid #ff4b4b;
        border-radius: 5px;
        margin-top: 10px;
    }
    
    /* 4. تنسيق عام */
    .stRadio label {
        direction: ltr; /* الاختيارات أرقام، فتكون يسار-يمين */
        text-align: left;
        font-size: 18px !important;
        background: #fff;
        padding: 10px;
        border: 1px solid #eee;
        border-radius: 8px;
    }
    
    /* إخفاء الروابط بجانب العناوين */
    a.anchor-link { display: none !important; }
    .css-1629p8f h4 a { display: none !important; }
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
        "ar": fr"صفيحة مربعة طول ضلعها ${s_box}\text{{ cm}}$. قُصت مربعات متطابقة من الأركان طول ضلعها $x$. أوجد قيمة $x$ لتجعل الحجم $V$ أكبر ما يمكن.",
        "en": fr"A square sheet of side ${s_box}\text{{ cm}}$. Squares of side $x$ are cut from corners. Find $x$ that maximizes the Volume $V$.",
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
        "ar": fr"مزارع لديه ${p_river}\text{{ ft}}$ من السياج لإحاطة حقل بجوار نهر. أوجد أكبر مساحة ممكنة $A$.",
        "en": fr"A farmer has ${p_river}\text{{ ft}}$ of fence next to a river. Find the maximum area $A$.",
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
        "ar": fr"منطقة مساحتها ${area}\text{{ ft}}^2$. تكلفة الجانبين $3\$ والآخرين $2\$. أوجد أقل تكلفة.",
        "en": fr"Area is ${area}\text{{ ft}}^2$. Two sides cost $3\$$, others $2\$$. Find min cost.",
        "correct": cost,
        "options": generate_distractors(cost, 20),
        "unit": "$"
    })

    return questions

# --- Session Management ---
if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = generate_questions()
    st.session_state.user_answers = [None] * 5
    st.session_state.current_q = 0
    st.session_state.start_time = time.time()
    st.session_state.submitted = False

# --- Timer ---
DURATION = 15 * 60
remaining = max(0, DURATION - (time.time() - st.session_state.start_time))
if remaining == 0 and not st.session_state.submitted:
    st.session_state.submitted = True
    st.rerun()

# --- Sidebar ---
with st.sidebar:
    st.metric("Timer", f"{int(remaining)//60:02}:{int(remaining)%60:02}")
    if st.button("Reset Quiz"):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()

# --- Main Page ---
st.title("📝 Optimization Quiz")
st.markdown("---")

if not st.session_state.submitted:
    # Navigation
    cols = st.columns(5)
    for i in range(5):
        done = st.session_state.user_answers[i] is not None
        btn_type = "primary" if i == st.session_state.current_q else "secondary"
        if cols[i].button(f"Q{i+1}" + (" ✅" if done else ""), key=f"n{i}", type=btn_type, use_container_width=True):
            st.session_state.current_q = i
            st.rerun()

    q_idx = st.session_state.current_q
    q_data = st.session_state.quiz_data[q_idx]

    # --- منطقة السؤال (The Question Box) ---
    with st.container(border=True):
        
        # 1. العربي: نستخدم h4 الذي برمجناه ليكون RTL مع حماية المعادلات
        st.markdown(f"#### س{q_idx+1}: {q_data['ar']}")
        
        # 2. الإنجليزي: نستخدم Markdown طبيعي لضمان سلامة المعادلات 100%
        # ونحيطه بـ success box لتمييزه
        st.success(f"**Q{q_idx+1}:** {q_data['en']}")

    # --- الاختيارات ---
    st.write("")
    st.info("👇 Select Answer:")
    opts = q_data['options']
    opts_labels = [f"{o} {q_data['unit']}" for o in opts]
    prev = st.session_state.user_answers[q_idx]
    idx = opts_labels.index(prev) if prev in opts_labels else None
    
    choice = st.radio("Options", opts_labels, index=idx, key=f"rad{q_idx}", label_visibility="collapsed")

    # --- التحكم ---
    c1, c2 = st.columns([1, 4])
    if c1.button("💾 Save Answer", use_container_width=True):
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
    st.header("📊 Results")
    for i, q in enumerate(st.session_state.quiz_data):
        u_ans = st.session_state.user_answers[i]
        corr = q['correct']
        is_correct = False
        if u_ans:
            val = float(u_ans.split()[0])
            if abs(val - corr) < 0.1:
                is_correct = True
                score += 1
        
        icon = "✅" if is_correct else "❌"
        with st.expander(f"Q{i+1}: {icon}"):
            st.markdown(q['en'])
            st.write(f"Your: {u_ans} | Correct: {corr} {q['unit']}")
    
    st.success(f"Final Score: {score}/5")
