import os
import sqlite3
import sys
from datetime import datetime, timedelta
import csv
import bcrypt #type: ignore
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
try:
    from ttkbootstrap import Style #type: ignore
    from ttkbootstrap.constants import * #type: ignore
except Exception:
    tk.Tk().withdraw()
    messagebox.showerror('Missing dependency',
                         'This app requires:\n\n    pip install ttkbootstrap\n\nInstall then re-run.')
    sys.exit(1)

try:
    import bcrypt #type: ignore
except Exception:
    tk.Tk().withdraw()
    messagebox.showerror('Missing dependency',
                         'This app requires:\n\n    pip install bcrypt\n\nInstall then re-run.')
    sys.exit(1)
DB_PATH = 'library.db'
LOAN_DAYS = 14
FINE_PER_DAY = 10  # Rs.10 per day
class DB:
    def __init__(self, path=DB_PATH):
        self.path = path
        self.conn = sqlite3.connect(self.path)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()
    def _create_tables(self):
        cur = self.conn.cursor()
        cur.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash BLOB NOT NULL,
            role TEXT DEFAULT 'admin'
        );
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isbn TEXT UNIQUE,
            title TEXT NOT NULL,
            author TEXT,
            publisher TEXT,
            year INTEGER,
            total_copies INTEGER DEFAULT 1,
            available_copies INTEGER DEFAULT 1,
            added_on TEXT
        );
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            member_since TEXT
        );
        CREATE TABLE IF NOT EXISTS issues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            member_id INTEGER,
            issue_date TEXT,
            due_date TEXT,
            return_date TEXT,
            fine_paid REAL DEFAULT 0,
            paid INTEGER DEFAULT 0,
            FOREIGN KEY(book_id) REFERENCES books(id),
            FOREIGN KEY(member_id) REFERENCES members(id)
        );
        """)
        self.conn.commit()
        # ensure default admin exists
        cur.execute("SELECT COUNT(*) AS c FROM users")
        if cur.fetchone()['c'] == 0:
            # default admin: admin/admin123 (hashed)
            pw = b"admin123"
            hashed = bcrypt.hashpw(pw, bcrypt.gensalt())
            cur.execute("INSERT INTO users (username, password_hash, role) VALUES (?,?,?)",
                        ('admin', hashed, 'admin'))
            self.conn.commit()
    def execute(self, sql, params=()):
        cur = self.conn.cursor()
        cur.execute(sql, params)
        self.conn.commit()
        return cur
    def fetchone(self, sql, params=()):
        cur = self.conn.cursor()
        cur.execute(sql, params)
        return cur.fetchone()
    def fetchall(self, sql, params=()):
        cur = self.conn.cursor()
        cur.execute(sql, params)
        return cur.fetchall()
def today_date():
    return datetime.now().date()

def iso(date_obj):
    return date_obj.isoformat()
class LoginWindow(tk.Toplevel):
    def __init__(self, parent, db: DB, on_success):
        super().__init__(parent)
        self.parent = parent
        self.db = db
        self.on_success = on_success
        self.title("📘 Library Management System — Login")
        self.resizable(False, False)
        # remove geometry while building
        self.withdraw()
        self.configure(padx=12, pady=12)
        # frame with modern look (rounded effect is visual; ttkbootstrap themes handle polish)
        frm = ttk.Frame(self, padding=12)
        frm.pack(fill='both', expand=True)
        logo_frame = ttk.Frame(frm)
        logo_frame.pack(fill='x', pady=(4, 12))
        lbl_logo = ttk.Label(logo_frame, text='📘', font=('Segoe UI Emoji', 28))
        lbl_logo.pack(side='left')
        ttk.Label(logo_frame, text='Library Management System', font=('Segoe UI', 16, 'bold')).pack(side='left', padx=8)

        # animated welcome text (simple sliding text)
        self.welcome_lbl = ttk.Label(frm, text='', font=('Segoe UI', 10, 'italic'))
        self.welcome_lbl.pack(fill='x', pady=(0,8))
        self._welcome_text = "Welcome to Library Management System"
        self._welcome_index = 0
        self.after(300, self._animate_welcome)

        # inputs
        ttk.Label(frm, text='Username').pack(anchor='w')
        self.ent_user = ttk.Entry(frm)
        self.ent_user.pack(fill='x', pady=4)
        ttk.Label(frm, text='Password').pack(anchor='w')
        pw_frm = ttk.Frame(frm)
        pw_frm.pack(fill='x', pady=(0,6))
        self.ent_pass = ttk.Entry(pw_frm, show='*')
        self.ent_pass.pack(side='left', fill='x', expand=True)
        self.show_pw = tk.BooleanVar(value=False)
        chk = ttk.Checkbutton(pw_frm, text='Show', variable=self.show_pw, command=self._toggle_pw, bootstyle='secondary')
        chk.pack(side='left', padx=6)

        btn_frm = ttk.Frame(frm)
        btn_frm.pack(fill='x', pady=6)
        ttk.Button(btn_frm, text='Login', bootstyle='primary', command=self.try_login).pack(side='left', fill='x', expand=True)
        ttk.Button(btn_frm, text='Quit', bootstyle='danger', command=self._quit).pack(side='left', padx=6)

        # place window off-screen (below) and slide in
        self.update_idletasks()
        w = self.winfo_width()
        h = self.winfo_height()
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        x = (screen_w - w) // 2
        start_y = screen_h  # start off-screen bottom
        target_y = (screen_h - h) // 2
        self.geometry(f"+{x}+{start_y}")
        self.deiconify()
        self._slide_in(x, start_y, target_y, step=20)
        self.ent_user.focus_set()

    def _animate_welcome(self):
        # simple slide-in characters
        if self._welcome_index < len(self._welcome_text):
            self._welcome_index += 1
            self.welcome_lbl.config(text=self._welcome_text[:self._welcome_index])
            self.after(40, self._animate_welcome)

    def _slide_in(self, x, y, target_y, step=20):
        if y <= target_y:
            self.geometry(f"+{x}+{target_y}")
            return
        y -= step
        self.geometry(f"+{x}+{y}")
        self.after(12, lambda: self._slide_in(x, y, target_y, step))

    def _toggle_pw(self):
        self.ent_pass.config(show='' if self.show_pw.get() else '*')

    def try_login(self):
        user = self.ent_user.get().strip()
        pw = self.ent_pass.get().encode('utf-8')
        if not user or not pw:
            messagebox.showwarning('Validation', 'Enter username and password')
            return
            
        row = self.db.fetchone("SELECT * FROM users WHERE username=?", (user,))
        
        # 1. Check if user exists
        if not row:
            messagebox.showerror('Login failed', 'Invalid credentials')
            return
            
        stored = row['password_hash']

        # 2. Check if the stored hash is valid (not None, and is bytes)
        if not stored or not isinstance(stored, bytes):
            # This handles case where the stored password hash is missing or corrupted
            messagebox.showerror('Error', 'Authentication data is corrupted. Contact administrator.')
            return

        # 3. Perform the bcrypt check
        try:
            if bcrypt.checkpw(pw, stored):
                # success
                self.destroy()
                self.on_success(user)
            else:
                messagebox.showerror('Login failed', 'Invalid credentials')
        except ValueError:
            # bcrypt.checkpw raises ValueError if the hash format is incorrect
            messagebox.showerror('Error', 'Authentication error: Invalid password hash format.')
        except Exception as e:
            # Catch any other unexpected exceptions and show the actual error for debugging
            messagebox.showerror('Error', f'Unexpected Authentication Error: {e}')

    def _quit(self):
        self.parent.destroy()

# ---------------- Main Application ----------------
class LibraryApp(tk.Tk):
    def __init__(self, db: DB, username:str):
        super().__init__()
        self.db = db
        self.user = username
        # system adaptive style
        try:
            self.style = Style(theme='system')
        except Exception:
            self.style = Style(theme='flatly')
        self.title('📘 Library Management System')
        self.geometry('1100x700')

        # menu bar
        men = tk.Menu(self)
        self.config(menu=men)
        system_menu = tk.Menu(men, tearoff=0)
        system_menu.add_command(label='Change Admin Password', command=self.change_password)
        system_menu.add_separator()
        system_menu.add_command(label='Exit', command=self.quit)
        men.add_cascade(label='Settings', menu=system_menu)

        # Notebook
        self.nb = ttk.Notebook(self)
        self.nb.pack(fill='both', expand=True, padx=12, pady=12)
        # tabs
        self.tab_dashboard = ttk.Frame(self.nb)
        self.tab_books = ttk.Frame(self.nb)
        self.tab_members = ttk.Frame(self.nb)
        self.tab_issue = ttk.Frame(self.nb)
        self.tab_return = ttk.Frame(self.nb)
        self.tab_fines = ttk.Frame(self.nb)

        self.nb.add(self.tab_dashboard, text='Dashboard')
        self.nb.add(self.tab_books, text='Books')
        self.nb.add(self.tab_members, text='Members')
        self.nb.add(self.tab_issue, text='Issue / Renew')
        self.nb.add(self.tab_return, text='Return')
        self.nb.add(self.tab_fines, text='Fines Report')

        # build UI
        self._build_dashboard()
        self._build_books_tab()
        self._build_members_tab()
        self._build_issue_tab()
        self._build_return_tab()
        self._build_fines_tab()

        self._refresh_all()

    # ---------- Dashboard ----------
    def _build_dashboard(self):
        frm = ttk.Frame(self.tab_dashboard, padding=14)
        frm.pack(fill='both', expand=True)
        header = ttk.Frame(frm)
        header.pack(fill='x')
        ttk.Label(header, text='📘 Library Dashboard', font=('Segoe UI', 18, 'bold')).pack(side='left')
        ttk.Label(header, text=f'Logged in as: {self.user}', foreground='gray').pack(side='right')

        stats = ttk.Frame(frm, padding=8)
        stats.pack(fill='x', pady=12)
        self.stat_books = ttk.Label(stats, text='Books: 0', font=('Segoe UI', 12))
        self.stat_members = ttk.Label(stats, text='Members: 0', font=('Segoe UI', 12))
        self.stat_issued = ttk.Label(stats, text='Currently Issued: 0', font=('Segoe UI', 12))
        self.stat_overdue = ttk.Label(stats, text='Overdue: 0', font=('Segoe UI', 12))
        for w in (self.stat_books, self.stat_members, self.stat_issued, self.stat_overdue):
            w.pack(anchor='w', pady=4)

    # ---------- Books ----------
    def _build_books_tab(self):
        top = ttk.Frame(self.tab_books, padding=10)
        top.pack(fill='x')
        form = ttk.Frame(top)
        form.pack(side='left', fill='x', expand=True)

        ttk.Label(form, text='ISBN *').grid(row=0, column=0, sticky='w')
        self.ent_isbn = ttk.Entry(form); self.ent_isbn.grid(row=0, column=1, sticky='ew', padx=6, pady=4)
        ttk.Label(form, text='Title *').grid(row=1, column=0, sticky='w')
        self.ent_title = ttk.Entry(form); self.ent_title.grid(row=1, column=1, sticky='ew', padx=6, pady=4)
        ttk.Label(form, text='Author').grid(row=2, column=0, sticky='w')
        self.ent_author = ttk.Entry(form); self.ent_author.grid(row=2, column=1, sticky='ew', padx=6, pady=4)
        ttk.Label(form, text='Publisher').grid(row=3, column=0, sticky='w')
        self.ent_publisher = ttk.Entry(form); self.ent_publisher.grid(row=3, column=1, sticky='ew', padx=6, pady=4)
        ttk.Label(form, text='Year').grid(row=4, column=0, sticky='w')
        self.ent_year = ttk.Entry(form); self.ent_year.grid(row=4, column=1, sticky='ew', padx=6, pady=4)
        ttk.Label(form, text='Total Copies *').grid(row=5, column=0, sticky='w')
        self.ent_total = ttk.Entry(form); self.ent_total.grid(row=5, column=1, sticky='ew', padx=6, pady=4)
        form.columnconfigure(1, weight=1)

        btns = ttk.Frame(top)
        btns.pack(side='right')
        ttk.Button(btns, text='Add / Update Book', bootstyle='success', command=self.add_update_book).pack(fill='x', pady=4)
        ttk.Button(btns, text='Import CSV', bootstyle='info', command=self.import_books_csv).pack(fill='x', pady=4)
        ttk.Button(btns, text='Clear Fields', command=self._clear_book_form).pack(fill='x', pady=4)

        mid = ttk.Frame(self.tab_books, padding=10)
        mid.pack(fill='both', expand=True)
        search_frm = ttk.Frame(mid); search_frm.pack(fill='x')
        ttk.Label(search_frm, text='Search:').pack(side='left')
        self.book_search_var = tk.StringVar()
        ent = ttk.Entry(search_frm, textvariable=self.book_search_var); ent.pack(side='left', fill='x', expand=True, padx=6)
        ent.bind('<Return>', lambda e: self._refresh_books())
        ttk.Button(search_frm, text='Go', bootstyle='primary', command=self._refresh_books).pack(side='left', padx=6)

        cols = ('id','isbn','title','author','year','total','available')
        self.tree_books = ttk.Treeview(mid, columns=cols, show='headings', height=12)
        for c,h in zip(cols, ('ID','ISBN','Title','Author','Year','Total','Available')):
            self.tree_books.heading(c, text=h); self.tree_books.column(c, anchor='w')
        self.tree_books.pack(fill='both', expand=True, pady=8)
        self.tree_books.bind('<<TreeviewSelect>>', self._on_book_select)

    def _clear_book_form(self):
        for e in (self.ent_isbn, self.ent_title, self.ent_author, self.ent_publisher, self.ent_year, self.ent_total):
            e.delete(0, 'end')

    def add_update_book(self):
        isbn = self.ent_isbn.get().strip()
        title = self.ent_title.get().strip()
        author = self.ent_author.get().strip()
        publisher = self.ent_publisher.get().strip()
        year = self.ent_year.get().strip()
        total = self.ent_total.get().strip()
        if not isbn or not title or not total:
            messagebox.showwarning('Validation', 'ISBN, Title and Total Copies are required.')
            return
        try:
            total_i = int(total); assert total_i>0
        except Exception:
            messagebox.showwarning('Validation', 'Total Copies must be a positive integer.')
            return
        try:
            year_i = int(year) if year else None
        except Exception:
            messagebox.showwarning('Validation', 'Year must be numeric.')
            return
        existing = self.db.fetchone('SELECT * FROM books WHERE isbn=?', (isbn,))
        if existing:
            old_total = existing['total_copies']
            old_avail = existing['available_copies']
            diff = total_i - old_total
            new_avail = max(0, old_avail + diff)
            self.db.execute('UPDATE books SET title=?,author=?,publisher=?,year=?,total_copies=?,available_copies=? WHERE isbn=?',
                            (title,author,publisher,year_i,total_i,new_avail,isbn))
            messagebox.showinfo('Updated', 'Book updated successfully.')
        else:
            added_on = datetime.now().isoformat()
            try:
                self.db.execute('INSERT INTO books (isbn,title,author,publisher,year,total_copies,available_copies,added_on) VALUES (?,?,?,?,?,?,?,?)',
                                (isbn,title,author,publisher, year_i, total_i, total_i, added_on))
                messagebox.showinfo('Added', 'Book added successfully.')
            except sqlite3.IntegrityError:
                messagebox.showerror('Error', 'ISBN must be unique.')
        self._clear_book_form()
        self._refresh_books()

    def _on_book_select(self, e):
        sel = self.tree_books.selection()
        if not sel: return
        vals = self.tree_books.item(sel[0])['values']
        bid = vals[0]
        r = self.db.fetchone('SELECT * FROM books WHERE id=?', (bid,))
        if r:
            self.ent_isbn.delete(0,'end'); self.ent_isbn.insert(0, r['isbn'] or '')
            self.ent_title.delete(0,'end'); self.ent_title.insert(0, r['title'] or '')
            self.ent_author.delete(0,'end'); self.ent_author.insert(0, r['author'] or '')
            self.ent_publisher.delete(0,'end'); self.ent_publisher.insert(0, r['publisher'] or '')
            self.ent_year.delete(0,'end'); self.ent_year.insert(0, r['year'] or '')
            self.ent_total.delete(0,'end'); self.ent_total.insert(0, r['total_copies'] or '')

    def _refresh_books(self):
        q = self.book_search_var.get().strip()
        if q:
            rows = self.db.fetchall("SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ? ORDER BY title",
                                    (f'%{q}%', f'%{q}%', f'%{q}%'))
        else:
            rows = self.db.fetchall("SELECT * FROM books ORDER BY title")
        for i in self.tree_books.get_children(): self.tree_books.delete(i)
        for r in rows:
            self.tree_books.insert('', 'end', values=(r['id'], r['isbn'], r['title'], r['author'], r['year'], r['total_copies'], r['available_copies']))

    def import_books_csv(self):
        path = filedialog.askopenfilename(filetypes=[('CSV','*.csv')])
        if not path: return
        count = 0
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                isbn = row.get('isbn','').strip()
                title = row.get('title','').strip() or 'Untitled'
                author = row.get('author','').strip()
                year = row.get('year')
                total = row.get('total_copies') or row.get('quantity') or '1'
                try: total_i = int(total)
                except: total_i = 1
                try:
                    self.db.execute('INSERT INTO books (isbn,title,author,year,total_copies,available_copies,added_on) VALUES (?,?,?,?,?,?,?)',
                                    (isbn, title, author, int(year) if year else None, total_i, total_i, datetime.now().isoformat()))
                    count += 1
                except Exception:
                    continue
        messagebox.showinfo('Import', f'Imported {count} records.')
        self._refresh_books()

    # ---------- Members ----------
    def _build_members_tab(self):
        left = ttk.Frame(self.tab_members, padding=10)
        left.pack(side='left', fill='y')
        ttk.Label(left, text='Name *').grid(row=0, column=0, sticky='w')
        self.ent_m_name = ttk.Entry(left); self.ent_m_name.grid(row=0, column=1, pady=4, padx=6)
        ttk.Label(left, text='Email').grid(row=1, column=0, sticky='w')
        self.ent_m_email = ttk.Entry(left); self.ent_m_email.grid(row=1, column=1, pady=4, padx=6)
        ttk.Label(left, text='Phone').grid(row=2, column=0, sticky='w')
        self.ent_m_phone = ttk.Entry(left); self.ent_m_phone.grid(row=2, column=1, pady=4, padx=6)
        ttk.Button(left, text='Add Member', bootstyle='success', command=self.add_member).grid(row=3, column=0, columnspan=2, pady=8, sticky='ew')
        ttk.Button(left, text='Clear', command=self._clear_member_form).grid(row=4, column=0, columnspan=2, pady=4, sticky='ew')

        right = ttk.Frame(self.tab_members, padding=10)
        right.pack(side='left', fill='both', expand=True)
        ttk.Label(right, text='Search:').pack(anchor='nw')
        self.member_search_var = tk.StringVar()
        ent = ttk.Entry(right, textvariable=self.member_search_var); ent.pack(fill='x', padx=6, pady=2)
        ent.bind('<Return>', lambda e: self._refresh_members())
        ttk.Button(right, text='Search', bootstyle='primary', command=self._refresh_members).pack(anchor='ne', padx=6)

        cols = ('id','name','email','phone','since')
        self.tree_members = ttk.Treeview(right, columns=cols, show='headings', height=12)
        for c,h in zip(cols, ('ID','Name','Email','Phone','Since')):
            self.tree_members.heading(c, text=h); self.tree_members.column(c, anchor='w')
        self.tree_members.pack(fill='both', expand=True, pady=8)
        self.tree_members.bind('<<TreeviewSelect>>', self._on_member_select)

    def _clear_member_form(self):
        for e in (self.ent_m_name, self.ent_m_email, self.ent_m_phone): e.delete(0,'end')

    def add_member(self):
        name = self.ent_m_name.get().strip()
        email = self.ent_m_email.get().strip()
        phone = self.ent_m_phone.get().strip()
        if not name:
            messagebox.showwarning('Validation', 'Member name required')
            return
        self.db.execute('INSERT INTO members (name,email,phone,member_since) VALUES (?,?,?,?)',
                        (name,email,phone, datetime.now().date().isoformat()))
        messagebox.showinfo('Added', 'Member added successfully')
        self._clear_member_form()
        self._refresh_members()

    def _on_member_select(self, e):
        sel = self.tree_members.selection()
        if not sel: return
        vals = self.tree_members.item(sel[0])['values']
        mid = vals[0]
        r = self.db.fetchone('SELECT * FROM members WHERE id=?', (mid,))
        if r:
            self.ent_m_name.delete(0,'end'); self.ent_m_name.insert(0, r['name'] or '')
            self.ent_m_email.delete(0,'end'); self.ent_m_email.insert(0, r['email'] or '')
            self.ent_m_phone.delete(0,'end'); self.ent_m_phone.insert(0, r['phone'] or '')

    def _refresh_members(self):
        q = self.member_search_var.get().strip()
        if q:
            rows = self.db.fetchall('SELECT * FROM members WHERE name LIKE ? OR email LIKE ? ORDER BY name', (f'%{q}%', f'%{q}%'))
        else:
            rows = self.db.fetchall('SELECT * FROM members ORDER BY name')
        for i in self.tree_members.get_children(): self.tree_members.delete(i)
        for r in rows:
            self.tree_members.insert('', 'end', values=(r['id'], r['name'], r['email'], r['phone'], r['member_since']))

    # ---------- Issue ----------
    def _build_issue_tab(self):
        frm = ttk.Frame(self.tab_issue, padding=12); frm.pack(fill='x')
        ttk.Label(frm, text='Book ISBN or ID').grid(row=0, column=0, sticky='w')
        self.q_book = ttk.Entry(frm); self.q_book.grid(row=0, column=1, sticky='ew', padx=6, pady=4)
        ttk.Label(frm, text='Member ID or Name').grid(row=1, column=0, sticky='w')
        self.q_member = ttk.Entry(frm); self.q_member.grid(row=1, column=1, sticky='ew', padx=6, pady=4)
        ttk.Button(frm, text='Find & Issue', bootstyle='success', command=self.issue_book).grid(row=2, column=0, columnspan=2, pady=8)
        frm.columnconfigure(1, weight=1)

        cols = ('id','book','member','issue','due','returned')
        self.tree_issues = ttk.Treeview(self.tab_issue, columns=cols, show='headings')
        for c,h in zip(cols, ('ID','Book','Member','Issued','Due','Returned')):
            self.tree_issues.heading(c, text=h); self.tree_issues.column(c, anchor='w')
        self.tree_issues.pack(fill='both', expand=True, padx=12, pady=8)

    def issue_book(self):
        qbook = self.q_book.get().strip(); qmem = self.q_member.get().strip()
        if not qbook or not qmem:
            messagebox.showwarning('Validation', 'Enter both book and member fields')
            return
        book = None
        if qbook.isdigit():
            book = self.db.fetchone('SELECT * FROM books WHERE id=?', (int(qbook),))
        if not book:
            book = self.db.fetchone('SELECT * FROM books WHERE isbn=? OR title LIKE ? LIMIT 1', (qbook, f'%{qbook}%'))
        if not book:
            messagebox.showerror('Not found', 'Book not found')
            return
        if book['available_copies'] <= 0:
            messagebox.showinfo('Unavailable', 'No available copies')
            return
        member = None
        if qmem.isdigit():
            member = self.db.fetchone('SELECT * FROM members WHERE id=?', (int(qmem),))
        if not member:
            member = self.db.fetchone('SELECT * FROM members WHERE name LIKE ? OR email=? LIMIT 1', (f'%{qmem}%', qmem))
        if not member:
            messagebox.showerror('Not found', 'Member not found')
            return
        issue_date = today_date()
        due = issue_date + timedelta(days=LOAN_DAYS)
        self.db.execute('INSERT INTO issues (book_id,member_id,issue_date,due_date) VALUES (?,?,?,?)',
                        (book['id'], member['id'], issue_date.isoformat(), due.isoformat()))
        self.db.execute('UPDATE books SET available_copies = available_copies - 1 WHERE id=?', (book['id'],))
        messagebox.showinfo('Issued', f'Book issued. Due date: {due.isoformat()}')
        self.q_book.delete(0,'end'); self.q_member.delete(0,'end')
        self._refresh_issues(); self._refresh_books(); self._refresh_fines()

    def _refresh_issues(self):
        rows = self.db.fetchall('''
            SELECT i.*, b.title book_title, m.name member_name FROM issues i
            LEFT JOIN books b ON b.id=i.book_id
            LEFT JOIN members m ON m.id=i.member_id
            ORDER BY i.issue_date DESC
        ''')
        for i in self.tree_issues.get_children(): self.tree_issues.delete(i)
        for r in rows:
            self.tree_issues.insert('', 'end', values=(r['id'], r['book_title'], r['member_name'], r['issue_date'], r['due_date'], r['return_date'] or ''))

    # ---------- Return ----------
    def _build_return_tab(self):
        frm = ttk.Frame(self.tab_return, padding=12); frm.pack(fill='x')
        ttk.Label(frm, text='Issue ID').grid(row=0, column=0, sticky='w')
        self.return_id = ttk.Entry(frm); self.return_id.grid(row=0, column=1, sticky='ew', padx=6, pady=4)
        ttk.Button(frm, text='Return & Calculate Fine', bootstyle='danger', command=self.return_book).grid(row=1, column=0, columnspan=2, pady=8)
        frm.columnconfigure(1, weight=1)
        self.txt_returns = tk.Text(self.tab_return, height=12)
        self.txt_returns.pack(fill='both', expand=True, padx=12, pady=8)

    def return_book(self):
        iid = self.return_id.get().strip()
        if not iid.isdigit():
            messagebox.showwarning('Validation', 'Enter numeric Issue ID')
            return
        rec = self.db.fetchone('SELECT * FROM issues WHERE id=?', (int(iid),))
        if not rec:
            messagebox.showerror('Not found', 'Issue record not found')
            return
        if rec['return_date']:
            messagebox.showinfo('Already returned', 'This book is already returned.')
            return
        due = datetime.fromisoformat(rec['due_date']).date()
        ret = today_date()
        overdue_days = (ret - due).days
        fine = (overdue_days * FINE_PER_DAY) if overdue_days>0 else 0
        # update issue
        self.db.execute('UPDATE issues SET return_date=?, fine_paid=?, paid=? WHERE id=?', (ret.isoformat(), fine, 0 if fine>0 else 1, int(iid)))
        # increment available
        self.db.execute('UPDATE books SET available_copies = available_copies + 1 WHERE id=?', (rec['book_id'],))
        if fine>0:
            messagebox.showwarning('Returned with Fine', f'Book returned late. Fine: Rs.{fine}\nPlease collect payment and mark as Paid in Fines Report.')
        else:
            messagebox.showinfo('Returned', 'Book returned on time. No fine.')
        self.return_id.delete(0,'end')
        self._refresh_issues(); self._refresh_books(); self._refresh_fines()
        self.txt_returns.insert('end', f'Issue {iid} returned on {ret.isoformat()} | Fine: Rs.{fine}\n'); self.txt_returns.see('end')

    # ---------- Fines ----------
    def _build_fines_tab(self):
        top = ttk.Frame(self.tab_fines, padding=12); top.pack(fill='x')
        ttk.Button(top, text='Refresh', bootstyle='primary', command=self._refresh_fines).pack(side='left')
        ttk.Button(top, text='Export CSV', bootstyle='info', command=self._export_fines).pack(side='left', padx=6)
        cols = ('id','book','member','due','returned','fine','paid')
        self.tree_fines = ttk.Treeview(self.tab_fines, columns=cols, show='headings')
        for c,h in zip(cols, ('IssueID','Book','Member','Due Date','Return Date','Fine (Rs)','Paid')):
            self.tree_fines.heading(c, text=h); self.tree_fines.column(c, anchor='w')
        self.tree_fines.pack(fill='both', expand=True, padx=12, pady=8)
        pay_frm = ttk.Frame(self.tab_fines, padding=8); pay_frm.pack(fill='x')
        ttk.Button(pay_frm, text='Mark as Paid', bootstyle='success', command=self._mark_paid).pack(side='left', padx=6)
        ttk.Button(pay_frm, text='Show Pending Only', bootstyle='secondary', command=lambda: self._refresh_fines(pending_only=True)).pack(side='left', padx=6)
        self.fines_summary = ttk.Label(self.tab_fines, text=''); self.fines_summary.pack(anchor='se', padx=12, pady=6)

    def _refresh_fines(self, pending_only=False):
        rows = self.db.fetchall('''
            SELECT i.*, b.title book_title, m.name member_name FROM issues i
            LEFT JOIN books b ON b.id=i.book_id
            LEFT JOIN members m ON m.id=i.member_id
            ORDER BY i.due_date DESC
        ''')
        for i in self.tree_fines.get_children(): self.tree_fines.delete(i)
        total_pending = 0; total_collected = 0
        for r in rows:
            fine_amt = r['fine_paid'] or 0
            if not r['return_date']:
                due = datetime.fromisoformat(r['due_date']).date()
                days = (today_date() - due).days
                if days>0:
                    fine_amt = days * FINE_PER_DAY
            paid = 'Yes' if r['paid'] else 'No'
            if r['paid']:
                total_collected += fine_amt
            else:
                total_pending += fine_amt
            if pending_only and r['paid']:
                continue
            self.tree_fines.insert('', 'end', values=(r['id'], r['book_title'], r['member_name'], r['due_date'], r['return_date'] or '', fine_amt, paid))
        self.fines_summary.config(text=f'Total pending: Rs.{total_pending}   |   Total collected: Rs.{total_collected}')

    def _mark_paid(self):
        sel = self.tree_fines.selection()
        if not sel:
            messagebox.showinfo('Select', 'Select an issue to mark paid')
            return
        vals = self.tree_fines.item(sel[0])['values']
        iid = vals[0]
        self.db.execute('UPDATE issues SET paid=1 WHERE id=?', (iid,))
        messagebox.showinfo('Updated', 'Marked as paid')
        self._refresh_fines()

    def _export_fines(self):
        path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV','*.csv')])
        if not path: return
        rows = self.db.fetchall('''
            SELECT i.*, b.title book_title, m.name member_name FROM issues i
            LEFT JOIN books b ON b.id=i.book_id
            LEFT JOIN members m ON m.id=i.member_id
            ORDER BY i.due_date DESC
        ''')
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['IssueID','Book','Member','IssueDate','DueDate','ReturnDate','Fine','Paid'])
            for r in rows:
                fine_amt = r['fine_paid'] or 0
                if not r['return_date']:
                    due = datetime.fromisoformat(r['due_date']).date()
                    days = (today_date() - due).days
                    if days>0:
                        fine_amt = days * FINE_PER_DAY
                writer.writerow([r['id'], r['book_title'], r['member_name'], r['issue_date'], r['due_date'], r['return_date'] or '', fine_amt, 'Yes' if r['paid'] else 'No'])
        messagebox.showinfo('Exported', 'Fines exported to CSV')     
        messagebox.showinfo('Updated', 'Marked as paid successfully.')
        self._refresh_fines()

    # ---------- Password change ----------
    def change_password(self):
        old = simpledialog.askstring('Old Password', 'Enter current admin password:', show='*')
        if not old:
            return
        user = self.db.fetchone('SELECT * FROM users WHERE username=?', (self.user,))
        if not user:
            messagebox.showerror('Error', 'User not found.')
            return
        if not bcrypt.checkpw(old.encode('utf-8'), user['password_hash']):
            messagebox.showerror('Error', 'Incorrect old password.')
            return
        new = simpledialog.askstring('New Password', 'Enter new password:', show='*')
        if not new:
            return
        hashed = bcrypt.hashpw(new.encode('utf-8'), bcrypt.gensalt())
        self.db.execute('UPDATE users SET password_hash=? WHERE username=?', (hashed, self.user))
        messagebox.showinfo('Done', 'Password changed successfully.')

    # ---------- Refresh all ----------
    def _refresh_all(self):
        self._refresh_books()
        self._refresh_members()
        self._refresh_issues()
        self._refresh_fines()
        self._update_dashboard_stats()

    def _update_dashboard_stats(self):
        total_books = self.db.fetchone('SELECT COUNT(*) AS c FROM books')['c']
        total_members = self.db.fetchone('SELECT COUNT(*) AS c FROM members')['c']
        issued = self.db.fetchone('SELECT COUNT(*) AS c FROM issues WHERE return_date IS NULL')['c']
        overdue = self.db.fetchone('SELECT COUNT(*) AS c FROM issues WHERE return_date IS NULL AND due_date < ?', (today_date().isoformat(),))['c']
        self.stat_books.config(text=f'Books: {total_books}')
        self.stat_members.config(text=f'Members: {total_members}')
        self.stat_issued.config(text=f'Currently Issued: {issued}')
        self.stat_overdue.config(text=f'Overdue: {overdue}')


# ---------- Launcher ----------
def main():
    root = tk.Tk()
    root.withdraw()  # hide main root until login succeeds
    db = DB()

    def on_success(username):
        app = LibraryApp(db, username)
        app.mainloop()

    LoginWindow(root, db, on_success)
    root.mainloop()


if __name__ == '__main__':
    main()

