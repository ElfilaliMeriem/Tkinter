import tkinter as tk
from tkinter import ttk, messagebox
import os
from PIL import Image, ImageTk

# --- Color Palette ---
background = "#F4E7CD"
framebg = "#3A8376"
framefg = "#FFFFFF"
framebg2 = "#F4E7CD"
framefg2 = "#E59047"
bag = "#457157"
navbar_bg = "#FFFFFF"
navbar_active_bg = framebg
navbar_active_fg = "#fff"
navbar_button_fg = framebg
navbar_fg = "#3A8376"
navbar_hover_bg = "#d5e8e1"

IMAGE_PATH = os.path.join(os.path.dirname(__file__), "images")

CURRENCY = "DH"

# ---------- Data Classes ----------
class Produit:
    def __init__(self, name, description, price, stock, image_filename, category):
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock
        self.image_filename = image_filename
        self.category = category
        self.image = None  # To hold Tkinter image (PhotoImage or ImageTk.PhotoImage)

class Client:
    def __init__(self, nom, telephone, email):
        self.nom = nom
        self.telephone = telephone
        self.email = email

class Vente:
    def __init__(self, client, items):
        self.client = client
        self.items = items

# ---------- Image Loading Utilities ----------
def load_product_image(path, size=(170, 170)):
    try:
        img = Image.open(path)
        img = img.convert("RGBA")
        img = img.resize(size, Image.LANCZOS)
        corner = 18
        mask = Image.new("L", size, 255)
        for x in range(size[0]):
            for y in range(size[1]):
                if (x < corner and y < corner and (x-corner)**2 + (y-corner)**2 > corner**2) or \
                   (x < corner and y > size[1]-corner-1 and (x-corner)**2 + (y-(size[1]-corner-1))**2 > corner**2) or \
                   (x > size[0]-corner-1 and y < corner and (x-(size[0]-corner-1))**2 + (y-corner)**2 > corner**2) or \
                   (x > size[0]-corner-1 and y > size[1]-corner-1 and (x-(size[0]-corner-1))**2 + (y-(size[1]-corner-1))**2 > corner**2):
                    mask.putpixel((x, y), 0)
        img.putalpha(mask)
        return ImageTk.PhotoImage(img)
    except Exception:
        blank = Image.new('RGBA', size, (240, 231, 205, 255))
        return ImageTk.PhotoImage(blank)

