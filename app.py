import os
from flask import Flask, render_template_string, request, redirect, url_for, session, send_from_directory
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import URL

app = Flask(__name__)
app.secret_key = 'salam_srca_secure_key_2026'

# إعداد قاعدة البيانات الدائمة
db_url = URL.create(
    drivername="postgresql",
    username="postgres.pfrqplchfsgwxqmeixql",
    password="Salam89Srca",
    host="aws-0-ap-northeast-1.pooler.supabase.com",
    port=6543,
    database="postgres"
)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

USER_CREDENTIALS = {
    "username": "salamsrca",
    "password": "srcca89"
}

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    file = db.Column(db.String(255), nullable=False)

class ArchiveItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    file = db.Column(db.String(255), nullable=False)

with app.app_context():
    db.create_all()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>سلطانة - قطاع السلام</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #ffffff; color: #1f2937; font-family: Tahoma, sans-serif; }
        .bg-custom-red { background-color: #dc2626; }
        .text-custom-red { color: #dc2626; }
        .border-custom-red { border-color: #dc2626; }
        .hover-red:hover { background-color: #b91c1c; }
    </style>
</head>
<body class="min-h-screen flex flex-col">

    {% if not session.get('logged_in') %}
    <div class="flex items-center justify-center flex-grow bg-gray-50">
        <div class="bg-white p-8 rounded-xl shadow-md w-full max-w-md border-t-4 border-custom-red">
            <h2 class="text-2xl font-bold text-center text-custom-red mb-6">سلطانة - قطاع السلام</h2>
            {% if error %}
                <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-2 rounded mb-4 text-sm">{{ error }}</div>
            {% endif %}
            <form method="POST" action="/login" class="space-y-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">اسم المستخدم</label>
                    <input type="text" name="username" required class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:border-custom-red">
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">كلمة المرور</label>
                    <input type="password" name="password" required class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:border-custom-red">
                </div>
                <button type="submit" class="w-full bg-custom-red text-white py-2 rounded-lg hover-red transition font-semibold">دخول النظام</button>
            </form>
        </div>
    </div>
    {% else %}
    <header class="bg-white border-b border-gray-200 shadow-sm">
        <div class="container mx-auto px-4 py-4 flex justify-between items-center">
            <h1 class="text-xl font-bold text-custom-red flex items-center gap-2">
                <span>🛡️</span> سلطانة - قطاع السلام
            </h1>
            <div class="flex items-center gap-4">
                <span class="text-sm text-gray-600">مرحباً، <b>salamsrca</b></span>
                <a href="/logout" class="bg-gray-100 text-red-600 px-3 py-1.5 rounded-lg text-sm hover:bg-red-50 transition">تسجيل الخروج</a>
            </div>
        </div>
        <nav class="bg-gray-50 border-t border-gray-100">
            <div class="container mx-auto px-4 flex gap-6 py-2">
                <a href="/" class="text-gray-700 hover:text-custom-red font-medium transition">الرئيسية</a>
                <a href="/employees" class="text-gray-700 hover:text-custom-red font-medium transition">الموظفين</a>
                <a href="/archive" class="text-gray-700 hover:text-custom-red font-medium transition">الأرشيف</a>
            </div>
        </nav>
    </header>

    <main class="container mx-auto px-4 py-8 flex-grow">
        {% if active_tab == 'home' %}
        <div class="space-y-6">
            <div class="bg-red-50 border-r-4 border-custom-red p-6 rounded-lg shadow-sm">
                <h2 class="text-2xl font-bold text-custom-red mb-2">مرحباً بك في نظام سلطانة</h2>
                <p class="text-gray-600">لوحة التحكم المركزية لإدارة الموظفين وأرشفة المستندات والتوكيلات والسيارات والحوادث والبلاغات بقطاع السلام (قاعدة بيانات دائمة).</p>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm hover:border-custom-red transition">
                    <h3 class="text-lg font-bold text-custom-red mb-2">👥 إدارة الموظفين</h3>
                    <p class="text-gray-600 text-sm mb-4">إضافة وتعديل بيانات الموظفين والمسميات الوظيفية وإرفاق الشهادات.</p>
                    <a href="/employees" class="text-custom-red font-semibold text-sm hover:underline">الانتقال للموظفين &larr;</a>
                </div>
                <div class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm hover:border-custom-red transition">
                    <h3 class="text-lg font-bold text-custom-red mb-2">📁 الأرشيف المركزي</h3>
                    <p class="text-gray-600 text-sm mb-4">إدارة النماذج، التوكيلات، السيارات، الحوادث، بلاغات خارج النطاق، وأخرى.</p>
                    <a href="/archive" class="text-custom-red font-semibold text-sm hover:underline">الانتقال للأرشيف &larr;</a>
                </div>
            </div>
        </div>

        {% elif active_tab == 'employees' %}
        <div class="space-y-6">
            <h2 class="text-2xl font-bold text-custom-red">إدارة الموظفين والشهادات</h2>
            
            <div class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
                <h3 class="text-lg font-semibold mb-4 text-gray-800">إضافة موظف جديد</h3>
                <form method="POST" action="/employees/add" enctype="multipart/form-data" class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">اسم الموظف</label>
                        <input type="text" name="name" required class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:border-custom-red">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">المسمى الوظيفي</label>
                        <input type="text" name="title" required class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:border-custom-red">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">ارفاق الشهادة / الملف</label>
                        <input type="file" name="certificate" required class="w-full px-2 py-1.5 border rounded-lg text-sm bg-gray-50">
                    </div>
                    <div class="md:col-span-3">
                        <button type="submit" class="bg-custom-red text-white px-6 py-2 rounded-lg hover-red transition font-semibold">حفظ وإضافة</button>
                    </div>
                </form>
            </div>

            <div class="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
                <table class="w-full text-right border-collapse">
                    <thead>
                        <tr class="bg-gray-50 border-b border-gray-200 text-gray-700 text-sm">
                            <th class="p-3">اسم الموظف</th>
                            <th class="p-3">المسمى الوظيفي</th>
                            <th class="p-3">الشهادة / المرفق</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-100 text-sm">
                        {% for emp in employees %}
                        <tr>
                            <td class="p-3 font-medium">{{ emp.name }}</td>
                            <td class="p-3 text-gray-600">{{ emp.title }}</td>
                            <td class="p-3">
                                <a href="/uploads/{{ emp.file }}" target="_blank" class="text-custom-red hover:underline font-semibold">عرض المرفق 📄</a>
                            </td>
                        </tr>
                        {% else %}
                        <tr>
                            <td colspan="3" class="p-6 text-center text-gray-400">لا توجد بيانات موظفين مضافة حتى الآن.</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>

        {% elif active_tab == 'archive' %}
        <div class="space-y-6">
            <h2 class="text-2xl font-bold text-custom-red">الأرشيف المركزي</h2>

            <div class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
                <h3 class="text-lg font-semibold mb-4 text-gray-800">إضافة ملف للأرشيف</h3>
                <form method="POST" action="/archive/add" enctype="multipart/form-data" class="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">القسم الداخلي</label>
                        <select name="category" class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:border-custom-red">
                            <option value="النماذج">النماذج</option>
                            <option value="التوكيلات">التوكيلات</option>
                            <option value="السيارات">السيارات</option>
                            <option value="الحوادث">الحوادث</option>
                            <option value="بلاغات خارج النطاق">بلاغات خارج النطاق</option>
                            <option value="اخرى">اخرى</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">عنوان الملف / الوصف</label>
                        <input type="text" name="title" required class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:border-custom-red">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">ملف المرفق</label>
                        <input type="file" name="file" required class="w-full px-2 py-1.5 border rounded-lg text-sm bg-gray-50">
                    </div>
                    <div class="flex items-end">
                        <button type="submit" class="w-full bg-custom-red text-white py-2 rounded-lg hover-red transition font-semibold">رفع للأرشيف</button>
                    </div>
                </form>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                {% for cat_name in ["النماذج", "التوكيلات", "السيارات", "الحوادث", "بلاغات خارج النطاق", "اخرى"] %}
                <div class="bg-white p-5 rounded-xl border border-gray-200 shadow-sm flex flex-col justify-between">
                    <div>
                        <h3 class="text-md font-bold text-custom-red mb-3 pb-2 border-b border-gray-100 flex justify-between items-center">
                            <span>📂 {{ cat_name }}</span>
                        </h3>
                        <ul class="space-y-2 mb-4 max-h-48 overflow-y-auto">
                            {% set items = archives.get(cat_name, []) %}
                            {% for item in items %}
                         <li class="text-sm flex justify-between items-center bg-gray-50 p-2 rounded">
    <span class="truncate max-w-[140px]" title="{{ item.title }}">{{ item.title }}</span>
    <div class="flex items-center gap-2">
        <a href="/uploads/{{ item.file }}" target="_blank" class="text-custom-red hover:underline font-semibold">استعراض</a>
        <form action="{{ url_for('delete_archive', id=item.id) }}" method="POST" onsubmit="return confirm('هل أنت متأكد من الحذف؟');" style="display:inline;">
            <button type="submit" class="text-red-600 hover:text-red-800 text-xs font-semibold bg-transparent border-0 cursor-pointer">حذف</button>
        </form>
    </div>
</li>
                            {% else %}
                            <li class="text-xs text-gray-400 text-center py-4">القسم فارغ</li>
                            {% endfor %}
                        </ul>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
        {% endif %}
    </main>

    <footer class="bg-white border-t border-gray-200 py-4 text-center text-xs text-gray-500">
        جميع الحقوق محفوظة &copy; سلطانة - قطاع السلام 2026
    </footer>
    {% endif %}
</body>
</html>
"""

@app.route('/')
def index():
    if not session.get('logged_in'):
        return render_template_string(HTML_TEMPLATE, error=None)
    return render_template_string(HTML_TEMPLATE, active_tab='home')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if username == USER_CREDENTIALS["username"] and password == USER_CREDENTIALS["password"]:
        session['logged_in'] = True
        return redirect(url_for('index'))
    return render_template_string(HTML_TEMPLATE, error="اسم المستخدم أو كلمة المرور غير صحيحة")

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

@app.route('/employees')
def employees_page():
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    all_employees = Employee.query.all()
    return render_template_string(HTML_TEMPLATE, active_tab='employees', employees=all_employees)

@app.route('/employees/add', methods=['POST'])
def add_employee():
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    name = request.form.get('name')
    title = request.form.get('title')
    file = request.files.get('certificate')
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        new_emp = Employee(name=name, title=title, file=filename)
        db.session.add(new_emp)
        db.session.commit()
    return redirect(url_for('employees_page'))

@app.route('/archive')
def archive_page():
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    all_items = ArchiveItem.query.all()
    archives_dict = {
        "النماذج": [],
        "التوكيلات": [],
        "السيارات": [],
        "الحوادث": [],
        "بلاغات خارج النطاق": [],
        "اخرى": []
    }
    for item in all_items:
        if item.category in archives_dict:
            archives_dict[item.category].append(item)
    return render_template_string(HTML_TEMPLATE, active_tab='archive', archives=archives_dict)

@app.route('/archive/add', methods=['POST'])
def add_archive():
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    category = request.form.get('category')
    title = request.form.get('title')
    file = request.files.get('file')
    if file and category:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        new_item = ArchiveItem(category=category, title=title, file=filename)
        db.session.add(new_item)
        db.session.commit()
    return redirect(url_for('archive_page'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
@app.route('/archive/delete/<int:id>', methods=['POST'])
def delete_archive(id):
    if 'logged_in' not in session:
        return redirect(url_for('index'))
    item = ArchiveItem.query.get_or_404(id)
    if item.file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], item.file)
        if os.path.exists(file_path):
            os.remove(file_path)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('archive_page'))
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
