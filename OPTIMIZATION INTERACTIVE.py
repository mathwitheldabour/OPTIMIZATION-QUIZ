import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Optimization Problems", layout="wide")

# --- CSS مخصص للطباعة وتنسيق النصوص ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
    }
    
    .question-container {
        border: 2px solid #2980b9;
        padding: 20px;
        border-radius: 10px;
        background-color: #fdfdfd;
        margin-bottom: 20px;
    }
    .ar-text {
        text-align: right;
        direction: rtl;
        font-size: 20px;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 10px;
    }
    .en-text {
        text-align: left;
        direction: ltr;
        font-size: 18px;
        color: #34495e;
        margin-bottom: 10px;
        font-family: 'Segoe UI', sans-serif;
    }
    
    /* إخفاء العناصر غير المرغوبة عند الطباعة */
    @media print {
        [data-testid="stSidebar"] { display: none; }
        .stButton { display: none; }
        header { display: none; }
        footer { display: none; }
        .block-container { padding-top: 0 !important; }
        .question-container { border: 2px solid #000; }
    }
</style>
""", unsafe_allow_html=True)

# --- البيانات (الأسئلة) ---
questions = {
    "Q3: Rectangular Field & Stream": {
        "ar": "3. حقل مستطيل الشكل سيتم إحاطته بسياج من ثلاثة جوانب، وجانب رابع يقع على طول مجرى مائي مستقيم. أوجد أبعاد الحقل التي تعطي أكبر مساحة ممكنة باستخدام سياج طوله 1000 قدم.",
        "en": "3. A rectangular field is to be bounded by a fence on three sides and by a straight stream on the fourth side. Find the dimensions of the field with maximum area using 1000 ft of fence.",
        "type": "river_rect",
        "constraint": 1000,
        "answer": "Dimensions: 250 ft × 500 ft | Max Area: 125,000 ft²"
    },
    "Q9: Rectangle in Circle": {
        "ar": "9. أوجد أبعاد المستطيل ذو أكبر مساحة ممكنة والذي يمكن رسمه داخل دائرة نصف قطرها 10 وحدات.",
        "en": "9. Find the dimensions of the rectangle with maximum area that can be inscribed in a circle of radius 10.",
        "type": "rect_in_circle",
        "constraint": 10,
        "answer": "Dimensions: 10√2 × 10√2 (Square) | Max Area: 200"
    },
    "Q14: Wire Cut (Circle & Square)": {
        "ar": "14. سلك طوله 12 إنش، يمكن ثنيه ليشكل دائرة ومربعاً. كم يجب أن يكون طول السلك المستخدم للدائرة لتكون المساحة الكلية (a) أكبر ما يمكن؟",
        "en": "14. A wire of length 12 in is cut to make a circle and a square. How much wire for the circle for (a) Maximum total area?",
        "type": "wire_cut",
        "constraint": 12,
        "answer": "Use all 12 inches for the circle (x = 12, Square side = 0)"
    }
}

# --- القائمة الجانبية ---
st.sidebar.title("🧮 Optimization Problems")
st.sidebar.markdown("Mr. Ibrahim Eldabour")
selected_q = st.sidebar.selectbox("Select Question", list(questions.keys()))
data = questions[selected_q]

# --- العنوان ---
st.markdown("<h2 style='text-align: center; color: #d35400;'>تطبيقات القيم القصوى (Optimization)</h2>", unsafe_allow_html=True)
st.markdown("---")

# --- تصميم الصفحة (عمودين: نص ورسم) ---
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown(f"""
    <div class="question-container">
        <div class="ar-text">{data['ar']}</div>
        <hr>
        <div class="en-text">{data['en']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.checkbox("Show Final Answer / عرض الإجابة النهائية"):
        st.success(data['answer'])

    st.info("💡 Tip: Press `Ctrl + P` (or Cmd + P) to save this page as a PDF without the sidebar.")

# --- دوال الرسم (Visualization) ---
def plot_river_rect(perimeter):
    fig, ax = plt.subplots(figsize=(6, 4))
    
    # النهر
    ax.axhline(0, color='blue', linewidth=4, label='Stream (River)')
    
    # المستطيل المثالي (الحل)
    # 2x + y = 1000 => x=250, y=500
    opt_x = perimeter / 4
    opt_y = perimeter / 2
    
    rect = patches.Rectangle((100, 0), opt_y, opt_x, linewidth=2, edgecolor='green', facecolor='#abebc6', label='Field')
    ax.add_patch(rect)
    
    # التسميات
    ax.text(100 + opt_y/2, opt_x + 20, f'Side y = {opt_y}', ha='center', fontsize=12, color='green')
    ax.text(80, opt_x/2, f'x = {opt_x}', va='center', fontsize=12, color='green')
    ax.text(100 + opt_y + 20, opt_x/2, f'x = {opt_x}', va='center', fontsize=12, color='green')
    
    ax.set_xlim(0, perimeter)
    ax.set_ylim(-50, perimeter/2)
    ax.set_aspect('equal')
    ax.legend(loc='upper right')
    ax.set_title(f"Optimization: Fence Length = {perimeter} ft")
    ax.axis('off')
    return fig

def plot_rect_in_circle(radius):
    fig, ax = plt.subplots(figsize=(5, 5))
    
    # الدائرة
    circle = plt.Circle((0, 0), radius, color='blue', fill=False, linewidth=2, label=f'Circle r={radius}')
    ax.add_patch(circle)
    
    # المستطيل (المربع هو الحل الأمثل)
    side = radius * np.sqrt(2) # 14.14
    rect = patches.Rectangle((-side/2, -side/2), side, side, linewidth=2, edgecolor='red', facecolor='#fadbd8', label='Max Area Rectangle')
    ax.add_patch(rect)
    
    # رسم نصف القطر
    ax.plot([0, side/2], [0, side/2], 'k--', label='Radius')
    
    ax.set_xlim(-radius-2, radius+2)
    ax.set_ylim(-radius-2, radius+2)
    ax.set_aspect('equal')
    ax.legend(loc='upper right')
    ax.set_title("Rectangle Inscribed in Circle")
    ax.axis('off')
    return fig

def plot_wire_cut(length):
    fig, ax = plt.subplots(figsize=(6, 2))
    
    # السلك كامل
    ax.plot([0, length], [0, 0], 'k-', linewidth=3, label='Total Wire')
    
    # نقطة القطع (الحل a: الكل للدائرة)
    # سنرسم تمثيل للدائرة والمربع
    
    circle_r = (length / (2*np.pi)) 
    
    # رسم الدائرة الناتجة
    circle = plt.Circle((2, 0.5), 0.5, color='blue', fill=True, label='Circle Part')
    ax.add_patch(circle)
    ax.text(2, -0.5, "Circle Mode", ha='center')
    
    # رسم المربع (صغير جداً لأن الحل a يطلب تعظيم المساحة للدائرة)
    rect = patches.Rectangle((8, 0), 1, 1, color='red', fill=True, label='Square Part')
    ax.add_patch(rect)
    ax.text(8.5, -0.5, "Square Mode", ha='center')

    ax.set_xlim(-1, length+1)
    ax.set_ylim(-1, 2)
    ax.axis('off')
    ax.set_title(f"Wire Length = {length} in")
    return fig

# --- عرض الرسم البياني ---
with col2:
    st.markdown("### 📊 Geometric Representation")
    if data['type'] == "river_rect":
        fig = plot_river_rect(data['constraint'])
        st.pyplot(fig)
    elif data['type'] == "rect_in_circle":
        fig = plot_rect_in_circle(data['constraint'])
        st.pyplot(fig)
    elif data['type'] == "wire_cut":
        fig = plot_wire_cut(data['constraint'])
        st.pyplot(fig)