class SupermarketApp:
    def __init__(self, root):
        if not os.path.exists(IMAGE_PATH):
            os.makedirs(IMAGE_PATH)
        self.root = root
        self.root.title("Supermarché Gestion")
        self.root.geometry("1100x650")
        self.root.configure(bg=background)
        self.root.iconbitmap("images/grocery-icon-vector.ico")
        self.root.resizable(False, False)

        # Add category list
        self.categories = [
            {"label": "Épicerie",       "key": "epicerie"},
            {"label": "Vêtements",      "key": "vetements"},
            {"label": "Chaussures",     "key": "chaussures"},
            {"label": "Articles Maison","key": "maison"},
        ]
        self.products = []
        self.load_products()
        self.clients = [
            Client("Alice Martin", "0601020304", "alice@exemple.fr"),
            Client("Jean Dubois", "0604050607", "jean@exemple.fr"),
        ]
        self.sales = []
        self.cart = []
        self.current_category = self.categories[0]["key"]  # Default 'epicerie'
        self._build_ui()
        
    # ------------------- PRODUCT ARCHITECTURE METHODS ------------------------
    def load_products(self):
        self.products = [
            # --- EPICERIE ---
            {
                "name": "Pomme",
                "description": "Fruits frais rouges croquants.",
                "price": 0.5,
                "stock": 50,
                "image": "pomme.png",
                "category": "epicerie"
            },
            {
                "name": "Baguette",
                "description": "Pain artisanal du boulanger.",
                "price": 1.2,
                "stock": 35,
                "image": "baguette.png",
                "category": "epicerie"
            },
            {
                "name": "Lait",
                "description": "Lait demi-écrémé 1L.",
                "price": 0.9,
                "stock": 40,
                "image": "lait.png",
                "category": "epicerie"
            },
            {
                "name": "Bananes",
                "description": "Bananes douces importées.",
                "price": 1.8,
                "stock": 30,
                "image": "banane.png",
                "category": "epicerie"
            },
            {
                "name": "Riz",
                "description": "Sachet de 1kg de riz Thaï.",
                "price": 2.2,
                "stock": 28,
                "image": "riz.png",
                "category": "epicerie"
            },
            {
                "name": "Tomate",
                "description": "Tomates bio du maraîcher.",
                "price": 0.7,
                "stock": 42,
                "image": "tomate.png",
                "category": "epicerie"
            },
            {
                "name": "Poulet",
                "description": "Blanc de poulet frais 200g.",
                "price": 3.4,
                "stock": 17,
                "image": "poulet.png",
                "category": "epicerie"
            },
            {
                "name": "Fromage",
                "description": "Camembert 250g AOP.",
                "price": 2.5,
                "stock": 22,
                "image": "fromage.png",
                "category": "epicerie"
            },
            # --- VETEMENTS ---
            {
                "name": "Veste Classique",
                "description": "Veste élégante pour toutes saisons.",
                "price": 59.99,
                "stock": 12,
                "image": "veste.png",
                "category": "vetements"
            },
            {
                "name": "T-Shirt Blanc",
                "description": "T-shirt de base 100% coton.",
                "price": 15.99,
                "stock": 24,
                "image": "t-shirt.png",
                "category": "vetements"
            },
            {
                "name": "Jean Printemps-Automne",
                "description": "Jean bleu, coupe moderne, doux et confortable.",
                "price": 39.99,
                "stock": 14,
                "image": "pngtree-spring-and-autumn-wild-beautiful-jeans.png",
                "category": "vetements"
            },
            {
                "name": "Pantalon Sport",
                "description": "Pantalon de sport respirant.",
                "price": 24.90,
                "stock": 30,
                "image": "pantalon-sport.png",
                "category": "vetements"
            },
            {
                "name": "Chemise Laine",
                "description": "Chemise en laine chaude.",
                "price": 29.90,
                "stock": 10,
                "image": "chomise_laine.png",
                "category": "vetements"
            },
            {
                "name": "Blazer Ceinture Beige",
                "description": "Blazer beige élégant avec ceinture.",
                "price": 69.90,
                "stock": 7,
                "image": "blazer-ceinture-beige-representations.png",
                "category": "vetements"
            },
            {
                "name": "Robe Rose Élégante",
                "description": "Robe de soirée longue rose.",
                "price": 49.99,
                "stock": 8,
                "image": "robe1.png",
                "category": "vetements"
            },
            {
                "name": "Robe Fleurie Courte",
                "description": "Robe courte à motif floral.",
                "price": 34.90,
                "stock": 12,
                "image": "robe2.png",
                "category": "vetements"
            },
            {
                "name": "Robe Noire Classique",
                "description": "Petite robe noire simple et chic.",
                "price": 44.50,
                "stock": 10,
                "image": "robe3.png",
                "category": "vetements"
            },
            {
                "name": "Robe d'Été Blanche",
                "description": "Robe d'été fluide blanche.",
                "price": 37.90,
                "stock": 16,
                "image": "robe4.png",
                "category": "vetements"
            },
            {
                "name": "Robe Soirée Bleue",
                "description": "Robe bleue élégante pour soirées.",
                "price": 54.00,
                "stock": 9,
                "image": "robe5.png",
                "category": "vetements"
            },
            # --- CHAUSSURES ---
            {
                "name": "Basket Sport",
                "description": "Chaussures de sport homme.",
                "price": 54.90,
                "stock": 12,
                "image": "basket.png",
                "category": "chaussures"
            },
            {
                "name": "Sandales",
                "description": "Sandales été femme, confortables.",
                "price": 19.99,
                "stock": 25,
                "image": "sandales.png",
                "category": "chaussures"
            },
            # --- MAISON ---
            {
                "name": "Lampe LED",
                "description": "Lampe de salon économique.",
                "price": 29.99,
                "stock": 5,
                "image": "lampe.png",
                "category": "maison"
            },
            {
                "name": "Coussin Déco",
                "description": "Coussin décoratif forme étoile.",
                "price": 12.5,
                "stock": 14,
                "image": "coussin.png",
                "category": "maison"
            },
        ]

    def create_navbar(self, parent):
        if hasattr(self, "navbar_frame"):
            self.navbar_frame.destroy()
        self.navbar_frame = tk.Frame(parent, bg=navbar_bg)
        self.navbar_frame.place(x=30, y=60, width=830, height=56)

        self._navbar_buttons = {}
        btn_font = ("Arial", 13, "bold")
        btn_radius = 20
        ncat = len(self.categories)
        btn_w = 180 if ncat < 5 else int(740/ncat)
        btn_space = (830 - ncat*btn_w) // (ncat+1)
        for i, cat in enumerate(self.categories):
            cat_label = cat["label"]
            cat_key = cat["key"]
            btn = tk.Button(
                self.navbar_frame,
                text=cat_label,
                font=btn_font,
                bd=0,
                cursor="hand2",
                relief="flat",
                highlightthickness=0,
                bg=navbar_active_bg if cat_key == self.current_category else navbar_bg,
                fg=navbar_active_fg if cat_key == self.current_category else navbar_button_fg,
                activebackground=navbar_hover_bg,
                activeforeground=framebg,
                command=lambda k=cat_key: self.show_category(k),
            )
            btn.place(x=btn_space + i * (btn_w + btn_space), y=7, width=btn_w, height=38)
            btn.bind("<Enter>", lambda e, b=btn, k=cat_key: self._navbar_hover_in(e, b, k))
            btn.bind("<Leave>", lambda e, b=btn, k=cat_key: self._navbar_hover_out(e, b, k))
            self._navbar_buttons[cat_key] = btn

    def _navbar_hover_in(self, event, btn, key):
        if key == self.current_category:
            btn.config(bg=navbar_active_bg, fg=navbar_active_fg)
        else:
            btn.config(bg=navbar_hover_bg)

    def _navbar_hover_out(self, event, btn, key):
        if key == self.current_category:
            btn.config(bg=navbar_active_bg, fg=navbar_active_fg)
        else:
            btn.config(bg=navbar_bg, fg=navbar_button_fg)

    def show_category(self, category):
        if category not in [c["key"] for c in self.categories]:
            return
        self.current_category = category
        for key, btn in self._navbar_buttons.items():
            if key == category:
                btn.config(bg=navbar_active_bg, fg=navbar_active_fg)
            else:
                btn.config(bg=navbar_bg, fg=navbar_button_fg)
        self.clear_products()
        filtered = [p for p in self.products if p["category"] == category]
        self._populate_product_cards(filtered)

    def clear_products(self):
        for card in getattr(self, "pw_cards", []):
            card.destroy()
        self.pw_cards = []
        self.cards_canvas.yview_moveto(0)
        self.cards_canvas.update_idletasks()

    def create_product_card(self, parent, product):
        card_w, card_h = 250, 370
        img_size = (170, 170)

        card_container = tk.Frame(parent, bg=background, width=card_w, height=card_h)
        card = tk.Canvas(card_container, bg=background, highlightthickness=0, bd=0,
                         width=card_w, height=card_h)
        card.place(x=0, y=0, width=card_w, height=card_h)

        shadow_offset = 6
        card.create_oval(shadow_offset, card_h - 26 - shadow_offset, card_w - shadow_offset, card_h - 12 + shadow_offset,
                         fill="#e0d2ba", outline="", stipple="gray50")
        corner = 24
        card.create_rectangle(4, 4, card_w-4, card_h-4, fill=framebg2, outline=framefg2, width=2)
        card.create_oval(4, 4, 4+2*corner, 4+2*corner, fill=framebg2, outline=framefg2, width=2)
        card.create_oval(card_w-2*corner-4, 4, card_w-4, 4+2*corner, fill=framebg2, outline=framefg2, width=2)
        card.create_oval(4, card_h-2*corner-4, 4+2*corner, card_h-4, fill=framebg2, outline=framefg2, width=2)
        card.create_oval(card_w-2*corner-4, card_h-2*corner-4, card_w-4, card_h-4, fill=framebg2, outline=framefg2, width=2)

        def on_card_enter(e, c=card):
            c.configure(bg="#ede3cc")
        def on_card_leave(e, c=card):
            c.configure(bg=background)
        card.bind("<Enter>", on_card_enter)
        card.bind("<Leave>", on_card_leave)

        if not hasattr(self, "_image_cache"):
            self._image_cache = {}
        img_key = product["image"]
        if img_key not in self._image_cache:
            path = os.path.join(IMAGE_PATH, img_key)
            self._image_cache[img_key] = load_product_image(path, img_size)
        img_tk = self._image_cache[img_key]
        img_lbl = tk.Label(card_container, bg=framebg2)
        img_lbl.configure(image=img_tk)
        img_lbl.image = img_tk
        img_lbl.place(x=(card_w-img_size[0])//2, y=16, width=img_size[0], height=img_size[1])
        img_lbl.lift()

        n = tk.Label(card_container, text=product["name"], font=("Arial", 15, "bold"),
            bg=framebg2, fg=framebg, anchor="w")
        n.place(x=22, y=28+img_size[1], width=card_w-44, height=28)

        desc_txt = product["description"]
        if len(desc_txt) > 53:
            desc_txt = desc_txt[:53].rstrip() + "..."
        d = tk.Label(card_container, text=desc_txt, font=("Arial", 10),
            bg=framebg2, fg="#8b8377", anchor="nw", justify="left", wraplength=card_w-48)
        d.place(x=22, y=62+img_size[1], width=card_w-44, height=32)

        p = tk.Label(card_container, text=f"{CURRENCY} {product['price']:.2f}", font=("Arial", 13, "bold"),
            bg=framebg2, fg=framefg2, anchor="w")
        p.place(x=22, y=101+img_size[1], width=90, height=21)

        s = tk.Label(card_container, text=f"Stock: {product['stock']}", font=("Arial", 11, "bold"),
            bg=framebg2, fg="#53a85e" if product['stock'] > 7 else "#c37244", anchor="e")
        s.place(x=card_w-104, y=101+img_size[1], width=82, height=21)

        def add_to_cart(prod=product):
            if prod['stock'] == 0:
                messagebox.showwarning("Stock épuisé", "Cet article est en rupture de stock.")
                return
            prod_obj = next((p for p in self.products if p["name"] == prod["name"] and p["category"] == prod["category"]), prod)
            if any(p is prod_obj for p, _ in self.cart):
                messagebox.showinfo("Déjà ajouté", "Ce produit est déjà dans la liste de vente.")
                return
            self.cart.append((prod_obj, 1))
            self.update_cart()
            messagebox.showinfo("Ajouté", "Produit ajouté à la vente.")

        def on_btn_enter(e, btn):
            btn.configure(bg=framefg2, fg=framefg, activebackground=framebg, activeforeground=framebg2)
        def on_btn_leave(e, btn):
            btn.configure(bg=framebg, fg=framefg, activebackground=framefg2, activeforeground=framebg2)
        def on_btn_press(e, btn):
            btn.configure(bg="#2a635a")
        def on_btn_release(e, btn):
            btn.configure(bg=framefg2 if "active" in btn.state() else framebg)

        btn = tk.Button(
            card_container,
            text="Ajouter à la liste",
            font=("Arial", 12, "bold"),
            bg=framebg, fg=framefg,
            activebackground=framefg2, activeforeground=framebg2,
            bd=0, command=add_to_cart, relief="flat", cursor="hand2",
            highlightthickness=0, borderwidth=0
        )
        btn.place(x=18, y=card_h-52, width=card_w-36, height=38)

        btn.bind("<Enter>", lambda e, b=btn: on_btn_enter(e,b))
        btn.bind("<Leave>", lambda e, b=btn: on_btn_leave(e,b))
        btn.bind("<ButtonPress-1>", lambda e, b=btn: on_btn_press(e,b))
        btn.bind("<ButtonRelease-1>", lambda e, b=btn: on_btn_release(e,b))

        return card_container

    def _populate_product_cards(self, products):
        self.pw_cards = []
        columns = 3
        card_w, card_h = 250, 370
        padding_x, padding_y = 24, 28
        dx = card_w + padding_x
        dy = card_h + padding_y
        parent = self.cards_inner_frame
        for idx, prod in enumerate(products):
            x = (idx % columns) * dx
            y = (idx // columns) * dy
            card_container = self.create_product_card(parent, prod)
            card_container.place(x=x, y=y, width=card_w, height=card_h)
            self.pw_cards.append(card_container)
        total_rows = (len(products) + columns - 1) // columns
        total_height = total_rows * dy
        total_width = columns * dx
        self.cards_inner_frame.configure(width=total_width, height=total_height)
        self.cards_inner_frame.update_idletasks()
        self.cards_canvas.configure(
            scrollregion=self.cards_canvas.bbox("all")
        )

    # -----------------------------------------------------------------------

    def _build_ui(self):
        self.sidebar = tk.Frame(self.root, bg=bag)
        self.sidebar.place(x=0, y=0, width=210, height=650)

        logo = tk.Label(self.sidebar, text="MON SUPERMARCHÉ", bg=bag, fg=framefg2, font=("Arial", 13, "bold"))
        logo.place(x=15, y=25)

        self.btn_prod = tk.Button(
            self.sidebar, text="Gestion Produits", font=("Arial", 11, "bold"),
            bg=bag, fg=framefg, activebackground=framefg2, activeforeground=framebg2,
            bd=0, command=self.show_produits, relief="flat", cursor="hand2"
        )
        self.btn_prod.place(x=10, y=120, width=190, height=50)

        self.btn_cli = tk.Button(
            self.sidebar, text="Gestion Clients", font=("Arial", 13, "bold"),
            bg=bag, fg=framefg, activebackground=framefg2, activeforeground=framebg2,
            bd=0, command=self.show_clients, relief="flat", cursor="hand2"
        )
        self.btn_cli.place(x=10, y=190, width=190, height=50)

        self.btn_ventes = tk.Button(
            self.sidebar, text="Gestion Ventes", font=("Arial", 13, "bold"),
            bg=bag, fg=framefg, activebackground=framefg2, activeforeground=framebg2,
            bd=0, command=self.show_sales, relief="flat", cursor="hand2"
        )
        self.btn_ventes.place(x=10, y=260, width=190, height=50)

        self.main_area = tk.Frame(self.root, bg=background)
        self.main_area.place(x=210, y=0, width=890, height=650)

        self._init_pages()
        self.show_produits()

    def _init_pages(self):
        self.frame_produit = self._create_produit_frame(self.main_area)
        self.frame_produit.place(x=0, y=0, width=890, height=650)

        self.frame_client = self._create_client_frame(self.main_area)
        self.frame_client.place(x=0, y=0, width=890, height=650)

        self.frame_vente = self._create_vente_frame(self.main_area)
        self.frame_vente.place(x=0, y=0, width=890, height=650)

        self.frames = {
            'produit': self.frame_produit,
            'client': self.frame_client,
            'vente': self.frame_vente,
        }
        for f in self.frames.values():
            f.place_forget()

    def _create_produit_frame(self, master):
        f = tk.Frame(master, bg=background)
        titre = tk.Label(f, text="Gestion des Produits", font=("Arial", 22, "bold"),
                         bg=background, fg=framebg)
        titre.place(x=30, y=15)

        self.create_navbar(f)

        canvas_x, canvas_y = 30, 124
        canvas_w, canvas_h = 830, 470
        scrollbar_x, scrollbar_y, scrollbar_w, scrollbar_h = canvas_x+canvas_w, canvas_y, 15, canvas_h

        self.cards_canvas = tk.Canvas(f, bg=background, highlightthickness=0, bd=0)
        self.cards_canvas.place(x=canvas_x, y=canvas_y, width=canvas_w, height=canvas_h)

        self.cards_scrollbar = tk.Scrollbar(f, orient="vertical", command=self.cards_canvas.yview)
        self.cards_scrollbar.place(x=scrollbar_x, y=scrollbar_y, width=scrollbar_w, height=scrollbar_h)
        self.cards_canvas.configure(yscrollcommand=self.cards_scrollbar.set)

        self.cards_inner_frame = tk.Frame(self.cards_canvas, bg=background)
        self.cards_canvas.create_window((0, 0), window=self.cards_inner_frame, anchor="nw")

        self.cards_inner_frame.bind(
            "<Configure>",
            lambda e: self.cards_canvas.configure(scrollregion=self.cards_canvas.bbox("all"))
        )

        def _on_mousewheel(event):
            if event.delta:
                self.cards_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            elif event.num == 5:
                self.cards_canvas.yview_scroll(1, "units")
            elif event.num == 4:
                self.cards_canvas.yview_scroll(-1, "units")
        self.cards_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        self.cards_canvas.bind_all("<Button-4>", _on_mousewheel)
        self.cards_canvas.bind_all("<Button-5>", _on_mousewheel)

        self.pw_cards = []
        self.show_category(self.current_category)
        return f

    # --- CLIENT PAGE (kept unchanged) ---
    def _create_client_frame(self, master):
        f = tk.Frame(master, bg=background)
        titre = tk.Label(f, text="Gestion des Clients", font=("Arial", 22, "bold"), bg=background, fg=framebg)
        titre.place(x=30, y=20)

        tk.Label(f, text="Nom:", font=("Arial", 12), bg=background, fg=framebg).place(x=40, y=80)
        self.cl_nom_entry = tk.Entry(f, font=("Arial", 12), bg=framefg, fg=framebg, relief="groove")
        self.cl_nom_entry.place(x=160, y=80, width=220)

        tk.Label(f, text="Téléphone:", font=("Arial", 12), bg=background, fg=framebg).place(x=40, y=120)
        self.cl_tel_entry = tk.Entry(f, font=("Arial", 12), bg=framefg, fg=framebg, relief="groove")
        self.cl_tel_entry.place(x=160, y=120, width=220)

        tk.Label(f, text="Email:", font=("Arial", 12), bg=background, fg=framebg).place(x=40, y=160)
        self.cl_email_entry = tk.Entry(f, font=("Arial", 12), bg=framefg, fg=framebg, relief="groove")
        self.cl_email_entry.place(x=160, y=160, width=220)

        self.cl_add_btn = tk.Button(f, text="Ajouter", font=("Arial", 11, "bold"),
                                    bg=framebg, fg=framefg,
                                    activebackground=framefg2, activeforeground=framebg2, bd=0,
                                    command=self._cl_add_client, relief="flat", cursor="hand2")
        self.cl_add_btn.place(x=440, y=80, width=120, height=35)

        self.cl_mod_btn = tk.Button(f, text="Modifier", font=("Arial", 11, "bold"),
                                    bg=bag, fg=framefg,
                                    activebackground=framefg2, activeforeground=framebg2, bd=0,
                                    command=self._cl_modifier_client, relief="flat", cursor="hand2")
        self.cl_mod_btn.place(x=440, y=125, width=120, height=35)

        self.cl_del_btn = tk.Button(f, text="Supprimer", font=("Arial", 11, "bold"),
                                    bg=framefg2, fg=framefg,
                                    activebackground=framebg, activeforeground=framebg2, bd=0,
                                    command=self._cl_supprimer_client, relief="flat", cursor="hand2")
        self.cl_del_btn.place(x=440, y=170, width=120, height=35)

        table_x, table_y, table_w, table_h = 40, 250, 630, 260
        scrollbar_x, scrollbar_y, scrollbar_w, scrollbar_h = table_x+table_w, table_y, 16, table_h
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Treeview.Heading", background=bag, foreground=framefg, font=("Arial", 11, "bold"))
        style.configure("Treeview", background=framebg2, foreground=framebg, rowheight=30, fieldbackground=framebg2, borderwidth=0, relief="flat")

        columns = ("nom", "telephone", "email")
        self.client_table = ttk.Treeview(f, columns=columns, show="headings", height=8)
        self.client_table.heading("nom", text="Nom")
        self.client_table.heading("telephone", text="Téléphone")
        self.client_table.heading("email", text="Email")
        self.client_table.column("nom", width=200, anchor="center")
        self.client_table.column("telephone", width=150, anchor="center")
        self.client_table.column("email", width=250, anchor="center")
        self.client_table.place(x=table_x, y=table_y, width=table_w, height=table_h)

        self.client_table_scroll = tk.Scrollbar(f, orient="vertical", command=self.client_table.yview)
        self.client_table_scroll.place(x=scrollbar_x, y=scrollbar_y, width=scrollbar_w, height=scrollbar_h)
        self.client_table.configure(yscrollcommand=self.client_table_scroll.set)

        self._cl_refresh_table()
        self.client_table.bind("<<TreeviewSelect>>", self._cl_on_table_select)
        return f

    def _cl_on_table_select(self, event):
        pass

    def _cl_add_client(self):
        nom = self.cl_nom_entry.get().strip()
        tel = self.cl_tel_entry.get().strip()
        email = self.cl_email_entry.get().strip()
        if not nom or not tel or not email:
            messagebox.showwarning("Données manquantes", "Tous les champs doivent être remplis.")
            return
        self.clients.append(Client(nom, tel, email))
        self.update_clients()
        self._cl_refresh_table()
        messagebox.showinfo("Ajouté", "Client ajouté avec succès.")
        self._cl_clear_fields()

    def _cl_modifier_client(self):
        selected_items = self.client_table.selection()
        if not selected_items:
            messagebox.showwarning("Selection", "Veuillez sélectionner un client à modifier.")
            return
        item = selected_items[0]
        values = self.client_table.item(item, "values")
        if not values or len(values) != 3:
            messagebox.showwarning("Erreur", "Client introuvable.")
            return
        self.cl_nom_entry.delete(0, tk.END)
        self.cl_nom_entry.insert(0, values[0])
        self.cl_tel_entry.delete(0, tk.END)
        self.cl_tel_entry.insert(0, values[1])
        self.cl_email_entry.delete(0, tk.END)
        self.cl_email_entry.insert(0, values[2])

    def _cl_supprimer_client(self):
        selected_items = self.client_table.selection()
        if not selected_items:
            messagebox.showwarning("Selection", "Veuillez sélectionner un client à supprimer.")
            return
        confirm = messagebox.askyesno("Confirmation", "Supprimer ce client ?")
        if confirm:
            for item in selected_items:
                values = self.client_table.item(item, "values")
                if values:
                    for idx, c in enumerate(self.clients):
                        if (c.nom, c.telephone, c.email) == tuple(values):
                            del self.clients[idx]
                            break
                self.client_table.delete(item)
            self.update_clients()
            self._cl_clear_fields()

    def _cl_clear_fields(self):
        self.cl_nom_entry.delete(0, tk.END)
        self.cl_tel_entry.delete(0, tk.END)
        self.cl_email_entry.delete(0, tk.END)

    def _cl_refresh_table(self):
        for row in self.client_table.get_children():
            self.client_table.delete(row)
        for c in self.clients:
            self.client_table.insert("", "end", values=(c.nom, c.telephone, c.email))

    # --- SALES PAGE (kept unchanged) ---
    def _create_vente_frame(self, master):
        f = tk.Frame(master, bg=background)
        titre = tk.Label(f, text="Gestion des Ventes", font=("Arial", 22, "bold"),
                         bg=background, fg=framebg)
        titre.place(x=30, y=20)

        tk.Label(f, text="Client:", font=("Arial", 12), bg=background, fg=framebg).place(x=40, y=80)
        self.ve_client_cb = ttk.Combobox(f, font=("Arial", 12), state="readonly", values=[c.nom for c in self.clients])
        self.ve_client_cb.place(x=120, y=80, width=220)
        style = ttk.Style()
        style.theme_use('default')
        style.map('TCombobox',
                  fieldbackground=[('readonly', framebg2)],
                  background=[('readonly', framebg2)])
        style.configure('TCombobox', fieldbackground=framebg2, background=framebg2, foreground=framebg)

        tk.Label(f, text="Produit:", font=("Arial", 12), bg=background, fg=framebg).place(x=40, y=120)
        self.ve_prod_cb = ttk.Combobox(f, font=("Arial", 12), state="readonly", values=[p["name"] for p in self.products])
        self.ve_prod_cb.place(x=120, y=120, width=220)

        tk.Label(f, text="Quantité:", font=("Arial", 12), bg=background, fg=framebg).place(x=40, y=160)
        self.ve_qty_entry = tk.Entry(f, font=("Arial", 12), bg=framefg, fg=framebg, relief="groove")
        self.ve_qty_entry.place(x=120, y=160, width=70)

        self.ve_add_btn = tk.Button(f, text="Ajouter à la vente", font=("Arial", 11, "bold"),
                                   bg=framebg, fg=framefg, bd=0,
                                   activebackground=framefg2, activeforeground=framebg2,
                                   command=self._ve_add_to_list, relief="flat", cursor="hand2")
        self.ve_add_btn.place(x=210, y=160, width=130, height=33)

        self.ve_listbox = tk.Listbox(f, font=("Arial", 12), bg=framebg2, fg=framebg,
                                  selectbackground=framebg, selectforeground=framefg,
                                  highlightthickness=0, bd=0)
        self.ve_listbox.place(x=40, y=210, width=470, height=240)

        self.ve_total_lbl = tk.Label(f, text=f"Total: {CURRENCY} 0.00", font=("Arial", 16, "bold"),
                                    bg=background, fg=framefg2)
        self.ve_total_lbl.place(x=50, y=470)

        self.ve_confirm_btn = tk.Button(f, text="Valider la vente", font=("Arial", 13, "bold"),
                                   bg=bag, fg=framefg, bd=0, activebackground=framefg2, activeforeground=framebg2,
                                   command=self._ve_validate_sale, relief="flat", cursor="hand2")
        self.ve_confirm_btn.place(x=200, y=460, width=190, height=50)

        self._ve_refresh_listbox()
        self._ve_update_total()
        return f

    def _ve_add_to_list(self):
        idx_prod = self.ve_prod_cb.current()
        qty_txt = self.ve_qty_entry.get()
        if idx_prod == -1 or not qty_txt.isdigit():
            messagebox.showwarning("Erreur", "Veuillez sélectionner un produit et entrer une quantité valide.")
            return
        qty = int(qty_txt)
        if qty <= 0:
            messagebox.showwarning("Erreur", "Quantité invalide.")
            return
        prod = self.products[idx_prod]
        if prod['stock'] < qty:
            messagebox.showwarning("Stock insuffisant", f"Stock disponible: {prod['stock']}")
            return
        for p, q in self.cart:
            if p == prod:
                messagebox.showwarning("Déjà ajouté", "Ce produit est déjà dans la liste de vente.")
                return
        self.cart.append((prod, qty))
        self._ve_refresh_listbox()
        self._ve_update_total()
        self.ve_qty_entry.delete(0, tk.END)

    def _ve_refresh_listbox(self):
        self.ve_listbox.delete(0, tk.END)
        for prod, qty in self.cart:
            self.ve_listbox.insert(tk.END, f"{prod['name']} x {qty} @ {CURRENCY} {prod['price']:.2f} = {CURRENCY} {prod['price']*qty:.2f}")

    def _ve_update_total(self):
        total = sum(prod['price'] * qty for prod, qty in self.cart)
        self.ve_total_lbl.config(text=f"Total: {CURRENCY} {total:.2f}")

    def _ve_validate_sale(self):
        idx_client = self.ve_client_cb.current()
        if idx_client == -1 or not self.cart:
            messagebox.showwarning("Manquant", "Sélectionnez un client et ajoutez au moins un produit à la vente.")
            return
        client = self.clients[idx_client]
        for prod, qty in self.cart:
            if prod['stock'] < qty:
                messagebox.showwarning("Stock insuffisant", f"Stock épuisé pour {prod['name']}.")
                return
        for prod, qty in self.cart:
            prod['stock'] -= qty
        self.sales.append(Vente(client, list(self.cart)))
        self.update_products_from_sale()
        self.ve_client_cb.set("")
        self.ve_prod_cb.set("")
        self.ve_qty_entry.delete(0, tk.END)

    # --- NAVIGATION + DATA SYNC ---
    def update_cart(self):
        self._ve_refresh_listbox()
        self._ve_update_total()

    def update_products_from_sale(self):
        self.show_category(self.current_category)
        self.cart.clear()
        self._ve_refresh_listbox()
        self._ve_update_total()

    def update_clients(self):
        self.ve_client_cb["values"] = [c.nom for c in self.clients]
        self._ve_refresh_listbox()
        self._cl_refresh_table()

    def show_produits(self):
        for f in self.frames.values():
            f.place_forget()
        self.frame_produit.place(x=0, y=0, width=890, height=650)
        self.create_navbar(self.frame_produit)
        self.show_category(self.current_category)

    def show_clients(self):
        for f in self.frames.values():
            f.place_forget()
        self.frame_client.place(x=0, y=0, width=890, height=650)
        self._cl_refresh_table()

    def show_sales(self):
        for f in self.frames.values():
            f.place_forget()
        self.frame_vente.place(x=0, y=0, width=890, height=650)
        self.ve_client_cb["values"] = [c.nom for c in self.clients]
        self.ve_prod_cb["values"] = [p["name"] for p in self.products]
        self._ve_refresh_listbox()
        self._ve_update_total()