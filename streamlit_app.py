#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
אפליקציית Streamlit לבדיקת מטלות אקסל
ניתן לפרסם ב-Streamlit Cloud
"""

import streamlit as st
import openpyxl
import pandas as pd
import json
from datetime import datetime
from pathlib import Path
import tempfile
import sys

# הוספת הנתיב לסוכן הבדיקה
sys.path.insert(0, str(Path(__file__).parent))
from excel_checker_advanced import AdvancedExcelChecker


# הגדרות עמוד
st.set_page_config(
    page_title="מערכת בדיקת מטלות אקסל",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# עיצוב CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        padding: 20px;
        background: linear-gradient(90deg, #e3f2fd 0%, #bbdefb 100%);
        border-radius: 10px;
        margin-bottom: 30px;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)


def main():
    """פונקציה ראשית"""
    
    # כותרת
    st.markdown('<div class="main-header"><h1>📊 מערכת בדיקת מטלות אקסל</h1><p>בדיקה אוטומטית של פונקציות ונוסחאות מול מחוון</p></div>', unsafe_allow_html=True)
    
    # סרגל צד - הגדרות
    with st.sidebar:
        st.header("⚙️ הגדרות")
        
        st.subheader("הגדרות בדיקה")
        partial_credit = st.checkbox("ציון חלקי", value=True, 
                                     help="אפשר ציון חלקי עבור בדיקות שעברו חלקית")
        
        similarity_threshold = st.slider(
            "רגישות התאמת שמות גליונות",
            min_value=0.3, max_value=1.0, value=0.6, step=0.1,
            help="רמת הדמיון הנדרשת בין שם הגליון במחוון לגליון בקובץ התלמיד"
        )
        
        strict_mode = st.checkbox("מצב קפדני", value=False,
                                 help="בדיקה קפדנית יותר - דורש התאמה מלאה")
        
        st.divider()
        st.subheader("📚 אודות")
        st.info("""
        **מערכת בדיקת מטלות אקסל**
        
        גרסה: 1.0
        
        המערכת בודקת:
        - קיום גליונות
        - שימוש בנוסחאות
        - שימוש בפונקציות ספציפיות
        - הפניות בין גליונות
        - תאי עזר
        
        פותח עבור בדיקת מטלות אקדמיות
        """)
    
    # טאבים ראשיים
    tab1, tab2, tab3 = st.tabs(["📤 העלאת קבצים", "📊 תוצאות", "📖 הנחיות"])
    
    with tab1:
        st.header("העלאת קבצים")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("1️⃣ העלה קובץ מחוון")
            rubric_file = st.file_uploader(
                "בחר קובץ אקסל של המחוון",
                type=['xlsx', 'xls'],
                key="rubric",
                help="קובץ המחוון מכיל את קריטריוני הבדיקה והניקוד"
            )
            
            if rubric_file:
                st.success(f"✅ נטען: {rubric_file.name}")
                
                # תצוגה מקדימה של המחוון
                with st.expander("👁️ תצוגה מקדימה של המחוון"):
                    try:
                        df = pd.read_excel(rubric_file, nrows=10)
                        st.dataframe(df, use_container_width=True)
                        rubric_file.seek(0)  # איפוס המצביע
                    except Exception as e:
                        st.error(f"שגיאה בטעינת תצוגה מקדימה: {e}")
        
        with col2:
            st.subheader("2️⃣ העלה קובץ תלמיד")
            student_file = st.file_uploader(
                "בחר קובץ אקסל של התלמיד",
                type=['xlsx', 'xls'],
                key="student",
                help="קובץ המטלה של התלמיד לבדיקה"
            )
            
            if student_file:
                st.success(f"✅ נטען: {student_file.name}")
                
                # תצוגה מקדימה של קובץ התלמיד
                with st.expander("👁️ תצוגה מקדימה של הקובץ"):
                    try:
                        # הצגת שמות הגליונות
                        temp_path = Path(tempfile.gettempdir()) / student_file.name
                        with open(temp_path, 'wb') as f:
                            f.write(student_file.getvalue())
                        
                        wb = openpyxl.load_workbook(temp_path, data_only=True)
                        st.write("**גליונות בקובץ:**", wb.sheetnames)
                        
                        # תצוגת נתונים מהגליון הראשון
                        student_file.seek(0)
                        df = pd.read_excel(student_file, nrows=10)
                        st.dataframe(df, use_container_width=True)
                        student_file.seek(0)
                    except Exception as e:
                        st.error(f"שגיאה בטעינת תצוגה מקדימה: {e}")
        
        st.divider()
        
        # כפתור בדיקה
        if rubric_file and student_file:
            col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
            with col_btn2:
                if st.button("🔍 בצע בדיקה", type="primary", use_container_width=True):
                    run_check(rubric_file, student_file, partial_credit, 
                            similarity_threshold, strict_mode)
        else:
            st.warning("⚠️ יש להעלות את שני הקבצים לפני ביצוע הבדיקה")
    
    with tab2:
        st.header("תוצאות בדיקה")
        
        if 'results' not in st.session_state:
            st.info("📝 טרם בוצעה בדיקה. העלה קבצים ולחץ על 'בצע בדיקה'")
        else:
            display_results(st.session_state.results)
    
    with tab3:
        st.header("📖 הנחיות שימוש")
        
        st.markdown("""
        ### איך להשתמש במערכת?
        
        #### 1. הכנת קובץ המחוון
        קובץ המחוון צריך להכיל את המבנה הבא:
        
        | עמודה A | עמודה B | עמודה C | עמודה D | עמודה E |
        |---------|---------|----------|----------|----------|
        | שם גליון | סעיף | תת-סעיף | ניקוד | הורדת ניקוד |
        
        **דוגמה:**
        ```
        | ריכוז הכנסות | חישובים | סה"כ לחיוב | 5 | 0 |
        | ריכוז הוצאות | נוסחאות | שימוש ב-SUM | 3 | 0 |
        ```
        
        #### 2. העלאת הקבצים
        - העלה את קובץ המחוון בצד שמאל
        - העלה את קובץ התלמיד בצד ימין
        - לחץ על "בצע בדיקה"
        
        #### 3. הגדרות מתקדמות
        בסרגל הצד ניתן להתאים:
        - **ציון חלקי**: אפשר ניקוד חלקי לבדיקות שעברו חלקית
        - **רגישות התאמה**: קובע עד כמה שמות הגליונות צריכים להיות דומים
        - **מצב קפדני**: בדיקה מחמירה יותר
        
        #### 4. מה המערכת בודקת?
        
        ✅ **קיום גליונות** - האם הגליונות הנדרשים קיימים
        
        ✅ **נוסחאות** - האם יש שימוש בנוסחאות
        
        ✅ **פונקציות ספציפיות**:
        - SUM - לסיכומים
        - IF - לתנאים
        - VLOOKUP - לחיפוש
        - COUNTIF - לספירה מותנית
        - SUMIF - לסיכום מותנה
        
        ✅ **הפניות בין גליונות** - שימוש ב-`גליון!תא`
        
        ✅ **תאי עזר** - שימוש בתאים עזר לחישובים
        
        #### 5. פענוח התוצאות
        
        - 🟢 **עבר** - הבדיקה עברה בהצלחה (80%+ מהדרישות)
        - 🟡 **עבר חלקית** - חלק מהדרישות התקיימו (50-79%)
        - 🔴 **נכשל** - הבדיקה נכשלה (פחות מ-50%)
        
        #### 6. ייצוא התוצאות
        ניתן להוריד את התוצאות בפורמטים:
        - **JSON** - לעיבוד אוטומטי
        - **TEXT** - לקריאה אנושית
        - **Excel** - לניתוח מפורט
        
        ---
        
        ### שאלות נפוצות
        
        **ש: מה קורה אם שם הגליון לא תואם בדיוק?**
        
        ת: המערכת משתמשת באלגוריתם התאמה חכם שמוצא גליונות דומים.
        
        **ש: האם המערכת בודקת את הערכים המחושבים?**
        
        ת: כרגע המערכת בודקת בעיקר את קיום הנוסחאות והפונקציות.
        
        **ש: איך אני יכול להתאים את הבדיקה לצרכים שלי?**
        
        ת: ניתן לערוך את קובץ המחוון ולהוסיף קריטריונים נוספים.
        
        ---
        
        ### תמיכה טכנית
        
        לבעיות או שאלות, אנא פנה למפתח המערכת.
        """)


def run_check(rubric_file, student_file, partial_credit, similarity_threshold, strict_mode):
    """הרצת בדיקה"""
    
    with st.spinner('🔄 מבצע בדיקה... אנא המתן'):
        try:
            # שמירת הקבצים לזמנית
            temp_dir = Path(tempfile.gettempdir())
            
            rubric_path = temp_dir / f"rubric_{rubric_file.name}"
            student_path = temp_dir / f"student_{student_file.name}"
            
            with open(rubric_path, 'wb') as f:
                f.write(rubric_file.getvalue())
            
            with open(student_path, 'wb') as f:
                f.write(student_file.getvalue())
            
            # הגדרות
            config = {
                'partial_credit': partial_credit,
                'sheet_name_similarity_threshold': similarity_threshold,
                'strict_mode': strict_mode
            }
            
            # יצירת הבודק
            checker = AdvancedExcelChecker(
                str(rubric_path),
                str(student_path),
                config,
                output_dir=str(temp_dir / "results")
            )
            
            # הרצת הבדיקה
            if checker.run_checks():
                # שמירת התוצאות ב-session state
                st.session_state.results = checker.results
                st.session_state.checker = checker
                
                # הצגת הודעת הצלחה
                st.success("✅ הבדיקה הושלמה בהצלחה!")
                st.balloons()
                
                # מעבר לטאב התוצאות
                st.rerun()
            else:
                st.error("❌ הבדיקה נכשלה. אנא בדוק את הקבצים.")
        
        except Exception as e:
            st.error(f"❌ שגיאה בביצוע הבדיקה: {str(e)}")
            st.exception(e)


def display_results(results):
    """הצגת תוצאות הבדיקה"""
    
    # סיכום כללי
    st.subheader("📊 סיכום כללי")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="ציון כולל",
            value=f"{results['total_score']:.1f}",
            delta=f"מתוך {results['max_score']}"
        )
    
    with col2:
        percentage = results['percentage']
        emoji = "🟢" if percentage >= 80 else "🟡" if percentage >= 60 else "🔴"
        st.metric(
            label="אחוז הצלחה",
            value=f"{percentage:.1f}%",
            delta=emoji
        )
    
    with col3:
        summary = results['summary']
        st.metric(
            label="בדיקות שעברו",
            value=summary['passed'],
            delta=f"מתוך {summary['total_checks']}"
        )
    
    with col4:
        st.metric(
            label="בדיקות שנכשלו",
            value=summary['failed'],
            delta=None
        )
    
    st.divider()
    
    # מיפוי גליונות
    if results.get('sheet_mapping'):
        with st.expander("🗺️ מיפוי גליונות", expanded=False):
            st.write("המערכת מיפתה את הגליונות הבאים:")
            for rubric_sheet, actual_sheet in results['sheet_mapping'].items():
                st.write(f"- **{rubric_sheet}** ← {actual_sheet}")
    
    # פירוט בדיקות
    st.subheader("📋 פירוט בדיקות")
    
    # סינון
    filter_status = st.multiselect(
        "סנן לפי סטטוס:",
        options=['עבר', 'עבר חלקית', 'נכשל', 'ממתין'],
        default=['עבר', 'עבר חלקית', 'נכשל']
    )
    
    # הצגת הבדיקות
    for i, check in enumerate(results['checks'], 1):
        if check['status'] not in filter_status:
            continue
        
        # אייקון סטטוס
        if check['status'] == 'עבר':
            status_color = "success-box"
            emoji = "✅"
        elif check['status'] == 'עבר חלקית':
            status_color = "warning-box"
            emoji = "⚠️"
        else:
            status_color = "error-box"
            emoji = "❌"
        
        with st.expander(f"{emoji} {i}. {check['sheet_rubric']} | {check['section']} | {check['subsection']}"):
            col_a, col_b = st.columns([2, 1])
            
            with col_a:
                st.markdown(f"**סטטוס:** {check['status']}")
                st.markdown(f"**ציון:** {check['earned_points']:.1f} / {check['max_points']}")
                
                if check['sheet_actual']:
                    st.markdown(f"**גליון:** {check['sheet_actual']}")
                
                if check['notes']:
                    st.markdown("**הערות:**")
                    for note in check['notes']:
                        st.write(f"- {note}")
            
            with col_b:
                # תרשים עוגה לציון
                if check['max_points'] > 0:
                    percentage = (check['earned_points'] / check['max_points']) * 100
                    st.progress(percentage / 100)
                    st.caption(f"{percentage:.0f}% מהניקוד")
            
            # דוגמאות נוסחאות
            if check.get('formulas_found'):
                st.markdown("**דוגמאות לנוסחאות:**")
                for formula in check['formulas_found'][:3]:
                    st.code(f"{formula['cell']}: {formula['formula']}", language="excel")
    
    st.divider()
    
    # כפתורי הורדה
    st.subheader("💾 ייצוא תוצאות")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # JSON
        json_str = json.dumps(results, ensure_ascii=False, indent=2)
        st.download_button(
            label="📄 הורד JSON",
            data=json_str,
            file_name=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    with col2:
        # TEXT
        if 'checker' in st.session_state:
            _, txt_path = st.session_state.checker.generate_report()
            with open(txt_path, 'r', encoding='utf-8') as f:
                txt_content = f.read()
            
            st.download_button(
                label="📝 הורד TEXT",
                data=txt_content,
                file_name=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
    
    with col3:
        # Excel
        if st.button("📊 ייצא ל-Excel"):
            export_to_excel(results)


def export_to_excel(results):
    """ייצוא תוצאות ל-Excel"""
    try:
        # יצירת DataFrame
        checks_data = []
        for check in results['checks']:
            checks_data.append({
                'גליון (מחוון)': check['sheet_rubric'],
                'גליון (בפועל)': check['sheet_actual'],
                'סעיף': check['section'],
                'תת-סעיף': check['subsection'],
                'סטטוס': check['status'],
                'ציון': check['earned_points'],
                'מקסימום': check['max_points'],
                'הערות': '\n'.join(check['notes'])
            })
        
        df = pd.DataFrame(checks_data)
        
        # שמירה לזמנית
        temp_file = Path(tempfile.gettempdir()) / f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        df.to_excel(temp_file, index=False, engine='openpyxl')
        
        # הורדה
        with open(temp_file, 'rb') as f:
            st.download_button(
                label="💾 שמור Excel",
                data=f.read(),
                file_name=temp_file.name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
        st.success("✅ קובץ Excel נוצר בהצלחה!")
    
    except Exception as e:
        st.error(f"❌ שגיאה ביצירת קובץ Excel: {e}")


if __name__ == "__main__":
    main()
