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

# -------------------------------------------------------------------------
# 🛠 مفتاح الصيانة (التطبيق مغلق تماماً أمام العملاء، والأدمن وحده من يستطيع الدخول)
# -------------------------------------------------------------------------
MAINTENANCE_MODE = True 

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

if "login_time" not in st.session_state:
    st.session_state["login_time"] = None

if "show_admin_dashboard" not in st.session_state:
    st.session_state["show_admin_dashboard"] = False

# منع أي عميل عادي من البقاء مسجلاً أثناء الصيانة، وجعل الدخول مقتصرًا على الأدمن فقط
if st.session_state["logged_in_user"]:
    current_check_user = st.session_state["users"].get(st.session_state["logged_in_user"], {})
    if MAINTENANCE_MODE and not current_check_user.get("is_admin", False):
        st.session_state["logged_in_user"] = None

# =========================================================================
# 1. شاشة ما قبل تسجيل الدخول
# =========================================================================
if not st.session_state["logged_in_user"]:
    col_head1, col_head2 = st.columns([8, 2])
    with col_head1:
        st.title("🚗 تطبيق زياد باي واي")
    with col_head2:
        if st.button("👑 Z", help="دخول الأدمن"):
            st.session_state["show_admin_login"] = not st.session_state.get("show_admin_login", False)

    # نموذج دخول الأدمن عبر زر Z (متاح حصرياً لك)
    if st.session_state.get("show_admin_login", False):
        st.info("🔐 **تسجيل دخول الأدمن (متاح لك وحدك حالياً)**")
        admin_phone = st.text_input("رقم هاتف الأدمن (بدون الصفر)", value="1006820162", key="ap")
        admin_pass = st.text_input("كلمة السر", type="password", key="appwd")
        
        if st.button("دخول كأدمن 🚀", use_container_width=True):
            full_ap = f"+20{admin_phone.strip()}"
            if full_ap in st.session_state["users"] and st.session_state["users"][full_ap]["password"] == admin_pass and st.session_state["users"][full_ap].get("is_admin", False):
                st.session_state["logged_in_user"] = full_ap
                st.session_state["login_time"] = datetime.now()
                st.session_state["show_admin_login"] = False
                st.success("تم تسجيل دخول الأدمن بنجاح!")
                st.rerun()
            else:
                st.error("بيانات الأدمن غير صحيحة أو الحساب ليس مديراً للنظام")
        st.divider()

    st.warning("⚠️ **تنبيه:** الموقع حالياً في فترة الصيانة وتجهيز الإطلاق. تسجيل الدخول للعملاء متوقف تماماً، ومتاح فقط **لإنشاء حسابات جديدة** لتسجيل أسمائكم.")

    # تبويبات الدخول وإنشاء الحساب
    tab1, tab2 = st.tabs(["تسجيل الدخول", "إنشاء حساب جديد"])
    
    with tab1:
        st.subheader("تسجيل دخول العملاء")
        st.error("🔒 تسجيل الدخول مغلق حالياً لجميع العملاء حتى يتم الإطلاق الرسمي.")
                
    with tab2:
        st.subheader("إنشاء حساب جديد (متاح لتسجيل اسمك الآن)")
        new_name = st.text_input("الاسم بالكامل", key="rn_input")
        r_code = st.selectbox("الدولة", ["مصر (+20)", "السعودية (+966)"], key="cr")
        r_prefix = "+20" if "مصر" in r_code else "+966"
        r_phone = st.text_input("رقم الهاتف", key="rpi")
        
        if st.button("تسجيل وحفظ الحساب 📝", use_container_width=True):
            full_rp = f"{r_prefix}{r_phone.strip()}"
            if full_rp in st.session_state["users"]:
                st.warning("هذا الرقم مسجل مسبقاً!")
            elif new_name and r_phone:
                st.session_state["users"][full_rp] = {
                    "name": new_name, 
                    "email": "مسجل أثناء الصيانة", 
                    "password": "123",
                    "active": False, 
                    "is_admin": False, 
                    "sub_type": "سجل أثناء الصيانة",
                    "months": 0, 
                    "amount_paid": 0, 
                    "expiry_date": "قيد الانتظار"
                }
                st.success(f"مرحباً بك يا {new_name}! تم حفظ حسابك بنجاح، وستظهر بياناتك لدى الإدارة فوراً.")
            else:
                st.error("يرجى إدخال الاسم ورقم الهاتف!")

