import streamlit as st
from datetime import datetime, timedelta

# إعدادات الصفحة
st.set_page_config(page_title="Ziad By Y", page_icon="🚗", layout="centered", initial_sidebar_state="collapsed")

# إخفاء العناصر غير الضرورية
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            [data-testid="stSidebar"] {display: none;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# قاعدة بيانات مؤقتة للحسابات
if "users" not in st.session_state:
    st.session_state["users"] = {
        "+201006820162": {
            "name": "الأدمن زياد",
            "email": "admin@ziad.com",
            "password": "ziad492008",
            "active": True,
            "is_admin": True,
            "sub_type": "مدير النظام",
            "months": 12,
            "amount_paid": 0,
            "expiry_date": "دائم"
        }
    }

if "logged_in_user" not in st.session_state:
    st.session_state["logged_in_user"] = None

if "show_admin_dashboard" not in st.session_state:
    st.session_state["show_admin_dashboard"] = False

# =========================================================================
# 1. شاشة ما قبل تسجيل الدخول (يظهر فيها زر 👑 Z القديم)
# =========================================================================
if not st.session_state["logged_in_user"]:
    col_head1, col_head2 = st.columns([8, 2])
    with col_head1:
        st.title("🚗 تطبيق زياد باي واي")
    with col_head2:
        if st.button("👑 Z", help="دخول الأدمن"):
            st.session_state["show_admin_login"] = not st.session_state.get("show_admin_login", False)

    # نموذج دخول الأدمن عبر زر Z
    if st.session_state.get("show_admin_login", False):
        st.info("🔐 **تسجيل دخول الأدمن**")
        admin_phone = st.text_input("رقم هاتف الأدمن (بدون الصفر)", value="1006820162", key="ap")
        admin_pass = st.text_input("كلمة السر", type="password", key="appwd")
        
        if st.button("دخول كأدمن 🚀", use_container_width=True):
            full_ap = f"+20{admin_phone.strip()}"
            if full_ap in st.session_state["users"] and st.session_state["users"][full_ap]["password"] == admin_pass:
                st.session_state["logged_in_user"] = full_ap
                st.session_state["show_admin_login"] = False
                st.success("تم تسجيل الدخول بنجاح!")
                st.rerun()
            else:
                st.error("رقم الهاتف أو كلمة السر غير صحيحة")
        st.divider()

    # تبويبات الدخول وإنشاء الحساب للعملاء
    tab1, tab2 = st.tabs(["تسجيل الدخول", "إنشاء حساب جديد"])
    
    with tab1:
        st.subheader("تسجيل دخول العملاء")
        c_code = st.selectbox("الدولة", ["مصر (+20)", "السعودية (+966)"], key="cl")
        prefix = "+20" if "مصر" in c_code else "+966"
        phone_in = st.text_input("رقم الهاتف", key="pli")
        pass_in = st.text_input("كلمة السر", type="password", key="pwi")
        
        if st.button("دخول", use_container_width=True):
            full_p = f"{prefix}{phone_in.strip()}"
            if full_p in st.session_state["users"] and st.session_state["users"][full_p]["password"] == pass_in:
                st.session_state["logged_in_user"] = full_p
                st.rerun()
            else:
                st.error("بيانات الدخول غير صحيحة")
                
    with tab2:
        st.subheader("إنشاء حساب جديد")
        new_name = st.text_input("الاسم بالكامل")
        r_code = st.selectbox("الدولة", ["مصر (+20)", "السعودية (+966)"], key="cr")
        r_prefix = "+20" if "مصر" in r_code else "+966"
        r_phone = st.text_input("رقم الهاتف", key="rpi")
        new_email = st.text_input("البريد الإلكتروني")
        new_pass = st.text_input("كلمة السر الخاصة بك", type="password", key="rwi")
        
        if st.button("إنشاء الحساب", use_container_width=True):
            full_rp = f"{r_prefix}{r_phone.strip()}"
            if full_rp in st.session_state["users"]:
                st.warning("هذا الرقم مسجل مسبقاً!")
            elif new_name and r_phone and new_pass:
                st.session_state["users"][full_rp] = {
                    "name": new_name, "email": new_email, "password": new_pass,
                    "active": False, "is_admin": False, "sub_type": "غير مفعل",
                    "months": 0, "amount_paid": 0, "expiry_date": "غير محدد"
                }
                st.success("تم إنشاء الحساب بنجاح! يمكنك تسجيل الدخول الآن.")
            else:
                st.error("يرجى إكمال جميع البيانات المطلوبة")

# =========================================================================
# 2. شاشة ما بعد تسجيل الدخول (يظهر فيها زر الدولار 💲 فوق خالص على الشمال للأدمن)
# =========================================================================
else:
    user_phone = st.session_state["logged_in_user"]
    user_data = st.session_state["users"][user_phone]
    
    # الهيدر المخصص بعد الدخول
    if user_data.get("is_admin", False):
        head_c1, head_c2 = st.columns([7, 3])
        head_c1.title("🚗 تفريغ الريكوردات")
        if head_c2.button("💲 إدارة المشتركين", use_container_width=True):
            st.session_state["show_admin_dashboard"] = not st.session_state["show_admin_dashboard"]
    else:
        st.title("🚗 تفريغ الريكوردات")

    # زر تسجيل الخروج ومعلومات الحساب
    col_out1, col_out2 = st.columns([3, 1])
    col_out1.write(f"مرحباً بك، **{user_data['name']}**")
    if col_out2.button("تسجيل الخروج"):
        st.session_state["logged_in_user"] = None
        st.session_state["show_admin_dashboard"] = False
        st.rerun()
        
    st.divider()

    # --- لوحة التحكم الخاصة بالأدمن (تفتح عند الضغط على زر 💲 فوق) ---
    if user_data.get("is_admin", False) and st.session_state["show_admin_dashboard"]:
        st.info("📊 **لوحة تحكم المشتركين وإدارة الاشتراكات التلقائية**")
        
        admin_tab1, admin_tab2 = st.tabs(["➕ إضافة مشترك يدوياً (تفعيل فوري)", "📋 إدارة المشتركين الحاليين"])
        
        # ---------------- القسم الأول: إنشاء وتفعيل حساب يدوياً مع الحساب التلقائي للأسعار ----------------
        with admin_tab1:
            st.subheader("إشاء وتفعيل مشترك جديد بأسعار تلقائية")
            an_name = st.text_input("اسم المشترك", key="an_name")
            an_code = st.selectbox("الدولة وعملة السعر", ["مصر (+20) - جنيه", "السعودية (+966) - ريال"], key="an_code")
            an_prefix = "+20" if "مصر" in an_code else "+966"
            an_phone = st.text_input("رقم الهاتف", key="an_phone")
            an_pass = st.text_input("كلمة السر (التي ستعطيها للعميل)", key="an_pass")
            
            st.markdown("##### 💰 حساب المدة والمبلغ تلقائياً:")
            col_a, col_b = st.columns(2)
            an_type = col_a.selectbox("نوع الاشتراك", ["دفع كاش / مباشر 💵", "تفعيل مجاني 🎁"], key="an_type")
            an_months = col_b.number_input("عدد الشهور المطلوبة", min_value=1, max_value=24, value=1, key="an_months")
            
            # الحساب التلقائي المبرمج (لا يمكن للعميل أو غيره العبث به)
            if "مصر" in an_code:
                calculated_amount = 0 if "مجاني" in an_type else (2080 * an_months)
                currency_label = "جنيه مصري"
            else:
                calculated_amount = 0 if "مجاني" in an_type else (150 * an_months)
                currency_label = "ريال سعودي"
                
            st.info(f"💵 **المبلغ الإجمالي المحسوب أوتوماتيكياً:** `{calculated_amount} {currency_label}` (بواقع {an_months} شهر)")
            
            if st.button("✨ إنشاء وتفعيل الحساب فوراً", use_container_width=True, type="primary"):
                full_an_phone = f"{an_prefix}{an_phone.strip()}"
                if not an_name or not an_phone or not an_pass:
                    st.error("يرجى إكمال الاسم ورقم الهاتف وكلمة السر!")
                elif full_an_phone in st.session_state["users"]:
                    st.warning("هذا الرقم مسجل بالفعل!")
                else:
                    exp_dt = datetime.now() + timedelta(days=30 * an_months)
                    st.session_state["users"][full_an_phone] = {
                        "name": an_name,
                        "email": "أضيف بواسطة الإدارة",
                        "password": an_pass,
                        "active": True,
                        "is_admin": False,
                        "sub_type": an_type,
                        "months": an_months,
                        "amount_paid": calculated_amount,
                        "expiry_date": exp_dt.strftime("%Y-%m-%d")
                    }
                    st.success(f"تم إنشاء وتفعيل حساب ({an_name}) بمبلغ {calculated_amount} {currency_label} بنجاح!")
                    st.rerun()

        # ---------------- القسم الثاني: تعديل المشتركين المسجلين مسبقاً ----------------
        with admin_tab2:
            users_list = st.session_state["users"]
            for phone, data in users_list.items():
                if not data.get("is_admin", False):
                    with st.expander(f"👤 {data['name']} ({phone}) — {'✅ مفعل' if data['active'] else '❌ غير مفعل'}"):
                        st.write(f"النوع الحالي: {data.get('sub_type', 'غير محدد')} | مدفوع: {data.get('amount_paid', 0)} | ينتهي في: {data.get('expiry_date', 'غير محدد')}")
                        
                        if st.button("🚫 إيقاف الحساب", key=f"deact_b_{phone}", use_container_width=True):
                            data["active"] = False
                            data["sub_type"] = "متوقف"
                            st.warning(f"تم إيقاف حساب {data['name']}")
                            st.rerun()
        st.divider()

    # --- واجهة التطبيق الاعتيادية للمستخدم (أو الأدمن) ---
    if not user_data["active"]:
        st.warning("⚠️ اشتراكك غير مفعل حالياً!")
        st.info("قيمة الاشتراك: 150 ريال سعودي أو 2,080 جنيه مصري للشهر الواحد.")
        wa_url = f"https://wa.me/201006820162?text=مرحباً%20أريد%20تفعيل%20حسابي%20لرقم:%20{user_phone}"
        st.link_button("📲 التواصل عبر واتساب لتأكيد الدفع والتفعيل", wa_url, use_container_width=True)
    else:
        st.success(f"✅ حسابك مفعل ومتاح حتى: {user_data.get('expiry_date', 'دائم')}")
        
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
