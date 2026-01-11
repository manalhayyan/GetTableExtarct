{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "bb7ea6d1-cdaa-4596-96bb-d00c2be84782",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2026-01-11 20:02:29.394 \n",
      "  \u001b[33m\u001b[1mWarning:\u001b[0m to view this Streamlit app on a browser, run it with the following\n",
      "  command:\n",
      "\n",
      "    streamlit run C:\\ProgramData\\anaconda3\\Lib\\site-packages\\ipykernel_launcher.py [ARGUMENTS]\n"
     ]
    }
   ],
   "source": [
    "import streamlit as st\n",
    "import re\n",
    "# إعداد الصفحة\n",
    "st.set_page_config(page_title=\"Table Extractor\", layout=\"centered\")\n",
    "st.title(\"📄 استخراج أسماء الجداول\")\n",
    "st.write(\"ارفع ملف نصي (TXT) وسيتم عرض أسماء الجداول الموجودة فيه\")\n",
    "# ============================\n",
    "# رفع الملف\n",
    "# ============================\n",
    "uploaded_file = st.file_uploader(\"📤 اختر ملف txt\", type=[\"txt\"])\n",
    "if uploaded_file is not None:\n",
    "   # قراءة محتوى الملف\n",
    "   text = uploaded_file.read().decode(\"utf-8\")\n",
    "   # ============================\n",
    "   # إزالة التعليقات\n",
    "   # ============================\n",
    "   text_clean = re.sub(r'--.*', '', text)\n",
    "   text_clean = re.sub(r'/\\*.*?\\*/', '', text_clean, flags=re.DOTALL)\n",
    "   tables = []\n",
    "   # ============================\n",
    "   # دالة تنظيف اسم الجدول\n",
    "   # ============================\n",
    "   def clean_table_name(name):\n",
    "       name = name.split()[0]               # إزالة alias\n",
    "       name = re.split(r'[#\"(\\}]', name)[0] # إيقاف عند الرموز غير المرغوب فيها\n",
    "       return name.strip()\n",
    "   # ============================\n",
    "   # استخراج FROM\n",
    "   # ============================\n",
    "   from_pattern = r'\\bFROM\\s+([^\\s;]+(?:\\s*,\\s*[^\\s;]+)*)'\n",
    "   from_matches = re.findall(from_pattern, text_clean, re.IGNORECASE)\n",
    "   for part in from_matches:\n",
    "       for t in part.split(','):\n",
    "           t = t.strip()\n",
    "           if t and not t.startswith('('):\n",
    "               tables.append(clean_table_name(t))\n",
    "   # ============================\n",
    "   # استخراج JOIN\n",
    "   # ============================\n",
    "   join_pattern = r'\\bJOIN\\s+([^\\s\\(\\);]+)'\n",
    "   join_matches = re.findall(join_pattern, text_clean, re.IGNORECASE)\n",
    "   for t in join_matches:\n",
    "       if not t.startswith('('):\n",
    "           tables.append(clean_table_name(t))\n",
    "   # ============================\n",
    "   # إزالة التكرار\n",
    "   # ============================\n",
    "   tables_unique = list(dict.fromkeys(tables))\n",
    "   # ============================\n",
    "   # عرض النتائج\n",
    "   # ============================\n",
    "   st.success(f\"✅ تم استخراج {len(tables_unique)} جدول\")\n",
    "   st.subheader(\"📋 أسماء الجداول\")\n",
    "   for table in tables_unique:\n",
    "       st.write(table)\n",
    "   # ============================\n",
    "   # تحميل النتائج كملف txt\n",
    "   # ============================\n",
    "   st.download_button(\n",
    "       label=\"⬇️ تحميل أسماء الجداول\",\n",
    "       data=\"\\n\".join(tables_unique),\n",
    "       file_name=\"tables_list.txt\",\n",
    "       mime=\"text/plain\"\n",
    "   )"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
