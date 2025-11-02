#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
אפליקציית Streamlit לבדיקת מטלות אקסל - גרסה משודרגת
תומכת בבדיקת מספר מטלות בבת אחת
"""

import streamlit as st
import openpyxl
import pandas as pd
import json
from datetime import datetime
from pathlib import Path
import tempfile
import sys
import zipfile
import io

# הוספת הנתיב לסוכן הבדיקה
sys.path.insert(0, str(Path(__file__).parent))
from excel_checker_advanced import AdvancedExcelChecker
from batch_excel_checker import BatchExcelChecker


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
</style>
""", unsafe_allow_html=True)


def main():
    """פונקציה ראשית"""
    
    # כותרת
    st.markdown('<div class="main-header"><h1>📊 מערכת בדיקת מטלות אקסל - גרסה משודרגת</h1><p>בדיקה אוטומטית של עד 50 מטלות בבת אחת!</p></div>', unsafe_allow_html=True)
    
    # סרגל צד - הגדרות
    with st.sidebar:
        st.header("⚙️ הגדרות")
        
        st.subheader("מצב עבודה")
        mode = st.radio(
            "בחרי מצב:",
            ["מטלה בודדת", "מספר מטלות (Batch)"],
            help="בחרי אם לבדוק מטלה אחת או מספר מטלות בבת אחת"
        )
        
        st.divider()
        
        st.subheader("הגדרות בדיקה")
        partial_credit = st.checkbox("ציון חלקי", value=True)
        
        similarity_threshold = st.slider(
            "רגישות התאמת שמות גליונות",
            min_value=0.3, max_value=1.0, value=0.6, step=0.1
        )
        
        strict_mode = st.checkbox("מצב קפדני", value=False)
        
        st.divider()
        
        # הגדרות API (אופציונלי)
        st.subheader("🤖 בדיקה חכמה (אופציונלי)")
        use_ai = st.checkbox(
            "השתמש ב-Claude API",
            help="לבדיקות מתקדמות יותר עם AI",
            value=False
        )
        
        if use_ai:
            api_key = st.text_input(
                "מפתח API:",
                type="password",
                help="הכנס את מפתח Claude API שלך"
            )
            if api_key:
                import os
                os.environ['ANTHROPIC_API_KEY'] = api_key
        
        st.divider()
        st.info("""
        **גרסה משודרגת 2.0**
        
        ✨ תכונות חדשות:
        - בדיקת עד 50 מטלות
        - גליון בדיקה בכל מטלה
        - קובץ סיכום Excel
        - תמיכה ב-Claude API
        """)
    
    # תוכן ראשי
    if mode == "מטלה בודדת":
        show_single_mode()
    else:
        show_batch_mode()


def show_single_mode():
    """מצב בדיקת מטלה בודדת"""
    
    tab1, tab2 = st.tabs(["📤 העלאת קבצים", "📊 תוצאות"])
    
    with tab1:
        st.header("העלאת קבצים - מטלה בודדת")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("1️⃣ העלה קובץ מחוון")
            rubric_file = st.file_uploader(
                "בחר קובץ אקסל של המחוון",
                type=['xlsx', 'xls'],
                key="rubric_single"
            )
            
            if rubric_file:
                st.success(f"✅ נטען: {rubric_file.name}")
        
        with col2:
            st.subheader("2️⃣ העלה קובץ תלמיד")
            student_file = st.file_uploader(
                "בחר קובץ אקסל של התלמיד",
                type=['xlsx', 'xls'],
                key="student_single"
            )
            
            if student_file:
                st.success(f"✅ נטען: {student_file.name}")
        
        st.divider()
        
        if rubric_file and student_file:
            if st.button("🔍 בצע בדיקה", type="primary", use_container_width=True):
                run_single_check(rubric_file, student_file)
        else:
            st.warning("⚠️ יש להעלות את שני הקבצים")
    
    with tab2:
        st.header("תוצאות בדיקה")
        
        if 'results' in st.session_state:
            display_results(st.session_state.results)
        else:
            st.info("📝 טרם בוצעה בדיקה")


