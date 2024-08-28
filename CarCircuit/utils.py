import pygame

def ridimensiona_immagine(immagine, fattore):
    dimensioni = round(immagine.get_width() * fattore), round(immagine.get_height() * fattore)
    return pygame.transform.scale(immagine, dimensioni)

def disegna_con_rotazione(visuale, immagine, angolo_superiore_sinistro, angolo):
    immagine_ruotata = pygame.transform.rotate(immagine, angolo)
    nuovo_rettangolo = immagine_ruotata.get_rect(
        center=immagine.get_rect(topleft=angolo_superiore_sinistro).center)
    visuale.blit(immagine_ruotata, nuovo_rettangolo.topleft)

def mostra_testo_centrato(visuale, font, testo):
    renderizzato = font.render(testo, 1, (200, 200, 200))
    visuale.blit(renderizzato, (visuale.get_width()/2 - renderizzato.get_width() /
                      2, visuale.get_height()/2 - renderizzato.get_height()/2))