import multiprocessing
import random
import time

# Variável global para o semáforo
semaforo = None


def init(sem):
    """Função de inicialização do Pool para injetar o semáforo globalmente"""
    global semaforo
    semaforo = sem


def carro_cruzamento(dados):
    global semaforo
    id_carro, sentido = dados

    print(
        f"Carro #{id_carro} chegou ao cruzamento querendo ir no sentido: {sentido}"
    )

    # Início da seção crítica (apenas 1 carro por vez passa no cruzamento)
    with semaforo:
        print(f"==> Carro #{id_carro} ESTÁ PASSANDO no sentido: {sentido}")
        time.sleep(random.uniform(1.0, 2.0))  # Simula o tempo atravessando
        print(f"<== Carro #{id_carro} JÁ PASSOU o cruzamento no sentido: {sentido}")


def main():
    sentidos = ["Norte-Sul", "Sul-Norte", "Leste-Oeste", "Oeste-Leste"]
    parametros = []

    # Criando os dados para 8 carros (ID e sentido)
    for i in range(1, 9):
        sentido_escolhido = random.choice(sentidos)
        parametros.append((i, sentido_escolhido))

    with multiprocessing.Manager() as gerenciador:
        # Cria o semáforo permitindo apenas 1 processo por vez na seção crítica
        sem = gerenciador.Semaphore(1)

        # Inicializa o Pool passando o semáforo através da função init
        with multiprocessing.Pool(
            processes=4, initializer=init, initargs=(sem,)
        ) as pool:
            pool.map(carro_cruzamento, parametros)

    print("\nFim do fluxo do cruzamento!")


if __name__ == "__main__":
    main()