def show_batch_mode():
    """מצב בדיקת מספר מטלות"""
    
    tab1, tab2, tab3 = st.tabs(["📤 העלאת קבצים", "📊 תוצאות", "📥 הורדות"])
    
    with tab1:
        st.header("העלאת קבצים - מספר מטלות")
        
        st.subheader("1️⃣ העלה קובץ מחוון")
        rubric_file = st.file_uploader(
            "בחר קובץ אקסל של המחוון",
            type=['xlsx', 'xls'],
            key="rubric_batch"
        )
        
        if rubric_file:
            st.success(f"✅ מחוון נטען: {rubric_file.name}")
        
        st.divider()
        
        st.subheader("2️⃣ העלה קבצי מטלות (עד 50)")
        student_files = st.file_uploader(
            "בחר קבצי אקסל של תלמידים",
            type=['xlsx', 'xls'],
            accept_multiple_files=True,
            key="students_batch"
        )
        
        if student_files:
            st.success(f"✅ נטענו {len(student_files)} מטלות")
            
            # תצוגה מקדימה של הקבצים
            with st.expander("👁️ רשימת הקבצים שנטענו"):
                for idx, file in enumerate(student_files, 1):
                    st.write(f"{idx}. {file.name}")
        
        st.divider()
        
        # אפשרות להזנת מזהים מותאמים אישית
        with st.expander("⚙️ הגדרות מתקדמות (אופציונלי)"):
            custom_ids = st.text_area(
                "מזהי תלמידים (שורה אחת לכל תלמיד):",
                height=150,
                help="אם ריק, ישתמש בשמות הקבצים"
            )
        
        if rubric_file and student_files:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🚀 בצע בדיקה לכל המטלות", type="primary", use_container_width=True):
                    student_ids = None
                    if custom_ids:
                        student_ids = [line.strip() for line in custom_ids.split('\n') if line.strip()]
                    
                    run_batch_check(rubric_file, student_files, student_ids)
        else:
            st.warning("⚠️ יש להעלות מחוון ולפחות מטלה אחת")
    
    with tab2:
        st.header("תוצאות בדיקות")
        
        if 'batch_results' in st.session_state:
            display_batch_results(st.session_state.batch_results)
        else:
            st.info("📝 טרם בוצעה בדיקה")
    
    with tab3:
        st.header("הורדת קבצים")
        
        if 'batch_results' in st.session_state:
            display_download_section()
        else:
            st.info("📝 אין תוצאות להורדה")


def run_single_check(rubric_file, student_file):
    """הרצת בדיקה של מטלה בודדת"""
    
    with st.spinner('🔄 מבצע בדיקה...'):
        try:
            temp_dir = Path(tempfile.gettempdir())
            
            rubric_path = temp_dir / f"rubric_{rubric_file.name}"
            student_path = temp_dir / f"student_{student_file.name}"
            
            with open(rubric_path, 'wb') as f:
                f.write(rubric_file.getvalue())
            
            with open(student_path, 'wb') as f:
                f.write(student_file.getvalue())
            
            config = {
                'partial_credit': st.session_state.get('partial_credit', True),
                'sheet_name_similarity_threshold': st.session_state.get('similarity_threshold', 0.6),
                'strict_mode': st.session_state.get('strict_mode', False)
            }
            
            checker = AdvancedExcelChecker(
                str(rubric_path),
                str(student_path),
                config,
                output_dir=str(temp_dir / "results")
            )
            
            if checker.run_checks():
                st.session_state.results = checker.results
                st.session_state.checker = checker
                st.success("✅ הבדיקה הושלמה!")
                st.balloons()
                st.rerun()
            else:
                st.error("❌ הבדיקה נכשלה")
        
        except Exception as e:
            st.error(f"❌ שגיאה: {str(e)}")
            st.exception(e)


def run_batch_check(rubric_file, student_files, student_ids=None):
    """הרצת בדיקה של מספר מטלות"""
    
    with st.spinner(f'🔄 מבצע בדיקה של {len(student_files)} מטלות... אנא המתן'):
        try:
            temp_dir = Path(tempfile.gettempdir()) / "batch_check"
            temp_dir.mkdir(exist_ok=True)
            
            # שמירת מחוון
            rubric_path = temp_dir / f"rubric_{rubric_file.name}"
            with open(rubric_path, 'wb') as f:
                f.write(rubric_file.getvalue())
            
            # שמירת כל קבצי התלמידים
            student_paths = []
            for student_file in student_files:
                student_path = temp_dir / student_file.name
                with open(student_path, 'wb') as f:
                    f.write(student_file.getvalue())
                student_paths.append(str(student_path))
            
            # הגדרות
            config = {
                'partial_credit': st.session_state.get('partial_credit', True),
                'sheet_name_similarity_threshold': st.session_state.get('similarity_threshold', 0.6),
                'strict_mode': st.session_state.get('strict_mode', False)
            }
            
            # יצירת בודק Batch
            checker = BatchExcelChecker(
                rubric_file=str(rubric_path),
                config=config,
                output_dir=str(temp_dir / "results"),
                use_ai=False
            )
            
            # הרצת הבדיקה
            if checker.check_batch(student_paths, student_ids):
                st.session_state.batch_results = checker.batch_results
                st.session_state.batch_checker = checker
                st.session_state.summary_file = checker.summary_df
                st.success(f"✅ בדיקת {len(student_files)} מטלות הושלמה!")
                st.balloons()
                st.rerun()
            else:
                st.error("❌ הבדיקה נכשלה")
        
        except Exception as e:
            st.error(f"❌ שגיאה: {str(e)}")
            st.exception(e)


