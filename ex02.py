import multiprocessing
import random
import time

semaforo = None


def pessoa_caminhando(id, sem):
    distancia_total = 200  # metros
    distancia_percorrida = 0
    velocidade = random.randint(4, 6)  # 4 a 6 m/s

    print(f"Pessoa #{id} começou a correr pelo corredor.")

    while distancia_percorrida < distancia_total:
        distancia_percorrida += velocidade
        if distancia_percorrida > distancia_total:
            distancia_percorrida = distancia_total
        print(f"Pessoa #{id} percorreu {distancia_percorrida}m de {distancia_total}m.")
        time.sleep(1)

    print(f"Pessoa #{id} chegou à porta e quer abrir/cruzar.")

    # Seção crítica: apenas 1 pessoa cruza a porta por vez
    with sem:
        tempo_porta = random.uniform(1.0, 2.0)  # 1 a 2 segundos para abrir e cruzar
        print(f"---> Pessoa #{id} está abrindo a porta e cruzando...")
        time.sleep(tempo_porta)
        print(f"<--- Pessoa #{id} CONSEGUIU cruzar a porta!")


def main():
    sem = None

    with multiprocessing.Manager() as gerenciador:
        sem = gerenciador.Semaphore(1)  # Apenas 1 pessoa por vez na porta

        processos = []
        for i in range(1, 5):  # 4 pessoas
            p = multiprocessing.Process(
                target=pessoa_caminhando, args=(i, sem)
            )
            processos.append(p)
            p.start()

        for p in processos:
            p.join()


if __name__ == "__main__":
    main()