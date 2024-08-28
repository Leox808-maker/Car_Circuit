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

        if differenza_y == 0:
            angolo_radiante = math.pi / 2
        else:
            angolo_radiante = math.atan(differenza_x / differenza_y)

        if y_obiettivo > self.posizione_y:
            angolo_radiante += math.pi

        differenza_angolo = self.angolo - math.degrees(angolo_radiante)
        if differenza_angolo >= 180:
            differenza_angolo -= 360

        if differenza_angolo > 0:
            self.angolo -= min(self.velocita_rotazione, abs(differenza_angolo))
        else:
            self.angolo += min(self.velocita_rotazione, abs(differenza_angolo))

    def aggiorna_punto_percorso(self):
        obiettivo = self.percorso[self.punto_corrente]
        rettangolo_auto = pygame.Rect(
            self.posizione_x, self.posizione_y, self.immagine.get_width(), self.immagine.get_height())
        if rettangolo_auto.collidepoint(*obiettivo):
            self.punto_corrente += 1

    def muovi(self):
        if self.punto_corrente >= len(self.percorso):
            return

        self.calcola_angolo()
        self.aggiorna_punto_percorso()
        super().muovi()

    def prossimo_livello(self, livello):
        self.resetta()
        self.velocita = self.velocita_massima + (livello - 1) * 0.2
        self.punto_corrente = 0

    def disegna(finestra, immagini, auto_giocatore, auto_computer, info_gioco):
        for immagine, posizione in immagini:
            finestra.blit(immagine, posizione)

        testo_livello = FONT_PRINCIPALE.render(
            f"Livello {info_gioco.livello}", 1, (255, 255, 255))
        finestra.blit(testo_livello, (10, ALTEZZA - testo_livello.get_height() - 70))

        testo_tempo = FONT_PRINCIPALE.render(
            f"Tempo: {info_gioco.ottieni_tempo_livello()}s", 1, (255, 255, 255))
        finestra.blit(testo_tempo, (10, ALTEZZA - testo_tempo.get_height() - 40))

        testo_velocita = FONT_PRINCIPALE.render(
            f"Velocità: {round(auto_giocatore.velocita, 1)}px/s", 1, (255, 255, 255))
        finestra.blit(testo_velocita, (10, ALTEZZA - testo_velocita.get_height() - 10))

        auto_giocatore.disegna(finestra)
        auto_computer.disegna(finestra)
        pygame.display.update()

    def muovi_giocatore(auto_giocatore):
        tasti = pygame.key.get_pressed()
        mosso = False

        if tasti[pygame.K_a]:
            auto_giocatore.ruota(sinistra=True)
        if tasti[pygame.K_d]:
            auto_giocatore.ruota(destra=True)
        if tasti[pygame.K_w]:
            mosso = True
            auto_giocatore.muovi_avanti()
        if tasti[pygame.K_s]:
            mosso = True
            auto_giocatore.muovi_indietro()

        if not mosso:
            auto_giocatore.riduci_velocita()

    def gestisci_collisione(auto_giocatore, auto_computer, info_gioco):
        if auto_giocatore.collisione(BORDO_PISTA_MASK) != None:
            auto_giocatore.rimbalza()

        auto_computer_traguardo = auto_computer.collisione(
            TRAGUARDO_MASK, *POSIZIONE_TRAGUARDO)
        if auto_computer_traguardo != None:
            mostra_testo_centrato(FINESTRA, FONT_PRINCIPALE, "Hai perso!")
            pygame.display.update()
            pygame.time.wait(5000)
            info_gioco.resetta()
            auto_giocatore.resetta()
            auto_computer.resetta()

        auto_giocatore_traguardo = auto_giocatore.collisione(
            TRAGUARDO_MASK, *POSIZIONE_TRAGUARDO)
        if auto_giocatore_traguardo != None:
            if auto_giocatore_traguardo[1] == 0:
                auto_giocatore.rimbalza()
            else:
                info_gioco.prossimo_livello()
                auto_giocatore.resetta()
                auto_computer.prossimo_livello(info_gioco.livello)

    esegui = True
    orologio = pygame.time.Clock()
    immagini = [(ERBA, (0, 0)), (PISTA, (0, 0)),
                (TRAGUARDO, POSIZIONE_TRAGUARDO), (BORDO_PISTA, (0, 0))]
    auto_giocatore = AutoGiocatore(4, 4)
    auto_computer = AutoComputer(2, 4, PERCORSO)
    info_gioco = InfoGioco()


while esegui:
    orologio.tick(FREQUENZA_FPS)

    disegna(FINESTRA, immagini, auto_giocatore, auto_computer, info_gioco)

    while not info_gioco.iniziato:
        mostra_testo_centrato(
            FINESTRA, FONT_PRINCIPALE, f"Premi un tasto per iniziare il livello {info_gioco.livello}!")
        pygame.display.update()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                break

            if evento.type == pygame.KEYDOWN:
                info_gioco.inizia_livello()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            esegui = False
            break

    muovi_giocatore(auto_giocatore)
    auto_computer.muovi()

    gestisci_collisione(auto_giocatore, auto_computer, info_gioco)

    if info_gioco.gioco_completato():
        mostra_testo_centrato(FINESTRA, FONT_PRINCIPALE, "Hai vinto il gioco!")
        pygame.time.wait(5000)
        info_gioco.resetta()
        auto_giocatore.resetta()
        auto_computer.resetta()


pygame.quit()