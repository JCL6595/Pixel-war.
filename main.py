from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.window import Window
import random

# =========================================
# CONFIG
# =========================================

Window.size = (720, 1280)
Window.clearcolor = (0.05, 0.05, 0.05, 1)

TAM = 52
MAPA_TAM = 60
CAMARA = 11

# =========================================
# JUEGO
# =========================================

class PixelWar(Widget):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.vida = 5
        self.monedas = 0
        self.inventario = []

        self.game_over = False

        self.player_x = MAPA_TAM // 2
        self.player_y = MAPA_TAM // 2

        # UI
        self.estado = Label(
            text="",
            font_size=24,
            bold=True,
            color=(1,1,1,1),
            size_hint=(1,None),
            pos=(0,1180)
        )

        self.add_widget(self.estado)

        # GAME OVER
        self.texto_gameover = Label(
            text="",
            font_size=60,
            bold=True,
            color=(1,0,0,1),
            center=(360,640)
        )

        self.add_widget(self.texto_gameover)

        # MAPA
        self.generar_mundo()

        # CONTROLES
        self.crear_controles()

        # DIBUJAR
        self.dibujar()

        # LOOP
        Clock.schedule_interval(
            self.mover_enemigos,
            0.4
        )

    # =========================================
    # GENERAR MUNDO
    # =========================================

    def generar_mundo(self):

        self.mapa = []

        for y in range(MAPA_TAM):

            fila = []

            for x in range(MAPA_TAM):

                if (
                    x == 0 or
                    y == 0 or
                    x == MAPA_TAM - 1 or
                    y == MAPA_TAM - 1
                ):

                    fila.append("W")

                else:

                    r = random.randint(1,100)

                    if r < 10:
                        fila.append("W")

                    elif r < 14:
                        fila.append("E")

                    elif r < 17:
                        fila.append("D")

                    elif r < 20:
                        fila.append("C")

                    elif r < 22:
                        fila.append("S")

                    elif r < 24:
                        fila.append("H")

                    else:
                        fila.append(".")

            self.mapa.append(fila)

        self.player_x = MAPA_TAM // 2
        self.player_y = MAPA_TAM // 2

        self.mapa[self.player_y][self.player_x] = "P"

        # PORTAL

        while True:

            rx = random.randint(2, MAPA_TAM-3)
            ry = random.randint(2, MAPA_TAM-3)

            if self.mapa[ry][rx] == ".":

                self.mapa[ry][rx] = "X"
                break

    # =========================================
    # DIBUJAR
    # =========================================

    def dibujar(self):

        self.canvas.before.clear()

        inicio_x = self.player_x - CAMARA // 2
        inicio_y = self.player_y - CAMARA // 2

        offset_x = 70
        offset_y = 1040

        with self.canvas.before:

            for yy in range(CAMARA):

                for xx in range(CAMARA):

                    mx = inicio_x + xx
                    my = inicio_y + yy

                    if (
                        mx < 0 or
                        my < 0 or
                        mx >= MAPA_TAM or
                        my >= MAPA_TAM
                    ):
                        continue

                    tipo = self.mapa[my][mx]

                    x = xx * TAM + offset_x
                    y = offset_y - yy * TAM

                    # =====================
                    # SUELO
                    # =====================

                    Color(0.25,0.45,0.18)

                    Rectangle(
                        pos=(x,y),
                        size=(TAM,TAM)
                    )

                    Color(0.2,0.35,0.15)

                    Rectangle(
                        pos=(x+2,y+2),
                        size=(TAM-4,TAM-4)
                    )

                    # =====================
                    # PARED
                    # =====================

                    if tipo == "W":

                        Color(0.1,0.15,0.1)

                        Rectangle(
                            pos=(x,y),
                            size=(TAM,TAM)
                        )

                    # =====================
                    # PLAYER
                    # =====================

                    elif tipo == "P":

                        # cuerpo

                        Color(0.05,0.05,0.05)

                        Rectangle(
                            pos=(x+10,y+6),
                            size=(32,38)
                        )

                        # cabeza minecraft

                        Color(1,0.85,0.78)

                        Rectangle(
                            pos=(x+12,y+30),
                            size=(28,18)
                        )

                        # pelo

                        Color(0.05,0.05,0.05)

                        Rectangle(
                            pos=(x+10,y+40),
                            size=(32,10)
                        )

                        # ojos

                        Color(1,1,1)

                        Rectangle(
                            pos=(x+18,y+34),
                            size=(4,4)
                        )

                        Rectangle(
                            pos=(x+30,y+34),
                            size=(4,4)
                        )

                        # pupilas

                        Color(0,0,0)

                        Rectangle(
                            pos=(x+19,y+34),
                            size=(2,2)
                        )

                        Rectangle(
                            pos=(x+31,y+34),
                            size=(2,2)
                        )

                        # espada espalda

                        if "Espada" in self.inventario:

                            Color(1,1,1)

                            Rectangle(
                                pos=(x+38,y+10),
                                size=(4,28)
                            )

                    # =====================
                    # ENEMIGO
                    # =====================

                    elif tipo == "E":

                        Color(0.8,0.15,0.15)

                        Rectangle(
                            pos=(x+8,y+8),
                            size=(36,36)
                        )

                        Color(1,1,1)

                        Rectangle(
                            pos=(x+16,y+24),
                            size=(5,5)
                        )

                        Rectangle(
                            pos=(x+31,y+24),
                            size=(5,5)
                        )

                    # =====================
                    # DIAMANTE
                    # =====================

                    elif tipo == "D":

                        Color(0,1,1)

                        Ellipse(
                            pos=(x+10,y+10),
                            size=(30,30)
                        )

                    # =====================
                    # MONEDA
                    # =====================

                    elif tipo == "C":

                        Color(1,0.85,0)

                        Ellipse(
                            pos=(x+12,y+12),
                            size=(26,26)
                        )

                    # =====================
                    # ESPADA
                    # =====================

                    elif tipo == "S":

                        Color(0.8,0.8,0.8)

                        Rectangle(
                            pos=(x+22,y+10),
                            size=(6,30)
                        )

                        Color(1,1,0)

                        Rectangle(
                            pos=(x+18,y+8),
                            size=(14,6)
                        )

                    # =====================
                    # VIDA
                    # =====================

                    elif tipo == "H":

                        Color(0,1,0)

                        Ellipse(
                            pos=(x+10,y+10),
                            size=(30,30)
                        )

                    # =====================
                    # PORTAL
                    # =====================

                    elif tipo == "X":

                        Color(0.7,0,1)

                        Rectangle(
                            pos=(x+8,y+8),
                            size=(36,36)
                        )

        self.estado.text = (
            f"❤️ {self.vida}     "
            f"💎 {self.inventario.count('Diamante')}     "
            f"🪙 {self.monedas}     "
            f"⚔ {'SI' if 'Espada' in self.inventario else 'NO'}"
        )

    # =========================================
    # CONTROLES
    # =========================================

    def crear_controles(self):

        size = 100

        arriba = Button(
            text="↑",
            font_size=40,
            size=(size,size),
            size_hint=(None,None),
            pos=(310,210)
        )

        abajo = Button(
            text="↓",
            font_size=40,
            size=(size,size),
            size_hint=(None,None),
            pos=(310,10)
        )

        izquierda = Button(
            text="←",
            font_size=40,
            size=(size,size),
            size_hint=(None,None),
            pos=(200,110)
        )

        derecha = Button(
            text="→",
            font_size=40,
            size=(size,size),
            size_hint=(None,None),
            pos=(420,110)
        )

        arriba.bind(
            on_press=lambda x:self.mover(0,-1)
        )

        abajo.bind(
            on_press=lambda x:self.mover(0,1)
        )

        izquierda.bind(
            on_press=lambda x:self.mover(-1,0)
        )

        derecha.bind(
            on_press=lambda x:self.mover(1,0)
        )

        self.add_widget(arriba)
        self.add_widget(abajo)
        self.add_widget(izquierda)
        self.add_widget(derecha)

    # =========================================
    # ENEMIGOS
    # =========================================

    def mover_enemigos(self, dt):

        if self.game_over:
            return

        enemigos = []

        for y in range(MAPA_TAM):

            for x in range(MAPA_TAM):

                if self.mapa[y][x] == "E":

                    enemigos.append((x,y))

        random.shuffle(enemigos)

        for ex, ey in enemigos:

            if self.mapa[ey][ex] != "E":
                continue

            dx, dy = random.choice([
                (1,0),
                (-1,0),
                (0,1),
                (0,-1)
            ])

            nx = ex + dx
            ny = ey + dy

            if (
                nx <= 0 or
                ny <= 0 or
                nx >= MAPA_TAM - 1 or
                ny >= MAPA_TAM - 1
            ):
                continue

            objetivo = self.mapa[ny][nx]

            if objetivo == "P":

                self.vida -= 1

                if self.vida <= 0:

                    self.game_over = True
                    self.texto_gameover.text = "GAME OVER"

                    return

            elif objetivo == ".":

                self.mapa[ey][ex] = "."
                self.mapa[ny][nx] = "E"

        self.dibujar()

    # =========================================
    # MOVER
    # =========================================

    def mover(self, dx, dy):

        if self.game_over:
            return

        nx = self.player_x + dx
        ny = self.player_y + dy

        tipo = self.mapa[ny][nx]

        # PARED

        if tipo == "W":
            return

        # DIAMANTE

        if tipo == "D":

            self.inventario.append("Diamante")

        # MONEDA

        if tipo == "C":

            self.monedas += 1

        # ESPADA

        if tipo == "S":

            if "Espada" not in self.inventario:

                self.inventario.append("Espada")

        # VIDA

        if tipo == "H":

            self.vida += 1

        # ENEMIGO

        if tipo == "E":

            if "Espada" in self.inventario:

                self.mapa[ny][nx] = "."

            else:

                self.vida -= 1

                if self.vida <= 0:

                    self.game_over = True
                    self.texto_gameover.text = "GAME OVER"

                    return

        # PORTAL

        if tipo == "X":

            self.generar_mundo()
            self.dibujar()
            return

        # MOVER PLAYER

        self.mapa[self.player_y][self.player_x] = "."

        self.player_x = nx
        self.player_y = ny

        self.mapa[self.player_y][self.player_x] = "P"

        self.dibujar()

# =========================================
# APP
# =========================================

class PixelWarApp(App):

    def build(self):

        return PixelWar()

# =========================================
# START
# =========================================

PixelWarApp().run()