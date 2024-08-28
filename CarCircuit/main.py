import pygame
import time
import math
from utils import scala_immagine, centra_rotazione_e_blit

ERBA = scala_immagine(pygame.image.load("imgs/terreno.jpg"), 2.5)
PISTA = scala_immagine(pygame.image.load("imgs/strada.png"), 0.9)

CONFINE_PISTA = scala_immagine(pygame.image.load("imgs/strada-bordo.png"), 0.9)

AUTO_ROSSA = scala_immagine(pygame.image.load("imgs/macchina_rossa.png"), 0.55)
AUTO_VERDE = scala_immagine(pygame.image.load("imgs/macchina_verde.png"), 0.55)

LARGHEZZA, ALTEZZA = PISTA.get_width(), PISTA.get_height()
FINESTRA = pygame.display.set_mode((LARGHEZZA, ALTEZZA))
pygame.display.set_caption("Gioco di Corse!")
FONT_PRINCIPALE = pygame.font.SysFont("comicsans", 44)

FREQUENZA_FPS = 60
PERCORSO = [(175, 119), (110, 70), (56, 133), (70, 481), (318, 731), (404, 680), (418, 521), (507, 475), (600, 551), (613, 715), (736, 713),
            (734, 399), (611, 357), (409, 343), (433, 257), (697, 258), (738, 123), (581, 71), (303, 78), (275, 377), (176, 388), (178, 260)]


class InfoGioco:
    LIVELLI = 10

    def __init__(self, livello=1):
        self.livello = livello
        self.iniziato = False
        self.tempo_inizio_livello = 0

    def prossimo_livello(self):
        self.livello += 1
        self.iniziato = False

    def resetta(self):
        self.livello = 1
        self.iniziato = False
        self.tempo_inizio_livello = 0

    def gioco_completato(self):
        return self.livello > self.LIVELLI

    def inizia_livello(self):
        self.iniziato = True
        self.tempo_inizio_livello = time.time()

    def ottieni_tempo_livello(self):
        if not self.iniziato:
            return 0
        return round(time.time() - self.tempo_inizio_livello)


class AutoGenerica:
    def __init__(self, velocita_massima, velocita_rotazione):
        self.immagine = self.IMMAGINE
        self.velocita_massima = velocita_massima
        self.velocita = 0
        self.velocita_rotazione = velocita_rotazione
        self.angolo = 0
        self.posizione_x, self.posizione_y = self.POSIZIONE_INIZIALE
        self.accelerazione = 0.1

    def ruota(self, sinistra=False, destra=False):
        if sinistra:
            self.angolo += self.velocita_rotazione
        elif destra:
            self.angolo -= self.velocita_rotazione

    def disegna(self, finestra):
        disegna_con_rotazione(finestra, self.immagine, (self.posizione_x, self.posizione_y), self.angolo)

    def muovi_avanti(self):
        self.velocita = min(self.velocita + self.accelerazione, self.velocita_massima)
        self.muovi()

    def muovi_indietro(self):
        self.velocita = max(self.velocita - self.accelerazione, -self.velocita_massima/2)
        self.muovi()

    def muovi(self):
        radianti = math.radians(self.angolo)
        verticale = math.cos(radianti) * self.velocita
        orizzontale = math.sin(radianti) * self.velocita

        self.posizione_y -= verticale
        self.posizione_x -= orizzontale

    def collisione(self, maschera, x=0, y=0):
        maschera_auto = pygame.mask.from_surface(self.immagine)
        offset = (int(self.posizione_x - x), int(self.posizione_y - y))
        punto_collisione = maschera.overlap(maschera_auto, offset)
        return punto_collisione

    def resetta(self):
        self.posizione_x, self.posizione_y = self.POSIZIONE_INIZIALE
        self.angolo = 0
        self.velocita = 0


class AutoGiocatore(AutoGenerica):
    IMMAGINE = AUTO_ROSSA
    POSIZIONE_INIZIALE = (180, 200)

    def riduci_velocita(self):
        self.velocita = max(self.velocita - self.accelerazione / 2, 0)
        self.muovi()

    def rimbalza(self):
        self.velocita = -self.velocita
        self.muovi()


class AutoComputer(AutoGenerica):
    IMMAGINE = AUTO_VERDE
    POSIZIONE_INIZIALE = (150, 200)

    def __init__(self, velocita_massima, velocita_rotazione, percorso=[]):
        super().__init__(velocita_massima, velocita_rotazione)
        self.percorso = percorso
        self.punto_corrente = 0
        self.velocita = velocita_massima

    def disegna_punti(self, finestra):
        for punto in self.percorso:
            pygame.draw.circle(finestra, (255, 0, 0), punto, 5)

    def disegna(self, finestra):
        super().disegna(finestra)
        # self.disegna_punti(finestra)

    def calcola_angolo(self):
        x_obiettivo, y_obiettivo = self.percorso[self.punto_corrente]
        differenza_x = x_obiettivo - self.posizione_x
        differenza_y = y_obiettivo - self.posizione_y