def display_results(results):
    """הצגת תוצאות מטלה בודדת"""
    
    # סיכום
    st.subheader("📊 סיכום")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("ציון כולל", f"{results['total_score']:.1f}", 
                 f"מתוך {results['max_score']}")
    
    with col2:
        percentage = results['percentage']
        emoji = "🟢" if percentage >= 80 else "🟡" if percentage >= 60 else "🔴"
        st.metric("אחוז הצלחה", f"{percentage:.1f}%", emoji)
    
    with col3:
        st.metric("בדיקות שעברו", results['summary']['passed'],
                 f"מתוך {results['summary']['total_checks']}")
    
    with col4:
        st.metric("בדיקות שנכשלו", results['summary']['failed'])
    
    st.divider()
    
    # פירוט בדיקות
    st.subheader("📋 פירוט בדיקות")
    
    for i, check in enumerate(results['checks'], 1):
        status_emoji = "✅" if check['status'] == 'עבר' else "⚠️" if check['status'] == 'עבר חלקית' else "❌"
        
        with st.expander(f"{status_emoji} {check['section']} | {check['subsection']}"):
            col_a, col_b = st.columns([2, 1])
            
            with col_a:
                st.markdown(f"**סטטוס:** {check['status']}")
                st.markdown(f"**ציון:** {check['earned_points']:.1f} / {check['max_points']}")
                
                if check['notes']:
                    st.markdown("**הערות:**")
                    for note in check['notes']:
                        st.write(f"- {note}")
            
            with col_b:
                if check['max_points'] > 0:
                    percentage = (check['earned_points'] / check['max_points']) * 100
                    st.progress(percentage / 100)
                    st.caption(f"{percentage:.0f}%")


def display_batch_results(results):
    """הצגת תוצאות batch"""
    
    st.subheader(f"📊 סיכום {len(results)} מטלות")
    
    # סטטיסטיקות כלליות
    col1, col2, col3, col4 = st.columns(4)
    
    total_passed = sum(1 for r in results if r['percentage'] >= 80)
    total_partial = sum(1 for r in results if 60 <= r['percentage'] < 80)
    total_failed = sum(1 for r in results if r['percentage'] < 60)
    avg_score = sum(r['percentage'] for r in results) / len(results)
    
    with col1:
        st.metric("עברו", total_passed, "🟢")
    
    with col2:
        st.metric("עברו חלקית", total_partial, "🟡")
    
    with col3:
        st.metric("נכשלו", total_failed, "🔴")
    
    with col4:
        st.metric("ממוצע", f"{avg_score:.1f}%")
    
    st.divider()
    
    # טבלת תוצאות
    st.subheader("📋 טבלת תוצאות")
    
    table_data = []
    for result in results:
        table_data.append({
            'מספר מטלה': result['student_id'],
            'ציון': f"{result['total_score']:.1f}",
            'מקסימום': result['max_score'],
            'אחוז': f"{result['percentage']:.1f}%",
            'סטטוס': '🟢 עבר' if result['percentage'] >= 80 else '🟡 חלקי' if result['percentage'] >= 60 else '🔴 נכשל'
        })
    
    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True)


def display_download_section():
    """סעיף הורדות"""
    
    st.subheader("💾 הורדת קבצים")
    
    if 'batch_checker' not in st.session_state:
        st.warning("אין קבצים להורדה")
        return
    
    checker = st.session_state.batch_checker
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📊 קובץ סיכום Excel")
        st.write("כולל את כל התוצאות בטבלה אחת")
        
        if st.session_state.get('summary_file') is not None:
            # המרה ל-Excel להורדה
            summary_excel = io.BytesIO()
            st.session_state.summary_file.to_excel(summary_excel, index=False)
            summary_excel.seek(0)
            
            st.download_button(
                label="📥 הורד קובץ סיכום",
                data=summary_excel,
                file_name=f"סיכום_מטלות_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    
    with col2:
        st.markdown("### 📁 קבצי מטלות עם בדיקה")
        st.write("כל מטלה עם גליון בדיקה")
        
        if st.button("📦 הכן ארכיון להורדה"):
            create_zip_archive()
    
    with col3:
        st.markdown("### 📄 דוחות JSON")
        st.write("נתונים גולמיים לעיבוד")
        
        json_data = json.dumps(st.session_state.batch_results, ensure_ascii=False, indent=2)
        st.download_button(
            label="📥 הורד JSON",
            data=json_data,
            file_name=f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )


def create_zip_archive():
    """יצירת ארכיון ZIP עם כל הקבצים"""
    
    with st.spinner('📦 יוצר ארכיון... אנא המתן'):
        try:
            checker = st.session_state.batch_checker
            output_dir = checker.output_dir
            
            # יצירת ZIP בזיכרון
            zip_buffer = io.BytesIO()
            
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                # הוספת כל הקבצים
                for student_result in st.session_state.batch_results:
                    student_id = student_result['student_id']
                    student_dir = output_dir / student_id
                    
                    if student_dir.exists():
                        for file_path in student_dir.glob('*'):
                            if file_path.is_file():
                                zip_file.write(file_path, f"{student_id}/{file_path.name}")
            
            zip_buffer.seek(0)
            
            st.download_button(
                label="💾 הורד ארכיון ZIP",
                data=zip_buffer,
                file_name=f"כל_המטלות_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                mime="application/zip"
            )
            
            st.success("✅ ארכיון מוכן להורדה!")
        
        except Exception as e:
            st.error(f"❌ שגיאה ביצירת ארכיון: {e}")


if __name__ == "__main__":
    main()
