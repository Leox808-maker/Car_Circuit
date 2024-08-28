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

FPS = 60


class VeicoloBase:
    def __init__(self, velocità_massima, velocità_rotazione):
        self.immagine = self.IMMAGINE
        self.velocità_massima = velocità_massima
        self.velocità_attuale = 0
        self.velocità_rotazione = velocità_rotazione
        self.angolo = 0
        self.posizione_x, self.posizione_y = self.POSIZIONE_INIZIALE
        self.accelerazione = 0.1

    def ruota(self, sinistra=False, destra=False):
        if sinistra:
            self.angolo += self.velocità_rotazione
        elif destra:
            self.angolo -= self.velocità_rotazione

    def disegna(self, finestra):
        centra_rotazione_e_blit(finestra, self.immagine, (self.posizione_x, self.posizione_y), self.angolo)

    def avanza(self):
        self.velocità_attuale = min(self.velocità_attuale + self.accelerazione, self.velocità_massima)
        self.muovi()

    def muovi(self):
        radiani = math.radians(self.angolo)
        verticale = math.cos(radiani) * self.velocità_attuale
        orizzontale = math.sin(radiani) * self.velocità_attuale

        self.posizione_y -= verticale
        self.posizione_x -= orizzontale

    def rallenta(self):
        self.velocità_attuale = max(self.velocità_attuale - self.accelerazione / 2, 0)
        self.muovi()


class AutoGiocatore(VeicoloBase):
    IMMAGINE = AUTO_ROSSA
    POSIZIONE_INIZIALE = (180, 200)


def aggiorna_schermo(finestra, immagini, auto_giocatore):
    for immagine, posizione in immagini:
        finestra.blit(immagine, posizione)

    auto_giocatore.disegna(finestra)
    pygame.display.update()


gioco_in_corso = True
orologio = pygame.time.Clock()
immagini = [(ERBA, (0, 0)), (PISTA, (0, 0))]
auto_giocatore = AutoGiocatore(4, 4)

while gioco_in_corso:
    orologio.tick(FPS)

    aggiorna_schermo(FINESTRA, immagini, auto_giocatore)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            gioco_in_corso = False
            break

    tasti_premuti = pygame.key.get_pressed()
    mosso = False

    if tasti_premuti[pygame.K_a]:
        auto_giocatore.ruota(sinistra=True)
    if tasti_premuti[pygame.K_d]:
        auto_giocatore.ruota(destra=True)
    if tasti_premuti[pygame.K_w]:
        mosso = True
        auto_giocatore.avanza()

    if not mosso:
        auto_giocatore.rallenta()


pygame.quit()