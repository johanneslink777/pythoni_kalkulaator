"""Prodigy — interaktiivne mootori kalkulaator. Python 3 + Tkinter."""
import math
import tkinter as tk
from tkinter import ttk
from mootorid import profiles
from arvutus import arvuta, hinnang, tooreziim

BG = '#0c1119'
PANEL = '#141d29'
INSET = '#101823'
FIELD = '#1e2c3c'
LINE = '#263446'
TEXT = '#edf3fa'
MUTED = '#9aaabd'
ACCENT = '#5fe0b6'
BLUE = '#97bfff'
FONT = 'Segoe UI'


def label(parent, text='', size=10, color=TEXT, bold=False, **kw):
    return tk.Label(parent, text=text, bg=parent.cget('bg'), fg=color,
                    font=(FONT, size, 'bold' if bold else 'normal'), **kw)


class Action(tk.Label):
    """Ühtlane tekstnupp ilma Windowsi täpilise fookusraamita."""
    def __init__(self, parent, text, command, background=FIELD):
        super().__init__(parent, text=text, bg=background, fg=TEXT,
                         font=(FONT, 10), padx=13, pady=8, bd=0,
                         cursor='hand2', takefocus=True)
        self.base = background
        self.bind('<ButtonRelease-1>', lambda e: command())
        self.bind('<Return>', lambda e: command())
        self.bind('<space>', lambda e: command())
        self.bind('<Enter>', lambda e: self.config(bg='#2a4052'))
        self.bind('<Leave>', lambda e: self.config(bg=self.base))
        self.bind('<FocusIn>', lambda e: self.config(fg=ACCENT))
        self.bind('<FocusOut>', lambda e: self.config(fg=TEXT))


class Dial(tk.Canvas):
    """Skaleeruv tahhomeeter. Lohistamine, nooled ja Home/End."""
    def __init__(self, parent, variable, low, high, step, caption, unit):
        super().__init__(parent, width=172, height=208, bg=PANEL,
                         highlightthickness=0, bd=0, takefocus=True, cursor='hand2')
        self.variable, self.low, self.high, self.step = variable, low, high, step
        self.caption, self.unit = caption, unit
        self.focused = False
        self._geometry = (86, 87, 66)
        self._last_progress = None
        variable.trace_add('write', lambda *args: self.draw())
        self.bind('<Configure>', lambda e: self.draw())
        self.bind('<ButtonPress-1>', self.begin_drag)
        self.bind('<B1-Motion>', self.drag)
        self.bind('<ButtonRelease-1>', lambda e: setattr(self, '_last_progress', None))
        for key, direction in [('Left', -1), ('Down', -1), ('Right', 1), ('Up', 1)]:
            self.bind('<'+key+'>', lambda e, d=direction: self.move(d))
        self.bind('<Home>', lambda e: self.set(self.low))
        self.bind('<End>', lambda e: self.set(self.high))
        self.bind('<FocusIn>', lambda e: self.focus(True))
        self.bind('<FocusOut>', lambda e: self.focus(False))

    def focus(self, focused):
        self.focused = focused
        self.draw()

    def set(self, value):
        value = max(self.low, min(self.high, value))
        self.variable.set(f'{value:.2f}' if self.step < 1 else str(round(value)))

    def set_limit(self, value):
        self.high = value
        self.draw()

    def move(self, direction):
        self.set(float(self.variable.get()) + direction*self.step)
        return 'break'

    def begin_drag(self, event):
        self.focus_set()
        self._last_progress = None
        self.drag(event)

    def drag(self, event):
        cx, cy, radius = self._geometry
        if math.hypot(event.x-cx, event.y-cy) < radius*.2:
            return
        angle = math.degrees(math.atan2(cy-event.y, event.x-cx))
        progress = (225-angle) % 360
        # Hoia alumises skaalavahes lähimat serva, väldi min/max hüpet.
        if progress > 270:
            if self._last_progress is not None:
                progress = 0 if self._last_progress < 135 else 270
            else:
                progress = 0 if progress > 315 else 270
        self._last_progress = progress
        raw = self.low + progress/270*(self.high-self.low)
        self.set(round(raw/self.step)*self.step)

    def draw(self):
        self.delete('all')
        try:
            value = float(self.variable.get())
        except ValueError:
            return
        width = max(self.winfo_width(), 160)
        cx, cy, radius = width/2, 83, min(width/2-14, 72)
        self._geometry = (cx, cy, radius)
        fraction = max(0, min(1, (value-self.low)/(self.high-self.low)))
        self.create_oval(cx-radius-5, cy-radius-5, cx+radius+5, cy+radius+5,
                         fill=INSET, outline=LINE, width=1)
        arc = (cx-radius, cy-radius, cx+radius, cy+radius)
        self.create_arc(*arc, start=-45, extent=270, style='arc', outline='#2a3a4e', width=5)
        if fraction > 0:
            self.create_arc(*arc, start=225, extent=-270*fraction,
                            style='arc', outline=ACCENT, width=5)
        for n in range(41):
            theta = math.radians(225-270*n/40)
            outer = radius-8
            inner = outer-(8 if n%5 == 0 else 3)
            self.create_line(cx+inner*math.cos(theta), cy-inner*math.sin(theta),
                             cx+outer*math.cos(theta), cy-outer*math.sin(theta),
                             fill='#c4d0df' if n%5 == 0 else '#52677f', width=1)
        theta = math.radians(225-270*fraction)
        length = radius*.64
        side = 2.3
        self.create_polygon(cx+side*math.sin(theta), cy+side*math.cos(theta),
                            cx+length*math.cos(theta), cy-length*math.sin(theta),
                            cx-side*math.sin(theta), cy-side*math.cos(theta),
                            fill=TEXT, outline='')
        self.create_oval(cx-5, cy-5, cx+5, cy+5, fill=ACCENT, outline=INSET, width=2)
        number = f'{value:.2f}'.rstrip('0').rstrip('.') if self.step < 1 else f'{value:,.0f}'.replace(',', ' ')
        self.create_text(cx, cy+radius*.55, text=number, fill=TEXT, font=(FONT, 19, 'bold'))
        self.create_text(cx-radius+5, cy+radius+14, text=f'{self.low:g}', fill=MUTED, font=(FONT, 8))
        self.create_text(cx+radius-5, cy+radius+14, text=f'{self.high:g}', fill=MUTED, font=(FONT, 8))
        self.create_text(cx, 184, text=self.caption, fill=ACCENT if self.focused else TEXT, font=(FONT, 10, 'bold'))
        self.create_text(cx, 202, text=self.unit, fill=MUTED, font=(FONT, 9))


