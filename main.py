import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from PIL import Image
import mysql.connector
from mysql.connector import Error
import os
import json
import base64
import hashlib
import hmac
import secrets
import shutil
import re

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Acceso local inicial solicitado: dorian / 123. La contraseña se guarda con hash.
DEFAULT_USER = "dorian"
DEFAULT_PASSWORD = "123"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOCAL_SETTINGS_FILE = os.path.join(BASE_DIR, "app_settings.json")
PROFILE_DIR = os.path.join(BASE_DIR, "profile_photos")
os.makedirs(PROFILE_DIR, exist_ok=True)


def hash_password(password):
    """Hash de contraseña compatible con el tamaño de usuario.contrasena (VARCHAR(100))."""
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 260000, dklen=32)
    return "pbkdf2_sha256${}${}${}".format(
        260000,
        base64.urlsafe_b64encode(salt).decode("ascii").rstrip("="),
        base64.urlsafe_b64encode(digest).decode("ascii").rstrip("="),
    )


def verify_password(password, stored_value):
    if not stored_value:
        return False
    if not str(stored_value).startswith("pbkdf2_sha256$"):
        # Compatibilidad temporal con contraseñas antiguas en texto plano del SQL existente.
        return hmac.compare_digest(str(password), str(stored_value))
    try:
        _algorithm, iterations, salt_text, digest_text = str(stored_value).split("$", 3)
        salt = base64.urlsafe_b64decode(salt_text + "=" * (-len(salt_text) % 4))
        expected = base64.urlsafe_b64decode(digest_text + "=" * (-len(digest_text) % 4))
        actual = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, int(iterations), dklen=len(expected))
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError):
        return False


