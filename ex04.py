import multiprocessing
import random
import time

# Variáveis globais
controle_pista = None
lock_equipes = None


def init(sem_pista, lks_equipes):
    global controle_pista, lock_equipes
    controle_pista = sem_pista
    lock_equipes = lks_equipes


def carro_f1(dados):
    global controle_pista, lock_equipes
    id_carro, id_equipe = dados

    print(f"Carro #{id_carro} (Escuderia {id_equipe}) está aguardando nos boxes...")

    # Garante que apenas um carro da mesma escuderia entre na pista por vez
    with lock_equipes[id_equipe]:
        # Pede vaga na pista (máximo de 5 carros simultâneos)
        with controle_pista:
            print(f">>> Carro #{id_carro} (Escuderia {id_equipe}) ENTROU NA PISTA!")

            # Cada piloto dá 3 voltas
            for volta in range(1, 4):
                tempo_volta = round(random.uniform(20.0, 35.0), 2)
                time.sleep(0.3)
                print(
                    f"    [Pista] Carro #{id_carro} (Escuderia {id_equipe}) completou a {volta}ª volta em {tempo_volta} segundos."
                )

            print(
                f"<<< Carro #{id_carro} (Escuderia {id_equipe}) SAIU DA PISTA para os boxes."
            )


def main():
    num_escuderias = 7
    carros_por_escuderia = 2
    parametros = []

    id_carro_contador = 1
    # Criando os parâmetros (ID do carro e ID da escuderia) para os 14 carros
    for equipe in range(num_escuderias):
        for _ in range(carros_por_escuderia):
            parametros.append((id_carro_contador, equipe))
            id_carro_contador += 1

    with multiprocessing.Manager() as gerenciador:
        # Máximo de 5 carros simultâneos na pista
        sem_pista = gerenciador.Semaphore(5)

        # Cria um Lock para cada escuderia (para impedir 2 carros da mesma equipe juntos)
        lks_equipes = [gerenciador.Semaphore(1) for _ in range(num_escuderias)]

        # Inicializa o Pool passando os objetos globais via initializer e initargs
        with multiprocessing.Pool(
            processes=6, initializer=init, initargs=(sem_pista, lks_equipes)
        ) as pool:
            pool.map(carro_f1, parametros)

    print("\nFim do Treino de Fórmula 1!")


if __name__ == "__main__":
    main()