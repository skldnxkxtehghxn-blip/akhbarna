# أخبارنا — تحديث تلقائي

الموقع مصمم ليُستضاف على GitHub Pages. GitHub Actions يشغّل `scripts/fetch_news.py` يومياً ويحدث `news.json` من خلاصات Google News RSS.

## التشغيل
1. ارفع الملفات إلى مستودع GitHub.
2. فعّل GitHub Pages من Settings > Pages واختر GitHub Actions.
3. شغّل Workflow `تحديث أخبارنا` مرة يدوياً من Actions للتأكد من أول تحديث.

ملاحظة: خلاصات RSS تجمع عناوين وروابط الأخبار من الناشرين؛ اقرأ الخبر الأصلي من المصدر قبل إعادة نشره، واحترم حقوق النشر وسياسات المصادر.
