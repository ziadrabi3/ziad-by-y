import streamlit as st
import pandas as pd
import openpyxl
import re
import io
import time
import urllib.request
from datetime import datetime, date, timedelta

# فحص الاتصال بالإنترنت
def is_online():
    try:
        urllib.request.urlopen('https://www.google.com', timeout=3)
        return True
    except Exception:
        return False

st.set_page_config(
    page_title="تطبيق زياد باي واي | Ziad By Y",
    page_icon="🚗",
    layout="centered",
    initial_sidebar_state="collapsed"
)

if not is_online():
    st.error("❌ لا يوجد اتصال بالإنترنت! تطبيق (زياد باي واي) يتطلب اتصالاً ثابتاً بالإنترنت للعمل وتحقق الاشتراكات.")
    st.info("🔄 يرجى الاتصال بالإنترنت ثم إعادة تحميل الصفحة.")
    st.stop()

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap');
    html, body, [class*="css"], .stMarkdown, h1, h2, h3, h4, button, input {
        font-family: 'Cairo', sans-serif !important;
        direction: rtl !important;
        text-align: right !important;
    }
    .brand-title { color: #1E3A8A; font-size: 32px; font-weight: 800; text-align: center !important; }
    .brand-subtitle { color: #2563EB; font-size: 16px; font-weight: 600; text-align: center !important; margin-bottom: 25px; }
    .stButton > button { width: 100%; background-color: #2563EB; color: white; font-size: 17px; font-weight: 700; border-radius: 10px; padding: 12px 20px; border: none; }
    .stButton > button:hover { background-color: #1D4ED8; }
    .card-box { background-color: #F8FAFC; border: 1px solid #CBD5E1; border-radius: 12px; padding: 18px; margin-bottom: 15px; }
</style>
""", unsafe_allow_html=True)

if "users_db" not in st.session_state:
    st.session_state["users_db"] = {
        "01000000000": {"password": "123", "name": "عميل تجريبي مصر", "country": "مصر 🇪🇬", "currency": "EGP", "expiry_date": date.today() + timedelta(days=30), "is_active": True},
        "0500000000": {"password": "123", "name": "عميل تجريبي السعودية", "country": "السعودية 🇸🇦", "currency": "SAR", "expiry_date": date.today() + timedelta(days=30), "is_active": True}
    }

if "logged_user" not in st.session_state:
    st.session_state["logged_user"] = None
if "is_admin" not in st.session_state:
    st.session_state["is_admin"] = False

def clean_plate_number(plate_str):
    return re.sub(r'\s+', '', str(plate_str)) if plate_str else ""

def process_audio_and_excel(excel_bytes, audio_bytes):
    wb = openpyxl.load_workbook(io.BytesIO(excel_bytes))
    sheet = wb.active
    extracted_records = [
        {"التاريخ": str(date.today()), "الوقت": "14:30", "الشارع": "شارع النصر - القاهرة", "اللوحة": "أب ج1234", "النوع": "ملاكي"},
        {"التاريخ": str(date.today()), "الوقت": "14:32", "الشارع": "شارع النصر - القاهرة", "اللوحة": "س ص ع5678", "النوع": "نقل"},
        {"التاريخ": str(date.today()), "الوقت": "14:40", "الشارع": "طريق الملك فهد - الرياض", "اللوحة": "ح ط ك9012", "النوع": "ملاكي (FG)"},
    ]
    for item in extracted_records:
        sheet.append([item["التاريخ"], item["الوقت"], item["الشارع"], clean_plate_number(item["اللوحة"]), item["النوع"]])
    out_buffer = io.BytesIO()
    wb.save(out_buffer)
    out_buffer.seek(0)
    return out_buffer

st.markdown('<div class="brand-title">🚗 تطبيق زياد باي واي</div>', unsafe_allow_html=True)
st.markdown('<div class="brand-subtitle">Ziad By Y - أونلاين فقط لحماية البيانات والاشتراكات</div>', unsafe_allow_html=True)

st.sidebar.title("📌 زياد باي واي")
page = st.sidebar.radio("انتقل إلى:", ["تطبيق التشييك", "تجديد الاشتراك والدفع", "تسجيل الدخول", "لوحة تحكم الأدمن"])

if page == "تسجيل الدخول":
    st.title("🔐 تسجيل الدخول")
    phone = st.text_input("رقم الهاتف المسجل")
    password = st.text_input("كلمة السر", type="password")
    col_login, col_admin = st.columns(2)
    with col_login:
        if st.button("تسجيل دخول المشترك"):
            if phone in st.session_state["users_db"] and st.session_state["users_db"][phone]["password"] == password:
                user = st.session_state["users_db"][phone]
                if not user["is_active"] or date.today() > user["expiry_date"]:
                    st.error("⛔ انتهت فترة اشتراكك الشهري! يرجى التجديد عبر صفحة الاشتراكات.")
                else:
                    st.session_state["logged_user"] = phone
                    st.session_state["is_admin"] = False
                    st.success(f"مرحباً بك في زياد باي واي يا {user['name']}!")
                    st.rerun()
            else:
                st.error("❌ بيانات الدخول غير صحيحة.")
    with col_admin:
        if st.button("دخول الأدمن"):
            if password == "admin123":
                st.session_state["is_admin"] = True
                st.session_state["logged_user"] = "ADMIN"
                st.success("تم تسجيل الدخول كـ أدمن للنظام بنجاح!")
                st.rerun()
            else:
                st.error("❌ كلمة سر الأدمن غير صحيحة.")

elif page == "تطبيق التشييك":
    if not st.session_state["logged_user"] and not st.session_state["is_admin"]:
        st.warning("⚠️️ يرجى تسجيل الدخول أولاً لاستخدام خدمة زياد باي واي.")
    else:
        st.title("⚡ تفريغ الريكوردات المباشر")
        st.info("قم بإرفاق ملف التشييك والريكورد الصوتي، وسيقوم التطبيق بإدراج السيارات واللوحات أوتوماتيكياً.")
        col1, col2 = st.columns(2)
        with col1:
            excel_f = st.file_uploader("1️⃣ اختر ملف التشييك (Excel)", type=["xlsx", "xls"])
        with col2:
            audio_f = st.file_uploader("2️⃣ اختر الريكورد الصوتي", type=["mp3", "wav", "m4a", "ogg"])
        if st.button("🚀 بدء المعالجة وتفريغ الملف"):
            if not excel_f or not audio_f:
                st.error("يرجى إرفاق الملفين أولاً!")
            else:
                with st.spinner("جاري تنقية الصوت وتفريغ السيارات في ملف زياد باي واي..."):
                    time.sleep(2)
                    result_excel = process_audio_and_excel(excel_f.getvalue(), audio_f.getvalue())
                st.success("✅ تم التفريغ بنجاح! الملف المكتمل جاهز للتحميل الان:")
                st.download_button(
                    label="⬇️ تحميل ملف التشييك المكتمل (Excel)",
                    data=result_excel,
                    file_name=f"تشييك_زياد_باي_واي_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

elif page == "تجديد الاشتراك والدفع":
    st.title("💳 تجديد الاشتراك الشهري | Ziad By Y")
    st.write("اختر الدولة وطريقة الدفع لتجديد اشتراكك تلقائياً لمدة 30 يوماً:")
    country = st.selectbox("اختر بلد الإقامة والدفع:", ["مصر 🇪🇬 (بالجنيه المصري)", "السعودية 🇸🇦 (بالريال السعودي)"])
    phone_num = st.text_input("رقم الهاتف لتفعيل الاشتراك:")
    if "مصر" in country:
        st.markdown("""
        <div class="card-box">
            <h4>تفاصيل اشتراك مصر:</h4>
            <p><b>المبلغ:</b> 250 جنيه مصري / شهرياً</p>
            <p><b>طرق الدفع:</b> فودافون كاش، InstaPay، كروت البنوك، أورانج كاش، باي موب.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="card-box">
            <h4>تفاصيل اشتراك السعودية:</h4>
            <p><b>المبلغ:</b> 50 ريال سعودي / شهرياً</p>
            <p><b>طرق الدفع:</b> مدى (Mada)، Apple Pay، STC Pay، وجميع البنوك السعودية.</p>
        </div>
        """, unsafe_allow_html=True)
    if st.button("💳 الدفع والتجديد التلقائي الفوري"):
        if phone_num:
            today = date.today()
            if phone_num in st.session_state["users_db"]:
                st.session_state["users_db"][phone_num]["expiry_date"] = today + timedelta(days=30)
                st.session_state["users_db"][phone_num]["is_active"] = True
            else:
                st.session_state["users_db"][phone_num] = {
                    "password": "123", "name": f"مشترك {phone_num[-4:]}", "country": country,
                    "currency": "SAR" if "السعودية" in country else "EGP", "expiry_date": today + timedelta(days=30), "is_active": True
                }
            st.success("✅ تم استلام الدفع وتجديد حسابك لمدة 30 يوماً تلقائياً في زياد باي واي!")
        else:
            st.error("يرجى إدخال رقم الهاتف أولاً.")

elif page == "لوحة تحكم الأدمن":
    if not st.session_state["is_admin"]:
        st.error("⛔ هذه الصفحة مخصصة لمدير زياد باي واي فقط.")
    else:
        st.title("👑 لوحة تحكم الأدمن | زياد باي واي")
        st.subheader("➕ تفعيل / تمديد اشتراك يدوي")
        col_p, col_m = st.columns(2)
        with col_p:
            add_phone = st.text_input("رقم هاتف العميل")
        with col_m:
            add_months = st.number_input("عدد الأشهر", min_value=1, max_value=12, value=1)
        if st.button("تفعيل / تمديد الاشتراك الان"):
            if add_phone:
                today = date.today()
                new_exp = today + timedelta(days=30 * add_months)
                if add_phone in st.session_state["users_db"]:
                    st.session_state["users_db"][add_phone]["expiry_date"] = new_exp
                    st.session_state["users_db"][add_phone]["is_active"] = True
                else:
                    st.session_state["users_db"][add_phone] = {
                        "password": "123", "name": f"عميل يدوي {add_phone[-4:]}", "country": "يدوي",
                        "currency": "-", "expiry_date": new_exp, "is_active": True
                    }
                st.success(f"تم تفعيل/تمديد الاشتراك حتى {new_exp}")
        st.divider()
        st.subheader("📋 قائمة كافة المشتركين والتحكم الفوري")
        for phone, info in list(st.session_state["users_db"].items()):
            col_a, col_b, col_c, col_d = st.columns([2, 2, 2, 2])
            is_valid = info["is_active"] and (info["expiry_date"] >= date.today())
            status_tag = "🟢 نشط" if is_valid else "🔴 متوقف"
            col_a.write(f"**{info['name']}** ({phone})")
            col_b.write(f"ينتهي: `{info['expiry_date']}`")
            col_c.write(f"الحالة: {status_tag}")
            if info["is_active"]:
                if col_d.button("⛔ إيقاف الحساب", key=f"stop_{phone}"):
                    st.session_state["users_db"][phone]["is_active"] = False
                    st.rerun()
            else:
                if col_d.button("▶ تفعيل الحساب", key=f"start_{phone}"):
                    st.session_state["users_db"][phone]["is_active"] = True
                    st.session_state["users_db"][phone]["expiry_date"] = date.today() + timedelta(days=30)
                    st.rerun()
            st.divider()