class EnginePicker(tk.Frame):
    """Põhiaknasse kinnitatud valikupaneel, otsinguta."""
    def __init__(self, parent, values):
        super().__init__(parent, bg=FIELD, bd=0)
        self.values = list(values)
        self.value = tk.StringVar(value=self.values[0])
        self.popup = None
        self.outside_binding = None
        self.button = label(self, size=13, bold=True, textvariable=self.value,
                            anchor='w', padx=17, pady=16, cursor='hand2', takefocus=True)
        self.button.pack(side='left', fill='both', expand=True)
        self.arrow = label(self, '⌄', size=17, color=ACCENT, padx=17, cursor='hand2')
        self.arrow.pack(side='right', fill='y')
        for widget in (self.button, self.arrow):
            for key in ('<ButtonRelease-1>', '<Return>', '<space>', '<Down>'):
                widget.bind(key, lambda e: self.toggle())
            widget.bind('<Enter>', lambda e: self.hover(True))
            widget.bind('<Leave>', lambda e: self.hover(False))
        self.button.bind('<FocusIn>', lambda e: self.button.config(fg=ACCENT))
        self.button.bind('<FocusOut>', lambda e: self.button.config(fg=TEXT))

    def hover(self, active):
        color = '#26394c' if active else FIELD
        self.configure(bg=color)
        self.button.configure(bg=color)
        self.arrow.configure(bg=color)

    def get(self):
        return self.value.get()

    def set(self, value):
        if value not in self.values:
            raise ValueError('Tundmatu mootoriprofiil')
        self.value.set(value)

    def toggle(self):
        self.close() if self.popup is not None else self.open()
        return 'break'

    def close(self, restore_focus=True):
        if self.popup is not None:
            if self.outside_binding:
                self.winfo_toplevel().unbind('<ButtonPress-1>', self.outside_binding)
                self.outside_binding = None
            self.popup.destroy()
            self.popup = None
            self.arrow.configure(text='⌄')
            if restore_focus:
                self.button.focus_set()

    def select(self, value):
        self.set(value)
        self.close()
        self.event_generate('<<ComboboxSelected>>')

    def open(self):
        if self.popup is not None:
            return
        root = self.winfo_toplevel()
        self.update_idletasks()
        width = min(self.winfo_width(), root.winfo_width()-24)
        height = min(370, root.winfo_height()-32)
        x = min(self.winfo_rootx()-root.winfo_rootx(), root.winfo_width()-width-8)
        y = self.winfo_rooty()-root.winfo_rooty()+self.winfo_height()+5
        if y+height > root.winfo_height()-8:
            y = max(8, root.winfo_height()-height-8)
        self.popup = tk.Frame(root, bg=LINE, bd=0)
        self.popup.place(x=x, y=y, width=width, height=height)
        self.popup.lift()
        inside = tk.Frame(self.popup, bg=PANEL)
        inside.pack(fill='both', expand=True, padx=1, pady=1)
        heading = tk.Frame(inside, bg=PANEL)
        heading.pack(fill='x', padx=15, pady=10)
        label(heading, 'VALI MOOTOR', 9, MUTED, True).pack(side='left')
        label(heading, f'{len(self.values)} profiili', 9, MUTED).pack(side='right')
        self.listbox = tk.Listbox(inside, bg=PANEL, fg=TEXT, bd=0,
                                 highlightthickness=0, font=(FONT, 12),
                                 selectbackground='#204b43', selectforeground=ACCENT,
                                 activestyle='none', exportselection=False)
        scroll = ttk.Scrollbar(inside, command=self.listbox.yview, style='Prodigy.Vertical.TScrollbar')
        scroll.pack(side='right', fill='y', padx=(0,5), pady=(0,10))
        self.listbox.pack(fill='both', expand=True, padx=12, pady=(0,12))
        self.listbox.configure(yscrollcommand=scroll.set)
        for name in self.values:
            self.listbox.insert('end', '  '+name)
        index = self.values.index(self.get())
        self.listbox.selection_set(index)
        self.listbox.activate(index)
        def commit(event=None):
            selected = self.listbox.curselection()
            if selected:
                self.select(self.values[selected[0]])
            return 'break'
        self.listbox.bind('<ButtonRelease-1>', commit)
        self.listbox.bind('<Return>', commit)
        self.listbox.bind('<Escape>', lambda e: self.close())
        self.listbox.bind('<Tab>', lambda e: self.close())
        self.popup.update_idletasks()
        self.listbox.see(index)
        self.listbox.focus_set()
        self.arrow.configure(text='⌃')
        def outside(event):
            node = event.widget
            while node is not None:
                if node in (self.popup, self):
                    return
                node = getattr(node, 'master', None)
            self.close(restore_focus=False)
        self.outside_binding = root.bind('<ButtonPress-1>', outside, add='+')


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Prodigy | Mootori kalkulaator')
        self.configure(bg=BG)
        self.minsize(700, 560)
        width, height = min(1080, self.winfo_screenwidth()-80), min(850, self.winfo_screenheight()-100)
        self.geometry(f'{width}x{height}')
        self.ready = False
        self.updating = False
        self.presets, self.profile_info = profiles()
        self.mode = None
        self.scroll_visible = False
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('Prodigy.Vertical.TScrollbar', background=LINE, troughcolor=BG,
                        borderwidth=0, arrowsize=10, arrowcolor=MUTED, width=10,
                        lightcolor=BG, darkcolor=BG, bordercolor=BG, relief='flat',
                        gripcount=0)
        style.map('Prodigy.Vertical.TScrollbar', background=[('active', '#435b71')])
        self.canvas = tk.Canvas(self, bg=BG, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, command=self.canvas.yview, style='Prodigy.Vertical.TScrollbar')
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side='left', fill='both', expand=True)
        self.content = tk.Frame(self.canvas, bg=BG)
        self.content_window = self.canvas.create_window(0, 0, window=self.content, anchor='nw')
        self.canvas.bind('<Configure>', self.resize)
        self.content.bind('<Configure>', lambda e: self.refresh_scroll())
        self.bind('<MouseWheel>', self.wheel, add='+')
        self.bind('<Configure>', self.root_configured, add='+')

        header = tk.Frame(self.content, bg=BG)
        header.pack(fill='x', padx=28, pady=(24, 16))
        brand = tk.Frame(header, bg=BG)
        brand.pack(fill='x')
        logo = tk.Canvas(brand, width=32, height=30, bg=BG, highlightthickness=0)
        logo.pack(side='left', padx=(0,10))
        logo.create_polygon(3,26,11,4,29,4,24,15,14,15,10,26, fill=ACCENT, outline='')
        logo.create_polygon(14,8,12,12,22,12,24,8, fill=BG, outline='')
        label(brand, 'P R O D I G Y', 11, TEXT, True).pack(side='left')
        label(brand, 'MOOTORI KALKULAATOR', 9, MUTED).pack(side='right')
        label(header, 'Mootori jõud arvudes.', 28, TEXT, True).pack(anchor='w', pady=(18,3))
        label(header, 'Vali mootor ja kujunda selle töörežiim.', 11, MUTED).pack(anchor='w')

        selector = tk.Frame(self.content, bg=BG)
        selector.pack(fill='x', padx=28, pady=(0,18))
        topline = tk.Frame(selector, bg=BG)
        topline.pack(fill='x', pady=(0,8))
        label(topline, '01  /  MOOTOR', 9, MUTED, True).pack(side='left')
        self.profile_count = label(topline, f'{len(self.presets)} profiili', 9, MUTED)
        self.profile_count.pack(side='right')
        self.choice = EnginePicker(selector, list(self.presets))
        self.choice.pack(fill='x')
        self.choice.bind('<<ComboboxSelected>>', lambda e: self.preset())
        self.choice.set('2.0L R6 Bensiin' if '2.0L R6 Bensiin' in self.presets else next(iter(self.presets)))

        self.body = tk.Frame(self.content, bg=BG)
        self.body.pack(fill='x', padx=28)
        self.controls = tk.Frame(self.body, bg=PANEL, padx=18, pady=18)
        self.results = tk.Frame(self.body, bg=BG)
        heading = tk.Frame(self.controls, bg=PANEL)
        heading.pack(fill='x')
        left = tk.Frame(heading, bg=PANEL)
        left.pack(side='left')
        label(left, '02  /  TÖÖREŽIIM', 9, MUTED, True).pack(anchor='w')
        self.modified = label(left, 'Profiili algväärtused', 9, MUTED)
        self.modified.pack(anchor='w', pady=(5,0))
        self.reset = Action(heading, 'Lähtesta', self.preset)
        self.reset.pack(side='right')
        label(self.controls, 'Lohista osutit või kasuta nooleklahve.', 9, MUTED).pack(anchor='w', pady=(14,8))
        gauge_row = tk.Frame(self.controls, bg=PANEL)
        gauge_row.pack(fill='x')
        self.variables = [tk.StringVar(value='2.0'), tk.StringVar(value='3000'), tk.StringVar(value='20')]
        self.sliders = []
        for i, (lo, hi, step, title, unit) in enumerate([
            (.5,10,.01,'Kubatuur','liitrit'), (600,7500,50,'Pöörded','p/min'),
            (-20,100,1,'Sisselaskeõhk','°C')]):
            gauge_row.columnconfigure(i, weight=1, uniform='gauges')
            dial = Dial(gauge_row, self.variables[i], lo, hi, step, title, unit)
            dial.grid(row=0, column=i, sticky='ew')
            self.sliders.append(dial)
        tk.Frame(self.controls, bg=LINE, height=1).pack(fill='x', pady=(16,13))
        summary_header = tk.Frame(self.controls, bg=PANEL)
        summary_header.pack(fill='x', pady=(0,8))
        label(summary_header, 'ÕHK JA KÜTUS', 9, MUTED, True).pack(side='left')
        label(summary_header, '●  Automaatne', 9, ACCENT).pack(side='right')
        self.fuel = tk.StringVar(value='—')
        self.air_flow = tk.StringVar(value='—')
        self.air_need = tk.StringVar(value='—')
        for title, var, unit in [('Kütusekogus',self.fuel,'g/min'), ('Õhuvool',self.air_flow,'kg/min'), ('Vajalik õhk',self.air_need,'kg/min')]:
            row = tk.Frame(self.controls, bg=PANEL)
            row.pack(fill='x', pady=4)
            label(row,title,10,MUTED).pack(side='left')
            label(row,unit,9,MUTED,width=6,anchor='e').pack(side='right')
            label(row,size=12,color=ACCENT,bold=True,textvariable=var).pack(side='right',padx=(0,8))

        self.power_card, self.power = self.result_card('VÕIMSUS', 'kW', ACCENT)
        self.torque_card, self.torque = self.result_card('VÄÄNDEMOMENT', 'Nm', BLUE)
        self.status = label(self.content, '●  Kütus ja õhk on tasakaalus', 9, MUTED, anchor='w')
        self.status.pack(fill='x', padx=30, pady=(16,18))
        for var in self.variables:
            var.trace_add('write', lambda *a: self.update_results())
        self.ready = True
        self.preset()
        self.bind('<Escape>', lambda e: self.choice.close())

    def result_card(self, title, unit, color):
        card = tk.Frame(self.results, bg=PANEL, padx=24, pady=22)
        label(card, '03  /  TULEMUS' if unit == 'kW' else 'VALITUD PÖÖRETEL',9,MUTED,True).pack(anchor='w')
        label(card,f'{title} · {unit}',10,TEXT,True).pack(anchor='w',pady=(20,8))
        # Fikseeritud mõõduga numbriala ei muuda kaardi suurust arvu kasvades.
        number_row = tk.Frame(card, bg=PANEL, width=240, height=72)
        number_row.pack(fill='x')
        number_row.pack_propagate(False)
        value = label(number_row, '—', 32, color, True, anchor='w')
        value.place(x=0, y=0, relwidth=1, relheight=1)
        label(card,'Arvutuslik hinnang',9,MUTED).pack(anchor='w',pady=(8,0))
        return card,value

    def root_configured(self, event):
        if event.widget is self and hasattr(self,'choice'):
            self.choice.close(restore_focus=False)

    def resize(self, event):
        width = min(event.width, 1220)
        self.canvas.itemconfigure(self.content_window, width=width)
        self.canvas.coords(self.content_window,max(0,(event.width-width)/2),0)
        if hasattr(self,'controls'):
            mode = 'wide' if width >= 1000 else 'compact'
            if mode != self.mode:
                self.mode = mode
                self.controls.grid_forget()
                self.results.grid_forget()
                self.power_card.grid_forget()
                self.torque_card.grid_forget()
                self.body.columnconfigure(0,weight=1)
                self.body.columnconfigure(1,weight=0)
                if mode == 'wide':
                    self.controls.grid(row=0,column=0,sticky='nsew',padx=(0,16))
                    self.results.grid(row=0,column=1,sticky='nsew')
                    self.results.columnconfigure(0,weight=1,uniform='')
                    self.results.columnconfigure(1,weight=0,uniform='')
                    self.power_card.grid(row=0,column=0,sticky='nsew',pady=(0,12))
                    self.torque_card.grid(row=1,column=0,sticky='nsew')
                else:
                    self.controls.grid(row=0,column=0,sticky='ew',columnspan=2)
                    self.results.grid(row=1,column=0,sticky='ew',columnspan=2,pady=(14,0))
                    self.results.columnconfigure(0,weight=1,uniform='result')
                    self.results.columnconfigure(1,weight=1,uniform='result')
                    self.power_card.grid(row=0,column=0,sticky='nsew',padx=(0,7))
                    self.torque_card.grid(row=0,column=1,sticky='nsew',padx=(7,0))
        self.after_idle(self.refresh_scroll)

    def refresh_scroll(self):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
        needed = self.content.winfo_reqheight() > self.canvas.winfo_height()+2
        if needed != self.scroll_visible:
            self.scroll_visible = needed
            if needed:
                self.scrollbar.pack(side='right',fill='y')
            else:
                self.scrollbar.pack_forget()
                self.canvas.yview_moveto(0)

    def wheel(self,event):
        if self.choice.popup is not None:
            return
        if self.scroll_visible:
            self.canvas.yview_scroll(-int(event.delta/120),'units')

    def preset(self):
        self.choice.close(restore_focus=False)
        base = self.presets[self.choice.get()]
        self.updating = True
        try:
            self.sliders[1].set_limit(5000 if 'Diisel' in self.choice.get() else 7500)
            for var,index in zip(self.variables,(0,1,3)):
                var.set(str(base[index]))
        finally:
            self.updating = False
        self.update_results()

    def update_results(self):
        if not self.ready or self.updating:
            return
        try:
            base = self.presets[self.choice.get()]
            values = list(base)
            for var,index in zip(self.variables,(0,1,3)):
                values[index] = float(var.get())
            diesel = 'Diisel' in self.choice.get()
            values[2],values[4] = tooreziim(base,values[1],diesel)
            values[5] = arvuta(*values)[3]
            _,mass,need,fuel = arvuta(*values)
            kw,nm = hinnang(values[5],fuel,values[1],diesel)
            self.fuel.set(f'{values[5]:.1f}')
            self.air_flow.set(f'{mass/1000:.2f}')
            self.air_need.set(f'{need/1000:.2f}')
            self.power.configure(text=f'≈ {kw:.0f}')
            self.torque.configure(text=f'≈ {nm:.0f}')
            modified = any(not math.isclose(values[i],base[i]) for i in (0,1,3))
            self.modified.configure(text='Kohandatud töörežiim' if modified else 'Profiili algväärtused',fg=ACCENT if modified else MUTED)
            self.status.configure(text='●  Kütus ja õhk on tasakaalus',fg=MUTED)
        except (ValueError,OverflowError,ZeroDivisionError):
            for var in (self.fuel,self.air_flow,self.air_need):
                var.set('—')
            self.power.configure(text='—')
            self.torque.configure(text='—')
            self.status.configure(text='Kontrolli töörežiimi väärtusi.',fg='#f4b48a')


if __name__ == '__main__':
    App().mainloop()