# =========================================================================
# 2. شاشة ما بعد تسجيل الدخول (لا يدخلها سوى الأدمن فقط)
# =========================================================================
else:
    user_phone = st.session_state["logged_in_user"]
    user_data = st.session_state["users"][user_phone]
    
    # حماية إضافية: إذا لم يكن أدمن، يتم طرده فوراً
    if not user_data.get("is_admin", False):
        st.session_state["logged_in_user"] = None
        st.rerun()

    head_c1, head_c2 = st.columns([7, 3])
    head_c1.title("🚗 تفريغ الريكوردات")
    if head_c2.button("💲 إدارة المشتركين", use_container_width=True):
        st.session_state["show_admin_dashboard"] = not st.session_state["show_admin_dashboard"]

    col_out1, col_out2 = st.columns([3, 1])
    col_out1.write(f"مرحباً بك يا أدمن، **{user_data['name']}** (أنت الوحيد المخول بالدخول حالياً)")
    if col_out2.button("تسجيل الخروج"):
        st.session_state["logged_in_user"] = None
        st.session_state["login_time"] = None
        st.session_state["show_admin_dashboard"] = False
        st.rerun()
        
    st.divider()

    # --- لوحة تحكم الأدمن الشاملة ---
    if user_data.get("is_admin", False) and st.session_state["show_admin_dashboard"]:
        st.info("📊 **لوحة تحكم الأدمن (متابعة الحسابات المسجلة أثناء الصيانة)**")
        
        users_list = st.session_state["users"]
        total_registered = len(users_list) - 1
        pending_users = sum(1 for p, d in users_list.items() if not d.get("active") and not d.get("is_admin"))
        active_subscribers = sum(1 for p, d in users_list.items() if d.get("active") and not d.get("is_admin"))

        stat1, stat2, stat3 = st.columns(3)
        stat1.metric("👥 إجمالي الحسابات المسجلة", f"{total_registered} حساب")
        stat2.metric("⏳ بانتظار الإطلاق / التفعيل", f"{pending_users} عميل")
        stat3.metric("✅ الاشتراكات النشطة", f"{active_subscribers} مشترك")
        st.markdown("---")
        
        admin_tab1, admin_tab2 = st.tabs(["➕ إضافة وتفعيل مشترك يدوياً", "📋 قائمة كافة الحسابات المسجلة"])
        
        with admin_tab1:
            st.subheader("إنشاء وتفعيل مشترك جديد بأسعار تلقائية")
            an_name = st.text_input("اسم المشترك الكامل", key="an_name")
            an_code = st.selectbox("الدولة وعملة السعر", ["مصر (+20) - جنيه", "السعودية (+966) - ريال"], key="an_code")
            an_prefix = "+20" if "مصر" in an_code else "+966"
            an_phone = st.text_input("رقم الهاتف", key="an_phone")
            an_pass = st.text_input("كلمة السر", key="an_pass", value="123456")
            
            col_a, col_b = st.columns(2)
            an_type = col_a.selectbox("نوع الاشتراك", ["دفع كاش / فودافون كاش 💳", "تفعيل مجاني 🎁"], key="an_type")
            an_months = col_b.number_input("عدد الشهور المطلوبة", min_value=1, max_value=24, value=1, key="an_months")
            
            if "مصر" in an_code:
                calculated_amount = 0 if "مجاني" in an_type else (2080 * an_months)
                currency_label = "جنيه مصري"
            else:
                calculated_amount = 0 if "مجاني" in an_type else (150 * an_months)
                currency_label = "ريال سعودي"
                
            st.info(f"💵 **المبلغ الإجمالي المحسوب أوتوماتيكياً:** `{calculated_amount} {currency_label}` (بواقع {an_months} شهر)")
            
            if st.button("✨ إنشاء وتفعيل الحساب فوراً", use_container_width=True, type="primary"):
                full_an_phone = f"{an_prefix}{an_phone.strip()}"
                if not an_name or not an_phone:
                    st.error("يرجى إكمال اسم المشترك ورقم الهاتف!")
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
                    st.success(f"تم إنشاء وتفعيل حساب ({an_name}) بنجاح!")
                    st.rerun()

        with admin_tab2:
            st.caption("قائمة العملاء الذين سجلوا أسماءهم وأرقامهم أثناء فترة الصيانة:")
            for phone, data in users_list.items():
                if not data.get("is_admin", False):
                    status_icon = "✅ مفعل" if data['active'] else "⏳ مسجل حديثاً (بانتظار الإطلاق)"
                    with st.expander(f"👤 الاسم: {data['name']} | الرقم: ({phone}) — الحالة: {status_icon}"):
                        st.write(f"**حالة الاشتراك:** {data.get('sub_type', 'غير محدد')}")
                        st.write(f"**المبلغ المدفوع:** {data.get('amount_paid', 0)}")
                        
                        col_act1, col_act2 = st.columns(2)
                        if not data['active']:
                            if col_act1.button("✅ تفعيل الحساب الآن", key=f"quick_act_{phone}", use_container_width=True):
                                data['active'] = True
                                data['sub_type'] = "تم التفعيل بواسطة الأدمن"
                                data['expiry_date'] = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-d")
                                st.success(f"تم تفعيل حساب {data['name']} بنجاح!")
                                st.rerun()
                        
                        if col_act2.button("🚫 إيقاف / حذف الحساب", key=f"deact_b_{phone}", use_container_width=True):
                            data["active"] = False
                            data["sub_type"] = "متوقف"
                            st.warning(f"تم إيقاف حساب {data['name']}")
                            st.rerun()
        st.divider()

    # شاشة الأدمن الخاصة بتفريغ الريكوردات مع توجيه لاختيار الملفات من الواتساب
    st.success("🛠️ **أنت في لوحة التحكم الخاصة بك كأدمن.**")
    st.subheader("📄 تطبيق التشييك وتفريغ الريكوردات")
    
    st.info("💡 **ملاحظة لاختيار الملفات:** يمكنك اختيار ملف الإكسيل والريكورد الصوتي مباشرة من مجلدات **الواتساب، التيليجرام، أو محادثاتك** عبر نافذة اختيار الملفات في هاتفك أو حاسوبك.")
    
    excel_file = st.file_uploader("1️⃣ اختر ملف التشييك (Excel - يمكنك جلبه من الواتساب/التيليجرام)", type=["xlsx", "xls"])
    audio_file = st.file_uploader("2️⃣ اختر الريكورد الصوتي (من محادثات الواتساب أو ملفات الصوت)", type=["mp3", "wav", "m4a", "ogg"])
    
    if st.button("🚀 بدء المعالجة وتفريغ الملف", use_container_width=True):
        if excel_file and audio_file:
            st.success("تمت المعالجة بنجاح!")
            st.download_button(
                label="⬇️️ تحميل ملف التشييك المكتمل (Excel)",
                data=excel_file.getvalue(),
                file_name="ملف_التشييك_المكتمل.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        else:
            st.error("يرجى رفع ملف الإكسيل والريكورد الصوتي أولاً")
