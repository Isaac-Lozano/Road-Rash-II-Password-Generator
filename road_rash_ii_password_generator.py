import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, Pango

class PasswordWindow(Gtk.Window):
    def __init__(self):
        self.money = 100
        self.level = 1
        self.bike = 0
        self.qual = 0

        Gtk.Window.__init__(self, title="Road Rash II Password Generator")
        self.set_border_width(10)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

        money_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)

        money_label = Gtk.Label("Money")
        self.money_entry = Gtk.Entry()
        self.money_entry.set_text("100")
        self.money_entry.connect('changed', self.money_changed)
        money_box.pack_start(money_label, True, True, 0)
        money_box.pack_start(self.money_entry, True, True, 0)
        vbox.pack_start(money_box, True, True, 0)

        level_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)

        level_label = Gtk.Label("Level")
        self.level_entry = Gtk.Entry()
        self.level_entry.set_text("1")
        self.level_entry.connect('changed', self.level_changed)
        level_box.pack_start(level_label, True, True, 0)
        level_box.pack_start(self.level_entry, True, True, 0)
        vbox.pack_start(level_box, True, True, 0)

        bike_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)

        bike_label = Gtk.Label("Bike")
        self.bike_combo = Gtk.ComboBoxText()
        self.bike_combo.append_text("Shuriken 400")
        self.bike_combo.append_text("Panda 500")
        self.bike_combo.append_text("Shuriken TT 250")
        self.bike_combo.append_text("Panda 900")
        self.bike_combo.append_text("Banzai 7.11")
        self.bike_combo.append_text("Banzai 600 N")
        self.bike_combo.append_text("Banzai 750 N")
        self.bike_combo.append_text("Shuriken 1000 N")
        self.bike_combo.append_text("Banzai 7.11 N")
        self.bike_combo.append_text("Diablo 1000 N")
        self.bike_combo.append_text("Panda 600")
        self.bike_combo.append_text("Banzai 600")
        self.bike_combo.append_text("Banzai 750")
        self.bike_combo.append_text("Shuriken 1000")
        self.bike_combo.append_text("Diablo 1000")
        self.bike_combo.append_text("Wild Thing 2000")
        self.bike_combo.set_active(0)
        self.bike_combo.connect('changed', self.aaa)
        bike_box.pack_start(bike_label, True, True, 0)
        bike_box.pack_start(self.bike_combo, True, True, 0)
        vbox.pack_start(bike_box, True, True, 0)

        vermont_button = Gtk.ToggleButton("Vermont")
        self.connect_toggle(vermont_button, 4)
        vbox.pack_start(vermont_button, True, True, 0)

        arizona_button = Gtk.ToggleButton("Arizona")
        self.connect_toggle(arizona_button, 3)
        vbox.pack_start(arizona_button, True, True, 0)

        tennesse_button = Gtk.ToggleButton("Tennesse")
        self.connect_toggle(tennesse_button, 2)
        vbox.pack_start(tennesse_button, True, True, 0)

        hawaii_button = Gtk.ToggleButton("Hawaii")
        self.connect_toggle(hawaii_button, 1)
        vbox.pack_start(hawaii_button, True, True, 0)

        alaska_button = Gtk.ToggleButton("Alaska")
        self.connect_toggle(alaska_button, 0)
        vbox.pack_start(alaska_button, True, True, 0)

        self.password_entry = Gtk.Entry()
        self.password_entry.set_text("00D8 110N")
        self.password_entry.modify_font(Pango.FontDescription("monospace"))
        self.password_entry.set_editable(False)
        vbox.pack_start(self.password_entry, True, True, 0)

        self.add(vbox)

    def money_changed(self, entry):
        amount = self.money_entry.get_text()
        amount = ''.join([i for i in amount if i in '0123456789'])
        try:
            amount = int(amount) % 65536
            self.money_entry.set_text(str(amount))
        except:
            amount = 0
            self.money_entry.set_text('')
        self.money = amount
        self.update_password()

    def level_changed(self, entry):
        amount = self.level_entry.get_text()
        amount = ''.join([i for i in amount if i in '0123456789'])
        self.level_entry.set_text(amount)
        try:
            amount = int(amount) % 8
            self.level_entry.set_text(str(amount))
        except:
            amount = 0
            self.level_entry.set_text('')
        self.level = amount
        self.update_password()

    def aaa(self, combo):
        self.bike = combo.get_active()
        self.update_password()

    def val_to_char(self, num):
        if num < 10:
            return str(num)
        else:
            return chr(ord('A') + num - 10)

    def update_password(self):
        second = (self.money + (self.money >> 4) + (self.money >> 8) + (self.money >> 12) + self.bike) & 0xF
        codearr = []
        codearr.append((((self.money >> 12) & 0xF) << 1))
        codearr.append((((self.money >> 8) & 0xF) << 1) | ((second >> 0) & 0x1))
        codearr.append((((self.money >> 4) & 0xF) << 1) | ((second >> 1) & 0x1))
        codearr.append(((self.money & 0xF) << 1) | ((second >> 2) & 0x1))
        codearr.append(self.level)
        codearr.append((self.bike << 1) | ((second >> 3) & 0x1))
        codearr.append(self.qual)
        checksum = ((codearr[0] + codearr[1] + codearr[2] +
                     codearr[3] + codearr[4] + codearr[5]) ^ codearr[6]) & 0x1F
        codearr.append(checksum)

        password = self.val_to_char(codearr[0])
        password += self.val_to_char(codearr[1])
        password += self.val_to_char(codearr[2])
        password += self.val_to_char(codearr[3]) + ' '
        password += self.val_to_char(codearr[4])
        password += self.val_to_char(codearr[5])
        password += self.val_to_char(codearr[6])
        password += self.val_to_char(codearr[7])

        self.password_entry.set_text(password)

    def connect_toggle(self, button, bit):
        def on_toggle(button):
            self.qual ^= 1 << bit
            self.update_password()
        button.connect('toggled', on_toggle)

if __name__ == "__main__":
    win = PasswordWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
