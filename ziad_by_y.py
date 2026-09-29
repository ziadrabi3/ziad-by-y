import streamlit as st

# إعدادات الصفحة
st.set_page_config(
    page_title="Ziad By Y | الأدمن والتطبيق", 
    page_icon="🚗", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- إخفاء أي عناصر خارجية لإبقاء الواجهة نظيفة تماماً ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            [data-testid="stSidebar"] {display: none;}
            [data-testid="collapsedControl"] {display: none;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# تهيئة قاعدة البيانات المؤقتة في الجلسة (Session State)
if "users" not in st.session_state:
    st.session_state["users"] = {
        "+201006820162": {
            "name": "الأدمن زياد",
            "email": "admin@ziad.com",
            "password": "ziad492008",
            "active": True,
            "is_admin": True
        }
    }

if "logged_in_user" not in st.session_state:
    st.session_state["logged_in_user"] = None

# --- زر اختصار المخفي في الأعلى بالرمز Z للأدمن ---
col_head1, col_head2 = st.columns([8, 2])
with col_head1:
    st.title("🚗 تطبيق زياد باي واي")
with col_head2:
    if st.button("👑 Z", help="لوحة تسجيل دخول الأدمن"):
        st.session_state["show_admin_login"] = not st.session_state.get("show_admin_login", False)

# --- شاشة دخول الأدمن المخفية المخصصة برقمك ورامزك ---
if st.session_state.get("show_admin_login", False):
    st.info("🔐 **منطقة تسجيل دخول الأدمن الخاصة**")
    admin_phone = st.text_input("رقم هاتف الأدمن (بدون الصفر الأول)", value="1006820162", key="admin_p")
    admin_pass = st.text_input("رمز مرور الأدمن الخاص", type="password", key="admin_pwd")
    
    if st.button("دخول الأدمن 🚀", use_container_width=True):
        full_admin_phone = f"+20{admin_phone.strip()}"
        if full_admin_phone in st.session_state["users"] and st.session_state["users"][full_admin_phone]["password"] == admin_pass:
            st.session_state["logged_in_user"] = full_admin_phone
            st.session_state["show_admin_login"] = False
            st.success("تم تسجيل دخول الأدمن بنجاح!")
            st.rerun()
        else:
            st.error("رقم الأدمن أو رمز المرور غير صحيح")
    st.divider()

# --- الشاشة الرئيسية: تسجيل الدخول / إنشاء حساب للمستخدمين العاديين ---
if not st.session_state["logged_in_user"]:
    tab1, tab2 = st.tabs(["تسجيل الدخول", "إنشاء حساب جديد"])
    
    with tab1:
        st.subheader("تسجيل دخول العملاء")
        country_code_login = st.selectbox("الدولة", ["مصر (+20)", "السعودية (+966)"], key="c_login")
        code_prefix_login = "+20" if "مصر" in country_code_login else "+966"
        
        phone_input = st.text_input("رقم الهاتف (بدون الصفر الأول)", key="login_phone")
        full_phone_login = f"{code_prefix_login}{phone_input.strip()}"
        
        login_pass = st.text_input("كلمة السر", type="password", key="login_pass")
        
        if st.button("دخول", use_container_width=True):
            users = st.session_state["users"]
            if full_phone_login in users and users[full_phone_login]["password"] == login_pass:
                st.session_state["logged_in_user"] = full_phone_login
                st.rerun()
            else:
                st.error("رقم الهاتف أو كلمة السر غير صحيحة")
                
    with tab2:
        st.subheader("إنشاء حساب جديد")
        new_name = st.text_input("الاسم بالكامل")
        
        country_code_reg = st.selectbox("الدولة", ["مصر (+20)", "السعودية (+966)"], key="c_reg")
        code_prefix_reg = "+20" if "مصر" in country_code_reg else "+966"
        
        reg_phone_input = st.text_input("رقم الهاتف (مثال: 1xxxxxxx لمصر أو 5xxxxxxx للسعودية)")
        full_phone_reg = f"{code_prefix_reg}{reg_phone_input.strip()}"
        
        new_email = st.text_input("البريد الإلكتروني")
        new_pass = st.text_input("كلمة السر الخاصة بك", type="password")
        
        if st.button("إنشاء الحساب", use_container_width=True):
            if not reg_phone_input:
                st.error("يرجى إدخال رقم الهاتف")
            elif full_phone_reg in st.session_state["users"]:
                st.warning("هذا الرقم مسجل بالفعل!")
            elif new_name and new_email and new_pass:
                st.session_state["users"][full_phone_reg] = {
                    "name": new_name,
                    "email": new_email,
                    "password": new_pass,
                    "active": False, # الحساب ينشأ غير مفعل للعميل
                    "is_admin": False
                }
                st.success("تم إنشاء الحساب بنجاح! يمكنك الآن تسجيل الدخول لتفعيل الاشتراك.")
            else:
                st.error("يرجى ملء جميع البيانات المطلوبة")

# --- شاشة ما بعد تسجيل الدخول (للأدمن أو للعميل) ---
else:
    user_phone = st.session_state["logged_in_user"]
    user_data = st.session_state["users"][user_phone]
    
    col_out1, col_out2 = st.columns([3, 1])
    col_out1.write(f"مرحباً بك، **{user_data['name']}** (`{user_phone}`)")
    if col_out2.button("تسجيل الخروج"):
        st.session_state["logged_in_user"] = None
        st.rerun()
        
    st.divider()

    # لوحة تحكم الأدمن (تظهر فقط لو سجلت بحساب الأدمن)
    if user_data.get("is_admin", False):
        st.subheader("👑 لوحة إدارة المشتركين وتفعيل الحسابات (خاصة بزياد)")
        
        users_list = st.session_state["users"]
        for phone, data in users_list.items():
            if phone != user_phone: # عدم تعديل حساب الأدمن الرئيسي
                c1, c2, c3 = st.columns([2, 2, 1])
                c1.write(f"**الاسم:** {data['name']}\n\n**الرقم:** `{phone}`")
                c2.write(f"**الإيميل:** {data['email']}")
                
                if data["active"]:
                    if c3.button("إيقاف الحساب", key=f"deact_{phone}"):
                        data["active"] = False
                        st.success(f"تم إيقاف حساب {data['name']}")
                        st.rerun()
                else:
                    if c3.button("تفعيل الاشتراك 🚀", key=f"act_{phone}"):
                        data["active"] = True
                        st.success(f"تم تفعيل حساب {data['name']}")
                        st.rerun()
        st.divider()

    # التحقق من حالة الاشتراك للعميل العادي
    if not user_data["active"]:
        st.warning("⚠️ اشتراكك غير مفعل حالياً!")
        st.info("""
        ### 💰 قيمة الاشتراك:
        * **150 ريال سعودي** (أو **2,080 جنيه مصري** للتحويل من داخل مصر).
        
        ---
        ### 💳 طرق الدفع والتحويل:
        * **داخل مصر (فودافون كاش):**
          * رقم التحويل: `01006820162`
        * **داخل السعودية (حساب بنكي / STC Pay):**
          * يرجى التواصل معنا للحصول على بيانات الحساب البنكي المباشر.
        
        ---
        ### 📲 خطوات التفعيل:
        1. قم بتمويل الاشتراك عبر فودافون كاش أو الحساب البنكي.
        2. اضغط على الزر بالأسفل لإرسال صورة التحويل ورقم حسابك لتفعيل الخدمة فوراً:
        """)
        
        wa_url = f"https://wa.me/201006820162?text=مرحباً،%20قمت%20بتحويل%20رسوم%20الاشتراك%20لتطبيق%20زياد%20باي%20واي.%20رقمي%20المسجل:%20{user_phone}"
        st.link_button("📲 التواصل عبر واتساب لتأكيد التحويل والتفعيل", wa_url, use_container_width=True)
        
    else:
        st.success("✅ الخدمة متاحة ومفعلة!")
        
        # --- واجهة التطبيق الرئيسية (تفريغ الملفات والريكورد) ---
        st.subheader("📄 تطبيق التشييك وتفريغ الريكوردات")
        excel_file = st.file_uploader("1️⃣ اختر ملف التشييك (Excel)", type=["xlsx", "xls"])
        audio_file = st.file_uploader("2️⃣ اختر الريكورد الصوتي", type=["mp3", "wav", "m4a", "ogg"])
        
        if st.button("🚀 بدء المعالجة وتفريغ الملف", use_container_width=True):
            if excel_file and audio_file:
                st.success("تمت المعالجة بنجاح!")
                st.download_button(
                    label="⬇️ تحميل ملف التشييك المكتمل (Excel)",
                    data=excel_file.getvalue(),
                    file_name="ملف_التشييك_المكتمل.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            else:
                st.error("يرجى رفع ملف الإكسيل والريكورد الصوتي أولاً")