def load_local_settings():
    defaults = {"admin_display_name": "Dorian", "admin_password_hash": hash_password(DEFAULT_PASSWORD), "admin_photo": ""}
    try:
        if os.path.exists(LOCAL_SETTINGS_FILE):
            with open(LOCAL_SETTINGS_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
            if not isinstance(data, dict):
                data = {}
            for key, value in defaults.items():
                if key not in data:
                    data[key] = value
            if not str(data.get("admin_password_hash", "")).startswith("pbkdf2_sha256$"):
                old_password = str(data.get("admin_password_hash") or DEFAULT_PASSWORD)
                data["admin_password_hash"] = hash_password(old_password)
            save_local_settings(data)
            return data
    except (OSError, json.JSONDecodeError):
        pass
    save_local_settings(defaults)
    return defaults


def save_local_settings(data):
    temp_path = LOCAL_SETTINGS_FILE + ".tmp"
    with open(temp_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
    os.replace(temp_path, LOCAL_SETTINGS_FILE)


# Configuración de XAMPP. Si tu usuario MySQL tiene contraseña, escríbela aquí.
DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "",
    "database": "drogueria_donmarcos",
    "charset": "utf8mb4",
}

BG = "#FCEBEC"
WHITE = "#FFFFFF"
NAVY = "#171717"
GREEN = "#C62828"
GREEN_DARK = "#A61F24"
GREEN_PALE = "#FDE3E4"
TEXT = "#202020"
MUTED = "#666666"
BORDER = "#E8C5C7"
RED = "#B91C1C"
AMBER = "#B7791F"

MODULES = {
    "Panel principal": ("⌂", "Resumen general"),
    "Productos": ("▣", "Catálogo y productos"),
    "Categorías": ("▦", "Clasificación de productos"),
    "Inventario": ("▤", "Existencias actuales"),
    "Movimientos": ("⇄", "Entradas, salidas y ajustes"),
    "Compras": ("＋", "Compras a proveedores"),
    "Ventas": ("＄", "Registro de ventas"),
    "Clientes": ("♙", "Directorio de clientes"),
    "Proveedores": ("▧", "Directorio de proveedores"),
    "Usuarios": ("♧", "Usuarios y roles"),
    "Solicitudes de registro": ("✉", "Aprobación de nuevas cuentas"),
    "Citas ópticas": ("◷", "Agenda de citas"),
    "Pedidos": ("☷", "Solicitudes de clientes"),
    "Reportes": ("▥", "Informes de gestión"),
    "Configuración": ("⚙", "Preferencias del sistema"),
}

TABLE_CONFIG = {
    "Productos": {
        "columns": [("Código", 100), ("Nombre del producto", 230), ("Categoría", 160), ("Precio venta", 120), ("Stock", 90), ("Estado", 100)],
        "rows": [
            ("PR-001", "Acetaminofén 500 mg", "Medicamentos", "$ 4.500", "120", "Activo"),
            ("PR-002", "Vitamina C", "Vitaminas", "$ 18.000", "34", "Activo"),
            ("PR-003", "Gafas de lectura", "Óptica", "$ 35.000", "8", "Stock bajo"),
            ("PR-004", "Alcohol antiséptico", "Primeros auxilios", "$ 7.000", "0", "Agotado"),
        ],
        "fields": ["Código", "Nombre del producto", "Categoría", "Precio de compra", "Precio de venta", "Stock actual", "Stock mínimo", "Lote", "Fecha de vencimiento"]
    },
    "Categorías": {
        "columns": [("Código", 110), ("Nombre", 220), ("Descripción", 350), ("Estado", 110)],
        "rows": [
            ("CAT-01", "Medicamentos", "Productos farmacéuticos", "Activa"),
            ("CAT-02", "Vitaminas", "Vitaminas y suplementos", "Activa"),
            ("CAT-03", "Cuidado personal", "Higiene y cuidado personal", "Activa"),
            ("CAT-04", "Óptica", "Productos y servicios ópticos", "Activa"),
            ("CAT-05", "Primeros auxilios", "Elementos básicos de primeros auxilios", "Activa"),
        ],
        "fields": ["Código", "Nombre", "Descripción", "Estado"]
    },
    "Inventario": {
        "columns": [("Código", 100), ("Producto", 240), ("Categoría", 160), ("Stock", 100), ("Mínimo", 100), ("Vencimiento", 130), ("Estado", 120)],
        "rows": [
            ("PR-001", "Acetaminofén 500 mg", "Medicamentos", "120", "20", "2027-08-15", "Disponible"),
            ("PR-002", "Vitamina C", "Vitaminas", "34", "10", "2027-03-12", "Disponible"),
            ("PR-003", "Gafas de lectura", "Óptica", "8", "10", "—", "Stock bajo"),
            ("PR-004", "Alcohol antiséptico", "Primeros auxilios", "0", "12", "2027-01-20", "Agotado"),
        ],
        "fields": ["Código", "Producto", "Categoría", "Stock actual", "Stock mínimo", "Lote", "Fecha de vencimiento"]
    },
    "Movimientos": {
        "columns": [("Código", 100), ("Fecha", 150), ("Producto", 220), ("Tipo", 130), ("Cantidad", 100), ("Responsable", 170), ("Motivo", 220)],
        "rows": [
            ("MOV-001", "2026-10-13", "Acetaminofén 500 mg", "Entrada", "50", "Dorian", "Compra"),
            ("MOV-002", "2026-10-13", "Vitamina C", "Salida", "3", "Empleado demo", "Venta"),
        ],
        "fields": ["Código", "Fecha", "Producto", "Tipo de movimiento", "Cantidad", "Responsable", "Motivo"]
    },
    "Compras": {
        "columns": [("Código", 110), ("Fecha", 130), ("Proveedor", 230), ("Responsable", 170), ("Total", 130), ("Estado", 110)],
        "rows": [
            ("COM-001", "2026-10-12", "Distribuciones Salud", "Dorian", "$ 250.000", "Registrada"),
            ("COM-002", "2026-10-10", "Óptica Central", "Dorian", "$ 180.000", "Registrada"),
        ],
        "fields": ["Código", "Proveedor", "Fecha", "Responsable", "Subtotal", "Total", "Estado"]
    },
    "Ventas": {
        "columns": [("Código", 110), ("Fecha", 130), ("Cliente", 210), ("Empleado", 170), ("Total", 130), ("Estado", 110)],
        "rows": [
            ("VEN-001", "2026-10-13", "Cliente ocasional", "Dorian", "$ 24.000", "Completada"),
            ("VEN-002", "2026-10-12", "María Pérez", "Empleado demo", "$ 48.500", "Completada"),
        ],
        "fields": ["Código", "Cliente", "Empleado", "Fecha", "Subtotal", "Total", "Estado"]
    },
    "Clientes": {
        "columns": [("Código", 110), ("Nombre completo", 230), ("Teléfono", 150), ("Correo", 250), ("Estado", 100)],
        "rows": [
            ("CLI-001", "María Pérez", "300 000 0000", "maria@example.com", "Activo"),
            ("CLI-002", "Carlos Ramírez", "301 000 0000", "carlos@example.com", "Activo"),
        ],
        "fields": ["Código", "Nombre completo", "Documento", "Teléfono", "Correo", "Dirección", "Estado"]
    },
    "Proveedores": {
        "columns": [("Código", 110), ("Razón social", 240), ("Contacto", 170), ("Teléfono", 150), ("Correo", 250)],
        "rows": [
            ("PRO-001", "Distribuciones Salud", "Laura Gómez", "607 000 0000", "ventas@example.com"),
            ("PRO-002", "Óptica Central", "Andrés Ruiz", "607 111 1111", "contacto@example.com"),
        ],
        "fields": ["Código", "Razón social", "Persona de contacto", "Documento", "Teléfono", "Correo", "Dirección", "Estado"]
    },
    "Usuarios": {
        "columns": [("Código", 110), ("Nombre", 210), ("Usuario", 150), ("Rol", 170), ("Estado", 100)],
        "rows": [
            ("USR-001", "Dorian", "dorian", "Administrador", "Activo"),
            ("USR-002", "Empleado demo", "empleado", "Empleado", "Activo"),
            ("USR-003", "Responsable óptico", "optica", "Responsable de citas", "Activo"),
        ],
        "fields": ["Código", "Nombre completo", "Correo", "Nombre de usuario", "Rol", "Estado"]
    },
    "Citas ópticas": {
        "columns": [("Código", 100), ("Cliente", 200), ("Fecha", 130), ("Hora", 100), ("Servicio", 220), ("Responsable", 170), ("Estado", 130)],
        "rows": [
            ("CIT-001", "María Pérez", "2026-10-14", "09:00", "Valoración óptica", "Responsable óptico", "Confirmada"),
            ("CIT-002", "Carlos Ramírez", "2026-10-14", "11:30", "Solicitud de lentes", "Responsable óptico", "Pendiente"),
        ],
        "fields": ["Código", "Cliente", "Fecha", "Hora", "Servicio", "Responsable", "Observaciones", "Estado"]
    },
    "Pedidos": {
        "columns": [("Código", 110), ("Cliente", 220), ("Fecha", 130), ("Productos", 250), ("Total estimado", 150), ("Estado", 140)],
        "rows": [
            ("PED-001", "María Pérez", "2026-10-13", "Vitamina C × 2", "$ 36.000", "Pendiente"),
            ("PED-002", "Carlos Ramírez", "2026-10-12", "Gafas de lectura × 1", "$ 35.000", "En preparación"),
        ],
        "fields": ["Código", "Cliente", "Fecha", "Productos solicitados", "Total estimado", "Estado"]
    },
}

class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, on_login, on_register):
        super().__init__(master, fg_color=BG, corner_radius=0)
        self.on_login = on_login
        self.on_register = on_register
        self.pack(fill="both", expand=True)
        shell = ctk.CTkFrame(self, fg_color=WHITE, corner_radius=24, border_width=1, border_color=BORDER)
        shell.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.82, relheight=0.78)
        left = ctk.CTkFrame(shell, fg_color=NAVY, corner_radius=20)
        left.place(relx=0, rely=0, relwidth=0.46, relheight=1)
        ctk.CTkLabel(left, text="✚", font=ctk.CTkFont(size=54, weight="bold"), text_color="#FFCACA").pack(anchor="w", padx=42, pady=(48, 14))
        ctk.CTkLabel(left, text="Droguería\nDon Marcos", font=ctk.CTkFont(size=31, weight="bold"), text_color=WHITE, justify="left").pack(anchor="w", padx=42)
        ctk.CTkLabel(left, text="Gestión inteligente para\ncuidar lo que importa.", font=ctk.CTkFont(size=15), text_color="#F3DCDC", justify="left").pack(anchor="w", padx=42, pady=(16, 0))
        ctk.CTkLabel(left, text="INVENTARIO  •  VENTAS  •  CITAS", text_color="#E8C5C7", font=ctk.CTkFont(size=11, weight="bold")).pack(anchor="w", padx=42, pady=(50, 0))

        right = ctk.CTkFrame(shell, fg_color=WHITE, corner_radius=0)
        right.place(relx=0.46, rely=0, relwidth=0.54, relheight=1)
        ctk.CTkLabel(right, text="Bienvenido", font=ctk.CTkFont(size=28, weight="bold"), text_color=TEXT).pack(anchor="w", padx=38, pady=(45, 5))
        ctk.CTkLabel(right, text="Ingresa con tu usuario o ID y contraseña", font=ctk.CTkFont(size=13), text_color=MUTED).pack(anchor="w", padx=38, pady=(0, 24))
        ctk.CTkLabel(right, text="Usuario o ID de usuario", font=ctk.CTkFont(size=12, weight="bold"), text_color=TEXT).pack(anchor="w", padx=38, pady=(0, 7))
        self.user = ctk.CTkEntry(right, height=44, placeholder_text="Ej. dorian o 3002", corner_radius=12)
        self.user.pack(fill="x", padx=38)
        ctk.CTkLabel(right, text="Contraseña", font=ctk.CTkFont(size=12, weight="bold"), text_color=TEXT).pack(anchor="w", padx=38, pady=(17, 7))
        self.password = ctk.CTkEntry(right, height=44, placeholder_text="Escribe tu contraseña", show="•", corner_radius=12)
        self.password.pack(fill="x", padx=38)
        self.show_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(right, text="Mostrar contraseña", variable=self.show_var, command=self.toggle_password, font=ctk.CTkFont(size=12), fg_color=GREEN, hover_color=GREEN_DARK).pack(anchor="w", padx=38, pady=(10, 0))
        ctk.CTkButton(right, text="Iniciar sesión  →", height=46, corner_radius=12, fg_color=GREEN, hover_color=GREEN_DARK, font=ctk.CTkFont(size=14, weight="bold"), command=self.login).pack(fill="x", padx=38, pady=(22, 10))
        ctk.CTkButton(right, text="Registrar cuenta de empleado", height=38, corner_radius=12, fg_color=WHITE, text_color=GREEN, border_width=1, border_color=GREEN, hover_color=GREEN_PALE, command=self.on_register).pack(fill="x", padx=38)
        self.error = ctk.CTkLabel(right, text="", text_color=RED, font=ctk.CTkFont(size=12), wraplength=350, justify="left")
        self.error.pack(anchor="w", padx=38, pady=(12, 0))
        self.user.bind("<Return>", lambda e: self.password.focus_set())
        self.password.bind("<Return>", lambda e: self.login())

    def toggle_password(self):
        self.password.configure(show="" if self.show_var.get() else "•")

    def login(self):
        username = self.user.get().strip()
        password = self.password.get()
        if not username or not password:
            self.error.configure(text="Escribe el usuario o ID y la contraseña.")
            return
        self.error.configure(text="Verificando acceso...")
        self.update_idletasks()
        self.on_login(username, password)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Droguería Don Marcos | Sistema de gestión")
        self.geometry("1440x900")
        self.minsize(1100, 700)
        self.configure(fg_color=BG)
        self.local_settings = load_local_settings()
        self.current_user = DEFAULT_USER
        self.current_display_name = self.local_settings.get("admin_display_name", "Dorian")
        self.current_role = "Administrador"
        self.current_user_id = None
        self.is_local_admin = True
        self.profile_photo_path = self.local_settings.get("admin_photo", "")
        self.db_conn = None
        self.active_module = "Panel principal"
        self.main_container = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        self.main_container.pack(fill="both", expand=True)
        self.show_login()

    def show_login(self):
        for child in self.main_container.winfo_children():
            child.destroy()
        LoginFrame(self.main_container, self.authenticate_login, self.register_employee)

    def authenticate_login(self, username, password):
        username_clean = username.strip()
        if username_clean.casefold() == DEFAULT_USER:
            self.local_settings = load_local_settings()
            if not verify_password(password, self.local_settings.get("admin_password_hash", "")):
                self._show_login_error("Usuario o contraseña incorrectos.")
                return
            session = {
                "username": DEFAULT_USER,
                "display_name": self.local_settings.get("admin_display_name", "Dorian"),
                "role": "Administrador",
                "user_id": None,
                "is_local_admin": True,
                "photo": self.local_settings.get("admin_photo", ""),
            }
            self.show_dashboard(session)
            return
        if not username_clean.isdigit():
            self._show_login_error("Para entrar como empleado, escribe tu ID numérico de usuario y contraseña.")
            return
        try:
            if self.db_conn is None or not self.db_conn.is_connected():
                self.db_conn = mysql.connector.connect(**DB_CONFIG)
            rows = self.db_query(
                "SELECT Dni_usu, Nombre, apellido, rol, contrasena FROM usuario WHERE Dni_usu=%s",
                (int(username_clean),),
            )
            if not rows or not verify_password(password, rows[0][4]):
                self._show_login_error("ID de usuario o contraseña incorrectos.")
                return
            user_id, first_name, last_name, role, stored_password = rows[0]
            if not str(stored_password).startswith("pbkdf2_sha256$"):
                self.db_query("UPDATE usuario SET contrasena=%s WHERE Dni_usu=%s", (hash_password(password), user_id), fetch=False)
            display_name = (str(first_name or "") + " " + str(last_name or "")).strip() or str(user_id)
            session = {
                "username": str(user_id),
                "display_name": display_name,
                "role": str(role or "Empleado"),
                "user_id": int(user_id),
                "is_local_admin": False,
                "photo": self._profile_photo_for(str(user_id)),
            }
            self.show_dashboard(session)
        except Error as exc:
            self._show_login_error("No se pudo verificar el usuario en MySQL. Comprueba que XAMPP/MySQL esté iniciado y revisa la conexión.\n" + str(exc))

    def _show_login_error(self, message):
        for child in self.main_container.winfo_children():
            if isinstance(child, LoginFrame):
                child.error.configure(text=message)
                break

    def _profile_photo_for(self, key):
        prefix = "profile_" + re.sub(r"[^A-Za-z0-9_-]", "", str(key))
        for ext in (".png", ".jpg", ".jpeg", ".webp", ".bmp"):
            candidate = os.path.join(PROFILE_DIR, prefix + ext)
            if os.path.isfile(candidate):
                return candidate
        return ""

    def show_dashboard(self, session):
        self.current_user = session["username"]
        self.current_display_name = session["display_name"]
        self.current_role = session["role"]
        self.current_user_id = session["user_id"]
        self.is_local_admin = session["is_local_admin"]
        self.profile_photo_path = session.get("photo", "")
        try:
            if self.db_conn is None or not self.db_conn.is_connected():
                self.db_conn = mysql.connector.connect(**DB_CONFIG)
        except Error as exc:
            messagebox.showerror(
                "No se pudo conectar a MySQL",
                "No fue posible conectar con la base de datos 'drogueria_donmarcos'.\n\n"
                "Verifica que MySQL esté iniciado en XAMPP y que los datos de conexión sean correctos.\n\n"
                f"Detalle: {exc}", parent=self
            )
            return
        for child in self.main_container.winfo_children():
            child.destroy()
        self.build_shell()
        self.show_module("Panel principal")

    def logout(self):
        if self.db_conn is not None:
            try:
                if self.db_conn.is_connected():
                    self.db_conn.close()
            except Error:
                pass
        self.db_conn = None
        self.current_user = DEFAULT_USER
        self.current_display_name = self.local_settings.get("admin_display_name", "Dorian")
        self.current_role = "Administrador"
        self.current_user_id = None
        self.is_local_admin = True
        self.profile_photo_path = self.local_settings.get("admin_photo", "")
        self.show_login()

    def register_employee(self):
        win = ctk.CTkToplevel(self)
        win.title("Solicitud de registro | Droguería Don Marcos")
        win.geometry("560x720")
        win.minsize(500, 560)
        win.configure(fg_color=BG)
        win.transient(self)
        win.grab_set()
        card = ctk.CTkFrame(win, fg_color=WHITE, corner_radius=20, border_width=1, border_color=BORDER)
        card.pack(fill="both", expand=True, padx=18, pady=18)
        ctk.CTkLabel(card, text="Solicitar registro", font=ctk.CTkFont(size=24, weight="bold"), text_color=TEXT).pack(anchor="w", padx=24, pady=(20, 4))
        ctk.CTkLabel(card, text="Tu cuenta solo se activa después de la aprobación de un administrador.", font=ctk.CTkFont(size=12), text_color=MUTED, wraplength=450).pack(anchor="w", padx=24, pady=(0, 10))
        scroll = ctk.CTkScrollableFrame(card, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=18)
        fields = {}
        for label, key, placeholder in [
            ("ID de usuario (documento) *", "id", "Ej. 3040"),
            ("Nombre *", "nombre", "Nombre"),
            ("Apellido *", "apellido", "Apellido"),
            ("Correo *", "correo", "correo@ejemplo.com"),
            ("Teléfono *", "telefono", "Solo números"),
            ("Contraseña (mínimo 8 caracteres) *", "password", "Crea una contraseña"),
            ("Confirmar contraseña *", "confirm", "Repite la contraseña"),
        ]:
            ctk.CTkLabel(scroll, text=label, font=ctk.CTkFont(size=12, weight="bold"), text_color=TEXT).pack(anchor="w", padx=6, pady=(7, 3))
            entry = ctk.CTkEntry(scroll, height=36, corner_radius=10, placeholder_text=placeholder, show="•" if key in ("password", "confirm") else "")
            entry.pack(fill="x", padx=6)
            fields[key] = entry
        photo_state = {"path": ""}
        photo_label = ctk.CTkLabel(scroll, text="Sin foto de perfil (opcional)", text_color=MUTED, anchor="w")
        photo_label.pack(fill="x", padx=6, pady=(10, 2))
        def choose_photo():
            selected = filedialog.askopenfilename(parent=win, title="Seleccionar foto de perfil", filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.webp *.bmp")])
            if selected:
                photo_state["path"] = selected
                photo_label.configure(text=os.path.basename(selected), text_color=TEXT)
        ctk.CTkButton(scroll, text="Seleccionar foto", command=choose_photo, height=32, fg_color=NAVY, hover_color="#3A3A3A").pack(anchor="w", padx=6, pady=(0, 10))

        def save_registration():
            values = {key: entry.get().strip() for key, entry in fields.items()}
            if any(not values[k] for k in fields):
                messagebox.showwarning("Campos obligatorios", "Completa todos los campos requeridos.", parent=win)
                return
            if not values["id"].isdigit() or int(values["id"]) <= 0 or not values["telefono"].isdigit() or int(values["telefono"]) <= 0:
                messagebox.showwarning("Datos inválidos", "El ID y el teléfono deben ser números enteros positivos.", parent=win)
                return
            if "@" not in values["correo"] or "." not in values["correo"].split("@")[-1]:
                messagebox.showwarning("Correo inválido", "Escribe un correo electrónico válido.", parent=win)
                return
            if len(values["password"]) < 8:
                messagebox.showwarning("Contraseña débil", "La contraseña debe tener al menos 8 caracteres.", parent=win)
                return
            if values["password"] != values["confirm"]:
                messagebox.showwarning("Contraseñas diferentes", "La confirmación no coincide con la contraseña.", parent=win)
                return
            try:
                duplicate_user = self.db_query("SELECT Dni_usu FROM usuario WHERE Dni_usu=%s OR LOWER(correo)=LOWER(%s) LIMIT 1", (int(values["id"]), values["correo"]))
                if duplicate_user:
                    messagebox.showwarning("Usuario existente", "Ya existe una cuenta activa con ese ID o correo.", parent=win)
                    return
                duplicate_request = self.db_query("SELECT id_solicitud FROM solicitud_de_registros WHERE (Dni_usu=%s OR LOWER(correo)=LOWER(%s)) AND estado='Pendiente' LIMIT 1", (int(values["id"]), values["correo"]))
                if duplicate_request:
                    messagebox.showwarning("Solicitud existente", "Ya hay una solicitud pendiente con ese ID o correo.", parent=win)
                    return
                photo_path = None
                if photo_state["path"]:
                    ext = os.path.splitext(photo_state["path"])[1].lower()
                    photo_path = os.path.join(PROFILE_DIR, f"solicitud_{values['id']}_{datetime.now().strftime('%Y%m%d%H%M%S')}{ext}")
                    shutil.copy2(photo_state["path"], photo_path)
                self.db_query(
                    "INSERT INTO solicitud_de_registros (Dni_usu, Nombre, apellido, correo, telefono, contrasena_hash, foto_temporal, estado) VALUES (%s,%s,%s,%s,%s,%s,%s,'Pendiente')",
                    (int(values["id"]), values["nombre"], values["apellido"], values["correo"], int(values["telefono"]), hash_password(values["password"]), photo_path),
                    fetch=False,
                )
                messagebox.showinfo("Solicitud enviada", "Solicitud enviada correctamente. Espera la aprobación de un administrador.", parent=win)
                win.destroy()
            except (Error, OSError) as exc:
                messagebox.showerror("No se pudo enviar", "No fue posible guardar la solicitud. Comprueba la conexión y que la migración SQL esté aplicada.\n\n" + str(exc), parent=win)

        buttons = ctk.CTkFrame(card, fg_color="transparent")
        buttons.pack(fill="x", padx=24, pady=14)
        ctk.CTkButton(buttons, text="Cancelar", fg_color=WHITE, text_color=TEXT, border_width=1, border_color=BORDER, hover_color=BG, corner_radius=10, command=win.destroy).pack(side="right", padx=(8, 0))
        ctk.CTkButton(buttons, text="Enviar solicitud", fg_color=GREEN, hover_color=GREEN_DARK, corner_radius=10, command=save_registration).pack(side="right")

    def build_shell(self):
        self.sidebar = ctk.CTkFrame(self.main_container, width=245, fg_color=NAVY, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        brand = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        brand.pack(fill="x", padx=20, pady=(22, 24))
        ctk.CTkLabel(brand, text="✚", font=ctk.CTkFont(size=27, weight="bold"), text_color="#FFD2D2").pack(side="left", padx=(0, 10))
        ctk.CTkLabel(brand, text="Don Marcos\nDROGUERÍA", justify="left", font=ctk.CTkFont(size=16, weight="bold"), text_color=WHITE).pack(side="left")
        ctk.CTkLabel(self.sidebar, text="MENÚ PRINCIPAL", text_color="#E8C5C7", font=ctk.CTkFont(size=10, weight="bold")).pack(anchor="w", padx=22, pady=(0, 9))
        nav_area = ctk.CTkScrollableFrame(self.sidebar, fg_color="transparent", corner_radius=0)
        nav_area.pack(fill="both", expand=True, padx=0, pady=0)
        self.nav_buttons = {}
        admin_only_modules = {"Usuarios", "Directorio de usuarios", "Solicitudes de registro", "Proveedores", "Categorías"}
        for name, (icon, subtitle) in MODULES.items():
            if name in admin_only_modules and not self.has_admin_permissions():
                continue
            btn = ctk.CTkButton(nav_area, text=f"{icon}   {name}", anchor="w", height=37, corner_radius=9,
                                fg_color=GREEN if name == self.active_module else "transparent",
                                hover_color="#3A3A3A", text_color=WHITE, font=ctk.CTkFont(size=12, weight="bold" if name == self.active_module else "normal"),
                                command=lambda n=name: self.show_module(n))
            btn.pack(fill="x", padx=12, pady=2)
            self.nav_buttons[name] = btn
        ctk.CTkFrame(self.sidebar, height=1, fg_color="#343434").pack(fill="x", padx=18, pady=(8, 10))
        ctk.CTkButton(self.sidebar, text="↪   Cerrar sesión", anchor="w", height=38, fg_color="transparent", hover_color="#3A3A3A", text_color="#F5C6C3", command=self.logout).pack(fill="x", padx=12, pady=(0, 12))

        self.content = ctk.CTkFrame(self.main_container, fg_color=BG, corner_radius=0)
        self.content.pack(side="left", fill="both", expand=True)
        top = ctk.CTkFrame(self.content, height=72, fg_color=WHITE, corner_radius=0, border_width=0)
        top.pack(fill="x")
        top.pack_propagate(False)
        ctk.CTkLabel(top, text="Sistema de gestión", font=ctk.CTkFont(size=14, weight="bold"), text_color=NAVY).pack(side="left", padx=28)
        ctk.CTkLabel(top, text="●  Sistema local  ", text_color=GREEN, font=ctk.CTkFont(size=12)).pack(side="right", padx=(8, 24))
        ctk.CTkLabel(top, text=f"{self.current_role}  |  {self.current_display_name}", text_color=TEXT, font=ctk.CTkFont(size=12, weight="bold")).pack(side="right", padx=8)
        avatar_text = "".join(part[0] for part in self.current_display_name.split()[:2]).upper() or "DM"
        avatar = ctk.CTkLabel(top, text=avatar_text, width=40, height=40, corner_radius=20, fg_color=GREEN_PALE, text_color=GREEN_DARK, font=ctk.CTkFont(size=12, weight="bold"))
        if self.profile_photo_path and os.path.isfile(self.profile_photo_path):
            try:
                self.avatar_image = ctk.CTkImage(light_image=Image.open(self.profile_photo_path), dark_image=Image.open(self.profile_photo_path), size=(40, 40))
                avatar.configure(text="", image=self.avatar_image, fg_color=WHITE)
            except Exception:
                pass
        avatar.pack(side="right", padx=(18, 0))
        self.page = ctk.CTkFrame(self.content, fg_color=BG, corner_radius=0)
        self.page.pack(fill="both", expand=True, padx=26, pady=22)

    def set_nav_active(self, module):
        for name, btn in self.nav_buttons.items():
            btn.configure(fg_color=GREEN if name == module else "transparent",
                          font=ctk.CTkFont(size=12, weight="bold" if name == module else "normal"))

    def has_admin_permissions(self):
        return bool(getattr(self, "is_local_admin", False) or str(getattr(self, "current_role", "")).strip().casefold() == "administrador")

    def show_module(self, module):
        admin_only = {"Usuarios", "Directorio de usuarios", "Solicitudes de registro", "Proveedores", "Categorías"}
        if module in admin_only and not self.has_admin_permissions():
            messagebox.showerror("Permiso denegado", "Este módulo solo está disponible para Dorian y los administradores.", parent=self)
            return
        self.active_module = module
        if hasattr(self, "nav_buttons"):
            self.set_nav_active(module)
        for child in self.page.winfo_children():
            child.destroy()
        if module == "Panel principal":
            self.render_dashboard()
        elif module == "Reportes":
            self.render_reports()
        elif module == "Configuración":
            self.render_settings()
        elif module == "Solicitudes de registro":
            self.render_registration_requests()
        else:
            self.render_table_module(module)

    def page_heading(self, title, subtitle, action_text=None, action=None):
        header = ctk.CTkFrame(self.page, fg_color="transparent")
        header.pack(fill="x", pady=(0, 18))
        left = ctk.CTkFrame(header, fg_color="transparent")
        left.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(left, text=title, font=ctk.CTkFont(size=26, weight="bold"), text_color=TEXT).pack(anchor="w")
        ctk.CTkLabel(left, text=subtitle, font=ctk.CTkFont(size=12), text_color=MUTED).pack(anchor="w", pady=(4, 0))
        if action_text:
            ctk.CTkButton(header, text=action_text, command=action, height=38, corner_radius=9, fg_color=GREEN, hover_color=GREEN_DARK).pack(side="right", padx=(12, 0))

    def render_dashboard(self):
        now = datetime.now().strftime("%A, %d de %B de %Y")
        self.page_heading("Panel principal", f"Bienvenido, {self.current_user}. Aquí tienes el resumen de la droguería.")
        cards = ctk.CTkFrame(self.page, fg_color="transparent")
        cards.pack(fill="x", pady=(0, 18))
        stats = [
            ("Productos registrados", "248", "En el catálogo", GREEN),
            ("Ventas de hoy", "$ 486.500", "Resumen de demostración", "#2766A5"),
            ("Stock bajo", "08", "Requieren revisión", AMBER),
            ("Citas pendientes", "05", "Próximas atenciones", "#A61F24"),
        ]
        for i, (label, value, hint, color) in enumerate(stats):
            cards.grid_columnconfigure(i, weight=1, uniform="stats")
            card = ctk.CTkFrame(cards, fg_color=WHITE, corner_radius=15, border_width=1, border_color=BORDER)
            card.grid(row=0, column=i, sticky="nsew", padx=(0 if i == 0 else 7, 0 if i == 3 else 7))
            ctk.CTkFrame(card, width=5, fg_color=color, corner_radius=3).pack(side="left", fill="y", padx=(0, 14), pady=16)
            body = ctk.CTkFrame(card, fg_color="transparent")
            body.pack(side="left", fill="both", expand=True, pady=16, padx=(0, 12))
            ctk.CTkLabel(body, text=label, text_color=MUTED, font=ctk.CTkFont(size=11)).pack(anchor="w")
            ctk.CTkLabel(body, text=value, text_color=TEXT, font=ctk.CTkFont(size=23, weight="bold")).pack(anchor="w", pady=(5, 2))
            ctk.CTkLabel(body, text=hint, text_color=color, font=ctk.CTkFont(size=10)).pack(anchor="w")
        lower = ctk.CTkFrame(self.page, fg_color="transparent")
        lower.pack(fill="both", expand=True)
        lower.grid_columnconfigure(0, weight=3)
        lower.grid_columnconfigure(1, weight=2)
        lower.grid_rowconfigure(0, weight=1)
        recent = ctk.CTkFrame(lower, fg_color=WHITE, corner_radius=15, border_width=1, border_color=BORDER)
        recent.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        ctk.CTkLabel(recent, text="Actividad reciente", text_color=TEXT, font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=20, pady=(18, 3))
        ctk.CTkLabel(recent, text="Movimientos registrados en el sistema", text_color=MUTED, font=ctk.CTkFont(size=11)).pack(anchor="w", padx=20, pady=(0, 12))
        for title, detail, tag, color in [
            ("Entrada de inventario", "Acetaminofén 500 mg · 50 unidades", "ENTRADA", GREEN),
            ("Venta completada", "Venta VEN-001 · $ 24.000", "VENTA", "#2766A5"),
            ("Stock bajo", "Gafas de lectura · quedan 8 unidades", "ALERTA", AMBER),
            ("Cita confirmada", "María Pérez · mañana a las 09:00", "CITA", "#A61F24"),
        ]:
            row = ctk.CTkFrame(recent, fg_color="#FFF8F8", corner_radius=10)
            row.pack(fill="x", padx=16, pady=5)
            ctk.CTkLabel(row, text="●", text_color=color, font=ctk.CTkFont(size=15)).pack(side="left", padx=12)
            txt = ctk.CTkFrame(row, fg_color="transparent")
            txt.pack(side="left", fill="x", expand=True, pady=10)
            ctk.CTkLabel(txt, text=title, text_color=TEXT, font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w")
            ctk.CTkLabel(txt, text=detail, text_color=MUTED, font=ctk.CTkFont(size=10)).pack(anchor="w", pady=(2, 0))
            ctk.CTkLabel(row, text=tag, text_color=color, font=ctk.CTkFont(size=9, weight="bold")).pack(side="right", padx=12)
        alerts = ctk.CTkFrame(lower, fg_color=WHITE, corner_radius=15, border_width=1, border_color=BORDER)
        alerts.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        ctk.CTkLabel(alerts, text="Alertas importantes", text_color=TEXT, font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=18, pady=(18, 14))
        for title, detail, color in [
            ("Existencias bajas", "8 productos por debajo del mínimo", AMBER),
            ("Productos agotados", "1 producto sin existencias", RED),
            ("Citas pendientes", "5 citas por confirmar o atender", "#A61F24"),
        ]:
            box = ctk.CTkFrame(alerts, fg_color="#FFF8F8", corner_radius=10)
            box.pack(fill="x", padx=14, pady=5)
            ctk.CTkFrame(box, width=4, fg_color=color, corner_radius=3).pack(side="left", fill="y", padx=(0, 10), pady=10)
            txt = ctk.CTkFrame(box, fg_color="transparent")
            txt.pack(side="left", fill="x", expand=True, pady=10, padx=(0, 8))
            ctk.CTkLabel(txt, text=title, text_color=TEXT, font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w")
            ctk.CTkLabel(txt, text=detail, text_color=MUTED, font=ctk.CTkFont(size=10), wraplength=220, justify="left").pack(anchor="w", pady=(3, 0))
        ctk.CTkLabel(alerts, text="Los datos mostrados son de demostración.", text_color=MUTED, font=ctk.CTkFont(size=10)).pack(anchor="w", padx=18, pady=(15, 0))

    def render_table_module(self, module):
        config = TABLE_CONFIG.get(module)
        if not config:
            self.page_heading(module, "Interfaz preparada para conectar con tu base de datos.")
            ctk.CTkFrame(self.page, fg_color=WHITE, corner_radius=15, border_width=1, border_color=BORDER).pack(fill="both", expand=True)
            ctk.CTkLabel(self.page.winfo_children()[-1], text="Este módulo está listo para implementar sus operaciones.", text_color=MUTED).pack(pady=60)
            return
        self.page_heading(module, MODULES[module][1], "+ Nuevo registro", lambda: self.open_form(module, config["fields"]))
        toolbar = ctk.CTkFrame(self.page, fg_color=WHITE, corner_radius=12, border_width=1, border_color=BORDER)
        toolbar.pack(fill="x", pady=(0, 14))
        search = ctk.CTkEntry(toolbar, placeholder_text=f"Buscar en {module.lower()}...", height=38, width=320, corner_radius=9)
        search.pack(side="left", padx=14, pady=12)
        ctk.CTkButton(toolbar, text="Buscar", width=90, height=38, corner_radius=9, fg_color=NAVY, hover_color="#3A3A3A",
                      command=lambda: self.filter_table(tree, search.get())).pack(side="left", pady=12)
        ctk.CTkLabel(toolbar, text=f"{len(config['rows'])} registros de ejemplo", text_color=MUTED, font=ctk.CTkFont(size=11)).pack(side="right", padx=16)
        table_frame = ctk.CTkFrame(self.page, fg_color=WHITE, corner_radius=12, border_width=1, border_color=BORDER)
        table_frame.pack(fill="both", expand=True)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=WHITE, foreground=TEXT, fieldbackground=WHITE, rowheight=36, borderwidth=0, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background="#FDE3E4", foreground=NAVY, font=("Segoe UI", 10, "bold"), relief="flat", padding=10)
        style.map("Treeview", background=[("selected", "#F8D7D9")], foreground=[("selected", TEXT)])
        columns = [c[0] for c in config["columns"]]
        tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col, width in config["columns"]:
            tree.heading(col, text=col)
            tree.column(col, width=width, minwidth=70, anchor="w")
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        tree.grid(row=0, column=0, sticky="nsew", padx=(12, 0), pady=12)
        vsb.grid(row=0, column=1, sticky="ns", pady=12, padx=(0, 12))
        hsb.grid(row=1, column=0, sticky="ew", padx=(12, 0))
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        for row in config["rows"]:
            tree.insert("", "end", values=row)
        footer = ctk.CTkFrame(self.page, fg_color="transparent")
        footer.pack(fill="x", pady=(12, 0))
        ctk.CTkLabel(footer, text="Selecciona un registro para ver las acciones disponibles.", text_color=MUTED, font=ctk.CTkFont(size=11)).pack(side="left")
        ctk.CTkButton(footer, text="Ver / editar", width=110, height=34, fg_color=WHITE, text_color=NAVY, border_width=1, border_color=BORDER, hover_color=GREEN_PALE, command=lambda: self.edit_selected(tree, module, config["fields"])).pack(side="right", padx=(8, 0))
        ctk.CTkButton(footer, text="Desactivar", width=100, height=34, fg_color="#FDE3E4", text_color=RED, hover_color="#F9CED0", command=lambda: self.deactivate_selected(tree)).pack(side="right")

    def filter_table(self, tree, query):
        q = query.strip().lower()
        for item in tree.get_children():
            values = tree.item(item, "values")
            tree.detach(item)
            if not q or any(q in str(v).lower() for v in values):
                tree.reattach(item, "", "end")

    def edit_selected(self, tree, module, fields):
        selected = tree.selection()
        if not selected:
            messagebox.showinfo("Seleccionar registro", "Selecciona primero un registro de la tabla.")
            return
        vals = tree.item(selected[0], "values")
        self.open_form(module, fields, initial=vals)

    def deactivate_selected(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showinfo("Seleccionar registro", "Selecciona primero un registro.")
            return
        if messagebox.askyesno("Confirmar", "¿Deseas marcar este registro de ejemplo como desactivado en esta vista?"):
            vals = list(tree.item(selected[0], "values"))
            vals[-1] = "Inactivo"
            tree.item(selected[0], values=vals)
            messagebox.showinfo("Vista de demostración", "Se actualizó el estado solo en esta vista. Conecta el backend para guardar cambios en MySQL.")

    def open_form(self, module, fields, initial=None):
        win = ctk.CTkToplevel(self)
        win.title(f"{'Editar' if initial else 'Nuevo'} registro | {module}")
        win.geometry("590x700")
        win.minsize(520, 480)
        win.configure(fg_color=BG)
        win.transient(self)
        win.grab_set()
        outer = ctk.CTkFrame(win, fg_color=WHITE, corner_radius=16, border_width=1, border_color=BORDER)
        outer.pack(fill="both", expand=True, padx=18, pady=18)
        ctk.CTkLabel(outer, text=f"{'Editar registro' if initial else 'Nuevo registro'}", text_color=TEXT, font=ctk.CTkFont(size=22, weight="bold")).pack(anchor="w", padx=22, pady=(22, 4))
        ctk.CTkLabel(outer, text=f"Módulo: {module}", text_color=MUTED, font=ctk.CTkFont(size=12)).pack(anchor="w", padx=22, pady=(0, 14))
        scroll = ctk.CTkScrollableFrame(outer, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=22)
        entries = {}
        for i, field in enumerate(fields):
            ctk.CTkLabel(scroll, text=field, text_color=TEXT, font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", pady=(8, 4))
            entry = ctk.CTkEntry(scroll, height=38, corner_radius=8, placeholder_text=f"Ingresa {field.lower()}")
            entry.pack(fill="x")
            if initial and i < len(initial):
                entry.insert(0, str(initial[i]))
            entries[field] = entry
        buttons = ctk.CTkFrame(outer, fg_color="transparent")
        buttons.pack(fill="x", padx=22, pady=18)
        ctk.CTkButton(buttons, text="Cancelar", fg_color=WHITE, text_color=TEXT, border_width=1, border_color=BORDER, hover_color=BG, command=win.destroy).pack(side="right", padx=(8, 0))
        def save():
            data = {k: v.get().strip() for k, v in entries.items()}
            empty = [k for k, v in data.items() if not v]
            if empty:
                messagebox.showwarning("Campos requeridos", "Completa los campos: " + ", ".join(empty[:5]), parent=win)
                return
            messagebox.showinfo("Formulario validado", "Los datos se validaron en la interfaz. Para guardarlos permanentemente, conecta este formulario con las operaciones de tu base de datos MySQL.", parent=win)
            win.destroy()
        ctk.CTkButton(buttons, text="Guardar", fg_color=GREEN, hover_color=GREEN_DARK, command=save).pack(side="right")

    def render_reports(self):
        self.page_heading("Reportes", "Ventas, inventario, movimientos y productos próximos a vencer")
        card = ctk.CTkFrame(self.page, fg_color=WHITE, corner_radius=15, border_width=1, border_color=BORDER)
        card.pack(fill="both", expand=True)
        ctk.CTkLabel(card, text="Reportes de gestión", font=ctk.CTkFont(size=20, weight="bold"), text_color=TEXT).pack(anchor="w", padx=24, pady=(20, 8))
        options = [
            ("Ventas registradas", "SELECT v.id_venta, v.fecha, v.total, v.metodo_pago, CONCAT(COALESCE(c.nombre,''),' ',COALESCE(c.apellido,'')) FROM venta v LEFT JOIN cliente c ON c.dni_client=v.dni_client ORDER BY v.fecha DESC"),
            ("Productos con pocas existencias", "SELECT id_producto, nombre, stock, stock_minimo FROM producto WHERE stock<=COALESCE(stock_minimo,0) ORDER BY stock ASC"),
            ("Productos próximos a vencer (90 días)", "SELECT id_producto, nombre, fecha_vencimiento, stock FROM producto WHERE fecha_vencimiento IS NOT NULL AND fecha_vencimiento BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 90 DAY) ORDER BY fecha_vencimiento"),
            ("Movimientos de inventario", "SELECT id_movimiento, fecha, tipo_movimiento, cantidad, motivo, id_producto FROM movimiento_inventario ORDER BY fecha DESC, id_movimiento DESC"),
            ("Ventas por empleado", "SELECT u.Dni_usu, CONCAT(u.Nombre,' ',u.apellido), COUNT(v.id_venta), COALESCE(SUM(v.total),0) FROM usuario u LEFT JOIN venta v ON v.Dni_usu=u.Dni_usu GROUP BY u.Dni_usu, u.Nombre, u.apellido ORDER BY SUM(v.total) DESC"),
        ]
        selector = ctk.CTkFrame(card, fg_color="transparent")
        selector.pack(fill="x", padx=22, pady=10)
        report_var = ctk.StringVar(value=options[0][0])
        ctk.CTkOptionMenu(selector, values=[x[0] for x in options], variable=report_var, width=330, fg_color=GREEN, button_color=GREEN_DARK).pack(side="left", padx=(0, 10))
        holder = ctk.CTkFrame(card, fg_color=WHITE)
        holder.pack(fill="both", expand=True, padx=22, pady=(0, 20))
        def load_report():
            for child in holder.winfo_children():
                child.destroy()
            query = dict(options)[report_var.get()]
            try:
                rows = self.db_query(query)
                if not rows:
                    ctk.CTkLabel(holder, text="No hay registros para mostrar en este reporte.", text_color=MUTED).pack(pady=30)
                    return
                headings = {
                    "Ventas registradas": ["Venta", "Fecha", "Total", "Método de pago", "Cliente"],
                    "Productos con pocas existencias": ["Producto", "Nombre", "Stock", "Stock mínimo"],
                    "Productos próximos a vencer (90 días)": ["Producto", "Nombre", "Vencimiento", "Stock"],
                    "Movimientos de inventario": ["Movimiento", "Fecha", "Tipo", "Cantidad", "Motivo", "Producto"],
                    "Ventas por empleado": ["Documento", "Empleado", "Cantidad ventas", "Total ventas"],
                }.get(report_var.get(), [f"Campo {i+1}" for i in range(len(rows[0]))])
                tree = ttk.Treeview(holder, columns=headings, show="headings", height=15)
                for col in headings:
                    tree.heading(col, text=col)
                    tree.column(col, width=165, minwidth=90, anchor="w")
                for row in rows:
                    tree.insert("", "end", values=tuple("" if value is None else str(value) for value in row))
                tree.pack(fill="both", expand=True)
                ctk.CTkLabel(holder, text=f"{len(rows)} registros encontrados", text_color=MUTED).pack(anchor="w", pady=(8, 0))
            except Error as exc:
                messagebox.showerror("Error al generar reporte", str(exc), parent=self)
        ctk.CTkButton(selector, text="Generar reporte", command=load_report, fg_color=NAVY, hover_color="#3A3A3A").pack(side="left")
        load_report()

    def render_settings(self):
        self.page_heading("Configuración", "Administra tu perfil, contraseña y foto de usuario.")
        scroll = ctk.CTkScrollableFrame(self.page, fg_color="transparent", corner_radius=0)
        scroll.pack(fill="both", expand=True)
        card = ctk.CTkFrame(scroll, fg_color=WHITE, corner_radius=18, border_width=1, border_color=BORDER)
        card.pack(fill="x", anchor="n", pady=(0, 14))
        ctk.CTkLabel(card, text="Mi perfil", text_color=TEXT, font=ctk.CTkFont(size=20, weight="bold")).pack(anchor="w", padx=24, pady=(22, 4))
        ctk.CTkLabel(card, text="Los cambios se guardan en este equipo o en MySQL según el tipo de cuenta.", text_color=MUTED, font=ctk.CTkFont(size=12)).pack(anchor="w", padx=24, pady=(0, 16))
        profile_row = ctk.CTkFrame(card, fg_color="transparent")
        profile_row.pack(fill="x", padx=24, pady=(0, 12))
        preview = ctk.CTkLabel(profile_row, text="Foto", width=92, height=92, corner_radius=46, fg_color=GREEN_PALE, text_color=GREEN_DARK, font=ctk.CTkFont(size=14, weight="bold"))
        self.profile_preview_image = None
        if self.profile_photo_path and os.path.isfile(self.profile_photo_path):
            try:
                self.profile_preview_image = ctk.CTkImage(light_image=Image.open(self.profile_photo_path), dark_image=Image.open(self.profile_photo_path), size=(92, 92))
                preview.configure(text="", image=self.profile_preview_image, fg_color=WHITE)
            except Exception:
                pass
        preview.pack(side="left", padx=(0, 18))
        photo_actions = ctk.CTkFrame(profile_row, fg_color="transparent")
        photo_actions.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(photo_actions, text="Foto de perfil", text_color=TEXT, font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", pady=(6, 4))
        ctk.CTkLabel(photo_actions, text="PNG, JPG, JPEG, WEBP o BMP. La imagen se conserva en este equipo.", text_color=MUTED, font=ctk.CTkFont(size=11), wraplength=520, justify="left").pack(anchor="w", pady=(0, 10))
        ctk.CTkButton(photo_actions, text="Seleccionar foto", width=150, height=36, corner_radius=10, fg_color=GREEN, hover_color=GREEN_DARK, command=self.choose_profile_photo).pack(anchor="w")

        name_fields = {}
        if self.is_local_admin:
            name_specs = [("Nombre para mostrar", "display_name", self.current_display_name)]
        else:
            try:
                row = self.db_query("SELECT Nombre, apellido FROM usuario WHERE Dni_usu=%s", (self.current_user_id,))
                current_first, current_last = row[0] if row else (self.current_display_name, "")
            except Error:
                current_first, current_last = self.current_display_name, ""
            name_specs = [("Nombre", "nombre", current_first or ""), ("Apellido", "apellido", current_last or "")]
        for label, key, value in name_specs:
            ctk.CTkLabel(card, text=label, text_color=TEXT, font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=24, pady=(8, 4))
            entry = ctk.CTkEntry(card, height=40, corner_radius=10, width=440)
            entry.pack(anchor="w", padx=24)
            entry.insert(0, str(value))
            name_fields[key] = entry

        ctk.CTkLabel(card, text="Cambiar contraseña (opcional)", text_color=TEXT, font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=24, pady=(22, 4))
        ctk.CTkLabel(card, text="Déjala vacía si no deseas cambiarla. Para cambiarla debes confirmar tu contraseña actual.", text_color=MUTED, font=ctk.CTkFont(size=11), wraplength=760, justify="left").pack(anchor="w", padx=24, pady=(0, 8))
        password_fields = {}
        for label, key in [("Contraseña actual", "current_password"), ("Nueva contraseña", "new_password"), ("Confirmar nueva contraseña", "confirm_password")]:
            ctk.CTkLabel(card, text=label, text_color=TEXT, font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=24, pady=(8, 4))
            entry = ctk.CTkEntry(card, height=40, corner_radius=10, width=440, show="•", placeholder_text=label)
            entry.pack(anchor="w", padx=24)
            password_fields[key] = entry

        def save_profile():
            names = {key: entry.get().strip() for key, entry in name_fields.items()}
            if any(not value for value in names.values()):
                messagebox.showwarning("Nombre obligatorio", "Completa los campos del nombre.", parent=self)
                return
            current_password = password_fields["current_password"].get()
            new_password = password_fields["new_password"].get()
            confirm_password = password_fields["confirm_password"].get()
            changing_password = bool(new_password or confirm_password or current_password)
            if changing_password:
                if not current_password:
                    messagebox.showwarning("Verificación necesaria", "Escribe tu contraseña actual para autorizar el cambio.", parent=self)
                    return
                if len(new_password) < 8:
                    messagebox.showwarning("Contraseña inválida", "La nueva contraseña debe tener al menos 8 caracteres.", parent=self)
                    return
                if new_password != confirm_password:
                    messagebox.showwarning("Contraseñas diferentes", "La confirmación de la nueva contraseña no coincide.", parent=self)
                    return
            try:
                if self.is_local_admin:
                    settings = load_local_settings()
                    if changing_password and not verify_password(current_password, settings.get("admin_password_hash", "")):
                        messagebox.showerror("Contraseña incorrecta", "La contraseña actual no es correcta.", parent=self)
                        return
                    settings["admin_display_name"] = names["display_name"]
                    if changing_password:
                        settings["admin_password_hash"] = hash_password(new_password)
                    if self.profile_photo_path:
                        settings["admin_photo"] = self.profile_photo_path
                    save_local_settings(settings)
                    self.local_settings = settings
                else:
                    rows = self.db_query("SELECT contrasena FROM usuario WHERE Dni_usu=%s", (self.current_user_id,))
                    if not rows:
                        messagebox.showerror("Cuenta no encontrada", "No se encontró tu usuario en MySQL.", parent=self)
                        return
                    if changing_password and not verify_password(current_password, rows[0][0]):
                        messagebox.showerror("Contraseña incorrecta", "La contraseña actual no es correcta.", parent=self)
                        return
                    if changing_password:
                        self.db_query("UPDATE usuario SET Nombre=%s, apellido=%s, contrasena=%s WHERE Dni_usu=%s", (names["nombre"], names["apellido"], hash_password(new_password), self.current_user_id), fetch=False)
                    else:
                        self.db_query("UPDATE usuario SET Nombre=%s, apellido=%s WHERE Dni_usu=%s", (names["nombre"], names["apellido"], self.current_user_id), fetch=False)
                if self.is_local_admin:
                    self.current_display_name = names["display_name"]
                else:
                    self.current_display_name = (names["nombre"] + " " + names["apellido"]).strip()
                messagebox.showinfo("Perfil actualizado", "Los cambios del perfil se guardaron correctamente.", parent=self)
                self.build_header_refresh()
            except (Error, OSError) as exc:
                messagebox.showerror("No se pudo guardar", f"No se pudieron guardar los cambios.\n\n{exc}", parent=self)

        ctk.CTkButton(card, text="Guardar cambios del perfil", height=44, corner_radius=12, fg_color=GREEN, hover_color=GREEN_DARK, command=save_profile).pack(anchor="w", padx=24, pady=24)

        info = ctk.CTkFrame(scroll, fg_color=WHITE, corner_radius=18, border_width=1, border_color=BORDER)
        info.pack(fill="x", pady=(0, 14))
        ctk.CTkLabel(info, text="Información del sistema", text_color=TEXT, font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", padx=24, pady=(20, 4))
        ctk.CTkLabel(info, text="Base de datos: drogueria_donmarcos · Tema visual: rojo, negro y blanco · Las fotos de perfil se guardan localmente en profile_photos.", text_color=MUTED, wraplength=800, justify="left", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=24, pady=(0, 20))

    def choose_profile_photo(self):
        path = filedialog.askopenfilename(
            parent=self,
            title="Seleccionar foto de perfil",
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.webp *.bmp"), ("Todos los archivos", "*.*")],
        )
        if not path:
            return
        try:
            with Image.open(path) as image:
                image.verify()
            key = "dorian" if self.is_local_admin else str(self.current_user_id)
            ext = os.path.splitext(path)[1].lower()
            if ext not in (".png", ".jpg", ".jpeg", ".webp", ".bmp"):
                raise ValueError("Formato de imagen no compatible.")
            target = os.path.join(PROFILE_DIR, "profile_" + key + ext)
            for old_ext in (".png", ".jpg", ".jpeg", ".webp", ".bmp"):
                old_path = os.path.join(PROFILE_DIR, "profile_" + key + old_ext)
                if old_path != target and os.path.isfile(old_path):
                    os.remove(old_path)
            shutil.copy2(path, target)
            self.profile_photo_path = target
            if self.is_local_admin:
                settings = load_local_settings()
                settings["admin_photo"] = target
                save_local_settings(settings)
                self.local_settings = settings
            messagebox.showinfo("Foto actualizada", "La foto se guardó correctamente.", parent=self)
            self.build_header_refresh()
        except (OSError, ValueError) as exc:
            messagebox.showerror("Imagen no válida", f"No se pudo utilizar esa imagen.\n\n{exc}", parent=self)

    def build_header_refresh(self):
        # Reconstruye el marco para actualizar el nombre y avatar, conservando el módulo actual.
        module_to_restore = self.active_module
        self.show_dashboard({
            "username": self.current_user,
            "display_name": self.current_display_name,
            "role": self.current_role,
            "user_id": self.current_user_id,
            "is_local_admin": self.is_local_admin,
            "photo": self.profile_photo_path,
        })
        if module_to_restore != "Panel principal":
            self.show_module(module_to_restore)


    # Consultas adaptadas a las tablas reales del archivo SQL del usuario.
    DB_VIEWS = {
        "Productos": {
            "sql": "SELECT p.id_producto AS codigo, p.nombre, COALESCE(c.nombre,'Sin categoría') AS categoria, p.precio_venta, p.stock, CASE WHEN p.stock = 0 THEN 'Agotado' WHEN p.stock <= COALESCE(p.stock_minimo,0) THEN 'Stock bajo' ELSE 'Disponible' END AS estado FROM producto p LEFT JOIN categoria c ON c.id_categoria=p.id_categoria ORDER BY p.id_producto",
            "columns": [("Código", 90), ("Nombre", 190), ("Categoría", 150), ("Precio venta", 110), ("Stock", 75), ("Estado", 100)],
            "table": "producto", "pk": "id_producto", "fields": [("ID producto", "id_producto", "required"), ("Nombre", "nombre", "required"), ("Descripción", "descripcion", "required"), ("Precio compra", "precio_compra", "required"), ("Precio venta", "precio_venta", "required"), ("Stock", "stock", "required"), ("Stock mínimo", "stock_minimo", "required"), ("Fecha vencimiento (AAAA-MM-DD)", "fecha_vencimiento", "optional"), ("Lote", "lote", "optional"), ("Registro sanitario", "registro_sanitario", "optional"), ("ID categoría", "id_categoria", "required"), ("ID proveedor", "id_provedor", "optional")],
        },
        "Categorías": {
            "sql": "SELECT id_categoria AS codigo, nombre, descripcion FROM categoria ORDER BY id_categoria",
            "columns": [("Código", 100), ("Nombre", 200), ("Descripción", 360)],
            "table": "categoria", "pk": "id_categoria", "fields": [("ID categoría", "id_categoria", "required"), ("Nombre", "nombre", "required"), ("Descripción", "descripcion", "required")],
        },
        "Inventario": {
            "sql": "SELECT p.id_producto AS codigo, p.nombre, COALESCE(c.nombre,'Sin categoría') AS categoria, p.stock, p.stock_minimo, p.fecha_vencimiento, CASE WHEN p.stock=0 THEN 'Agotado' WHEN p.stock<=COALESCE(p.stock_minimo,0) THEN 'Stock bajo' ELSE 'Disponible' END AS estado FROM producto p LEFT JOIN categoria c ON c.id_categoria=p.id_categoria ORDER BY p.id_producto",
            "columns": [("Código", 85), ("Producto", 180), ("Categoría", 145), ("Stock", 70), ("Mínimo", 75), ("Vencimiento", 120), ("Estado", 100)],
        },
        "Movimientos": {
            "sql": "SELECT m.id_movimiento AS codigo, m.fecha, COALESCE(p.nombre,'Producto eliminado') AS producto, m.tipo_movimiento, m.cantidad, COALESCE(CONCAT(u.Nombre,' ',u.apellido),'Dorian / sin usuario MySQL') AS responsable, m.motivo, COALESCE(m.id_compra,''), COALESCE(m.id_venta,'') FROM movimiento_inventario m LEFT JOIN producto p ON p.id_producto=m.id_producto LEFT JOIN usuario u ON u.Dni_usu=m.Dni_usu ORDER BY m.fecha DESC, m.id_movimiento DESC",
            "columns": [("Código", 80), ("Fecha", 100), ("Producto", 170), ("Tipo", 100), ("Cantidad", 80), ("Responsable", 160), ("Motivo", 180), ("ID compra", 90), ("ID venta", 90)],
        },
        "Compras": {
            "sql": "SELECT co.id_compra AS codigo, co.fecha, COALESCE(pr.nombre_empre,'Sin proveedor') AS proveedor, COALESCE(CONCAT(u.Nombre,' ',u.apellido),'Sin usuario') AS responsable, co.total FROM compra co LEFT JOIN proveedor pr ON pr.id_provedor=co.id_provedor LEFT JOIN usuario u ON u.Dni_usu=co.Dni_usu ORDER BY co.fecha DESC, co.id_compra DESC",
            "columns": [("Código", 85), ("Fecha", 100), ("Proveedor", 190), ("Responsable", 170), ("Total", 110)],
        },
        "Ventas": {
            "sql": "SELECT v.id_venta AS codigo, v.fecha, COALESCE(CONCAT(cl.nombre,' ',cl.apellido),'Cliente no indicado') AS cliente, COALESCE(CONCAT(u.Nombre,' ',u.apellido),'Sin usuario') AS empleado, v.total, v.metodo_pago FROM venta v LEFT JOIN cliente cl ON cl.dni_client=v.dni_client LEFT JOIN usuario u ON u.Dni_usu=v.Dni_usu ORDER BY v.fecha DESC, v.id_venta DESC",
            "columns": [("Código", 85), ("Fecha", 100), ("Cliente", 180), ("Empleado", 170), ("Total", 110), ("Pago", 100)],
        },
        "Clientes": {
            "sql": "SELECT dni_client AS documento, nombre, apellido, telefono, correo, COALESCE(direccion,'') AS direccion FROM cliente ORDER BY nombre, apellido",
            "columns": [("Documento", 100), ("Nombre", 130), ("Apellido", 130), ("Teléfono", 120), ("Correo", 220), ("Dirección", 160)],
            "table": "cliente", "pk": "dni_client", "fields": [("Documento cliente", "dni_client", "required"), ("Nombre", "nombre", "required"), ("Apellido", "apellido", "required"), ("Teléfono", "telefono", "required"), ("Correo", "correo", "required"), ("Dirección", "direccion", "optional")],
        },
        "Proveedores": {
            "sql": "SELECT id_provedor AS codigo, nombre_empre, NIT, telefono, correo, COALESCE(direccion,'') AS direccion FROM proveedor ORDER BY id_provedor",
            "columns": [("Código", 85), ("Empresa", 180), ("NIT", 120), ("Teléfono", 120), ("Correo", 210), ("Dirección", 150)],
            "table": "proveedor", "pk": "id_provedor", "fields": [("ID proveedor", "id_provedor", "required"), ("Nombre empresa", "nombre_empre", "required"), ("NIT", "NIT", "required"), ("Teléfono", "telefono", "required"), ("Correo", "correo", "required"), ("Dirección", "direccion", "optional")],
        },
        "Usuarios": {
            "sql": "SELECT Dni_usu AS documento, Nombre, apellido, correo, telefono, rol FROM usuario ORDER BY Dni_usu",
            "columns": [("Documento", 95), ("Nombre", 140), ("Apellido", 140), ("Correo", 210), ("Teléfono", 120), ("Rol", 120)],
            "table": "usuario", "pk": "Dni_usu", "fields": [("Documento usuario", "Dni_usu", "required"), ("Nombre", "Nombre", "required"), ("Apellido", "apellido", "required"), ("Correo", "correo", "required"), ("Teléfono", "telefono", "required"), ("Rol", "rol", "required"), ("Contraseña", "contrasena", "required")],
        },
        "Citas ópticas": {
            "sql": "SELECT ci.id_citas AS codigo, CONCAT(COALESCE(cl.nombre,''),' ',COALESCE(cl.apellido,'')) AS cliente, ci.fecha, ci.hora, ci.motivo, ci.estado, COALESCE(CONCAT(u.Nombre,' ',u.apellido),'Sin responsable') AS responsable FROM citas_opticas ci LEFT JOIN cliente cl ON cl.dni_client=ci.dni_client LEFT JOIN usuario u ON u.Dni_usu=ci.Dni_usu ORDER BY ci.fecha, ci.hora",
            "columns": [("Código", 80), ("Cliente", 170), ("Fecha", 100), ("Hora", 85), ("Motivo", 190), ("Estado", 100), ("Responsable", 160)],
            "table": "citas_opticas", "pk": "id_citas", "fields": [("ID cita", "id_citas", "required"), ("Fecha (AAAA-MM-DD)", "fecha", "required"), ("Hora (HH:MM:SS)", "hora", "required"), ("Motivo", "motivo", "required"), ("Estado", "estado", "required"), ("Documento cliente (opcional)", "dni_client", "optional"), ("Documento usuario (opcional)", "Dni_usu", "optional")],
        },
    }

    def db_query(self, sql, params=None, fetch=True):
        if self.db_conn is None or not self.db_conn.is_connected():
            self.db_conn = mysql.connector.connect(**DB_CONFIG)
        cursor = self.db_conn.cursor()
        try:
            cursor.execute(sql, params or ())
            if fetch:
                return cursor.fetchall()
            self.db_conn.commit()
            return cursor.lastrowid
        finally:
            cursor.close()

    def render_table_module(self, module):
        config = self.DB_VIEWS.get(module)
        if not config:
            self.page_heading(module, "Este módulo todavía no tiene una tabla equivalente en la base de datos.")
            card = ctk.CTkFrame(self.page, fg_color=WHITE, corner_radius=15, border_width=1, border_color=BORDER)
            card.pack(fill="both", expand=True)
            ctk.CTkLabel(card, text="La base de datos recibida no contiene una tabla de pedidos. Los demás módulos se están conectando a las tablas existentes.", text_color=MUTED, wraplength=700).pack(pady=60, padx=25)
            return
        try:
            rows = self.db_query(config["sql"])
        except Error as exc:
            self.page_heading(module, "No se pudo consultar la tabla de MySQL.")
            messagebox.showerror("Error de consulta", f"Módulo: {module}\
\
{exc}", parent=self)
            return
        if module == "Compras":
            self.page_heading(module, "Registra una compra con sus productos; las existencias y movimientos se actualizan automáticamente.", "+ Nueva compra" if self.has_admin_permissions() else None, (lambda: self.open_transaction_form("Compras")) if self.has_admin_permissions() else None)
        elif module == "Ventas":
            self.page_heading(module, "Registra una venta; se valida el stock y se generan los movimientos de salida.", "+ Nueva venta", lambda: self.open_transaction_form("Ventas"))
        elif module == "Movimientos":
            self.page_heading(module, "Historial automático: cada compra crea entradas y cada venta crea salidas.")
        else:
            can_add = bool(config.get("table") and config.get("fields"))
            if module in {"Productos", "Categorías", "Proveedores", "Usuarios"} and not self.has_admin_permissions():
                can_add = False
            self.page_heading(module, MODULES[module][1], "+ Nuevo registro" if can_add else None, (lambda: self.open_db_form(module, config)) if can_add else None)
        toolbar = ctk.CTkFrame(self.page, fg_color=WHITE, corner_radius=12, border_width=1, border_color=BORDER)
        toolbar.pack(fill="x", pady=(0, 14))
        search = ctk.CTkEntry(toolbar, placeholder_text=f"Buscar en {module.lower()}...", height=38, width=320, corner_radius=9)
        search.pack(side="left", padx=14, pady=12)
        tree_holder = ctk.CTkFrame(self.page, fg_color=WHITE, corner_radius=12, border_width=1, border_color=BORDER)
        tree_holder.pack(fill="both", expand=True)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=WHITE, foreground=TEXT, fieldbackground=WHITE, rowheight=36, borderwidth=0, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background="#FDE3E4", foreground=NAVY, font=("Segoe UI", 10, "bold"), relief="flat", padding=10)
        columns = [c[0] for c in config["columns"]]
        tree = ttk.Treeview(tree_holder, columns=columns, show="headings")
        for col, width in config["columns"]:
            tree.heading(col, text=col)
            tree.column(col, width=width, minwidth=70, anchor="w")
        vsb = ttk.Scrollbar(tree_holder, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(tree_holder, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        tree.grid(row=0, column=0, sticky="nsew", padx=(12, 0), pady=12)
        vsb.grid(row=0, column=1, sticky="ns", pady=12, padx=(0, 12))
        hsb.grid(row=1, column=0, sticky="ew", padx=(12, 0))
        tree_holder.grid_rowconfigure(0, weight=1)
        tree_holder.grid_columnconfigure(0, weight=1)
        for row in rows:
            tree.insert("", "end", values=tuple("" if v is None else str(v) for v in row))
        ctk.CTkButton(toolbar, text="Buscar", width=90, height=38, corner_radius=9, fg_color=NAVY, hover_color="#3A3A3A", command=lambda: self.filter_table(tree, search.get())).pack(side="left", pady=12)
        if module == "Movimientos":
            movement_type = ctk.StringVar(value="Entrada (Compra)")
            ctk.CTkOptionMenu(toolbar, variable=movement_type, values=["Entrada (Compra)", "Salida (Venta)"], width=170, fg_color=GREEN, button_color=GREEN_DARK).pack(side="left", padx=(12, 4), pady=12)
            def continue_movement():
                selected_type = movement_type.get()
                if selected_type.startswith("Entrada"):
                    if not self.has_admin_permissions():
                        messagebox.showerror("Permiso denegado", "Solo Dorian o un administrador puede registrar entradas mediante compras.", parent=self)
                        return
                    self.open_transaction_form("Compras")
                else:
                    self.open_transaction_form("Ventas")
            ctk.CTkButton(toolbar, text="Continuar", width=100, height=38, fg_color=GREEN, hover_color=GREEN_DARK, command=continue_movement).pack(side="left", padx=4, pady=12)
        ctk.CTkLabel(toolbar, text=f"{len(rows)} registros reales", text_color=MUTED, font=ctk.CTkFont(size=11)).pack(side="right", padx=16)
        footer = ctk.CTkFrame(self.page, fg_color="transparent")
        footer.pack(fill="x", pady=(12, 0))
        ctk.CTkLabel(footer, text="Datos consultados directamente desde MySQL.", text_color=MUTED, font=ctk.CTkFont(size=11)).pack(side="left")
        ctk.CTkButton(footer, text="Actualizar", width=110, height=34, fg_color=WHITE, text_color=NAVY, border_width=1, border_color=BORDER, hover_color=GREEN_PALE, command=lambda: self.show_module(module)).pack(side="right", padx=(8, 0))
        if config.get("pk") and config.get("table") and config.get("fields") and (module not in {"Productos", "Categorías", "Proveedores", "Usuarios"} or self.has_admin_permissions()):
            ctk.CTkButton(footer, text="Editar seleccionado", width=155, height=34, fg_color=NAVY, text_color=WHITE, hover_color="#3A3A3A", command=lambda: self.edit_db_selected(module, config, tree)).pack(side="right", padx=(8, 0))

    def edit_db_selected(self, module, config, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Selecciona un registro", "Selecciona una fila de la tabla que deseas modificar.", parent=self)
            return
        values = tree.item(selected[0], "values")
        if not values:
            return
        primary_value = values[0]
        if module in {"Usuarios", "Proveedores", "Categorías", "Productos"} and not self.has_admin_permissions():
            messagebox.showerror("Permiso denegado", "Solo Dorian o un administrador puede editar este módulo.", parent=self)
            return
        columns = [col for _label, col, _required in config["fields"] if not (module == "Usuarios" and col == "contrasena")]
        try:
            row = self.db_query(f"SELECT {', '.join('`'+c+'`' for c in columns)} FROM `{config['table']}` WHERE `{config['pk']}`=%s", (primary_value,))
            if not row:
                messagebox.showerror("Registro no encontrado", "No se encontró el registro seleccionado en MySQL.", parent=self)
                return
            self.open_db_form(module, config, initial=dict(zip(columns, row[0])))
        except Error as exc:
            messagebox.showerror("No se pudo cargar", f"No fue posible abrir el registro para editarlo.\n\n{exc}", parent=self)

    def validate_database_value(self, column, value, label):
        numeric_integer = {
            "id_producto", "id_categoria", "id_provedor", "id_proveedor", "id_movimiento", "id_compra", "id_venta", "id_detalle", "id_citas",
            "Dni_usu", "dni_client", "telefono", "stock", "stock_minimo", "cantidad", "total"
        }
        if column in numeric_integer:
            if not re.fullmatch(r"\d+", value):
                return f"{label}: debe ser un número entero sin letras ni símbolos."
            number = int(value)
            if column in {"cantidad", "stock", "stock_minimo"} and number < 0:
                return f"{label}: no puede ser negativo."
            if column == "cantidad" and number == 0:
                return f"{label}: debe ser mayor que cero."
            if column.startswith("id_") or column in {"Dni_usu", "dni_client", "telefono"}:
                if number <= 0:
                    return f"{label}: debe ser mayor que cero."
        if column in {"precio_compra", "precio_venta", "total", "subtotal"}:
            try:
                amount = float(value.replace(",", "."))
            except ValueError:
                return f"{label}: escribe una cantidad numérica válida."
            if amount < 0:
                return f"{label}: no puede ser negativo."
            if column in {"precio_compra", "precio_venta"} and amount <= 0:
                return f"{label}: debe ser mayor que cero."
        if column in {"fecha", "fecha_vencimiento"} and value:
            try:
                datetime.strptime(value, "%Y-%m-%d")
            except ValueError:
                return f"{label}: utiliza el formato AAAA-MM-DD, por ejemplo 2026-10-16."
        if column == "hora" and value:
            try:
                datetime.strptime(value, "%H:%M:%S")
            except ValueError:
                try:
                    datetime.strptime(value, "%H:%M")
                except ValueError:
                    return f"{label}: utiliza HH:MM o HH:MM:SS."
        if column == "correo" and value and ("@" not in value or "." not in value.split("@")[-1]):
            return f"{label}: escribe un correo electrónico válido."
        if column == "rol" and value.casefold() not in {"administrador", "empleado", "enfermera", "responsable de citas", "cliente"}:
            return "Rol: elige Administrador, Empleado, Enfermera, Responsable de citas o Cliente."
        return None

    def open_db_form(self, module, config, initial=None):
        if module in {"Usuarios", "Proveedores", "Categorías", "Productos"} and not self.has_admin_permissions():
            messagebox.showerror("Permiso denegado", "Solo Dorian o un administrador puede crear o editar este módulo.", parent=self)
            return
        win = ctk.CTkToplevel(self)
        win.title(f"{'Editar registro' if initial else 'Nuevo registro'} | {module}")
        win.geometry("590x700")
        win.minsize(520, 480)
        win.configure(fg_color=BG)
        win.transient(self)
        win.grab_set()
        outer = ctk.CTkFrame(win, fg_color=WHITE, corner_radius=16, border_width=1, border_color=BORDER)
        outer.pack(fill="both", expand=True, padx=18, pady=18)
        ctk.CTkLabel(outer, text="Editar registro" if initial else "Nuevo registro", text_color=TEXT, font=ctk.CTkFont(size=22, weight="bold")).pack(anchor="w", padx=22, pady=(22, 4))
        ctk.CTkLabel(outer, text=f"Módulo: {module} · Los campos ID se ingresan manualmente", text_color=MUTED, font=ctk.CTkFont(size=11)).pack(anchor="w", padx=22, pady=(0, 14))
        scroll = ctk.CTkScrollableFrame(outer, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=22)
        entries = {}
        for label, col, required in config["fields"]:
            # Nunca mostrar la contraseña guardada; al editar solo se permite definir una nueva.
            if module == "Usuarios" and initial and col == "contrasena":
                label = "Nueva contraseña (opcional)"
                required = "optional"
            ctk.CTkLabel(scroll, text=label + (" *" if required == "required" else ""), text_color=TEXT, font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", pady=(8, 4))
            if module == "Productos" and col == "id_categoria":
                category_rows = self.db_query("SELECT id_categoria, nombre FROM categoria ORDER BY nombre")
                category_map = {f"{name} (ID {category_id})": str(category_id) for category_id, name in category_rows}
                entry = ctk.CTkComboBox(scroll, height=36, corner_radius=10, values=list(category_map.keys()), state="readonly")
                selected_label = next((display for display, category_id in category_map.items() if initial and str(initial.get(col)) == category_id), "")
                entry.set(selected_label)
                entry._category_id_map = category_map
            elif module == "Productos" and col == "id_provedor":
                provider_rows = self.db_query("SELECT id_provedor, nombre_empre FROM proveedor ORDER BY nombre_empre")
                provider_map = {f"{name} (ID {provider_id})": str(provider_id) for provider_id, name in provider_rows}
                entry = ctk.CTkComboBox(scroll, height=36, corner_radius=10, values=list(provider_map.keys()), state="readonly")
                selected_label = next((display for display, provider_id in provider_map.items() if initial and str(initial.get(col)) == provider_id), "")
                entry.set(selected_label)
                entry._category_id_map = provider_map
            else:
                entry = ctk.CTkEntry(scroll, height=36, corner_radius=10, placeholder_text=f"Ingresa {label.lower()}", show="•" if col == "contrasena" else "")
                if initial and col in initial and initial[col] is not None:
                    entry.insert(0, str(initial[col]))
            entry.pack(fill="x")
            if initial and col == config.get("pk"):
                entry.configure(state="disabled")
            entries[col] = (entry, label, required)
        buttons = ctk.CTkFrame(outer, fg_color="transparent")
        buttons.pack(fill="x", padx=22, pady=18)
        ctk.CTkButton(buttons, text="Cancelar", fg_color=WHITE, text_color=TEXT, border_width=1, border_color=BORDER, hover_color=BG, command=win.destroy).pack(side="right", padx=(8, 0))
        def save():
            cols, vals = [], []
            missing = []
            for col, (entry, label, required) in entries.items():
                if initial and col == config.get("pk"):
                    continue
                value = entry.get().strip()
                if hasattr(entry, "_category_id_map") and value:
                    value = entry._category_id_map.get(value, "")
                if required == "required" and not value:
                    missing.append(label)
                if module == "Usuarios" and initial and col == "contrasena" and not value:
                    continue
                if value:
                    validation_error = self.validate_database_value(col, value, label)
                    if validation_error:
                        messagebox.showwarning("Dato inválido", validation_error, parent=win)
                        return
                    if module == "Usuarios" and col == "contrasena":
                        if len(value) < 8:
                            messagebox.showwarning("Contraseña débil", "La contraseña debe tener al menos 8 caracteres.", parent=win)
                            return
                        value = hash_password(value)
                if col in {"precio_compra", "precio_venta", "subtotal"} and value:
                    value = value.replace(",", ".")
                cols.append(col)
                vals.append(value if value else None)
            if missing:
                messagebox.showwarning("Campos requeridos", "Completa: " + ", ".join(missing[:6]), parent=win)
                return
            if not cols:
                messagebox.showwarning("Formulario vacío", "Ingresa al menos un dato.", parent=win)
                return
            try:
                if initial:
                    assignments = ", ".join(f"`{col}`=%s" for col in cols)
                    vals.append(initial[config["pk"]])
                    sql = f"UPDATE `{config['table']}` SET {assignments} WHERE `{config['pk']}`=%s"
                    self.db_query(sql, vals, fetch=False)
                    success = "Los cambios se guardaron correctamente en MySQL."
                else:
                    placeholders = ", ".join(["%s"] * len(cols))
                    sql = f"INSERT INTO `{config['table']}` ({', '.join('`'+c+'`' for c in cols)}) VALUES ({placeholders})"
                    self.db_query(sql, vals, fetch=False)
                    success = "El registro se guardó correctamente en MySQL."
                messagebox.showinfo("Registro guardado", success, parent=win)
                win.destroy()
                self.show_module(module)
            except Error as exc:
                messagebox.showerror("No se pudo guardar", f"Revisa los IDs relacionados, los formatos de fecha y los campos obligatorios.\n\nDetalle: {exc}", parent=win)
        ctk.CTkButton(buttons, text="Guardar en MySQL", fg_color=GREEN, hover_color=GREEN_DARK, command=save).pack(side="right")

    def render_registration_requests(self):
        if not self.has_admin_permissions():
            messagebox.showerror("Permiso denegado", "Solo Dorian y los administradores pueden revisar solicitudes.", parent=self)
            return
        self.page_heading("Solicitudes de registro", "Revisa los datos y aprueba o rechaza nuevas cuentas de empleado.")
        try:
            rows = self.db_query("SELECT id_solicitud, Dni_usu, Nombre, apellido, correo, telefono, fecha_solicitud, estado FROM solicitud_de_registros WHERE estado='Pendiente' ORDER BY fecha_solicitud ASC")
        except Error as exc:
            messagebox.showerror("No se pudieron cargar las solicitudes", "Comprueba que exista la tabla solicitud_de_registros y que la migración esté aplicada.\n\n" + str(exc), parent=self)
            return
        toolbar = ctk.CTkFrame(self.page, fg_color=WHITE, corner_radius=12, border_width=1, border_color=BORDER)
        toolbar.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(toolbar, text=f"Solicitudes pendientes: {len(rows)}", text_color=TEXT, font=ctk.CTkFont(size=13, weight="bold")).pack(side="left", padx=14, pady=12)
        ctk.CTkButton(toolbar, text="Actualizar", command=lambda: self.show_module("Solicitudes de registro"), fg_color=NAVY, hover_color="#3A3A3A").pack(side="right", padx=12, pady=8)
        holder = ctk.CTkFrame(self.page, fg_color=WHITE, corner_radius=12, border_width=1, border_color=BORDER)
        holder.pack(fill="both", expand=True)
        columns = ("Solicitud", "ID usuario", "Nombre", "Correo", "Teléfono", "Fecha")
        tree = ttk.Treeview(holder, columns=columns, show="headings", height=14)
        widths = (90, 100, 200, 230, 120, 160)
        for col, width in zip(columns, widths):
            tree.heading(col, text=col)
            tree.column(col, width=width, minwidth=80, anchor="w")
        for row in rows:
            request_id, user_id, first, last, email, phone, date, _state = row
            tree.insert("", "end", iid=str(request_id), values=(request_id, user_id, f"{first} {last}", email, phone, date))
        tree.pack(fill="both", expand=True, padx=12, pady=12)
        actions = ctk.CTkFrame(self.page, fg_color="transparent")
        actions.pack(fill="x", pady=(12, 0))
        def selected_id():
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("Selecciona una solicitud", "Selecciona una solicitud de la lista.", parent=self)
                return None
            return int(sel[0])
        ctk.CTkButton(actions, text="Ver perfil", command=lambda: self.view_registration_request(selected_id()) if tree.selection() else selected_id(), fg_color=NAVY, hover_color="#3A3A3A").pack(side="left")
        ctk.CTkButton(actions, text="Rechazar", command=lambda: self.review_registration_request(selected_id(), False) if tree.selection() else selected_id(), fg_color="#B91C1C", hover_color="#991B1B").pack(side="right", padx=(8, 0))
        ctk.CTkButton(actions, text="Aprobar y crear usuario", command=lambda: self.review_registration_request(selected_id(), True) if tree.selection() else selected_id(), fg_color=GREEN, hover_color=GREEN_DARK).pack(side="right")

    def view_registration_request(self, request_id):
        if request_id is None:
            return
        try:
            rows = self.db_query("SELECT Dni_usu, Nombre, apellido, correo, telefono, foto_temporal, fecha_solicitud, estado FROM solicitud_de_registros WHERE id_solicitud=%s", (request_id,))
        except Error as exc:
            messagebox.showerror("Error", str(exc), parent=self)
            return
        if not rows:
            messagebox.showwarning("Solicitud no encontrada", "La solicitud pudo haber sido revisada por otro administrador.", parent=self)
            return
        user_id, first, last, email, phone, photo, requested_at, status = rows[0]
        win = ctk.CTkToplevel(self)
        win.title("Perfil del solicitante")
        win.geometry("500x540")
        win.transient(self)
        win.grab_set()
        card = ctk.CTkFrame(win, fg_color=WHITE, corner_radius=16)
        card.pack(fill="both", expand=True, padx=18, pady=18)
        if photo and os.path.isfile(photo):
            try:
                img = Image.open(photo)
                profile_img = ctk.CTkImage(light_image=img, dark_image=img, size=(120, 120))
                ctk.CTkLabel(card, text="", image=profile_img).pack(pady=(18, 8))
                win._profile_img = profile_img
            except Exception:
                ctk.CTkLabel(card, text="Foto no disponible", text_color=MUTED).pack(pady=18)
        else:
            ctk.CTkLabel(card, text="Sin foto de perfil", text_color=MUTED).pack(pady=18)
        ctk.CTkLabel(card, text=f"{first} {last}", font=ctk.CTkFont(size=22, weight="bold"), text_color=TEXT).pack(pady=(0, 12))
        for label, value in [("ID de usuario", user_id), ("Correo", email), ("Teléfono", phone), ("Fecha de solicitud", requested_at), ("Estado", status)]:
            ctk.CTkLabel(card, text=f"{label}: {value}", text_color=TEXT, anchor="w").pack(fill="x", padx=28, pady=4)
        ctk.CTkButton(card, text="Cerrar", command=win.destroy, fg_color=NAVY, hover_color="#3A3A3A").pack(pady=18)

    def review_registration_request(self, request_id, approve):
        if request_id is None:
            return
        if not self.has_admin_permissions():
            messagebox.showerror("Permiso denegado", "Solo un administrador puede revisar solicitudes.", parent=self)
            return
        action = "aprobar y crear esta cuenta" if approve else "rechazar esta solicitud"
        if not messagebox.askyesno("Confirmar", f"¿Deseas {action}?", parent=self):
            return
        cursor = None
        try:
            if self.db_conn is None or not self.db_conn.is_connected():
                self.db_conn = mysql.connector.connect(**DB_CONFIG)
            self.db_conn.start_transaction()
            cursor = self.db_conn.cursor()
            cursor.execute("SELECT Dni_usu, Nombre, apellido, correo, telefono, contrasena_hash, foto_temporal, estado FROM solicitud_de_registros WHERE id_solicitud=%s FOR UPDATE", (request_id,))
            row = cursor.fetchone()
            if not row or row[7] != "Pendiente":
                self.db_conn.rollback()
                messagebox.showwarning("Solicitud ya revisada", "Esta solicitud ya no está pendiente.", parent=self)
                return
            user_id, first, last, email, phone, password_hash, photo, _status = row
            if approve:
                cursor.execute("SELECT Dni_usu FROM usuario WHERE Dni_usu=%s OR LOWER(correo)=LOWER(%s) LIMIT 1", (user_id, email))
                if cursor.fetchone():
                    self.db_conn.rollback()
                    messagebox.showerror("Datos duplicados", "Ya existe una cuenta activa con ese ID o correo. La solicitud no se aprobó.", parent=self)
                    return
                cursor.execute("INSERT INTO usuario (Dni_usu, Nombre, apellido, correo, telefono, rol, contrasena) VALUES (%s,%s,%s,%s,%s,'Empleado',%s)", (user_id, first, last, email, phone, password_hash))
                cursor.execute("UPDATE solicitud_de_registros SET estado='Aprobada', revisado_por=%s, fecha_revision=NOW() WHERE id_solicitud=%s AND estado='Pendiente'", (self.current_user, request_id))
                if photo and os.path.isfile(photo):
                    ext = os.path.splitext(photo)[1].lower()
                    destination = os.path.join(PROFILE_DIR, f"profile_{user_id}{ext}")
                    try:
                        shutil.copy2(photo, destination)
                    except OSError:
                        pass
            else:
                cursor.execute("UPDATE solicitud_de_registros SET estado='Rechazada', revisado_por=%s, fecha_revision=NOW() WHERE id_solicitud=%s AND estado='Pendiente'", (self.current_user, request_id))
            self.db_conn.commit()
            messagebox.showinfo("Solicitud revisada", "Cuenta creada con rol Empleado." if approve else "La solicitud fue rechazada; no se creó una cuenta.", parent=self)
            self.show_module("Solicitudes de registro")
        except Error as exc:
            if self.db_conn:
                self.db_conn.rollback()
            messagebox.showerror("No se pudo revisar", str(exc), parent=self)
        finally:
            if cursor:
                cursor.close()

    def open_transaction_form(self, module):
        if module not in {"Compras", "Ventas"}:
            return
        if module == "Compras" and not self.has_admin_permissions():
            messagebox.showerror("Permiso denegado", "Registrar compras y aumentar existencias por compra requiere permisos de administrador.", parent=self)
            return
        is_purchase = module == "Compras"
        try:
            products = self.db_query("SELECT id_producto, nombre, precio_compra, precio_venta, COALESCE(stock,0) FROM producto ORDER BY nombre")
            providers = self.db_query("SELECT id_provedor, nombre_empre FROM proveedor ORDER BY nombre_empre") if is_purchase else []
            customers = self.db_query("SELECT dni_client, CONCAT(nombre,' ',apellido) FROM cliente ORDER BY nombre, apellido") if not is_purchase else []
        except Error as exc:
            messagebox.showerror("Error de datos", "No fue posible cargar productos, proveedores o clientes.\n\n" + str(exc), parent=self)
            return
        if not products:
            messagebox.showwarning("Sin productos", "Primero registra al menos un producto.", parent=self)
            return
        if is_purchase and not providers:
            messagebox.showwarning("Sin proveedores", "Primero registra un proveedor.", parent=self)
            return
        win = ctk.CTkToplevel(self)
        win.title("Nueva compra" if is_purchase else "Nueva venta")
        win.geometry("980x760")
        win.minsize(820, 620)
        win.configure(fg_color=BG)
        win.transient(self)
        win.grab_set()
        outer = ctk.CTkFrame(win, fg_color=WHITE, corner_radius=16, border_width=1, border_color=BORDER)
        outer.pack(fill="both", expand=True, padx=16, pady=16)
        ctk.CTkLabel(outer, text="Registrar compra" if is_purchase else "Registrar venta", text_color=TEXT, font=ctk.CTkFont(size=23, weight="bold")).pack(anchor="w", padx=20, pady=(18, 4))
        ctk.CTkLabel(outer, text=f"Fecha automática: {datetime.now().strftime('%Y-%m-%d')} · El ID lo genera MySQL al guardar.", text_color=MUTED).pack(anchor="w", padx=20, pady=(0, 10))
        meta = ctk.CTkFrame(outer, fg_color="transparent")
        meta.pack(fill="x", padx=20, pady=(0, 10))
        provider_map = {f"{name} (ID {pid})": int(pid) for pid, name in providers}
        customer_map = {f"{name} (ID {cid})": int(cid) for cid, name in customers}
        if is_purchase:
            ctk.CTkLabel(meta, text="Proveedor *", text_color=TEXT).pack(side="left", padx=(0, 8))
            party = ctk.CTkComboBox(meta, values=list(provider_map.keys()), width=340, state="readonly")
            party.pack(side="left")
            if provider_map:
                party.set(next(iter(provider_map)))
            payment = None
        else:
            ctk.CTkLabel(meta, text="Cliente (opcional)", text_color=TEXT).pack(side="left", padx=(0, 8))
            party = ctk.CTkComboBox(meta, values=["Cliente ocasional"] + list(customer_map.keys()), width=340, state="readonly")
            party.pack(side="left")
            party.set("Cliente ocasional")
            ctk.CTkLabel(meta, text="Método de pago *", text_color=TEXT).pack(side="left", padx=(14, 8))
            payment = ctk.CTkComboBox(meta, values=["Efectivo", "Tarjeta", "Transferencia", "Nequi", "Otro"], width=170, state="readonly")
            payment.pack(side="left")
            payment.set("Efectivo")
        line_header = ctk.CTkFrame(outer, fg_color=GREEN_PALE, corner_radius=8)
        line_header.pack(fill="x", padx=20, pady=(6, 0))
        for text_value, width in [("Producto (escribe para filtrar)", 410), ("Cantidad", 110), ("Precio unitario", 150)]:
            ctk.CTkLabel(line_header, text=text_value, width=width, text_color=TEXT, font=ctk.CTkFont(size=11, weight="bold")).pack(side="left", padx=6, pady=8)
        line_area = ctk.CTkScrollableFrame(outer, fg_color="transparent", height=330)
        line_area.pack(fill="both", expand=True, padx=20, pady=(0, 8))
        product_map = {}
        product_displays = []
        product_info = {}
        for pid, name, price_buy, price_sell, stock in products:
            display = f"{name} (ID {pid})"
            product_displays.append(display)
            product_map[display] = int(pid)
            product_info[display] = {"id": int(pid), "buy": Decimal(str(price_buy or 0)), "sell": Decimal(str(price_sell or 0)), "stock": int(stock or 0)}
        line_widgets = []
        def add_line():
            row_frame = ctk.CTkFrame(line_area, fg_color=WHITE, corner_radius=8, border_width=1, border_color=BORDER)
            row_frame.pack(fill="x", pady=4)
            combo = ctk.CTkComboBox(row_frame, values=product_displays, width=410, command=lambda chosen, target=None: None)
            combo.pack(side="left", padx=6, pady=7)
            combo.set("")
            qty = ctk.CTkEntry(row_frame, width=110, placeholder_text="1")
            qty.pack(side="left", padx=6, pady=7)
            qty.insert(0, "1")
            price = ctk.CTkEntry(row_frame, width=150, placeholder_text="0")
            price.pack(side="left", padx=6, pady=7)
            line = {"frame": row_frame, "combo": combo, "qty": qty, "price": price}
            def selected_product(chosen):
                if chosen in product_info:
                    price.delete(0, "end")
                    price.insert(0, str(product_info[chosen]["buy" if is_purchase else "sell"]))
                calculate_total()
            line["select_product"] = selected_product
            combo.configure(command=selected_product)
            def filter_values(_event=None):
                current = combo.get()
                needle = current.casefold().strip()
                filtered = [x for x in product_displays if needle in x.casefold()] if needle else product_displays
                combo.configure(values=filtered or product_displays)
                combo.set(current)
            combo.bind("<KeyRelease>", filter_values)
            line_widgets.append(line)
            qty.bind("<KeyRelease>", lambda _e: calculate_total())
            price.bind("<KeyRelease>", lambda _e: calculate_total())
            return line
        add_line()
        add_line()
        add_line()
        controls = ctk.CTkFrame(outer, fg_color="transparent")
        controls.pack(fill="x", padx=20, pady=4)
        ctk.CTkButton(controls, text="+ Agregar producto", command=add_line, fg_color=NAVY, hover_color="#3A3A3A", height=32).pack(side="left")
        total_label = ctk.CTkLabel(controls, text="Total: $ 0", text_color=TEXT, font=ctk.CTkFont(size=17, weight="bold"))
        total_label.pack(side="right")
        def calculate_total():
            total = Decimal("0")
            for line in line_widgets:
                display = line["combo"].get().strip()
                qty_text = line["qty"].get().strip()
                price_text = line["price"].get().strip().replace(",", ".")
                if display in product_map and qty_text.isdigit() and int(qty_text) > 0 and price_text:
                    try:
                        price_value = Decimal(price_text)
                        if price_value > 0:
                            total += price_value * int(qty_text)
                    except InvalidOperation:
                        pass
            total_label.configure(text=f"Total: $ {total.quantize(Decimal('1'), rounding=ROUND_HALF_UP):,.0f}".replace(",", "."))
        for line in line_widgets:
            line["qty"].bind("<KeyRelease>", lambda _e: calculate_total())
            line["price"].bind("<KeyRelease>", lambda _e: calculate_total())
            line["combo"].configure(command=line["select_product"])
        def save_transaction():
            selected_lines = []
            for line in line_widgets:
                display = line["combo"].get().strip()
                qty_text = line["qty"].get().strip()
                price_text = line["price"].get().strip().replace(",", ".")
                if not display and not price_text and qty_text in {"", "1"}:
                    continue
                if display not in product_map:
                    messagebox.showwarning("Producto inválido", "Selecciona un producto de la lista filtrada en cada fila utilizada.", parent=win)
                    return
                if not qty_text.isdigit() or int(qty_text) <= 0:
                    messagebox.showwarning("Cantidad inválida", "Las cantidades deben ser enteros mayores que cero.", parent=win)
                    return
                try:
                    unit_price = Decimal(price_text)
                except (InvalidOperation, ValueError):
                    messagebox.showwarning("Precio inválido", "Ingresa un precio unitario válido.", parent=win)
                    return
                if not unit_price.is_finite() or unit_price <= 0:
                    messagebox.showwarning("Precio inválido", "El precio unitario debe ser mayor que cero.", parent=win)
                    return
                selected_lines.append({"id": product_map[display], "name": display, "qty": int(qty_text), "price": unit_price})
            if not selected_lines:
                messagebox.showwarning("Sin productos", "Agrega al menos un producto válido.", parent=win)
                return
            party_id = None
            if is_purchase:
                party_id = provider_map.get(party.get())
                if not party_id:
                    messagebox.showwarning("Proveedor obligatorio", "Selecciona un proveedor.", parent=win)
                    return
            else:
                party_id = customer_map.get(party.get())
                if not payment.get().strip():
                    messagebox.showwarning("Pago obligatorio", "Selecciona el método de pago.", parent=win)
                    return
            total = sum((line["price"] * line["qty"] for line in selected_lines), Decimal("0"))
            total = total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            cursor = None
            try:
                if self.db_conn is None or not self.db_conn.is_connected():
                    self.db_conn = mysql.connector.connect(**DB_CONFIG)
                self.db_conn.start_transaction()
                cursor = self.db_conn.cursor()
                user_id = self.current_user_id if self.current_user_id else None
                if is_purchase:
                    cursor.execute("INSERT INTO compra (fecha, total, id_provedor, Dni_usu) VALUES (CURDATE(), %s, %s, %s)", (total, party_id, user_id))
                    transaction_id = cursor.lastrowid
                else:
                    cursor.execute("INSERT INTO venta (fecha, total, metodo_pago, dni_client, Dni_usu) VALUES (CURDATE(), %s, %s, %s, %s)", (total, payment.get().strip(), party_id, user_id))
                    transaction_id = cursor.lastrowid
                for line in selected_lines:
                    pid, qty, price = line["id"], line["qty"], line["price"]
                    cursor.execute("SELECT stock FROM producto WHERE id_producto=%s FOR UPDATE", (pid,))
                    stock_row = cursor.fetchone()
                    if not stock_row:
                        raise ValueError(f"El producto {line['name']} ya no existe.")
                    current_stock = int(stock_row[0] or 0)
                    if is_purchase:
                        cursor.execute("INSERT INTO detalle_compra (cantidad, precio_unitario, subtotal, id_producto, id_compra) VALUES (%s,%s,%s,%s,%s)", (qty, price, price * qty, pid, transaction_id))
                        cursor.execute("UPDATE producto SET stock=COALESCE(stock,0)+%s, precio_compra=%s WHERE id_producto=%s", (qty, price, pid))
                        cursor.execute("INSERT INTO movimiento_inventario (tipo_movimiento, cantidad, fecha, motivo, id_producto, Dni_usu, id_compra, id_venta) VALUES ('Entrada',%s,CURDATE(),%s,%s,%s,%s,NULL)", (qty, f"Compra #{transaction_id}", pid, user_id, transaction_id))
                    else:
                        cursor.execute("UPDATE producto SET stock=COALESCE(stock,0)-%s WHERE id_producto=%s AND COALESCE(stock,0)>=%s", (qty, pid, qty))
                        if cursor.rowcount != 1:
                            raise ValueError(f"Stock insuficiente para {line['name']}. Disponible: {current_stock}; solicitado: {qty}.")
                        cursor.execute("INSERT INTO detalle_venta (cantidad, precio_unitario, subtotal, id_venta, id_producto) VALUES (%s,%s,%s,%s,%s)", (qty, price, price * qty, transaction_id, pid))
                        cursor.execute("INSERT INTO movimiento_inventario (tipo_movimiento, cantidad, fecha, motivo, id_producto, Dni_usu, id_compra, id_venta) VALUES ('Salida',%s,CURDATE(),%s,%s,%s,NULL,%s)", (qty, f"Venta #{transaction_id}", pid, user_id, transaction_id))
                self.db_conn.commit()
                messagebox.showinfo("Operación completada", f"{'Compra' if is_purchase else 'Venta'} #{transaction_id} registrada. Fecha: {datetime.now().strftime('%Y-%m-%d')}. Total: $ {total:,.2f}.\nEl inventario y los movimientos se actualizaron correctamente.", parent=win)
                win.destroy()
                self.show_module(module)
            except (Error, ValueError) as exc:
                if self.db_conn:
                    self.db_conn.rollback()
                messagebox.showerror("No se pudo registrar", "No se guardó la operación; se revirtieron sus cambios para mantener la consistencia.\n\n" + str(exc), parent=win)
            finally:
                if cursor:
                    cursor.close()
        buttons = ctk.CTkFrame(outer, fg_color="transparent")
        buttons.pack(fill="x", padx=20, pady=(8, 16))
        ctk.CTkButton(buttons, text="Cancelar", command=win.destroy, fg_color=WHITE, text_color=TEXT, border_width=1, border_color=BORDER, hover_color=BG).pack(side="right", padx=(8, 0))
        ctk.CTkButton(buttons, text="Guardar compra" if is_purchase else "Guardar venta", command=save_transaction, fg_color=GREEN, hover_color=GREEN_DARK).pack(side="right")

    def render_dashboard(self):
        self.page_heading("Panel principal", f"Bienvenido, {self.current_display_name}. Resumen actualizado desde la base de datos.")
        try:
            products = self.db_query("SELECT COUNT(*) FROM producto")[0][0]
            sales = self.db_query("SELECT COALESCE(SUM(total),0) FROM venta WHERE fecha=CURDATE()")[0][0]
            low = self.db_query("SELECT COUNT(*) FROM producto WHERE stock<=COALESCE(stock_minimo,0)")[0][0]
            appointments = self.db_query("SELECT COUNT(*) FROM citas_opticas WHERE estado='Programada'")[0][0]
        except Error as exc:
            ctk.CTkLabel(self.page, text=f"No se pudieron cargar los indicadores de MySQL: {exc}", text_color=RED).pack(pady=25)
            return
        cards = ctk.CTkFrame(self.page, fg_color="transparent")
        cards.pack(fill="x", pady=(0, 18))
        stats = [("Productos registrados", str(products), "En tu base de datos", GREEN), ("Ventas de hoy", f"$ {sales:,.0f}", "Total del día", "#2766A5"), ("Stock bajo", str(low), "Requieren revisión", AMBER), ("Citas programadas", str(appointments), "Agenda óptica", "#A61F24")]
        for i, (label, value, hint, color) in enumerate(stats):
            cards.grid_columnconfigure(i, weight=1, uniform="stats")
            card = ctk.CTkFrame(cards, fg_color=WHITE, corner_radius=15, border_width=1, border_color=BORDER)
            card.grid(row=0, column=i, sticky="nsew", padx=(0 if i == 0 else 7, 0 if i == 3 else 7))
            ctk.CTkFrame(card, width=5, fg_color=color, corner_radius=3).pack(side="left", fill="y", padx=(0, 14), pady=16)
            body = ctk.CTkFrame(card, fg_color="transparent")
            body.pack(side="left", fill="both", expand=True, pady=16, padx=(0, 12))
            ctk.CTkLabel(body, text=label, text_color=MUTED, font=ctk.CTkFont(size=11)).pack(anchor="w")
            ctk.CTkLabel(body, text=value, text_color=TEXT, font=ctk.CTkFont(size=23, weight="bold")).pack(anchor="w", pady=(5, 2))
            ctk.CTkLabel(body, text=hint, text_color=color, font=ctk.CTkFont(size=10)).pack(anchor="w")
        info = ctk.CTkFrame(self.page, fg_color=WHITE, corner_radius=15, border_width=1, border_color=BORDER)
        info.pack(fill="both", expand=True, pady=(5, 0))
        ctk.CTkLabel(info, text="Conexión activa", text_color=TEXT, font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", padx=24, pady=(24, 8))
        ctk.CTkLabel(info, text="La aplicación está consultando drogueria_donmarcos. Entra a Productos, Clientes, Proveedores, Usuarios o Citas ópticas para ver registros reales.", text_color=MUTED, wraplength=850, justify="left", font=ctk.CTkFont(size=13)).pack(anchor="w", padx=24, pady=(0, 20))
        ctk.CTkButton(info, text="Ver productos", fg_color=GREEN, hover_color=GREEN_DARK, command=lambda: self.show_module("Productos")).pack(anchor="w", padx=24, pady=(0, 24))


if __name__ == "__main__":
    app = App()
    app.mainloop()
