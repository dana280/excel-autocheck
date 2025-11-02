# 📊 מערכת בדיקת מטלות אקסל

מערכת אוטומטית לבדיקת מטלות אקסל אקדמיות מול מחוון, עם תמיכה בפונקציות ונוסחאות מתקדמות.

## 🎯 תכונות

- ✅ בדיקת קיום גליונות
- ✅ זיהוי ובדיקת נוסחאות
- ✅ זיהוי שימוש בפונקציות ספציפיות (SUM, IF, VLOOKUP, וכו')
- ✅ בדיקת הפניות בין גליונות
- ✅ זיהוי תאי עזר
- ✅ התאמה חכמה של שמות גליונות
- ✅ ציון חלקי אופציונלי
- ✅ ייצוא תוצאות ל-JSON, TEXT ו-Excel

## 🚀 התקנה והפעלה

### דרישות מקדימות

- Python 3.8 ומעלה
- pip

### התקנה מקומית

1. שכפל את הפרויקט:
```bash
git clone https://github.com/YOUR_USERNAME/excel-checker.git
cd excel-checker
```

2. התקן את החבילות הנדרשות:
```bash
pip install -r requirements.txt
```

3. הרץ את האפליקציה:
```bash
streamlit run streamlit_app.py
```

## 🌐 פריסה ב-Streamlit Cloud

1. העלה את הקוד ל-GitHub
2. היכנס ל-[Streamlit Cloud](https://streamlit.io/cloud)
3. לחץ על "New app"
4. בחר את הריפוזיטורי שלך
5. הגדר:
   - **Main file path**: `streamlit_app.py`
   - **Python version**: 3.8+
6. לחץ על "Deploy"

## 📖 שימוש

### שימוש דרך ממשק ה-Web (Streamlit)

1. העלה קובץ מחוון (Excel)
2. העלה קובץ תלמיד לבדיקה (Excel)
3. התאם הגדרות בסרגל הצד (אופציונלי)
4. לחץ על "בצע בדיקה"
5. צפה בתוצאות והורד דוחות

### שימוש דרך Command Line

```bash
python excel_checker_advanced.py <קובץ_מחוון.xlsx> <קובץ_תלמיד.xlsx>
```

דוגמה:
```bash
python excel_checker_advanced.py rubric.xlsx student_work.xlsx
```

## 📋 מבנה קובץ המחוון

קובץ המחוון צריך להכיל את העמודות הבאות:

| עמודה | תיאור | דוגמה |
|-------|-------|--------|
| A | שם הגליון | "ריכוז הכנסות" |
| B | סעיף | "חישובים בסיסיים" |
| C | תת-סעיף | "סה\"כ לחיוב" |
| D | ניקוד מקסימלי | 5 |
| E | הורדת ניקוד (אופציונלי) | 0 |

### דוגמה למחוון:

```
| גליון          | סעיף              | תת סעיף           | ניקוד | הורדה |
|----------------|-------------------|-------------------|-------|-------|
| ריכוז הכנסות   | חישובים          | סה"כ מע"מ         | 5     | 0     |
| ריכוז הכנסות   | נוסחאות          | שימוש ב-SUM       | 3     | 0     |
| ריכוז הוצאות   | תנאים            | שימוש ב-IF        | 4     | 0     |
```

## 🔧 הגדרות מתקדמות

### בממשק Web

- **ציון חלקי**: מאפשר ניקוד חלקי לבדיקות שעברו חלקית
- **רגישות התאמה**: קובע את רמת הדמיון הנדרשת בין שמות גליונות
- **מצב קפדני**: בדיקה מחמירה יותר

### בקוד Python

```python
config = {
    'sheet_name_similarity_threshold': 0.6,  # 0.0-1.0
    'partial_credit': True,                  # True/False
    'strict_mode': False,                    # True/False
    'check_formulas': True,                  # True/False
    'check_functions': True,                 # True/False
    'check_references': True                 # True/False
}

checker = AdvancedExcelChecker(rubric_file, student_file, config)
```

## 📊 פענוח תוצאות

### סטטוסים

- 🟢 **עבר** - 80%+ מהדרישות התקיימו
- 🟡 **עבר חלקית** - 50-79% מהדרישות התקיימו
- 🔴 **נכשל** - פחות מ-50% מהדרישות התקיימו

### פורמטי ייצוא

1. **JSON** - לעיבוד אוטומטי ואינטגרציה עם מערכות אחרות
2. **TEXT** - דוח קריא לבני אדם
3. **Excel** - לניתוח מפורט והמשך עיבוד

## 🛠️ מבנה הפרויקט

```
excel-checker/
├── streamlit_app.py              # אפליקציית Streamlit
├── excel_checker_advanced.py     # מנוע הבדיקה
├── requirements.txt              # חבילות נדרשות
├── README.md                     # תיעוד
├── .gitignore                    # קבצים להתעלמות
└── examples/                     # דוגמאות
    ├── rubric_example.xlsx
    └── student_example.xlsx
```

## 🤝 תרומה לפרויקט

נשמח לקבל תרומות! אנא:

1. עשה Fork לפרויקט
2. צור branch חדש (`git checkout -b feature/amazing-feature`)
3. בצע Commit לשינויים (`git commit -m 'Add amazing feature'`)
4. דחוף ל-Branch (`git push origin feature/amazing-feature`)
5. פתח Pull Request

## 📝 רישיון

פרויקט זה זמין תחת רישיון MIT. ראה קובץ `LICENSE` לפרטים.

## 👥 יוצרים

פותח עבור מוסדות אקדמיים לבדיקת מטלות אקסל.

## 🐛 דיווח על בעיות

נמצאת בעיה? [פתח issue](https://github.com/YOUR_USERNAME/excel-checker/issues)

## 📞 יצירת קשר

לשאלות ותמיכה, אנא פנה דרך GitHub Issues.

---

## 🎓 דוגמאות שימוש

### דוגמה 1: בדיקה בסיסית

```python
from excel_checker_advanced import AdvancedExcelChecker

checker = AdvancedExcelChecker('rubric.xlsx', 'student.xlsx')
checker.run_checks()
checker.generate_report()
```

### דוגמה 2: בדיקה עם הגדרות מותאמות

```python
config = {
    'partial_credit': False,  # ללא ציון חלקי
    'strict_mode': True       # מצב קפדני
}

checker = AdvancedExcelChecker('rubric.xlsx', 'student.xlsx', config)
checker.run_checks()
json_path, txt_path = checker.generate_report()
```

## 🔍 מה המערכת בודקת?

### 1. קיום גליונות
- בדיקה שכל הגליונות הנדרשים קיימים
- התאמה חכמה של שמות דומים

### 2. נוסחאות
- זיהוי נוסחאות בתאים
- ספירת נוסחאות לפי גליון

### 3. פונקציות ספציפיות
המערכת מזהה ובודקת:
- `SUM` - סיכומים
- `IF` - תנאים
- `VLOOKUP` / `HLOOKUP` - חיפוש
- `COUNTIF` - ספירה מותנית
- `SUMIF` - סיכום מותנה
- ועוד...

### 4. הפניות בין גליונות
- זיהוי שימוש בהפניות מסוג `Sheet1!A1`
- בדיקת קישורים בין גליונות

### 5. תאי עזר
- זיהוי שימוש בתאי ביניים
- בדיקת מבנה חישובים

## 🎯 מקרי שימוש

- ✅ בדיקת מטלות סטודנטים בקורסי אקסל
- ✅ הערכה אוטומטית של תרגילים
- ✅ בקרת איכות של קבצי אקסל
- ✅ בדיקת עמידה בסטנדרטים

## 📈 ביצועים

- בדיקת קובץ ממוצע: 2-5 שניות
- תמיכה בקבצים עד 100MB
- עיבוד מקביל של בדיקות

## 🔒 אבטחה ופרטיות

- הקבצים מעובדים באופן מקומי
- אין שליחת מידע לשרתים חיצוניים
- קבצים זמניים נמחקים אוטומטית

## 🌟 תכונות עתידיות

- [ ] תמיכה בתרשימים
- [ ] בדיקת ערכים מחושבים
- [ ] השוואה לפתרון מלא
- [ ] ייצוא ל-PDF
- [ ] API REST
- [ ] תמיכה במספר שפות

---

Made with ❤️ for educators and students
